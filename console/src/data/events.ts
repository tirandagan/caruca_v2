/**
 * One event format for replay and live alike (§7).
 *
 * The rule that shapes this module: **numbers come from files, never from reading terminal
 * text.** The terminal recording is what a person saw; these events are what the run recorded.
 * They are kept apart deliberately, because parsing a progress bar for a token count is how a
 * reported figure stops matching the evidence behind it.
 *
 * Phase 0(a) constrains the timing. Sidecars are written when the run ends and every one
 * carries the run's start time, so a turn's own clock time was never recorded. Turn timings
 * here are therefore *derived*: each turn is placed by accumulating the `wall_clock_seconds`
 * of the turns before it. That is honest about ordering and duration, and every derived
 * timestamp is marked `timingDerived: true` so no screen presents it as measured.
 */
import type { LoadedRun } from "./runs.js";
import type { RunManifest, TelemetryRecord } from "./schema.js";
import { annotationFormatOf } from "./commandLine.js";

export type RunEvent =
  | RunStartEvent
  | PromptSentEvent
  | ModelTurnEvent
  | ToolCallEvent
  | TraceSessionEvent
  | ArtifactWrittenEvent
  | CheckEvent
  | RunEndEvent;

interface EventBase {
  /** Seconds from the start of the run. */
  readonly at: number;
  /**
   * True when `at` was computed rather than recorded (Phase 0(a)). Every v2 event from an
   * existing run is derived; only a run this console started records its own timings.
   */
  readonly timingDerived: boolean;
  readonly runId: string;
}

export interface RunStartEvent extends EventBase {
  readonly kind: "run_start";
  readonly side: "v1" | "v2";
  readonly stage: string;
  readonly command: string;
  readonly argv: string[];
  /** True when `argv` was rebuilt from the manifest rather than captured (Phase 0(b)). */
  readonly argvReconstructed: boolean;
  readonly model: string;
  readonly where: "mac" | "lima";
}

export interface PromptSentEvent extends EventBase {
  readonly kind: "prompt_sent";
  readonly system: string;
  readonly user: string;
  readonly promptHash: string;
  readonly promptFiles: string[];
  readonly promptVariant: string;
}

export interface ModelTurnEvent extends EventBase {
  readonly kind: "model_turn";
  readonly turn: number;
  readonly configIndex: number | null;
  readonly promptTokens: number;
  readonly completionTokens: number;
  readonly costUsd: number;
  readonly seconds: number;
  readonly modelId: string;
}

export interface ToolCallEvent extends EventBase {
  readonly kind: "tool_call";
  readonly configIndex: number | null;
  readonly name: string;
  readonly allowed: boolean;
  /** Why a call was refused. Present only for refusals. */
  readonly reason?: string;
  readonly arguments?: unknown;
}

export interface TraceSessionEvent extends EventBase {
  readonly kind: "trace_session";
  readonly configIndex: number;
  readonly invocation: string;
  /** `"ok"`, or `"no_report"` for a session that never called the reporting tool. */
  readonly status: string;
  /**
   * Whether the session reported anything at all.
   *
   * Derived from `status`, not from the interaction count: a session that ran and genuinely
   * observed nothing is a different outcome from one that ended without reporting, and zero
   * interactions cannot tell them apart. One of `cat`'s five sessions is the latter (§10).
   */
  readonly reported: boolean;
  /** Why the session stopped: `finished`, `no_tool_calls`, a turn cap. */
  readonly stopReason: string | null;
  readonly interactions: number;
  readonly rejectedInteractions: number;
  readonly executions: number;
  readonly turns: number;
  readonly costUsd: number;
  readonly error: string | null;
}

export interface ArtifactWrittenEvent extends EventBase {
  readonly kind: "artifact_written";
  readonly path: string;
  /** Which stage consumes this file next, where one does. */
  readonly consumedBy: string | null;
}

export interface CheckEvent extends EventBase {
  readonly kind: "check";
  readonly name: string;
  readonly passed: boolean | null;
  readonly detail: unknown;
}

export interface RunEndEvent extends EventBase {
  readonly kind: "run_end";
  readonly status: "ok" | "failed";
  readonly failureReason: string | null;
  readonly turns: number;
  readonly costUsd: number;
  readonly promptTokens: number;
  readonly completionTokens: number;
}

/** Which stage reads each stage's output next, for the artifacts panel (§6.3). */
const CONSUMED_BY: Record<string, string | null> = {
  syntax_spec: "generate",
  generate: "trace",
  trace: "annotate",
  annotate: null,
};

function whereItRan(manifest: RunManifest): "mac" | "lima" {
  const isolation = manifest.inputs["isolation"];
  if (typeof isolation === "string" && isolation.startsWith("lima")) return "lima";
  const runner = manifest.inputs["v1_runner"];
  if (typeof runner === "string" && runner === "lima") return "lima";
  return "mac";
}

