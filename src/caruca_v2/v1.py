"""The single boundary between caruca_v2 and the caruca v1 checkout.

Two rules live here and nowhere else:

1. **Subprocess only.** v1 is never imported as a library (`import caruca` must not
   appear anywhere in this package). Anything that needs v1's own semantics runs
   through v1's venv interpreter as a child process.
2. **Nothing from v1 is committed.** v1 is private and unlicensed, so its man pages,
   syntax specs, and data fixtures are read from ``CARUCA_V1_ROOT`` at runtime and
   injected into prompts, never checked into this repo.
"""

from __future__ import annotations

import contextlib
import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import V1AccessError

DEFAULT_V1_ROOT = "/Users/tirandagan/dev/stevens/caruca"

# v1's few-shot exemplars, in v1's own order (llm.py: `cmd_example_names`).
EXEMPLAR_COMMANDS = ("touch", "rm", "mv", "ls")

# v1's validation timeout. Importing a spec module is near-instant; this only guards
# against a generated file that blocks (e.g. reads stdin) at import time.
VALIDATION_TIMEOUT_SECONDS = 30


def slug(command: str) -> str:
    """v1's filename convention for multi-word commands: ``git commit`` -> ``git_commit``."""
    return "_".join(command.split())


def v1_root() -> Path:
    """The v1 repository root: the directory containing ``caruca/``."""
    root = Path(os.environ.get("CARUCA_V1_ROOT", DEFAULT_V1_ROOT)).expanduser()
    if not root.is_dir():
        raise V1AccessError(
            f"caruca v1 checkout not found at {root}. "
            "Set CARUCA_V1_ROOT to the v1 repository root (the directory containing `caruca/`)."
        )
    return root


def package_root() -> Path:
    """v1's Python package source directory: ``<v1_root>/caruca/src/caruca``."""
    path = v1_root() / "caruca" / "src" / "caruca"
    if not path.is_dir():
        raise V1AccessError(
            f"caruca v1 package source not found at {path}. "
            "CARUCA_V1_ROOT should point at the repository root, not the package directory."
        )
    return path


def _read(path: Path, what: str) -> str:
    if not path.is_file():
        raise V1AccessError(f"{what} not found at {path}.")
    return path.read_text()


def man_page_path(command: str) -> Path:
    return package_root() / "doc_sources" / "man" / f"{slug(command)}.txt"


def man_page(command: str) -> str:
    """The documentation v1 feeds its own LLM step, for the same command."""
    path = man_page_path(command)
    if not path.is_file():
        raise V1AccessError(
            f"No man page for {command!r} in the v1 corpus (looked for {path}). "
            "Pass --docs PATH to supply documentation from elsewhere."
        )
    return path.read_text()


def syntax_spec_path(command: str) -> Path:
    return package_root() / "syntax_specs" / f"{slug(command)}.py"


def syntax_spec(command: str) -> str:
    """The committed, hand-curated syntax spec for a command: v1's ground truth."""
    path = syntax_spec_path(command)
    if not path.is_file():
        raise V1AccessError(
            f"No committed syntax spec for {command!r} in the v1 corpus (looked for {path})."
        )
    return path.read_text()


def traces_path(command: str) -> Path:
    return v1_root() / "caruca" / "outputs" / f"{slug(command)}.json"


def data_fixture_dir() -> Path:
    """v1's `data/` payloads (human_1.txt, math_1.txt, json.json, ...).

    Stage 3 materializes workspaces from these verbatim: identical inputs are what makes
    the trace comparison meaningful, so the fixtures are never substituted or enriched.
    """
    return package_root() / "data"


@dataclass(frozen=True)
class Exemplar:
    """One few-shot pair: a command's documentation and its committed spec."""

    command: str
    man_page: str
    syntax_spec: str


