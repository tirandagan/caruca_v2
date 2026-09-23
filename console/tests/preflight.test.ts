/**
 * The pre-flight.
 *
 * Everything here reads or counts; nothing spends money and nothing executes a traced command.
 * The counting tests run v1's real `generate`, which prints invocation strings and executes
 * nothing — that is what makes counting `rm` safe.
 */
import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";
import {
  DESTRUCTIVE_COMMANDS,
  checkEnvironment,
  countEnumeration,
  envFileVariableNames,
  estimateCost,
  whereItMustRun,
} from "../src/data/preflight.js";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { v1Root } from "../src/data/paths.js";

function v1Present(): boolean {
  try {
    return existsSync(join(v1Root(), "caruca", ".venv", "bin", "caruca"));
  } catch {
    return false;
  }
}

describe.skipIf(!v1Present())("counting what v1 will actually do", () => {
  it("counts mkdir at v1's defaults as 4,240 printed and 1,094 distinct", { timeout: 120_000 }, async () => {
    // §10's acceptance figure, and the reason counting is done by reading what v1 prints.
    const count = await countEnumeration("mkdir");
    expect(count.printed).toBe(4240);
    expect(count.distinct).toBe(1094);
    expect(count.capped).toBe(false);
  });

  it("gives pwd a count, where --number crashes", { timeout: 60_000 }, async () => {
    // `generate pwd --number` dies with ValueError: max() iterable argument is empty.
    // Counting what v1 prints works regardless.
    const count = await countEnumeration("pwd");
    expect(count.printed).toBe(16);
    expect(count.distinct).toBeGreaterThan(0);
  });

  it("never passes --number", { timeout: 60_000 }, async () => {
    const count = await countEnumeration("pwd");
    expect(count.argv).not.toContain("--number");
  });

  it("passes the bounds it was given, because a different bound measures the bound", { timeout: 60_000 }, async () => {
    const count = await countEnumeration("cat", { maxCount: 1 });
    expect(count.argv).toContain("--max-count");
    expect(count.printed).toBeLessThan(100);
  });

  it("stops at the line cap and says so", { timeout: 120_000 }, async () => {
    const count = await countEnumeration("mkdir", {}, { lineCap: 100 });
    expect(count.printed).toBe(100);
    expect(count.capped).toBe(true);
    expect(count.cappedReason).toContain("cap");
  });
});

describe("where each step has to run", () => {
  it("sends v1's trace and annotate to the VM", () => {
    expect(whereItMustRun("v1", "trace", "cat").where).toBe("lima");
    expect(whereItMustRun("v1", "annotate", "cat", "darwin").where).toBe("lima");
  });

  it("explains why v1's annotate cannot run on macOS", () => {
    expect(whereItMustRun("v1", "annotate", "cat", "darwin").reason).toContain("/private/tmp");
  });

  it("keeps v1's generate and syntax-spec on the host", () => {
    expect(whereItMustRun("v1", "generate", "cat").where).toBe("mac");
    expect(whereItMustRun("v1", "syntax_spec", "cat").where).toBe("mac");
  });

  it("sends v2's trace to the VM for a destructive command only", () => {
    expect(whereItMustRun("v2", "trace", "rm").where).toBe("lima");
    expect(whereItMustRun("v2", "trace", "cat").where).toBe("mac");
    expect(whereItMustRun("v2", "trace", "rm").reason).toContain("destructive");
  });

  it("sends v2's annotate to the VM on macOS, because it calls v1's", () => {
    expect(whereItMustRun("v2", "annotate", "cat", "darwin").where).toBe("lima");
    expect(whereItMustRun("v2", "annotate", "cat", "linux").where).toBe("mac");
  });

  it("knows rm is destructive", () => {
    expect(DESTRUCTIVE_COMMANDS).toContain("rm");
  });
});

describe("cost estimates", () => {
  it("estimates from measured runs and states its basis", () => {
    const estimate = estimateCost("syntax_spec", "openai/gpt-4o");
    expect(estimate.basedOn).toBeGreaterThan(0);
    expect(estimate.usdPerRun).toBeGreaterThan(0);
    // An estimate without its basis is a guess, so the basis is never empty.
    expect(estimate.basis).toContain("measured run");
    expect(estimate.basis).toContain("range");
  });

  it("says it cannot estimate rather than guessing", () => {
    const estimate = estimateCost("syntax_spec", "a/model-nobody-has-run");
    expect(estimate.usdPerRun).toBeNull();
    expect(estimate.basedOn).toBe(0);
    expect(estimate.basis).toContain("nothing to estimate from");
  });
});

describe("environment checks", () => {
  const checks = checkEnvironment();

  it("checks both CLIs, the VM, v1's commit and the keys", () => {
    const names = checks.map((check) => check.name);
    expect(names).toContain("caruca-v2");
    expect(names).toContain("v1 commit");
    expect(names).toContain("OPENROUTER_API_KEY");
    expect(names.some((name) => name.startsWith("Lima VM"))).toBe(true);
  });

  it("counts a key in .env as present, because caruca-v2 loads it", () => {
    // The key does not have to be in the console's own shell: `caruca-v2` reads `.env` when
    // it starts. Calling it missing would send someone hunting a problem that is not there.
    const key = checks.find((check) => check.name === "OPENROUTER_API_KEY")!;
    expect(key.state).toBe("ok");
    expect(key.detail).toMatch(/\.env|this shell/);
  });

  it("reads variable names out of .env and never their values", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-env-"));
    const file = join(dir, ".env");
    writeFileSync(file, "OPENROUTER_API_KEY=sk-secret-value-1234567890\n# a comment\nexport OTHER=1\n\n");
    const names = envFileVariableNames(file);
    expect([...names].sort()).toEqual(["OPENROUTER_API_KEY", "OTHER"]);
    // The set holds names. There is nowhere for a value to be.
    expect([...names].join(" ")).not.toContain("sk-secret");
  });

  it("treats a missing .env as empty rather than failing", () => {
    expect(envFileVariableNames("/nowhere/.env").size).toBe(0);
  });

  it("reports key presence without touching the value", () => {
    const key = checks.find((check) => check.name === "OPENROUTER_API_KEY")!;
    // Whatever the state, the detail must not contain anything that looks like a key.
    expect(key.detail).not.toMatch(/sk-|[A-Za-z0-9]{32,}/);
    if (key.state === "ok") expect(key.detail).toContain("never read");
  });

  it("names the pinned v1 commit when it disagrees", () => {
    const commit = checks.find((check) => check.name === "v1 commit");
    if (commit?.state === "missing") {
      expect(commit.detail).toContain("pinned to");
      expect(commit.detail).toContain("not comparable");
    } else {
      expect(commit?.detail ?? "").toMatch(/pinned commit|could not read/);
    }
  });
});
