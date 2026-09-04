"""Stage 2: parsing the model's output, and diffing it against v1's own enumeration."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from caruca_v2 import cli, llm, v1
from caruca_v2.stages import generate
from fakes import FakeClient

CONFIG = {"name": "mkdir", "body": [], "string": {}, "stdin": "HUMAN_TEXT"}


def jsonl(*invocations: str) -> str:
    return (
        "\n".join(
            json.dumps({"invocation": invocation, "config": {**CONFIG, "name": "mkdir"}})
            for invocation in invocations
        )
        + "\n"
    )


def test_parse_reads_one_object_per_line():
    parsed = generate.parse_jsonl(jsonl("mkdir relpath_1", "mkdir abspath_1"))

    assert parsed.invocations == ["mkdir relpath_1", "mkdir abspath_1"]
    assert parsed.parsed == 2
    assert parsed.unparseable_lines == []
    assert parsed.malformed_objects == 0


def test_a_truncated_final_line_is_dropped_and_counted_not_repaired():
    text = jsonl("mkdir relpath_1") + '{"invocation": "mkdir abs'
    parsed = generate.parse_jsonl(text)

    assert parsed.parsed == 1
    assert len(parsed.unparseable_lines) == 1


def test_an_object_missing_a_required_key_is_counted_as_malformed():
    text = jsonl("mkdir relpath_1") + json.dumps({"invocation": "mkdir x"}) + "\n"
    parsed = generate.parse_jsonl(text)

    assert parsed.parsed == 1
    assert parsed.malformed_objects == 1


def test_prose_around_the_output_does_not_derail_the_parse():
    text = "Here you go:\n" + jsonl("mkdir relpath_1")
    parsed = generate.parse_jsonl(text)

    assert parsed.parsed == 1
    assert len(parsed.unparseable_lines) == 1


def test_comparison_reports_matches_misses_and_spurious_invocations():
    reference = v1.ReferenceInvocations(
        invocations=["a", "b", "c"], count=3, length_hint=99, available=True
    )

    result = generate.compare_invocations(["a", "b", "z"], reference)

    assert result["matched"] == 2
    assert result["missing"] == 1
    assert result["spurious"] == 1
    assert result["recall"] == pytest.approx(2 / 3)
    assert result["precision"] == pytest.approx(2 / 3)
    # v1's own length hint disagrees with its line count; it is reported, never divided by.
    assert result["v1_count"] == 3
    assert result["v1_length_hint"] == 99


def test_comparison_records_unavailability_rather_than_scoring_zero():
    reference = v1.ReferenceInvocations.unavailable("v1 enumeration timed out")

    result = generate.compare_invocations(["a"], reference)

    assert result["available"] is False
    assert "timed out" in result["error"]


def test_the_defaults_mirror_v1s_own_cli_defaults():
    # v1's `--max-arity` default is 1, not the 2 task 002's draft assumed; the paper's
    # "two-flag limit" is `--max-count`, a different knob.
    assert generate.V1_DEFAULT_MAX_ARITY == 1
    assert generate.V1_DEFAULT_MAX_COUNT == 4
    assert generate.V1_DEFAULT_STDIN == "simple"
    assert generate.V1_DEFAULT_CONTENT == "simple"


@pytest.fixture
def invoke(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    def _invoke(response_text: str, *args: str, **client_kwargs):
        client = FakeClient(response_text, **client_kwargs)
        monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)
        argv = [
            "generate",
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


def test_a_successful_run_writes_both_output_files(fake_v1_root: Path, invoke, tmp_path: Path):
    code, runs, _ = invoke(jsonl("mkdir relpath_1", "mkdir abspath_1"), "mkdir")

    assert code == cli.EXIT_OK
    run_dir = runs[0]

    lines = (run_dir / "mkdir.invocations.txt").read_text().splitlines()
    assert lines == ["mkdir relpath_1", "mkdir abspath_1"]

    configs = json.loads((run_dir / "mkdir.configs.json").read_text())
    assert len(configs) == 2

    manifest = read_manifest(run_dir)
    assert manifest["status"] == "ok"
    assert manifest["stage"] == "generate"
    assert manifest["component"] == "llm_pipeline"
    assert manifest["validation"]["passed"] is True
    assert manifest["validation"]["elements"] == 2


def test_the_prompt_carries_v1s_value_table_and_the_stated_bounds(fake_v1_root: Path, invoke):
    _, _, client = invoke(jsonl("mkdir relpath_1"), "mkdir", "--max-arity", "3")

    user_message = client.calls[0]["messages"][1]["content"]
    system_message = client.calls[0]["messages"][0]["content"]

    # The spec names types; the values they stand for come from v1's DSL at runtime.
    assert '"*.txt"' in user_message
    assert "relpath_1" in user_message
    assert "at most 3 time(s)" in user_message
    assert "CommandConfig" in system_message


def test_the_invocation_set_diff_against_v1_is_recorded(fake_v1_root: Path, invoke):
    # The fake v1 emits three invocations; the model gets two right and invents one.
    _, runs, _ = invoke(jsonl("mkdir relpath_1", "mkdir abspath_1", "mkdir --invented"), "mkdir")

    comparison = read_manifest(runs[0])["checks"]["invocation_comparison"]
    assert comparison["available"] is True
    assert comparison["v1_count"] == 3
    assert comparison["matched"] == 2
    assert comparison["missing"] == 1
    assert comparison["spurious"] == 1
    assert comparison["v1_length_hint"] == 99


def test_no_compare_skips_v1s_enumeration_and_says_so(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(jsonl("mkdir relpath_1"), "mkdir", "--no-compare")

    comparison = read_manifest(runs[0])["checks"]["invocation_comparison"]
    assert comparison["available"] is False


def test_continuation_happens_only_when_the_token_cap_cut_the_response(
    fake_v1_root: Path, invoke
):
    _, runs, client = invoke(jsonl("mkdir relpath_1"), "mkdir", finish_reason="length")

    manifest = read_manifest(runs[0])
    assert manifest["turns"] == 4  # the default cap
    assert len(client.calls) == 4
    assert manifest["checks"]["parse"]["hit_turn_cap_while_truncated"] is True
    assert client.calls[1]["messages"][-1]["content"] == llm.CONTINUE_INSTRUCTION


def test_a_model_that_stops_on_its_own_is_never_asked_for_more(fake_v1_root: Path, invoke):
    _, runs, client = invoke(jsonl("mkdir relpath_1"), "mkdir")

    assert len(client.calls) == 1
    assert read_manifest(runs[0])["checks"]["parse"]["hit_turn_cap_while_truncated"] is False


def test_every_turn_gets_its_own_sidecar_and_metrics_row(
    fake_v1_root: Path, invoke, tmp_path: Path
):
    _, runs, _ = invoke(jsonl("mkdir relpath_1"), "mkdir", finish_reason="length")

    sidecars = sorted(runs[0].glob("*.telemetry.json"))
    assert [path.name for path in sidecars] == [
        f"mkdir.turn-{turn:02d}.telemetry.json" for turn in range(4)
    ]

    with sqlite3.connect(tmp_path / "metrics.db") as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT turn FROM runs ORDER BY turn").fetchall()
    assert [row["turn"] for row in rows] == [0, 1, 2, 3]

    manifest = read_manifest(runs[0])
    # Totals are summed across turns, not taken from the last one.
    assert manifest["prompt_tokens"] == 6842 * 4
    assert manifest["cost_usd"] == pytest.approx(0.0213 * 4)


def test_unusable_output_fails_without_writing_output_files(fake_v1_root: Path, invoke):
    code, runs, client = invoke("I am afraid I cannot enumerate that.\n", "mkdir")

    assert code == cli.EXIT_RUN_FAILED
    assert len(client.calls) == 1
    assert not (runs[0] / "mkdir.invocations.txt").exists()
    manifest = read_manifest(runs[0])
    assert manifest["status"] == "failed"
    assert "no usable output" in manifest["failure_reason"]


def test_configs_v1_rejects_are_recorded_as_a_result(fake_v1_root: Path, invoke):
    bad = json.dumps({"invocation": "mkdir x", "config": {"body": []}}) + "\n"
    code, runs, _ = invoke(bad, "mkdir")

    assert code == cli.EXIT_RUN_FAILED
    manifest = read_manifest(runs[0])
    assert manifest["validation"]["available"] is True
    assert manifest["validation"]["passed"] is False
    assert manifest["validation"]["error"]
    # The rejected output is kept: it is the finding.
    assert (runs[0] / "mkdir.configs.json").is_file()


def test_the_spec_override_lets_the_two_stages_be_chained(
    fake_v1_root: Path, invoke, tmp_path: Path
):
    spec = tmp_path / "generated_spec.py"
    spec.write_text("mkdir_syntax_spec = ['from a task 001 run']\n")

    _, runs, client = invoke(jsonl("mkdir relpath_1"), "mkdir", "--spec", str(spec))

    assert "from a task 001 run" in client.calls[0]["messages"][1]["content"]
    assert read_manifest(runs[0])["inputs"]["spec_source"] == str(spec)


def test_the_knobs_used_are_recorded_so_the_v1_side_can_match_them(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(
        jsonl("mkdir relpath_1"), "mkdir",
        "--max-arity", "2", "--max-count", "3", "--stdin", "varied", "--content", "split",
    )

    inputs = read_manifest(runs[0])["inputs"]
    assert inputs["max_arity"] == 2
    assert inputs["max_count"] == 3
    assert inputs["stdin_variation"] == "varied"
    assert inputs["content_variation"] == "split"
