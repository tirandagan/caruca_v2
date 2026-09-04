"""Stage 4 — traces in, a consumer's annotation out.

Covers v1's stages 4 and 5 together, exactly as v1's own `annotate` command does: property
derivation (`tracer/data.py::to_annotation`) and format rendering (the whole `annotator/`
package), roughly 850 lines between them.

The default input is v1's *own* committed traces file, because that makes the headline
experiment the default behavior: identical trace input goes into v1's annotator and into
this one, and the two outputs are diffed. Point `--traces` at a stage-3 run to chain the
pipeline instead.
"""

from __future__ import annotations

import difflib
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

STAGE = "annotate"
COMPONENT = "llm_pipeline"
CONDITION = "plain"

DEFAULT_MAX_TURNS = 4

JSON_FORMAT_INSTRUCTIONS = """\
JSON conforming to this schema:

```json
{schema}
```"""

HASKELL_FORMAT_INSTRUCTIONS = """\
A Haskell module of exactly this shape, with the patterns filled in:

```haskell
{skeleton}
```"""


def format_instructions(definition: dict[str, Any]) -> str:
    """Turn v1's own adapter definition into the format section of the prompt."""
    if definition["kind"] == "json":
        return JSON_FORMAT_INSTRUCTIONS.format(schema=json.dumps(definition["schema"], indent=1))
    return HASKELL_FORMAT_INSTRUCTIONS.format(skeleton=definition["skeleton"])


