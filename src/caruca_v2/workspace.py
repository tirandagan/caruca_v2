"""Throwaway working directories, laid out exactly as v1 lays them out.

Fidelity here is load-bearing: every downstream comparison assumes the LLM saw the same
starting state v1's tracer saw. So the layout is not reimplemented — `v1.py` hands the
configuration to v1's own `prepare_env` code and lets it build the directory. Explicit
direction from Tiran (2026-09-03): no extra files, no richer fixtures, no "helpful"
additions. Comparability requires identical inputs.
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import v1

STDIN_FILENAME = "caruca_v2_stdin"


@dataclass(frozen=True)
class Workspace:
    """One configuration's prepared working directory."""

    root: Path
    sandbox: Path
    stdin_path: Path
    scratch: Path
    invocation: str | None
    stdin_name: str | None
    listing: list[str]

    @property
    def stdin_bytes(self) -> bytes:
        return self.stdin_path.read_bytes()

    def rewrite(self, path: str) -> str:
        """Map a path the command touched into v1's fixed sandbox namespace.

        v1's tracer does the same thing, and v1's annotator hardcodes the destination, so
        a traces file that skips this step is unreadable by v1's own tooling. Relative
        paths, and the three stream names, are passed through as v1 passes them through.
        """
        if path in ("stdin", "stdout", "stderr"):
            return path

        candidate = Path(path)
        if not candidate.is_absolute():
            return path

        try:
            relative = candidate.resolve().relative_to(self.sandbox.resolve())
        except ValueError:
            return path
        return str(Path(v1.PLACEHOLDER_SANDBOX) / relative)


class MaterializationFailure(Exception):
    """v1 could not build the working directory for this configuration.

    A plain exception on purpose: a frozen-dataclass exception cannot have
    `__traceback__` assigned, which makes `contextlib` explode with a
    `FrozenInstanceError` that shadows the real failure. Caught live by pilot
    campaign C0 on 2026-09-08, on the first model-generated config v1 rejected.
    """

    def __init__(self, reason: str, traceback: str | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.traceback = traceback

    def __str__(self) -> str:
        return self.reason


@contextmanager
def materialize(
    config: dict[str, Any], *, keep: bool = False, root_dir: Path | None = None
) -> Iterator[Workspace]:
    """Prepare one config's working directory; remove it afterwards unless `keep`.

    The nested directories mirror v1's own `CommandConfig.env()`, which creates a
    top-level temporary directory and a sandbox inside it. The stdin payload and the
    scratch directory are written *outside* the sandbox, so neither appears in a directory
    listing the command can see — the same reason v1 keeps its `TMPDIR` outside.

    `root_dir` overrides where the workspace is created. An isolation backend needs this:
    the platform temp directory does not exist inside the Lima VM, which mounts only the
    home directory, so a workspace created there would give the command a working
    directory that is absent on the far side.
    """
    if root_dir is not None:
        root_dir.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="caruca_v2_toplevel_", dir=root_dir))
    sandbox = root / "sandbox_inner"
    sandbox.mkdir()
    scratch = root / "tmp"
    scratch.mkdir()
    stdin_path = root / STDIN_FILENAME

    prepared = v1.materialize_config(config, sandbox, stdin_path)
    if not prepared.prepared:
        if not keep:
            shutil.rmtree(root, ignore_errors=True)
        raise MaterializationFailure(
            reason=f"v1 could not prepare the workspace: {prepared.error}",
            traceback=prepared.traceback,
        )

    workspace = Workspace(
        root=root,
        sandbox=sandbox,
        stdin_path=stdin_path,
        scratch=scratch,
        invocation=prepared.invocation,
        stdin_name=prepared.stdin_name,
        listing=prepared.listing,
    )
    try:
        yield workspace
    finally:
        if not keep:
            shutil.rmtree(root, ignore_errors=True)
