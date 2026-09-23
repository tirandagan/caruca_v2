/**
 * Deleting runs, and knowing what a deletion costs before making it.
 *
 * This is the only destructive operation in the console, and it is destructive in a way that
 * is easy to underestimate, so three things are built in rather than left to the person
 * clicking:
 *
 *   1. **An impact report first.** A run can be cited by a scored campaign cell and by a
 *      written-up finding. Deleting it does not change those documents - it makes the numbers
 *      in them permanently un-recheckable, which is a silent failure that only shows up much
 *      later. `analyzeDeletion` says exactly what depends on each run before anything happens.
 *      Tiran's call on 2026-09-22: warn clearly, then allow it.
 *   2. **A containment check.** Nothing outside `eval/runs/` and `eval/v1_runs/` can be
 *      removed, and the check is made on the resolved real path, so a symbolic link cannot
 *      point the deletion somewhere else.
 *   3. **A log.** Every deletion appends a line to `eval/deleted_runs.jsonl` recording what
 *      went, when, and what depended on it at the time. In a research record an unexplained
 *      gap is worse than a documented removal: a year from now, "why is there no run for
 *      `tee`?" needs an answer that is not a shrug.
 *
 * **What this does not do, and cannot.** Run data has been committed since `eedd91a` - 769
 * files under `eval/runs` are in git. Deleting them from disk leaves every one of them in the
 * repository's history. That makes an accidental deletion recoverable, and it means this is
 * not a way to make something go away.
 */
import { appendFileSync, existsSync, readdirSync, realpathSync, rmSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { join, resolve, sep } from "node:path";
import { repoPaths } from "./paths.js";
import { listCampaigns, loadLedger } from "./campaigns.js";
import { listFindings } from "./findings.js";
import { loadManifest } from "./runs.js";

export class UnsafeDeletionError extends Error {}

export const DELETION_LOG = "deleted_runs.jsonl";

/** A run id is a directory name and nothing else. No separators, no traversal. */
const RUN_ID = /^[A-Za-z0-9_.:-]+$/;

/**
 * Resolve a run id to a directory that is provably inside one of the run roots.
 *
 * The check is on the *resolved* path, after following links, and it compares against the
 * resolved root with a trailing separator - so neither `..` nor a symlink nor a prefix
 * coincidence like `eval/runs-backup` can get past it.
 */
export function resolveDeletableRun(runId: string, roots?: string[]): string {
  if (!RUN_ID.test(runId)) {
    throw new UnsafeDeletionError(`"${runId}" is not a run id.`);
  }

  const paths = repoPaths();
  for (const root of roots ?? [paths.v2Runs, paths.v1Runs]) {
    if (!existsSync(root)) continue;
    const candidate = join(root, runId);
    if (!existsSync(candidate)) continue;

    const realRoot = realpathSync(root);
    const realCandidate = realpathSync(candidate);
    if (realCandidate === realRoot || !realCandidate.startsWith(realRoot + sep)) {
      throw new UnsafeDeletionError(
        `${runId} resolves to ${realCandidate}, which is outside ${realRoot}.`,
      );
    }
    if (!statSync(realCandidate).isDirectory()) {
      throw new UnsafeDeletionError(`${runId} is not a directory.`);
    }
    return realCandidate;
  }

  throw new UnsafeDeletionError(`No run directory named ${runId} under the run roots.`);
}

export interface RunDependency {
  readonly kind: "campaign" | "finding";
  /** The campaign id, or the finding's id. */
  readonly id: string;
  /** What in it refers to this run. */
  readonly detail: string;
}

export interface RunImpact {
  readonly runId: string;
  readonly dir: string;
  readonly files: number;
  readonly bytes: number;
  /** True for a run that died before recording anything. Nothing can depend on these. */
  readonly empty: boolean;
  /** A one-line description, where the run recorded enough to have one. */
  readonly describes: string | null;
  /** Rows in the metrics database that would go with it. */
  readonly metricsRows: number;
  readonly dependencies: RunDependency[];
}

export interface DeletionAnalysis {
  readonly runs: RunImpact[];
  readonly totalFiles: number;
  readonly totalBytes: number;
  readonly totalMetricsRows: number;
  /** Runs that something depends on. Deleting these makes a published number uncheckable. */
  readonly cited: RunImpact[];
  readonly problems: { runId: string; reason: string }[];
}

function directorySize(dir: string): { files: number; bytes: number } {
  let files = 0;
  let bytes = 0;
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    const stats = statSync(path);
    if (stats.isDirectory()) {
      const inner = directorySize(path);
      files += inner.files;
      bytes += inner.bytes;
    } else {
      files += 1;
      bytes += stats.size;
    }
  }
  return { files, bytes };
}

