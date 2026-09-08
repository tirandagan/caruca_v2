"""Stage 3 — configurations in, execution traces out.

v1 does this with roughly 675 lines of strace orchestration and syscall parsing. Here the
model runs the command itself, through a tool surface it cannot step outside of, and
reports what it saw. It cannot see syscalls, so some of what strace records is simply not
observable this way: where that shows up, it is recorded as a structural gap, because the
size of that gap is one of the findings.

Division of labor, per the shared design: the model observes; our code packages. Grouping
the observations into v1's `Traces` envelope, and rewriting workspace paths into v1's
fixed sandbox namespace, is deterministic plumbing done in code — and done by asking v1's
own models to build the file, so it is valid by construction.
"""

from __future__ import annotations

import contextlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openai import OpenAI

from .. import llm, metrics_db, prompting, telemetry, tools, v1, workspace
from ..errors import V1AccessError
from ..telemetry import (
    DecodingParams,
    RunManifest,
    TelemetryRecord,
    ValidationReport,
)

STAGE = "trace"
COMPONENT = "llm_pipeline"
CONDITION = "plain"

# Small on purpose. This stage is where the cost lives: one agent conversation per
# configuration, several turns each. Running a full config set is an explicit choice.
DEFAULT_LIMIT = 5
DEFAULT_MAX_TURNS = 15

TRACES_SUFFIX = ".traces.json"
ENTRIES_SUFFIX = ".observations.json"


@dataclass
class ConfigOutcome:
    """One configuration's session: what the model reported, and what it cost."""

    index: int
    invocation: str | None
    status: str
    responses: list[llm.LLMResponse] = field(default_factory=list)
    entry: dict[str, Any] | None = None
    audit: list[dict[str, Any]] = field(default_factory=list)
    executions: int = 0
    stop_reason: str | None = None
    error: str | None = None
    messages: list[dict[str, Any]] = field(default_factory=list)
    prompt: prompting.Prompt | None = None


def load_configs(command: str, configs_path: Path | None, out_root: Path) -> tuple[list[dict], str]:
    """The configurations to trace, and a note of where they came from.

    With no explicit path, the most recent `generate` run for this command under `--out`
    is used, so the two stages chain without the caller repeating a path.
    """
    if configs_path is None:
        slug = v1.slug(command)
        candidates = sorted(out_root.glob(f"*_{slug}_*/{slug}.configs.json"))
        if not candidates:
            raise V1AccessError(
                f"no `generate` output found for {command!r} under {out_root}. "
                "Run `caruca-v2 generate` first, or pass --configs PATH."
            )
        configs_path = candidates[-1]

    if not configs_path.is_file():
        raise V1AccessError(f"configurations file not found at {configs_path}.")

    payload = json.loads(configs_path.read_text())
    if not isinstance(payload, list):
        raise V1AccessError(
            f"{configs_path} should hold a JSON list of CommandConfig objects, "
            f"got {type(payload).__name__}."
        )
    return payload, str(configs_path)


def normalize_interactions(
    reported: list[dict[str, Any]], space: workspace.Workspace
) -> tuple[list[list[str]], list[dict[str, Any]]]:
    """Turn the model's reported interactions into v1's `[action, path]` pairs.

    Paths are rewritten into v1's sandbox namespace here, for the same reason v1's own
    tracer rewrites them: v1's annotator hardcodes that namespace. Entries whose action is
    not one v1 knows are dropped and returned separately, never silently coerced into a
    neighbouring action.
    """
    known = {"rf", "wf", "ad", "mo", "de", "md", "rd"}
    pairs: list[list[str]] = []
    rejected: list[dict[str, Any]] = []

    for item in reported:
        if not isinstance(item, dict):
            rejected.append({"entry": item, "reason": "not an object"})
            continue
        action = str(item.get("action", ""))
        path = item.get("path")
        if action not in known:
            rejected.append({"entry": item, "reason": f"unknown action {action!r}"})
            continue
        if not isinstance(path, str) or not path:
            rejected.append({"entry": item, "reason": "missing path"})
            continue
        pairs.append([action, space.rewrite(path)])

    return pairs, rejected


