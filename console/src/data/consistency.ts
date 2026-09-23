/**
 * Spread across repeated runs, for every metric a method reports.
 *
 * This is evaluation dimension 4 - how much a result moves when the same configuration is run
 * again - and the console computes it here because the existing report does not compute it
 * fully. `report.py::consistency()` measures a method's headline metric only, which hides real
 * variation whenever the headline happens to be stable:
 *
 *   - Stage 1, `tac`: the exact-argument rate is 0.8, 1.0, 1.0 - a spread of 0.200. The report
 *     shows no spread, because it measures F1, which is 1.0 every time.
 *   - Stage 3, `pwd`: core recall is 1.0, 1.0, 0.6 - a spread of 0.400. The report shows 0.25,
 *     which is the spread in F1.
 *
 * Both are real variation in a number the paper would quote. So every numeric metric gets a
 * spread, and the headline is one column among them rather than the only one.
 *
 * Non-numeric and boolean fields are left out rather than coerced: `scoreable` is a flag, and
 * averaging flags produces a number that means nothing.
 */
import type { LedgerRow } from "./schema.js";
import { groupBySample } from "./campaigns.js";

export interface MetricSpread {
  readonly metric: string;
  readonly values: number[];
  readonly min: number;
  readonly max: number;
  /** max - min. The plainest statement of "how much did this move". */
  readonly spread: number;
  readonly mean: number;
  /** How many samples contributed. A spread over one sample is not a spread. */
  readonly samples: number;
}

export interface CellConsistency {
  readonly key: string;
  readonly stage: string;
  readonly command: string;
  readonly model: string;
  readonly temperature: number;
  readonly promptVariant: string;
  readonly samples: number;
  /** Every numeric metric this cell's scorer reported, by name. */
  readonly metrics: MetricSpread[];
}

/** Numbers only, and no booleans: `scoreable` is a flag, not a measurement. */
function numericMetrics(score: Record<string, unknown> | null): Map<string, number> {
  const out = new Map<string, number>();
  if (!score) return out;
  for (const [key, value] of Object.entries(score)) {
    if (typeof value === "number" && Number.isFinite(value)) out.set(key, value);
  }
  return out;
}

function spreadOf(metric: string, values: number[]): MetricSpread {
  const min = Math.min(...values);
  const max = Math.max(...values);
  return {
    metric,
    values,
    min,
    max,
    spread: max - min,
    mean: values.reduce((sum, value) => sum + value, 0) / values.length,
    samples: values.length,
  };
}

/**
 * One entry per configuration, with a spread for each metric its samples reported.
 *
 * A metric absent from some samples is measured only over the samples that have it, and
 * `samples` says how many those were. It is not treated as zero in the others - the same rule
 * the project applies to undefined cells everywhere else.
 */
export function consistencyByCell(rows: LedgerRow[]): CellConsistency[] {
  const out: CellConsistency[] = [];

  for (const [key, group] of groupBySample(rows)) {
    const collected = new Map<string, number[]>();
    for (const row of group) {
      for (const [metric, value] of numericMetrics(row.score)) {
        const list = collected.get(metric);
        if (list) list.push(value);
        else collected.set(metric, [value]);
      }
    }

    const first = group[0];
    if (!first) continue;

    out.push({
      key,
      stage: first.stage,
      command: first.command,
      model: first.model,
      temperature: first.temperature,
      promptVariant: first.prompt_variant,
      samples: group.length,
      metrics: [...collected]
        .map(([metric, values]) => spreadOf(metric, values))
        .sort((a, b) => b.spread - a.spread || a.metric.localeCompare(b.metric)),
    });
  }

  return out.sort((a, b) => a.key.localeCompare(b.key));
}

/**
 * The metric each stage's report treats as its headline.
 *
 * Recorded here so the console can show what the existing report would have said next to what
 * it actually found, which is the difference §10 asks to be demonstrated.
 */
export const HEADLINE_METRIC: Record<string, string> = {
  syntax_spec: "f1",
  generate: "invocation.f1",
  trace: "core.micro.f1",
  annotate: "agreement",
};

export interface HiddenVariation {
  readonly cell: CellConsistency;
  readonly headline: MetricSpread | null;
  /** Metrics that moved more than the headline did. These are what a headline-only view loses. */
  readonly moreVariableThanHeadline: MetricSpread[];
}

/** Where reporting the headline alone would understate how much a cell moved. */
export function hiddenVariation(cells: CellConsistency[]): HiddenVariation[] {
  const out: HiddenVariation[] = [];
  for (const cell of cells) {
    if (cell.samples < 2) continue;
    const headlineName = HEADLINE_METRIC[cell.stage];
    const headline = cell.metrics.find((metric) => metric.metric === headlineName) ?? null;
    const threshold = headline?.spread ?? 0;
    const worse = cell.metrics.filter(
      (metric) => metric.metric !== headlineName && metric.spread > threshold,
    );
    if (worse.length > 0) out.push({ cell, headline, moreVariableThanHeadline: worse });
  }
  return out;
}
