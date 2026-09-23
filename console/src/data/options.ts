/**
 * One option table, mirroring both CLIs (§7).
 *
 * It drives the pipeline forms, the command-line preview and the input checks. The point of
 * having exactly one is that the console cannot quietly disagree with the programs it runs:
 * a flag renamed in either CLI shows up as a failing test here rather than as a form that
 * silently stops working.
 *
 * `tests/options.test.ts` runs each CLI's own `--help` and checks this table against it in
 * both directions — nothing here that the CLI does not have, nothing there that this does not
 * know about.
 *
 * **Defaults are the CLI's own**, read from its argument parser rather than from its help
 * text, because several of v1's options document a default the code does not use. Two are
 * flagged below.
 */

export type Side = "v1" | "v2";

export interface CliOption {
  readonly flag: string;
  /** A short form, where the CLI has one (`-p` for v1's `--parallel`). */
  readonly short?: string;
  /** False for a switch that takes no value. */
  readonly takesValue: boolean;
  /** The CLI's own default, as a string for display. Absent when there is none. */
  readonly default?: string;
  readonly choices?: readonly string[];
  /** The option's own help text, shown beside the field (§6). */
  readonly help: string;
  /** Something a person needs to know that the help text does not say. */
  readonly caveat?: string;
  /** Options set once per run and applied to both sides (§6.1). */
  readonly shared?: boolean;
  readonly required?: boolean;
}

export interface CliSubcommand {
  readonly side: Side;
  /** The subcommand as typed. */
  readonly name: string;
  /** Positional arguments, in order. */
  readonly positionals: readonly string[];
  readonly options: readonly CliOption[];
  /** Which console screen it belongs on (§4). */
  readonly screen: "pipeline" | "compare" | "runs" | "tools";
  readonly stage?: 1 | 2 | 3 | 4;
}

/** v2's decoding and output options, shared by all four stages. */
const V2_COMMON: readonly CliOption[] = [
  { flag: "--model", takesValue: true, required: true, help: "Model id to send to the provider." },
  {
    flag: "--temperature",
    takesValue: true,
    required: true,
    help: "Decoding temperature.",
    caveat:
      "Required on purpose: no run is recorded without the configuration that produced it being stated.",
  },
  { flag: "--seed", takesValue: true, default: "42", help: "Seed requested from the provider." },
  { flag: "--max-tokens", takesValue: true, default: "4096", help: "Completion token cap." },
  { flag: "--provider", takesValue: true, help: "Pin the upstream provider." },
  { flag: "--out", takesValue: true, help: "Where the run directory goes." },
  { flag: "--db", takesValue: true, help: "Metrics database to append to." },
  { flag: "--log-conversation", takesValue: false, help: "Record every message to conversation.jsonl." },
  { flag: "--plain", takesValue: false, help: "Line output instead of the live display." },
];

/** v1's generation options, shared by `generate` and `trace`. */
const V1_GENERATION: readonly CliOption[] = [
  {
    flag: "--skip",
    takesValue: true,
    shared: true,
    help: "Comma separated list of flags to ignore.",
    caveat: 'Set without a value it means "--version,--help,--interactive".',
  },
  { flag: "--max-arity", takesValue: true, default: "1", shared: true, help: "Maximum generated arity for repeatable args." },
  { flag: "--elaborate-relations", takesValue: false, help: "Use more elaborate file system relations." },
  {
    flag: "--stdin",
    takesValue: true,
    default: "simple",
    choices: ["simple", "varied", "split"],
    shared: true,
    help: "Degree of variation to stdin input.",
    caveat:
      "v1's annotator reaches `stateless` only from split-input traces, so a comparison at the default measures the trace configuration as much as the annotator.",
  },
  {
    flag: "--content",
    takesValue: true,
    default: "simple",
    choices: ["simple", "varied", "split"],
    shared: true,
    help: "Degree of variation to file content.",
  },
  { flag: "--max-count", takesValue: true, default: "4", shared: true, help: "Maximum optional flags per invocation." },
  { flag: "--path", takesValue: true, help: "Path to the syntax spec." },
];

