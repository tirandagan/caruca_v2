/**
 * The pipeline plan.
 *
 * What these protect is that the screen shows the run it would actually make. A preview that
 * omits the flag placing a step in the VM, or that draws v1's chain as though it had four
 * links, describes a run nobody would get.
 */
import { describe, expect, it } from "vitest";
import { planPipeline, planStep, STAGE_ORDER, IDENTICAL_INPUT } from "../src/data/pipelinePlan.js";
import { v1ProtectedOutputs } from "../src/data/paths.js";

const BASE = { command: "cat", model: "openai/gpt-4o", bounds: { maxArity: 1, maxCount: 1 } };

describe("the two chains have different shapes", () => {
  it("marks v1's generate as not part of v1's chain", () => {
    // v1's trace works out its own invocations; generate prints what trace will run.
    const step = planStep("generate", "v1", BASE);
    expect(step.inChain).toBe(false);
    expect(step.notes.join(" ")).toContain("works out its own invocations");
  });

  it("keeps every v2 stage in the chain", () => {
    for (const stage of STAGE_ORDER) {
      expect(planStep(stage, "v2", BASE).inChain).toBe(true);
    }
  });

  it("names the three places v2 can take v1's artifact instead", () => {
    expect(Object.keys(IDENTICAL_INPUT).sort()).toEqual(["annotate", "generate", "trace"]);
  });
});

describe("the previewed command matches where the step runs", () => {
  it("puts --isolation lima on a destructive trace", () => {
    const step = planStep("trace", "v2", { ...BASE, command: "rm" });
    expect(step.where).toBe("lima");
    expect(step.v2Argv?.join(" ")).toContain("--isolation lima");
    expect(step.v2Argv?.join(" ")).toContain("--lima-instance caruca");
  });

  it("uses the host for a trace that does not need the VM", () => {
    const step = planStep("trace", "v2", { ...BASE, command: "cat", platform: "linux" });
    expect(step.v2Argv?.join(" ")).toContain("--isolation host");
  });

  it("sends v2's annotate through the VM on macOS, because it calls v1's", () => {
    const step = planStep("annotate", "v2", { ...BASE, platform: "darwin" });
    expect(step.v2Argv?.join(" ")).toContain("--v1-runner lima");
    // The consumer format is a positional and must come before the command.
    const argv = step.v2Argv!;
    expect(argv.indexOf("pash")).toBeLessThan(argv.indexOf("cat"));
  });

  it("carries the bounds into v2's generate, since a different bound measures the bound", () => {
    const step = planStep("generate", "v2", { ...BASE, bounds: { maxArity: 2, maxCount: 4 } });
    expect(step.v2Argv?.join(" ")).toContain("--max-arity 2");
    expect(step.v2Argv?.join(" ")).toContain("--max-count 4");
  });

  it("always states a model and a temperature", () => {
    for (const stage of STAGE_ORDER) {
      const argv = planStep(stage, "v2", BASE).v2Argv!;
      expect(argv).toContain("--model");
      expect(argv).toContain("--temperature");
    }
  });
});

describe("v1's steps are the forms §3 records", () => {
  it("writes v1's trace output into the run's own folder, never v1's", () => {
    const step = planStep("trace", "v1", { ...BASE, runId: "2026-09-23T000000Z_cat_abcd1234" });
    const output = step.invocation!.outputPath!;
    expect(output).toContain("/eval/v1_runs/");
    expect(output.startsWith(v1ProtectedOutputs())).toBe(false);
  });

  it("sets no isolation variable, so v1 runs under its own default", () => {
    const step = planStep("trace", "v1", BASE);
    expect(step.invocation!.argv.join(" ")).not.toContain("CARUCA_ISOLATION_METHOD");
    expect(step.notes.join(" ")).toContain("left unset");
  });

  it("uses the archived output for v1's stage 1 by default, and says it is not a live run", () => {
    const step = planStep("syntax_spec", "v1", BASE);
    expect(step.callsModel).toBe(false);
    expect(step.invocation).toBeNull();
    expect(step.notes.join(" ")).toContain("Not a live run");
  });

  it("blocks a live v1 stage 1 when the key is absent, rather than starting it", () => {
    const step = planStep("syntax_spec", "v1", {
      ...BASE,
      v1Stage1: "live",
      openAiKeyPresent: false,
    });
    expect(step.callsModel).toBe(true);
    expect(step.blockers.join(" ")).toContain("OPENAI_API_KEY");
  });

  it("says a live v1 stage 1 is a paid call v1 does not meter", () => {
    const step = planStep("syntax_spec", "v1", {
      ...BASE,
      v1Stage1: "live",
      openAiKeyPresent: true,
    });
    expect(step.blockers).toEqual([]);
    expect(step.notes.join(" ")).toContain("does not meter");
  });
});

describe("the whole plan", () => {
  const plan = planPipeline(STAGE_ORDER, ["v1", "v2"], BASE);

  it("counts four paid steps: v2's four stages, and none of v1's by default", () => {
    expect(plan.paidSteps).toHaveLength(4);
    expect(plan.paidSteps.every((step) => step.side === "v2")).toBe(true);
  });

  it("totals only the estimates that exist, and says how many are missing", () => {
    expect(plan.estimatedUsd).toBeGreaterThan(0);
    expect(plan.unestimatedSteps).toBe(0);
  });

  it("reports no estimate at all for a model nothing has been run with", () => {
    const unknown = planPipeline(STAGE_ORDER, ["v2"], {
      ...BASE,
      model: "a/model-nobody-has-run",
    });
    expect(unknown.estimatedUsd).toBeNull();
    expect(unknown.unestimatedSteps).toBe(4);
  });

  it("surfaces a blocker from any step", () => {
    const blocked = planPipeline(["syntax_spec"], ["v1"], {
      ...BASE,
      v1Stage1: "live",
      openAiKeyPresent: false,
    });
    expect(blocked.blockers).toHaveLength(1);
    expect(blocked.blockers[0]!.side).toBe("v1");
  });
});
