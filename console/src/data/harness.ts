/**
 * Calling the Python harness.
 *
 * Task 010 §6.4 is explicit that the console must call the same modules `scripts/parity_diff.py`
 * uses, "so the console and the script cannot disagree". So nothing here recomputes a score.
 * The console runs `caruca-v2` and reads what it prints.
 *
 * **Processes are started from argument lists, never a shell string** (§7). Nothing in this
 * file interpolates a value into a command; a campaign id or command name arrives as its own
 * element of `argv`, so a stray quote or space cannot become a second command.
 *
 * `--json` writes the report to stdout and its progress chatter to stderr, so the two are read
 * separately rather than by hunting for the first `{`.
 */
import { spawn } from "node:child_process";
import { join } from "node:path";
import { repoPaths } from "./paths.js";

export class HarnessError extends Error {
  constructor(
    message: string,
    readonly argv: readonly string[],
    readonly exitCode: number | null,
    readonly stderr: string,
  ) {
    super(message);
  }
}

export interface HarnessResult {
  readonly stdout: string;
  readonly stderr: string;
  readonly exitCode: number;
  /** Exactly what was run, so any screen can show it and anyone can repeat it. */
  readonly argv: readonly string[];
  readonly seconds: number;
}

/** Where `caruca-v2` lives. The console never uses a `caruca-v2` found on PATH. */
export function carucaV2Bin(root = repoPaths().root): string {
  return join(root, ".venv", "bin", "caruca-v2");
}

const DEFAULT_TIMEOUT_MS = 120_000;

/**
 * Run `caruca-v2` with the given arguments and return what it printed.
 *
 * No shell, no `cwd` guesswork: it runs from the repo root, which is where every relative path
 * the harness prints is relative to.
 */
export function runCarucaV2(
  args: readonly string[],
  options: { timeoutMs?: number; root?: string } = {},
): Promise<HarnessResult> {
  const root = options.root ?? repoPaths().root;
  const argv = [carucaV2Bin(root), ...args];
  const startedAt = Date.now();

  return new Promise((resolve, reject) => {
    const child = spawn(argv[0]!, argv.slice(1), {
      cwd: root,
      // `--plain` is passed by callers; this also keeps colour out of anything that checks TTY.
      env: { ...process.env, NO_COLOR: "1" },
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    let settled = false;

    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill("SIGTERM");
      reject(
        new HarnessError(
          `${argv.join(" ")} did not finish within ${options.timeoutMs ?? DEFAULT_TIMEOUT_MS}ms.`,
          argv,
          null,
          stderr,
        ),
      );
    }, options.timeoutMs ?? DEFAULT_TIMEOUT_MS);

    child.stdout.on("data", (chunk: Buffer) => (stdout += chunk.toString()));
    child.stderr.on("data", (chunk: Buffer) => (stderr += chunk.toString()));

    child.on("error", (cause) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      reject(new HarnessError(`Could not run ${argv[0]}: ${cause.message}`, argv, null, stderr));
    });

    child.on("close", (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (code !== 0) {
        reject(
          new HarnessError(
            `${argv.join(" ")} exited with ${code}.`,
            argv,
            code,
            stderr.trim() || stdout.trim(),
          ),
        );
        return;
      }
      resolve({
        stdout,
        stderr,
        exitCode: code,
        argv,
        seconds: (Date.now() - startedAt) / 1000,
      });
    });
  });
}

/** The reference a rescore is measured against. Bare means each stage's own default. */
export type RescoreReference = "stage-default" | "v1-specs" | "ground-truth";

export interface ReportArms {
  readonly arm: string;
  readonly model: string;
  readonly prompt_variant: string;
  readonly temperature: number;
  readonly cells: number;
  readonly ok: number;
  readonly failed: number;
  readonly errored: number;
  readonly first_pass_validity: number;
  readonly scored_cells: number;
  readonly cost_usd: number;
  readonly prompt_tokens: number;
  readonly completion_tokens: number;
  readonly cost_per_scored_cell: number;
  /** Each metric the stage reports, as a distribution. Keys vary by stage. */
  readonly [metric: string]: unknown;
}