def exemplars(commands: tuple[str, ...] = EXEMPLAR_COMMANDS) -> list[Exemplar]:
    """v1's four few-shot examples, read from the checkout in v1's own order."""
    return [
        Exemplar(command=command, man_page=man_page(command), syntax_spec=syntax_spec(command))
        for command in commands
    ]


def venv_python() -> Path:
    """v1's own interpreter (3.12), the only thing that can import a v1-DSL spec."""
    path = v1_root() / "caruca" / ".venv" / "bin" / "python"
    if not path.is_file():
        raise V1AccessError(
            f"v1's virtualenv interpreter not found at {path}. "
            "The generated spec can only be validated by v1's own environment."
        )
    return path


# Runs inside v1's venv, not ours: it imports the generated module the way v1's `llm.py`
# does, then additionally asserts the reflectively-required `<cmd>_syntax_spec` binding
# exists (v1's own check stops at import; command registration needs the binding too).
_VALIDATE_SCRIPT = """
import importlib.util, json, sys, traceback

spec_path, symbol = sys.argv[1], sys.argv[2]
result = {"passed": False, "symbol": symbol, "error": None, "traceback": None, "elements": None}
try:
    spec = importlib.util.spec_from_file_location("caruca_v2_generated_spec", spec_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, symbol):
        result["error"] = f"module imported but does not define {symbol}"
    else:
        value = getattr(module, symbol)
        try:
            result["elements"] = sum(len(group) for form in value for group in form)
        except TypeError:
            result["elements"] = None
        result["passed"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of asking v1 whether a generated spec is a valid v1-DSL spec.

    `available` is False only when v1's environment could not be reached at all, which
    is a different fact from "the spec is invalid" and is reported as such.
    """

    passed: bool
    available: bool
    error: str | None = None
    traceback: str | None = None
    elements: int | None = None

    @classmethod
    def unavailable(cls, reason: str) -> ValidationResult:
        return cls(passed=False, available=False, error=reason)


def validate_syntax_spec(command: str, spec_path: Path) -> ValidationResult:
    """Import the generated spec through v1's venv and report what happened.

    The result is recorded, never acted on: a failed validation is a measurement of the
    naive baseline, not a trigger to ask the model again.
    """
    try:
        python = venv_python()
    except V1AccessError as exc:
        return ValidationResult.unavailable(str(exc))

    # cwd mirrors v1, which validated from the directory holding the spec file.
    # Bytecode writing is disabled so validation leaves no `__pycache__` inside a run
    # directory: run directories are evidence, and nothing but evidence belongs in them.
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

    try:
        completed = subprocess.run(
            [str(python), "-c", _VALIDATE_SCRIPT, str(spec_path), f"{slug(command)}_syntax_spec"],
            capture_output=True,
            text=True,
            timeout=VALIDATION_TIMEOUT_SECONDS,
            cwd=str(spec_path.parent),
            env=environment,
        )
    except subprocess.TimeoutExpired:
        return ValidationResult(
            passed=False,
            available=True,
            error=f"import timed out after {VALIDATION_TIMEOUT_SECONDS}s",
        )

    payload = completed.stdout.strip().splitlines()
    if not payload:
        return ValidationResult.unavailable(
            f"v1 validation subprocess produced no output (exit {completed.returncode}): "
            f"{completed.stderr.strip()[:500]}"
        )

    try:
        data = json.loads(payload[-1])
    except json.JSONDecodeError:
        return ValidationResult.unavailable(
            f"v1 validation subprocess produced unparseable output: {payload[-1][:500]}"
        )

    return ValidationResult(
        passed=bool(data["passed"]),
        available=True,
        error=data["error"],
        traceback=data["traceback"],
        elements=data["elements"],
    )


# --- Stage 2 support: v1's DSL semantics and its own generator, as reference material ---

