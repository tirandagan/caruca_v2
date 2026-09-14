"""The stage-3 scorer: how much of what v1 saw with strace can a model recover by probing?

Task 003 recorded that this comparison needs "a partial-credit protocol still to be defined."
This is that protocol.

**Project before scoring.** v1's raw traces are mostly dynamic-loader noise: tracing
`dirname relpath_1` records 640 `(action, path)` pairs, of which v1's own relevance filter
keeps 80 and only **one** is distinct. The rest are reads of `/usr/bin/dirname`,
`/etc/ld.so.cache`, `libc.so.6` and friends — invisible to `list_dir`/`read_file`/`stat_path`
and irrelevant to a specification. Scored raw, `dirname` recall would be capped near 12%
however perfectly the model observed. The projection is therefore a correctness requirement,
not a convenience, and it is **v1's own semantics** (`tracer/data.py::__readwrite`) rather
than something invented here: reads outside the sandbox are dropped, writes are kept unless
they are under `/proc` or a null device, and a `.jpg` suffix is stripped.

**Two tiers, never summed.** v1's `FSInteraction.modified` split is exactly the boundary
that matters for a black-box observer:

* ``core`` — ``ad md de mo wf rd``. Every one is recoverable from a pre/post listing, a type
  check, or the command's own streams. A miss here is a model failure.
* ``inference`` — ``rf``. A read leaves no trace a prober can see directly; it can only be
  inferred from output content or from an error when the file is absent. A miss here is at
  least partly a limit of the observation model, and the record says so.

Adding them would make the score a function of how many files the command happens to read.

**Distinct pairs, not multiset.** strace records `libc.so.6` three times for one `arch` run
because the loader opens it three times. A model reporting it once is not wrong. v1's own
filter builds `set()`s for the same reason.

**No `Path.resolve()` anywhere.** Resolving is what makes v1's annotator unrunnable on
macOS: `/tmp` is a symlink to `/private/tmp`, so resolving moves every path out from under
the sandbox prefix it is about to be compared against.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from . import methods

METHOD = methods.TRACE_RECOVERY_DIFF.method
INSTRUMENT = "projected_fs_interactions"

#: State changes. Recoverable through the stage-3 tool surface.
CORE_ACTIONS = ("ad", "md", "de", "mo", "wf", "rd")
#: Reads. Not directly observable; inferable at best.
INFERENCE_ACTIONS = ("rf",)

STREAMS = ("stdin", "stdout", "stderr")
NULL_DEVICES = ("/dev/null", "/dev/zero")

#: v1's placeholder sandbox, hardcoded in its annotator. Used when a config carries no
#: sandbox of its own.
PLACEHOLDER_SANDBOX = "/tmp/sandbox_outer/sandbox_inner"

_PROC_PID = re.compile(r"^/proc/\d+(/|$)")

PROJECTION_RULE = (
    "v1's own CommandInvocationTraces.__readwrite (tracer/data.py): reads outside the "
    "sandbox dropped, writes under /proc or to a null device dropped, '.jpg' stripped, "
    "paths made sandbox-relative. Applied without Path.resolve()."
)


@dataclass
class Projection:
    """One side's interactions after v1's relevance filter, with what was removed."""

    pairs: set[tuple[str, str]] = field(default_factory=set)
    raw_count: int = 0
    kept_count: int = 0
    system_paths_excluded: int = 0
    proc_paths_normalized: int = 0
    null_device_writes_excluded: int = 0
    #: Relative paths naming a top-level system directory. v1 itself leaks these when a
    #: command runs with cwd `/` — `groups` yields ('rf', 'etc'). Counted so reference noise
    #: is visible rather than charged to the model.
    suspected_reference_leakage: int = 0


_SYSTEM_ROOTS = frozenset(
    {"etc", "usr", "lib", "lib64", "bin", "sbin", "proc", "sys", "dev", "var", "opt", "run"}
)


def normalize_path(path: str, sandbox: str) -> str | None:
    """A path made sandbox-relative, or `None` if it is not part of the scored set.

    Deliberately string-prefix work: see the module docstring on `Path.resolve()`.
    """
    if path in STREAMS:
        return path
    if _PROC_PID.match(path):
        path = re.sub(r"^/proc/\d+", "/proc/<pid>", path)
    if sandbox and path == sandbox:
        return "."
    if sandbox and path.startswith(sandbox.rstrip("/") + "/"):
        return path[len(sandbox.rstrip("/")) + 1 :].removesuffix(".jpg")
    if not path.startswith("/"):
        return path.removesuffix(".jpg")
    return None  # absolute, outside the sandbox


def project(traces: list[Any], sandbox: str) -> Projection:
    """Apply v1's relevance filter to one configuration's `(action, path)` list."""
    result = Projection()
    for entry in traces or []:
        if not entry or len(entry) < 2:
            continue
        action, path = str(entry[0]), str(entry[1])
        result.raw_count += 1

        if path in STREAMS:
            result.pairs.add((action, path))
            result.kept_count += 1
            continue

        is_write = action in CORE_ACTIONS
        if is_write and path in NULL_DEVICES:
            result.null_device_writes_excluded += 1
            continue

        if _PROC_PID.match(path):
            result.proc_paths_normalized += 1

        normalized = normalize_path(path, sandbox)
        if normalized is None:
            # Absolute and outside the sandbox. v1 drops these on reads outright; on writes
            # it keeps them unless they are under /proc.
            if is_write and not path.startswith("/proc"):
                result.pairs.add((action, path.removesuffix(".jpg")))
                result.kept_count += 1
            else:
                result.system_paths_excluded += 1
            continue

        if normalized.split("/")[0] in _SYSTEM_ROOTS:
            result.suspected_reference_leakage += 1

        result.pairs.add((action, normalized))
        result.kept_count += 1
    return result


def _sandbox_of(config: dict[str, Any]) -> str:
    """The sandbox root a configuration ran in, read off its own arguments."""
    for node in (config.get("command") or {}).get("body", []) or []:
        for arg in node.get("args") or []:
            sandbox = arg.get("sandbox")
            if sandbox:
                return str(sandbox)
    return PLACEHOLDER_SANDBOX


def _configs(traces_payload: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Every configuration in a `Traces` file, keyed by the invocation it ran."""
    out: dict[str, list[dict[str, Any]]] = {}
    for group in traces_payload or []:
        key = group.get("true_str", "")
        out.setdefault(key, []).extend(group.get("configs") or [])
    return out


