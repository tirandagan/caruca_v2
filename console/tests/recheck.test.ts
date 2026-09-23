/**
 * Re-checking recorded numbers.
 *
 * The two subtle cases, both found by running this against the real findings:
 *
 *   1. A number written in a document is rounded. Comparing 0.606 exactly against a scorer's
 *      0.6062992125984252 marks every number ever written down as "changed", which makes the
 *      whole check useless. Comparison happens at the precision the number was stated to.
 *   2. `report --json` publishes its two metric slots under the fixed names `f1` and
 *      `exact_argument_rate` for every stage, filled from that stage's own metric list. So
 *      stage 2's invocation recall arrives under the key `exact_argument_rate`. Reading those
 *      keys at face value attaches a stage-1 name to a stage-2 number.
 */
import { describe, expect, it } from "vitest";
import { compareEvidence, evidenceSchema, statedPrecision } from "../src/data/findings.js";
import { recipeOf, reportKeyFor } from "../src/data/recheck.js";
import { listFindings } from "../src/data/findings.js";

function evidence(value: number, extra: Record<string, unknown> = {}) {
  return evidenceSchema.parse({
    label: "a rate",
    value,
    denominator: "the cases where it is defined",
    metric: "recall",
    method: "invocation_set_diff",
    ...extra,
  });
}

describe("comparing at the precision a number was written to", () => {
  it("reads the precision off the recorded value", () => {
    expect(statedPrecision(0.606)).toBe(3);
    expect(statedPrecision(0.8)).toBe(1);
  });

  it("assumes three places for a rate whose decimals YAML threw away", () => {
    // "F1 = 1.000" and "F1 = 1" are the same value once parsed. Treating it as a whole number
    // would let a recomputed 0.999 pass as a match, which is exactly the regression worth
    // catching at stage 1.
    expect(statedPrecision(1)).toBe(3);
    expect(statedPrecision(0)).toBe(3);
  });

  it("compares a genuine count as the whole number it is", () => {
    expect(statedPrecision(25)).toBe(0);
    expect(statedPrecision(224394)).toBe(0);
    expect(compareEvidence(evidence(25), 25.4).verdict).toBe("matches");
    expect(compareEvidence(evidence(25), 26).verdict).toBe("changed");
  });

  it("calls a rounded match a match", () => {
    // The parity study says 0.606; the scorer says 0.6062992125984252.
    expect(compareEvidence(evidence(0.606), 0.6062992125984252).verdict).toBe("matches");
    expect(compareEvidence(evidence(0.878), 0.8775132275132275).verdict).toBe("matches");
    expect(compareEvidence(evidence(0.325), 0.3246753246753247).verdict).toBe("matches");
  });

  it("still catches a real move at that precision", () => {
    // 0.623 against 0.606 is a different number, not a rounding artefact.
    expect(compareEvidence(evidence(0.606), 0.6227272727272727).verdict).toBe("changed");
    expect(compareEvidence(evidence(1.0), 0.999).verdict).toBe("changed");
  });

  it("keeps the recomputed value at full precision whatever the comparison used", () => {
    const result = compareEvidence(evidence(0.606), 0.6062992125984252);
    expect(result.recomputed).toBe(0.6062992125984252);
    expect(result.comparedAtPrecision).toBe(3);
  });

  it("never calls an un-recomputable number a match", () => {
    const result = compareEvidence(evidence(0.606), null, "the campaign is not on this machine");
    expect(result.verdict).toBe("not_recomputable");
    expect(result.comparedAtPrecision).toBeNull();
  });
});

describe("finding a metric in the report's fixed slots", () => {
  it("maps a stage-1 metric to its own name", () => {
    expect(reportKeyFor("q2_syntax_diff", "f1")).toBe("f1");
    expect(reportKeyFor("q2_syntax_diff", "exact_argument_rate")).toBe("exact_argument_rate");
  });

  it("maps stage 2's recall to the slot that actually carries it", () => {
    // The value is invocation recall; the key it arrives under is `exact_argument_rate`.
    expect(reportKeyFor("invocation_set_diff", "recall")).toBe("exact_argument_rate");
    expect(reportKeyFor("invocation_set_diff", "f1")).toBe("f1");
  });

  it("maps stage 3's core recall likewise", () => {
    expect(reportKeyFor("trace_recovery_diff", "core.micro.recall")).toBe("exact_argument_rate");
    expect(reportKeyFor("trace_recovery_diff", "core.micro.f1")).toBe("f1");
  });

  it("says so when a metric is past the two slots the report publishes", () => {
    // `precision` is third in invocation_set_diff's list; the report carries only two.
    expect(reportKeyFor("invocation_set_diff", "precision")).toBeNull();
    expect(reportKeyFor("q2_syntax_diff", "recall")).toBeNull();
  });

  it("returns null for a metric the method does not declare", () => {
    expect(reportKeyFor("invocation_set_diff", "nonsense")).toBeNull();
  });
});

describe("recipes on the backfilled findings", () => {
  const findings = listFindings().findings;

  it("reads a recipe where one is recorded, and null where none is", () => {
    const all = findings.flatMap((finding) => finding.frontmatter.evidence);
    expect(all.length).toBeGreaterThan(0);
    const withRecipe = all.filter((item) => recipeOf(item) !== null);
    expect(withRecipe.length).toBeGreaterThan(0);
    for (const item of withRecipe) {
      expect(["campaign_metric", "campaign_pooled", "spec_score"]).toContain(
        recipeOf(item)!.kind,
      );
    }
  });

  it("every recorded number states what it is counted over", () => {
    // The schema enforces this, so the test is really about the backfill having taken it
    // seriously rather than writing "n/a" everywhere.
    for (const finding of findings) {
      for (const item of finding.frontmatter.evidence) {
        expect(item.denominator.length).toBeGreaterThan(8);
        expect(item.denominator.toLowerCase()).not.toBe("n/a");
      }
    }
  });

  it("no finding uses the word coverage for something that is not real-world reach", () => {
    // The project reserves that word; several of these rates were once described with it.
    for (const finding of findings) {
      for (const item of finding.frontmatter.evidence) {
        expect(item.label.toLowerCase()).not.toContain("coverage");
      }
    }
  });

  it("a corrected finding records what the old value was and why it moved", () => {
    const corrected = findings.filter(
      (finding) => finding.frontmatter.corrections.length > 0,
    );
    expect(corrected.length).toBeGreaterThan(0);
    for (const finding of corrected) {
      for (const correction of finding.frontmatter.corrections) {
        expect(correction.why.length).toBeGreaterThan(20);
        expect(correction.old_value).not.toBeNull();
      }
    }
  });
});
