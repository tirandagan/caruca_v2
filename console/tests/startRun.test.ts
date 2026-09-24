/**
 * Starting runs, and the confirmation that has to come first.
 *
 * Phase 5 is the only part of the console that can spend money, so most of what is tested here
 * is what it refuses. Nothing in this file starts a process: `startV2` throws before reaching
 * the registry when a confirmation is missing or stale, which is the behaviour worth pinning.
 */
import { describe, expect, it } from "vitest";
import { PaidRunNotConfirmedError, newRunId } from "../src/server/startRun.js";
import { startV2 } from "../src/server/startRun.js";
import {
  assertProgramAllowed,
  parseV2RunDir,
  ProgramNotAllowedError,
} from "../src/server/processes.js";
import { estimateCost } from "../src/data/preflight.js";
import { repoPaths } from "../src/data/paths.js";
import { join } from "node:path";

describe("nothing paid starts without being asked for", () => {
  it("refuses a v2 stage with no confirmation", () => {
    expect(() =>
      startV2({ stage: "syntax_spec", command: "cat", model: "openai/gpt-4o" }),
    ).toThrow(PaidRunNotConfirmedError);
  });

  it("refuses a confirmation that was not actually given", () => {
    expect(() =>
      startV2({
        stage: "syntax_spec",
        command: "cat",
        model: "openai/gpt-4o",
        confirmation: { acceptedUsd: 0.0117, confirmed: false },
      }),
    ).toThrow(PaidRunNotConfirmedError);
  });

  it("refuses when the estimate has moved since it was shown", () => {
    // Nobody should agree to one figure and be charged against another.
    const actual = estimateCost("syntax_spec", "openai/gpt-4o").usdPerRun!;
    expect(() =>
      startV2({
        stage: "syntax_spec",
        command: "cat",
        model: "openai/gpt-4o",
        confirmation: { acceptedUsd: actual + 5, confirmed: true },
      }),
    ).toThrow(/estimate has moved/);
  });

  it("says what both figures were, so the difference is visible", () => {
    const actual = estimateCost("syntax_spec", "openai/gpt-4o").usdPerRun!;
    try {
      startV2({
        stage: "syntax_spec",
        command: "cat",
        model: "openai/gpt-4o",
        confirmation: { acceptedUsd: actual + 5, confirmed: true },
      });
      expect.unreachable("should have refused");
    } catch (cause) {
      expect((cause as Error).message).toContain(actual.toFixed(4));
      expect((cause as Error).message).toContain((actual + 5).toFixed(4));
    }
  });
});

describe("only a fixed set of programs may be started", () => {
  it("allows the two CLIs and limactl", () => {
    expect(() =>
      assertProgramAllowed(join(repoPaths().root, ".venv", "bin", "caruca-v2")),
    ).not.toThrow();
    expect(() => assertProgramAllowed("limactl")).not.toThrow();
  });

  it("refuses anything else, however plausible", () => {
    for (const program of ["/bin/sh", "/usr/bin/env", "python3", "/bin/rm", "caruca-v2"]) {
      expect(() => assertProgramAllowed(program), program).toThrow(ProgramNotAllowedError);
    }
  });

  it("refuses a program that merely shares a name with an allowed one", () => {
    // The check is on the resolved path, not the basename.
    expect(() => assertProgramAllowed("/tmp/evil/caruca-v2")).toThrow(ProgramNotAllowedError);
  });
});

describe("run ids", () => {
  it("follow the shape v2's own run directories use", () => {
    const id = newRunId("cat");
    expect(id).toMatch(/^\d{4}-\d{2}-\d{2}T\d{6}Z_cat_[0-9a-f]{8}$/);
  });

  it("do not collide when two are made in the same second", () => {
    const ids = new Set(Array.from({ length: 200 }, () => newRunId("cat")));
    expect(ids.size).toBe(200);
  });
});

describe("finding the run directory v2 made for itself", () => {
  it("reads it from v2's summary line", () => {
    // v2 mints its own run id, so the console cannot know it in advance. Without this the
    // recording is orphaned in a directory holding nothing else, and the Run screen — which
    // looks a run up by v2's id — finds no recording for a run that was recorded.
    const output =
      "naive-llm cat\r\n" +
      "run      eval/runs/2026-09-24T164219Z_cat_0c81e1eb\r\n" +
      "spec     cat.py, 13 elements — validated\r\n" +
      "cost     $0.017460\r\n";
    expect(parseV2RunDir(output)).toBe("eval/runs/2026-09-24T164219Z_cat_0c81e1eb");
  });

  it("sees through the escape sequences the live display writes", () => {
    const output =
      "\u001b[?25l⠋ asking openai/gpt-4o\r\u001b[2K" +
      "run      eval/runs/2026-09-24T164219Z_cat_0c81e1eb\r\n";
    expect(parseV2RunDir(output)).toBe("eval/runs/2026-09-24T164219Z_cat_0c81e1eb");
  });

  it("does not mistake a path mentioned elsewhere for the run directory", () => {
    const output =
      "reading eval/runs/2026-01-01T000000Z_old_deadbeef/manifest.json for comparison\r\n" +
      "run      eval/runs/2026-09-24T164219Z_cat_0c81e1eb\r\n";
    expect(parseV2RunDir(output)).toBe("eval/runs/2026-09-24T164219Z_cat_0c81e1eb");
  });

  it("returns null when v2 printed no run line, rather than guessing", () => {
    expect(parseV2RunDir("something went wrong before it started\r\n")).toBeNull();
    expect(parseV2RunDir("")).toBeNull();
  });
});
