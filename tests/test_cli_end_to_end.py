"""The whole `naive-llm` path with the model mocked: files on disk, row in the database.

Also the guardrail tests. "Exactly one call, never re-asked" is the defining property of
the naive control, so it is asserted rather than assumed.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from caruca_v2 import cli, llm
from fakes import FakeClient


@pytest.fixture
def invoke(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Run the CLI against a fake client, returning (exit code, run dirs, client)."""

    def _invoke(
        response_text: str, *args: str, **client_kwargs
    ) -> tuple[int, list[Path], FakeClient]:
        client = FakeClient(response_text, **client_kwargs)
        monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)
        argv = [
            "naive-llm",
            *args,
            "--model",
            "openai/gpt-4o",
            "--temperature",
            "0.0",
            "--out",
            str(tmp_path / "runs"),
            "--db",
            str(tmp_path / "metrics.db"),
            "--plain",
        ]
        code = cli.main(argv)
        runs = sorted(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
        return code, runs, client

    return _invoke


def read_manifest(run_dir: Path) -> dict:
    return json.loads((run_dir / "manifest.json").read_text())


def test_a_successful_run_writes_spec_sidecar_and_manifest(
    fake_v1_root: Path, valid_spec_response: str, invoke, tmp_path: Path
):
    code, runs, client = invoke(valid_spec_response, "mkdir")

    assert code == cli.EXIT_OK
    assert len(runs) == 1
    run_dir = runs[0]

    assert (run_dir / "mkdir.py").is_file()
    assert "mkdir_syntax_spec" in (run_dir / "mkdir.py").read_text()

    sidecar = json.loads((run_dir / "mkdir.telemetry.json").read_text())
    assert sidecar["component"] == "naive_llm"
    assert sidecar["condition"] == "plain"
    assert sidecar["stage"] == "syntax_spec"
    assert sidecar["prompt_tokens"] == 6842
    assert sidecar["completion_tokens"] == 1103
    assert sidecar["cost_usd"] == 0.0213
    assert sidecar["seed"] == 42
    assert sidecar["decoding_params"] == {"temperature": 0.0, "max_tokens": 4096}
    assert len(sidecar["prompt_hash"]) == 64

    manifest = read_manifest(run_dir)
    assert manifest["status"] == "ok"
    assert manifest["validation"]["passed"] is True
    assert manifest["validation"]["available"] is True
    assert manifest["inputs"]["exemplar_commands"] == ["touch", "rm", "mv", "ls"]
    assert manifest["inputs"]["output_fenced"] is True


def test_the_run_appends_exactly_one_row_to_the_metrics_database(
    fake_v1_root: Path, valid_spec_response: str, invoke, tmp_path: Path
):
    invoke(valid_spec_response, "mkdir")

    with sqlite3.connect(tmp_path / "metrics.db") as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM runs").fetchall()

    assert len(rows) == 1
    assert rows[0]["command"] == "mkdir"
    assert rows[0]["validation_passed"] == 1
    assert rows[0]["model_id"] == "openai/gpt-4o"


def test_exactly_one_model_call_is_made(
    fake_v1_root: Path, valid_spec_response: str, invoke
):
    _, _, client = invoke(valid_spec_response, "mkdir")
    assert len(client.calls) == 1


def test_an_invalid_spec_is_recorded_and_never_re_asked(fake_v1_root: Path, invoke):
    code, runs, client = invoke("```python\nthis is not python(\n```\n", "mkdir")

    assert code == cli.EXIT_RUN_FAILED
    assert len(client.calls) == 1

    manifest = read_manifest(runs[0])
    assert manifest["status"] == "failed"
    assert manifest["validation"]["available"] is True
    assert manifest["validation"]["passed"] is False
    assert "SyntaxError" in manifest["validation"]["error"]
    # The unusable output is kept verbatim: it is the finding.
    assert "this is not python(" in manifest["raw_response"]


def test_a_response_with_no_fence_falls_back_to_the_raw_text_as_v1_does(
    fake_v1_root: Path, invoke
):
    code, runs, _ = invoke("mkdir_syntax_spec = [[[('-a',)], [('PATH',)]]]\n", "mkdir")

    manifest = read_manifest(runs[0])
    assert manifest["inputs"]["output_fenced"] is False
    assert code == cli.EXIT_OK


def test_an_empty_response_fails_without_writing_a_spec_file(fake_v1_root: Path, invoke):
    code, runs, _ = invoke("   \n", "mkdir")

    assert code == cli.EXIT_RUN_FAILED
    assert not (runs[0] / "mkdir.py").exists()
    manifest = read_manifest(runs[0])
    assert manifest["status"] == "failed"
    assert manifest["validation"] is None
    assert "no specification text" in manifest["failure_reason"]


def test_a_truncated_response_is_flagged_not_retried(
    fake_v1_root: Path, valid_spec_response: str, invoke
):
    _, runs, client = invoke(valid_spec_response, "mkdir", finish_reason="length")

    manifest = read_manifest(runs[0])
    assert manifest["output_truncated"] is True
    assert manifest["finish_reason"] == "length"
    assert len(client.calls) == 1


def test_conversation_logging_is_off_by_default_and_verbatim_when_on(
    fake_v1_root: Path, valid_spec_response: str, invoke
):
    _, first, _ = invoke(valid_spec_response, "mkdir")
    assert not (first[0] / "conversation.jsonl").exists()

    # Two runs can start in the same second, so the new directory is found by difference
    # rather than by sort order.
    _, both, _ = invoke(valid_spec_response, "mkdir", "--log-conversation")
    logged = next(run for run in both if run not in first)
    log = (logged / "conversation.jsonl").read_text().splitlines()
    lines = [json.loads(line) for line in log]
    assert [message["role"] for message in lines] == ["system", "user", "assistant"]
    assert "MKDIR(1)" in lines[1]["content"]


def test_docs_override_replaces_the_v1_man_page(
    fake_v1_root: Path, valid_spec_response: str, invoke, tmp_path: Path
):
    docs = tmp_path / "custom.txt"
    docs.write_text("CUSTOM DOCUMENTATION FOR MKDIR")

    _, runs, client = invoke(valid_spec_response, "mkdir", "--docs", str(docs))

    assert "CUSTOM DOCUMENTATION FOR MKDIR" in client.calls[0]["messages"][1]["content"]
    assert read_manifest(runs[0])["inputs"]["docs_source"] == str(docs)


def test_multi_word_commands_use_v1s_filename_convention(
    fake_v1_root: Path, invoke
):
    response = "```python\ngit_commit_syntax_spec = [[[('-a',)], [('PATH',)]]]\n```\n"
    code, runs, _ = invoke(response, "git", "commit")

    assert code == cli.EXIT_OK
    assert (runs[0] / "git_commit.py").is_file()
    assert (runs[0] / "git_commit.telemetry.json").is_file()
    assert read_manifest(runs[0])["command"] == "git commit"


def test_a_provider_that_ignores_seed_is_flagged_honestly(
    fake_v1_root: Path, valid_spec_response: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    client = FakeClient(valid_spec_response)
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)

    cli.main(
        [
            "naive-llm", "mkdir",
            "--model", "anthropic/claude-sonnet-4",
            "--temperature", "0.0",
            "--out", str(tmp_path / "runs"),
            "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    run_dir = next(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
    manifest = read_manifest(run_dir)
    assert manifest["seed"] == 42
    assert manifest["seed_honored"] is False


def test_a_missing_v1_checkout_exits_with_the_setup_code(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, valid_spec_response: str
):
    monkeypatch.setenv("CARUCA_V1_ROOT", str(tmp_path / "absent"))
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: FakeClient(valid_spec_response))

    code = cli.main(
        [
            "naive-llm", "mkdir",
            "--model", "openai/gpt-4o",
            "--temperature", "0.0",
            "--out", str(tmp_path / "runs"),
            "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    assert code == cli.EXIT_SETUP_ERROR
    # Nothing failed halfway: a misconfigured run leaves no directory behind.
    assert not (tmp_path / "runs").exists()


def test_metrics_rebuild_reproduces_the_database_from_the_run_directories(
    fake_v1_root: Path, valid_spec_response: str, invoke, tmp_path: Path
):
    invoke(valid_spec_response, "mkdir")
    db_path = tmp_path / "metrics.db"
    db_path.unlink()

    code = cli.main(
        ["metrics", "rebuild", "--out", str(tmp_path / "runs"), "--db", str(db_path), "--plain"]
    )

    assert code == cli.EXIT_OK
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("SELECT count(*) FROM runs").fetchone()[0] == 1
