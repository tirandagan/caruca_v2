/**
 * The comparison matrix: one row per command, one column per stage (§6.4).
 *
 * Built from the campaign ledgers directly, because a matrix has to be fast enough to filter
 * and the ledgers already hold every scored cell. The *aggregate* numbers still come from the
 * harness (`harness.ts`), so nothing here becomes a second opinion on a published figure.
 *
 * Two rules the design system and the project both insist on, encoded here rather than left to
 * each screen:
 *
 *   - **Every number carries its denominator.** `HEADLINE` names, for each stage, what the
 *     figure is counted over, in the project's own vocabulary. "Coverage" appears nowhere: it
 *     is reserved for real-world reach, and none of these are that.
 *   - **A rate that is undefined is not zero.** A cell whose scorer could not score it is
 *     `unscoreable`, with the reason, and it is left out of every mean rather than dragging
 *     one down.
 */
import type { LedgerRow, Stage } from "./schema.js";
import { consistencyByCell, type MetricSpread } from "./consistency.js";
import { groupBySample } from "./campaigns.js";

export interface HeadlineDefinition {
  /** The scorer's key for the stage's headline figure. */
  readonly metric: string;
  /**
   * For a stage whose scorer records counts rather than a rate, the key holding the
   * denominator.
   *
   * Stage 4 is the case: `agreement.pclass` is a *count* of agreeing cases and
   * `agreement.comparable` is how many cases were aligned at all. Averaging `agreement.pclass`
   * across cells produces 1.19, which is not a rate and not anything. Where this is set, the
   * figure is the pooled numerator over the pooled denominator - "25 of 77", not the mean of
   * nine small fractions.
   */
  readonly denominatorMetric?: string;
  /** What a reader should call it. */
  readonly label: string;
  /** What it is counted over. Shown wherever the number is. */
  readonly denominator: string;
  /** The comparison method that produced it, from the harness. */
  readonly method: string;
}

/**
 * Each stage's headline figure.
 *
 * These are the metrics `report.py` leads with, which is exactly why the console also shows
 * the spread of every *other* metric beside them: at stage 1 the headline is F1, which does
 * not move, while the exact-argument rate moves by 0.200.
 */
export const HEADLINE: Record<Stage, HeadlineDefinition> = {
  syntax_spec: {
    metric: "f1",
    label: "flag F1",
    denominator: "flags in the reference specification",
    method: "q2_syntax_diff",
  },
  generate: {
    metric: "f1",
    label: "invocation F1",
    denominator: "v1's distinct invocations at the same limits",
    method: "invocation_set_diff",
  },
  trace: {
    metric: "core.micro.f1",
    label: "core interaction F1",
    denominator: "v1's projected filesystem interactions",
    method: "trace_recovery_diff",
  },
  annotate: {
    metric: "agreement.pclass",
    denominatorMetric: "agreement.comparable",
    label: "parallelizability-class agreement",
    denominator: "aligned cases where both sides state a class",
    method: "annotation_diff",
  },
};

/**
 * What a cell says about the two systems.
 *
 * Deliberately coarse, and deliberately not a grade. `replicates` means v2 reproduced v1
 * closely; `diverges` means it did not; `improves` is reserved for a figure that is better
 * than v1's *and* measured against a reference that is not v1 itself - otherwise "better than
 * v1" is a contradiction in terms.
 */
export type Verdict = "replicates" | "diverges" | "improves" | "unscoreable";

/** Above this, v2 reproduced v1 closely enough to call it replication. */
const REPLICATES_AT = 0.9;

