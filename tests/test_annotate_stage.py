"""Stage 4: producing a consumer's annotation, and the two diffs that judge it."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from caruca_v2 import cli, llm, v1
from caruca_v2.stages import annotate
from fakes import FakeClient

ANNOTATION = {
    "command": "mkdir",
    "cases": [
        {
            "predicate": "default",
            "pclass": "stateless",
            "inputs": [],
            "outputs": ["stdout"],
            "true_str": "mkdir relpath_1",
        }
    ],
}


def test_a_code_fence_is_stripped_if_the_model_adds_one_anyway():
    body, fenced = annotate.strip_fence('```json\n{"a": 1}\n```')
    assert body == '{"a": 1}'
    assert fenced is True

    plain, not_fenced = annotate.strip_fence('{"a": 1}')
    assert plain == '{"a": 1}'
    assert not_fenced is False


def test_json_comparison_ignores_formatting_but_not_content():
    same = annotate.compare_json('{"a": 1, "b": 2}', '{"b": 2,\n "a": 1}', label="x")
    assert same["structurally_identical"] is True
    assert same["identical"] is False  # the text differs even though the content does not

    different = annotate.compare_json('{"a": 1}', '{"a": 2}', label="x")
    assert different["structurally_identical"] is False


def test_comparison_against_a_missing_reference_is_unavailable_not_zero():
    result = annotate.compare_json('{"a": 1}', None, label="x")
    assert result["available"] is False
    assert "structurally_identical" not in result


def test_text_comparison_reports_diff_shape_not_a_similarity_score():
    result = annotate.compare_text("a\nb\nc\n", "a\nx\nc\n", label="x")
    assert result["identical"] is False
    assert result["diff_lines"] == 2
    assert result["diff_sample"]


def test_format_instructions_come_from_v1s_own_adapters(fake_v1_root: Path):
    schema = v1.annotation_format_definition("pash", "mkdir")
    assert schema["kind"] == "json"
    assert "PaSh" in json.dumps(schema["schema"])

    haskell = v1.annotation_format_definition("shellcheck", "mkdir")
    assert haskell["kind"] == "haskell"
    assert "module Caruca" in haskell["skeleton"]


def test_an_unknown_format_is_rejected_before_anything_runs(fake_v1_root: Path):
    with pytest.raises(Exception, match="unknown annotation format"):
        v1.annotation_format_definition("nonsense", "mkdir")


@pytest.fixture
def invoke(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    def _invoke(response_text: str, *args: str, fmt: str = "pash", **client_kwargs):
        client = FakeClient(response_text, **client_kwargs)
        monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)
        argv = [
            "annotate", fmt, "mkdir",
            *args,
            "--model", "openai/gpt-4o",
            "--temperature", "0.0",
            "--out", str(tmp_path / "runs"),
            "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
        code = cli.main(argv)
        runs = sorted(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
        return code, runs, client

    return _invoke


def read_manifest(run_dir: Path) -> dict:
    return json.loads((run_dir / "manifest.json").read_text())


def test_a_well_formed_annotation_is_written_and_validated(fake_v1_root: Path, invoke):
    code, runs, _ = invoke(json.dumps(ANNOTATION))

    assert code == cli.EXIT_OK
    written = json.loads((runs[0] / "mkdir.pash.annotation").read_text())
    assert written == ANNOTATION

    manifest = read_manifest(runs[0])
    assert manifest["status"] == "ok"
    assert manifest["stage"] == "annotate"
    assert manifest["validation"]["passed"] is True
    assert manifest["checks"]["format"] == "pash"


def test_v1s_own_traces_are_the_default_input(fake_v1_root: Path, invoke):
    _, runs, client = invoke(json.dumps(ANNOTATION))

    source = read_manifest(runs[0])["inputs"]["traces_source"]
    assert source.endswith("caruca/outputs/mkdir.json")
    # The traces themselves reach the prompt, which is the whole point of the A/B.
    assert '"md"' in client.calls[0]["messages"][1]["content"]


def test_both_diffs_are_recorded_and_kept_distinct(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(json.dumps(ANNOTATION))

    comparisons = read_manifest(runs[0])["checks"]["comparisons"]

    # The fake v1 produces exactly this annotation; the ground truth differs by pclass.
    assert comparisons["vs_v1_same_traces"]["structurally_identical"] is True
    assert comparisons["vs_ground_truth"]["structurally_identical"] is False
    # The ground-truth diff must never be presented as the paper's execution-based numbers.
    assert comparisons["vs_ground_truth"]["method"] == "annotation_diff"


def test_the_v1_commit_travels_with_every_comparison(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(json.dumps(ANNOTATION))
    # The fake checkout is not a git repository, so this is honestly null rather than wrong.
    assert "caruca_v1_commit" in read_manifest(runs[0])["inputs"]


def test_no_compare_skips_both_diffs(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(json.dumps(ANNOTATION), "--no-compare")
    assert read_manifest(runs[0])["checks"]["comparisons"] == {}


def test_malformed_output_is_recorded_as_a_result(fake_v1_root: Path, invoke):
    code, runs, client = invoke('{"command": "mkdir"}')  # missing the required `cases`

    assert code == cli.EXIT_RUN_FAILED
    assert len(client.calls) == 1  # never re-asked
    manifest = read_manifest(runs[0])
    assert manifest["validation"]["available"] is True
    assert manifest["validation"]["passed"] is False
    assert (runs[0] / "mkdir.pash.annotation").is_file()


def test_an_empty_response_writes_no_annotation(fake_v1_root: Path, invoke):
    code, runs, _ = invoke("   \n")

    assert code == cli.EXIT_RUN_FAILED
    assert not (runs[0] / "mkdir.pash.annotation").exists()
    assert "no annotation text" in read_manifest(runs[0])["failure_reason"]


def test_the_shellcheck_format_is_haskell_and_checked_more_weakly(fake_v1_root: Path, invoke):
    module = "-- Command: mkdir\nmodule Caruca.DangerousDelete where\ndeletePatterns = [ ]\n"
    code, runs, client = invoke(module, fmt="shellcheck")

    assert code == cli.EXIT_OK
    assert (runs[0] / "mkdir.shellcheck.annotation").is_file()
    assert "module Caruca" in client.calls[0]["messages"][0]["content"]

    manifest = read_manifest(runs[0])
    assert manifest["response_format"] == "haskell"
    # There is no hand-curated ShellCheck ground truth, and that is said rather than scored.
    assert manifest["checks"]["comparisons"]["vs_ground_truth"]["available"] is False


def test_a_traces_override_lets_stage_three_feed_stage_four(
    fake_v1_root: Path, invoke, tmp_path: Path
):
    traces = tmp_path / "from_stage_three.json"
    traces.write_text(json.dumps([{"command": {}, "true_str": "mkdir", "configs": []}]))

    _, runs, _ = invoke(json.dumps(ANNOTATION), "--traces", str(traces))

    assert read_manifest(runs[0])["inputs"]["traces_source"] == str(traces)


def test_every_format_is_reachable_from_the_cli():
    parser = cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            ["annotate", "not-a-format", "mkdir", "--model", "m", "--temperature", "0"]
        )
