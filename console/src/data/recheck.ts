/**
 * Re-checking a finding's numbers against today's scorer.
 *
 * This is the point of keeping findings as structured files. A number written into a document
 * is inert: nothing notices when the scorer that produced it changes, or when the runs behind
 * it are deleted. A number recorded with its campaign, its metric, its method and its
 * denominator can be recomputed and compared, and that check would have caught both errors the
 * parity study has already had to correct in public.
 *
 * **Everything here re-derives through the harness, never through a second implementation.**
 * `caruca-v2 report --rescore` recomputes a campaign's scores from the saved run artifacts
 * with the current scorer; `caruca-v2 score` does the same for one stage-1 specification. The
 * console's own comparison code is used for exactly one case, stated below.
 *
 * `report --rescore` is read-only - it recomputes in memory and prints. It does not rewrite
 * the ledger, so re-checking a finding cannot alter the evidence it is checking.
 */
import { loadCampaignReport, runCarucaV2, HarnessError } from "./harness.js";
import { v1Root } from "./paths.js";
import { buildMatrix, summarizeStages } from "./compare.js";
import { loadCampaignSet } from "./parityCampaigns.js";
import { compareEvidence, type Evidence, type RecheckResult } from "./findings.js";
import type { Stage } from "./schema.js";

/**
 * How a recorded number is recomputed.
 *
 * Written into the finding file so the recipe travels with the number. A finding whose
 * evidence has no recipe can still be read; it simply cannot be checked, and says so.
 */
export type RecheckRecipe =
  | {
      /**
       * A campaign-level metric: the mean of one metric across an arm's scored cells,
       * re-derived from the run artifacts with today's scorer.
       */
      readonly kind: "campaign_metric";
      readonly campaign: string;
      /** The metric's real name, as the scorer records it - not the report's slot name. */
      readonly metric: string;
      /** The comparison method, which says which report slot holds that metric. */
      readonly method: string;
      /** Which arm, when the campaign has more than one. Defaults to the only one. */
      readonly arm?: string;
      /** Stage-3 rescoring needs to be told where v1's reference traces are. */
      readonly referenceTraces?: string;
    }
  | {
      /**
       * A pooled count over a count, like stage 4's "25 of 77".
       *
       * `report` has no such figure - it reports per-metric distributions, and averaging a
       * count is meaningless - so this one is computed by the console's own matrix code from
       * the ledger **as recorded**, not rescored. The result says so, because "matches" under
       * a weaker check is a weaker statement.
       */
      readonly kind: "campaign_pooled";
      readonly campaign: string;
      readonly stage: Stage;
    }
  | {
      /** One stage-1 specification, re-scored against its reference. */
      readonly kind: "spec_score";
      readonly command: string;
      /** The generated spec, relative to the repo root. */
      readonly specPath: string;
      readonly reference?: "v1-specs" | "ground-truth";
      readonly metric: string;
    };

export interface RecheckOutcome extends RecheckResult {
  /** What was actually run or read, so the check can be repeated by hand. */
  readonly how: string;
  /**
   * Whether the number was genuinely re-derived with today's scorer, or only re-read from
   * what was recorded at run time. A match under the weaker check is a weaker statement and
   * is never presented as the stronger one.
   */
  readonly rederived: boolean;
  readonly seconds: number;
}

/**
 * Which metric each comparison method reports, in the order it declares them.
 *
 * Mirrored from `harness/methods.py`, and needed because of a quirk in the report's JSON:
 * `Arm.as_dict` emits its two metric slots under the fixed names `f1` and
 * `exact_argument_rate` **whatever stage the campaign is**, while filling them from the
 * method's own list. So `report p1_generate --json` reports invocation recall under the key
 * `exact_argument_rate`, and `report p1_trace --json` reports core recall under it.
 *
 * Reading those keys at face value would attach a stage-1 name to a stage-2 number. This table
 * turns a real metric name back into the slot that actually holds it.
 *
 * Keep in step with `methods.py` if a method's metric list changes.
 */
