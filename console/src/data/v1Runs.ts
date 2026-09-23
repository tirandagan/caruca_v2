/**
 * v1's run records, in `eval/v1_runs/<run_id>/`.
 *
 * v1 writes no event log of its own - that gap is task 005's to close - so for any v1 run the
 * console starts, this record IS the evidence. It is written by the console, never by v1.
 *
 * Two rules from decision 7 are encoded in the shape:
 *
 *   1. **v1 runs exactly as the parity study ran it.** The record keeps the argument list as
 *      given, the working directory, which virtual environment, and whether it ran on the Mac
 *      or inside the Lima VM - because "the same kind of run the measurements came from" is
 *      only checkable if all of that was written down.
 *   2. **v1 never writes into its own checkout.** Every output path is inside the run's own
 *      folder. `$CARUCA_V1_ROOT/caruca/outputs/` holds the parity study's traces and is
 *      gitignored in v1, so anything overwritten there cannot be restored.
 *
 * Unlike a v2 manifest, `argv` here is **recorded, not reconstructed** - the console knows
 * exactly what it spawned. That difference is carried through to the screens, which label a v2
 * command line "reconstructed" and a v1 one not.
 *
 * What v1 does not record shows as absent rather than zero: `perStepSeconds` and the LLM
 * step's token counts stay null until task 005 adds them, and `null` here must never be
 * rendered as `0`.
 */
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";
import { repoPaths } from "./paths.js";

export class V1RunUnreadableError extends Error {}

export const V1_MANIFEST_NAME = "manifest.json";
export const V1_RECORDING_NAME = "terminal.cast";

export const v1RunManifestSchema = z
  .object({
    run_id: z.string(),
    /** Which of v1's subcommands ran. `syntax-spec` is the LLM step. */
    subcommand: z.enum(["syntax-spec", "generate", "trace", "annotate", "oracle"]),
    command: z.string(),
    /** For `annotate`, the consumer format: pash, posh, sash or shellcheck. */
    format: z.string().nullable().default(null),

    /** Exactly what was spawned. Recorded, never rebuilt. */
    argv: z.array(z.string()),
    /** The directory it ran from - `$CARUCA_V1_ROOT/caruca` for every parity-study form. */
    cwd: z.string(),
    /** `.venv`, or `.venv-llm` for `syntax-spec`, which the plain venv cannot import. */
    venv: z.string(),
    where: z.enum(["mac", "lima"]),
    lima_instance: z.string().nullable().default(null),
    /**
     * The one form that needs a shell: `annotate` inside the VM, which `v1.py` already passes
     * to `sh -lc`. Recorded so a reader can see it was deliberate and copied, not invented.
     */
    used_shell: z.boolean().default(false),

    v1_commit: z.string(),
    /** Names only. A value is never written into a run record. */
    env_var_names: z.array(z.string()).default([]),

    started_at: z.string(),
    ended_at: z.string().nullable().default(null),
    exit_code: z.number().int().nullable().default(null),
    machine: z.string(),
    /** v1's progress bar sizes itself to the width, so a replay needs the original size. */
    terminal_size: z.object({ cols: z.number().int(), rows: z.number().int() }),

    /**
     * Whether another run was going at the same time.
     *
     * Both sides then share the Mac's processors, and the VM when both are tracing, so
     * wall-clock times from such runs are flagged and left out of timing comparisons (§6.3).
     */
    concurrent_with: z.array(z.string()).default([]),

    /** Every file the run wrote. All inside this folder, by construction. */
    output_paths: z.array(z.string()).default([]),

    /**
     * Tokens and cost for a live stage-1 run, as the OpenRouter meter reported them.
     *
     * Null for every other subcommand, and for a stage-1 run that used v1's archived output.
     * Null means "not recorded", never zero - which is also what it means for every v1 run
     * made outside the console.
     */
    llm_prompt_tokens: z.number().int().nullable().default(null),
    llm_completion_tokens: z.number().int().nullable().default(null),
    llm_cost_usd: z.number().nullable().default(null),
    llm_model_reported: z.string().nullable().default(null),

    /** Per-step timing inside the run. Task 005's job; null until then. */
    per_step_seconds: z.record(z.number()).nullable().default(null),
  })
  .passthrough();
export type V1RunManifest = z.infer<typeof v1RunManifestSchema>;

export interface LoadedV1Run {
  readonly runId: string;
  readonly dir: string;
  readonly manifest: V1RunManifest;
  readonly recordingPath: string | null;
  /** Ready to copy into a terminal. This one was captured, so it is exact. */
  readonly display: string;
}

function quoteIfNeeded(token: string): string {
  return /^[A-Za-z0-9_@%+=:,./-]+$/.test(token) ? token : `'${token.replace(/'/g, `'\\''`)}'`;
}

export function loadV1Run(dir: string): LoadedV1Run {
  const path = join(dir, V1_MANIFEST_NAME);
  let json: unknown;
  try {
    json = JSON.parse(readFileSync(path, "utf8"));
  } catch (cause) {
    throw new V1RunUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }
  const parsed = v1RunManifestSchema.safeParse(json);
  if (!parsed.success) {
    throw new V1RunUnreadableError(
      `${path} does not match the v1 run record shape: ${parsed.error.issues
        .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
        .join("; ")}`,
    );
  }
  const recording = join(dir, V1_RECORDING_NAME);
  return {
    runId: parsed.data.run_id,
    dir,
    manifest: parsed.data,
    recordingPath: existsSync(recording) ? recording : null,
    display: parsed.data.argv.map(quoteIfNeeded).join(" "),
  };
}

export interface ListV1RunsResult {
  readonly runs: LoadedV1Run[];
  readonly unreadable: { dir: string; reason: string }[];
}

/** Every v1 run the console has recorded. Empty until Phase 5 starts one. */
export function listV1Runs(root = repoPaths().v1Runs): ListV1RunsResult {
  const runs: LoadedV1Run[] = [];
  const unreadable: { dir: string; reason: string }[] = [];
  if (!existsSync(root)) return { runs, unreadable };

  for (const name of readdirSync(root).sort()) {
    const dir = join(root, name);
    try {
      if (!statSync(dir).isDirectory()) continue;
      runs.push(loadV1Run(dir));
    } catch (cause) {
      unreadable.push({ dir: name, reason: (cause as Error).message });
    }
  }
  runs.sort((a, b) => b.runId.localeCompare(a.runId));
  return { runs, unreadable };
}

export function writeV1Manifest(dir: string, manifest: V1RunManifest): string {
  const parsed = v1RunManifestSchema.parse(manifest);
  mkdirSync(dir, { recursive: true });
  const path = join(dir, V1_MANIFEST_NAME);
  writeFileSync(path, `${JSON.stringify(parsed, null, 2)}\n`);
  return path;
}