export const SUBCOMMANDS: readonly CliSubcommand[] = [
  // ---- stage 1 ----
  {
    side: "v1",
    name: "syntax-spec",
    positionals: ["COMMAND"],
    screen: "pipeline",
    stage: 1,
    options: [
      {
        flag: "--fetch",
        takesValue: false,
        help: "Fetch a prewritten specification if possible.",
        caveat: "Reads v1's committed, hand-checked specification. Not a live model run.",
      },
      { flag: "--json", takesValue: false, help: "Serialize output as json." },
    ],
  },
  {
    side: "v2",
    name: "naive-llm",
    positionals: ["command"],
    screen: "pipeline",
    stage: 1,
    options: [
      { flag: "--docs", takesValue: true, help: "Documentation to read. Defaults to v1's man page." },
      { flag: "--prompt-variant", takesValue: true, default: "default", help: "Which wording of the prompt to send." },
      ...V2_COMMON,
    ],
  },

  // ---- stage 2 ----
  {
    side: "v1",
    name: "generate",
    positionals: ["COMMAND"],
    screen: "pipeline",
    stage: 2,
    options: [
      ...V1_GENERATION,
      {
        flag: "--number",
        takesValue: false,
        help: "Only print number of invocations.",
        caveat:
          "Never use this. It disagrees with what v1 actually prints on all 90 commands checked, and crashes on 14 including pwd.",
      },
      {
        flag: "--output",
        takesValue: true,
        help: "Path to store output file.",
        caveat:
          "Accepted and never used: cli/generate.py only prints. The help text's stated default is not written either.",
      },
      { flag: "--full", takesValue: false, help: "Generate the most elaborate invocations; overrides the other generation options." },
    ],
  },
  {
    side: "v2",
    name: "generate",
    positionals: ["command"],
    screen: "pipeline",
    stage: 2,
    options: [
      { flag: "--spec", takesValue: true, help: "Syntax spec to expand. Defaults to v1's committed spec." },
      { flag: "--max-arity", takesValue: true, default: "1", shared: true, help: "Maximum generated arity." },
      { flag: "--max-count", takesValue: true, default: "4", shared: true, help: "Maximum optional flags per invocation." },
      { flag: "--stdin", takesValue: true, default: "simple", choices: ["simple", "varied", "split"], shared: true, help: "Degree of variation to stdin input." },
      { flag: "--content", takesValue: true, default: "simple", choices: ["simple", "varied", "split"], shared: true, help: "Degree of variation to file content." },
      { flag: "--skip", takesValue: true, shared: true, help: "Comma separated list of flags to ignore." },
      { flag: "--max-turns", takesValue: true, default: "4", help: "Cap on model turns." },
      { flag: "--no-compare", takesValue: false, help: "Skip the comparison against v1's enumeration." },
      { flag: "--compare-timeout", takesValue: true, default: "300", help: "Seconds to allow v1's enumeration." },
      ...V2_COMMON,
    ],
  },

  // ---- stage 3 ----
  {
    side: "v1",
    name: "trace",
    positionals: ["COMMAND"],
    screen: "pipeline",
    stage: 3,
    options: [
      ...V1_GENERATION,
      { flag: "--prefix", takesValue: true, help: "Prefix the command, to use an alternate binary." },
      {
        flag: "--output",
        takesValue: true,
        help: "Directory to store trace files.",
        caveat:
          "The help says directory; cli/trace.py treats it as a FILE path. The console always passes a file inside the run's own folder.",
      },
      { flag: "--parallel", short: "-p", takesValue: true, help: "Run invocations in parallel." },
      { flag: "--pash", takesValue: false, help: "Use simplified specifications for PaSh." },
      { flag: "--posh", takesValue: false, help: "Use simplified specifications for POSH." },
      {
        flag: "--length-only",
        takesValue: false,
        help: "Calculate the number of executions needed.",
        caveat:
          "Counts executions including duplicates — 10,368 for mkdir at defaults, against 1,094 distinct invocations.",
      },
    ],
  },
  {
    side: "v2",
    name: "trace",
    positionals: ["command"],
    screen: "pipeline",
    stage: 3,
    options: [
      { flag: "--configs", takesValue: true, help: "Configurations to trace. Defaults to the most recent." },
      { flag: "--limit", takesValue: true, default: "5", help: "Maximum configurations to attempt." },
      { flag: "--max-turns", takesValue: true, default: "15", help: "Cap on model turns." },
      { flag: "--isolation", takesValue: true, default: "host", choices: ["host", "lima"], help: "Where the command is executed." },
      { flag: "--lima-instance", takesValue: true, help: "Which Lima VM to use." },
      { flag: "--keep-workspace", takesValue: false, help: "Leave the sandbox workspace in place afterwards." },
      ...V2_COMMON,
    ],
  },

  // ---- stage 4 ----
  {
    side: "v1",
    name: "annotate",
    positionals: ["FORMAT", "COMMAND"],
    screen: "pipeline",
    stage: 4,
    options: [
      { flag: "--input", takesValue: true, help: "Path to the trace file." },
      { flag: "--human", takesValue: false, help: "Output in a human readable way." },
      { flag: "--hide-trivial", takesValue: false, help: "Hide trivial or vacuous annotations." },
      { flag: "--include-all-traces", takesValue: false, help: "Use all traces, including those using files outside the sandbox." },
    ],
  },
  {
    side: "v2",
    name: "annotate",
    positionals: ["FORMAT", "command"],
    screen: "pipeline",
    stage: 4,
    options: [
      { flag: "--traces", takesValue: true, help: "Traces to annotate. Defaults to v1's." },
      { flag: "--max-turns", takesValue: true, default: "4", help: "Cap on model turns." },
      { flag: "--no-compare", takesValue: false, help: "Skip the comparison against v1's annotation." },
      { flag: "--v1-runner", takesValue: true, default: "host", choices: ["host", "lima"], help: "Where v1's annotator runs." },
      { flag: "--lima-instance", takesValue: true, help: "Which Lima VM to use." },
      ...V2_COMMON,
    ],
  },

  // ---- tools ----
  {
    side: "v1",
    name: "oracle",
    positionals: [],
    screen: "tools",
    options: [
      { flag: "--no-strat", takesValue: false, help: "Only output the matched args, without the strategy." },
      { flag: "--full-match-only", takesValue: false, help: "Only output full matches." },
      { flag: "--exclude", takesValue: true, help: "Strategies to exclude." },
      { flag: "--summary", takesValue: false, help: "Accumulate all results and deduplicate." },
    ],
  },
  {
    side: "v2",
    name: "score",
    positionals: ["command"],
    screen: "tools",
    options: [
      { flag: "--spec", takesValue: true, help: "Generated spec file to score." },
      { flag: "--reference", takesValue: true, default: "v1-specs", choices: ["v1-specs", "ground-truth"], help: "What to score against." },
      { flag: "--reference-path", takesValue: true, help: "Explicit reference spec file." },
      { flag: "--transform", takesValue: true, help: "Rename map applied to the reference." },
      { flag: "--cmp-specs", takesValue: false, help: "Also run v1's own eval/cmp_specs.py." },
      { flag: "--self-test", takesValue: false, help: "Score each committed exemplar against itself." },
      { flag: "--json", takesValue: false, help: "Print the full record as JSON." },
      { flag: "--plain", takesValue: false, help: "Line output." },
    ],
  },
  {
    side: "v2",
    name: "report",
    positionals: ["campaign_id"],
    screen: "compare",
    options: [
      { flag: "--ledger-root", takesValue: true, default: "eval/campaigns", help: "Where campaign ledgers live." },
      {
        flag: "--rescore",
        takesValue: true,
        choices: ["stage-default", "v1-specs", "ground-truth"],
        help: "Re-derive every score from the saved run artifacts with the current scorer.",
        caveat: "Read-only: it recomputes in memory and does not rewrite the ledger.",
      },
      { flag: "--reference-traces", takesValue: true, help: "Where v1's reference traces live, with {command} substituted." },
      { flag: "--json", takesValue: false, help: "Print the full report as JSON." },
      { flag: "--out", takesValue: true, help: "Write the report here." },
      { flag: "--plain", takesValue: false, help: "Line output." },
    ],
  },
];

export function subcommand(side: Side, name: string): CliSubcommand | undefined {
  return SUBCOMMANDS.find((entry) => entry.side === side && entry.name === name);
}

/** Options set once per run and applied to both sides (§6.1). */
export function sharedOptions(): CliOption[] {
  const seen = new Map<string, CliOption>();
  for (const entry of SUBCOMMANDS) {
    for (const option of entry.options) {
      if (option.shared && !seen.has(option.flag)) seen.set(option.flag, option);
    }
  }
  return [...seen.values()];
}
