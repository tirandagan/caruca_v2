"""Campaign aggregation: ledgers in, comparison tables and records out.

Three rules this module exists to enforce:

* **Small samples are reported as small samples.** Configuration selection runs three to
  ten samples per cell. A mean with a normal-approximation interval implies a precision
  that many observations cannot carry, so every arm reports `n`, the median, the full
  range, and a bootstrap interval — and the raw per-sample values stay in the record so a
  reader can see the spread rather than trust a summary of it.
* **Nothing is blended across comparison methods.** Every figure carries the `method` tag
  from `ai_docs/prep/data_telemetry_schema.md` (`q2_syntax_diff`, `annotation_diff`,
  `q1_execution`). Two numbers produced by different methods are never averaged together.
* **Absence is reported, not dropped.** Cells that errored, produced nothing, or could not
  be scored are counted and named. An arm's quality figure states how many cells it rests
  on, so a high mean over two survivors cannot be mistaken for a high mean over ten.
"""

from __future__ import annotations

import json
import random
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import v1
from ..errors import CarucaV2Error
from . import methods
from . import rescore as rescore_module
from . import score as score_module
from . import sweep as sweep_module

#: Passed to `--rescore` when the caller wants each stage's own default reference rather than
#: naming one. Stage 1 has two (`v1-specs`, `ground-truth`); the others have exactly one.
RESCORE_DEFAULT = "stage-default"

# Fixed so an aggregation is reproducible: the same ledger yields the same interval.
BOOTSTRAP_SEED = 20260908
BOOTSTRAP_RESAMPLES = 10_000


def load_ledger(
    campaign_id: str, ledger_root: Path = sweep_module.DEFAULT_LEDGER_ROOT
) -> list[dict[str, Any]]:
    """Every recorded cell for a campaign, in the order it ran."""
    path = ledger_root / campaign_id / "ledger.jsonl"
    if not path.is_file():
        raise CarucaV2Error(f"no ledger at {path}. Run the campaign first, or pass --ledger-root.")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


@dataclass
class Distribution:
    """A metric's spread over the cells that produced it."""

    values: list[float] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.values)

    def summary(self) -> dict[str, Any] | None:
        """None when nothing was measured — an empty arm must not report a zero."""
        if not self.values:
            return None
        ordered = sorted(self.values)
        low, high = bootstrap_interval(ordered)
        return {
            "n": len(ordered),
            "mean": statistics.fmean(ordered),
            "median": statistics.median(ordered),
            "min": ordered[0],
            "max": ordered[-1],
            "stdev": statistics.stdev(ordered) if len(ordered) > 1 else 0.0,
            "ci95_low": low,
            "ci95_high": high,
            "values": ordered,
        }


def bootstrap_interval(
    values: Sequence[float], confidence: float = 0.95
) -> tuple[float | None, float | None]:
    """Percentile bootstrap interval for the mean.

    Chosen over a t-interval because these samples are small, bounded to [0, 1], and often
    skewed (many perfect scores, a few failures) — conditions where a symmetric interval
    can run past the ends of the scale and imply precision the data does not have. A single
    observation has no interval at all, which is reported as `None` rather than as a point.
    """
    if len(values) < 2:
        return (None, None)
    rng = random.Random(BOOTSTRAP_SEED)
    size = len(values)
    means = sorted(
        statistics.fmean(rng.choices(values, k=size)) for _ in range(BOOTSTRAP_RESAMPLES)
    )
    tail = (1.0 - confidence) / 2.0
    return (
        means[int(tail * BOOTSTRAP_RESAMPLES)],
        means[min(int((1.0 - tail) * BOOTSTRAP_RESAMPLES), BOOTSTRAP_RESAMPLES - 1)],
    )


@dataclass
class Arm:
    """One experimental condition: a model, a wording, and a temperature."""

    model: str
    prompt_variant: str
    temperature: float

    cells: int = 0
    ok: int = 0
    failed: int = 0
    errored: int = 0
    validated: int = 0
    scoreable: int = 0
    cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    f1: Distribution = field(default_factory=Distribution)
    exact: Distribution = field(default_factory=Distribution)
    per_command: dict[str, list[float]] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return sweep_module.arm_name(self.model, self.prompt_variant)

    @property
    def key(self) -> tuple[str, str, float]:
        return (self.model, self.prompt_variant, self.temperature)

    def first_pass_validity(self) -> float | None:
        """Fraction of cells whose very first response v1 accepted.

        This is the quantity v1's retry loop existed to paper over, so it is reported in its
        own right rather than folded into the quality figure.
        """
        produced = self.ok + self.failed
        return self.validated / produced if produced else None

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.name,
            "model": self.model,
            "prompt_variant": self.prompt_variant,
            "temperature": self.temperature,
            "cells": self.cells,
            "ok": self.ok,
            "failed": self.failed,
            "errored": self.errored,
            "first_pass_validity": self.first_pass_validity(),
            "scored_cells": self.scoreable,
            "f1": self.f1.summary(),
            "exact_argument_rate": self.exact.summary(),
            "cost_usd": round(self.cost_usd, 6),
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "cost_per_scored_cell": (
                round(self.cost_usd / self.scoreable, 6) if self.scoreable else None
            ),
        }