def trace_one(
    command: str,
    config: dict[str, Any],
    index: int,
    *,
    model: str,
    temperature: float,
    seed: int | None,
    max_tokens: int,
    max_turns: int,
    isolation: tools.IsolationBackend | None,
    keep_workspace: bool,
    provider: str | None,
    client: OpenAI,
) -> ConfigOutcome:
    """Run one agent session against one configuration's prepared workspace."""
    # `materialize` is a generator-based context manager, so its body — including the
    # failure raise — runs at `__enter__`, not at the call. The enter therefore has to
    # sit inside the try, or a config v1 rejects crashes the whole run instead of being
    # recorded as this configuration's outcome. Caught live by pilot campaign C0.
    stack = contextlib.ExitStack()
    try:
        space = stack.enter_context(
            workspace.materialize(
                config,
                keep=keep_workspace,
                root_dir=isolation.workspace_root if isolation else None,
            )
        )
    except workspace.MaterializationFailure as exc:
        return ConfigOutcome(
            index=index, invocation=None, status="workspace_failed", error=str(exc)
        )

    with stack:
        executor = tools.ToolExecutor(command=command, workspace=space, isolation=isolation)
        prompt = prompting.build(
            STAGE,
            {
                "command": command,
                "invocation": space.invocation or "",
                "listing": "\n".join(space.listing) if space.listing else "(empty)",
                "stdin_name": space.stdin_name or "unknown",
            },
        )

        try:
            loop = llm.run_tool_loop(
                prompt.as_messages(),
                model=model,
                temperature=temperature,
                seed=seed,
                max_tokens=max_tokens,
                max_turns=max_turns,
                tools=tools.tool_definitions(command),
                execute=lambda name, arguments: tools.format_result(
                    executor.execute(name, arguments)
                ),
                is_finished=lambda: executor.report is not None,
                provider=provider,
                client=client,
            )
        except tools.IsolationRequired as exc:
            return ConfigOutcome(
                index=index,
                invocation=space.invocation,
                status="isolation_required",
                error=str(exc),
                audit=executor.audit_trail(),
                prompt=prompt,
            )

        outcome = ConfigOutcome(
            index=index,
            invocation=space.invocation,
            status="ok",
            responses=loop.responses,
            audit=executor.audit_trail(),
            executions=executor.executions,
            stop_reason=loop.stop_reason,
            messages=loop.messages,
            prompt=prompt,
        )

        if executor.report is None:
            outcome.status = "no_report"
            outcome.error = (
                f"the session ended ({loop.stop_reason}) without calling "
                "report_observations"
            )
            return outcome

        pairs, rejected = normalize_interactions(
            executor.report.get("interactions") or [], space
        )
        outcome.entry = {
            "config": config,
            "return_code": executor.report.get("return_code"),
            "stdout": executor.report.get("stdout"),
            "stderr": executor.report.get("stderr"),
            "traces": pairs,
            "rejected_interactions": rejected,
        }
        return outcome