export interface MatrixCell {
  readonly stage: Stage;
  readonly command: string;
  readonly model: string;
  readonly temperature: number;
  readonly promptVariant: string;
  readonly samples: number;
  /** The headline figure, averaged over samples. Null when no sample could be scored. */
  readonly value: number | null;
  readonly headline: HeadlineDefinition;
  readonly verdict: Verdict;
  /** How far the headline moved across samples. */
  readonly spread: number | null;
  /** The headline's full spread record, kept so its values can be judged alongside others. */
  readonly headlineSpreadDetail: MetricSpread | null;
  /**
   * Metrics that moved more than the headline did.
   *
   * Surfaced in the cell because this is the variation a headline-only report loses, and it is
   * the reason dimension 4 is measured per metric here.
   */
  readonly moreVariable: MetricSpread[];
  /** The scorer's own count breakdown, where it recorded one. */
  readonly counts: Record<string, number> | null;
  /** Why a cell could not be scored. Null when it was. */
  readonly unscoreableReason: string | null;
  /**
   * For a count-based stage, the pooled numerator and denominator behind `value`.
   *
   * Shown as "25 of 77" rather than 0.325 alone, because the denominator moves between
   * samples and a bare rate hides that.
   */
  readonly pooledCounts: { top: number; bottom: number } | null;
  /**
   * For a count-based stage, each sample's own counts.
   *
   * This is where its variation shows. `tail` agreed on 8 of 14 aligned cases in one sample
   * and 2 of 2 in another - both the numerator and the denominator move, because the
   * denominator counts cases that aligned at all, which depends on what v2 produced.
   */
  readonly perSampleCounts: { sample: number; top: number | null; bottom: number | null }[] | null;
  readonly runIds: string[];
}

