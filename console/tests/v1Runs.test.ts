/**
 * v1's run records.
 *
 * No v1 run exists yet - the console creates the first one in Phase 5 - so these tests work
 * against records written into a temporary directory. What they pin is the shape: the things
 * decision 7 requires to be written down, and the two places where absent must not become zero.
 */
import { describe, expect, it } from "vitest";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  listV1Runs,
  loadV1Run,
  v1RunManifestSchema,
  writeV1Manifest,
  V1RunUnreadableError,
} from "../src/data/v1Runs.js";
import { v1ProtectedOutputs } from "../src/data/paths.js";

/** The parity study's stage-3 form: v1's trace, inside the Lima VM. */
function traceRecord(overrides: Record<string, unknown> = {}) {
  return v1RunManifestSchema.parse({
    run_id: "2026-09-22T120000Z_cat_v1trace",
    subcommand: "trace",
    command: "cat",
    argv: [
      "limactl",
      "shell",
      "caruca",
      "--",
      "/home/tirandagan/caruca-venv/bin/caruca",
      "trace",
      "cat",
      "--max-count",
      "1",
      "--output",
      "/Users/tirandagan/dev/stevens/caruca_v2/eval/v1_runs/2026-09-22T120000Z_cat_v1trace/cat.json",
    ],
    cwd: "/Users/tirandagan/dev/stevens/caruca/caruca",
    venv: "~/caruca-venv",
    where: "lima",
    lima_instance: "caruca",
    v1_commit: "d8032407346aadc135b14c043618c8c1d4f4e0cf",
    env_var_names: ["PATH", "HOME"],
    started_at: "2026-09-22T12:00:00Z",
    machine: "mac",
    terminal_size: { cols: 117, rows: 30 },
    ...overrides,
  });
}

describe("the v1 run record", () => {
  it("round-trips, keeping the argument list exactly as spawned", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-v1run-"));
    const runDir = join(dir, "2026-09-22T120000Z_cat_v1trace");
    writeV1Manifest(runDir, traceRecord());

    const loaded = loadV1Run(runDir);
    expect(loaded.manifest.where).toBe("lima");
    expect(loaded.manifest.lima_instance).toBe("caruca");
    // Unlike a v2 run, this was captured rather than rebuilt - so it is shown without the
    // "reconstructed" label.
    expect(loaded.display).toContain("limactl shell caruca --");
    expect(loaded.display).toContain("--max-count 1");
  });

  it("records what v1 does not measure as absent, never as zero", () => {
    // Until task 005, v1 records no per-step timing and no tokens for its LLM step. A screen
    // rendering these as 0 would claim v1's LLM step is free, which is exactly the gap the
    // project is trying to close.
    const record = traceRecord();
    expect(record.per_step_seconds).toBeNull();
    expect(record.llm_prompt_tokens).toBeNull();
    expect(record.llm_cost_usd).toBeNull();
  });

  it("keeps v1's output inside the run's own folder, never v1's checkout", () => {
    // Decision 7. v1's own outputs/ is gitignored in v1, so anything overwritten is gone.
    const record = traceRecord();
    const outputArg = record.argv[record.argv.indexOf("--output") + 1]!;
    expect(outputArg).toContain("/eval/v1_runs/");
    expect(outputArg.startsWith(v1ProtectedOutputs())).toBe(false);
  });

  it("notes when another run was going at the same time", () => {
    // Wall-clock from an overlapping run is flagged and kept out of timing comparisons (§6.3).
    const record = traceRecord({ concurrent_with: ["2026-09-22T120000Z_cat_9f3a11bc"] });
    expect(record.concurrent_with).toHaveLength(1);
  });

  it("records the terminal size, because v1's progress bar is sized to it", () => {
    expect(traceRecord().terminal_size.cols).toBe(117);
  });

  it("records that the annotate-in-VM form used a shell, rather than hiding it", () => {
    const record = traceRecord({
      subcommand: "annotate",
      format: "pash",
      used_shell: true,
      argv: ["limactl", "shell", "caruca", "--", "sh", "-lc", "~/caruca-venv/bin/caruca annotate pash cat --input /x/cat.json"],
    });
    expect(record.used_shell).toBe(true);
  });

  it("refuses a record that is missing a required field", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-v1run-"));
    const runDir = join(dir, "broken");
    expect(() => writeV1Manifest(runDir, { run_id: "x" } as never)).toThrow();
  });

  it("reports an unreadable record instead of dropping it from the listing", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-v1run-"));
    writeV1Manifest(join(dir, "good"), traceRecord());
    expect(listV1Runs(dir).runs).toHaveLength(1);
    expect(() => loadV1Run(join(dir, "absent"))).toThrow(V1RunUnreadableError);
  });

  it("is empty, not an error, before the first v1 run exists", () => {
    expect(listV1Runs(join(tmpdir(), "definitely-not-here"))).toEqual({
      runs: [],
      unreadable: [],
    });
  });
});
