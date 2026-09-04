"""Stage 2 — syntax specification in, concrete invocations and their environments out.

v1 does this with roughly 715 lines of nested combinatorial Python across `ir/string.py`,
`ir/environment.py`, `ir/contents.py`, and `ir/mixin.py`. Here an LLM is told what the
input is, what to produce, and what format to produce it in — and nothing about how.
Whether it can enumerate a combinatorial space at all is the question being asked, so a
model that stops early, repeats itself, or runs out of room is measured, not corrected.

The one thing supplied beyond the specification is the DSL's value-expansion table. The
specification names types (`Glob`, `Signal`); the values those types stand for live in
v1's DSL runtime. Without them no invocation string could match v1's, and the comparison
would measure a missing input rather than the model. That is input material, like the man
page in stage 1 — not a hint about method.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

from .. import llm, metrics_db, prompting, telemetry, v1
from ..errors import V1AccessError
from ..telemetry import (
    DecodingParams,
    RunManifest,
    TelemetryRecord,
    ValidationReport,
)

STAGE = "generate"
COMPONENT = "llm_pipeline"
CONDITION = "plain"

# v1's own CLI defaults (`cli/__init__.py`), verified by reading them rather than assumed.
# Note that `--max-arity` defaults to 1, not 2: task 002's draft said 2, and the paper's
# "two-flag limit" is `--max-count`, a different knob. Whatever is used here must be used
# on the v1 side of any comparison, which is why all four are recorded in the manifest.
V1_DEFAULT_MAX_ARITY = 1
V1_DEFAULT_MAX_COUNT = 4
V1_DEFAULT_STDIN = "simple"
V1_DEFAULT_CONTENT = "simple"
V1_DEFAULT_SKIP: str | None = None  # v1's `--skip` has no default: nothing is skipped
# What v1's bare `--skip` means (`cli/__init__.py:10`, `const=DEFAULT_SKIP`).
V1_SKIP_CONST = "--version,--help,--interactive"

DEFAULT_MAX_TURNS = 4

INVOCATIONS_SUFFIX = ".invocations.txt"
CONFIGS_SUFFIX = ".configs.json"


@dataclass(frozen=True)
class ParsedOutput:
    """What survived parsing the model's JSON Lines, and what did not."""

    invocations: list[str]
    configs: list[dict[str, Any]]
    line_count: int
    unparseable_lines: list[str]
    malformed_objects: int

    @property
    def parsed(self) -> int:
        return len(self.configs)


def parse_jsonl(text: str) -> ParsedOutput:
    """Read one JSON object per line, keeping a count of everything discarded.

    A truncated final line is simply unparseable and lands in `unparseable_lines`; the
    stage records that rather than trying to repair it, because a repaired line would be
    partly our output and partly the model's.
    """
    invocations: list[str] = []
    configs: list[dict[str, Any]] = []
    unparseable: list[str] = []
    malformed = 0
    lines = [line for line in text.splitlines() if line.strip()]

    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            unparseable.append(line)
            continue

        if not isinstance(entry, dict) or "invocation" not in entry or "config" not in entry:
            malformed += 1
            continue

        invocations.append(str(entry["invocation"]))
        configs.append(entry["config"])

    return ParsedOutput(
        invocations=invocations,
        configs=configs,
        line_count=len(lines),
        unparseable_lines=unparseable[:20],
        malformed_objects=malformed,
    )


def compare_invocations(produced: list[str], reference: v1.ReferenceInvocations) -> dict[str, Any]:
    """Set-diff the model's invocation strings against `caruca generate CMD`.

    The denominator is v1's actual line count, never its `--number` length hint: those
    disagree (280 against 12,720 for `mkdir` at arity 1), and the hint is recorded only so
    the discrepancy stays visible.
    """
    if not reference.available:
        return {"available": False, "error": reference.error}

    produced_set = set(produced)
    reference_set = set(reference.invocations)
    matched = produced_set & reference_set

    return {
        "available": True,
        "v1_count": reference.count,
        "v1_unique_count": len(reference_set),
        "v1_length_hint": reference.length_hint,
        "produced_count": len(produced),
        "produced_unique_count": len(produced_set),
        "matched": len(matched),
        "missing": len(reference_set - produced_set),
        "spurious": len(produced_set - reference_set),
        "recall": len(matched) / len(reference_set) if reference_set else None,
        "precision": len(matched) / len(produced_set) if produced_set else None,
        "missing_sample": sorted(reference_set - produced_set)[:20],
        "spurious_sample": sorted(produced_set - reference_set)[:20],
    }


