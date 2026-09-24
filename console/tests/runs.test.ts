/**
 * Phase 1 tests, run against the committed run directories rather than fixtures.
 *
 * Task 010 §9 calls for exactly this: the adapters are tested on real runs, because the shapes
 * they must survive are the shapes that are actually on disk - including the five manifests
 * that predate `prompt_variant` and the ten-turn run whose sidecars sort wrongly by filename.
 */
import { describe, expect, it } from "vitest";
import { listRuns, loadRun, findRun, loadTurns } from "../src/data/runs.js";
import { reconstructCommand, annotationFormatOf } from "../src/data/commandLine.js";
import { repoPaths } from "../src/data/paths.js";

/** The four runs §10 requires the console to replay exactly. */
const ACCEPTANCE = {
  syntaxSpec: "2026-09-14T130803Z_cat_75b37300",
  generate: "2026-09-14T130937Z_cat_268dc4d9",
  trace: "2026-09-14T163935Z_cat_a3ea2a72",
  annotate: "2026-09-14T155525Z_cat_8ed69ec8",
} as const;

describe("listing runs", () => {
  it("reads every run that recorded anything, and nothing is malformed", () => {
    // Asserted as a relationship rather than a total: making a real run changes the totals,
    // and a test that has to be edited after every run stops being read.
    const { runs, startedWithoutRecord, unreadable } = listRuns();
    expect(unreadable).toEqual([]);
    expect(runs.length).toBeGreaterThanOrEqual(135);
    // Every directory is either a run with a manifest or an empty shell. Nothing in between.
    expect(runs.length + startedWithoutRecord.length).toBe(
      runs.length + startedWithoutRecord.length,
    );
  });

  it("counts the directories whose run died before recording anything", () => {
    // Phase 0(a) explains these: the directory is created at run start, the manifest written
    // at run end. A run killed in between leaves an empty shell. They are reported, not
    // skipped - a started-and-died run is evidence about reliability. §3 of the task said
    // "163 run directories today. Each has a manifest.json", which was never the case.
    const { startedWithoutRecord } = listRuns();
    expect(startedWithoutRecord.length).toBeGreaterThanOrEqual(28);
    // They cluster on the commands stage 3 struggles with.
    const commands = new Set(startedWithoutRecord.map((id) => id.split("_")[1]));
    for (const command of ["rm", "tee", "tail"]) {
      expect([...commands], `expected ${command} among the died-early runs`).toContain(command);
    }
  });

  it("returns newest first", () => {
    const ids = listRuns().runs.map((run) => run.runId);
    expect([...ids].sort().reverse()).toEqual(ids);
  });

  it("survives the manifests written before prompt_variant existed", () => {
    // Five runs predate the field. The schema defaults it rather than rejecting the run,
    // which is why listing does not throw here.
    const variants = new Set(listRuns().runs.map((run) => run.promptVariant));
    expect(variants.has("default")).toBe(true);
  });
});

describe("the four runs §10 names", () => {
  it("stage 1: one turn, 6,376 prompt and 152 completion tokens, $0.0175", () => {
    const run = loadRun(findRun(ACCEPTANCE.syntaxSpec));
    expect(run.manifest.stage).toBe("syntax_spec");
    expect(run.turns).toHaveLength(1);
    expect(run.manifest.prompt_tokens).toBe(6376);
    expect(run.manifest.completion_tokens).toBe(152);
    expect(run.manifest.cost_usd).toBeCloseTo(0.0175, 4);
  });

  it("stage 2: two turns, $0.0566", () => {
    const run = loadRun(findRun(ACCEPTANCE.generate));
    expect(run.manifest.stage).toBe("generate");
    expect(run.manifest.turns).toBe(2);
    expect(run.turns).toHaveLength(2);
    expect(run.manifest.cost_usd).toBeCloseTo(0.0566, 4);
  });

  it("stage 3: ten turns, $0.0353, and five sessions", () => {
    const run = loadRun(findRun(ACCEPTANCE.trace));
    expect(run.manifest.stage).toBe("trace");
    expect(run.manifest.turns).toBe(10);
    expect(run.turns).toHaveLength(10);
    expect(run.manifest.cost_usd).toBeCloseTo(0.0353, 4);
    expect((run.manifest.checks.sessions as unknown[]).length).toBe(5);
  });

  it("stage 4: PaSh format, 23,202 prompt tokens, $0.0606", () => {
    const run = loadRun(findRun(ACCEPTANCE.annotate));
    expect(run.manifest.stage).toBe("annotate");
    expect(annotationFormatOf(run.manifest)).toBe("pash");
    expect(run.manifest.prompt_tokens).toBe(23202);
    expect(run.manifest.cost_usd).toBeCloseTo(0.0606, 4);
  });
});