def aggregate(rows: Iterable[dict[str, Any]]) -> list[Arm]:
    """Group ledger rows into arms. Order follows first appearance, i.e. run order."""
    arms: dict[tuple[str, str, float], Arm] = {}

    for row in rows:
        key = (
            row.get("model", "unknown"),
            row.get("prompt_variant", "default"),
            float(row.get("temperature", 0.0)),
        )
        arm = arms.setdefault(key, Arm(model=key[0], prompt_variant=key[1], temperature=key[2]))
        arm.cells += 1

        status = row.get("status")
        if status == "ok":
            arm.ok += 1
        elif status == "error":
            arm.errored += 1
        else:
            arm.failed += 1

        if row.get("validation_passed"):
            arm.validated += 1
        arm.cost_usd += float(row.get("cost_usd") or 0.0)
        arm.prompt_tokens += int(row.get("prompt_tokens") or 0)
        arm.completion_tokens += int(row.get("completion_tokens") or 0)

        score = row.get("score") or {}
        # Read the metric this row's own method declares, not `f1`. Stage 3's headline is
        # `core.micro.f1` and stage 4's is `agreement.fully_agreeing`; neither has an `f1`
        # key, so a hardcoded lookup silently drops every non-stage-1 cell from the
        # aggregation — which is why `report` showed nothing for those campaigns.
        headline = _headline_metric(score)
        if score.get("scoreable") and headline is not None:
            arm.scoreable += 1
            arm.f1.values.append(headline)
            arm.per_command.setdefault(row.get("command", "?"), []).append(headline)
            secondary = _secondary_metric(score)
            if secondary is not None:
                arm.exact.values.append(secondary)

    return list(arms.values())


def _metric(score: dict[str, Any], index: int) -> float | None:
    """The score's own method's metric at `index`, as a float, or None.

    A ledger row carries whichever metrics its method declares; `methods.REGISTRY` says which
    one leads. Falling back to `f1` keeps rows written before methods were tagged readable.
    """
    method = score.get("method")
    if method in methods.REGISTRY:
        names = methods.get(method).metrics
        if index < len(names):
            value = score.get(names[index])
            return None if value is None else float(value)
        return None
    legacy = ("f1", "exact_argument_rate")
    value = score.get(legacy[index]) if index < len(legacy) else None
    return None if value is None else float(value)


def _headline_metric(score: dict[str, Any]) -> float | None:
    return _metric(score, 0)


def _secondary_metric(score: dict[str, Any]) -> float | None:
    return _metric(score, 1)


def consistency(arm: Arm) -> dict[str, Any] | None:
    """How much an arm's quality moves when only the sampling changes.

    Evaluation dimension 4 (consistency across repeated runs) is a result in its own right:
    v1 is deterministic given its inputs, so any spread here is a cost of the LLM approach
    that v1 does not pay. Only commands sampled more than once contribute.
    """
    repeated = {command: values for command, values in arm.per_command.items() if len(values) > 1}
    if not repeated:
        return None
    spreads = [max(values) - min(values) for values in repeated.values()]
    identical = sum(1 for values in repeated.values() if len(set(values)) == 1)
    return {
        "commands_sampled_more_than_once": len(repeated),
        "identical_across_samples": identical,
        "identical_rate": identical / len(repeated),
        "mean_spread": statistics.fmean(spreads),
        "max_spread": max(spreads),
    }


#: Why a v1 number is or is not present, and whether a delta may be derived from it.
V1_REFERENCE = "reference"  # v1 *defines* the scale; it scores 1.0 by construction
V1_MEASURED = "measured"  # v1 was measured independently, by the same method
V1_CONSTANT = "constant"  # v1 is deterministic here, so the value is known without measuring
V1_UNAVAILABLE = "unavailable"  # the v1 side has not been measured yet

#: Methods where v1 is the reference. A percent change against a reference is an identity
#: wearing a hat: v1 scores 1.0 by construction, so `(v2 - 1) / 1` is just `v2 - 1`, and
#: publishing it invites "v2 is N% worse than v1" claims derived from nothing.
REFERENCE_METHODS = frozenset(
    {
        methods.INVOCATION_SET_DIFF.method,
        methods.CONFIG_ENV_DIFF.method,
        methods.TRACE_RECOVERY_DIFF.method,
    }
)

