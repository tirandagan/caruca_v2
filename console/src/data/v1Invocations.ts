/**
 * v1's argument lists, defined in one place (§7), in exactly the forms the parity study used.
 *
 * Decision 7: a v1 run started from the console must be the same kind of run the measurements
 * came from. That is only checkable if there is one definition of each form, so this is it —
 * `tests/v1Invocations.test.ts` checks these against §3's table, and every v1 run the console
 * starts is built here.
 *
 * Two rules are structural rather than advisory:
 *
 *   1. **v1 never writes into its own checkout.** `$CARUCA_V1_ROOT/caruca/outputs/` holds the
 *      parity study's traces and annotations, is gitignored in v1, and cannot be restored.
 *      v1's `trace` and `annotate` default to it, relative to where they run — so an output
 *      path is always passed explicitly, always inside the run's own folder, and
 *      `refuseUnsafeOutput` rejects anything else.
 *   2. **Nothing is built by string interpolation into a shell.** Every form is an argument
 *      list. The one exception is `annotate` inside the VM, which `v1.py` already passes to
 *      `sh -lc`; the console copies that form rather than inventing one, and quotes each part.
 */
import { join, resolve, sep } from "node:path";
import { v1Root, v1ProtectedOutputs, repoPaths } from "./paths.js";

export class UnsafeV1OutputError extends Error {}

/** v1's two virtualenvs. `syntax-spec` works only in the second (DSPy 3.x broke the first). */
export const VENV_DEFAULT = ".venv";
export const VENV_LLM = ".venv-llm";

/** v1's entry point inside the Lima VM, as `v1.py::LIMA_V1_PYTHON` has it. */
export const LIMA_V1_CARUCA = "~/caruca-venv/bin/caruca";

export type V1Subcommand = "syntax-spec" | "generate" | "trace" | "annotate" | "oracle";
export type Where = "mac" | "lima";

export interface V1Invocation {
  readonly subcommand: V1Subcommand;
  readonly command: string;
  readonly argv: string[];
  /** Where it runs. The parity study ran `generate` on the Mac and the rest in the VM. */
  readonly where: Where;
  readonly limaInstance: string | null;
  /** v1 is always run from its own package directory. */
  readonly cwd: string;
  readonly venv: string;
  /** True only for the `annotate`-in-VM form, which v1.py already passes to `sh -lc`. */
  readonly usesShell: boolean;
  /** Where v1 was told to write, when it was told at all. Always inside the run's folder. */
  readonly outputPath: string | null;
}

/** v1's package directory: where every parity-study form was run from. */
export function v1Cwd(root = v1Root()): string {
  return join(root, "caruca");
}

/** v1's entry point on the Mac. */
export function v1Executable(venv: string = VENV_DEFAULT, root = v1Root()): string {
  return join(v1Cwd(root), venv, "bin", "caruca");
}

/**
 * Refuse any output path that would land inside v1's checkout.
 *
 * The third of §9's Phase 4 tests. The comparison is on resolved paths with a trailing
 * separator, so neither `..` nor a path that merely starts with the same characters
 * (`outputs-backup`) can slip past.
 */
export function refuseUnsafeOutput(path: string, root = v1Root()): string {
  const resolved = resolve(path);
  const protectedDir = resolve(v1ProtectedOutputs(root));
  const checkout = resolve(root);

  if (resolved === protectedDir || resolved.startsWith(protectedDir + sep)) {
    throw new UnsafeV1OutputError(
      `${resolved} is inside v1's own outputs directory. That folder holds the parity study's ` +
        `traces and annotations, is gitignored in v1, and cannot be restored. ` +
        `v1 output must go inside the run's own folder.`,
    );
  }
  if (resolved === checkout || resolved.startsWith(checkout + sep)) {
    throw new UnsafeV1OutputError(
      `${resolved} is inside v1's checkout. The console never writes there.`,
    );
  }
  return resolved;
}

/** The folder a v1 run writes into: `eval/v1_runs/<run_id>/`. */
export function v1RunDir(runId: string): string {
  return join(repoPaths().v1Runs, runId);
}

