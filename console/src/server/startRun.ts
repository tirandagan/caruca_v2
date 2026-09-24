/**
 * Starting a run, and the confirmation that has to come first.
 *
 * Phase 5 is the only part of the console that can spend money, so the rule here is that
 * **nothing that calls a paid model starts without being asked for by name.** A caller must
 * pass the estimate it showed and say the person agreed to it; a mismatch between what was
 * shown and what is about to run is refused rather than reconciled.
 *
 * Everything v1 runs is built through `v1Invocations.ts`, so the forms and the output guard
 * apply here by construction rather than by remembering to apply them.
 */
import { randomBytes } from "node:crypto";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
import { repoPaths, v1Root } from "../data/paths.js";
import {
  displayInvocation,
  v1Annotate,
  v1Generate,
  v1SyntaxSpec,
  v1Trace,
  type GenerationBounds,
  type V1Invocation,
} from "../data/v1Invocations.js";
import { PINNED_V1_COMMIT, estimateCost, whereItMustRun } from "../data/preflight.js";
import { TERMINAL_COLS, TERMINAL_ROWS, start, type LiveRun } from "./processes.js";
import type { Stage } from "../data/schema.js";
import type { V1RunManifest } from "../data/v1Runs.js";

export class PaidRunNotConfirmedError extends Error {}

/** `<UTC timestamp>_<command>_<suffix>`, the same shape v2's own run directories use. */
export function newRunId(command: string): string {
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\..*/, "Z");
  const compact = `${stamp.slice(0, 4)}-${stamp.slice(4, 6)}-${stamp.slice(6)}`;
  return `${compact}_${command}_${randomBytes(4).toString("hex")}`;
}

export interface StartV1Options {
  readonly stage: Stage;
  readonly command: string;
  readonly bounds?: GenerationBounds;
  readonly limaInstance?: string;
  /** For stage 1 only: a live model call, or v1's committed specification. */
  readonly stage1Mode?: "live" | "fetch";
  readonly format?: string;
  /**
   * Required when the step calls a paid model.
   *
   * Carries the figure that was shown, so a run cannot start against an estimate the person
   * never saw.
   */
  readonly confirmation?: { readonly acceptedUsd: number | null; readonly confirmed: boolean };
}

function v1Commit(root: string): string {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: root,
      encoding: "utf8",
      timeout: 10_000,
    }).trim();
  } catch {
    return "unknown";
  }
}

/**
 * Environment variable *names* the run will see, for the record.
 *
 * Names only, and only the ones that matter to how v1 behaves. A value is never recorded.
 */
function recordedEnvNames(): string[] {
  return ["PATH", "HOME", "SHELL", "TERM", "CARUCA_V1_ROOT", "CARUCA_ISOLATION_METHOD"].filter(
    (name) => name in process.env,
  );
}

function v1ManifestFor(
  runId: string,
  invocation: V1Invocation,
  options: StartV1Options,
): Omit<V1RunManifest, "ended_at" | "exit_code" | "concurrent_with"> {
  const root = v1Root();
  return {
    run_id: runId,
    subcommand: invocation.subcommand,
    command: options.command,
    format: options.format ?? null,
    argv: [...invocation.argv],
    cwd: invocation.cwd,
    venv: invocation.venv,
    where: invocation.where,
    lima_instance: invocation.limaInstance,
    used_shell: invocation.usesShell,
    v1_commit: v1Commit(root),
    env_var_names: recordedEnvNames(),
    started_at: new Date().toISOString(),
    machine: process.platform === "darwin" ? "mac" : process.platform,
    terminal_size: { cols: TERMINAL_COLS, rows: TERMINAL_ROWS },
    output_paths: invocation.outputPath ? [invocation.outputPath] : [],
    llm_prompt_tokens: null,
    llm_completion_tokens: null,
    llm_cost_usd: null,
    llm_model_reported: null,
    per_step_seconds: null,
  };
}

export interface StartedRun {
  readonly run: LiveRun;
  readonly commandLine: string;
  /** True when this run sent a prompt to a paid model. */
  readonly paid: boolean;
}

/**
 * Start one of v1's steps.
 *
 * Only stage 1 in `live` mode costs anything, and only then is a confirmation required. v1's
 * own LLM step is unmetered — it records no tokens and no cost — which is why the console
 * routes it through a meter, and why the pre-flight says plainly that it is a paid call v1
 * does not account for.
 */
export function startV1(options: StartV1Options): StartedRun {
  const runId = newRunId(options.command);
  const runDir = join(repoPaths().v1Runs, runId);
  const bounds = options.bounds ?? {};
  const paid = options.stage === "syntax_spec" && options.stage1Mode === "live";

  if (paid && !options.confirmation?.confirmed) {
    throw new PaidRunNotConfirmedError(
      "A live v1 stage 1 is a paid call that v1 itself does not meter. It needs an explicit go-ahead.",
    );
  }

  let invocation: V1Invocation;
  switch (options.stage) {
    case "syntax_spec":
      invocation = v1SyntaxSpec(options.command, {
        ...(options.stage1Mode === "fetch" ? { fetch: true } : {}),
      });
      break;
    case "generate":
      invocation = v1Generate(options.command, bounds);
      break;
    case "trace":
      invocation = v1Trace(options.command, join(runDir, `${options.command}.json`), bounds, {
        ...(options.limaInstance ? { limaInstance: options.limaInstance } : {}),
      });
      break;
    case "annotate":
      invocation = v1Annotate(
        options.format ?? "pash",
        options.command,
        join(runDir, `${options.command}.json`),
        { ...(options.limaInstance ? { limaInstance: options.limaInstance } : {}) },
      );
      break;
  }

  const run = start({
    runId,
    side: "v1",
    argv: invocation.argv,
    cwd: invocation.cwd,
    runDir,
    where: invocation.where,
    limaInstance: invocation.limaInstance,
    v1Manifest: v1ManifestFor(runId, invocation, options),
    title: `v1 ${invocation.subcommand} ${options.command}`,
  });

  return { run, commandLine: displayInvocation(invocation), paid };
}

