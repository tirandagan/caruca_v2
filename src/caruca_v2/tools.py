"""The tool surface for stage 3, and the boundary that makes it safe.

This is the only place in the project where a model's choice reaches a real shell, so the
rules are enforced here in code rather than asked for in the prompt. The prompt says what
is allowed; this module guarantees it. Every rejection is returned to the model as a tool
result, so a refused call is visible in the conversation log and in the audit trail rather
than silently swallowed.

Three boundaries:

1. **Binary allowlist.** `run_command` runs the command under test and nothing else.
2. **Path jail.** Every path a tool touches, and *every* argument in an argument vector,
   must resolve inside the workspace. Checking only absolute arguments is not enough:
   `run_command` sets cwd to the workspace, so a relative `../../etc/hosts` escapes just
   as effectively as an absolute path would.
3. **Destructive commands are refused on this machine.** Commands that delete or
   overwrite by nature only run under an isolation backend (the Lima VM), never directly
   on the developer's Mac.

Observation is done in Python, never by spawning a binary, so inspecting the workspace
cannot violate "you may only use the command under test".
"""

from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import v1
from .workspace import Workspace

MAX_READ_BYTES = 8192
MAX_LISTING_ENTRIES = 200

# Workspaces for isolated runs must sit under the home directory: that is the only path
# the Lima VM mounts, and it is mounted at the same path on both sides.
LIMA_WORKSPACE_ROOT = Path.home() / ".caruca_v2" / "workspaces"

# Commands whose whole purpose is to remove or overwrite. A path jail is not enough
# insurance for these on a machine with the researcher's real work on it, so they are
# refused unless an isolation backend is carrying the execution.
DESTRUCTIVE_COMMANDS = frozenset(
    {
        "rm", "rmdir", "unlink", "shred", "truncate", "dd", "mkfs", "fdisk",
        "mv", "chmod", "chown", "chgrp", "ln", "install", "tee",
    }
)


class IsolationRequired(RuntimeError):
    """A destructive command was requested without an isolation backend to run it in."""


def requires_isolation(command: str) -> bool:
    return command.split()[0] in DESTRUCTIVE_COMMANDS


@dataclass
class ToolCallRecord:
    """One tool call and what the executor did with it."""

    name: str
    arguments: dict[str, Any]
    allowed: bool
    reason: str | None
    result: dict[str, Any]


def tool_definitions(command: str) -> list[dict[str, Any]]:
    """The tools the model is offered, named in terms of the command under test."""
    return [
        {
            "type": "function",
            "function": {
                "name": "run_command",
                "description": (
                    f"Run `{command}` once in the working directory. The argument vector "
                    f"must begin with `{command}`. No other program can be run."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "argv": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": (
                                "The full argument vector, including the command name "
                                "itself as the first element(s)."
                            ),
                        }
                    },
                    "required": ["argv"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_dir",
                "description": "List the entries of a directory in the working directory.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string", "default": "."}},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": (
                    f"Read the first {MAX_READ_BYTES} bytes of a file in the working directory."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "stat_path",
                "description": "Report whether a path exists, its type, and its size.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "report_observations",
                "description": (
                    "Submit the final record of what running the command did. Calling "
                    "this ends the session."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interactions": {
                            "type": "array",
                            "description": "Every file-system interaction observed.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "action": {
                                        "type": "string",
                                        "enum": [
                                            "rf", "wf", "ad", "mo", "de", "md", "rd",
                                        ],
                                        "description": (
                                            "rf read file, wf wrote file, ad created "
                                            "file, mo modified file, de deleted file, "
                                            "md created directory, rd replaced with "
                                            "directory."
                                        ),
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": (
                                            "The path touched, or one of stdin, stdout, "
                                            "stderr."
                                        ),
                                    },
                                },
                                "required": ["action", "path"],
                            },
                        },
                        "return_code": {"type": ["integer", "null"]},
                        "stdout": {"type": ["string", "null"]},
                        "stderr": {"type": ["string", "null"]},
                    },
                    "required": ["interactions", "return_code", "stdout", "stderr"],
                },
            },
        },
    ]


