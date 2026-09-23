/**
 * Findings as files (decision 6), and the re-check that catches a number that has moved.
 *
 * The case that matters most is the last one: a finding that was corrected after publication
 * must read "changed" against its original value and "matches" against its correction. That is
 * §10's requirement, and it is modelled on the real 0.185 -> 0.208 correction.
 */
import { describe, expect, it } from "vitest";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  compareEvidence,
  evidenceSchema,
  findingFrontmatterSchema,
  listFindings,
  parseFinding,
  readFinding,
  serializeFinding,
  writeFinding,
  FindingUnreadableError,
} from "../src/data/findings.js";

const ENV_AGREEMENT = evidenceSchema.parse({
  label: "environment agreement",
  value: 0.208,
  denominator: "the 24 cells where it is defined",
  metric: "environment.agreement",
  method: "generate",
  campaign_ids: ["p1_generate"],
  aggregation: "mean over cells, undefined cells excluded",
  scorer_commit: "d8032407",
  excluded: "uniq's cells, where the value is undefined on both sides",
});

function frontmatter() {
  return findingFrontmatterSchema.parse({
    id: "stage2-environment-agreement",
    claim: "v2 and v1 agree on 0.208 of the environment fields where agreement is defined.",
    status: "corrected",
    created: "2026-09-22",
    dimensions: [1],
    stages: ["generate"],
    paper_sections: ["§4"],
    evidence: [ENV_AGREEMENT],
    corrections: [
      {
        date: "2026-09-22",
        old_value: 0.185,
        new_value: 0.208,
        why: "The first figure divided by 27 rather than 24, counting uniq's undefined cells as zeros.",
      },
    ],
    source_document: "ai_docs/analysis/v1_v2_parity_study.md",
  });
}

describe("finding files", () => {
  it("round-trips through the file format", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-findings-"));
    const body = "Agreement is measured only where both sides define the field.";
    const path = writeFinding(frontmatter(), body, dir);

    const read = readFinding(path);
    expect(read.frontmatter.claim).toBe(frontmatter().claim);
    expect(read.frontmatter.evidence[0]!.value).toBe(0.208);
    expect(read.frontmatter.corrections[0]!.old_value).toBe(0.185);
    expect(read.body).toBe(body);
  });

  it("refuses a number with no denominator", () => {
    // The 0.185 error survived review precisely because the denominator was not stated.
    expect(() =>
      evidenceSchema.parse({
        label: "environment agreement",
        value: 0.185,
        metric: "environment.agreement",
        method: "generate",
      }),
    ).toThrow();
  });

  it("refuses a file with no frontmatter rather than guessing", () => {
    expect(() => parseFinding("# Just a heading\n", "x.md")).toThrow(FindingUnreadableError);
  });

  it("refuses frontmatter missing a claim", () => {
    const text = serializeFinding(frontmatter(), "body").replace(/^claim:.*$/m, "");
    expect(() => parseFinding(text, "x.md")).toThrow(FindingUnreadableError);
  });

  it("lists findings from a directory, and an absent directory is empty, not an error", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-findings-"));
    expect(listFindings(dir).findings).toEqual([]);
    writeFinding(frontmatter(), "body", dir);
    expect(listFindings(dir).findings).toHaveLength(1);
    expect(listFindings(join(dir, "nope")).findings).toEqual([]);
  });
});

describe("re-checking a number", () => {
  it("says matches when the scorer reproduces it", () => {
    expect(compareEvidence(ENV_AGREEMENT, 0.208).verdict).toBe("matches");
  });

  it("says changed when it does not", () => {
    const result = compareEvidence(ENV_AGREEMENT, 0.185);
    expect(result.verdict).toBe("changed");
    expect(result.recomputed).toBe(0.185);
  });

  it("marks a corrected finding changed against its old value and matching against the new", () => {
    // §10's requirement, on the real correction.
    const original = { ...ENV_AGREEMENT, value: 0.185 };
    expect(compareEvidence(original, 0.208).verdict).toBe("changed");
    expect(compareEvidence(ENV_AGREEMENT, 0.208).verdict).toBe("matches");
  });

  it("never calls an un-recomputable number a match", () => {
    // 25 of the runs the database knows about have no directory left; a finding resting on one
    // of them cannot be re-checked, and saying so is the only honest answer.
    const result = compareEvidence(ENV_AGREEMENT, null, "the runs behind this figure are gone");
    expect(result.verdict).toBe("not_recomputable");
    expect(result.reason).toContain("gone");
  });
});
