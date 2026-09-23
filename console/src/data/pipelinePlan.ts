/**
 * What a pipeline run would consist of, built without running anything (§6.1).
 *
 * The two sides do not have the same shape, and drawing them as though they did is the main
 * thing this module exists to prevent:
 *
 *   v2:  specification → generate (invocations and configurations) → trace --configs → annotate --traces
 *   v1:  specification → trace → annotate --input
 *
 * v1's `trace` works out its own invocations from the specification and the generation
 * options. v1's `generate` feeds nothing — it prints the invocations `trace` will run — so the
 * console shows it as stage 3's preview and count rather than as a step in the chain.
 */
import { join } from "node:path";
import type { Stage } from "./schema.js";
import { repoPaths, v1Root } from "./paths.js";
import {
  v1Annotate,
  v1Generate,
  v1SyntaxSpec,
  v1Trace,
  type GenerationBounds,
  type V1Invocation,
} from "./v1Invocations.js";
import { estimateCost, whereItMustRun, type CostEstimate } from "./preflight.js";

export const STAGE_ORDER: readonly Stage[] = ["syntax_spec", "generate", "trace", "annotate"];

export const STAGE_TITLE: Record<Stage, string> = {
  syntax_spec: "Stage 1 · specification",
  generate: "Stage 2 · invocations and configurations",
  trace: "Stage 3 · execution and tracing",
  annotate: "Stage 4 · annotation",
};

/** What each side does at this stage, in one sentence. */
export const STAGE_ROLE: Record<Stage, { v1: string; v2: string }> = {
  syntax_spec: {
    v1: "Generates a specification from the man page with DSPy. Needs .venv-llm and a key.",
    v2: "Sends the documentation to a model and parses the specification back.",
  },
  generate: {
    v1: "Prints the invocations trace will run. Feeds nothing: it is stage 3's preview.",
    v2: "Expands the specification into invocations and the environments they need.",
  },
  trace: {
    v1: "Works out its own invocations from the specification, executes them under strace.",
    v2: "Executes the configurations it is given in a sandbox and reports what it observed.",
  },
  annotate: {
    v1: "Derives a consumer specification from the trace file procedurally.",
    v2: "Asks a model to derive the same specification from the same traces.",
  },
};

/** Where v2 can take v1's artifact instead of its own, for a comparison on identical input. */
export const IDENTICAL_INPUT: Partial<Record<Stage, { takes: string; note: string }>> = {
  generate: {
    takes: "v1's committed specification",
    note: "already the default",
  },
  trace: {
    takes: "v1's own configuration expansion, eval/v1_configs/CMD.configs.json",
    note: "as the parity study did",
  },
  annotate: {
    takes: "v1's traces",
    note: "already the default",
  },
};

export interface StepPlan {
  readonly stage: Stage;
  readonly side: "v1" | "v2";
  /** False where this side has no step at this stage in the chain. */
  readonly inChain: boolean;
  readonly where: "mac" | "lima";
  readonly whyThere: string;
  /** True when the step sends a prompt to a paid model. */
  readonly callsModel: boolean;
  readonly estimate: CostEstimate | null;
  /** The exact argument list, for v1. */
  readonly invocation: V1Invocation | null;
  /** The command line v2 would be given, for a v2 step. */
  readonly v2Argv: string[] | null;
  /** Anything that would stop this step running, stated before it runs. */
  readonly blockers: string[];
  readonly notes: string[];
}

export interface PlanOptions {
  readonly command: string;
  readonly bounds?: GenerationBounds;
  readonly model?: string;
  readonly runId?: string;
  readonly limaInstance?: string;
  readonly platform?: NodeJS.Platform;
  /** Whether v1's stage 1 would run live, or read its archived output. */
  readonly v1Stage1?: "live" | "archived" | "fetch";
  readonly openAiKeyPresent?: boolean;
}

function v1RunFile(runId: string, name: string): string {
  return join(repoPaths().v1Runs, runId, name);
}

/**
 * Plan one side's step at one stage.
 *
 * Nothing is executed. Every v1 argument list is built through `v1Invocations.ts`, so a step
 * that cannot be expressed safely — an output path inside v1's checkout — fails here, before
 * a process could ever start.
 */