@dataclass(frozen=True)
class IsolationBackend:
    """Where `run_command` actually runs.

    `workspace_root` exists because the backend decides where a workspace has to live. The
    Lima VM mounts only the Mac *home* directory, at the same path; the platform temp
    directory (`/var/folders/...` on macOS) does not exist inside the guest at all. A
    workspace created there would leave the command with a working directory that is not
    present on the far side.
    """

    name: str
    prefix: list[str]
    workspace_root: Path | None = None

    @classmethod
    def lima(cls, instance: str = "caruca") -> IsolationBackend:
        return cls(
            name=f"lima:{instance}",
            prefix=["limactl", "shell", instance, "--"],
            workspace_root=LIMA_WORKSPACE_ROOT,
        )


@dataclass
class ToolExecutor:
    """Executes the model's tool calls against one workspace, enforcing the boundaries.

    `isolation` is the backend that carries `run_command`. `None` means "run here", which
    is refused outright for destructive commands.
    """

    command: str
    workspace: Workspace
    isolation: IsolationBackend | None = None
    calls: list[ToolCallRecord] = field(default_factory=list)
    report: dict[str, Any] | None = None
    executions: int = 0

    @property
    def command_argv(self) -> list[str]:
        return self.command.split()

    def _resolve(self, path: str) -> Path:
        """Resolve a path inside the workspace, or refuse."""
        candidate = Path(path)
        target = candidate if candidate.is_absolute() else self.workspace.sandbox / candidate
        resolved = target.resolve()
        sandbox = self.workspace.sandbox.resolve()
        if resolved != sandbox and not resolved.is_relative_to(sandbox):
            raise PermissionError(f"{path!r} is outside the working directory")
        return resolved

    def _check_argv(self, argv: list[str]) -> None:
        if not argv:
            raise PermissionError("argv is empty")

        expected = self.command_argv
        if argv[: len(expected)] != expected:
            raise PermissionError(
                f"only `{self.command}` may be run; this argument vector starts with "
                f"{argv[: len(expected)]!r}"
            )

        # Every argument is checked, not only the ones starting with `/`. The command runs
        # with cwd set to the workspace, so `../../etc/hosts` escapes exactly as well as
        # `/etc/hosts` does. Arguments that are not paths (`--mode=0755`, `-n`, `42`)
        # resolve harmlessly to a nonexistent name inside the workspace and are allowed;
        # only something that resolves *outside* is refused.
        for argument in argv[len(expected) :]:
            try:
                self._resolve(argument)
            except (ValueError, OSError):
                # Not resolvable as a path at all (embedded NUL, absurd length). It cannot
                # name a file outside the workspace either, so it is not a jail concern.
                continue

    def _record(
        self,
        name: str,
        arguments: dict[str, Any],
        allowed: bool,
        reason: str | None,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        self.calls.append(
            ToolCallRecord(
                name=name, arguments=arguments, allowed=allowed, reason=reason, result=result
            )
        )
        return result

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Dispatch one tool call. Never raises: a refusal is a result the model reads."""
        handlers = {
            "run_command": self._run_command,
            "list_dir": self._list_dir,
            "read_file": self._read_file,
            "stat_path": self._stat_path,
            "report_observations": self._report_observations,
        }
        handler = handlers.get(name)
        if handler is None:
            return self._record(
                name, arguments, False, "unknown tool", {"error": f"no tool named {name!r}"}
            )
        try:
            return handler(arguments)
        except PermissionError as exc:
            return self._record(name, arguments, False, str(exc), {"error": f"refused: {exc}"})
        except IsolationRequired:
            raise
        except Exception as exc:  # a tool failing is data, not a crash
            return self._record(
                name, arguments, True, None, {"error": f"{type(exc).__name__}: {exc}"}
            )

    def _run_command(self, arguments: dict[str, Any]) -> dict[str, Any]:
        argv = [str(item) for item in arguments.get("argv", [])]
        self._check_argv(argv)

        if requires_isolation(self.command) and self.isolation is None:
            raise IsolationRequired(
                f"`{self.command}` is destructive and will not be run directly on this "
                "machine. Re-run with an isolation backend (--isolation lima)."
            )

        self.executions += 1
        completed = _run(argv, self.workspace, self.isolation)
        return self._record("run_command", {"argv": argv}, True, None, completed)

    def _list_dir(self, arguments: dict[str, Any]) -> dict[str, Any]:
        target = self._resolve(str(arguments.get("path", ".")))
        if not target.is_dir():
            return self._record(
                "list_dir",
                arguments,
                True,
                None,
                {"error": f"{arguments.get('path')} is not a directory"},
            )
        entries = sorted(
            (
                {"name": child.name, "type": "directory" if child.is_dir() else "file"}
                for child in target.iterdir()
            ),
            key=lambda entry: entry["name"],
        )
        return self._record(
            "list_dir", arguments, True, None, {"entries": entries[:MAX_LISTING_ENTRIES]}
        )

    def _read_file(self, arguments: dict[str, Any]) -> dict[str, Any]:
        target = self._resolve(str(arguments["path"]))
        data = target.read_bytes()[:MAX_READ_BYTES]
        return self._record(
            "read_file",
            arguments,
            True,
            None,
            {
                "content": data.decode("utf-8", errors="replace"),
                "truncated": target.stat().st_size > MAX_READ_BYTES,
            },
        )

    def _stat_path(self, arguments: dict[str, Any]) -> dict[str, Any]:
        target = self._resolve(str(arguments["path"]))
        if not target.exists():
            return self._record("stat_path", arguments, True, None, {"exists": False})
        info = target.stat()
        return self._record(
            "stat_path",
            arguments,
            True,
            None,
            {
                "exists": True,
                "type": "directory" if target.is_dir() else "file",
                "size": info.st_size,
            },
        )

    def _report_observations(self, arguments: dict[str, Any]) -> dict[str, Any]:
        self.report = arguments
        return self._record("report_observations", arguments, True, None, {"accepted": True})

    def audit_trail(self) -> list[dict[str, Any]]:
        """Every call, with the executor's decision — the evidence that the jail held."""
        return [
            {
                "tool": call.name,
                "arguments": call.arguments,
                "allowed": call.allowed,
                "reason": call.reason,
            }
            for call in self.calls
        ]


def _execution_env(workspace: Workspace) -> dict[str, str]:
    """Exactly the environment v1's tracer gives a traced command, and nothing else.

    v1 builds this dict from scratch (`tracer/tracer.py:54-57`) and adds `TMPDIR`
    (`tracer.py`, `run()`); it never inherits the parent environment. Inheriting would let
    `LANG`, `LC_ALL`, `COLUMNS`, and `HOME` through, and those change what `ls`, `sort`,
    `wc`, and `date` actually do — so an inherited variable would show up later as an
    apparent v1/v2 disagreement that has nothing to do with the model.
    """
    return {**v1.EXECUTION_ENV, "TMPDIR": str(workspace.scratch)}


def _remote_command(
    argv: list[str], workspace: Workspace, isolation: IsolationBackend
) -> list[str]:
    """The argument vector for running `argv` inside an isolation backend.

    The working directory and the environment are set explicitly on the far side rather
    than inherited from the launcher, so an isolated run gets the same environment as a
    host run instead of the guest shell's.
    """
    assignments = [f"{name}={value}" for name, value in sorted(_execution_env(workspace).items())]
    inner = " ".join(
        shlex.quote(part) for part in ["env", "-i", *assignments, *argv]
    )
    script = f"cd {shlex.quote(str(workspace.sandbox))} && exec {inner}"
    return [*isolation.prefix, "sh", "-c", script]


def _run(
    argv: list[str], workspace: Workspace, isolation: IsolationBackend | None
) -> dict[str, Any]:
    """Execute the command in v1's environment: v1's PATH, v1's SHELL, v1's 2s timeout."""
    if isolation is None:
        command = list(argv)
        environment = _execution_env(workspace)
    else:
        command = _remote_command(argv, workspace, isolation)
        # The launcher itself (`limactl`) needs a real environment to start; the command
        # under test does not get it, because `_remote_command` replaces it with `env -i`.
        environment = None

    try:
        completed = subprocess.run(
            command,
            cwd=str(workspace.sandbox),
            input=workspace.stdin_bytes,
            capture_output=True,
            timeout=v1.EXECUTION_TIMEOUT_SECONDS,
            env=environment,
        )
    except subprocess.TimeoutExpired:
        return {
            "return_code": None,
            "stdout": None,
            "stderr": None,
            "timed_out": True,
        }
    except FileNotFoundError as exc:
        return {"error": f"could not execute: {exc}"}

    return {
        "return_code": completed.returncode,
        "stdout": completed.stdout.decode("utf-8", errors="replace"),
        "stderr": completed.stderr.decode("utf-8", errors="replace"),
        "timed_out": False,
    }


def format_result(result: dict[str, Any]) -> str:
    """Tool results go back to the model as JSON, the same shape every time."""
    return json.dumps(result)
