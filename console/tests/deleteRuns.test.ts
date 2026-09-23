/**
 * Deleting runs.
 *
 * This is the only destructive thing the console does, so the tests here are mostly about what
 * it refuses and what it records, not about the happy path. The containment tests matter most:
 * a bug in path handling here removes something that is not a run.
 */
import { describe, expect, it, beforeEach, afterEach } from "vitest";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  analyzeDeletion,
  deleteRuns,
  resolveDeletableRun,
  UnsafeDeletionError,
  DELETION_LOG,
} from "../src/data/deleteRuns.js";

/**
 * A throwaway repo root that looks enough like caruca_v2 for `repoPaths()` to accept it.
 *
 * `CARUCA_V2_ROOT` is what makes these tests safe: without it they would resolve to the real
 * checkout, and a mistake would delete real evidence.
 */
let root: string;
const originalRoot = process.env.CARUCA_V2_ROOT;

function makeRun(runId: string, files: Record<string, string> = {}) {
  const dir = join(root, "eval", "runs", runId);
  mkdirSync(dir, { recursive: true });
  for (const [name, body] of Object.entries(files)) writeFileSync(join(dir, name), body);
  return dir;
}

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "caruca-del-"));
  for (const dir of ["eval/runs", "eval/v1_runs", "eval/campaigns", "prompts", "src/caruca_v2/harness"]) {
    mkdirSync(join(root, dir), { recursive: true });
  }
  writeFileSync(join(root, "pyproject.toml"), "");
  process.env.CARUCA_V2_ROOT = root;
});

afterEach(() => {
  if (originalRoot === undefined) delete process.env.CARUCA_V2_ROOT;
  else process.env.CARUCA_V2_ROOT = originalRoot;
  rmSync(root, { recursive: true, force: true });
});

describe("what it refuses to touch", () => {
  it("refuses anything that is not a plain run id", () => {
    for (const bad of ["../../etc", "a/b", "..", "", "run id with spaces"]) {
      expect(() => resolveDeletableRun(bad)).toThrow(UnsafeDeletionError);
    }
  });

  it("refuses a run id that does not exist", () => {
    expect(() => resolveDeletableRun("2026-09-14T000000Z_nope_abcdef12")).toThrow(
      UnsafeDeletionError,
    );
  });

  it("refuses a symbolic link that points outside the run roots", () => {
    // The check is made on the resolved real path for exactly this case: a link inside
    // eval/runs pointing at something that is not a run.
    const outside = mkdtempSync(join(tmpdir(), "caruca-outside-"));
    writeFileSync(join(outside, "important.txt"), "do not delete me");
    symlinkSync(outside, join(root, "eval", "runs", "escape"));

    expect(() => resolveDeletableRun("escape")).toThrow(UnsafeDeletionError);
    expect(existsSync(join(outside, "important.txt"))).toBe(true);
    rmSync(outside, { recursive: true, force: true });
  });

  it("reports a bad id as a problem rather than throwing the whole deletion away", () => {
    makeRun("2026-09-14T120000Z_cat_aaaaaaaa");
    const analysis = analyzeDeletion(["2026-09-14T120000Z_cat_aaaaaaaa", "../escape"]);
    expect(analysis.runs).toHaveLength(1);
    expect(analysis.problems).toHaveLength(1);
    expect(analysis.problems[0]!.runId).toBe("../escape");
  });
});

