"""Stage 3: the workspace, the agent loop, and the v1-compatible traces file."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from caruca_v2 import cli, llm, v1, workspace
from caruca_v2.stages import trace as trace_stage
from fakes import ScriptedClient, tool_call

CONFIG = {
    "name": "cat",
    "body": [{"flag": None, "args": ["relpath_1"]}],
    "string": {"name": "cat", "body": [{"flag": None, "args": ["relpath_1"]}]},
    "stdin": "HUMAN_TEXT",
}

REPORT = {
    "interactions": [
        {"action": "rf", "path": "relpath_1"},
        {"action": "wf", "path": "stdout"},
    ],
    "return_code": 0,
    "stdout": "fixture\n",
    "stderr": "",
}


def session(*, report=REPORT) -> list:
    """A well-behaved session: look, run, report."""
    return [
        [tool_call("list_dir", {"path": "."}, "c1")],
        [tool_call("run_command", {"argv": ["cat", "relpath_1"]}, "c2")],
        [tool_call("report_observations", report, "c3")],
    ]


def test_the_workspace_is_built_by_v1_not_reimplemented(fake_v1_root: Path):
    with workspace.materialize(CONFIG) as space:
        assert (space.sandbox / "relpath_1").is_file()
        assert space.listing == ["relpath_1"]
        assert space.invocation == "cat relpath_1"
        assert space.stdin_name == "HUMAN_TEXT"
        assert space.stdin_bytes == b"standard input\n"
        root = space.root

    # It is a throwaway: nothing is left behind.
    assert not root.exists()


def test_keeping_the_workspace_leaves_it_in_place(fake_v1_root: Path):
    with workspace.materialize(CONFIG, keep=True) as space:
        root = space.root
    assert root.exists()


def test_a_config_v1_cannot_prepare_raises_rather_than_producing_an_empty_workspace(
    fake_v1_root: Path,
):
    with pytest.raises(workspace.MaterializationFailure):
        with workspace.materialize({"not": "a config"}):
            pass


def test_absolute_paths_are_rewritten_into_v1s_sandbox_namespace(fake_v1_root: Path):
    with workspace.materialize(CONFIG) as space:
        rewritten = space.rewrite(str(space.sandbox / "relpath_1"))

        # v1's annotator hardcodes this prefix, so a traces file has to use it.
        assert rewritten == f"{v1.PLACEHOLDER_SANDBOX}/relpath_1"
        # Relative paths and stream names pass through, as they do in v1.
        assert space.rewrite("relpath_1") == "relpath_1"
        assert space.rewrite("stdout") == "stdout"
        # A path outside the workspace is left alone rather than forced into the namespace.
        assert space.rewrite("/usr/bin/cat") == "/usr/bin/cat"


def test_unknown_interaction_actions_are_dropped_not_coerced(fake_v1_root: Path):
    with workspace.materialize(CONFIG) as space:
        pairs, rejected = trace_stage.normalize_interactions(
            [
                {"action": "rf", "path": "relpath_1"},
                {"action": "opened", "path": "relpath_1"},
                {"action": "wf"},
            ],
            space,
        )

    assert pairs == [["rf", "relpath_1"]]
    assert len(rejected) == 2
    assert "unknown action" in rejected[0]["reason"]


@pytest.fixture
def invoke(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    def _invoke(turns: list, *args: str, configs=None):
        client = ScriptedClient(turns)
        monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)

        configs_path = tmp_path / "configs.json"
        configs_path.write_text(json.dumps(configs if configs is not None else [CONFIG]))

        argv = [
            "trace", "cat",
            "--configs", str(configs_path),
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


def test_a_session_produces_a_traces_file_v1_accepts(fake_v1_root: Path, invoke):
    code, runs, _ = invoke(session())

    assert code == cli.EXIT_OK
    traces = json.loads((runs[0] / "cat.traces.json").read_text())

    assert len(traces) == 1
    assert traces[0]["true_str"] == "cat relpath_1"
    entry = traces[0]["configs"][0]
    assert entry["return_code"] == 0
    assert entry["traces"] == [["rf", "relpath_1"], ["wf", "stdout"]]

    manifest = read_manifest(runs[0])
    assert manifest["status"] == "ok"
    assert manifest["validation"]["passed"] is True
    assert manifest["stage"] == "trace"


def test_the_loop_stops_as_soon_as_the_report_arrives(fake_v1_root: Path, invoke):
    _, runs, client = invoke(session())

    assert len(client.calls) == 3
    sessions = read_manifest(runs[0])["checks"]["sessions"]
    assert sessions[0]["stop_reason"] == "finished"
    assert sessions[0]["executions"] == 1


def test_a_session_that_never_reports_is_recorded_as_such(fake_v1_root: Path, invoke):
    code, runs, _ = invoke([[tool_call("list_dir", {"path": "."}, "c1")]], "--max-turns", "3")

    assert code == cli.EXIT_RUN_FAILED
    manifest = read_manifest(runs[0])
    session_record = manifest["checks"]["sessions"][0]
    assert session_record["status"] == "no_report"
    assert session_record["stop_reason"] == "turn_cap"
    assert session_record["turns"] == 3
    assert "no configuration produced a usable observation report" in manifest["failure_reason"]


def test_a_refused_tool_call_is_counted_and_the_session_continues(fake_v1_root: Path, invoke):
    turns = [
        [tool_call("run_command", {"argv": ["ls", "-la"]}, "c1")],
        [tool_call("run_command", {"argv": ["cat", "relpath_1"]}, "c2")],
        [tool_call("report_observations", REPORT, "c3")],
    ]
    code, runs, _ = invoke(turns)

    assert code == cli.EXIT_OK
    manifest = read_manifest(runs[0])
    assert manifest["checks"]["refused_calls"] == 1

    audit = manifest["checks"]["tool_audit"][0]["calls"]
    assert audit[0]["allowed"] is False
    assert "only `cat` may be run" in audit[0]["reason"]


def test_the_limit_is_the_cost_brake(fake_v1_root: Path, invoke):
    _, runs, client = invoke(session(), "--limit", "2", configs=[CONFIG, CONFIG, CONFIG])

    configs = read_manifest(runs[0])["checks"]["configs"]
    assert configs["available"] == 3
    assert configs["attempted"] == 2
    assert configs["reported"] == 2
    assert len(client.calls) == 6  # three turns per configuration


def test_every_turn_of_every_session_gets_a_telemetry_record(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(session(), "--limit", "2", configs=[CONFIG, CONFIG])

    sidecars = sorted((runs[0]).glob("*.telemetry.json"))
    assert len(sidecars) == 6

    manifest = read_manifest(runs[0])
    assert manifest["turns"] == 6
    assert manifest["prompt_tokens"] == 6842 * 6


def test_each_session_records_the_hash_of_its_own_prompt(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(session())

    sessions = read_manifest(runs[0])["checks"]["sessions"]
    assert len(sessions[0]["prompt_hash"]) == 64

    sidecar = next(runs[0].glob("*.telemetry.json"))
    assert json.loads(sidecar.read_text())["prompt_hash"] == sessions[0]["prompt_hash"]


def test_the_prompt_states_the_allowlist_and_the_starting_listing(fake_v1_root: Path, invoke):
    _, _, client = invoke(session())

    system = client.calls[0]["messages"][0]["content"]
    user = client.calls[0]["messages"][1]["content"]

    assert "You may run `cat` and nothing else" in system
    assert "cat relpath_1" in user
    assert "relpath_1" in user
    assert "HUMAN_TEXT" in user


def test_v1s_execution_environment_is_recorded_with_the_run(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(session())

    inputs = read_manifest(runs[0])["inputs"]
    assert inputs["execution_env"] == {
        "PATH": "/usr/bin:/bin:/usr/local/sbin:/usr/local/bin",
        "SHELL": "/bin/sh",
    }
    assert inputs["execution_timeout_seconds"] == 2
    assert inputs["isolation"] == "host"


def test_tracing_a_destructive_command_on_the_host_is_refused_before_any_model_call(
    fake_v1_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    client = ScriptedClient(session())
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)
    configs_path = tmp_path / "configs.json"
    configs_path.write_text(json.dumps([CONFIG]))

    code = cli.main(
        [
            "trace", "rm",
            "--configs", str(configs_path),
            "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    assert code == cli.EXIT_SETUP_ERROR
    assert client.calls == []
    assert not (tmp_path / "runs").exists()


def test_conversation_logging_captures_tool_calls_and_results(fake_v1_root: Path, invoke):
    _, runs, _ = invoke(session(), "--log-conversation")

    lines = [
        json.loads(line)
        for line in (runs[0] / "conversation.jsonl").read_text().splitlines()
    ]
    roles = [line["role"] for line in lines]

    assert roles[:2] == ["system", "user"]
    assert "tool" in roles
    assert all(line["config_index"] == 0 for line in lines)
    # The executor's answer to the model is in the log verbatim.
    assert any("fixture" in (line.get("content") or "") for line in lines if line["role"] == "tool")