const METHOD_METRICS: Record<string, readonly string[]> = {
  q2_syntax_diff: ["f1", "exact_argument_rate", "precision", "recall"],
  invocation_set_diff: ["f1", "recall", "precision"],
  config_env_diff: ["env_agreement_rate"],
  trace_recovery_diff: ["core.micro.f1", "core.micro.recall", "core.micro.precision"],
  annotation_diff: [
    "rates.fully_agreeing",
    "rates.pclass",
    "agreement.fully_agreeing",
    "agreement.pclass",
    "agreement.comparable",
  ],
  measured_cost: ["cost_usd"],
};

/** The two keys the report always uses, in slot order. */
const REPORT_SLOTS = ["f1", "exact_argument_rate"] as const;

/**
 * The report key that actually carries `metric` for a campaign scored by `method`.
 *
 * Null when the metric is not in one of the two slots the report publishes - the report
 * simply does not carry it, and saying so beats reading a neighbouring number.
 */
export function reportKeyFor(method: string, metric: string): string | null {
  const declared = METHOD_METRICS[method];
  if (!declared) return REPORT_SLOTS.includes(metric as never) ? metric : null;
  const slot = declared.indexOf(metric);
  if (slot < 0 || slot >= REPORT_SLOTS.length) return null;
  return REPORT_SLOTS[slot]!;
}

