/**
 * Reading v2's run directories.
 *
 * A run directory is the unit of evidence: one manifest, one telemetry sidecar per model turn,
 * and the stage's outputs. Nothing here recomputes a number - it reads what the run recorded.
 * Where a run recorded nothing, that shows as absent, never as zero (the rule the Python side
 * states in `telemetry.py`: "A null token count is a bug, not a zero").
 */
import { readFileSync, readdirSync, statSync } from "node:fs";
import { basename, join } from "node:path";
import {
  runManifestSchema,
  telemetryRecordSchema,
  type RunManifest,
  type Stage,
  type TelemetryRecord,
} from "./schema.js";
import { reconstructCommand, type ReconstructedCommand } from "./commandLine.js";
import { repoPaths } from "./paths.js";

const SIDECAR_SUFFIX = ".telemetry.json";
const MANIFEST_NAME = "manifest.json";
const CONVERSATION_NAME = "conversation.jsonl";
/** Written by this console for runs it starts (task 010 §7). Older runs have none. */
export const RECORDING_NAME = "terminal.cast";

export class RunNotFoundError extends Error {}
export class RunUnreadableError extends Error {}

export interface RunFile {
  readonly name: string;
  readonly path: string;
  readonly bytes: number;
}

export interface LoadedRun {
  readonly runId: string;
  readonly dir: string;
  readonly manifest: RunManifest;
  /** One per model turn, ordered by turn. Empty for a run that recorded none. */
  readonly turns: TelemetryRecord[];
  readonly commandLine: ReconstructedCommand;
  /** Absent for every run made before this console existed - all 163 of them. */
  readonly recordingPath: string | null;
  /** No run has used `--log-conversation` so far; the Inspect screen says so. */
  readonly conversationPath: string | null;
  readonly files: RunFile[];
}

function readJson(path: string): unknown {
  let text: string;
  try {
    text = readFileSync(path, "utf8");
  } catch (cause) {
    throw new RunUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }
  try {
    return JSON.parse(text);
  } catch (cause) {
    throw new RunUnreadableError(`${path} is not valid JSON: ${(cause as Error).message}`);
  }
}

export function loadManifest(runDir: string): RunManifest {
  const path = join(runDir, MANIFEST_NAME);
  const parsed = runManifestSchema.safeParse(readJson(path));
  if (!parsed.success) {
    throw new RunUnreadableError(
      `${path} does not match the manifest shape: ${parsed.error.issues
        .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
        .join("; ")}`,
    );
  }
  return parsed.data;
}

/**
 * Every telemetry sidecar in a run directory, ordered by turn.
 *
 * Stage 1 writes `<command>.telemetry.json`; the agentic stages write
 * `<command>.turn-NN.telemetry.json`, and stage 4 puts the format in too. Rather than parse
 * those names, the turn number is taken from inside each record, which is where it is
 * authoritative. Sorting on the filename would put turn-10 before turn-02 for a ten-turn run,
 * which is exactly the `cat` trace in §10's acceptance table.
 */
export function loadTurns(runDir: string): TelemetryRecord[] {
  const records: TelemetryRecord[] = [];
  for (const name of readdirSync(runDir)) {
    if (!name.endsWith(SIDECAR_SUFFIX)) continue;
    const path = join(runDir, name);
    const parsed = telemetryRecordSchema.safeParse(readJson(path));
    if (!parsed.success) {
      throw new RunUnreadableError(
        `${path} does not match the telemetry shape: ${parsed.error.issues
          .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
          .join("; ")}`,
      );
    }
    records.push(parsed.data);
  }
  records.sort((a, b) => a.turn - b.turn || (a.config_index ?? 0) - (b.config_index ?? 0));
  return records;
}

function optionalFile(dir: string, name: string): string | null {
  const path = join(dir, name);
  try {
    return statSync(path).isFile() ? path : null;
  } catch {
    return null;
  }
}

