"""Regressions for the seven defects found in the 2026-09-03 code review.

Each test names the defect it pins down. They exist because every one of these was a
silent divergence: the code ran, produced output, and was wrong in a way that would only
have shown up as an unexplained v1/v2 disagreement in the eventual comparison.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
from pathlib import Path

import pytest

from caruca_v2 import cli, llm, telemetry, tools, workspace
from caruca_v2 import ui as ui_module
from caruca_v2.workspace import Workspace
from conftest import CARUCA_ARGV_LOG
from fakes import FakeClient, ScriptedClient, tool_call


def make_workspace(tmp_path: Path) -> Workspace:
    root = tmp_path / "toplevel"
    sandbox = root / "sandbox_inner"
    sandbox.mkdir(parents=True)
    (sandbox / "relpath_1").write_text("inside\n")
    stdin_path = root / "stdin"
    stdin_path.write_bytes(b"")
    scratch = root / "tmp"
    scratch.mkdir()
    (tmp_path / "OUTSIDE.txt").write_text("outside the workspace\n")
    return Workspace(
        root=root,
        sandbox=sandbox,
        stdin_path=stdin_path,
        scratch=scratch,
        invocation="cat relpath_1",
        stdin_name="HUMAN_TEXT",
        listing=["relpath_1"],
    )


# --- Defect 4: the path jail admitted relative traversal ----------------------------


@pytest.mark.parametrize(
    "argument",
    [
        "../OUTSIDE.txt",
        "../../OUTSIDE.txt",
        "./../OUTSIDE.txt",
        "subdir/../../OUTSIDE.txt",
        "../" * 12 + "etc/hosts",
    ],
)
def test_relative_traversal_in_an_argument_is_refused(tmp_path: Path, argument: str):
    # `run_command` sets cwd to the workspace, so a relative escape works exactly as well
    # as an absolute one. Only absolute arguments used to be checked.
    executor = tools.ToolExecutor(command="cat", workspace=make_workspace(tmp_path))

    result = executor.execute("run_command", {"argv": ["cat", argument]})

    assert "refused" in result["error"], f"{argument} escaped the jail"
    assert executor.executions == 0


def test_an_absolute_traversal_is_still_refused(tmp_path: Path):
    space = make_workspace(tmp_path)
    executor = tools.ToolExecutor(command="cat", workspace=space)

    result = executor.execute("run_command", {"argv": ["cat", str(tmp_path / "OUTSIDE.txt")]})

    assert "refused" in result["error"]


def test_non_path_arguments_are_not_refused_by_the_stricter_check(tmp_path: Path):
    # The stricter rule must not start rejecting ordinary flags and values.
    executor = tools.ToolExecutor(command="cat", workspace=make_workspace(tmp_path))

    for argv in (["cat", "-n", "relpath_1"], ["cat", "--number", "relpath_1"], ["cat"]):
        result = executor.execute("run_command", {"argv": argv})
        assert "error" not in result, f"{argv} was wrongly refused: {result}"


def test_a_permission_error_is_never_swallowed_by_the_unresolvable_path_branch(
    tmp_path: Path,
):
    # `PermissionError` subclasses `OSError`; catching OSError around the resolve call
    # without re-raising would silently disable the whole jail.
    executor = tools.ToolExecutor(command="cat", workspace=make_workspace(tmp_path))
    result = executor.execute("run_command", {"argv": ["cat", "../OUTSIDE.txt"]})
    assert result["error"].startswith("refused:")


# --- Defect 1: the traced command inherited the full process environment -------------


def test_the_traced_command_sees_only_v1s_environment(tmp_path: Path, monkeypatch):
    # v1 builds its env from scratch and never inherits. Inherited LANG/LC_ALL change what
    # ls, sort, wc and date do, which would surface later as a fake v1/v2 disagreement.
    monkeypatch.setenv("LC_ALL", "en_US.UTF-8")
    monkeypatch.setenv("CARUCA_V2_LEAK_CANARY", "leaked")

    space = make_workspace(tmp_path)
    executor = tools.ToolExecutor(command="env", workspace=space)
    result = executor.execute("run_command", {"argv": ["env"]})

    seen = {
        line.split("=", 1)[0]
        for line in result["stdout"].splitlines()
        if "=" in line
    }
    assert seen == {"PATH", "SHELL", "TMPDIR"}, seen
    assert "CARUCA_V2_LEAK_CANARY" not in result["stdout"]
    assert "LC_ALL" not in result["stdout"]


def test_the_environment_values_are_v1s_own_constants(tmp_path: Path):
    space = make_workspace(tmp_path)
    environment = tools._execution_env(space)

    assert environment["PATH"] == "/usr/bin:/bin:/usr/local/sbin:/usr/local/bin"
    assert environment["SHELL"] == "/bin/sh"
    # v1 points TMPDIR at scratch space outside the sandbox, so it never shows up in a
    # listing the command can see.
    assert environment["TMPDIR"] == str(space.scratch)
    assert not Path(environment["TMPDIR"]).is_relative_to(space.sandbox)


# --- Defect 3: --isolation lima could not work --------------------------------------


def test_the_lima_backend_puts_workspaces_where_the_vm_can_see_them():
    backend = tools.IsolationBackend.lima("caruca")
    # The VM mounts only the home directory, at the same path. The platform temp dir
    # (/var/folders/... on macOS) does not exist inside the guest at all.
    assert backend.workspace_root is not None
    assert backend.workspace_root.is_relative_to(Path.home())
    assert not Path(tempfile.gettempdir()).is_relative_to(Path.home())


def test_the_host_backend_leaves_the_workspace_location_alone():
    assert tools.IsolationBackend("host", []).workspace_root is None


def test_materialize_honours_the_backend_workspace_root(fake_v1_root: Path, tmp_path: Path):
    root_dir = tmp_path / "home_like"
    config = {"name": "cat", "body": [], "string": {}, "stdin": "HUMAN_TEXT"}

    with workspace.materialize(config, root_dir=root_dir) as space:
        assert space.root.is_relative_to(root_dir)
        assert space.sandbox.is_dir()
        assert space.scratch.is_dir()


def test_the_isolated_command_sets_its_own_directory_and_environment(tmp_path: Path):
    space = make_workspace(tmp_path)
    backend = tools.IsolationBackend.lima("caruca")

    command = tools._remote_command(["cat", "relpath_1"], space, backend)

    assert command[:4] == ["limactl", "shell", "caruca", "--"]
    script = command[-1]
    # cwd and env are set on the far side rather than inherited from the guest shell.
    assert script.startswith(f"cd {space.sandbox}")
    assert "env -i" in script
    assert "PATH=/usr/bin:/bin:/usr/local/sbin:/usr/local/bin" in script
    assert "SHELL=/bin/sh" in script


def test_the_isolated_command_quotes_paths_with_spaces(tmp_path: Path):
    space = make_workspace(tmp_path)
    odd = space.sandbox / "a file"
    command = tools._remote_command(["cat", str(odd)], space, tools.IsolationBackend.lima())
    assert "'" in command[-1]


# --- Defect 2: the v1 reference run ignored --max-count and --skip -------------------


def test_the_reference_enumeration_receives_every_bound_the_prompt_stated(
    fake_v1_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    client = FakeClient(
        json.dumps({"invocation": "mkdir relpath_1", "config": {"name": "mkdir"}}) + "\n"
    )
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)

    cli.main(
        [
            "generate", "mkdir",
            "--max-arity", "2", "--max-count", "3", "--skip=--version,--help",
            "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    invoked = (fake_v1_root / CARUCA_ARGV_LOG).read_text()
    assert "--max-arity 2" in invoked
    # Without these, `mkdir` yields 44 invocations at --max-count 1 and 4,240 at 4, so the
    # set-diff would be measuring the mismatch in bounds rather than the model.
    assert "--max-count 3" in invoked
    assert "--skip --version,--help" in invoked


def test_a_bare_skip_means_exactly_what_v1s_bare_skip_means():
    args = cli.build_parser().parse_args(
        ["generate", "mkdir", "--skip", "--model", "m", "--temperature", "0"]
    )
    assert args.skip == "--version,--help,--interactive"


def test_nothing_is_skipped_by_default_as_in_v1(
    fake_v1_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    client = FakeClient(
        json.dumps({"invocation": "mkdir relpath_1", "config": {"name": "mkdir"}}) + "\n"
    )
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: client)

    cli.main(
        [
            "generate", "mkdir",
            "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    assert "--skip" not in (fake_v1_root / CARUCA_ARGV_LOG).read_text()
    assert "--max-count 4" in (fake_v1_root / CARUCA_ARGV_LOG).read_text()


# --- Defect 5: per-configuration cost was not attributable --------------------------


CONFIG = {
    "name": "cat",
    "body": [{"flag": None, "args": ["relpath_1"]}],
    "string": {"name": "cat", "body": [{"flag": None, "args": ["relpath_1"]}]},
    "stdin": "HUMAN_TEXT",
}
REPORT = {
    "interactions": [{"action": "rf", "path": "relpath_1"}],
    "return_code": 0,
    "stdout": "",
    "stderr": "",
}


def test_every_turn_names_the_configuration_it_belongs_to(
    fake_v1_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    turns = [
        [tool_call("run_command", {"argv": ["cat", "relpath_1"]}, "c1")],
        [tool_call("report_observations", REPORT, "c2")],
    ]
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: ScriptedClient(turns))
    configs_path = tmp_path / "configs.json"
    configs_path.write_text(json.dumps([CONFIG, CONFIG]))

    cli.main(
        [
            "trace", "cat", "--configs", str(configs_path), "--limit", "2",
            "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    run_dir = next(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
    indices = [
        json.loads(path.read_text())["config_index"]
        for path in sorted(run_dir.glob("*.telemetry.json"))
    ]
    assert indices == [0, 0, 1, 1]

    with sqlite3.connect(tmp_path / "metrics.db") as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT config_index FROM runs ORDER BY turn").fetchall()
    assert [row["config_index"] for row in rows] == [0, 0, 1, 1]


def test_cost_is_totalled_per_configuration(
    fake_v1_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    turns = [
        [tool_call("run_command", {"argv": ["cat", "relpath_1"]}, "c1")],
        [tool_call("report_observations", REPORT, "c2")],
    ]
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: ScriptedClient(turns))
    configs_path = tmp_path / "configs.json"
    configs_path.write_text(json.dumps([CONFIG]))

    cli.main(
        [
            "trace", "cat", "--configs", str(configs_path),
            "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )

    run_dir = next(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
    session = json.loads((run_dir / "manifest.json").read_text())["checks"]["sessions"][0]

    assert session["turns"] == 2
    assert session["prompt_tokens"] == 6842 * 2
    assert session["completion_tokens"] == 1103 * 2
    assert session["cost_usd"] == pytest.approx(0.0213 * 2)
    assert session["wall_clock_seconds"] > 0


def test_config_index_is_absent_rather_than_faked_for_single_session_stages(
    fake_v1_root: Path, valid_spec_response: str, monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    monkeypatch.setattr(llm, "build_client", lambda *a, **k: FakeClient(valid_spec_response))
    cli.main(
        [
            "naive-llm", "mkdir", "--model", "openai/gpt-4o", "--temperature", "0.0",
            "--out", str(tmp_path / "runs"), "--db", str(tmp_path / "metrics.db"),
            "--plain",
        ]
    )
    run_dir = next(p for p in (tmp_path / "runs").glob("*") if p.is_dir())
    sidecar = json.loads(next(run_dir.glob("*.telemetry.json")).read_text())
    assert sidecar["config_index"] is None


# --- Defect 6: run-id entropy was 16 bits, and a collision crashed the run -----------


def test_many_runs_in_the_same_second_do_not_collide(tmp_path: Path):
    # 2 bytes collided for ~7% of batches of 100 and ~71% of batches of 400, and a
    # collision raised an uncaught FileExistsError.
    ids = {telemetry.create_run_directory(tmp_path, "mkdir").run_id for _ in range(400)}
    assert len(ids) == 400


def test_a_collision_is_retried_rather_than_crashing(tmp_path: Path, monkeypatch):
    # Force the first draw to repeat an existing directory name.
    draws = iter(["dead", "dead", "beef"])
    monkeypatch.setattr(telemetry.secrets, "token_hex", lambda n: next(draws))

    first = telemetry.create_run_directory(tmp_path, "mkdir")
    second = telemetry.create_run_directory(tmp_path, "mkdir")

    assert first.run_id.endswith("_dead")
    assert second.run_id.endswith("_beef")
    assert first.path.is_dir() and second.path.is_dir()


def test_a_reused_directory_is_never_silently_accepted(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(telemetry.secrets, "token_hex", lambda n: "same")
    telemetry.create_run_directory(tmp_path, "mkdir")

    # Evidence must never be overwritten; exhausting the retries is an error, not a reuse.
    with pytest.raises(Exception, match="could not find an unused run directory"):
        telemetry.create_run_directory(tmp_path, "mkdir")


# --- Defect 7: the summary mangled bracket-containing invocations -------------------


@pytest.mark.parametrize(
    "invocation",
    ["test [ -f relpath_1 ]", "find . -name '[a-z]*'", "cat a[/]b", "sed 's/[abc]//'"],
)
def test_invocations_containing_brackets_are_displayed_verbatim(invocation: str, capsys):
    import io
    import re

    stream = io.StringIO()
    stream.isatty = lambda: True
    ui = ui_module.UI(plain=False, stream=stream)

    # `[a-z]` used to be swallowed as a style tag and `[/]` used to raise MarkupError
    # part-way through a run.
    ui.detail("config 1/1", ui_module.compose(invocation, " — ", ui.verdict(True, "ok", "no")))

    rendered = re.sub(r"\x1b\[[0-9;]*m", "", stream.getvalue())
    assert invocation in rendered


def test_a_summary_table_also_escapes_its_values():
    import io
    import re

    stream = io.StringIO()
    stream.isatty = lambda: True
    ui = ui_module.UI(plain=False, stream=stream)
    ui.summary("trace test", [("spec", ui_module.compose("weird [a-z] name"))])

    rendered = re.sub(r"\x1b\[[0-9;]*m", "", stream.getvalue())
    assert "[a-z]" in rendered