function toolCallsFrom(manifest: RunManifest, runId: string, at: number): ToolCallEvent[] {
  const audit = manifest.checks["tool_audit"];
  if (!Array.isArray(audit)) return [];

  const events: ToolCallEvent[] = [];
  for (const entry of audit) {
    if (typeof entry !== "object" || entry === null) continue;
    const record = entry as { index?: unknown; calls?: unknown };
    const configIndex = typeof record.index === "number" ? record.index : null;
    if (!Array.isArray(record.calls)) continue;
    for (const call of record.calls) {
      if (typeof call !== "object" || call === null) continue;
      const c = call as Record<string, unknown>;
      // The audit records the tool under `tool`. `name` is accepted too, so a later stage that
      // uses the more conventional key does not silently produce a rail full of "(unnamed)".
      const tool = typeof c["tool"] === "string" ? (c["tool"] as string) : c["name"];
      events.push({
        kind: "tool_call",
        runId,
        at,
        timingDerived: true,
        configIndex,
        name: typeof tool === "string" ? tool : "(tool not recorded)",
        allowed: c["allowed"] !== false,
        ...(typeof c["reason"] === "string" ? { reason: c["reason"] as string } : {}),
        ...(c["arguments"] !== undefined ? { arguments: c["arguments"] } : {}),
      });
    }
  }
  return events;
}

function sessionsFrom(manifest: RunManifest, runId: string, at: number): TraceSessionEvent[] {
  const sessions = manifest.checks["sessions"];
  if (!Array.isArray(sessions)) return [];

  const int = (value: unknown): number => {
    if (typeof value === "number") return value;
    // Recorded as a count today; tolerate a list in case a later stage records the items.
    return Array.isArray(value) ? value.length : 0;
  };

  return sessions.flatMap((entry, position) => {
    if (typeof entry !== "object" || entry === null) return [];
    const s = entry as Record<string, unknown>;
    const status = typeof s["status"] === "string" ? (s["status"] as string) : "unknown";
    return [
      {
        kind: "trace_session" as const,
        runId,
        at,
        timingDerived: true,
        configIndex: typeof s["index"] === "number" ? (s["index"] as number) : position,
        invocation: typeof s["invocation"] === "string" ? (s["invocation"] as string) : "",
        status,
        reported: status !== "no_report",
        stopReason: typeof s["stop_reason"] === "string" ? (s["stop_reason"] as string) : null,
        interactions: int(s["interactions"]),
        rejectedInteractions: int(s["rejected_interactions"]),
        executions: int(s["executions"]),
        turns: int(s["turns"]),
        costUsd: typeof s["cost_usd"] === "number" ? (s["cost_usd"] as number) : 0,
        error: typeof s["error"] === "string" ? (s["error"] as string) : null,
      },
    ];
  });
}

/**
 * Build the event stream for a v2 run that is already on disk.
 *
 * Turn events are laid out by accumulating each turn's own duration, because no per-turn
 * clock time was recorded. Everything else is attached at the point in that timeline where it
 * can be justified: the prompt at the start, artifacts and checks at the end.
 */
export function eventsForRun(run: LoadedRun): RunEvent[] {
  const { manifest, turns } = run;
  const runId = manifest.run_id;
  const events: RunEvent[] = [];

  events.push({
    kind: "run_start",
    runId,
    at: 0,
    timingDerived: true,
    side: "v2",
    stage: manifest.stage,
    command: manifest.command,
    argv: [run.commandLine.program, ...run.commandLine.args],
    argvReconstructed: true,
    model: manifest.model_requested,
    where: whereItRan(manifest),
  });

  events.push({
    kind: "prompt_sent",
    runId,
    at: 0,
    timingDerived: true,
    system: manifest.prompt_system,
    user: manifest.prompt_user,
    promptHash: manifest.prompt_hash,
    promptFiles: manifest.prompt_files,
    promptVariant: manifest.prompt_variant,
  });

  let elapsed = 0;
  for (const turn of turns as TelemetryRecord[]) {
    elapsed += turn.wall_clock_seconds;
    events.push({
      kind: "model_turn",
      runId,
      at: elapsed,
      timingDerived: true,
      turn: turn.turn,
      configIndex: turn.config_index,
      promptTokens: turn.prompt_tokens,
      completionTokens: turn.completion_tokens,
      costUsd: turn.cost_usd,
      seconds: turn.wall_clock_seconds,
      modelId: turn.model_id,
    });
  }

  events.push(...sessionsFrom(manifest, runId, elapsed));
  events.push(...toolCallsFrom(manifest, runId, elapsed));

  for (const path of manifest.output_paths) {
    events.push({
      kind: "artifact_written",
      runId,
      at: elapsed,
      timingDerived: true,
      path,
      consumedBy: CONSUMED_BY[manifest.stage] ?? null,
    });
  }

  if (manifest.validation) {
    events.push({
      kind: "check",
      runId,
      at: elapsed,
      timingDerived: true,
      name: "v1_validation",
      // `available: false` means v1's environment could not be reached, which is not the same
      // as v1 rejecting the artifact. Null keeps the two apart.
      passed: manifest.validation.available ? manifest.validation.passed : null,
      detail: manifest.validation,
    });
  }

  events.push({
    kind: "run_end",
    runId,
    at: elapsed,
    timingDerived: true,
    status: manifest.status,
    failureReason: manifest.failure_reason,
    turns: manifest.turns,
    costUsd: manifest.cost_usd,
    promptTokens: manifest.prompt_tokens,
    completionTokens: manifest.completion_tokens,
  });

  return events;
}

/** A one-line description of a run, for the stage rail beside the terminal. */
export function describeRun(manifest: RunManifest): string {
  const format = manifest.stage === "annotate" ? annotationFormatOf(manifest) : null;
  const what = format ? `${manifest.stage} (${format})` : manifest.stage;
  return `${what} · ${manifest.command} · ${manifest.model_reported || manifest.model_requested}`;
}