@dataclass(frozen=True)
class TraceResult:
    """Everything a caller needs from one tracing run."""

    run_id: str
    run_dir: Path
    status: str
    traces_path: Path | None
    records: list[TelemetryRecord]
    manifest: RunManifest
    validation: ValidationReport | None
    outcomes: list[ConfigOutcome]

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
    configs_path: Path | None = None,
    limit: int = DEFAULT_LIMIT,
    isolation: tools.IsolationBackend | None = None,
    keep_workspace: bool = False,
    out_root: Path = metrics_db.DEFAULT_RUNS_ROOT,
    db_path: Path = metrics_db.DEFAULT_DB_PATH,
    log_conversation: bool = False,
    provider: str | None = None,
    client: OpenAI | None = None,
    progress=None,
) -> TraceResult:
    """Trace up to `limit` configurations, one agent session each."""
    slug = v1.slug(command)

    if tools.requires_isolation(command) and isolation is None:
        raise V1AccessError(
            f"`{command}` is destructive and will not be traced directly on this machine. "
            "Re-run with --isolation lima, which runs it inside the caruca VM."
        )

    active_client = client or llm.build_client()
    configs, configs_source = load_configs(command, configs_path, out_root)
    selected = configs[:limit]

    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = telemetry.create_run_directory(out_root, slug)

    outcomes: list[ConfigOutcome] = []
    for index, config in enumerate(selected):
        outcome = trace_one(
            command,
            config,
            index,
            model=model,
            temperature=temperature,
            seed=seed,
            max_tokens=max_tokens,
            max_turns=max_turns,
            isolation=isolation,
            keep_workspace=keep_workspace,
            provider=provider,
            client=active_client,
        )
        outcomes.append(outcome)
        if progress is not None:
            progress(outcome, len(selected))

    if log_conversation:
        for outcome in outcomes:
            if outcome.messages:
                telemetry.append_conversation(
                    run_dir,
                    [{"config_index": outcome.index, **message} for message in outcome.messages],
                )

    entries = [outcome.entry for outcome in outcomes if outcome.entry is not None]
    traces_path: Path | None = None
    validation: ValidationReport | None = None
    status = "failed"
    failure_reason: str | None = None

    if not entries:
        failure_reason = (
            f"no configuration produced a usable observation report "
            f"({len(selected)} attempted)"
        )
    else:
        entries_path = run_dir.file(f"{slug}{ENTRIES_SUFFIX}")
        entries_path.write_text(json.dumps(entries, indent=1) + "\n")

        traces_path = run_dir.file(f"{slug}{TRACES_SUFFIX}")
        assembly = v1.assemble_traces(entries_path, traces_path)
        if not assembly.assembled:
            traces_path = None
            failure_reason = f"v1 could not assemble a Traces file: {assembly.error}"
            validation = ValidationReport(
                passed=False, available=True, error=assembly.error,
                traceback=assembly.traceback,
            )
        else:
            outcome_check = v1.validate_traces(traces_path)
            validation = ValidationReport(
                passed=outcome_check.passed,
                available=outcome_check.available,
                error=outcome_check.error,
                traceback=outcome_check.traceback,
                elements=outcome_check.count,
            )
            if outcome_check.passed:
                status = "ok"
            elif not outcome_check.available:
                failure_reason = f"validation unavailable: {outcome_check.error}"
            else:
                failure_reason = f"v1 rejected the traces file: {outcome_check.error}"

    decoding = DecodingParams(temperature=temperature, max_tokens=max_tokens)
    records: list[TelemetryRecord] = []
    turn = 0
    for outcome in outcomes:
        # Each configuration gets its own prompt (different invocation, different
        # starting listing), so each session's records carry that session's hash.
        session_hash = outcome.prompt.prompt_hash if outcome.prompt else ""
        for response in outcome.responses:
            records.append(
                TelemetryRecord(
                    run_id=run_dir.run_id,
                    config_index=outcome.index,
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
                    prompt_hash=session_hash,
                    timestamp=run_dir.timestamp,
                    decoding_params=decoding,
                    turn=turn,
                )
            )
            turn += 1

    responses = [response for outcome in outcomes for response in outcome.responses]
    first = responses[0] if responses else None

    manifest = RunManifest(
        run_id=run_dir.run_id,
        timestamp=run_dir.timestamp,
        command=command,
        component=COMPONENT,
        condition=CONDITION,
        stage=STAGE,
        status=status,
        failure_reason=failure_reason,
        model_requested=model,
        model_reported=first.model_reported if first else model,
        provider=first.provider if first else None,
        seed=seed,
        seed_honored=seed is not None and llm.seed_is_honored(model),
        decoding_params=decoding,
        response_format="tool_calls",
        # One run covers several sessions, so the run-level hash is over the per-session
        # hashes in order. The individual hashes are in `checks.sessions`.
        prompt_hash=prompting.hash_prompt(
            STAGE, "\n".join(o.prompt.prompt_hash if o.prompt else "" for o in outcomes)
        ),
        prompt_files=[f"prompts/{STAGE}/system.md", f"prompts/{STAGE}/user.md"],
        prompt_system=outcomes[0].prompt.system if outcomes and outcomes[0].prompt else "",
        prompt_user=outcomes[0].prompt.user if outcomes and outcomes[0].prompt else "",
        raw_response=json.dumps(
            [{"index": o.index, "report": o.entry} for o in outcomes if o.entry], indent=1
        ),
        finish_reason=responses[-1].finish_reason if responses else None,
        turns=len(records),
        output_paths=[str(path) for path in (traces_path,) if path],
        validation=validation,
        checks={
            "configs": {
                "available": len(configs),
                "attempted": len(selected),
                "reported": len(entries),
                "limit": limit,
            },
            "sessions": [
                {
                    "index": outcome.index,
                    "invocation": outcome.invocation,
                    "status": outcome.status,
                    "prompt_hash": outcome.prompt.prompt_hash if outcome.prompt else None,
                    "turns": len(outcome.responses),
                    "stop_reason": outcome.stop_reason,
                    "executions": outcome.executions,
                    # Cost lives in this stage, and it is spent per configuration, so it
                    # is totalled per configuration here as well as per turn in the
                    # sidecars (which now carry `config_index` to join back on).
                    "prompt_tokens": sum(r.prompt_tokens for r in outcome.responses),
                    "completion_tokens": sum(r.completion_tokens for r in outcome.responses),
                    "cost_usd": sum(r.cost_usd for r in outcome.responses),
                    "wall_clock_seconds": sum(r.wall_clock_seconds for r in outcome.responses),
                    "interactions": (
                        len(outcome.entry["traces"]) if outcome.entry else 0
                    ),
                    "rejected_interactions": (
                        outcome.entry["rejected_interactions"] if outcome.entry else []
                    ),
                    "error": outcome.error,
                }
                for outcome in outcomes
            ],
            # The evidence that the boundary held: every tool call and the decision made
            # about it, including every refusal.
            "tool_audit": [
                {"index": outcome.index, "calls": outcome.audit} for outcome in outcomes
            ],
            "refused_calls": sum(
                1 for outcome in outcomes for call in outcome.audit if not call["allowed"]
            ),
        },
        prompt_tokens=sum(response.prompt_tokens for response in responses),
        completion_tokens=sum(response.completion_tokens for response in responses),
        cost_usd=sum(response.cost_usd for response in responses),
        wall_clock_seconds=sum(response.wall_clock_seconds for response in responses),
        inputs={
            "configs_source": configs_source,
            "caruca_v1_root": str(v1.v1_root()),
            "isolation": isolation.name if isolation else "host",
            "max_turns": max_turns,
            "limit": limit,
            "execution_env": v1.EXECUTION_ENV,
            "execution_timeout_seconds": v1.EXECUTION_TIMEOUT_SECONDS,
            "placeholder_sandbox": v1.PLACEHOLDER_SANDBOX,
            "replaces_v1_modules": ["tracer/tracer.py", "tracer/strace_parser.py"],
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

    return TraceResult(
        run_id=run_dir.run_id,
        run_dir=run_dir.path,
        status=status,
        traces_path=traces_path,
        records=records,
        manifest=manifest,
        validation=validation,
        outcomes=outcomes,
    )
