/**
 * Rebuilding a v2 run's command line from its manifest.
 *
 * Phase 0(b) established that no manifest records `sys.argv`. What it does record is every
 * option-bearing value, so the line below is rebuilt rather than recalled. It is labelled
 * "reconstructed" everywhere it is shown - not because it is approximate, but because its
 * provenance differs from a line that was captured as typed, and the console does not blur
 * that distinction.
 *
 * Flags the manifest genuinely cannot account for are returned in `notRecorded` instead of
 * being guessed at. `--out`, `--db`, `--plain` and `--log-conversation` change where output
 * goes and how it looks, never what the model was asked, so a reconstruction missing them is
 * still faithful about the experiment - and saying so is better than silently emitting a
 * default that may not have been used.
 */
import type { RunManifest, Stage } from "./schema.js";

/** The CLI subcommand each stage is invoked as. Only stage 1 differs from its internal name. */
const SUBCOMMAND: Record<Stage, string> = {
  syntax_spec: "naive-llm",
  generate: "generate",
  trace: "trace",
  annotate: "annotate",
};

/** Options that exist on every stage and are recorded in the manifest. */
function sharedModelArgs(manifest: RunManifest): string[] {
  const args = ["--model", manifest.model_requested];
  const { temperature, max_tokens, ...rest } = manifest.decoding_params;
  args.push("--temperature", String(temperature));
  if (manifest.seed !== null) args.push("--seed", String(manifest.seed));
  args.push("--max-tokens", String(max_tokens));
  if (manifest.provider) args.push("--provider", manifest.provider);
  // Anything a later stage started recording in decoding_params, surfaced rather than dropped.
  for (const [key, value] of Object.entries(rest)) {
    args.push(`--${key.replace(/_/g, "-")}`, String(value));
  }
  return args;
}

function str(inputs: Record<string, unknown>, key: string): string | null {
  const value = inputs[key];
  return typeof value === "string" ? value : null;
}

function num(inputs: Record<string, unknown>, key: string): number | null {
  const value = inputs[key];
  return typeof value === "number" ? value : null;
}

export interface ReconstructedCommand {
  /** The program, as it would be invoked from the repo root. */
  readonly program: string;
  readonly args: string[];
  /** Ready to copy into a terminal. */
  readonly display: string;
  /**
   * Options this run may have used that the manifest does not record, so they could not be
   * rebuilt. Shown beside the line rather than folded into it.
   */
  readonly notRecorded: string[];
  /** Always true for a v2 run: no manifest holds the argument list as typed (Phase 0(b)). */
  readonly reconstructed: true;
}

/**
 * Which annotation format a stage-4 run produced.
 *
 * The format is a positional argument, and `inputs` does not carry it - but every stage-4 run
 * names its output `<command>.<format>.annotation`, so the artifact says what the arguments
 * did not. Returns null rather than assuming `pash` when the output is missing.
 */
export function annotationFormatOf(manifest: RunManifest): string | null {
  for (const path of manifest.output_paths) {
    const match = /\.([a-z]+)\.annotation$/.exec(path);
    if (match?.[1]) return match[1];
  }
  return null;
}

export function reconstructCommand(manifest: RunManifest): ReconstructedCommand {
  const inputs = manifest.inputs as Record<string, unknown>;
  const args: string[] = [SUBCOMMAND[manifest.stage]];
  const notRecorded: string[] = ["--out", "--db", "--log-conversation", "--plain"];

  switch (manifest.stage) {
    case "syntax_spec": {
      const docs = str(inputs, "docs_source");
      if (docs) args.push("--docs", docs);
      if (manifest.prompt_variant !== "default") {
        args.push("--prompt-variant", manifest.prompt_variant);
      }
      break;
    }
    case "generate": {
      const spec = str(inputs, "spec_source");
      if (spec) args.push("--spec", spec);
      const maxArity = num(inputs, "max_arity");
      if (maxArity !== null) args.push("--max-arity", String(maxArity));
      const maxCount = num(inputs, "max_count");
      if (maxCount !== null) args.push("--max-count", String(maxCount));
      const stdin = str(inputs, "stdin_variation");
      if (stdin) args.push("--stdin", stdin);
      const content = str(inputs, "content_variation");
      if (content) args.push("--content", content);
      const skip = str(inputs, "skip_flags");
      if (skip) args.push("--skip", skip);
      const maxTurns = num(inputs, "max_turns");
      if (maxTurns !== null) args.push("--max-turns", String(maxTurns));
      // Whether v1 was consulted is not recorded; the comparison's result is, but not the flag.
      notRecorded.push("--no-compare", "--compare-timeout");
      break;
    }
    case "trace": {
      const configs = str(inputs, "configs_source");
      if (configs) args.push("--configs", configs);
      const limit = num(inputs, "limit");
      if (limit !== null) args.push("--limit", String(limit));
      const maxTurns = num(inputs, "max_turns");
      if (maxTurns !== null) args.push("--max-turns", String(maxTurns));
      // Recorded as "host" or "lima:<instance>", which is two CLI options in one field.
      const isolation = str(inputs, "isolation");
      if (isolation) {
        const [kind, instance] = isolation.split(":", 2);
        if (kind) args.push("--isolation", kind);
        if (instance) args.push("--lima-instance", instance);
      }
      notRecorded.push("--keep-workspace");
      break;
    }
    case "annotate": {
      const traces = str(inputs, "traces_source");
      if (traces) args.push("--traces", traces);
      const maxTurns = num(inputs, "max_turns");
      if (maxTurns !== null) args.push("--max-turns", String(maxTurns));
      const runner = str(inputs, "v1_runner");
      if (runner) args.push("--v1-runner", runner);
      notRecorded.push("--no-compare", "--lima-instance");
      break;
    }
  }

  args.push(...sharedModelArgs(manifest));

  // Positionals go last: argparse accepts them anywhere, and keeping them together with the
  // command reads better than threading them through each stage's branch.
  if (manifest.stage === "annotate") {
    const format = annotationFormatOf(manifest);
    args.push(format ?? "<format not recorded>");
  }
  args.push(...manifest.command.split(" "));

  const program = ".venv/bin/caruca-v2";
  return {
    program,
    args,
    display: [program, ...args].map(quoteIfNeeded).join(" "),
    notRecorded,
    reconstructed: true,
  };
}

/** Shell-safe for display and copying. Nothing here is ever handed to a shell. */
function quoteIfNeeded(token: string): string {
  return /^[A-Za-z0-9_@%+=:,./-]+$/.test(token) ? token : `'${token.replace(/'/g, `'\\''`)}'`;
}
