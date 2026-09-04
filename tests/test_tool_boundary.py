"""The safety boundary for stage 3, tested before any model is connected to it.

This is the only place in the project where a model's choice reaches a real shell. The
prompt asks; this module's rules are what actually hold, so they are tested directly
rather than through the stage.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from caruca_v2 import tools
from caruca_v2.workspace import Workspace


@pytest.fixture
def space(tmp_path: Path) -> Workspace:
    root = tmp_path / "toplevel"
    sandbox = root / "sandbox_inner"
    sandbox.mkdir(parents=True)
    (sandbox / "relpath_1").write_text("hello\n")
    (sandbox / "subdir").mkdir()
    stdin_path = root / "stdin"
    stdin_path.write_bytes(b"standard input\n")
    scratch = root / "tmp"
    scratch.mkdir()
    # A file the command must never be able to reach.
    (tmp_path / "outside_the_jail.txt").write_text("secret\n")
    return Workspace(
        root=root,
        sandbox=sandbox,
        stdin_path=stdin_path,
        scratch=scratch,
        invocation="cat relpath_1",
        stdin_name="HUMAN_TEXT",
        listing=["relpath_1", "subdir"],
    )


def executor(space: Workspace, command: str = "cat") -> tools.ToolExecutor:
    return tools.ToolExecutor(command=command, workspace=space)


def test_the_command_under_test_runs(space: Workspace):
    result = executor(space).execute("run_command", {"argv": ["cat", "relpath_1"]})
    assert result["return_code"] == 0
    assert result["stdout"] == "hello\n"


def test_any_other_binary_is_refused(space: Workspace):
    executed = executor(space)
    result = executed.execute("run_command", {"argv": ["ls", "-la"]})

    assert "refused" in result["error"]
    assert executed.executions == 0
    assert executed.audit_trail()[0]["allowed"] is False


def test_a_shell_wrapping_the_command_is_refused(space: Workspace):
    result = executor(space).execute("run_command", {"argv": ["sh", "-c", "cat relpath_1"]})
    assert "refused" in result["error"]


def test_an_absolute_path_argument_outside_the_workspace_is_refused(space: Workspace):
    outside = str(space.root.parent / "outside_the_jail.txt")
    result = executor(space).execute("run_command", {"argv": ["cat", outside]})

    assert "refused" in result["error"]
    assert "outside the working directory" in result["error"]


def test_an_absolute_path_argument_inside_the_workspace_is_allowed(space: Workspace):
    inside = str(space.sandbox / "relpath_1")
    result = executor(space).execute("run_command", {"argv": ["cat", inside]})
    assert result["return_code"] == 0


def test_the_command_receives_the_configurations_stdin(space: Workspace):
    result = executor(space).execute("run_command", {"argv": ["cat"]})
    assert result["stdout"] == "standard input\n"


def test_multi_word_commands_match_on_the_whole_prefix(space: Workspace):
    executed = executor(space, command="git commit")
    assert "refused" in executed.execute("run_command", {"argv": ["git", "log"]})["error"]


@pytest.mark.parametrize(
    "path",
    ["../outside_the_jail.txt", "/etc/passwd", "subdir/../../outside_the_jail.txt"],
)
def test_observation_tools_cannot_escape_the_workspace(space: Workspace, path: str):
    executed = executor(space)
    for tool in ("read_file", "stat_path", "list_dir"):
        result = executed.execute(tool, {"path": path})
        assert "refused" in result["error"], f"{tool} let {path} through"


def test_observation_tools_do_not_spawn_a_binary(space: Workspace):
    # "You may only use `cat`" has to survive the model looking around, so observation is
    # Python-side. If it ever shelled out, this would count as an execution.
    executed = executor(space)
    executed.execute("list_dir", {"path": "."})
    executed.execute("read_file", {"path": "relpath_1"})
    executed.execute("stat_path", {"path": "subdir"})
    assert executed.executions == 0


def test_list_dir_reports_names_and_types(space: Workspace):
    result = executor(space).execute("list_dir", {"path": "."})
    assert {"name": "relpath_1", "type": "file"} in result["entries"]
    assert {"name": "subdir", "type": "directory"} in result["entries"]


def test_read_file_flags_truncation_rather_than_hiding_it(space: Workspace):
    big = space.sandbox / "big.txt"
    big.write_text("x" * (tools.MAX_READ_BYTES + 10))

    result = executor(space).execute("read_file", {"path": "big.txt"})

    assert result["truncated"] is True
    assert len(result["content"]) == tools.MAX_READ_BYTES


def test_destructive_commands_are_refused_on_the_host(space: Workspace):
    executed = tools.ToolExecutor(command="rm", workspace=space, isolation=None)
    with pytest.raises(tools.IsolationRequired) as excinfo:
        executed.execute("run_command", {"argv": ["rm", "relpath_1"]})

    assert "--isolation lima" in str(excinfo.value)
    assert (space.sandbox / "relpath_1").exists()


def test_destructive_commands_are_recognised_by_name():
    assert tools.requires_isolation("rm")
    assert tools.requires_isolation("mv")
    assert tools.requires_isolation("git commit") is False
    assert tools.requires_isolation("cat") is False


def test_a_lima_backend_prefixes_the_execution_rather_than_changing_it():
    backend = tools.IsolationBackend.lima("caruca")
    assert backend.prefix == ["limactl", "shell", "caruca", "--"]
    assert backend.name == "lima:caruca"


def test_an_unknown_tool_name_is_reported_not_raised(space: Workspace):
    result = executor(space).execute("delete_everything", {})
    assert "no tool named" in result["error"]


def test_report_observations_ends_the_session(space: Workspace):
    executed = executor(space)
    assert executed.report is None

    executed.execute(
        "report_observations",
        {"interactions": [{"action": "rf", "path": "relpath_1"}], "return_code": 0,
         "stdout": "hello\n", "stderr": ""},
    )

    assert executed.report is not None
    assert executed.report["return_code"] == 0


def test_the_audit_trail_records_every_call_and_decision(space: Workspace):
    executed = executor(space)
    executed.execute("run_command", {"argv": ["cat", "relpath_1"]})
    executed.execute("run_command", {"argv": ["ls"]})

    trail = executed.audit_trail()
    assert [call["allowed"] for call in trail] == [True, False]
    assert "only `cat` may be run" in trail[1]["reason"]


def test_tool_definitions_name_the_command_under_test(space: Workspace):
    definitions = tools.tool_definitions("cat")
    names = [definition["function"]["name"] for definition in definitions]
    assert names == ["run_command", "list_dir", "read_file", "stat_path", "report_observations"]
    assert "`cat`" in definitions[0]["function"]["description"]


def test_results_go_back_to_the_model_as_json(space: Workspace):
    assert json.loads(tools.format_result({"return_code": 0})) == {"return_code": 0}
