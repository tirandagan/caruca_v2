/**
 * The shapes on disk, mirrored from `src/caruca_v2/telemetry.py`.
 *
 * These parse evidence a paper revision is argued from, so the rule from the Python side
 * carries over: a value we could not obtain is an error, never a default. Nothing here fills a
 * missing token count with zero. Where a field is genuinely optional on disk it is optional
 * here too, and callers are made to handle the absence.
 *
 * `passthrough()` is deliberate wherever the Python model allows extra keys: a stage that
 * records a new field must not make older readers throw, and `checks` is explicitly open-ended
 * on the Python side.
 */
import { z } from "zod";

export const STAGES = ["syntax_spec", "generate", "trace", "annotate"] as const;
export type Stage = (typeof STAGES)[number];

export const COMPONENTS = ["baseline", "naive_llm", "tool_augmentation", "llm_pipeline"] as const;
export const CONDITIONS = ["plain", "augmented"] as const;

/** Every decoding parameter actually sent. Open, because a stage may add one. */
export const decodingParamsSchema = z
  .object({ temperature: z.number(), max_tokens: z.number().int() })
  .passthrough();

export const telemetryRecordSchema = z.object({
  run_id: z.string(),
  command: z.string(),
  component: z.enum(COMPONENTS),
  condition: z.enum(CONDITIONS),
  stage: z.enum(STAGES),
  model_id: z.string(),
  prompt_tokens: z.number().int(),
  completion_tokens: z.number().int(),
  cost_usd: z.number(),
  wall_clock_seconds: z.number(),
  seed: z.number().int().nullable(),
  prompt_hash: z.string(),
  /**
   * Phase 0(a): this is the RUN's start time, repeated on every turn - not the turn's own
   * time. All ten turns of 2026-09-14T163935Z_cat_a3ea2a72 read 16:39:35. Never subtract two
   * of these to get a duration; accumulate `wall_clock_seconds` instead.
   */
  timestamp: z.string(),
  decoding_params: decodingParamsSchema,
  turn: z.number().int().default(0),
  config_index: z.number().int().nullable().default(null),
});
export type TelemetryRecord = z.infer<typeof telemetryRecordSchema>;

export const validationReportSchema = z.object({
  passed: z.boolean(),
  /** False means v1's environment could not be reached - a different finding from "v1 said no". */
  available: z.boolean(),
  error: z.string().nullable().default(null),
  traceback: z.string().nullable().default(null),
  elements: z.number().int().nullable().default(null),
});
export type ValidationReport = z.infer<typeof validationReportSchema>;

export const runManifestSchema = z
  .object({
    run_id: z.string(),
    timestamp: z.string(),
    command: z.string(),
    component: z.enum(COMPONENTS),
    condition: z.enum(CONDITIONS),
    stage: z.enum(STAGES),
    status: z.enum(["ok", "failed"]),
    failure_reason: z.string().nullable().default(null),

    model_requested: z.string(),
    model_reported: z.string(),
    provider: z.string().nullable().default(null),
    seed: z.number().int().nullable(),
    seed_honored: z.boolean(),
    decoding_params: decodingParamsSchema,
    response_format: z.string(),

    prompt_hash: z.string(),
    prompt_files: z.array(z.string()),
    prompt_variant: z.string().default("default"),
    prompt_system: z.string(),
    prompt_user: z.string(),
    raw_response: z.string(),

    finish_reason: z.string().nullable().default(null),
    output_truncated: z.boolean().default(false),
    turns: z.number().int().default(1),
    output_paths: z.array(z.string()).default([]),
    validation: validationReportSchema.nullable().default(null),

    /** Stage-specific findings. Open by design on the Python side; kept open here. */
    checks: z.record(z.unknown()).default({}),

    prompt_tokens: z.number().int(),
    completion_tokens: z.number().int(),
    cost_usd: z.number(),
    wall_clock_seconds: z.number(),

    /** Everything the stage was configured with. Phase 0(b): this is what a command line is rebuilt from. */
    inputs: z.record(z.unknown()).default({}),
  })
  .passthrough();
export type RunManifest = z.infer<typeof runManifestSchema>;

/** One scored cell in a campaign ledger (`eval/campaigns/<id>/ledger.jsonl`). */
export const ledgerRowSchema = z
  .object({
    cell_key: z.string(),
    campaign_id: z.string(),
    stage: z.enum(STAGES),
    command: z.string(),
    model: z.string(),
    temperature: z.number(),
    sample: z.number().int(),
    prompt_variant: z.string().default("default"),
    attempts: z.number().int(),
    run_id: z.string().nullable().default(null),
    run_dir: z.string().nullable().default(null),
    status: z.string(),
    validation_passed: z.boolean().nullable().default(null),

    /**
     * Cost and tokens are absent on a cell that errored before anything was billed - a
     * request rejected for exceeding the context window, for instance.
     *
     * They are nullable rather than defaulted to zero, and required rather than optional in
     * meaning: null says "this cell never billed", which is a different statement from "this
     * cell cost nothing to run". Six of the 27 cells in `p1_annotate` are in this state.
     *
     * Making these required is what the first version of this schema did, and it rejected
     * those six rows outright - which silently removed every failed `rm` and `tee` cell from
     * the comparison matrix and made stage 4 look like it had nine working commands.
     */
    cost_usd: z.number().nullable().default(null),
    prompt_tokens: z.number().int().nullable().default(null),
    completion_tokens: z.number().int().nullable().default(null),

    /** Why the cell errored, where it did. Present instead of a score, not alongside one. */
    error: z.string().nullable().default(null),

    /** The scorer's output. Shape is the method's business, not this layer's. */
    score: z.record(z.unknown()).nullable().default(null),
  })
  .passthrough();
export type LedgerRow = z.infer<typeof ledgerRowSchema>;

export const campaignSummarySchema = z
  .object({
    campaign_id: z.string(),
    cells_total: z.number().int(),
    completed: z.number().int(),
    skipped_resumed: z.number().int(),
    failed_content: z.number().int(),
    errored: z.number().int(),
    transport_retries: z.number().int(),
    cost_usd: z.number(),
    prompt_tokens: z.number().int(),
    completion_tokens: z.number().int(),
    stopped_reason: z.string().nullable().default(null),
    by_model: z.record(z.unknown()).default({}),
  })
  .passthrough();
export type CampaignSummary = z.infer<typeof campaignSummarySchema>;
