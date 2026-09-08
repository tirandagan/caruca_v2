"""The campaign runner: (commands × models × temperatures × samples) over one stage.

Design rules, from task 006:

* **Transport failures are retried; content failures never are.** A connection error or
  a 429 means no model output was observed — no measurement happened, so the attempt is
  repeated with backoff and the attempt count recorded. A response that parses badly or
  fails v1's validation IS the measurement; it is recorded and never re-asked.
* **The freeze gate is code, not memory.** A campaign marked `post_freeze` refuses to
  run unless `eval_config.frozen.json` exists and matches, so the project's
  chosen-once-then-frozen rule cannot be drifted past by accident.
* **Budget brakes are belt-and-suspenders.** Every campaign file carries `max_runs` and
  `max_usd`; the runner stops at whichever trips first, independent of the approval
  that authorized the campaign.
* **Model comparison is first-class.** Cells run model-major (every cell of the first
  model, then the next), and the summary rolls results up per model, so "gpt-4o first,
  then claude-haiku-4.5 against it" is one campaign file, not two runs glued together.

Resume: each completed cell is a line in the campaign ledger
(`eval/campaigns/<id>/ledger.jsonl`). Re-running the same campaign skips cells already
in the ledger; run directories and sidecars remain the source of truth.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import openai
from openai import OpenAI
from pydantic import BaseModel, Field

from .. import llm, metrics_db
from ..errors import CarucaV2Error, SetupError
from ..stages import annotate as annotate_stage
from ..stages import generate as generate_stage
from ..stages import syntax_spec as syntax_stage
from ..stages import trace as trace_stage
from . import score as score_module

DEFAULT_FROZEN_CONFIG_PATH = Path("eval_config.frozen.json")
DEFAULT_LEDGER_ROOT = Path("eval/campaigns")

STAGES = ("syntax_spec", "generate", "trace", "annotate")

# Backoff for transport-level failures only. Five attempts, then the cell errors out.
BACKOFF_SECONDS = (1, 3, 7, 15, 30)


class Campaign(BaseModel):
    """One declarative campaign file — one stage, a cell grid, and its brakes."""

    campaign_id: str
    description: str = ""
    stage: str
    commands: list[str]
    models: list[str]
    temperatures: list[float]
    samples: int = 1
    seed: int | None = llm.DEFAULT_SEED
    max_tokens: int = llm.DEFAULT_MAX_TOKENS
    post_freeze: bool = False
    # C4-style campaigns vary the model deliberately after the freeze; they say so here
    # and the reason is recorded, instead of the gate being loosened for everyone.
    frozen_model_only: bool = True
    max_runs: int
    max_usd: float
    score_after: bool = False
    score_reference: str = score_module.REFERENCE_V1_SPECS
    stage_options: dict[str, Any] = Field(default_factory=dict)

    def validate_shape(self) -> None:
        if self.stage not in STAGES:
            raise SetupError(
                f"campaign {self.campaign_id}: unknown stage {self.stage!r}; "
                f"expected one of {STAGES}."
            )
        if self.stage == "annotate" and "format" not in self.stage_options:
            raise SetupError(
                f"campaign {self.campaign_id}: annotate campaigns must set "
                "stage_options.format (pash|posh|sash|shellcheck)."
            )
        if self.stage_options.get("isolation"):
            raise SetupError(
                f"campaign {self.campaign_id}: isolation backends are not wired into "
                "the sweep runner yet (they arrive with the per-stage campaign C5); "
                "run isolated traces through the CLI directly."
            )
        if not self.commands or not self.models or not self.temperatures:
            raise SetupError(
                f"campaign {self.campaign_id}: commands, models, and temperatures "
                "must all be non-empty."
            )


@dataclass(frozen=True)
class Cell:
    command: str
    model: str
    temperature: float
    sample: int

    @property
    def key(self) -> str:
        return f"{self.command}|{self.model}|{self.temperature}|{self.sample}"


def load_campaign(path: Path) -> Campaign:
    campaign = Campaign.model_validate_json(path.read_text())
    campaign.validate_shape()
    return campaign


def enumerate_cells(campaign: Campaign) -> list[Cell]:
    """Model-major order: the whole grid for the first model, then the next model."""
    return [
        Cell(command=command, model=model, temperature=temperature, sample=sample)
        for model in campaign.models
        for temperature in campaign.temperatures
        for command in campaign.commands
        for sample in range(campaign.samples)
    ]


def check_freeze_gate(campaign: Campaign, frozen_path: Path) -> None:
    if not campaign.post_freeze:
        return
    if not frozen_path.is_file():
        raise SetupError(
            f"campaign {campaign.campaign_id} is marked post_freeze but no frozen "
            f"configuration exists at {frozen_path}. Run configuration selection (C1) "
            "and freeze before any post-freeze campaign."
        )
    frozen = json.loads(frozen_path.read_text())
    if campaign.temperatures != [frozen["temperature"]]:
        raise SetupError(
            f"campaign {campaign.campaign_id}: temperatures {campaign.temperatures} do "
            f"not match the frozen temperature {frozen['temperature']}."
        )
    if campaign.frozen_model_only and campaign.models != [frozen["model"]]:
        raise SetupError(
            f"campaign {campaign.campaign_id}: models {campaign.models} do not match "
            f"the frozen model {frozen['model']!r}. Cross-model campaigns must set "
            "frozen_model_only: false and say why in their description."
        )


def _is_transient(exc: BaseException) -> bool:
    if isinstance(
        exc,
        openai.APIConnectionError | openai.APITimeoutError | openai.RateLimitError
        | openai.InternalServerError,
    ):
        return True
    status = getattr(exc, "status_code", None)
    return isinstance(exc, openai.APIStatusError) and status is not None and status >= 500


def _dispatch(
    campaign: Campaign,
    cell: Cell,
    *,
    out_root: Path,
    db_path: Path,
    client: OpenAI,
) -> tuple[str, str, str, bool | None, float, int, int]:
    """Run one cell through its stage. Returns
    (run_id, run_dir, status, validation_passed, cost, prompt_tokens, completion_tokens)."""
    options = campaign.stage_options
    common: dict[str, Any] = {
        "model": cell.model,
        "temperature": cell.temperature,
        "seed": campaign.seed,
        "max_tokens": campaign.max_tokens,
        "out_root": out_root,
        "db_path": db_path,
        "client": client,
    }

    if campaign.stage == "syntax_spec":
        docs = options.get("docs")
        result: Any = syntax_stage.run(
            cell.command, docs_path=None if docs is None else Path(docs), **common
        )
        records = [result.record]
    elif campaign.stage == "generate":
        result = generate_stage.run(
            cell.command,
            max_turns=int(options.get("max_turns", generate_stage.DEFAULT_MAX_TURNS)),
            max_arity=int(options.get("max_arity", generate_stage.V1_DEFAULT_MAX_ARITY)),
            max_count=int(options.get("max_count", generate_stage.V1_DEFAULT_MAX_COUNT)),
            compare=bool(options.get("compare", True)),
            **common,
        )
        records = result.records
    elif campaign.stage == "trace":
        result = trace_stage.run(
            cell.command,
            max_turns=int(options.get("max_turns", trace_stage.DEFAULT_MAX_TURNS)),
            limit=int(options.get("limit", trace_stage.DEFAULT_LIMIT)),
            isolation=None,
            **common,
        )
        records = result.records
    else:  # annotate — validate_shape guarantees format is present
        traces = options.get("traces")
        result = annotate_stage.run(
            cell.command,
            options["format"],
            max_turns=int(options.get("max_turns", annotate_stage.DEFAULT_MAX_TURNS)),
            traces_path=None if traces is None else Path(traces),
            compare=bool(options.get("compare", True)),
            v1_runner=str(options.get("v1_runner", "host")),
            **common,
        )
        records = result.records

    validation = result.validation
    return (
        result.run_id,
        str(result.run_dir),
        result.status,
        None if validation is None else validation.passed,
        sum(r.cost_usd for r in records),
        sum(r.prompt_tokens for r in records),
        sum(r.completion_tokens for r in records),
    )


def _spec_path_of(result_run_dir: str, command: str) -> Path:
    from .. import v1 as v1_module

    return Path(result_run_dir) / f"{v1_module.slug(command)}.py"


@dataclass
class CampaignReport:
    campaign_id: str
    cells_total: int = 0
    completed: int = 0
    skipped_resumed: int = 0
    failed_content: int = 0
    errored: int = 0
    transport_retries: int = 0
    cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    stopped_reason: str | None = None
    ledger_path: Path | None = None
    by_model: dict[str, dict[str, Any]] = field(default_factory=dict)
    dry_run_cells: list[str] = field(default_factory=list)


def _model_bucket(report: CampaignReport, model: str) -> dict[str, Any]:
    return report.by_model.setdefault(
        model,
        {
            "cells": 0,
            "ok": 0,
            "failed": 0,
            "validated": 0,
            "cost_usd": 0.0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "scores": [],
        },
    )


def summarize_by_model(report: CampaignReport) -> dict[str, dict[str, Any]]:
    """The model-comparison rollup: one row per model, means over its scored cells."""
    rollup: dict[str, dict[str, Any]] = {}
    for model, bucket in report.by_model.items():
        scores = [s for s in bucket["scores"] if s is not None]
        rollup[model] = {
            "cells": bucket["cells"],
            "ok": bucket["ok"],
            "failed": bucket["failed"],
            "validated": bucket["validated"],
            "cost_usd": round(bucket["cost_usd"], 6),
            "prompt_tokens": bucket["prompt_tokens"],
            "completion_tokens": bucket["completion_tokens"],
            "mean_f1": (sum(scores) / len(scores)) if scores else None,
            "scored_cells": len(scores),
        }
    return rollup


def run_campaign(
    campaign: Campaign,
    *,
    out_root: Path = metrics_db.DEFAULT_RUNS_ROOT,
    db_path: Path = metrics_db.DEFAULT_DB_PATH,
    ledger_root: Path = DEFAULT_LEDGER_ROOT,
    frozen_path: Path = DEFAULT_FROZEN_CONFIG_PATH,
    client: OpenAI | None = None,
    dry_run: bool = False,
    sleeper: Callable[[float], None] = time.sleep,
    progress: Callable[[str], None] | None = None,
) -> CampaignReport:
    """Run (or resume) one campaign. Every completed cell becomes a ledger line."""
    campaign.validate_shape()
    check_freeze_gate(campaign, frozen_path)

    cells = enumerate_cells(campaign)
    report = CampaignReport(campaign_id=campaign.campaign_id, cells_total=len(cells))

    if dry_run:
        report.dry_run_cells = [cell.key for cell in cells]
        return report

    ledger_dir = ledger_root / campaign.campaign_id
    ledger_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = ledger_dir / "ledger.jsonl"
    report.ledger_path = ledger_path

    done: set[str] = set()
    if ledger_path.is_file():
        for line in ledger_path.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["cell_key"])

    active_client = client or llm.build_client()
    runs_started = len(done)

    with ledger_path.open("a") as ledger:
        for cell in cells:
            if cell.key in done:
                report.skipped_resumed += 1
                continue
            if runs_started >= campaign.max_runs:
                report.stopped_reason = f"max_runs ({campaign.max_runs}) reached"
                break
            if report.cost_usd >= campaign.max_usd:
                report.stopped_reason = (
                    f"max_usd (${campaign.max_usd}) reached at ${report.cost_usd:.4f}"
                )
                break

            if progress is not None:
                progress(cell.key)

            entry: dict[str, Any] = {
                "cell_key": cell.key,
                "campaign_id": campaign.campaign_id,
                "stage": campaign.stage,
                "command": cell.command,
                "model": cell.model,
                "temperature": cell.temperature,
                "sample": cell.sample,
                "attempts": 0,
            }
            bucket = _model_bucket(report, cell.model)

            outcome: tuple[str, str, str, bool | None, float, int, int] | None = None
            error: str | None = None
            for attempt, backoff in enumerate([*BACKOFF_SECONDS, None]):
                entry["attempts"] = attempt + 1
                try:
                    outcome = _dispatch(
                        campaign, cell, out_root=out_root, db_path=db_path,
                        client=active_client,
                    )
                    break
                except Exception as exc:  # noqa: BLE001 — sorted immediately below
                    if _is_transient(exc) and backoff is not None:
                        report.transport_retries += 1
                        sleeper(backoff)
                        continue
                    if isinstance(exc, CarucaV2Error) or _is_transient(exc):
                        error = f"{type(exc).__name__}: {exc}"
                        break
                    raise

            runs_started += 1
            bucket["cells"] += 1

            if outcome is None:
                entry["status"] = "error"
                entry["error"] = error
                report.errored += 1
                bucket["failed"] += 1
            else:
                run_id, run_dir, status, validated, cost, p_tokens, c_tokens = outcome
                entry.update(
                    run_id=run_id,
                    run_dir=run_dir,
                    status=status,
                    validation_passed=validated,
                    cost_usd=cost,
                    prompt_tokens=p_tokens,
                    completion_tokens=c_tokens,
                )
                report.completed += 1
                report.cost_usd += cost
                report.prompt_tokens += p_tokens
                report.completion_tokens += c_tokens
                bucket["cost_usd"] += cost
                bucket["prompt_tokens"] += p_tokens
                bucket["completion_tokens"] += c_tokens
                if status == "ok":
                    bucket["ok"] += 1
                else:
                    report.failed_content += 1
                    bucket["failed"] += 1
                if validated:
                    bucket["validated"] += 1

                if campaign.score_after and campaign.stage == "syntax_spec":
                    entry["score"] = _score_cell(cell, run_dir, campaign)
                    f1 = (entry["score"] or {}).get("f1")
                    bucket["scores"].append(f1)

            ledger.write(json.dumps(entry) + "\n")
            ledger.flush()

    summary = {
        "campaign_id": campaign.campaign_id,
        "cells_total": report.cells_total,
        "completed": report.completed,
        "skipped_resumed": report.skipped_resumed,
        "failed_content": report.failed_content,
        "errored": report.errored,
        "transport_retries": report.transport_retries,
        "cost_usd": round(report.cost_usd, 6),
        "prompt_tokens": report.prompt_tokens,
        "completion_tokens": report.completion_tokens,
        "stopped_reason": report.stopped_reason,
        "by_model": summarize_by_model(report),
    }
    (ledger_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return report


def _score_cell(cell: Cell, run_dir: str, campaign: Campaign) -> dict[str, Any] | None:
    """Score a syntax-spec cell right after it ran. Failures are recorded, not raised."""
    spec_path = _spec_path_of(run_dir, cell.command)
    if not spec_path.is_file():
        return {"scoreable": False, "error": "no spec file was written"}
    try:
        record = score_module.score_spec(
            cell.command, spec_path, reference=campaign.score_reference
        )
    except CarucaV2Error as exc:
        return {"scoreable": False, "error": str(exc)}
    return {
        "scoreable": record.get("scoreable"),
        "f1": record.get("f1"),
        "exact_argument_rate": record.get("exact_argument_rate"),
        "counts": record.get("counts"),
        "error": record.get("error"),
    }