function numeric(score: Record<string, unknown> | null, key: string): number | null {
  const value = score?.[key];
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function countsOf(score: Record<string, unknown> | null): Record<string, number> | null {
  const counts = score?.["counts"];
  if (counts === null || typeof counts !== "object") return null;
  const out: Record<string, number> = {};
  for (const [key, value] of Object.entries(counts as Record<string, unknown>)) {
    if (typeof value === "number") out[key] = value;
  }
  return Object.keys(out).length > 0 ? out : null;
}

/**
 * Is this metric a rate, so that a spread in it is comparable with a spread in another?
 *
 * Not every recorded metric is one. Stage 4 records `agreement.comparable`, a count of aligned
 * cases, which moved by 12 between samples - a true statement about the data and a meaningless
 * one to rank against a 0.200 movement in a rate. Counts are excluded from "widest spread" and
 * shown in the cell's own breakdown instead.
 *
 * The test is the values, not the name: a metric every one of whose samples lies in [0, 1] is
 * treated as a rate. That misclassifies a count that happens never to exceed 1, which costs
 * nothing - its spread is then at most 1 and it ranks like the rate it resembles.
 */
function isRateLike(metric: MetricSpread): boolean {
  return metric.values.every((value) => value >= 0 && value <= 1);
}

function verdictFor(value: number | null, unscoreable: boolean): Verdict {
  if (unscoreable || value === null) return "unscoreable";
  return value >= REPLICATES_AT ? "replicates" : "diverges";
}

export interface MatrixFilter {
  readonly model?: string;
  readonly temperature?: number;
  readonly promptVariant?: string;
  readonly command?: string;
}

/**
 * Fold a stage's ledger rows into one cell per configuration.
 *
 * Samples of the same configuration are averaged; a sample the scorer could not score is left
 * out of that average rather than counted as zero, and if no sample could be scored the cell
 * says so instead of showing 0.000.
 */
export function buildMatrix(rows: LedgerRow[], filter: MatrixFilter = {}): MatrixCell[] {
  const filtered = rows.filter(
    (row) =>
      (filter.model === undefined || row.model === filter.model) &&
      (filter.temperature === undefined || row.temperature === filter.temperature) &&
      (filter.promptVariant === undefined || row.prompt_variant === filter.promptVariant) &&
      (filter.command === undefined || row.command === filter.command),
  );

  const spreads = new Map(consistencyByCell(filtered).map((cell) => [cell.key, cell]));
  const cells: MatrixCell[] = [];

  for (const [key, group] of groupBySample(filtered)) {
    const first = group[0];
    if (!first) continue;

    const headline = HEADLINE[first.stage];

    // A stage whose scorer records counts is pooled, not averaged: the denominator is itself
    // per-sample (how many cases aligned at all), so a mean of ratios weights a sample that
    // aligned two cases the same as one that aligned fourteen.
    const pooled = headline.denominatorMetric
      ? group.reduce(
          (totals, row) => {
            const score = row.score as Record<string, unknown> | null;
            const top = numeric(score, headline.metric);
            const bottom = numeric(score, headline.denominatorMetric!);
            if (top === null || bottom === null) return totals;
            return { top: totals.top + top, bottom: totals.bottom + bottom, cells: totals.cells + 1 };
          },
          { top: 0, bottom: 0, cells: 0 },
        )
      : null;

    const values = group
      .map((row) => numeric(row.score as Record<string, unknown> | null, headline.metric))
      .filter((value): value is number => value !== null);

    // A cell can fail in two places: the scorer could not score what came back, or the run
    // itself never happened. The second records its reason on the row, not in the score - six
    // of `p1_annotate`'s cells are of that kind, rejected for exceeding the context window.
    const errors = group
      .flatMap((row) => [(row.score as Record<string, unknown> | null)?.["error"], row.error])
      .filter((error): error is string => typeof error === "string" && error.length > 0);

    const consistency = spreads.get(key);
    const headlineDetail =
      consistency?.metrics.find((metric) => metric.metric === headline.metric) ?? null;
    const headlineSpread = headlineDetail?.spread ?? null;

    const value = pooled
      ? pooled.bottom > 0
        ? pooled.top / pooled.bottom
        : null
      : values.length > 0
        ? values.reduce((sum, item) => sum + item, 0) / values.length
        : null;

    const scoredSamples = pooled ? pooled.cells : values.length;

    cells.push({
      stage: first.stage,
      command: first.command,
      model: first.model,
      temperature: first.temperature,
      promptVariant: first.prompt_variant,
      samples: group.length,
      value,
      headline,
      verdict: verdictFor(value, scoredSamples === 0),
      // For a count-based headline the "spread" would be a movement in a count, which is not
      // a consistency figure. The per-sample counts are shown instead.
      spread: headline.denominatorMetric ? null : headlineSpread,
      headlineSpreadDetail: headline.denominatorMetric ? null : headlineDetail,
      // Only rates, and never the numerator or denominator of a count-based headline. A cell
      // reporting "agreement.comparable moved 7.000" is stating that seven more cases aligned
      // in one sample than another - true, and not a statement about consistency.
      moreVariable:
        consistency?.metrics.filter(
          (metric) =>
            metric.metric !== headline.metric &&
            metric.metric !== headline.denominatorMetric &&
            metric.samples > 1 &&
            isRateLike(metric) &&
            metric.spread > (headlineSpread ?? 0),
        ) ?? [],
      counts: countsOf(group[0]!.score as Record<string, unknown> | null),
      unscoreableReason:
        scoredSamples === 0 ? (errors[0] ?? "the scorer reported no value") : null,
      pooledCounts: pooled && pooled.bottom > 0 ? { top: pooled.top, bottom: pooled.bottom } : null,
      perSampleCounts: headline.denominatorMetric
        ? group.map((row) => {
            const score = row.score as Record<string, unknown> | null;
            return {
              sample: row.sample,
              top: numeric(score, headline.metric),
              bottom: numeric(score, headline.denominatorMetric!),
            };
          })
        : null,
      runIds: group.map((row) => row.run_id).filter((id): id is string => id !== null),
    });
  }

  return cells.sort(
    (a, b) => a.command.localeCompare(b.command) || a.stage.localeCompare(b.stage),
  );
}

export interface MatrixView {
  readonly commands: string[];
  readonly stages: Stage[];
  /** `cell(command, stage)`, or undefined where that pair was never run. */
  readonly byKey: Map<string, MatrixCell>;
  readonly cells: MatrixCell[];
  /** Every distinct value seen, for the filter controls. */
  readonly models: string[];
  readonly temperatures: number[];
  readonly promptVariants: string[];
}

export function matrixKey(command: string, stage: string): string {
  return `${command}|${stage}`;
}

export function toMatrixView(cells: MatrixCell[]): MatrixView {
  const commands = [...new Set(cells.map((cell) => cell.command))].sort();
  const stages = (["syntax_spec", "generate", "trace", "annotate"] as Stage[]).filter((stage) =>
    cells.some((cell) => cell.stage === stage),
  );
  return {
    commands,
    stages,
    byKey: new Map(cells.map((cell) => [matrixKey(cell.command, cell.stage), cell])),
    cells,
    models: [...new Set(cells.map((cell) => cell.model))].sort(),
    temperatures: [...new Set(cells.map((cell) => cell.temperature))].sort((a, b) => a - b),
    promptVariants: [...new Set(cells.map((cell) => cell.promptVariant))].sort(),
  };
}

export interface StageSummary {
  readonly stage: Stage;
  readonly headline: HeadlineDefinition;
  /**
   * The stage's figure over the cells that could be scored.
   *
   * A mean of per-command rates for the stages whose scorer reports rates; a pooled
   * numerator over a pooled denominator for the stages whose scorer reports counts.
   */
  readonly mean: number | null;
  /** For a pooled stage, the counts behind `mean` - "25 of 77" rather than 0.325 alone. */
  readonly pooledCounts: { top: number; bottom: number } | null;
  readonly scoredCells: number;
  readonly unscoreableCells: number;
  /** The largest spread any single metric showed, and which one. */
  readonly widestSpread: { metric: string; spread: number; command: string } | null;
}

/**
 * Per-stage summary, with the widest spread found in any *rate* the stage reports.
 *
 * The widest spread is reported because it is the honest answer to "how reproducible is this
 * stage" - the headline's own spread answers a narrower question, and at stage 1 it answers it
 * with a zero that is true of F1 and false of the stage.
 */
const STAGE_ORDER: Stage[] = ["syntax_spec", "generate", "trace", "annotate"];

export function summarizeStages(cells: MatrixCell[]): StageSummary[] {
  const present = new Set(cells.map((cell) => cell.stage));
  const stages = STAGE_ORDER.filter((stage) => present.has(stage));

  return stages.map((stage) => {
    const forStage = cells.filter((cell) => cell.stage === stage);
    const scored = forStage.filter((cell) => cell.value !== null);

    let widest: { metric: string; spread: number; command: string } | null = null;
    for (const cell of forStage) {
      const candidates: MetricSpread[] = [
        ...cell.moreVariable,
        ...(cell.spread !== null && cell.headlineSpreadDetail !== null
          ? [cell.headlineSpreadDetail]
          : []),
      ];
      for (const candidate of candidates) {
        // The numerator and denominator of a count-based headline are counts by definition,
        // whatever values they happen to take in a small sample.
        if (candidate.metric === cell.headline.denominatorMetric) continue;
        if (cell.headline.denominatorMetric && candidate.metric === cell.headline.metric) continue;
        if (!isRateLike(candidate)) continue;
        if (widest === null || candidate.spread > widest.spread) {
          widest = { metric: candidate.metric, spread: candidate.spread, command: cell.command };
        }
      }
    }

    // A count-based stage is pooled across commands as well as samples. Averaging the
    // per-command rates would weight `cat`, which aligned one case, the same as `tail`, which
    // aligned fourteen - and the per-command rates for this stage range over a denominator
    // from 1 to 14.
    const pooledTotals = forStage.reduce(
      (totals, cell) =>
        cell.pooledCounts
          ? { top: totals.top + cell.pooledCounts.top, bottom: totals.bottom + cell.pooledCounts.bottom }
          : totals,
      { top: 0, bottom: 0 },
    );
    const isPooled = HEADLINE[stage].denominatorMetric !== undefined;

    return {
      stage,
      headline: HEADLINE[stage],
      mean: isPooled
        ? pooledTotals.bottom > 0
          ? pooledTotals.top / pooledTotals.bottom
          : null
        : scored.length > 0
          ? scored.reduce((sum, cell) => sum + (cell.value ?? 0), 0) / scored.length
          : null,
      pooledCounts: isPooled && pooledTotals.bottom > 0 ? pooledTotals : null,
      scoredCells: scored.length,
      unscoreableCells: forStage.length - scored.length,
      widestSpread: widest,
    };
  });
}