function numberAt(source: unknown, path: string): number | null {
  let current: unknown = source;
  for (const part of path.split(".")) {
    if (current === null || typeof current !== "object") return null;
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "number" && Number.isFinite(current) ? current : null;
}

/**
 * A metric's mean for one arm of a rescored campaign.
 *
 * The metric key can itself contain dots (`core.micro.f1`), which is why the arm's metric
 * object is looked up whole rather than by walking a dotted path.
 */
function armMetricMean(arm: Record<string, unknown>, metric: string): number | null {
  const entry = arm[metric];
  if (entry === undefined) return null;
  if (typeof entry === "number") return entry;
  return numberAt(entry, "mean");
}

/**
 * Expand `{CARUCA_V1_ROOT}` in a recipe's path.
 *
 * Two machines are in play and neither path is canonical, so a recipe that hardcoded one would
 * stop working on the other. `{command}` is left alone: the harness substitutes that itself.
 */
function expandPath(pattern: string): string {
  if (!pattern.includes("{CARUCA_V1_ROOT}")) return pattern;
  return pattern.replace("{CARUCA_V1_ROOT}", v1Root());
}

async function recheckCampaignMetric(
  evidence: Evidence,
  recipe: Extract<RecheckRecipe, { kind: "campaign_metric" }>,
): Promise<RecheckOutcome> {
  const startedAt = Date.now();
  const how = `caruca-v2 report ${recipe.campaign} --rescore --json`;

  try {
    const { report } = await loadCampaignReport(recipe.campaign, {
      rescore: true,
      ...(recipe.referenceTraces
        ? { referenceTraces: expandPath(recipe.referenceTraces) }
        : {}),
    });

    const arm = recipe.arm
      ? report.arms.find((candidate) => candidate.arm === recipe.arm)
      : report.arms[0];

    if (!arm) {
      return {
        ...compareEvidence(evidence, null, `no arm ${recipe.arm ?? "(first)"} in ${recipe.campaign}`),
        how,
        rederived: false,
        seconds: (Date.now() - startedAt) / 1000,
      };
    }

    const key = reportKeyFor(recipe.method, recipe.metric);
    if (!key) {
      return {
        ...compareEvidence(
          evidence,
          null,
          `report publishes only the first two metrics of ${recipe.method}; ` +
            `${recipe.metric} is not among them`,
        ),
        how,
        rederived: false,
        seconds: (Date.now() - startedAt) / 1000,
      };
    }

    const value = armMetricMean(arm as Record<string, unknown>, key);
    return {
      ...compareEvidence(
        evidence,
        value,
        value === null
          ? `${recipe.campaign} reports no value in the slot that holds ${recipe.metric} ` +
            `(read as "${key}")`
          : null,
      ),
      how: `${how}  →  ${recipe.metric} (reported under "${key}")`,
      rederived: value !== null,
      seconds: (Date.now() - startedAt) / 1000,
    };
  } catch (cause) {
    const reason =
      cause instanceof HarnessError
        ? `${cause.message}${cause.stderr ? ` — ${cause.stderr.split("\n")[0]}` : ""}`
        : (cause as Error).message;
    return {
      ...compareEvidence(evidence, null, reason),
      how,
      rederived: false,
      seconds: (Date.now() - startedAt) / 1000,
    };
  }
}

function recheckCampaignPooled(
  evidence: Evidence,
  recipe: Extract<RecheckRecipe, { kind: "campaign_pooled" }>,
): RecheckOutcome {
  const startedAt = Date.now();
  const how = `pooled from ${recipe.campaign}'s ledger as recorded (not rescored)`;

  const set = loadCampaignSet([recipe.campaign]);
  if (set.absent.length > 0) {
    return {
      ...compareEvidence(evidence, null, `${recipe.campaign} is not on this machine`),
      how,
      rederived: false,
      seconds: (Date.now() - startedAt) / 1000,
    };
  }

  const summary = summarizeStages(buildMatrix(set.rows)).find(
    (candidate) => candidate.stage === recipe.stage,
  );

  return {
    ...compareEvidence(
      evidence,
      summary?.mean ?? null,
      summary ? null : `no ${recipe.stage} cells in ${recipe.campaign}`,
    ),
    how,
    // Honest: the ledger's recorded scores were re-pooled, not recomputed from artifacts.
    rederived: false,
    seconds: (Date.now() - startedAt) / 1000,
  };
}

async function recheckSpecScore(
  evidence: Evidence,
  recipe: Extract<RecheckRecipe, { kind: "spec_score" }>,
): Promise<RecheckOutcome> {
  const startedAt = Date.now();
  const args = [
    "score",
    recipe.command,
    "--spec",
    recipe.specPath,
    "--reference",
    recipe.reference ?? "v1-specs",
    "--json",
    "--plain",
  ];
  const how = `caruca-v2 ${args.join(" ")}`;

  try {
    const result = await runCarucaV2(args);
    const parsed = JSON.parse(result.stdout) as Record<string, unknown>;
    const value =
      typeof parsed[recipe.metric] === "number"
        ? (parsed[recipe.metric] as number)
        : numberAt(parsed, recipe.metric);
    return {
      ...compareEvidence(
        evidence,
        value,
        value === null ? `the scorer reported no ${recipe.metric}` : null,
      ),
      how,
      rederived: value !== null,
      seconds: (Date.now() - startedAt) / 1000,
    };
  } catch (cause) {
    return {
      ...compareEvidence(evidence, null, (cause as Error).message),
      how,
      rederived: false,
      seconds: (Date.now() - startedAt) / 1000,
    };
  }
}

/**
 * Read a recipe off a piece of evidence.
 *
 * Validated loosely on purpose: the recipe comes from a hand-editable Markdown file, and a
 * malformed one should make that number un-checkable rather than make the whole finding
 * unreadable.
 */
export function recipeOf(evidence: Evidence): RecheckRecipe | null {
  const raw = evidence.recheck;
  if (!raw || typeof raw !== "object") return null;
  const kind = (raw as Record<string, unknown>)["kind"];
  if (kind === "campaign_metric" || kind === "campaign_pooled" || kind === "spec_score") {
    return raw as unknown as RecheckRecipe;
  }
  return null;
}

/** Re-derive one recorded number and say whether it still holds. */
export async function recheckEvidence(
  evidence: Evidence,
  recipe: RecheckRecipe | null,
): Promise<RecheckOutcome> {
  if (!recipe) {
    return {
      ...compareEvidence(
        evidence,
        null,
        "no recipe is recorded for this number, so it cannot be recomputed",
      ),
      how: "—",
      rederived: false,
      seconds: 0,
    };
  }

  switch (recipe.kind) {
    case "campaign_metric":
      return recheckCampaignMetric(evidence, recipe);
    case "campaign_pooled":
      return recheckCampaignPooled(evidence, recipe);
    case "spec_score":
      return recheckSpecScore(evidence, recipe);
  }
}

/**
 * Re-check every number in a finding.
 *
 * Runs them one after another rather than in parallel: each `report --rescore` re-derives a
 * whole campaign from its run artifacts, and several at once on this Mac only makes them all
 * slower.
 */
export async function recheckAll(
  items: { evidence: Evidence; recipe: RecheckRecipe | null }[],
): Promise<RecheckOutcome[]> {
  const results: RecheckOutcome[] = [];
  for (const item of items) results.push(await recheckEvidence(item.evidence, item.recipe));
  return results;
}