/** Shell-quote one argument. Used only for the `sh -lc` form v1.py already requires. */
function quote(token: string): string {
  return /^[A-Za-z0-9_@%+=:,./~-]+$/.test(token) ? token : `'${token.replace(/'/g, `'\\''`)}'`;
}

function limaPrefix(instance: string): string[] {
  return ["limactl", "shell", instance, "--"];
}

export interface GenerationBounds {
  readonly maxArity?: number;
  readonly maxCount?: number;
  readonly stdin?: string;
  readonly content?: string;
  readonly skip?: string;
  readonly elaborateRelations?: boolean;
}

function boundsArgs(bounds: GenerationBounds): string[] {
  const args: string[] = [];
  if (bounds.maxArity !== undefined) args.push("--max-arity", String(bounds.maxArity));
  if (bounds.maxCount !== undefined) args.push("--max-count", String(bounds.maxCount));
  if (bounds.stdin !== undefined) args.push("--stdin", bounds.stdin);
  if (bounds.content !== undefined) args.push("--content", bounds.content);
  if (bounds.skip !== undefined) args.push("--skip", bounds.skip);
  if (bounds.elaborateRelations) args.push("--elaborate-relations");
  return args;
}

/**
 * `generate`: on the Mac, from v1's package directory.
 *
 * No `--output`: v1's `generate` accepts the flag and never uses it — `cli/generate.py` only
 * prints. The console captures stdout into the run's folder instead.
 */
export function v1Generate(
  command: string,
  bounds: GenerationBounds = {},
  options: { root?: string; lengthOnly?: boolean } = {},
): V1Invocation {
  const root = options.root ?? v1Root();
  return {
    subcommand: "generate",
    command,
    argv: [v1Executable(VENV_DEFAULT, root), "generate", command, ...boundsArgs(bounds)],
    where: "mac",
    limaInstance: null,
    cwd: v1Cwd(root),
    venv: VENV_DEFAULT,
    usesShell: false,
    outputPath: null,
  };
}

/**
 * `trace`: inside the Lima VM, under v1's default isolation.
 *
 * `CARUCA_ISOLATION_METHOD` is left unset, which means v1's own default of `try`. That is what
 * the parity study ran under, and setting it would be running a different v1.
 *
 * `--output` takes a *file* path despite its help text saying directory (`cli/trace.py`).
 */
export function v1Trace(
  command: string,
  outputFile: string,
  bounds: GenerationBounds = {},
  options: { root?: string; limaInstance?: string; lengthOnly?: boolean } = {},
): V1Invocation {
  const root = options.root ?? v1Root();
  const instance = options.limaInstance ?? "caruca";
  const output = refuseUnsafeOutput(outputFile, root);

  const inner = [
    LIMA_V1_CARUCA,
    "trace",
    command,
    ...boundsArgs(bounds),
    ...(options.lengthOnly ? ["--length-only"] : ["--output", output]),
  ];

  return {
    subcommand: "trace",
    command,
    argv: [...limaPrefix(instance), ...inner],
    where: "lima",
    limaInstance: instance,
    cwd: v1Cwd(root),
    venv: LIMA_V1_CARUCA,
    usesShell: false,
    outputPath: options.lengthOnly ? null : output,
  };
}

/**
 * `annotate`: inside the Lima VM, through `sh -lc`.
 *
 * The one form that needs a shell, because that is what `v1.py::reference_annotation` already
 * does. The console copies it rather than inventing a different one — a v1 run that differs
 * from how the measurements were taken is not the run decision 7 asks for.
 *
 * On macOS this cannot run on the host at all: v1's `tracer/data.py` resolves `/tmp` to
 * `/private/tmp` and then fails a `relative_to` against the sandbox path.
 */
export function v1Annotate(
  format: string,
  command: string,
  inputFile: string,
  options: { root?: string; limaInstance?: string } = {},
): V1Invocation {
  const root = options.root ?? v1Root();
  const instance = options.limaInstance ?? "caruca";
  const input = refuseUnsafeOutput(inputFile, root);

  const inner = [LIMA_V1_CARUCA, "annotate", format, command, "--input", input]
    .map(quote)
    .join(" ");

  return {
    subcommand: "annotate",
    command,
    argv: [...limaPrefix(instance), "sh", "-lc", inner],
    where: "lima",
    limaInstance: instance,
    cwd: v1Cwd(root),
    venv: LIMA_V1_CARUCA,
    usesShell: true,
    outputPath: null,
  };
}

/**
 * `syntax-spec`: v1's LLM step, on the Mac, from `.venv-llm`.
 *
 * The plain `.venv` copy dies at import against DSPy 3.3.1, so this form is the only one that
 * can run. With `--fetch` it reads v1's committed specification and calls no model at all.
 */
export function v1SyntaxSpec(
  command: string,
  options: { root?: string; fetch?: boolean; json?: boolean } = {},
): V1Invocation {
  const root = options.root ?? v1Root();
  return {
    subcommand: "syntax-spec",
    command,
    argv: [
      v1Executable(options.fetch ? VENV_DEFAULT : VENV_LLM, root),
      "syntax-spec",
      command,
      ...(options.fetch ? ["--fetch"] : []),
      ...(options.json ? ["--json"] : []),
    ],
    // `--fetch` only reads a committed file, so the working venv is fine for it.
    where: "mac",
    limaInstance: null,
    cwd: v1Cwd(root),
    venv: options.fetch ? VENV_DEFAULT : VENV_LLM,
    usesShell: false,
    outputPath: null,
  };
}

/** Ready to copy into a terminal. */
export function displayInvocation(invocation: V1Invocation): string {
  return invocation.argv.map(quote).join(" ");
}
