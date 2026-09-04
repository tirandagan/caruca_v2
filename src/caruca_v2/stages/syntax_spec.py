"""Stage 1 — documentation in, syntax specification out.

This is the naive control (task 001). It replaces the one place v1 uses an LLM with a
single few-shot prompt and nothing else: no tools, no retry, no validation-driven
regeneration. Prof. Eiers' guardrail is the design, not a limitation to route around —
the point of the control is to be weak, so the evaluation can say how much v1's
engineered pipeline buys over an off-the-shelf prompt.

`run()` is the typed entry point; `cli.py` only parses arguments and calls it.
"""

from __future__ import annotations

import re
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

STAGE = "syntax_spec"
COMPONENT = "naive_llm"
CONDITION = "plain"

# v1's own extraction (`llm.py::extract_code`): first fenced block, or the whole response
# when there is no fence. Reproduced rather than improved, including the fallback.
FENCE_PATTERN = re.compile(r"```.*?\n([\s\S]*?)```")


def extract_code(text: str) -> tuple[str, bool]:
    """Return the spec source and whether it actually came from a fenced block."""
    match = FENCE_PATTERN.search(text)
    if match is None:
        return text, False
    return match.group(1), True


def render_exemplars(exemplars: list[v1.Exemplar]) -> str:
    """Lay the four few-shot pairs out as Markdown.

    This is a deliberate deviation from v1, which serialized its examples through DSPy's
    `LabeledFewShot` wire format. The example *content* is identical (same four commands,
    same man pages, same committed specs); only the framing differs, because reproducing
    DSPy's rendering would mean depending on DSPy. Stated in the write-up.
    """
    blocks = []
    for exemplar in exemplars:
        blocks.append(
            f"### Example: `{exemplar.command}`\n\n"
            f"#### Documentation for `{exemplar.command}`\n\n"
            f"```\n{exemplar.man_page}\n```\n\n"
            f"#### Syntax specification for `{exemplar.command}`\n\n"
            f"```python\n{exemplar.syntax_spec}\n```"
        )
    return "\n\n".join(blocks)


def load_documentation(command: str, docs_path: Path | None) -> tuple[str, str]:
    """The command's documentation, and a note of where it came from."""
    if docs_path is None:
        return v1.man_page(command), str(v1.man_page_path(command))
    if not docs_path.is_file():
        raise V1AccessError(f"documentation file not found at {docs_path}.")
    return docs_path.read_text(), str(docs_path)


@dataclass(frozen=True)
class SyntaxSpecResult:
    """Everything a caller (CLI, agent, or harness) needs from one run."""

    run_id: str
    run_dir: Path
    status: str
    spec_path: Path | None
    record: TelemetryRecord
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
    docs_path: Path | None = None,
    out_root: Path = metrics_db.DEFAULT_RUNS_ROOT,
    db_path: Path = metrics_db.DEFAULT_DB_PATH,
    log_conversation: bool = False,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> SyntaxSpecResult:
    """Generate one syntax specification, measure it, and record what happened.

    Exactly one model call. A response that cannot be turned into a valid spec is a
    result: it is written down, the run exits non-zero, and the model is never re-asked.
    """
    slug = v1.slug(command)
    spec_symbol = f"{slug}_syntax_spec"

    # Everything that can fail on configuration fails before a run directory exists, so a
    # misconfigured invocation never leaves a half-written run behind.
    active_client = client or llm.build_client()
    man_page, docs_source = load_documentation(command, docs_path)
    exemplars = v1.exemplars()

    prompt = prompting.build(
        STAGE,
        {
            "command": command,
            "man_page": man_page,
            "few_shot_examples": render_exemplars(exemplars),
            "spec_symbol": spec_symbol,
        },
    )

    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = telemetry.create_run_directory(out_root, slug)

    response = llm.complete(
        prompt.as_messages(),
        model=model,
        seed=seed,
        temperature=temperature,
        max_tokens=max_tokens,
        provider=provider,
        client=active_client,
    )

    if log_conversation:
        telemetry.append_conversation(run_dir, [*prompt.as_messages(), response.message])

    code, fenced = extract_code(response.text)
    truncated = response.finish_reason == "length"

    spec_path: Path | None = None
    validation: ValidationReport | None = None
    status = "failed"
    failure_reason: str | None = None

    if not code.strip():
        failure_reason = "model returned no specification text"
    else:
        spec_path = run_dir.file(f"{slug}.py")
        spec_path.write_text(code if code.endswith("\n") else code + "\n")
        outcome = v1.validate_syntax_spec(command, spec_path)
        validation = ValidationReport(
            passed=outcome.passed,
            available=outcome.available,
            error=outcome.error,
            traceback=outcome.traceback,
            elements=outcome.elements,
        )
        if outcome.passed:
            status = "ok"
        elif not outcome.available:
            failure_reason = f"validation unavailable: {outcome.error}"
        else:
            failure_reason = f"v1 rejected the generated spec: {outcome.error}"

    decoding = DecodingParams(temperature=temperature, max_tokens=max_tokens)

    record = TelemetryRecord(
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
    )

    inputs: dict[str, Any] = {
        "docs_source": docs_source,
        "exemplar_commands": [exemplar.command for exemplar in exemplars],
        "caruca_v1_root": str(v1.v1_root()),
        "output_fenced": fenced,
    }

    manifest = RunManifest(
        run_id=run_dir.run_id,
        timestamp=run_dir.timestamp,
        command=command,
        component=COMPONENT,
        condition=CONDITION,
        stage=STAGE,
        status=status,
        failure_reason=failure_reason,
        model_requested=response.model_requested,
        model_reported=response.model_reported,
        provider=response.provider,
        seed=seed,
        seed_honored=seed is not None and llm.seed_is_honored(model),
        decoding_params=decoding,
        response_format="text",
        prompt_hash=prompt.prompt_hash,
        prompt_files=[f"prompts/{STAGE}/system.md", f"prompts/{STAGE}/user.md"],
        prompt_system=prompt.system,
        prompt_user=prompt.user,
        raw_response=response.text,
        finish_reason=response.finish_reason,
        output_truncated=truncated,
        output_paths=[] if spec_path is None else [str(spec_path)],
        validation=validation,
        prompt_tokens=response.prompt_tokens,
        completion_tokens=response.completion_tokens,
        cost_usd=response.cost_usd,
        wall_clock_seconds=response.wall_clock_seconds,
        inputs=inputs,
    )

    telemetry.write_sidecar(run_dir, slug, record)
    telemetry.write_manifest(run_dir, manifest)
    metrics_db.append_run(
        record,
        run_dir=run_dir.path,
        validation_passed=None if validation is None else validation.passed,
        db_path=db_path,
    )

    return SyntaxSpecResult(
        run_id=run_dir.run_id,
        run_dir=run_dir.path,
        status=status,
        spec_path=spec_path,
        record=record,
        manifest=manifest,
        validation=validation,
    )