def _prf(tp: int, fp: int, fn: int) -> dict[str, Any]:
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (
        (2 * precision * recall / (precision + recall))
        if (precision and recall and (precision + recall))
        else (0.0 if (precision is not None and recall is not None) else None)
    )
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def _tier(
    pairs: list[tuple[set[tuple[str, str]], set[tuple[str, str]]]], actions: tuple[str, ...]
) -> dict[str, Any]:
    """Micro (pooled) and macro (per-configuration mean) scores for one tier."""
    wanted = set(actions)
    tp = fp = fn = 0
    per_config: list[tuple[float | None, float | None]] = []
    for produced, reference in pairs:
        left = {p for p in produced if p[0] in wanted}
        right = {p for p in reference if p[0] in wanted}
        hit, miss, extra = len(left & right), len(right - left), len(left - right)
        tp += hit
        fp += extra
        fn += miss
        cell = _prf(hit, extra, miss)
        per_config.append((cell["precision"], cell["recall"]))

    def mean(values: list[float | None]) -> float | None:
        present = [v for v in values if v is not None]
        return (sum(present) / len(present)) if present else None

    macro_p = mean([p for p, _ in per_config])
    macro_r = mean([r for _, r in per_config])
    macro_f1 = (
        (2 * macro_p * macro_r / (macro_p + macro_r))
        if (macro_p and macro_r and (macro_p + macro_r))
        else (0.0 if (macro_p is not None and macro_r is not None) else None)
    )
    return {
        "actions": list(actions),
        "micro": _prf(tp, fp, fn),
        "macro": {"precision": macro_p, "recall": macro_r, "f1": macro_f1, "n": len(per_config)},
    }


