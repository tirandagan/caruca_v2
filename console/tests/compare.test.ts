/**
 * The comparison matrix.
 *
 * Most of these tests exist because of mistakes the first version of this module made against
 * the real ledgers, each of which produced a plausible-looking number that was wrong:
 *
 *   - averaging `agreement.pclass` gave 1.19, which is not a rate, because the stage-4 scorer
 *     records counts and not rates;
 *   - ranking metric spreads together reported stage 4's widest variation as 12.000, which was
 *     the movement in a *count* of aligned cases;
 *   - averaging per-command rates weighted `cat`, with one aligned case, the same as `tail`,
 *     with fourteen.
 *
 * The synthetic cases pin the behaviour; the cases against the real campaigns pin the figures.
 */
import { describe, expect, it } from "vitest";
import { join } from "node:path";
import { buildMatrix, summarizeStages, toMatrixView, HEADLINE, matrixKey } from "../src/data/compare.js";
import { listCampaigns, loadLedger } from "../src/data/campaigns.js";
import { ledgerRowSchema, type LedgerRow } from "../src/data/schema.js";
import { repoPaths } from "../src/data/paths.js";

function row(overrides: Partial<LedgerRow> & { sample: number }): LedgerRow {
  return ledgerRowSchema.parse({
    cell_key: "x",
    campaign_id: "synthetic",
    stage: "syntax_spec",
    command: "cat",
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

describe("rates and counts are not the same thing", () => {
  it("pools a count-based stage instead of averaging its ratios", () => {
    // Two commands: one aligned 1 case and agreed on it, one aligned 9 and agreed on 1.
    // Averaging the ratios gives (1.0 + 0.111) / 2 = 0.56. Pooling gives 2 of 10 = 0.2.
    const cells = buildMatrix([
      row({
        sample: 0,
        stage: "annotate",
        command: "cat",
        score: { "agreement.pclass": 1, "agreement.comparable": 1 },
      }),
      row({
        sample: 0,
        stage: "annotate",
        command: "tail",
        score: { "agreement.pclass": 1, "agreement.comparable": 9 },
      }),
    ]);
    const [summary] = summarizeStages(cells);
    expect(summary?.pooledCounts).toEqual({ top: 2, bottom: 10 });
    expect(summary?.mean).toBeCloseTo(0.2, 10);
  });

  it("shows a count-based cell as a ratio of pooled counts across its samples", () => {
    const cells = buildMatrix([
      row({ sample: 0, stage: "annotate", score: { "agreement.pclass": 8, "agreement.comparable": 14 } }),
      row({ sample: 1, stage: "annotate", score: { "agreement.pclass": 7, "agreement.comparable": 12 } }),
      row({ sample: 2, stage: "annotate", score: { "agreement.pclass": 2, "agreement.comparable": 2 } }),
    ]);
    expect(cells[0]!.pooledCounts).toEqual({ top: 17, bottom: 28 });
    expect(cells[0]!.value).toBeCloseTo(17 / 28, 10);
  });

  it("keeps a count's movement out of the widest-spread ranking", () => {
    // `agreement.comparable` moving from 2 to 14 is a true statement about the data and a
    // meaningless one to rank against a 0.2 movement in a rate.
    const cells = buildMatrix([
      row({ sample: 0, stage: "annotate", score: { "agreement.pclass": 1, "agreement.comparable": 2 } }),
      row({ sample: 1, stage: "annotate", score: { "agreement.pclass": 1, "agreement.comparable": 14 } }),
    ]);
    const [summary] = summarizeStages(cells);
    expect(summary?.widestSpread?.metric).not.toBe("agreement.comparable");
  });
});

describe("undefined is not zero", () => {
  it("marks a cell no sample could score, rather than showing 0.000", () => {
    const cells = buildMatrix([
      row({ sample: 0, command: "rm", status: "error", score: { error: "v1 produced no annotation" } }),
    ]);
    expect(cells[0]!.verdict).toBe("unscoreable");
    expect(cells[0]!.value).toBeNull();
    expect(cells[0]!.unscoreableReason).toContain("v1 produced no annotation");
  });

  it("leaves an unscoreable cell out of the stage mean instead of dragging it down", () => {
    const cells = buildMatrix([
      row({ sample: 0, command: "cat", score: { f1: 1.0 } }),
      row({ sample: 0, command: "rm", score: { error: "nothing to compare" } }),
    ]);
    const [summary] = summarizeStages(cells);
    expect(summary?.mean).toBe(1.0);
    expect(summary?.scoredCells).toBe(1);
    expect(summary?.unscoreableCells).toBe(1);
  });
});

describe("the matrix view", () => {
  it("indexes cells by command and stage, and offers the filter values", () => {
    const view = toMatrixView(
      buildMatrix([
        row({ sample: 0, command: "cat", score: { f1: 1 } }),
        row({ sample: 0, command: "wc", stage: "generate", score: { f1: 0.5 } }),
      ]),
    );
    expect(view.commands).toEqual(["cat", "wc"]);
    expect(view.byKey.get(matrixKey("cat", "syntax_spec"))?.value).toBe(1);
    expect(view.models).toEqual(["openai/gpt-4o"]);
  });

  it("filters by model, temperature and variant", () => {
    const rows = [
      row({ sample: 0, score: { f1: 1 } }),
      row({ sample: 0, model: "anthropic/claude-haiku-4.5", score: { f1: 0.4 } }),
    ];
    expect(buildMatrix(rows, { model: "openai/gpt-4o" })).toHaveLength(1);
    expect(buildMatrix(rows, { temperature: 0 })).toHaveLength(2);
    expect(buildMatrix(rows, { promptVariant: "nope" })).toHaveLength(0);
  });
});

const campaignsPresent = listCampaigns().length > 0;
describe.skipIf(!campaignsPresent)("against the real parity campaigns", () => {
  function stage(id: string) {
    return buildMatrix(loadLedger(join(repoPaths().campaigns, id, "ledger.jsonl")).rows);
  }

  it("stage 1: flag F1 is 1.000, and the variation is in a metric the headline hides", () => {
    const [summary] = summarizeStages(stage("p1_syntax_spec"));
    expect(summary?.mean).toBeCloseTo(1.0, 10);
    expect(summary?.widestSpread?.metric).toBe("exact_argument_rate");
    expect(summary?.widestSpread?.spread).toBeCloseTo(0.2, 10);
    expect(summary?.widestSpread?.command).toBe("tac");
  });

  it("stage 3: four of nine commands could not be scored at all", () => {
    const [summary] = summarizeStages(stage("p1_trace"));
    expect(summary?.scoredCells).toBe(5);
    expect(summary?.unscoreableCells).toBe(4);
    expect(summary?.widestSpread?.command).toBe("pwd");
    expect(summary?.widestSpread?.spread).toBeCloseTo(0.4, 10);
  });

  it("stage 4 pools to 25 of 77, not the 10 of 33 that §10 quotes", () => {
    // §10's figure is sample 0 alone. The three samples give 10/33, 9/30 and 6/14 - the
    // denominator moves because it counts *aligned* cases, which depend on what v2 produced.
    // Pooling all three is 25 of 77.
    const [summary] = summarizeStages(stage("p1_annotate"));
    expect(summary?.pooledCounts).toEqual({ top: 25, bottom: 77 });
    expect(summary?.mean).toBeCloseTo(25 / 77, 10);
  });

  it("stage 4: rm and tee could not be scored in any sample", () => {
    const cells = stage("p1_annotate");
    const unscoreable = cells.filter((cell) => cell.verdict === "unscoreable").map((c) => c.command);
    expect(unscoreable.sort()).toEqual(["rm", "tee"]);
  });

  it("every stage's headline names what it is counted over", () => {
    for (const definition of Object.values(HEADLINE)) {
      expect(definition.denominator.length).toBeGreaterThan(10);
      // "Coverage" is reserved for real-world reach; none of these is that.
      expect(definition.label.toLowerCase()).not.toContain("coverage");
      expect(definition.denominator.toLowerCase()).not.toContain("coverage");
    }
  });
});

describe("what a cell reports as movement", () => {
  it("never reports a count's movement as a consistency figure", () => {
    // `agreement.comparable` going from 2 to 14 says seven times as many cases aligned, not
    // that the stage is inconsistent. It belongs in the cell's own breakdown, not here.
    const cells = buildMatrix([
      row({ sample: 0, stage: "annotate", score: { "agreement.pclass": 1, "agreement.comparable": 2 } }),
      row({ sample: 1, stage: "annotate", score: { "agreement.pclass": 8, "agreement.comparable": 14 } }),
    ]);
    const names = cells[0]!.moreVariable.map((metric) => metric.metric);
    expect(names).not.toContain("agreement.comparable");
    expect(names).not.toContain("agreement.pclass");
    // And the headline itself has no "spread", because it is a count.
    expect(cells[0]!.spread).toBeNull();
  });

  it("shows each sample's own counts, where both parts of the ratio move", () => {
    const cells = buildMatrix([
      row({ sample: 0, stage: "annotate", score: { "agreement.pclass": 8, "agreement.comparable": 14 } }),
      row({ sample: 1, stage: "annotate", score: { "agreement.pclass": 2, "agreement.comparable": 2 } }),
    ]);
    expect(cells[0]!.perSampleCounts).toEqual([
      { sample: 0, top: 8, bottom: 14 },
      { sample: 1, top: 2, bottom: 2 },
    ]);
  });

  it("keeps a rate's movement, which is a consistency figure", () => {
    const cells = buildMatrix([
      row({ sample: 0, score: { f1: 1.0, exact_argument_rate: 0.8 } }),
      row({ sample: 1, score: { f1: 1.0, exact_argument_rate: 1.0 } }),
    ]);
    expect(cells[0]!.moreVariable.map((m) => m.metric)).toEqual(["exact_argument_rate"]);
  });

  it("orders the stage summaries by stage, not by whatever the data happened to give", () => {
    const cells = buildMatrix([
      row({ sample: 0, stage: "annotate", score: { "agreement.pclass": 1, "agreement.comparable": 1 } }),
      row({ sample: 0, stage: "syntax_spec", score: { f1: 1 } }),
      row({ sample: 0, stage: "trace", score: { "core.micro.f1": 1 } }),
    ]);
    expect(summarizeStages(cells).map((s) => s.stage)).toEqual([
      "syntax_spec",
      "trace",
      "annotate",
    ]);
  });
});