/** Every campaign cell and finding that names one of these runs. */
function findDependencies(runIds: Set<string>): Map<string, RunDependency[]> {
  const found = new Map<string, RunDependency[]>();
  const add = (runId: string, dependency: RunDependency) => {
    const list = found.get(runId);
    if (list) list.push(dependency);
    else found.set(runId, [dependency]);
  };

  const paths = repoPaths();
  for (const campaign of listCampaigns()) {
    let rows;
    try {
      rows = loadLedger(join(paths.campaigns, campaign, "ledger.jsonl")).rows;
    } catch {
      continue;
    }
    for (const row of rows) {
      if (row.run_id && runIds.has(row.run_id)) {
        add(row.run_id, {
          kind: "campaign",
          id: campaign,
          detail: `scored cell ${row.cell_key}`,
        });
      }
    }
  }

  for (const finding of listFindings().findings) {
    for (const evidence of finding.frontmatter.evidence) {
      for (const runId of evidence.run_ids) {
        if (runIds.has(runId)) {
          add(runId, {
            kind: "finding",
            id: finding.frontmatter.id,
            detail: `evidence for "${evidence.label}" = ${evidence.value}`,
          });
        }
      }
    }
  }

  return found;
}

function metricsRowCount(runIds: string[]): Map<string, number> {
  const counts = new Map<string, number>();
  const paths = repoPaths();
  if (!existsSync(paths.metricsDb) || runIds.length === 0) return counts;

  const require = createRequire(import.meta.url);
  const { DatabaseSync } = require("node:sqlite") as {
    DatabaseSync: new (
      path: string,
      options?: { readOnly?: boolean },
    ) => {
      prepare(sql: string): { all(...params: unknown[]): unknown[] };
      close(): void;
    };
  };

  const db = new DatabaseSync(paths.metricsDb, { readOnly: true });
  try {
    const placeholders = runIds.map(() => "?").join(",");
    const rows = db
      .prepare(
        `SELECT run_id, COUNT(*) AS n FROM runs WHERE run_id IN (${placeholders}) GROUP BY run_id`,
      )
      .all(...runIds) as { run_id: string; n: number }[];
    for (const row of rows) counts.set(row.run_id, row.n);
  } finally {
    db.close();
  }
  return counts;
}

/** What deleting these runs would cost. Reads only; changes nothing. */
export function analyzeDeletion(runIds: string[]): DeletionAnalysis {
  const problems: { runId: string; reason: string }[] = [];
  const resolved: { runId: string; dir: string }[] = [];

  for (const runId of runIds) {
    try {
      resolved.push({ runId, dir: resolveDeletableRun(runId) });
    } catch (cause) {
      problems.push({ runId, reason: (cause as Error).message });
    }
  }

  const dependencies = findDependencies(new Set(resolved.map((entry) => entry.runId)));
  const metricsRows = metricsRowCount(resolved.map((entry) => entry.runId));

  const runs: RunImpact[] = resolved.map(({ runId, dir }) => {
    const { files, bytes } = directorySize(dir);
    let describes: string | null = null;
    if (files > 0) {
      try {
        const manifest = loadManifest(dir);
        describes = `${manifest.stage} · ${manifest.command} · ${manifest.model_requested}`;
      } catch {
        describes = null;
      }
    }
    return {
      runId,
      dir,
      files,
      bytes,
      empty: files === 0,
      describes,
      metricsRows: metricsRows.get(runId) ?? 0,
      dependencies: dependencies.get(runId) ?? [],
    };
  });

  return {
    runs,
    totalFiles: runs.reduce((sum, run) => sum + run.files, 0),
    totalBytes: runs.reduce((sum, run) => sum + run.bytes, 0),
    totalMetricsRows: runs.reduce((sum, run) => sum + run.metricsRows, 0),
    cited: runs.filter((run) => run.dependencies.length > 0),
    problems,
  };
}