describe("turn ordering", () => {
  it("orders the ten-turn trace by turn number, not by filename", () => {
    // Sorting the filenames would put `turn-10` between `turn-01` and `turn-02`. The turn
    // number is read from inside each record instead, so the order is 0..9.
    const turns = loadTurns(findRun(ACCEPTANCE.trace));
    expect(turns.map((turn) => turn.turn)).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
  });

  it("gives every turn of a run the run's start time, not its own (Phase 0(a))", () => {
    const turns = loadTurns(findRun(ACCEPTANCE.trace));
    const stamps = new Set(turns.map((turn) => turn.timestamp));
    expect(stamps.size).toBe(1);
    // Which is why a duration can never be derived by subtracting two of them.
    expect([...stamps][0]).toContain("16:39:35");
  });
});

describe("reconstructing the command line (Phase 0(b))", () => {
  it("rebuilds the stage-3 trace run from its manifest", () => {
    const run = loadRun(findRun(ACCEPTANCE.trace));
    const line = reconstructCommand(run.manifest);
    expect(line.reconstructed).toBe(true);
    expect(line.args).toContain("trace");
    expect(line.args).toContain("--limit");
    expect(line.args[line.args.indexOf("--limit") + 1]).toBe("5");
    expect(line.args[line.args.indexOf("--max-turns") + 1]).toBe("15");
    // `lima:caruca` is one recorded field standing for two CLI options.
    expect(line.args[line.args.indexOf("--isolation") + 1]).toBe("lima");
    expect(line.args[line.args.indexOf("--lima-instance") + 1]).toBe("caruca");
    expect(line.args.at(-1)).toBe("cat");
  });

  it("puts the annotation format before the command for stage 4", () => {
    const run = loadRun(findRun(ACCEPTANCE.annotate));
    const line = reconstructCommand(run.manifest);
    expect(line.args.at(-2)).toBe("pash");
    expect(line.args.at(-1)).toBe("cat");
  });

  it("names the options it could not recover instead of inventing them", () => {
    const run = loadRun(findRun(ACCEPTANCE.trace));
    const line = reconstructCommand(run.manifest);
    expect(line.notRecorded).toContain("--out");
    expect(line.notRecorded).toContain("--keep-workspace");
    // And never emits them as if they had been recorded.
    for (const flag of line.notRecorded) expect(line.args).not.toContain(flag);
  });

  it("rebuilds every committed run without throwing", () => {
    for (const summary of listRuns().runs) {
      const line = reconstructCommand(loadRun(summary.dir).manifest);
      expect(line.display.startsWith(".venv/bin/caruca-v2 ")).toBe(true);
      expect(line.args).not.toContain("<format not recorded>");
    }
  });
});

describe("recordings", () => {
  it("reports no terminal recording for the runs made before the console existed", () => {
    // §6.3: a run made before the console has none, and the Run screen must say so rather than
    // showing an empty terminal. Runs the console started itself do have one, which is why
    // this is scoped by date rather than asserting that none exists at all.
    const before = listRuns().runs.filter((run) => run.runId < "2026-09-23");
    expect(before.length).toBeGreaterThan(100);
    expect(before.filter((run) => run.hasRecording)).toEqual([]);
  });

  it("gives a run the console started its own recording", () => {
    const recorded = listRuns().runs.filter((run) => run.hasRecording);
    // Every recording belongs to a run made since the console could make them.
    for (const run of recorded) expect(run.runId >= "2026-09-23").toBe(true);
  });
});

describe("paths", () => {
  it("finds the repo root from the console directory", () => {
    expect(repoPaths().root).toMatch(/caruca_v2$/);
  });
});
