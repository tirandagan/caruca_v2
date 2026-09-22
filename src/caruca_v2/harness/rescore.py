"""Score a completed run from its artifacts, whichever stage produced it.

The stage-agnostic successor to `report.rescore`'s syntax-spec-only path. A run directory
plus its manifest carries everything needed: the stage, the command, the bounds that were
stated to the model, and the artifact itself. That means a comparison can be re-derived long
after the run — including for stages that were never scored when they ran, which is every
stage but the first.

Each stage dispatches to its own module, and each module owns one `method`. Nothing here
averages across them.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .. import v1
from ..errors import CarucaV2Error
from . import annotation, config_env, invocation, methods, trace_recovery
from . import score as score_module

#: What each stage's scorer compares against, first entry being the default.
REFERENCES: dict[str, tuple[str, ...]] = {
    "syntax_spec": (score_module.REFERENCE_V1_SPECS, score_module.REFERENCE_GROUND_TRUTH),
    "generate": ("v1-enumeration",),
    "trace": ("v1-strace",),
    "annotate": ("v1-same-traces", "ground-truth"),
}


def default_reference(stage: str) -> str | None:
    options = REFERENCES.get(stage)
    return options[0] if options else None


def _manifest(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "manifest.json"
    if not path.is_file():
        raise CarucaV2Error(f"no manifest.json in {run_dir}")
    return json.loads(path.read_text())


def _artifact(run_dir: Path, *names: str) -> Path | None:
    for name in names:
        candidate = run_dir / name
        if candidate.is_file():
            return candidate
    return None


def _bounds(manifest: dict[str, Any]) -> dict[str, Any]:
    """The bounds stated to the model, so v1's side can be generated to match.

    Not cosmetic: `mkdir` at arity 1 yields 44 invocations at `--max-count 1` and 4,240 at
    v1's default of 4. Generating the reference with different bounds measures the bounds.
    """
    inputs = manifest.get("inputs") or {}
    return {
        "max_arity": inputs.get("max_arity", 1),
        "max_count": inputs.get("max_count", 4),
        "skip": inputs.get("skip_flags"),
        "stdin_variation": inputs.get("stdin_variation", "simple"),
        "content_variation": inputs.get("content_variation", "simple"),
    }


def _score_syntax_spec(run_dir: Path, manifest: dict, command: str, reference: str) -> dict:
    spec = _artifact(run_dir, f"{v1.slug(command)}.py")
    if spec is None:
        return {"scoreable": False, "error": "no spec file was written"}
    return score_module.score_spec(command, spec, reference=reference)


def _score_generate(run_dir: Path, manifest: dict, command: str, reference: str) -> dict:
    """Both stage-2 comparisons: the invocation set, and the environments requested."""
    configs = _artifact(run_dir, f"{v1.slug(command)}.configs.json")
    invocations_file = _artifact(run_dir, f"{v1.slug(command)}.invocations.txt")
    if invocations_file is None:
        return {"scoreable": False, "error": "no invocations file was written"}

    bounds = _bounds(manifest)
    produced = [line for line in invocations_file.read_text().splitlines() if line.strip()]
    reference_invocations = v1.reference_invocations(
        command,
        max_arity=bounds["max_arity"],
        max_count=bounds["max_count"],
        skip=bounds["skip"],
    )
    record = invocation.compare_invocation_sets(
        produced, reference_invocations, command=command, bounds=bounds
    )

    # The environment comparison needs the configs paired back to their invocations. The
    # artifact is a flat list in the same order the invocations file records.
    if configs is not None:
        payload = json.loads(configs.read_text())
        by_invocation: dict[str, list[dict[str, Any]]] = {}
        for text, config in zip(produced, payload, strict=False):
            by_invocation.setdefault(text, []).append(config)
        reference_configs = v1.reference_configs(
            command,
            max_arity=bounds["max_arity"],
            max_count=bounds["max_count"],
            skip=bounds["skip"],
            stdin_variation=bounds["stdin_variation"],
            content_variation=bounds["content_variation"],
        )
        record["config_comparison"] = config_env.compare_config_sets(
            by_invocation, reference_configs, command=command, bounds=bounds
        )
    return record


def _score_trace(
    run_dir: Path, manifest: dict, command: str, reference: str, reference_path: Path | None = None
) -> dict:
    """Score v2's observed interactions against v1's strace record.

    `reference_path` is explicit because v1's default (`caruca/outputs/<cmd>.json`) exists for
    only 18 commands, none of which overlap the set that has ground-truth annotations. A
    parity campaign traces commands whose v1 reference had to be generated for it, so without
    a way to name that file every cell scores as unscoreable — which is exactly what happened
    to all 12 successful stage-3 cells of the first run.
    """
    produced = _artifact(run_dir, f"{v1.slug(command)}.traces.json")
    if produced is None:
        return {"scoreable": False, "error": "no traces file was written"}
    resolved = reference_path or v1.traces_path(command)
    payload = json.loads(resolved.read_text()) if resolved.is_file() else None
    return trace_recovery.compare_traces(
        json.loads(produced.read_text()),
        payload,
        command=command,
        reference_source=str(resolved) if payload is not None else None,
    )


def _score_annotate(run_dir: Path, manifest: dict, command: str, reference: str) -> dict:
    fmt = ((manifest.get("checks") or {}).get("format")) or (
        (manifest.get("inputs") or {}).get("format")
    )
    if not fmt:
        return {"scoreable": False, "error": "the manifest does not record which format ran"}
    produced = _artifact(run_dir, f"{v1.slug(command)}.{fmt}.annotation")
    if produced is None:
        return {"scoreable": False, "error": "no annotation file was written"}
    text = produced.read_text()

    if reference == "ground-truth":
        return annotation.compare_annotation(
            fmt,
            text,
            v1.ground_truth_annotation(command, fmt),
            label="hand-curated ground truth",
            reference_kind=annotation.REFERENCE_GROUND_TRUTH,
        )
    # v1's own annotator on the identical traces. Needs v1 runnable, which on macOS means
    # Lima — v1's annotator cannot run on a Mac at all.
    traces_source = (manifest.get("inputs") or {}).get("traces_source")
    if not traces_source:
        return {"scoreable": False, "error": "the manifest does not record its traces source"}
    outcome = v1.reference_annotation(command, fmt, Path(traces_source))
    if not outcome.available:
        return {"scoreable": False, "error": outcome.error, "runner": outcome.runner}
    return annotation.compare_annotation(
        fmt,
        text,
        outcome.text,
        label="v1 on identical traces",
        reference_kind=annotation.REFERENCE_V1_SAME_TRACES,
    )


_DISPATCH = {
    "syntax_spec": _score_syntax_spec,
    "generate": _score_generate,
    "trace": _score_trace,
    "annotate": _score_annotate,
}


def score_run(
    run_dir: Path,
    *,
    stage: str | None = None,
    reference: str | None = None,
    reference_path: Path | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Re-derive a run's comparison from its artifacts.

    Failures are returned as records, not raised: one unscoreable cell must not sink a
    campaign's aggregation.
    """
    run_dir = Path(run_dir)
    # The manifest is the normal source of stage and command, but it is not required when the
    # caller already knows them — a ledger row carries both. That lets a run directory pruned
    # down to its artifact still be re-scored, which matters while the retention rule is open.
    try:
        manifest = _manifest(run_dir)
    except CarucaV2Error as exc:
        if not (stage and command):
            return {"scoreable": False, "error": str(exc)}
        manifest = {}

    resolved_stage = stage or manifest.get("stage")
    command = command or manifest.get("command")
    if resolved_stage not in _DISPATCH:
        return {"scoreable": False, "error": f"no scorer for stage {resolved_stage!r}"}
    if not command:
        return {"scoreable": False, "error": "the manifest does not record a command"}

    resolved_reference = reference or default_reference(resolved_stage)
    scorer = _DISPATCH[resolved_stage]
    extra = {"reference_path": reference_path} if resolved_stage == "trace" else {}
    try:
        record = scorer(run_dir, manifest, command, resolved_reference, **extra)
    except CarucaV2Error as exc:
        return {"scoreable": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001 - a scorer crash is a result, not a run failure
        return {"scoreable": False, "error": f"{type(exc).__name__}: {exc}"}

    record.setdefault("scoreable", record.get("available", True))
    record.setdefault("method", methods.PRIMARY_BY_STAGE.get(resolved_stage))
    record.setdefault("reference", resolved_reference)
    return record


def ledger_entry(record: dict[str, Any]) -> dict[str, Any]:
    """The subset a campaign ledger carries, keyed so `report.py` can find it per method.

    Every metric the record's method declares is copied through, so aggregation never has to
    know which stage produced the row.
    """
    method = record.get("method")
    entry: dict[str, Any] = {
        "scoreable": record.get("scoreable"),
        "method": method,
        "instrument": record.get("instrument"),
        "reference": record.get("reference"),
        "error": record.get("error"),
        "counts": record.get("counts"),
    }
    if method and method in methods.REGISTRY:
        for metric in methods.get(method).metrics:
            value: Any = record
            for part in metric.split("."):
                value = value.get(part) if isinstance(value, dict) else None
            entry[metric] = value
    # Stage 2 carries a second method in the same row; keep it whole rather than flattening
    # two denominators together.
    if "config_comparison" in record:
        entry["config_comparison"] = {
            "method": record["config_comparison"].get("method"),
            "env_agreement_rate": record["config_comparison"].get("env_agreement_rate"),
            "rates": record["config_comparison"].get("rates"),
        }
    return entry
