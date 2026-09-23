/**
 * Reading `eval/metrics.db`, the per-turn index over every model call.
 *
 * Uses Node's built-in `node:sqlite` rather than a native package. That was forced -
 * `better-sqlite3` does not build against the installed Node 26 - but it is the better answer
 * anyway: the console gains no compiled dependency, so a Node upgrade cannot break the ability
 * to read the evidence.
 *
 * **Always opened read-only.** The database is a rebuildable cache (`caruca-v2 metrics
 * rebuild` recreates it from the run directories), but it is also the fastest way to get every
 * number wrong at once. Rebuilding is the CLI's job; the console only reads.
 *
 * One row per model turn, so a five-turn run contributes five rows. Any per-run figure must
 * aggregate, and the primary key is (run_id, turn).
 */
import { createRequire } from "node:module";
import { repoPaths } from "./paths.js";

/**
 * `node:sqlite` is resolved at runtime rather than imported statically.
 *
 * It is a real Node builtin (22.5+), but it is newer than the builtin list Vite ships, so a
 * static `import ... from "node:sqlite"` gets rewritten to a bare `sqlite` and fails to
 * resolve under vitest. Going through `createRequire` leaves nothing for a bundler to rewrite.
 * Revert to a static import once Vite knows the module.
 */
interface SqliteModule {
  DatabaseSync: new (path: string, options?: { readOnly?: boolean }) => DatabaseHandle;
}
interface DatabaseHandle {
  prepare(sql: string): { all(...params: unknown[]): unknown[]; get(...params: unknown[]): unknown };
  close(): void;
}

const { DatabaseSync } = createRequire(import.meta.url)("node:sqlite") as SqliteModule;

export interface MetricsRow {
  readonly run_id: string;
  readonly turn: number;
  readonly config_index: number | null;
  readonly timestamp: string;
  readonly command: string;
  readonly component: string;
  readonly condition: string;
  readonly stage: string;
  readonly model_id: string;
  readonly prompt_tokens: number;
  readonly completion_tokens: number;
  readonly cost_usd: number;
  readonly wall_clock_seconds: number;
  readonly seed: number | null;
  readonly decoding_params: string;
  readonly prompt_hash: string;
  readonly validation_passed: number | null;
  readonly run_dir: string;
}

export interface MetricsFilter {
  readonly stage?: string;
  readonly command?: string;
  readonly model?: string;
  readonly runId?: string;
}

function open(dbPath: string): DatabaseHandle {
  return new DatabaseSync(dbPath, { readOnly: true });
}

/** Turn-level rows, filtered. Ordered so a run's turns come out in the order they happened. */
export function queryTurns(filter: MetricsFilter = {}, dbPath = repoPaths().metricsDb): MetricsRow[] {
  const where: string[] = [];
  const params: (string | number)[] = [];
  if (filter.stage) (where.push("stage = ?"), params.push(filter.stage));
  if (filter.command) (where.push("command = ?"), params.push(filter.command));
  if (filter.model) (where.push("model_id = ?"), params.push(filter.model));
  if (filter.runId) (where.push("run_id = ?"), params.push(filter.runId));

  const sql =
    "SELECT * FROM runs" +
    (where.length ? ` WHERE ${where.join(" AND ")}` : "") +
    " ORDER BY run_id, turn";

  const db = open(dbPath);
  try {
    return db.prepare(sql).all(...params) as unknown as MetricsRow[];
  } finally {
    db.close();
  }
}

export interface RunTotals {
  readonly run_id: string;
  readonly stage: string;
  readonly command: string;
  readonly model_id: string;
  readonly turns: number;
  readonly prompt_tokens: number;
  readonly completion_tokens: number;
  readonly cost_usd: number;
  readonly wall_clock_seconds: number;
}

/**
 * Per-run totals, summed from the turn rows.
 *
 * `wall_clock_seconds` is summed, matching how each stage builds its manifest (it sums each
 * turn's elapsed time). That is time spent in model calls, not the run's elapsed wall clock -
 * the two differ by whatever the run spent executing commands, and stage 3 spends a lot there.
 * Do not present this as "how long the run took".
 */
export function runTotals(filter: MetricsFilter = {}, dbPath = repoPaths().metricsDb): RunTotals[] {
  const rows = queryTurns(filter, dbPath);
  const byRun = new Map<string, RunTotals & { turns: number }>();
  for (const row of rows) {
    const existing = byRun.get(row.run_id);
    if (!existing) {
      byRun.set(row.run_id, {
        run_id: row.run_id,
        stage: row.stage,
        command: row.command,
        model_id: row.model_id,
        turns: 1,
        prompt_tokens: row.prompt_tokens,
        completion_tokens: row.completion_tokens,
        cost_usd: row.cost_usd,
        wall_clock_seconds: row.wall_clock_seconds,
      });
      continue;
    }
    byRun.set(row.run_id, {
      ...existing,
      turns: existing.turns + 1,
      prompt_tokens: existing.prompt_tokens + row.prompt_tokens,
      completion_tokens: existing.completion_tokens + row.completion_tokens,
      cost_usd: existing.cost_usd + row.cost_usd,
      wall_clock_seconds: existing.wall_clock_seconds + row.wall_clock_seconds,
    });
  }
  return [...byRun.values()];
}

/** Run ids present in the database. Used to find runs the database does not know about. */
export function indexedRunIds(dbPath = repoPaths().metricsDb): Set<string> {
  const db = open(dbPath);
  try {
    const rows = db.prepare("SELECT DISTINCT run_id FROM runs").all() as unknown as {
      run_id: string;
    }[];
    return new Set(rows.map((row) => row.run_id));
  } finally {
    db.close();
  }
}