/**
 * One dimension's v1-versus-v2 line, as `report.py` builds it.
 *
 * This is the roll-up §5 asks for, and it is taken from the harness rather than assembled
 * here - including `percent_change`, which is null wherever a percent change would not be
 * valid. The console shows the reason instead of computing one anyway.
 */
export interface ComparisonRecord {
  readonly campaign_id: string;
  readonly arm: string;
  readonly dimension: string;
  readonly comparison_system: string;
  readonly profile: string;
  readonly method: string;
  readonly instrument: string;
  /** What the rate is counted over. Always shown beside the number. */
  readonly denominator: string;
  readonly v1_value: number | null;
  readonly v1_value_kind: string;
  readonly v1_value_source: string | null;
  readonly v1_value_note: string | null;
  readonly v2_value: number | null;
  readonly match_rate: number | null;
  readonly n_samples: number;
  readonly exact_match: boolean | null;
  /** Null where a percent change is not valid. The reason is in `v1_value_note`. */
  readonly percent_change: number | null;
  readonly caruca_v1_commit: string;
  readonly evidence_refs: string[];
}

/**
 * The existing report's consistency figure, per arm.
 *
 * Kept so the console can show it next to the per-metric spread it computes itself. The
 * difference is the point: this one measures the stage's headline metric only, so it reports
 * stage 1 as perfectly consistent while `tac`'s exact-argument rate moves by 0.200.
 */
export interface HeadlineConsistency {
  readonly commands_sampled_more_than_once: number;
  readonly identical_across_samples: number;
  readonly identical_rate: number;
  readonly mean_spread: number;
  readonly max_spread: number;
}

export interface CampaignReport {
  readonly campaign_id: string;
  readonly cells_recorded: number;
  /** Whether the numbers came from the ledger as recorded, or were re-derived today. */
  readonly scores_from: string;
  readonly arms: ReportArms[];
  readonly consistency: Record<string, HeadlineConsistency>;
  readonly comparison_records: ComparisonRecord[];
  /** The Markdown table the harness itself prints, reused rather than rebuilt. */
  readonly table: string;
}

export interface LoadedReport {
  readonly report: CampaignReport;
  readonly argv: readonly string[];
  readonly seconds: number;
}

/**
 * Aggregate a campaign by running `caruca-v2 report --json`.
 *
 * With `rescore`, every score is re-derived from the saved run artifacts using today's scorer
 * instead of what the ledger recorded at run time - which is how a scorer fix is applied
 * without paying for the campaign again.
 */
export async function loadCampaignReport(
  campaignId: string,
  options: {
    rescore?: RescoreReference | true;
    referenceTraces?: string;
    ledgerRoot?: string;
    timeoutMs?: number;
  } = {},
): Promise<LoadedReport> {
  const args = ["report", campaignId, "--json", "--plain"];
  if (options.rescore) {
    args.push("--rescore");
    if (options.rescore !== true) args.push(options.rescore);
  }
  if (options.referenceTraces) args.push("--reference-traces", options.referenceTraces);
  if (options.ledgerRoot) args.push("--ledger-root", options.ledgerRoot);

  const result = await runCarucaV2(args, { timeoutMs: options.timeoutMs ?? 300_000 });

  let parsed: unknown;
  try {
    parsed = JSON.parse(result.stdout);
  } catch (cause) {
    throw new HarnessError(
      `report ${campaignId} did not print JSON: ${(cause as Error).message}`,
      result.argv,
      result.exitCode,
      result.stderr,
    );
  }

  return { report: parsed as CampaignReport, argv: result.argv, seconds: result.seconds };
}

/** Run the scorer's own self-test. Free, and the quickest check that the harness is sound. */
export async function scoreSelfTest(): Promise<HarnessResult> {
  return runCarucaV2(["score", "--self-test", "--plain"]);
}