export interface StartV2Options {
  readonly stage: Stage;
  readonly command: string;
  readonly model: string;
  readonly temperature?: number;
  readonly bounds?: GenerationBounds;
  readonly format?: string;
  readonly limaInstance?: string;
  readonly extraArgs?: readonly string[];
  readonly confirmation?: { readonly acceptedUsd: number | null; readonly confirmed: boolean };
}

const V2_SUBCOMMAND: Record<Stage, string> = {
  syntax_spec: "naive-llm",
  generate: "generate",
  trace: "trace",
  annotate: "annotate",
};

/**
 * Start one of v2's stages.
 *
 * **Every v2 stage calls a paid model**, so every one needs a confirmation. The estimate that
 * was shown is checked against the one that holds now: if the two differ by more than a cent
 * the run is refused, because the figure the person agreed to is no longer the figure in
 * front of them.
 */
export function startV2(options: StartV2Options): StartedRun {
  const estimate = estimateCost(options.stage, options.model);

  if (!options.confirmation?.confirmed) {
    throw new PaidRunNotConfirmedError(
      `${options.stage} with ${options.model} calls a paid model and needs an explicit go-ahead.`,
    );
  }

  const shown = options.confirmation.acceptedUsd;
  if (shown !== null && estimate.usdPerRun !== null && Math.abs(shown - estimate.usdPerRun) > 0.01) {
    throw new PaidRunNotConfirmedError(
      `The estimate has moved since it was shown: $${shown.toFixed(4)} then, ` +
        `$${estimate.usdPerRun.toFixed(4)} now. Look again before starting it.`,
    );
  }

  const runId = newRunId(options.command);
  const paths = repoPaths();
  const { where } = whereItMustRun("v2", options.stage, options.command);

  const argv = [
    join(paths.root, ".venv", "bin", "caruca-v2"),
    V2_SUBCOMMAND[options.stage],
  ];

  const bounds = options.bounds ?? {};
  if (options.stage === "generate") {
    if (bounds.maxArity !== undefined) argv.push("--max-arity", String(bounds.maxArity));
    if (bounds.maxCount !== undefined) argv.push("--max-count", String(bounds.maxCount));
  }
  if (options.stage === "trace") {
    argv.push("--isolation", where === "lima" ? "lima" : "host");
    if (where === "lima") argv.push("--lima-instance", options.limaInstance ?? "caruca");
  }
  if (options.stage === "annotate") {
    argv.push("--v1-runner", where === "lima" ? "lima" : "host");
    if (where === "lima") argv.push("--lima-instance", options.limaInstance ?? "caruca");
    argv.push(options.format ?? "pash");
  }

  argv.push(
    options.command,
    "--model",
    options.model,
    "--temperature",
    String(options.temperature ?? 0),
    ...(options.extraArgs ?? []),
  );

  // v2 writes its own run directory; the console records the terminal beside it.
  const runDir = join(paths.v2Runs, runId);

  const run = start({
    runId,
    side: "v2",
    argv,
    cwd: paths.root,
    runDir,
    where,
    limaInstance: where === "lima" ? (options.limaInstance ?? "caruca") : null,
    v1Manifest: null,
    title: `v2 ${V2_SUBCOMMAND[options.stage]} ${options.command}`,
    // v2 mints its own run id; the recording is moved into its directory when it ends.
    adoptV2RunDir: true,
  });

  return { run, commandLine: argv.join(" "), paid: true };
}

/** The pinned commit, re-exported so callers can warn without importing the pre-flight. */
export { PINNED_V1_COMMIT };

/**
 * The free v2 tools: the ones that call no model.
 *
 * `score --self-test` scores each committed exemplar specification against itself, so every
 * cell must come out perfect — it is the quickest check that the harness is sound, and it
 * costs nothing. `metrics rebuild` regenerates the database from the telemetry files on disk.
 *
 * Kept apart from `startV2` because these need no confirmation: there is nothing to confirm.
 */
export type V2Tool = "score-self-test" | "metrics-rebuild";

const V2_TOOL_ARGS: Record<V2Tool, string[]> = {
  "score-self-test": ["score", "--self-test"],
  "metrics-rebuild": ["metrics", "rebuild"],
};

export function startV2Tool(tool: V2Tool): StartedRun {
  const paths = repoPaths();
  const runId = newRunId(tool.replace(/[^a-z0-9]+/g, "-"));
  const argv = [join(paths.root, ".venv", "bin", "caruca-v2"), ...V2_TOOL_ARGS[tool]];

  const run = start({
    runId,
    side: "v2",
    argv,
    cwd: paths.root,
    // A tool writes no run directory of its own, so the recording goes beside the v1 runs,
    // which is where the console keeps recordings it owns.
    runDir: join(paths.v1Runs, runId),
    where: "mac",
    limaInstance: null,
    v1Manifest: null,
    title: `v2 ${V2_TOOL_ARGS[tool].join(" ")}`,
  });

  return { run, commandLine: argv.join(" "), paid: false };
}
