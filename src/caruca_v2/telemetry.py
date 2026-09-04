"""Telemetry records, run directories, and the manifest.

These files are the evidence a paper revision is argued from, so the rule here is
stricter than for the code around them: every field is populated from what actually
happened, and a value we could not obtain is an error rather than a default. A null token
count is a bug, not a zero.

Shapes follow `ai_docs/prep/data_telemetry_schema.md`, with the additive
`decoding_params` object added by task 001.
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .errors import CarucaV2Error

Component = Literal["baseline", "naive_llm", "tool_augmentation", "llm_pipeline"]
Condition = Literal["plain", "augmented"]
Stage = Literal["syntax_spec", "generate", "trace", "annotate"]

SIDECAR_SUFFIX = ".telemetry.json"
MANIFEST_NAME = "manifest.json"
CONVERSATION_NAME = "conversation.jsonl"


class DecodingParams(BaseModel):
    """Every decoding parameter actually sent, recorded verbatim.

    `model_config`'s `extra="allow"` is deliberate: a future stage that sets an extra
    parameter records it here without a schema change, so telemetry never silently
    under-reports the configuration a run used.
    """

    model_config = ConfigDict(extra="allow")

    temperature: float
    max_tokens: int


class TelemetryRecord(BaseModel):
    """One record per LLM call. Agentic stages emit several per run, sharing `run_id`."""

    run_id: str
    command: str
    component: Component
    condition: Condition
    stage: Stage
    model_id: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    wall_clock_seconds: float
    seed: int | None
    prompt_hash: str
    timestamp: str
    decoding_params: DecodingParams
    turn: int = 0

    # Which configuration this turn belongs to, for the stages that open one session per
    # configuration. Without it a per-turn cost cannot be attributed to the configuration
    # that incurred it, and "cost per configuration" is not answerable from the sidecars.
    config_index: int | None = None


class ValidationReport(BaseModel):
    """What v1 said about the generated artifact. Recorded, never acted on.

    `available` False means v1's environment could not be reached, which is a different
    finding from "v1 rejected the spec" and must not be collapsed into it.
    """

    passed: bool
    available: bool
    error: str | None = None
    traceback: str | None = None
    elements: int | None = None


class RunManifest(BaseModel):
    """The full account of one run: what was asked, what came back, what it cost."""

    run_id: str
    timestamp: str
    command: str
    component: Component
    condition: Condition
    stage: Stage
    status: Literal["ok", "failed"]
    failure_reason: str | None = None

    model_requested: str
    model_reported: str
    provider: str | None = None
    seed: int | None
    seed_honored: bool
    decoding_params: DecodingParams
    response_format: str

    prompt_hash: str
    prompt_files: list[str]
    prompt_system: str
    prompt_user: str
    raw_response: str

    finish_reason: str | None = None
    output_truncated: bool = False
    turns: int = 1
    output_paths: list[str] = Field(default_factory=list)
    validation: ValidationReport | None = None

    # Stage-specific structured findings (a stage-2 invocation set-diff, a stage-3
    # workspace summary). Kept open rather than modelled per stage: these are evidence to
    # read, and a stage should be able to record a new one without a schema migration.
    checks: dict[str, Any] = Field(default_factory=dict)

    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    wall_clock_seconds: float

    inputs: dict[str, Any] = Field(default_factory=dict)


def utc_now() -> datetime:
    return datetime.now(UTC)


def timestamp_for(moment: datetime) -> str:
    """ISO-8601 UTC, used inside records."""
    return moment.isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class RunDirectory:
    """A single run's output directory, named after its `run_id`."""

    run_id: str
    path: Path
    started_at: datetime

    @property
    def timestamp(self) -> str:
        return timestamp_for(self.started_at)

    def file(self, name: str) -> Path:
        return self.path / name


# Four bytes, not two. Two gives 16 bits, which collides for about 7% of batches of 100
# runs started in the same second and 71% of batches of 400 — well inside what a
# full-corpus harness does. `exist_ok=False` is deliberate (a reused directory would
# overwrite evidence), so a collision was a hard crash rather than a near miss.
RUN_ID_SUFFIX_BYTES = 4
RUN_ID_ATTEMPTS = 8


def create_run_directory(out_root: Path, command_slug: str) -> RunDirectory:
    """Create `<out_root>/<UTC timestamp>_<command>_<suffix>/`.

    The random suffix exists because two runs of the same command can start in the same
    second, and a silently reused directory would overwrite evidence. `exist_ok=False`
    keeps that guarantee; the retry keeps an unlucky draw from ending the run.
    """
    started_at = utc_now()
    stamp = started_at.strftime("%Y-%m-%dT%H%M%SZ")

    for _ in range(RUN_ID_ATTEMPTS):
        run_id = f"{stamp}_{command_slug}_{secrets.token_hex(RUN_ID_SUFFIX_BYTES)}"
        path = out_root / run_id
        try:
            path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        return RunDirectory(run_id=run_id, path=path, started_at=started_at)

    raise CarucaV2Error(
        f"could not find an unused run directory under {out_root} after "
        f"{RUN_ID_ATTEMPTS} attempts."
    )


def _write_json(path: Path, payload: BaseModel) -> Path:
    path.write_text(payload.model_dump_json(indent=2) + "\n")
    return path


def write_sidecar(run_dir: RunDirectory, command_slug: str, record: TelemetryRecord) -> Path:
    return _write_json(run_dir.file(f"{command_slug}{SIDECAR_SUFFIX}"), record)


def write_manifest(run_dir: RunDirectory, manifest: RunManifest) -> Path:
    return _write_json(run_dir.file(MANIFEST_NAME), manifest)


def append_conversation(run_dir: RunDirectory, messages: list[dict[str, Any]]) -> Path:
    """Append messages verbatim to `conversation.jsonl`, one JSON object per line."""
    path = run_dir.file(CONVERSATION_NAME)
    with path.open("a") as handle:
        for message in messages:
            handle.write(json.dumps(message) + "\n")
    return path


def load_sidecar(path: Path) -> TelemetryRecord:
    return TelemetryRecord.model_validate_json(path.read_text())


def load_manifest(path: Path) -> RunManifest:
    return RunManifest.model_validate_json(path.read_text())