def strip_fence(text: str) -> tuple[str, bool]:
    """Remove a surrounding code fence if the model added one despite being asked not to."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped, False
    lines = stripped.splitlines()
    if len(lines) < 2:
        return stripped, False
    body = lines[1:]
    if body and body[-1].strip().startswith("```"):
        body = body[:-1]
    return "\n".join(body).strip(), True


def load_traces(command: str, traces_path: Path | None) -> tuple[str, str]:
    """The traces to annotate, and a note of where they came from."""
    path = traces_path if traces_path is not None else v1.traces_path(command)
    if not path.is_file():
        raise V1AccessError(
            f"traces file not found at {path}. Pass --traces PATH, or run "
            "`caruca-v2 trace` first."
        )
    return path.read_text(), str(path)


def compare_text(produced: str, reference: str | None, *, label: str) -> dict[str, Any]:
    """Diff two annotations, reporting shape rather than a single similarity score.

    Line counts and a bounded diff sample, not a percentage: presentation differences and
    substantive ones are not interchangeable, and collapsing them into one number would
    hide exactly the distinction the write-up has to make.
    """
    if reference is None:
        return {"label": label, "available": False}

    produced_lines = produced.splitlines()
    reference_lines = reference.splitlines()
    diff = list(
        difflib.unified_diff(
            reference_lines, produced_lines, fromfile="v1", tofile="v2", lineterm="", n=1
        )
    )
    return {
        "label": label,
        "available": True,
        "identical": produced.strip() == reference.strip(),
        "produced_lines": len(produced_lines),
        "reference_lines": len(reference_lines),
        # `---`/`+++` are unified-diff file headers, not differing content lines.
        "diff_lines": len(
            [
                line
                for line in diff
                if line.startswith(("+", "-")) and not line.startswith(("---", "+++"))
            ]
        ),
        "diff_sample": diff[:60],
    }


def compare_json(produced: str, reference: str | None, *, label: str) -> dict[str, Any]:
    """Compare two JSON annotations structurally, falling back to a text diff.

    Structural equality is the meaningful question for the three JSON consumers: key order
    and indentation are not differences a downstream tool would notice.
    """
    result = compare_text(produced, reference, label=label)
    if not result["available"]:
        return result

    try:
        result["structurally_identical"] = json.loads(produced) == json.loads(reference)
    except (json.JSONDecodeError, TypeError) as exc:
        result["structurally_identical"] = None
        result["structural_error"] = f"{type(exc).__name__}: {exc}"
    return result


@dataclass(frozen=True)
class AnnotateResult:
    """Everything a caller needs from one annotation run."""

    run_id: str
    run_dir: Path
    status: str
    annotation_path: Path | None
    records: list[TelemetryRecord]
    manifest: RunManifest
    validation: ValidationReport | None

    @property
    def succeeded(self) -> bool:
        return self.status == "ok"


def run(
    command: str,
    fmt: str,
    *,
    model: str,
    temperature: float,
    seed: int | None = llm.DEFAULT_SEED,
    max_tokens: int = llm.DEFAULT_MAX_TOKENS,
    max_turns: int = DEFAULT_MAX_TURNS,
    traces_path: Path | None = None,
    compare: bool = True,
    v1_runner: str = "host",
    lima_instance: str = "caruca",
    out_root: Path = metrics_db.DEFAULT_RUNS_ROOT,
    db_path: Path = metrics_db.DEFAULT_DB_PATH,
    log_conversation: bool = False,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> AnnotateResult:
    """Derive one consumer's annotation from a traces file, and diff it against v1's."""
    if fmt not in v1.ANNOTATION_FORMATS:
        raise V1AccessError(
            f"unknown annotation format {fmt!r}; expected one of {v1.ANNOTATION_FORMATS}."
        )

    slug = v1.slug(command)

    active_client = client or llm.build_client()
    traces, traces_source = load_traces(command, traces_path)
    definition = v1.annotation_format_definition(fmt, command)

    prompt = prompting.build(
        STAGE,
        {
            "command": command,
            "format": fmt,
            "traces": traces,
            "format_instructions": format_instructions(definition),
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

    combined = "".join(response.text for response in responses)
    annotation, was_fenced = strip_fence(combined)
    truncated = responses[-1].finish_reason == "length"

    annotation_path: Path | None = None
    validation: ValidationReport | None = None
    status = "failed"
    failure_reason: str | None = None

    if not annotation:
        failure_reason = "model returned no annotation text"
    else:
        annotation_path = run_dir.file(f"{slug}.{fmt}.annotation")
        annotation_path.write_text(annotation if annotation.endswith("\n") else annotation + "\n")

        outcome = v1.validate_annotation(fmt, annotation_path)
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
            failure_reason = f"v1 rejected the generated {fmt} annotation: {outcome.error}"

    comparisons: dict[str, Any] = {}
    if compare:
        reference = v1.reference_annotation(
            command,
            fmt,
            Path(traces_source),
            runner=v1_runner,
            lima_instance=lima_instance,
        )
        compare_fn = compare_text if fmt == "shellcheck" else compare_json
        if reference.available:
            comparisons["vs_v1_same_traces"] = compare_fn(
                annotation, reference.text, label="v1 on identical traces"
            )
        else:
            comparisons["vs_v1_same_traces"] = {
                "label": "v1 on identical traces",
                "available": False,
                "error": reference.error,
                "runner": reference.runner,
            }

        # Labeled `annotation_diff`, never `q1_execution`: this is a diff against the
        # hand-curated files, not a rerun of the consumers' own test suites, and the two
        # are not interchangeable (`memory/caruca_v1_eval_tooling_notes.md`).
        truth = v1.ground_truth_annotation(command, fmt)
        comparisons["vs_ground_truth"] = {
            **compare_fn(annotation, truth, label="hand-curated ground truth"),
            "method": "annotation_diff",
        }

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
        response_format="json" if fmt != "shellcheck" else "haskell",
        prompt_hash=prompt.prompt_hash,
        prompt_files=[f"prompts/{STAGE}/system.md", f"prompts/{STAGE}/user.md"],
        prompt_system=prompt.system,
        prompt_user=prompt.user,
        raw_response=combined,
        finish_reason=responses[-1].finish_reason,
        output_truncated=truncated,
        turns=len(responses),
        output_paths=[] if annotation_path is None else [str(annotation_path)],
        validation=validation,
        checks={
            "format": fmt,
            "output_was_fenced": was_fenced,
            "comparisons": comparisons,
        },
        prompt_tokens=sum(response.prompt_tokens for response in responses),
        completion_tokens=sum(response.completion_tokens for response in responses),
        cost_usd=sum(response.cost_usd for response in responses),
        wall_clock_seconds=sum(response.wall_clock_seconds for response in responses),
        inputs={
            "traces_source": traces_source,
            "caruca_v1_root": str(v1.v1_root()),
            # Every comparison is against a specific v1 revision; a stale reference is a
            # silent wrong answer, so the commit travels with the result.
            "caruca_v1_commit": v1.v1_commit(),
            "v1_runner": v1_runner,
            "max_turns": max_turns,
            "replaces_v1_modules": ["tracer/data.py::to_annotation", "annotator/"],
        },
    )

    for record in records:
        telemetry.write_sidecar(run_dir, f"{slug}.{fmt}.turn-{record.turn:02d}", record)
        metrics_db.append_run(
            record,
            run_dir=run_dir.path,
            validation_passed=None if validation is None else validation.passed,
            db_path=db_path,
        )
    telemetry.write_manifest(run_dir, manifest)

    return AnnotateResult(
        run_id=run_dir.run_id,
        run_dir=run_dir.path,
        status=status,
        annotation_path=annotation_path,
        records=records,
        manifest=manifest,
        validation=validation,
    )