_REFERENCE_NOTE = (
    "v1's own output defines the reference set for this method; v1 scores 1.0 by "
    "construction, so a percent change against it is an identity, not a comparison"
)


@dataclass(frozen=True)
class V1Side:
    """The v1 half of a comparison, and whether a delta may be computed from it."""

    value: float | None
    kind: str
    source: str | None = None
    note: str | None = None


def v1_side(
    method: str,
    *,
    reference_kind: str | None = None,
    measured: float | None = None,
    source: str | None = None,
) -> V1Side:
    """Resolve what belongs in `v1_value` for one method.

    The rule this encodes: **a percent change is meaningful only when both sides are
    independently measured values of the same quantity by the same method, and the v1 side
    is not the reference that defines the scale.**

    Where a delta IS meaningful:

    * `q2_syntax_diff` — v1 has its own LLM step, and its output is committed at
      `outputs/llm-dsl-generation/`. Measured 2026-09-14 it scores **78/116** by v1's own
      `cmp_specs`, not the paper's 116/120; see `memory/caruca_v1_stage1_baseline.md`.
    * `annotation_diff` against **ground truth** — both annotators are scored against a third
      party, and v1 is not guaranteed 1.0: E0 found v1 on `main` deriving "side-effectful"
      for `cp` where the paper says "pure".
    * cost and wall-clock, once v1's side has actually been measured.
    """
    if method in REFERENCE_METHODS:
        return V1Side(value=None, kind=V1_REFERENCE, note=_REFERENCE_NOTE)

    if method == methods.ANNOTATION_DIFF.method and reference_kind != "ground_truth":
        return V1Side(value=None, kind=V1_REFERENCE, note=_REFERENCE_NOTE)

    if measured is None:
        return V1Side(
            value=None,
            kind=V1_UNAVAILABLE,
            note="the v1 side of this method has not been measured yet",
        )
    return V1Side(value=measured, kind=V1_MEASURED, source=source)


def percent_change(side: V1Side, v2_value: float | None) -> float | None:
    """A delta, or `None` when one would be meaningless.

    Enforcement rather than a docstring promise: there is no path through this function that
    produces a number for a method where v1 is the reference.
    """
    if side.kind != V1_MEASURED or not side.value or v2_value is None:
        return None
    return (v2_value - side.value) / side.value


def method_of(rows: Sequence[dict[str, Any]]) -> str:
    """The comparison method a campaign's rows were scored by.

    Read from the rows rather than defaulting to stage 1's: a report that labels a trace
    campaign `q2_syntax_diff` is claiming a denominator of "arguments in the reference
    specification" for a number counted in filesystem interactions.
    """
    for row in rows:
        method = (row.get("score") or {}).get("method")
        if method in methods.REGISTRY:
            return method
    for row in rows:
        primary = methods.PRIMARY_BY_STAGE.get(row.get("stage") or "")
        if primary:
            return primary
    return score_module.METHOD


def comparison_records(
    arms: Sequence[Arm],
    campaign_id: str,
    method: str = score_module.METHOD,
    *,
    reference_kind: str | None = None,
    v1_measured: float | None = None,
    v1_source: str | None = None,
) -> list[dict[str, Any]]:
    """Arms rendered as the comparison records the telemetry schema defines.

    `v1_value` is filled only where it can be filled honestly. `v1_value_kind` says which
    case applies, so an absent number reads as a decision rather than an oversight.
    """
    commit = v1.v1_commit()
    spec = methods.get(method)
    side = v1_side(
        method, reference_kind=reference_kind, measured=v1_measured, source=v1_source
    )
    records = []
    for arm in arms:
        summary = arm.f1.summary()
        v2_value = None if summary is None else summary["mean"]
        records.append(
            {
                "campaign_id": campaign_id,
                "arm": arm.name,
                "dimension": "correctness",
                "comparison_system": "caruca_v2",
                "profile": "v1_faithful",
                "method": method,
                "instrument": spec.primary_instrument,
                "denominator": spec.denominator,
                "v1_value": side.value,
                "v1_value_kind": side.kind,
                "v1_value_source": side.source,
                "v1_value_note": side.note,
                "v2_value": v2_value,
                "match_rate": v2_value,
                "n_samples": 0 if summary is None else summary["n"],
                "exact_match": None if summary is None else summary["min"] == 1.0,
                "percent_change": percent_change(side, v2_value),
                "caruca_v1_commit": commit,
                "evidence_refs": [f"eval/campaigns/{campaign_id}/ledger.jsonl"],
            }
        )
    return records


def _fmt(value: float | None, places: int = 3) -> str:
    return "n/a" if value is None else f"{value:.{places}f}"


