"use server";

/**
 * The console's only mutating operations.
 *
 * Kept in one file so that "what can this page change" has a single answer. Everything else in
 * the console reads.
 */
import { revalidatePath } from "next/cache";
import { analyzeDeletion, deleteRuns, type DeletionAnalysis, type DeletionResult } from "../data/deleteRuns.js";
import { listFindings } from "../data/findings.js";
import { recheckEvidence, recipeOf, type RecheckOutcome } from "../data/recheck.js";
import { countEnumeration } from "../data/preflight.js";
import { all, get, stop, type LiveRun, type RunState, type StopResult } from "../server/processes.js";
import {
  startV1,
  startV2,
  startV2Tool,
  PaidRunNotConfirmedError,
  type StartV1Options,
  type StartV2Options,
  type V2Tool,
} from "../server/startRun.js";

/** What deleting these runs would cost. Reads only. */
export async function previewDeletion(runIds: string[]): Promise<DeletionAnalysis> {
  return analyzeDeletion(runIds);
}

/**
 * Delete runs. Irreversible on disk, though the files remain in git history.
 *
 * The analysis is re-run inside `deleteRuns`, so a confirmation built from a stale page cannot
 * cause something other than what it described to be removed.
 */
export async function confirmDeletion(
  runIds: string[],
  reason: string,
): Promise<DeletionResult> {
  const trimmed = reason.trim();
  const result = deleteRuns(runIds, trimmed ? { reason: trimmed } : {});
  revalidatePath("/");
  return result;
}

export interface FindingRecheck {
  readonly findingId: string;
  readonly outcomes: (RecheckOutcome & { label: string })[];
}

/**
 * Re-derive every number in one finding and report whether each still holds.
 *
 * Slow on purpose: a campaign-level check re-scores the whole campaign from its run artifacts
 * with today's scorer, which takes tens of seconds. That is the price of an answer that means
 * something. Nothing is written - `report --rescore` recomputes in memory, so a re-check
 * cannot alter the evidence it is checking.
 */
export async function recheckFinding(findingId: string): Promise<FindingRecheck> {
  const finding = listFindings().findings.find(
    (candidate) => candidate.frontmatter.id === findingId,
  );
  if (!finding) throw new Error(`No finding named ${findingId}.`);

  const outcomes: (RecheckOutcome & { label: string })[] = [];
  for (const evidence of finding.frontmatter.evidence) {
    const outcome = await recheckEvidence(evidence, recipeOf(evidence));
    outcomes.push({ ...outcome, label: evidence.label });
  }
  return { findingId, outcomes };
}

export interface CountResult {
  readonly printed: number;
  readonly distinct: number;
  readonly executions: number | null;
  readonly capped: boolean;
  readonly cappedReason: string | null;
  readonly argv: string[];
  readonly seconds: number;
}

/**
 * Count what v1 would enumerate, by running its `generate` and counting the lines.
 *
 * Free and safe: `generate` prints invocation strings and executes nothing. `--number` is
 * never used — it disagrees with actual emission on every command checked.
 */
export async function countInvocations(
  command: string,
  maxArity: number,
  maxCount: number,
): Promise<CountResult> {
  const result = await countEnumeration(command, { maxArity, maxCount });
  return {
    printed: result.printed,
    distinct: result.distinct,
    executions: result.executions,
    capped: result.capped,
    cappedReason: result.cappedReason,
    argv: [...result.argv],
    seconds: result.seconds,
  };
}

export interface StartedRunSummary {
  readonly runId: string;
  readonly side: "v1" | "v2";
  readonly commandLine: string;
  readonly where: "mac" | "lima";
  readonly paid: boolean;
  /** Runs that were already going. Their wall-clock times are not comparable with this one. */
  readonly concurrentWith: string[];
}

function summarize(run: LiveRun, commandLine: string, paid: boolean): StartedRunSummary {
  return {
    runId: run.runId,
    side: run.side,
    commandLine,
    where: run.where,
    paid,
    concurrentWith: run.concurrentWith,
  };
}

/**
 * Start one of v1's steps.
 *
 * Only a live stage 1 costs anything, and it is refused without an explicit go-ahead — v1's
 * LLM step is a paid call that v1 itself does not meter.
 */
export async function startV1Run(options: StartV1Options): Promise<StartedRunSummary> {
  const started = startV1(options);
  revalidatePath("/");
  return summarize(started.run, started.commandLine, started.paid);
}

/**
 * Start one of v2's stages. Every one calls a paid model, so every one needs a go-ahead, and
 * the estimate that was shown is checked against the one that holds now.
 */
export async function startV2Run(options: StartV2Options): Promise<StartedRunSummary> {
  const started = startV2(options);
  revalidatePath("/");
  return summarize(started.run, started.commandLine, started.paid);
}

/**
 * Stop a run, on this Mac and — for a Lima run — inside the VM as well.
 *
 * The result says what was still running in the guest afterwards, rather than assuming that
 * killing `limactl` on the host stopped what it started inside.
 */
export async function stopRun(runId: string): Promise<StopResult> {
  const result = await stop(runId);
  revalidatePath("/");
  return result;
}

export interface LiveRunSummary {
  readonly runId: string;
  readonly side: "v1" | "v2";
  readonly argv: string[];
  readonly where: "mac" | "lima";
  readonly state: RunState;
  readonly exitCode: number | null;
  readonly startedAt: number;
  readonly concurrentWith: string[];
}

/** Every run this server knows about, including ones that have finished since it started. */
export async function liveRuns(): Promise<LiveRunSummary[]> {
  return all().map((run) => ({
    runId: run.runId,
    side: run.side,
    argv: [...run.argv],
    where: run.where,
    state: run.state,
    exitCode: run.exitCode,
    startedAt: run.startedAt,
    concurrentWith: run.concurrentWith,
  }));
}

export async function liveRun(runId: string): Promise<LiveRunSummary | null> {
  const run = get(runId);
  if (!run) return null;
  return {
    runId: run.runId,
    side: run.side,
    argv: [...run.argv],
    where: run.where,
    state: run.state,
    exitCode: run.exitCode,
    startedAt: run.startedAt,
    concurrentWith: run.concurrentWith,
  };
}

export { PaidRunNotConfirmedError };

/** Run one of v2's free tools. Nothing to confirm: they call no model. */
export async function startV2ToolRun(tool: V2Tool): Promise<StartedRunSummary> {
  const started = startV2Tool(tool);
  revalidatePath("/");
  return summarize(started.run, started.commandLine, started.paid);
}