# The syntax spec file names value types; it does not carry the values those types expand
# into. Those live in v1's DSL runtime (`ir/syntax.py`), which is where the invocation
# strings actually come from. Extracting the table at runtime keeps it true to whatever
# the checkout contains -- including v1's own quirks, which are reproduced rather than
# corrected (`Hostname` expands to nine single characters because its options tuple was
# written without a trailing comma; that is v1's behavior and therefore the target).
_PROBE_VALUES_SCRIPT = """
import inspect, json
import caruca.ir.syntax as syntax

table = {}
for name in sorted(n for n in dir(syntax) if not n.startswith("_")):
    obj = getattr(syntax, name)
    if not inspect.isclass(obj) or not issubclass(obj, syntax.ValueArgument):
        continue
    if obj is syntax.ValueArgument:
        continue
    try:
        instance = obj()
        if isinstance(instance, syntax.Path):
            instance.elaborate_relations = False
        table[name] = [str(value) for value in instance.syntax()]
    except Exception as exc:
        table[name] = {"unavailable": f"{type(exc).__name__}: {exc}"}

print(json.dumps(table))
"""

_CONFIG_SCHEMA_SCRIPT = """
import json
from caruca.ir.environment import CommandConfig

print(json.dumps(CommandConfig.model_json_schema()))
"""

