/**
 * The metrics database, and how it disagrees with the run directories.
 *
 * These numbers are pinned deliberately. The console's Runs screen has three possible
 * denominators - directories on disk, manifests, and rows in the database - and they are all
 * different. Any screen that mixes them up reports a wrong count, so the difference is
 * measured here rather than discovered later in a figure.
 */
import { describe, expect, it } from "vitest";
import { indexedRunIds, queryTurns, runTotals } from "../src/data/metricsDb.js";
import { listRuns } from "../src/data/runs.js";

describe("the metrics database", () => {
  it("holds one row per model turn", () => {
    // A count rather than a fixed total: making a real run adds rows, and a test that has to
    // be edited after every run stops being read. What matters is that every row is a turn of
    // a run the database also knows.
    const rows = queryTurns();
    expect(rows.length).toBeGreaterThanOrEqual(511);
    expect(new Set(rows.map((row) => `${row.run_id}|${row.turn}`)).size).toBe(rows.length);
  });

  it("knows runs whose directories are gone, all from one day", () => {
    const indexed = indexedRunIds();
    expect(indexed.size).toBeGreaterThanOrEqual(160);

    const onDisk = new Set(listRuns().runs.map((run) => run.runId));
    const orphaned = [...indexed].filter((id) => !onDisk.has(id));
    // 2026-09-08 runs whose artifacts are gone. Their turn-level numbers survive, but their
    // prompts, responses and outputs do not - so Inspect can show nothing for them and must
    // say why rather than render an empty page.
    expect(orphaned.length).toBeGreaterThanOrEqual(25);
    expect(orphaned.every((id) => id.startsWith("2026-09-08"))).toBe(true);
  });

  it("indexes every run that has a manifest", () => {
    // The gap runs one way only. A manifest missing from the database would mean the database
    // is stale and `metrics rebuild` is due; there are none.
    const indexed = indexedRunIds();
    const missing = listRuns().runs.filter((run) => !indexed.has(run.runId));
    expect(missing).toEqual([]);
  });

  it("sums a run's turns back to what its manifest reports", () => {
    const runId = "2026-09-14T163935Z_cat_a3ea2a72";
    const [totals] = runTotals({ runId });
    expect(totals?.turns).toBe(10);
    expect(totals?.cost_usd).toBeCloseTo(0.0353, 4);
  });

  it("filters by stage and command", () => {
    const rows = queryTurns({ stage: "syntax_spec", command: "cat" });
    expect(rows.length).toBeGreaterThan(0);
    expect(rows.every((row) => row.stage === "syntax_spec" && row.command === "cat")).toBe(true);
  });
});