def render_table(arms: Sequence[Arm]) -> str:
    """A Markdown table for the write-up, one row per arm."""
    header = (
        "| Arm | Temp | Cells | First-pass valid | Mean F1 | 95% CI | Spread | "
        "Cost | $/scored cell |\n"
        "|---|---|---|---|---|---|---|---|---|"
    )
    lines = [header]
    for arm in sorted(arms, key=lambda a: (a.model, a.prompt_variant, a.temperature)):
        data = arm.as_dict()
        f1 = data["f1"]
        if f1 is None:
            quality, interval, spread = "n/a", "n/a", "n/a"
        else:
            quality = _fmt(f1["mean"])
            interval = (
                "single sample"
                if f1["ci95_low"] is None
                else f"{_fmt(f1['ci95_low'])}–{_fmt(f1['ci95_high'])}"
            )
            spread = f"{_fmt(f1['min'])}–{_fmt(f1['max'])}"
        per_cell = data["cost_per_scored_cell"]
        per_cell_text = "n/a" if per_cell is None else f"${per_cell:.4f}"
        lines.append(
            f"| {data['arm']} | {arm.temperature} | "
            f"{data['ok']}/{data['cells']} ok | "
            f"{_fmt(data['first_pass_validity'], 2)} | {quality} | {interval} | {spread} | "
            f"${data['cost_usd']:.4f} | {per_cell_text} |"
        )
    return "\n".join(lines)


def rescore(
    rows: Iterable[dict[str, Any]],
    reference: str | None = None,
    *,
    stage: str | None = None,
    reference_path_pattern: str | None = None,
) -> list[dict[str, Any]]:
    """Re-run the current scorer over each cell's saved output, whatever stage produced it.

    A ledger's `score` is whatever the scorer said on the day the campaign ran, so a later
    scorer fix would otherwise be invisible until the campaign was re-run — paying again for
    model output that is already on disk. The artifacts are the durable record; scores are
    derived. Cells whose output is gone are marked unscoreable rather than silently kept at
    their old value.

    This dispatches through `rescore_module.score_run`, so it covers all four stages. It was
    syntax-spec-only until 2026-09-20, which meant a scorer change could not be applied to an
    existing stage-2/3/4 campaign at all: the choice was re-running it or re-deriving the
    numbers by hand outside the harness. Stage 3's figures were published that way once.

    `reference_path_pattern` names v1's side per command for stages where it cannot be
    inferred — `{command}` is substituted. Stage 3 needs it because v1's default trace path
    exists for only 18 commands, none of which have hand-curated annotations.
    """
    rescored = []
    for row in rows:
        updated = dict(row)
        run_dir = row.get("run_dir")
        command = row.get("command")
        if not run_dir or not command:
            updated["score"] = {"scoreable": False, "error": "no run directory recorded"}
            rescored.append(updated)
            continue

        reference_path = (
            Path(reference_path_pattern.format(command=v1.slug(command), raw_command=command))
            if reference_path_pattern
            else None
        )
        # Prefer the reference this cell was actually scored against. Falling through to a
        # stage's first reference silently changes the question: an annotate campaign run
        # against the hand-curated ground truth would otherwise be rescored against v1's own
        # annotator, which needs Lima and answers something else entirely.
        recorded = (row.get("score") or {}).get("reference")
        record = rescore_module.score_run(
            Path(run_dir),
            stage=stage or row.get("stage"),
            reference=reference or recorded,
            reference_path=reference_path,
            command=command,
        )
        updated["score"] = rescore_module.ledger_entry(record)
        rescored.append(updated)
    return rescored


def build(
    campaign_id: str,
    ledger_root: Path = sweep_module.DEFAULT_LEDGER_ROOT,
    *,
    rescore_with: str | None = None,
    rescore_stage: str | None = None,
    reference_path_pattern: str | None = None,
) -> dict[str, Any]:
    """The full aggregation for one campaign.

    `rescore_with` names a scorer reference (`v1-specs` / `ground-truth`) to re-derive every
    score from the saved artifacts instead of trusting what the ledger recorded at run time.
    """
    rows = load_ledger(campaign_id, ledger_root)
    if rescore_with is not None:
        rows = rescore(
            rows,
            None if rescore_with == RESCORE_DEFAULT else rescore_with,
            stage=rescore_stage,
            reference_path_pattern=reference_path_pattern,
        )
    arms = aggregate(rows)
    return {
        "campaign_id": campaign_id,
        "cells_recorded": len(rows),
        "scores_from": (
            "ledger (as recorded at run time)"
            if rescore_with is None
            else f"rescored against {rescore_with} with the current scorer"
        ),
        "arms": [arm.as_dict() for arm in arms],
        "consistency": {arm.name: consistency(arm) for arm in arms},
        "comparison_records": comparison_records(arms, campaign_id, method_of(rows)),
        "table": render_table(arms),
    }