def load_specification(command: str, spec_path: Path | None) -> tuple[str, str]:
    """The syntax specification text, and a note of where it came from."""
    if spec_path is None:
        return v1.syntax_spec(command), str(v1.syntax_spec_path(command))
    if not spec_path.is_file():
        raise V1AccessError(f"syntax specification not found at {spec_path}.")
    return spec_path.read_text(), str(spec_path)


@dataclass(frozen=True)
class GenerateResult:
    """Everything a caller needs from one configuration-generation run."""

    run_id: str
    run_dir: Path
    status: str
    invocations_path: Path | None
    configs_path: Path | None
    records: list[TelemetryRecord]
    manifest: RunManifest
    validation: ValidationReport | None

    @property
    def succeeded(self) -> bool:
        return self.status == "ok"


def run(
    command: str,
    *,
    model: str,
    temperature: float,
    seed: int | None = llm.DEFAULT_SEED,
    max_tokens: int = llm.DEFAULT_MAX_TOKENS,
    max_turns: int = DEFAULT_MAX_TURNS,
    spec_path: Path | None = None,
    max_arity: int = V1_DEFAULT_MAX_ARITY,
    max_count: int = V1_DEFAULT_MAX_COUNT,
    stdin_variation: str = V1_DEFAULT_STDIN,
    content_variation: str = V1_DEFAULT_CONTENT,
    skip_flags: str | None = V1_DEFAULT_SKIP,
    compare: bool = True,
    compare_timeout: int = 300,
    out_root: Path = metrics_db.DEFAULT_RUNS_ROOT,
    db_path: Path = metrics_db.DEFAULT_DB_PATH,
    log_conversation: bool = False,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> GenerateResult:
    """Ask a model to enumerate a command's invocations, then measure what came back."""
    slug = v1.slug(command)

    active_client = client or llm.build_client()
    specification, spec_source = load_specification(command, spec_path)
    probe_values = v1.probe_values()
    config_schema = v1.command_config_schema()

    prompt = prompting.build(
        STAGE,
        {
            "command": command,
            "syntax_spec": specification,
            "probe_values": json.dumps(probe_values, indent=1),
            "config_schema": json.dumps(config_schema, indent=1),
            "max_arity": str(max_arity),
            "max_count": str(max_count),
            "stdin_variation": stdin_variation,
            "content_variation": content_variation,
            "skip_flags": skip_flags or "(none)",
        },
    )

    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = telemetry.create_run_directory(out_root, slug)

    responses = llm.complete_series(
        prompt.as_messages(),
        model=model,
        temperature=temperature,
        seed=seed,
        max_tokens=max_tokens,
        max_turns=max_turns,
        provider=provider,
        client=active_client,
    )

    if log_conversation:
        messages: list[dict[str, Any]] = list(prompt.as_messages())
        for index, response in enumerate(responses):
            messages.append(response.message)
            if index < len(responses) - 1:
                messages.append({"role": "user", "content": llm.CONTINUE_INSTRUCTION})
        telemetry.append_conversation(run_dir, messages)

    combined = "\n".join(response.text for response in responses)
    parsed = parse_jsonl(combined)
    truncated = responses[-1].finish_reason == "length"

    invocations_path: Path | None = None
    configs_path: Path | None = None
    validation: ValidationReport | None = None
    status = "failed"
    failure_reason: str | None = None

    if not parsed.configs:
        failure_reason = (
            f"no usable output: {parsed.line_count} line(s) returned, none of them a "
            "JSON object carrying both `invocation` and `config`"
        )
    else:
        invocations_path = run_dir.file(f"{slug}{INVOCATIONS_SUFFIX}")
        invocations_path.write_text("\n".join(parsed.invocations) + "\n")

        configs_path = run_dir.file(f"{slug}{CONFIGS_SUFFIX}")
        configs_path.write_text(json.dumps(parsed.configs, indent=1) + "\n")

        outcome = v1.validate_configs(configs_path)
        validation = ValidationReport(
            passed=outcome.passed,
            available=outcome.available,
            error=outcome.error,
            traceback=outcome.traceback,
            elements=outcome.count,
        )
        if outcome.passed:
            status = "ok"
        elif not outcome.available:
            failure_reason = f"validation unavailable: {outcome.error}"
        else:
            index = outcome.invalid_index
            where = "" if index is None else f" (first failure at entry {index})"
            failure_reason = f"v1 rejected the generated configs{where}: {outcome.error}"

    comparison: dict[str, Any] = {"available": False, "error": "comparison not requested"}
    if compare:
        # Same bounds on both sides, or the diff measures the bounds instead of the model.
        reference = v1.reference_invocations(
            command,
            max_arity=max_arity,
            max_count=max_count,
            skip=skip_flags,
            timeout=compare_timeout,
        )
        comparison = compare_invocations(parsed.invocations, reference)

    decoding = DecodingParams(temperature=temperature, max_tokens=max_tokens)
    records = [
        TelemetryRecord(
            run_id=run_dir.run_id,
            command=command,
            component=COMPONENT,
            condition=CONDITION,
            stage=STAGE,
            model_id=response.model_reported,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            cost_usd=response.cost_usd,
            wall_clock_seconds=response.wall_clock_seconds,
            seed=seed,
            prompt_hash=prompt.prompt_hash,
            timestamp=run_dir.timestamp,
            decoding_params=decoding,
            turn=turn,
        )
        for turn, response in enumerate(responses)
    ]

    manifest = RunManifest(
        run_id=run_dir.run_id,
        timestamp=run_dir.timestamp,
        command=command,
        component=COMPONENT,
        condition=CONDITION,
        stage=STAGE,
        status=status,
        failure_reason=failure_reason,
        model_requested=responses[0].model_requested,
        model_reported=responses[0].model_reported,
        provider=responses[0].provider,
        seed=seed,
        seed_honored=seed is not None and llm.seed_is_honored(model),
        decoding_params=decoding,
        response_format="jsonl",
        prompt_hash=prompt.prompt_hash,
        prompt_files=[f"prompts/{STAGE}/system.md", f"prompts/{STAGE}/user.md"],
        prompt_system=prompt.system,
        prompt_user=prompt.user,
        raw_response=combined,
        finish_reason=responses[-1].finish_reason,
        output_truncated=truncated,
        turns=len(responses),
        output_paths=[str(path) for path in (invocations_path, configs_path) if path],
        validation=validation,
        checks={
            "parse": {
                "lines_returned": parsed.line_count,
                "objects_parsed": parsed.parsed,
                "unparseable_lines": len(parsed.unparseable_lines),
                "unparseable_sample": parsed.unparseable_lines,
                "malformed_objects": parsed.malformed_objects,
                # A run that hit the turn cap while still truncated did not finish
                # enumerating. Distinguishing that from a model that simply stopped is
                # what separates "the cap bound" from "the model bound".
                "hit_turn_cap_while_truncated": truncated and len(responses) >= max_turns,
            },
            "invocation_comparison": comparison,
        },
        prompt_tokens=sum(response.prompt_tokens for response in responses),
        completion_tokens=sum(response.completion_tokens for response in responses),
        cost_usd=sum(response.cost_usd for response in responses),
        wall_clock_seconds=sum(response.wall_clock_seconds for response in responses),
        inputs={
            "spec_source": spec_source,
            "caruca_v1_root": str(v1.v1_root()),
            "max_arity": max_arity,
            "max_count": max_count,
            "stdin_variation": stdin_variation,
            "content_variation": content_variation,
            "skip_flags": skip_flags,
            "max_turns": max_turns,
            "replaces_v1_modules": [
                "ir/string.py",
                "ir/environment.py",
                "ir/contents.py",
                "ir/mixin.py",
            ],
        },
    )

    for record in records:
        telemetry.write_sidecar(run_dir, f"{slug}.turn-{record.turn:02d}", record)
        metrics_db.append_run(
            record,
            run_dir=run_dir.path,
            validation_passed=None if validation is None else validation.passed,
            db_path=db_path,
        )
    telemetry.write_manifest(run_dir, manifest)

    return GenerateResult(
        run_id=run_dir.run_id,
        run_dir=run_dir.path,
        status=status,
        invocations_path=invocations_path,
        configs_path=configs_path,
        records=records,
        manifest=manifest,
        validation=validation,
    )