describe("the impact report", () => {
  it("measures what would go", () => {
    makeRun("2026-09-14T120000Z_cat_aaaaaaaa", { "a.json": "12345", "b.json": "678" });
    const analysis = analyzeDeletion(["2026-09-14T120000Z_cat_aaaaaaaa"]);
    expect(analysis.totalFiles).toBe(2);
    expect(analysis.totalBytes).toBe(8);
    expect(analysis.runs[0]!.empty).toBe(false);
  });

  it("recognises a run that recorded nothing", () => {
    // The 28 empty directories are the safe case: nothing can depend on them.
    makeRun("2026-09-14T120000Z_rm_bbbbbbbb");
    const analysis = analyzeDeletion(["2026-09-14T120000Z_rm_bbbbbbbb"]);
    expect(analysis.runs[0]!.empty).toBe(true);
    expect(analysis.cited).toEqual([]);
  });

  it("names the campaign cell that depends on a run", () => {
    const runId = "2026-09-14T120000Z_cat_cccccccc";
    makeRun(runId, { "x.json": "{}" });
    mkdirSync(join(root, "eval", "campaigns", "p1_trace"), { recursive: true });
    writeFileSync(
      join(root, "eval", "campaigns", "p1_trace", "ledger.jsonl"),
      `${JSON.stringify({
        cell_key: "cat|openai/gpt-4o|0.0|0",
        campaign_id: "p1_trace",
        stage: "trace",
        command: "cat",
        model: "openai/gpt-4o",
        temperature: 0,
        sample: 0,
        attempts: 1,
        run_id: runId,
        status: "ok",
        cost_usd: 0.1,
        prompt_tokens: 1,
        completion_tokens: 1,
        score: { "core.micro.f1": 1 },
      })}\n`,
    );

    const analysis = analyzeDeletion([runId]);
    expect(analysis.cited).toHaveLength(1);
    expect(analysis.cited[0]!.dependencies[0]).toMatchObject({
      kind: "campaign",
      id: "p1_trace",
    });
  });

  it("names the finding that rests on a run", () => {
    const runId = "2026-09-14T120000Z_cat_dddddddd";
    makeRun(runId, { "x.json": "{}" });
    const findings = join(root, "ai_docs", "analysis", "findings");
    mkdirSync(findings, { recursive: true });
    writeFileSync(
      join(findings, "some-finding.md"),
      `---
id: some-finding
claim: v2 reproduces v1 at stage 3.
status: confirmed
created: "2026-09-22"
evidence:
  - label: core recall
    value: 0.606
    denominator: v1's projected filesystem interactions
    metric: core.micro.recall
    method: trace_recovery_diff
    run_ids:
      - ${runId}
---

Body.
`,
    );

    const analysis = analyzeDeletion([runId]);
    expect(analysis.cited[0]!.dependencies[0]).toMatchObject({
      kind: "finding",
      id: "some-finding",
    });
    // The figure that would become un-recheckable is named, not just the file.
    expect(analysis.cited[0]!.dependencies[0]!.detail).toContain("0.606");
  });
});

describe("deleting", () => {
  it("removes the directory and logs what went", () => {
    const runId = "2026-09-14T120000Z_cat_eeeeeeee";
    const dir = makeRun(runId, { "a.json": "{}" });

    const result = deleteRuns([runId], { reason: "duplicate of an earlier run" });

    expect(existsSync(dir)).toBe(false);
    expect(result.deleted).toEqual([runId]);
    expect(result.failed).toEqual([]);

    const logged = JSON.parse(readFileSync(join(root, "eval", DELETION_LOG), "utf8").trim());
    expect(logged.run_ids).toEqual([runId]);
    expect(logged.reason).toBe("duplicate of an earlier run");
    expect(logged.files_removed).toBe(1);
    // The log says the files are still in git, because they are.
    expect(logged.note).toContain("git");
  });

  it("records what depended on a run, since that is what cannot be reconstructed after", () => {
    const runId = "2026-09-14T120000Z_cat_ffffffff";
    makeRun(runId, { "a.json": "{}" });
    mkdirSync(join(root, "eval", "campaigns", "p1_trace"), { recursive: true });
    writeFileSync(
      join(root, "eval", "campaigns", "p1_trace", "ledger.jsonl"),
      `${JSON.stringify({
        cell_key: "cat|m|0.0|0",
        campaign_id: "p1_trace",
        stage: "trace",
        command: "cat",
        model: "m",
        temperature: 0,
        sample: 0,
        attempts: 1,
        run_id: runId,
        status: "ok",
      })}\n`,
    );

    const result = deleteRuns([runId]);
    expect(result.citedAtDeletion).toHaveLength(1);
    const logged = JSON.parse(readFileSync(join(root, "eval", DELETION_LOG), "utf8").trim());
    expect(logged.depended_on_by[0].id).toBe("p1_trace");
  });

  it("deletes several at once and leaves the others alone", () => {
    makeRun("2026-09-14T120000Z_a_11111111", { "x": "1" });
    makeRun("2026-09-14T120000Z_b_22222222", { "x": "1" });
    const keep = makeRun("2026-09-14T120000Z_c_33333333", { "x": "1" });

    const result = deleteRuns(["2026-09-14T120000Z_a_11111111", "2026-09-14T120000Z_b_22222222"]);
    expect(result.deleted).toHaveLength(2);
    expect(existsSync(keep)).toBe(true);
  });

  it("appends to the log rather than replacing it", () => {
    makeRun("2026-09-14T120000Z_a_44444444", { "x": "1" });
    makeRun("2026-09-14T120000Z_b_55555555", { "x": "1" });
    deleteRuns(["2026-09-14T120000Z_a_44444444"]);
    deleteRuns(["2026-09-14T120000Z_b_55555555"]);
    const lines = readFileSync(join(root, "eval", DELETION_LOG), "utf8").trim().split("\n");
    expect(lines).toHaveLength(2);
  });
});
