/**
 * Consistency across repeated runs, and the two cases the existing report gets wrong.
 *
 * `eval/campaigns/` is the one part of the run data that is NOT committed, so the main tests
 * build synthetic ledgers and run without it. The two acceptance cases from §10 are checked
 * against the real campaigns when they are present on this machine, and skipped with a clear
 * message when they are not - rather than silently passing on a fresh clone.
 */
import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { consistencyByCell, hiddenVariation, HEADLINE_METRIC } from "../src/data/consistency.js";
import { loadLedger, groupBySample, listCampaigns } from "../src/data/campaigns.js";
import { ledgerRowSchema, type LedgerRow } from "../src/data/schema.js";
import { repoPaths } from "../src/data/paths.js";

function row(overrides: Partial<LedgerRow> & { sample: number }): LedgerRow {
  return ledgerRowSchema.parse({
    cell_key: "x",
    campaign_id: "synthetic",
    stage: "syntax_spec",
    command: "tac",
    model: "openai/gpt-4o",
    temperature: 0,
    prompt_variant: "default",
    attempts: 1,
    status: "ok",
    cost_usd: 0,
    prompt_tokens: 0,
    completion_tokens: 0,
    ...overrides,
  });
}

describe("per-metric spread", () => {
  it("reports a spread for every numeric metric, not just the headline", () => {
    const cells = consistencyByCell([
      row({ sample: 0, score: { f1: 1.0, exact_argument_rate: 0.8 } }),
      row({ sample: 1, score: { f1: 1.0, exact_argument_rate: 1.0 } }),
      row({ sample: 2, score: { f1: 1.0, exact_argument_rate: 1.0 } }),
    ]);

    expect(cells).toHaveLength(1);
    const names = cells[0]!.metrics.map((metric) => metric.metric);
    expect(names).toContain("f1");
    expect(names).toContain("exact_argument_rate");

    const exact = cells[0]!.metrics.find((metric) => metric.metric === "exact_argument_rate")!;
    expect(exact.spread).toBeCloseTo(0.2, 10);
    const f1 = cells[0]!.metrics.find((metric) => metric.metric === "f1")!;
    expect(f1.spread).toBe(0);
  });

  it("flags the case where the headline hides the variation", () => {
    const cells = consistencyByCell([
      row({ sample: 0, score: { f1: 1.0, exact_argument_rate: 0.8 } }),
      row({ sample: 1, score: { f1: 1.0, exact_argument_rate: 1.0 } }),
    ]);
    const hidden = hiddenVariation(cells);
    expect(hidden).toHaveLength(1);
    expect(hidden[0]!.headline?.spread).toBe(0);
    expect(hidden[0]!.moreVariableThanHeadline.map((metric) => metric.metric)).toEqual([
      "exact_argument_rate",
    ]);
  });

  it("ignores flags and non-numbers rather than averaging them", () => {
    const cells = consistencyByCell([
      row({ sample: 0, score: { f1: 1.0, scoreable: true, note: "fine" } }),
      row({ sample: 1, score: { f1: 0.5, scoreable: false, note: "also fine" } }),
    ]);
    expect(cells[0]!.metrics.map((metric) => metric.metric)).toEqual(["f1"]);
  });

  it("measures a partly-reported metric over the samples that have it", () => {
    const cells = consistencyByCell([
      row({ sample: 0, score: { f1: 1.0, extra: 0.4 } }),
      row({ sample: 1, score: { f1: 1.0 } }),
    ]);
    const extra = cells[0]!.metrics.find((metric) => metric.metric === "extra")!;
    // Two samples in the cell, one value for this metric. Not averaged against a zero.
    expect(extra.samples).toBe(1);
    expect(extra.spread).toBe(0);
    expect(cells[0]!.samples).toBe(2);
  });

  it("does not call one sample a spread", () => {
    expect(hiddenVariation(consistencyByCell([row({ sample: 0, score: { f1: 1 } })]))).toEqual([]);
  });

  it("groups by everything except the sample number", () => {
    const groups = groupBySample([
      row({ sample: 0 }),
      row({ sample: 1 }),
      row({ sample: 0, command: "cat" }),
    ]);
    expect(groups.size).toBe(2);
  });
});

/**
 * The two cases §10 names, checked against the real campaigns if this machine has them.
 */
const campaignsPresent = listCampaigns().length > 0;
describe.skipIf(!campaignsPresent)("the two cases §10 names (needs local campaigns)", () => {
  it("stage 1: tac's exact-argument rate spreads by 0.200 while F1 does not move", () => {
    const path = join(repoPaths().campaigns, "p1_syntax_spec", "ledger.jsonl");
    expect(existsSync(path)).toBe(true);
    const cells = consistencyByCell(
      loadLedger(path).rows.filter((candidate) => candidate.command === "tac"),
    );
    const metrics = cells[0]!.metrics;
    expect(metrics.find((metric) => metric.metric === "exact_argument_rate")!.spread).toBeCloseTo(
      0.2,
      10,
    );
    expect(
      metrics.find((metric) => metric.metric === HEADLINE_METRIC.syntax_spec)!.spread,
    ).toBe(0);
  });

  it("stage 3: pwd's core recall spreads by 0.400 while F1 shows 0.25", () => {
    const path = join(repoPaths().campaigns, "p1_trace", "ledger.jsonl");
    expect(existsSync(path)).toBe(true);
    const cells = consistencyByCell(
      loadLedger(path).rows.filter((candidate) => candidate.command === "pwd"),
    );
    const metrics = cells[0]!.metrics;
    expect(metrics.find((metric) => metric.metric === "core.micro.recall")!.spread).toBeCloseTo(
      0.4,
      10,
    );
    expect(
      metrics.find((metric) => metric.metric === HEADLINE_METRIC.trace)!.spread,
    ).toBeCloseTo(0.25, 10);
  });
});