export function planStep(stage: Stage, side: "v1" | "v2", options: PlanOptions): StepPlan {
  const command = options.command;
  const runId = options.runId ?? "PREVIEW";
  const bounds = options.bounds ?? {};
  const model = options.model ?? "openai/gpt-4o";
  const { where, reason } = whereItMustRun(side, stage, command, options.platform);

  const blockers: string[] = [];
  const notes: string[] = [];
  let invocation: V1Invocation | null = null;
  let inChain = true;
  let callsModel = false;

  if (side === "v2") {
    callsModel = true;
    const identical = IDENTICAL_INPUT[stage];
    if (identical) notes.push(`Can take ${identical.takes} — ${identical.note}.`);
    return {
      stage,
      side,
      inChain,
      where,
      whyThere: reason,
      callsModel,
      estimate: estimateCost(stage, model),
      invocation: null,
      v2Argv: v2CommandLine(stage, options, where),
      blockers,
      notes,
    };
  }

  // ---- v1 ----
  try {
    switch (stage) {
      case "syntax_spec": {
        const mode = options.v1Stage1 ?? "archived";
        if (mode === "live") {
          callsModel = true;
          invocation = v1SyntaxSpec(command, { root: v1Root() });
          if (options.openAiKeyPresent === false) {
            blockers.push(
              "OPENAI_API_KEY is not set. v1's llm.py calls OpenAI directly, with gpt-4o fixed in its code.",
            );
          }
          notes.push(
            "A live v1 stage 1 is a paid call v1 does not meter. The console's forwarder records the tokens and cost OpenRouter reports, which is the first time v1's LLM step has been costed.",
          );
        } else if (mode === "fetch") {
          invocation = v1SyntaxSpec(command, { fetch: true, root: v1Root() });
          notes.push("Reads v1's committed, hand-checked specification. Not a live run.");
        } else {
          invocation = null;
          notes.push(
            "Uses v1's archived LLM output, which is what the parity study used. Not a live run.",
          );
        }
        break;
      }

      case "generate": {
        // v1's generate feeds nothing: it prints what trace will run.
        inChain = false;
        invocation = v1Generate(command, bounds);
        notes.push(
          "Not a step in v1's chain. v1's trace works out its own invocations; this is the preview and the count.",
        );
        notes.push("--output is accepted and never used, so nothing is written.");
        break;
      }

      case "trace": {
        invocation = v1Trace(command, v1RunFile(runId, `${command}.json`), bounds, {
          ...(options.limaInstance ? { limaInstance: options.limaInstance } : {}),
        });
        notes.push(
          "Runs under v1's default isolation: CARUCA_ISOLATION_METHOD is left unset, which is what the parity study ran under.",
        );
        break;
      }

      case "annotate": {
        invocation = v1Annotate("pash", command, v1RunFile(runId, `${command}.json`), {
          ...(options.limaInstance ? { limaInstance: options.limaInstance } : {}),
        });
        notes.push("The one form that needs a shell — v1.py already passes it to sh -lc.");
        break;
      }
    }
  } catch (cause) {
    blockers.push((cause as Error).message);
  }

  return {
    stage,
    side,
    inChain,
    where,
    whyThere: reason,
    callsModel,
    estimate: null,
    invocation,
    v2Argv: null,
    blockers,
    notes,
  };
}

/** v2's CLI name for each stage. Only stage 1 differs from its internal name. */
const V2_SUBCOMMAND: Record<Stage, string> = {
  syntax_spec: "naive-llm",
  generate: "generate",
  trace: "trace",
  annotate: "annotate",
};

/**
 * The command line v2 would actually be given.
 *
 * Built rather than sketched, because the flags that place a step somewhere are the ones most
 * worth seeing: a stage-3 preview that omits `--isolation lima` shows a command that would not
 * do what the row beside it says. The bounds are included for the same reason — a run at
 * different bounds from the one it is compared against measures the bounds.
 */
function v2CommandLine(stage: Stage, options: PlanOptions, where: "mac" | "lima"): string[] {
  const argv = [".venv/bin/caruca-v2", V2_SUBCOMMAND[stage]];
  const bounds = options.bounds ?? {};

  if (stage === "generate") {
    if (bounds.maxArity !== undefined) argv.push("--max-arity", String(bounds.maxArity));
    if (bounds.maxCount !== undefined) argv.push("--max-count", String(bounds.maxCount));
  }

  if (stage === "trace") {
    argv.push("--isolation", where === "lima" ? "lima" : "host");
    if (where === "lima") argv.push("--lima-instance", options.limaInstance ?? "caruca");
  }

  if (stage === "annotate") {
    // v2's annotate calls v1's annotator, which cannot run on macOS at all.
    argv.push("--v1-runner", where === "lima" ? "lima" : "host");
    if (where === "lima") argv.push("--lima-instance", options.limaInstance ?? "caruca");
    argv.push("pash");
  }

  argv.push(options.command, "--model", options.model ?? "openai/gpt-4o", "--temperature", "0.0");
  return argv;
}

export interface PipelinePlan {
  readonly command: string;
  readonly steps: StepPlan[];
  /** Steps that would send a prompt to a paid model. */
  readonly paidSteps: StepPlan[];
  /** Total of the estimates that exist. Null when none does. */
  readonly estimatedUsd: number | null;
  /** Paid steps with no measured run behind them, so the total understates. */
  readonly unestimatedSteps: number;
  readonly blockers: { stage: Stage; side: "v1" | "v2"; reason: string }[];
}

export function planPipeline(
  stages: readonly Stage[],
  sides: readonly ("v1" | "v2")[],
  options: PlanOptions,
): PipelinePlan {
  const steps = stages.flatMap((stage) => sides.map((side) => planStep(stage, side, options)));
  const paidSteps = steps.filter((step) => step.callsModel);

  const withEstimate = paidSteps.filter((step) => step.estimate?.usdPerRun != null);
  return {
    command: options.command,
    steps,
    paidSteps,
    estimatedUsd:
      withEstimate.length > 0
        ? withEstimate.reduce((sum, step) => sum + (step.estimate?.usdPerRun ?? 0), 0)
        : null,
    unestimatedSteps: paidSteps.length - withEstimate.length,
    blockers: steps.flatMap((step) =>
      step.blockers.map((reason) => ({ stage: step.stage, side: step.side, reason })),
    ),
  };
}