def compare_traces(
    produced: list[dict[str, Any]],
    reference: list[dict[str, Any]] | None,
    *,
    command: str,
    reference_source: str | None = None,
    reference_runner: str | None = None,
) -> dict[str, Any]:
    """Score v2's observed interactions against v1's strace-derived ones."""
    record = methods.envelope(
        METHOD,
        INSTRUMENT,
        command=command,
        reference_source=reference_source,
        reference_runner=reference_runner,
    )
    if reference is None:
        record.update(
            {
                "available": False,
                "error": "no v1 strace reference for these configurations",
                "note": (
                    "the reference has to be generated by running v1's own tracer on the "
                    "identical configurations; it cannot be synthesized here"
                ),
            }
        )
        return record

    produced_configs, reference_configs = _configs(produced), _configs(reference)
    left_projection, right_projection = Projection(), Projection()
    aligned: list[tuple[set[tuple[str, str]], set[tuple[str, str]]]] = []
    unpaired_produced = unpaired_reference = 0

    def merge(into: Projection, part: Projection) -> None:
        into.raw_count += part.raw_count
        into.kept_count += part.kept_count
        into.system_paths_excluded += part.system_paths_excluded
        into.proc_paths_normalized += part.proc_paths_normalized
        into.null_device_writes_excluded += part.null_device_writes_excluded
        into.suspected_reference_leakage += part.suspected_reference_leakage

    for invocation, configs in produced_configs.items():
        counterparts = reference_configs.get(invocation)
        if not counterparts:
            unpaired_produced += len(configs)
            continue
        # Configurations under one invocation are compared pairwise by position; v1's
        # environment variants appear in a stable order on both sides.
        for index, config in enumerate(configs):
            if index >= len(counterparts):
                unpaired_produced += 1
                continue
            left = project(config.get("traces") or [], _sandbox_of(config))
            right = project(
                counterparts[index].get("traces") or [], _sandbox_of(counterparts[index])
            )
            merge(left_projection, left)
            merge(right_projection, right)
            aligned.append((left.pairs, right.pairs))
        unpaired_reference += max(0, len(counterparts) - len(configs))

    for invocation, configs in reference_configs.items():
        if invocation not in produced_configs:
            unpaired_reference += len(configs)

    core = _tier(aligned, CORE_ACTIONS)
    inference = _tier(aligned, INFERENCE_ACTIONS)
    inference["caveat"] = (
        "reads are not directly observable through list_dir/read_file/stat_path; a miss here "
        "is partly a limit of the observation model, not only a model failure"
    )

    by_action: dict[str, dict[str, int]] = {}
    for action in (*CORE_ACTIONS, *INFERENCE_ACTIONS):
        tp = fp = fn = 0
        for left_pairs, right_pairs in aligned:
            left = {p for p in left_pairs if p[0] == action}
            right = {p for p in right_pairs if p[0] == action}
            tp += len(left & right)
            fp += len(left - right)
            fn += len(right - left)
        by_action[action] = {"tp": tp, "fp": fp, "fn": fn}

    missing = sorted({p for left, right in aligned for p in (right - left)})[:20]
    spurious = sorted({p for left, right in aligned for p in (left - right)})[:20]

    record.update(
        {
            "available": True,
            "projection": {
                "rule": PROJECTION_RULE,
                "reference_raw_pairs": right_projection.raw_count,
                "reference_projected_pairs": right_projection.kept_count,
                "reference_distinct_projected": len({p for _, right in aligned for p in right}),
                "produced_raw_pairs": left_projection.raw_count,
                "produced_projected_pairs": left_projection.kept_count,
                "system_paths_excluded": right_projection.system_paths_excluded,
                "proc_paths_normalized": right_projection.proc_paths_normalized,
                "null_device_writes_excluded": right_projection.null_device_writes_excluded,
                "suspected_reference_leakage": right_projection.suspected_reference_leakage,
            },
            "configs": {
                "reference": sum(len(v) for v in reference_configs.values()),
                "produced": sum(len(v) for v in produced_configs.values()),
                "paired": len(aligned),
                "unpaired_produced": unpaired_produced,
                "unpaired_reference": unpaired_reference,
            },
            "core": core,
            "inference": inference,
            # The projection *is* the ceiling, which is what makes "fraction of the
            # recoverability ceiling achieved" computable rather than rhetorical.
            "ceiling_fraction": core["micro"]["recall"],
            "ceiling_units": core["micro"]["tp"] + core["micro"]["fn"],
            "by_action": by_action,
            "scoring_note": (
                "distinct (action, path) pairs, not a multiset: strace records one loader "
                "open three times per run, which is not three specification facts"
            ),
            "missing_sample": [list(p) for p in missing],
            "spurious_sample": [list(p) for p in spurious],
        }
    )
    return record


def self_test(traces_payload: list[dict[str, Any]], *, command: str) -> dict[str, Any]:
    """Score a traces file against itself, and against a PID-shifted copy of itself.

    The PID case pins the `/proc/<pid>/maps` normalization: a trace taken in a different
    process must not score as a different trace.
    """
    identity = compare_traces(traces_payload, traces_payload, command=command)

    def shift_pids(payload: Any) -> Any:
        if isinstance(payload, list):
            return [shift_pids(item) for item in payload]
        if isinstance(payload, dict):
            return {key: shift_pids(value) for key, value in payload.items()}
        if isinstance(payload, str):
            return re.sub(r"^/proc/\d+", "/proc/99999", payload)
        return payload

    shifted = compare_traces(shift_pids(traces_payload), traces_payload, command=command)
    return {
        "command": command,
        "identity": {
            "core_recall": identity["core"]["micro"]["recall"],
            "inference_recall": identity["inference"]["micro"]["recall"],
            "passed": identity["core"]["micro"]["recall"] in (1.0, None)
            and identity["inference"]["micro"]["recall"] in (1.0, None),
        },
        "pid_shifted": {
            "core_recall": shifted["core"]["micro"]["recall"],
            "inference_recall": shifted["inference"]["micro"]["recall"],
            "passed": shifted["core"]["micro"]["recall"] in (1.0, None)
            and shifted["inference"]["micro"]["recall"] in (1.0, None),
        },
        "projection": identity["projection"],
    }