_VALIDATE_CONFIGS_SCRIPT = """
import json, sys, traceback

from caruca.ir.environment import CommandConfig

result = {"passed": False, "count": 0, "error": None, "traceback": None, "invalid_index": None}
try:
    payload = json.loads(open(sys.argv[1]).read())
    if not isinstance(payload, list):
        raise TypeError(
            f"expected a JSON list of CommandConfig objects, got {type(payload).__name__}"
        )
    for index, entry in enumerate(payload):
        result["invalid_index"] = index
        CommandConfig.model_validate(entry)
    result["invalid_index"] = None
    result["count"] = len(payload)
    result["passed"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""


def _run_in_v1_venv(script: str, *args: str, timeout: int = VALIDATION_TIMEOUT_SECONDS) -> Any:
    """Run a snippet inside v1's interpreter and parse its single JSON line of output."""
    python = venv_python()
    completed = subprocess.run(
        [str(python), "-c", script, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    lines = completed.stdout.strip().splitlines()
    if not lines:
        raise V1AccessError(
            f"v1 subprocess produced no output (exit {completed.returncode}): "
            f"{completed.stderr.strip()[:500]}"
        )
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise V1AccessError(
            f"v1 subprocess produced unparseable output: {lines[-1][:500]}"
        ) from exc


def probe_values() -> dict[str, Any]:
    """Every DSL value type mapped to the concrete values v1 expands it into."""
    return _run_in_v1_venv(_PROBE_VALUES_SCRIPT)


def command_config_schema() -> dict[str, Any]:
    """The JSON schema of v1's `CommandConfig`, read from v1's own pydantic model."""
    return _run_in_v1_venv(_CONFIG_SCHEMA_SCRIPT)


@dataclass(frozen=True)
class ConfigValidationResult:
    """Whether a generated configs file is accepted by v1's own `CommandConfig` model."""

    passed: bool
    available: bool
    count: int = 0
    error: str | None = None
    traceback: str | None = None
    invalid_index: int | None = None

    @classmethod
    def unavailable(cls, reason: str) -> ConfigValidationResult:
        return cls(passed=False, available=False, error=reason)


def validate_configs(configs_path: Path) -> ConfigValidationResult:
    """Ask v1 whether every entry in a configs JSON file is a valid `CommandConfig`."""
    try:
        data = _run_in_v1_venv(_VALIDATE_CONFIGS_SCRIPT, str(configs_path))
    except (V1AccessError, subprocess.TimeoutExpired) as exc:
        return ConfigValidationResult.unavailable(str(exc))
    return ConfigValidationResult(
        passed=bool(data["passed"]),
        available=True,
        count=int(data["count"]),
        error=data["error"],
        traceback=data["traceback"],
        invalid_index=data["invalid_index"],
    )


@dataclass(frozen=True)
class ReferenceInvocations:
    """What `caruca generate CMD` itself produces, for the set-diff comparison.

    `length_hint` is v1's `--number` output. It is *not* the number of lines: v1 computes
    it from a different formula than the one the enumerator actually follows (for `mkdir`
    it reports 280 against 4,240 real invocations). Both are recorded, and only `count`
    is ever used as a denominator.
    """

    invocations: list[str]
    count: int
    length_hint: int | None
    available: bool
    error: str | None = None

    @classmethod
    def unavailable(cls, reason: str) -> ReferenceInvocations:
        return cls(invocations=[], count=0, length_hint=None, available=False, error=reason)


def _caruca_executable() -> Path:
    path = v1_root() / "caruca" / ".venv" / "bin" / "caruca"
    if not path.is_file():
        raise V1AccessError(f"v1's `caruca` entry point not found at {path}.")
    return path


def reference_invocations(
    command: str,
    *,
    max_arity: int = 1,
    max_count: int = 4,
    skip: str | None = None,
    timeout: int = 300,
) -> ReferenceInvocations:
    """Run v1's own `generate` for the command, as the comparison target.

    **Every bound that was stated to the model has to be passed here too.** They are not
    cosmetic: `mkdir` at arity 1 yields 44 invocations with `--max-count 1` and 4,240 with
    v1's default of 4. Generating the reference with different bounds than the prompt
    stated produces a set-diff that measures the mismatch in bounds, not the model.
    """
    try:
        executable = _caruca_executable()
    except V1AccessError as exc:
        return ReferenceInvocations.unavailable(str(exc))

    package_dir = v1_root() / "caruca"
    base = [
        str(executable),
        "generate",
        *command.split(),
        "--max-arity",
        str(max_arity),
        "--max-count",
        str(max_count),
    ]
    if skip:
        base += ["--skip", skip]

    try:
        listing = subprocess.run(
            base, capture_output=True, text=True, timeout=timeout, cwd=str(package_dir)
        )
        counting = subprocess.run(
            [*base, "--number"], capture_output=True, text=True, timeout=timeout,
            cwd=str(package_dir),
        )
    except subprocess.TimeoutExpired:
        return ReferenceInvocations.unavailable(
            f"`caruca generate {command}` did not finish within {timeout}s; "
            "enumeration cost is itself a v1 result, so this is recorded, not worked around."
        )

    if listing.returncode != 0:
        return ReferenceInvocations.unavailable(
            f"`caruca generate {command}` exited {listing.returncode}: "
            f"{listing.stderr.strip()[:500]}"
        )

    invocations = [line for line in listing.stdout.splitlines() if line.strip()]
    hint: int | None = None
    if counting.returncode == 0:
        with contextlib.suppress(ValueError):
            hint = int(counting.stdout.strip().splitlines()[-1])

    return ReferenceInvocations(
        invocations=invocations,
        count=len(invocations),
        length_hint=hint,
        available=True,
    )


# --- Stage 3 support: workspace materialization and Traces assembly, done by v1 itself ---

# v1's tracer runs each command inside a temporary sandbox but rewrites every absolute
# path it observes into this fixed namespace before recording it. v1's annotator then
# hardcodes the same path, so any trace file meant to be read by v1 has to use it.
PLACEHOLDER_SANDBOX = "/tmp/sandbox_outer/sandbox_inner"

# v1's execution environment (`tracer/tracer.py`), reproduced exactly.
EXECUTION_ENV = {"PATH": "/usr/bin:/bin:/usr/local/sbin:/usr/local/bin", "SHELL": "/bin/sh"}
EXECUTION_TIMEOUT_SECONDS = 2

# Materialization runs v1's own `prepare_env` calls rather than reimplementing them.
# Reimplementing would mean maintaining a second copy of v1's environment semantics and
# hoping the two stay equal; calling v1's makes them equal by construction. The stdin
# payload comes from v1's `Content` enum, which reads the fixture files in `data/`.
_MATERIALIZE_SCRIPT = """
import json, sys, traceback
from pathlib import Path

from caruca.ir.environment import CommandConfig

result = {"prepared": False, "error": None, "traceback": None, "stdin_name": None,
          "invocation": None, "listing": []}
try:
    config = CommandConfig.model_validate(json.loads(sys.argv[1]))
    sandbox = Path(sys.argv[2])
    for sequence in config.body:
        sequence.prepare(sandbox)
    Path(sys.argv[3]).write_bytes(config.stdin.value)
    result["stdin_name"] = config.stdin.name
    result["invocation"] = config.true_string
    result["listing"] = sorted(
        str(path.relative_to(sandbox)) for path in sandbox.rglob("*")
    )
    result["prepared"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""

# Grouping and envelope construction go through v1's own pydantic models, so a file that
# comes out of here is valid by construction rather than by our imitation of the format.
_ASSEMBLE_TRACES_SCRIPT = """
import json, sys, traceback
from pathlib import Path

from caruca.ir.environment import CommandConfig
from caruca.tracer.data import (
    CommandInvocationTraceSet,
    CommandInvocationTraces,
    FSInteraction,
    Traces,
)

result = {"assembled": False, "error": None, "traceback": None, "sets": 0, "configs": 0}
try:
    entries = json.loads(Path(sys.argv[1]).read_text())
    groups = {}
    order = []
    for entry in entries:
        config = CommandConfig.model_validate(entry["config"])
        traces = []
        for action, path in entry["traces"]:
            interaction = FSInteraction(action)
            target = path if path in ("stdin", "stdout", "stderr") else Path(path)
            traces.append((interaction, target))
        record = CommandInvocationTraces(
            command=config,
            return_code=entry["return_code"],
            stdout=entry["stdout"],
            stderr=entry["stderr"],
            traces=traces,
        )
        key = json.dumps(config.string, sort_keys=True)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(record)

    sets = [
        CommandInvocationTraceSet(
            command=json.loads(key),
            true_str=groups[key][0].command.true_string,
            configs=groups[key],
        )
        for key in order
    ]
    Path(sys.argv[2]).write_text(Traces(sets).model_dump_json(indent=1))
    result["sets"] = len(sets)
    result["configs"] = sum(len(groups[key]) for key in order)
    result["assembled"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""

_VALIDATE_TRACES_SCRIPT = """
import json, sys, traceback
from pathlib import Path

from caruca.tracer.data import Traces

result = {"passed": False, "sets": 0, "error": None, "traceback": None}
try:
    traces = Traces.model_validate_json(Path(sys.argv[1]).read_text())
    result["sets"] = len(traces.root)
    result["passed"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""


@dataclass(frozen=True)
class MaterializedConfig:
    """The result of asking v1 to lay out one configuration's working directory."""

    prepared: bool
    invocation: str | None
    stdin_name: str | None
    listing: list[str]
    error: str | None = None
    traceback: str | None = None


def materialize_config(
    config: dict[str, Any], sandbox: Path, stdin_path: Path
) -> MaterializedConfig:
    """Build the working directory for one config, using v1's own `prepare_env` calls."""
    try:
        data = _run_in_v1_venv(
            _MATERIALIZE_SCRIPT, json.dumps(config), str(sandbox), str(stdin_path)
        )
    except (V1AccessError, subprocess.TimeoutExpired) as exc:
        return MaterializedConfig(
            prepared=False, invocation=None, stdin_name=None, listing=[], error=str(exc)
        )
    return MaterializedConfig(
        prepared=bool(data["prepared"]),
        invocation=data["invocation"],
        stdin_name=data["stdin_name"],
        listing=list(data["listing"]),
        error=data["error"],
        traceback=data["traceback"],
    )


@dataclass(frozen=True)
class AssemblyResult:
    """Whether v1's models accepted the observations and produced a Traces file."""

    assembled: bool
    sets: int = 0
    configs: int = 0
    error: str | None = None
    traceback: str | None = None


def assemble_traces(entries_path: Path, output_path: Path) -> AssemblyResult:
    """Group per-config observations into v1's Traces envelope, built by v1's own models."""
    try:
        data = _run_in_v1_venv(_ASSEMBLE_TRACES_SCRIPT, str(entries_path), str(output_path))
    except (V1AccessError, subprocess.TimeoutExpired) as exc:
        return AssemblyResult(assembled=False, error=str(exc))
    return AssemblyResult(
        assembled=bool(data["assembled"]),
        sets=int(data["sets"]),
        configs=int(data["configs"]),
        error=data["error"],
        traceback=data["traceback"],
    )


def validate_traces(traces_path: Path) -> ConfigValidationResult:
    """Ask v1 whether a traces file validates against its own `Traces` model."""
    try:
        data = _run_in_v1_venv(_VALIDATE_TRACES_SCRIPT, str(traces_path))
    except (V1AccessError, subprocess.TimeoutExpired) as exc:
        return ConfigValidationResult.unavailable(str(exc))
    return ConfigValidationResult(
        passed=bool(data["passed"]),
        available=True,
        count=int(data["sets"]),
        error=data["error"],
        traceback=data["traceback"],
    )


# --- Stage 4 support: annotation formats, v1's own annotator, and the ground truth ---

ANNOTATION_FORMATS = ("pash", "posh", "sash", "shellcheck")

# Three of the four formats are pydantic models and can be validated properly. The
# ShellCheck adapter emits rendered Haskell, so all that can be checked cheaply is that it
# is a module of the expected shape -- a genuinely weaker check, reported as such rather
# than dressed up as equivalent.
_ANNOTATION_SCHEMA_SCRIPT = """
import json, sys

from caruca.annotator import PaSh, Posh, SaSh, render_shellcheck_module

fmt = sys.argv[1]
models = {"pash": PaSh, "posh": Posh, "sash": SaSh}
if fmt == "shellcheck":
    print(json.dumps({
        "kind": "haskell",
        "skeleton": render_shellcheck_module(sys.argv[2], [], missing_destination=None),
    }))
else:
    print(json.dumps({"kind": "json", "schema": models[fmt].model_json_schema()}))
"""

_VALIDATE_ANNOTATION_SCRIPT = """
import json, sys, traceback
from pathlib import Path

from caruca.annotator import PaSh, Posh, SaSh

result = {"passed": False, "count": 0, "error": None, "traceback": None}
fmt, path = sys.argv[1], Path(sys.argv[2])
try:
    text = path.read_text()
    if fmt == "shellcheck":
        if "module Caruca" not in text:
            raise ValueError("not a Caruca ShellCheck module (no `module Caruca` line)")
        result["count"] = text.count("DeletePattern")
    else:
        model = {"pash": PaSh, "posh": Posh, "sash": SaSh}[fmt]
        parsed = model.model_validate_json(text)
        root = getattr(parsed, "root", None)
        result["count"] = len(root) if root is not None else len(getattr(parsed, "cases", []))
    result["passed"] = True
except BaseException as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
    result["traceback"] = traceback.format_exc()

print(json.dumps(result))
"""


def annotation_format_definition(fmt: str, command: str) -> dict[str, Any]:
    """The output-format definition for one consumer, taken from v1's own adapter."""
    if fmt not in ANNOTATION_FORMATS:
        raise V1AccessError(
            f"unknown annotation format {fmt!r}; expected one of {ANNOTATION_FORMATS}."
        )
    return _run_in_v1_venv(_ANNOTATION_SCHEMA_SCRIPT, fmt, command)


def validate_annotation(fmt: str, path: Path) -> ConfigValidationResult:
    """Ask v1 whether an annotation file is well formed for the requested consumer."""
    try:
        data = _run_in_v1_venv(_VALIDATE_ANNOTATION_SCRIPT, fmt, str(path))
    except (V1AccessError, subprocess.TimeoutExpired) as exc:
        return ConfigValidationResult.unavailable(str(exc))
    return ConfigValidationResult(
        passed=bool(data["passed"]),
        available=True,
        count=int(data["count"]),
        error=data["error"],
        traceback=data["traceback"],
    )


@dataclass(frozen=True)
class ReferenceAnnotation:
    """What v1's own annotator produced from the same traces, or why it could not."""

    text: str | None
    available: bool
    error: str | None = None
    runner: str = "host"

    @classmethod
    def unavailable(cls, reason: str, runner: str = "host") -> ReferenceAnnotation:
        return cls(text=None, available=False, error=reason, runner=runner)


# v1's annotator resolves observed paths against a hardcoded `/tmp/sandbox_outer/...`
# prefix. On macOS `/tmp` is a symlink to `/private/tmp`, so `Path.resolve()` moves the
# path out from under that prefix and `relative_to` raises: v1's `annotate` cannot run on
# a Mac at all. Verified 2026-09-03 against v1's own committed `outputs/ls.json`. That is
# why the Lima runner exists; it is not an optimization.
LIMA_V1_PYTHON = "~/caruca-venv/bin/caruca"


def reference_annotation(
    command: str,
    fmt: str,
    traces_path: Path,
    *,
    runner: str = "host",
    lima_instance: str = "caruca",
    timeout: int = 600,
) -> ReferenceAnnotation:
    """Run v1's own `annotate` on the same traces, as the A/B comparison target."""
    if runner == "lima":
        remote = " ".join(
            shlex.quote(part)
            for part in ["annotate", fmt, *command.split(), "--input", str(traces_path)]
        )
        argv = [
            "limactl", "shell", lima_instance, "--",
            "sh", "-lc",
            f"{LIMA_V1_PYTHON} {remote}",
        ]
    else:
        try:
            executable = _caruca_executable()
        except V1AccessError as exc:
            return ReferenceAnnotation.unavailable(str(exc), runner)
        argv = [str(executable), "annotate", fmt, *command.split(), "--input", str(traces_path)]

    try:
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(v1_root() / "caruca"),
        )
    except subprocess.TimeoutExpired:
        return ReferenceAnnotation.unavailable(
            f"v1's annotate did not finish within {timeout}s", runner
        )
    except FileNotFoundError as exc:
        return ReferenceAnnotation.unavailable(f"could not launch v1's annotate: {exc}", runner)

    if completed.returncode != 0:
        return ReferenceAnnotation.unavailable(
            f"v1's `annotate {fmt} {command}` exited {completed.returncode}: "
            f"{completed.stderr.strip()[-500:]}",
            runner,
        )
    return ReferenceAnnotation(text=completed.stdout, available=True, runner=runner)


def ground_truth_annotation_path(command: str, fmt: str) -> Path | None:
    """Where the hand-curated annotation for this command and consumer lives, if anywhere.

    These files cost two graduate students eighty hours; they are the most expensive input
    to the whole evaluation and are read, never regenerated.
    """
    annotations = v1_root() / "benchmarks" / "annotations"
    if fmt == "pash":
        return annotations / "pash" / f"{slug(command)}.json"
    if fmt == "posh":
        return annotations / "posh.txt"
    return None


def ground_truth_annotation(command: str, fmt: str) -> str | None:
    path = ground_truth_annotation_path(command, fmt)
    if path is None or not path.is_file():
        return None
    return path.read_text()


def v1_commit() -> str | None:
    """The v1 commit every comparison is against. Recorded with every result."""
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=30, cwd=str(v1_root()),
        )
    except (OSError, subprocess.TimeoutExpired, V1AccessError):
        return None
    return completed.stdout.strip() or None
