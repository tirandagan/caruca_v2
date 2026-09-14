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
from . import score as score_module
from . import sweep as sweep_module

# Fixed so an aggregation is reproducible: the same ledger yields the same interval.
BOOTSTRAP_SEED = 20260908
BOOTSTRAP_RESAMPLES = 10_000


def load_ledger(
    campaign_id: str, ledger_root: Path = sweep_module.DEFAULT_LEDGER_ROOT
) -> list[dict[str, Any]]:
    """Every recorded cell for a campaign, in the order it ran."""
    path = ledger_root / campaign_id / "ledger.jsonl"
    if not path.is_file():
        raise CarucaV2Error(
            f"no ledger at {path}. Run the campaign first, or pass --ledger-root."
        )
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
        arm = arms.setdefault(
            key, Arm(model=key[0], prompt_variant=key[1], temperature=key[2])
        )
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
        if score.get("scoreable") and score.get("f1") is not None:
            arm.scoreable += 1
            arm.f1.values.append(float(score["f1"]))
            arm.per_command.setdefault(row.get("command", "?"), []).append(
                float(score["f1"])
            )
            if score.get("exact_argument_rate") is not None:
                arm.exact.values.append(float(score["exact_argument_rate"]))

    return list(arms.values())


def consistency(arm: Arm) -> dict[str, Any] | None:
    """How much an arm's quality moves when only the sampling changes.

    Evaluation dimension 4 (consistency across repeated runs) is a result in its own right:
    v1 is deterministic given its inputs, so any spread here is a cost of the LLM approach
    that v1 does not pay. Only commands sampled more than once contribute.
    """
    repeated = {
        command: values for command, values in arm.per_command.items() if len(values) > 1
    }
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


def comparison_records(
    arms: Sequence[Arm], campaign_id: str, method: str = score_module.METHOD
) -> list[dict[str, Any]]:
    """Arms rendered as the comparison records the telemetry schema defines.

    `v1_value` is deliberately absent: this module compares v2 arms with each other. A
    v1-versus-v2 percent change is only meaningful once the v1 side has been measured by the
    same `method`, and inventing a denominator here would produce exactly the blended
    figure the schema's `method` tag exists to prevent.
    """
    commit = v1.v1_commit()
    records = []
    for arm in arms:
        summary = arm.f1.summary()
        records.append(
            {
                "campaign_id": campaign_id,
                "arm": arm.name,
                "dimension": "correctness",
                "comparison_system": "caruca_v2",
                "profile": "v1_faithful",
                "method": method,
                "v1_value": None,
                "v2_value": None if summary is None else summary["mean"],
                "n_samples": 0 if summary is None else summary["n"],
                "exact_match": None if summary is None else summary["min"] == 1.0,
                "percent_change": None,
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


def rescore(rows: Iterable[dict[str, Any]], reference: str) -> list[dict[str, Any]]:
    """Re-run the current scorer over each cell's saved output.

    A ledger's `score` is whatever the scorer said on the day the campaign ran, so a later
    scorer fix would otherwise be invisible until the campaign was re-run — paying again for
    model output that is already on disk. The artifacts are the durable record; scores are
    derived. Cells whose output is gone are marked unscoreable rather than silently kept at
    their old value.
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

        spec_path = Path(run_dir) / f"{v1.slug(command)}.py"
        if not spec_path.is_file():
            updated["score"] = {"scoreable": False, "error": f"no output at {spec_path}"}
            rescored.append(updated)
            continue

        try:
            record = score_module.score_spec(command, spec_path, reference=reference)
        except CarucaV2Error as exc:
            updated["score"] = {"scoreable": False, "error": str(exc)}
        else:
            updated["score"] = {
                "scoreable": record.get("scoreable"),
                "f1": record.get("f1"),
                "exact_argument_rate": record.get("exact_argument_rate"),
                "counts": record.get("counts"),
                "error": record.get("error"),
            }
        rescored.append(updated)
    return rescored


def build(
    campaign_id: str,
    ledger_root: Path = sweep_module.DEFAULT_LEDGER_ROOT,
    *,
    rescore_with: str | None = None,
) -> dict[str, Any]:
    """The full aggregation for one campaign.

    `rescore_with` names a scorer reference (`v1-specs` / `ground-truth`) to re-derive every
    score from the saved artifacts instead of trusting what the ledger recorded at run time.
    """
    rows = load_ledger(campaign_id, ledger_root)
    if rescore_with is not None:
        rows = rescore(rows, rescore_with)
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
        "comparison_records": comparison_records(arms, campaign_id),
        "table": render_table(arms),
    }