/**
 * Remove the metrics-database rows for these runs.
 *
 * The one place the console opens the database for writing. Worth knowing: the database is
 * regenerated from the telemetry files by `caruca-v2 metrics rebuild`, so deleting rows alone
 * accomplishes nothing - a later rebuild restores them. It is only meaningful together with
 * the files, or for a run whose files are already gone and whose row is the last trace left.
 */
function deleteMetricsRows(runIds: string[]): number {
  const paths = repoPaths();
  if (!existsSync(paths.metricsDb) || runIds.length === 0) return 0;

  const require = createRequire(import.meta.url);
  const { DatabaseSync } = require("node:sqlite") as {
    DatabaseSync: new (path: string) => {
      prepare(sql: string): { run(...params: unknown[]): { changes: number | bigint } };
      close(): void;
    };
  };

  const db = new DatabaseSync(paths.metricsDb);
  try {
    const placeholders = runIds.map(() => "?").join(",");
    const result = db.prepare(`DELETE FROM runs WHERE run_id IN (${placeholders})`).run(...runIds);
    return Number(result.changes);
  } finally {
    db.close();
  }
}

export interface DeletionResult {
  readonly deleted: string[];
  readonly failed: { runId: string; reason: string }[];
  readonly filesRemoved: number;
  readonly bytesRemoved: number;
  readonly metricsRowsRemoved: number;
  readonly logPath: string;
  /** What depended on the deleted runs, recorded at the moment of deletion. */
  readonly citedAtDeletion: RunDependency[];
}

/**
 * Delete runs: their directories, and their rows in the metrics database.
 *
 * The analysis is re-run here rather than trusted from the caller, so what gets logged is what
 * was actually true at the moment of deletion and not what a page rendered some minutes ago.
 */
export function deleteRuns(runIds: string[], options: { reason?: string } = {}): DeletionResult {
  const analysis = analyzeDeletion(runIds);
  const deleted: string[] = [];
  const failed = [...analysis.problems];
  let filesRemoved = 0;
  let bytesRemoved = 0;

  for (const run of analysis.runs) {
    try {
      // Re-resolve immediately before removing: the containment check must hold now, not when
      // the impact report was built.
      const dir = resolveDeletableRun(run.runId);
      rmSync(dir, { recursive: true, force: false });
      deleted.push(run.runId);
      filesRemoved += run.files;
      bytesRemoved += run.bytes;
    } catch (cause) {
      failed.push({ runId: run.runId, reason: (cause as Error).message });
    }
  }

  const metricsRowsRemoved = deleteMetricsRows(deleted);

  const paths = repoPaths();
  const logPath = join(resolve(paths.root, "eval"), DELETION_LOG);
  const citedAtDeletion = analysis.runs
    .filter((run) => deleted.includes(run.runId))
    .flatMap((run) => run.dependencies);

  appendFileSync(
    logPath,
    `${JSON.stringify({
      deleted_at: new Date().toISOString(),
      run_ids: deleted,
      reason: options.reason ?? null,
      files_removed: filesRemoved,
      bytes_removed: bytesRemoved,
      metrics_rows_removed: metricsRowsRemoved,
      // Recorded because it is the part that cannot be reconstructed afterwards: once the run
      // is gone, nothing says which figures used to rest on it.
      depended_on_by: citedAtDeletion,
      note: "Run data is committed to git; these files remain in the repository's history.",
    })}\n`,
  );

  return {
    deleted,
    failed,
    filesRemoved,
    bytesRemoved,
    metricsRowsRemoved,
    logPath,
    citedAtDeletion,
  };
}
