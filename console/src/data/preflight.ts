/**
 * The pre-flight: what a run would do, before anything runs (§6.2).
 *
 * Everything here reads or counts. Nothing it does costs money and nothing it does executes a
 * traced command. Its job is to make the three things that have caught this project out
 * visible in advance: how much v1 would actually enumerate, which steps would call a paid
 * model, and whether the environment each side needs is actually there.
 */
import { execFile, execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { promisify } from "node:util";
import { repoPaths, v1Root } from "./paths.js";
import { v1Generate, v1Trace, type GenerationBounds } from "./v1Invocations.js";
import { runTotals } from "./metricsDb.js";
import type { Stage } from "./schema.js";

const run = promisify(execFile);

/** v1's commit the whole comparison is pinned to. */
export const PINNED_V1_COMMIT = "d8032407346aadc135b14c043618c8c1d4f4e0cf";

/**
 * Caps on the counting itself.
 *
 * E0 found 16 of 120 commands exceed 500,000 printed lines, and `convert`'s own hint is
 * 4.7 billion invocations. Counting has to be able to give up and say so, because a pre-flight
 * that hangs is worse than one that reports a bound.
 */
export const LINE_CAP = 500_000;
export const COUNT_TIMEOUT_MS = 120_000;

export interface EnumerationCount {
  readonly command: string;
  /** Lines v1 printed. Duplicates included, because v1 emits them and the tracer runs them. */
  readonly printed: number;
  /** How many of those are distinct. */
  readonly distinct: number;
  /** Executions `trace` would perform, from `--length-only`. Null when not asked for. */
  readonly executions: number | null;
  /** True when counting stopped at the cap or the time limit. */
  readonly capped: boolean;
  readonly cappedReason: string | null;
  /** Exactly what was run, so anyone can repeat it. */
  readonly argv: readonly string[];
  readonly seconds: number;
}

/**
 * Count by running v1's `generate` and counting what it prints.
 *
 * **`--number` is never used.** E0 found it disagrees with actual emission on all 90 commands
 * that enumerate fully, and crashes outright on 14 — including `pwd`, which is in the parity
 * set. It uses a different code path from the enumeration it claims to count.
 *
 * `generate` executes nothing: it prints invocation strings. So this is free and safe even for
 * `rm`.
 */
export async function countEnumeration(
  command: string,
  bounds: GenerationBounds = {},
  options: { lineCap?: number; timeoutMs?: number } = {},
): Promise<EnumerationCount> {
  const invocation = v1Generate(command, bounds);
  const cap = options.lineCap ?? LINE_CAP;
  const startedAt = Date.now();

  let stdout = "";
  let capped = false;
  let cappedReason: string | null = null;

  try {
    const result = await run(invocation.argv[0]!, invocation.argv.slice(1), {
      cwd: invocation.cwd,
      timeout: options.timeoutMs ?? COUNT_TIMEOUT_MS,
      // Each line is short; the cap is on lines, and this bounds the buffer well past it.
      maxBuffer: 256 * 1024 * 1024,
      encoding: "utf8",
    });
    stdout = result.stdout;
  } catch (cause) {
    const error = cause as { stdout?: string; killed?: boolean; code?: string; message: string };
    stdout = error.stdout ?? "";
    capped = true;
    cappedReason = error.killed
      ? `stopped after ${(options.timeoutMs ?? COUNT_TIMEOUT_MS) / 1000}s`
      : error.message.split("\n")[0]!;
  }

  const lines = stdout.split("\n").filter((line) => line.length > 0);
  if (lines.length >= cap) {
    capped = true;
    cappedReason = cappedReason ?? `stopped at the ${cap.toLocaleString("en-US")}-line cap`;
  }

  const counted = lines.slice(0, cap);
  return {
    command,
    printed: counted.length,
    distinct: new Set(counted).size,
    executions: null,
    capped,
    cappedReason,
    argv: invocation.argv,
    seconds: (Date.now() - startedAt) / 1000,
  };
}

/**
 * How many executions `trace` would perform, from v1's own `--length-only`.
 *
 * Shown for what it is: executions including duplicates. At v1's defaults `mkdir` prints 4,240
 * invocations of which 1,094 are distinct, and tracing them is 10,368 executions — the tracer
 * inherits the duplicated stream rather than deduplicating it.
 */
export function countExecutions(
  command: string,
  bounds: GenerationBounds = {},
  options: { limaInstance?: string; timeoutMs?: number } = {},
): number | null {
  const invocation = v1Trace(command, join(repoPaths().v1Runs, "_length-only", "unused.json"), bounds, {
    ...(options.limaInstance ? { limaInstance: options.limaInstance } : {}),
    lengthOnly: true,
  });
  try {
    const stdout = execFileSync(invocation.argv[0]!, invocation.argv.slice(1), {
      cwd: invocation.cwd,
      timeout: options.timeoutMs ?? COUNT_TIMEOUT_MS,
      encoding: "utf8",
    });
    const match = /(\d[\d,]*)/.exec(stdout.trim());
    return match ? Number(match[1]!.replace(/,/g, "")) : null;
  } catch {
    return null;
  }
}

/**
 * The variable names assigned in a `.env` file.
 *
 * Names only. The right-hand side is never parsed, so a secret cannot end up in a check
 * result, a log line or a screen. A missing or unreadable file is simply an empty set.
 */
export function envFileVariableNames(path: string): Set<string> {
  const names = new Set<string>();
  if (!existsSync(path)) return names;
  try {
    for (const line of readFileSync(path, "utf8").split("\n")) {
      const match = /^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=/.exec(line);
      if (match?.[1]) names.add(match[1]);
    }
  } catch {
    // Unreadable is the same as absent for this purpose.
  }
  return names;
}

export type CheckState = "ok" | "missing" | "unknown";

export interface EnvironmentCheck {
  readonly name: string;
  readonly state: CheckState;
  readonly detail: string;
}

/**
 * What each side needs, checked rather than assumed.
 *
 * API keys are checked for **presence only**. A value is never read into the console, never
 * logged and never displayed; the run record lists variable names, never values.
 */
export function checkEnvironment(options: { limaInstance?: string } = {}): EnvironmentCheck[] {
  const checks: EnvironmentCheck[] = [];
  const instance = options.limaInstance ?? "caruca";

  // --- the two CLIs ---
  const v2Bin = join(repoPaths().root, ".venv", "bin", "caruca-v2");
  checks.push({
    name: "caruca-v2",
    state: existsSync(v2Bin) ? "ok" : "missing",
    detail: existsSync(v2Bin) ? v2Bin : `not found at ${v2Bin} — run \`uv sync\``,
  });

  let root: string | null = null;
  try {
    root = v1Root();
  } catch {
    root = null;
  }

  if (!root) {
    checks.push({
      name: "v1 checkout",
      state: "missing",
      detail: "not found. Set CARUCA_V1_ROOT to the directory containing caruca/.",
    });
  } else {
    const venv = join(root, "caruca", ".venv", "bin", "caruca");
    checks.push({
      name: "v1 caruca (.venv)",
      state: existsSync(venv) ? "ok" : "missing",
      detail: existsSync(venv) ? venv : `not found at ${venv}`,
    });

    const venvLlm = join(root, "caruca", ".venv-llm", "bin", "caruca");
    checks.push({
      name: "v1 caruca (.venv-llm)",
      state: existsSync(venvLlm) ? "ok" : "missing",
      detail: existsSync(venvLlm)
        ? `${venvLlm} — the only venv v1's syntax-spec can run from`
        : "not found. v1's LLM step cannot run; the pre-flight will offer the archived output instead.",
    });

    // --- v1 pinned to the commit the comparison was measured at ---
    try {
      const head = execFileSync("git", ["rev-parse", "HEAD"], {
        cwd: root,
        encoding: "utf8",
        timeout: 10_000,
      }).trim();
      checks.push({
        name: "v1 commit",
        state: head === PINNED_V1_COMMIT ? "ok" : "missing",
        detail:
          head === PINNED_V1_COMMIT
            ? `${head.slice(0, 8)} — the pinned commit`
            : `${head.slice(0, 8)}, but the comparison is pinned to ${PINNED_V1_COMMIT.slice(0, 8)}. ` +
              `A run against a different v1 is not comparable with the recorded measurements.`,
      });
    } catch {
      checks.push({
        name: "v1 commit",
        state: "unknown",
        detail: "could not read v1's HEAD",
      });
    }
  }

  // --- Lima, which stage 3 needs on macOS ---
  try {
    const listed = execFileSync("limactl", ["list", "--format", "{{.Name}} {{.Status}}"], {
      encoding: "utf8",
      timeout: 15_000,
    });
    const line = listed
      .split("\n")
      .find((row) => row.trim().startsWith(`${instance} `));
    const running = line?.includes("Running") ?? false;
    checks.push({
      name: `Lima VM "${instance}"`,
      state: running ? "ok" : "missing",
      detail: line
        ? running
          ? line.trim()
          : `${line.trim()} — start it with \`limactl start ${instance}\``
        : `no VM named ${instance}`,
    });
  } catch {
    checks.push({
      name: `Lima VM "${instance}"`,
      state: "unknown",
      detail: "limactl is not on PATH. Tracing and v1's annotate both need it on macOS.",
    });
  }

  // --- keys: presence only, never the value ---
  //
  // Checked in two places, because the console's own environment is not where the key has to
  // be: `caruca-v2` loads `.env` itself when it starts. A key present only in `.env` is
  // perfectly usable, and reporting it as missing would send someone looking for a problem
  // that is not there.
  //
  // `.env` is scanned for the variable *name* at the start of a line. The value is never
  // parsed, never held and never returned.
  const dotEnvNames = envFileVariableNames(join(repoPaths().root, ".env"));

  for (const variable of ["OPENROUTER_API_KEY", "OPENAI_API_KEY"] as const) {
    const inProcess = Boolean(process.env[variable]);
    const inFile = dotEnvNames.has(variable);
    const present = inProcess || inFile;

    const where = inProcess && inFile ? "this shell and .env" : inProcess ? "this shell" : ".env";

    checks.push({
      name: variable,
      state: present ? "ok" : "missing",
      detail: present
        ? `set in ${where} (the value is never read, shown or recorded)`
        : variable === "OPENAI_API_KEY"
          ? "not set. v1's LLM step reaches OpenAI through this variable; the console points it at OpenRouter."
          : "not set, in this shell or in .env. Every v2 stage needs it.",
    });
  }

  return checks;
}

export interface CostEstimate {
  readonly stage: Stage;
  readonly model: string;
  /** Null when nothing comparable has been measured. Never a guess. */
  readonly usdPerRun: number | null;
  readonly promptTokens: number | null;
  readonly completionTokens: number | null;
  /** How many past runs the estimate is based on. */
  readonly basedOn: number;
  /** Stated in full, because an estimate without its basis is a guess. */
  readonly basis: string;
}

/**
 * What a stage is likely to cost, from measured runs of the same stage and model.
 *
 * **With no measured runs it says so rather than guessing.** A confident number with nothing
 * behind it is worse than an admission, because it gets quoted.
 */
export function estimateCost(stage: Stage, model: string): CostEstimate {
  const totals = runTotals({ stage, model }).filter((row) => row.cost_usd > 0);

  if (totals.length === 0) {
    return {
      stage,
      model,
      usdPerRun: null,
      promptTokens: null,
      completionTokens: null,
      basedOn: 0,
      basis: `no run of ${stage} with ${model} has been measured, so there is nothing to estimate from`,
    };
  }

  const mean = (pick: (row: (typeof totals)[number]) => number) =>
    totals.reduce((sum, row) => sum + pick(row), 0) / totals.length;

  const costs = totals.map((row) => row.cost_usd).sort((a, b) => a - b);
  return {
    stage,
    model,
    usdPerRun: mean((row) => row.cost_usd),
    promptTokens: Math.round(mean((row) => row.prompt_tokens)),
    completionTokens: Math.round(mean((row) => row.completion_tokens)),
    basedOn: totals.length,
    basis:
      `mean of ${totals.length} measured run${totals.length === 1 ? "" : "s"} of ${stage} ` +
      `with ${model}; observed range $${costs[0]!.toFixed(4)} to $${costs.at(-1)!.toFixed(4)}`,
  };
}

/** Commands v2's tooling refuses to execute on the host, so stage 3 must use Lima for them. */
export const DESTRUCTIVE_COMMANDS = ["rm", "rmdir", "mv", "dd", "shred", "truncate"] as const;

/**
 * Where a step has to run, decided rather than asked.
 *
 * §6.2: v1 always uses the forms in §3; v2's `trace` runs in Lima for any destructive command
 * because the host refuses it; v2's `annotate` uses `--v1-runner lima` on macOS, because v1's
 * annotator cannot run on macOS at all.
 */
export function whereItMustRun(
  side: "v1" | "v2",
  stage: Stage,
  command: string,
  platform: NodeJS.Platform = process.platform,
): { where: "mac" | "lima"; reason: string } {
  if (side === "v1") {
    if (stage === "trace") {
      return { where: "lima", reason: "v1's tracer needs strace and overlayfs" };
    }
    if (stage === "annotate") {
      return {
        where: "lima",
        reason:
          platform === "darwin"
            ? "v1's annotate cannot run on macOS at all: tracer/data.py resolves /tmp to /private/tmp and then fails a relative_to against the sandbox path"
            : "the parity study ran v1's annotate in the VM",
      };
    }
    return { where: "mac", reason: "the parity study ran it on the host" };
  }

  if (stage === "trace" && DESTRUCTIVE_COMMANDS.includes(command as never)) {
    return { where: "lima", reason: `${command} is destructive; the host refuses to execute it` };
  }
  if (stage === "annotate" && platform === "darwin") {
    return { where: "lima", reason: "it calls v1's annotate, which cannot run on macOS" };
  }
  return { where: "mac", reason: "nothing about this step needs the VM" };
}