export function loadRun(runDir: string): LoadedRun {
  let entries: string[];
  try {
    entries = readdirSync(runDir);
  } catch {
    throw new RunNotFoundError(`No run directory at ${runDir}`);
  }

  const manifest = loadManifest(runDir);
  const files: RunFile[] = entries
    .map((name) => ({ name, path: join(runDir, name) }))
    .filter((file) => {
      try {
        return statSync(file.path).isFile();
      } catch {
        return false;
      }
    })
    .map((file) => ({ ...file, bytes: statSync(file.path).size }))
    .sort((a, b) => a.name.localeCompare(b.name));

  return {
    runId: manifest.run_id,
    dir: runDir,
    manifest,
    turns: loadTurns(runDir),
    commandLine: reconstructCommand(manifest),
    recordingPath: optionalFile(runDir, RECORDING_NAME),
    conversationPath: optionalFile(runDir, CONVERSATION_NAME),
    files,
  };
}

export interface RunSummary {
  readonly runId: string;
  readonly dir: string;
  readonly stage: Stage;
  readonly command: string;
  readonly timestamp: string;
  readonly status: "ok" | "failed";
  readonly model: string;
  readonly promptVariant: string;
  readonly turns: number;
  readonly costUsd: number;
  readonly promptTokens: number;
  readonly completionTokens: number;
  readonly wallClockSeconds: number;
  readonly hasRecording: boolean;
}

function summarize(runDir: string, manifest: RunManifest): RunSummary {
  return {
    runId: manifest.run_id,
    dir: runDir,
    stage: manifest.stage,
    command: manifest.command,
    timestamp: manifest.timestamp,
    status: manifest.status,
    model: manifest.model_reported || manifest.model_requested,
    promptVariant: manifest.prompt_variant,
    turns: manifest.turns,
    costUsd: manifest.cost_usd,
    promptTokens: manifest.prompt_tokens,
    completionTokens: manifest.completion_tokens,
    wallClockSeconds: manifest.wall_clock_seconds,
    hasRecording: optionalFile(runDir, RECORDING_NAME) !== null,
  };
}

export interface ListRunsResult {
  readonly runs: RunSummary[];
  /**
   * Directories created by a run that then recorded nothing at all - not even a sidecar.
   *
   * There are 28 of these among the 163 directories on disk (measured 2026-09-22), and they
   * are a direct consequence of Phase 0(a): the directory is created when the run starts, and
   * the manifest is written only when it ends, so anything that dies in between leaves an
   * empty shell. They are mostly `rm`, `tee` and `tail` - the commands stage 3 has most
   * trouble with.
   *
   * They are counted, not hidden. A started-and-died run is evidence about reliability, and
   * silently dropping it from the listing would make the failure rate unobservable. But it is
   * not a run with results, so it is kept out of `runs`.
   */
  readonly startedWithoutRecord: string[];
  /**
   * Directories holding files that could not be parsed, with the reason.
   *
   * Distinct from the above: this is data that exists but is malformed, which is a defect to
   * investigate rather than a run that died. There are none today.
   */
  readonly unreadable: { dir: string; reason: string }[];
}

/** Every v2 run on disk, newest first, with the ones that recorded nothing kept separately. */
export function listRuns(runsRoot = repoPaths().v2Runs): ListRunsResult {
  const runs: RunSummary[] = [];
  const startedWithoutRecord: string[] = [];
  const unreadable: { dir: string; reason: string }[] = [];

  let entries: string[];
  try {
    entries = readdirSync(runsRoot);
  } catch {
    return { runs, startedWithoutRecord, unreadable };
  }

  for (const name of entries.sort()) {
    const dir = join(runsRoot, name);
    try {
      if (!statSync(dir).isDirectory()) continue;
    } catch {
      continue;
    }

    if (readdirSync(dir).length === 0) {
      startedWithoutRecord.push(name);
      continue;
    }

    try {
      runs.push(summarize(dir, loadManifest(dir)));
    } catch (cause) {
      unreadable.push({ dir: basename(dir), reason: (cause as Error).message });
    }
  }

  runs.sort((a, b) => b.runId.localeCompare(a.runId));
  return { runs, startedWithoutRecord, unreadable };
}

/** Find one run by its id, without the caller knowing which root it lives under. */
export function findRun(runId: string, roots?: string[]): string {
  const paths = repoPaths();
  for (const root of roots ?? [paths.v2Runs, paths.v1Runs]) {
    const dir = join(root, runId);
    try {
      if (statSync(dir).isDirectory()) return dir;
    } catch {
      // Not under this root; try the next.
    }
  }
  throw new RunNotFoundError(`No run directory named ${runId}`);
}
