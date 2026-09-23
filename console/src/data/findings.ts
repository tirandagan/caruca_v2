/**
 * Findings: one Markdown file per claim, in `ai_docs/analysis/findings/`.
 *
 * Decision 6, confirmed by Tiran on 2026-09-22. Files rather than a database, because git
 * history, co-author review and the existing Markdown-to-PDF pipeline all work on files, and a
 * database would be a second source of truth for numbers that already live in run directories.
 *
 * The shape enforces the project's measurement discipline: **no number without its source.**
 * Every recorded value carries the runs or campaign it came from, the metric and method that
 * produced it, its denominator, and the scorer commit it was computed with. That is what makes
 * the re-check in §6.6 possible - and the re-check is the point, because it would have caught
 * both errors already published in the parity study:
 *
 *   - the first environment-agreement figure, 0.185, counted `uniq`'s undefined cells as zeros
 *     (correct figure 0.208, over the 24 cells where it is defined);
 *   - the first stage-3 figures were computed by hand from one sample per command.
 *
 * `denominator` is therefore required, not optional. A rate without one is how the first of
 * those errors survived review.
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";
import { z } from "zod";
import { repoPaths } from "./paths.js";

export class FindingUnreadableError extends Error {}

export const FINDING_STATUSES = [
  "draft",
  "confirmed",
  "corrected",
  "superseded",
  "withdrawn",
] as const;
export type FindingStatus = (typeof FINDING_STATUSES)[number];

/** One number, with everything needed to compute it again. */
export const evidenceSchema = z.object({
  /** What the number is called, in the project's vocabulary - never a bare "coverage". */
  label: z.string().min(1),
  value: z.number(),
  /** What it was counted over. Required: a rate without a denominator hid a real error once. */
  denominator: z.string().min(1),
  /** The scorer's metric key, e.g. `core.micro.recall`. */
  metric: z.string().min(1),
  /** The comparison method that produced it, from `harness/methods.py`. */
  method: z.string().min(1),
  run_ids: z.array(z.string()).default([]),
  campaign_ids: z.array(z.string()).default([]),
  /** How samples were combined, where they were. */
  aggregation: z.string().nullable().default(null),
  /** The commit the scorer was at. A number recomputed by a different scorer is a new number. */
  scorer_commit: z.string().nullable().default(null),
  /** Cases left out because the value is undefined for them, and why. */
  excluded: z.string().nullable().default(null),
  /**
   * How to recompute this number.
   *
   * Kept with the number rather than in code, so the recipe travels with the claim and a
   * finding written today can still be checked after the console changes. Its shapes are in
   * `recheck.ts`. A number with no recipe is still readable; it just reports that it cannot
   * be checked, which is itself worth knowing.
   */
  recheck: z.record(z.unknown()).nullable().default(null),
});
export type Evidence = z.infer<typeof evidenceSchema>;

export const correctionSchema = z.object({
  date: z.string(),
  old_value: z.union([z.number(), z.string(), z.null()]),
  new_value: z.union([z.number(), z.string(), z.null()]),
  why: z.string().min(1),
});
export type Correction = z.infer<typeof correctionSchema>;

export const findingFrontmatterSchema = z.object({
  /** Stable file-name slug. */
  id: z.string().min(1),
  /** The whole finding in one sentence. */
  claim: z.string().min(1),
  status: z.enum(FINDING_STATUSES),
  created: z.string(),
  updated: z.string().nullable().default(null),
  /** Evaluation dimensions 1-6, by number. */
  dimensions: z.array(z.number().int().min(1).max(6)).default([]),
  stages: z.array(z.string()).default([]),
  /** Which parts of the paper this bears on. */
  paper_sections: z.array(z.string()).default([]),
  evidence: z.array(evidenceSchema).default([]),
  corrections: z.array(correctionSchema).default([]),
  /** Some findings are questions only v1's authors can settle. */
  needs_v1_authors: z.boolean().default(false),
  /** Where the claim was first written, for the Phase 3 backfill. */
  source_document: z.string().nullable().default(null),
});
export type FindingFrontmatter = z.infer<typeof findingFrontmatterSchema>;

export interface Finding {
  readonly frontmatter: FindingFrontmatter;
  /** The plain-language explanation. Markdown, below the frontmatter. */
  readonly body: string;
  readonly path: string;
}

const FRONTMATTER = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/;

export function parseFinding(text: string, path: string): Finding {
  const match = FRONTMATTER.exec(text);
  if (!match) {
    throw new FindingUnreadableError(`${path} has no YAML frontmatter block.`);
  }
  let raw: unknown;
  try {
    raw = parseYaml(match[1]!);
  } catch (cause) {
    throw new FindingUnreadableError(`${path} frontmatter is not valid YAML: ${(cause as Error).message}`);
  }
  const parsed = findingFrontmatterSchema.safeParse(raw);
  if (!parsed.success) {
    throw new FindingUnreadableError(
      `${path} frontmatter is missing or malformed: ${parsed.error.issues
        .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
        .join("; ")}`,
    );
  }
  return { frontmatter: parsed.data, body: (match[2] ?? "").trim(), path };
}

export function serializeFinding(frontmatter: FindingFrontmatter, body: string): string {
  const yaml = stringifyYaml(frontmatter, { lineWidth: 0 }).trimEnd();
  return `---\n${yaml}\n---\n\n${body.trim()}\n`;
}

export function readFinding(path: string): Finding {
  try {
    return parseFinding(readFileSync(path, "utf8"), path);
  } catch (cause) {
    if (cause instanceof FindingUnreadableError) throw cause;
    throw new FindingUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }
}

export interface ListFindingsResult {
  readonly findings: Finding[];
  readonly unreadable: { file: string; reason: string }[];
}

export function listFindings(dir = repoPaths().findings): ListFindingsResult {
  const findings: Finding[] = [];
  const unreadable: { file: string; reason: string }[] = [];
  if (!existsSync(dir)) return { findings, unreadable };

  for (const name of readdirSync(dir).sort()) {
    if (!name.endsWith(".md") || name === "README.md") continue;
    try {
      findings.push(readFinding(join(dir, name)));
    } catch (cause) {
      unreadable.push({ file: name, reason: (cause as Error).message });
    }
  }
  return { findings, unreadable };
}

/**
 * Write a finding to its file.
 *
 * The console writes files and never commits: that stays Tiran's call (§6.6).
 */
export function writeFinding(
  frontmatter: FindingFrontmatter,
  body: string,
  dir = repoPaths().findings,
): string {
  const parsed = findingFrontmatterSchema.parse(frontmatter);
  mkdirSync(dir, { recursive: true });
  const path = join(dir, `${parsed.id}.md`);
  writeFileSync(path, serializeFinding(parsed, body));
  return path;
}

export type RecheckVerdict = "matches" | "changed" | "not_recomputable";

export interface RecheckResult {
  readonly evidence: Evidence;
  readonly verdict: RecheckVerdict;
  /** The recomputed value at full precision, whatever precision the claim was stated to. */
  readonly recomputed: number | null;
  /** Why a number could not be recomputed, when that is the verdict. */
  readonly reason: string | null;
  /** Decimal places the comparison used, taken from how the number was written down. */
  readonly comparedAtPrecision: number | null;
}

/**
 * How many decimal places a recorded number was written to.
 *
 * A figure quoted in a document is rounded - the parity study says 0.606, the scorer says
 * 0.6062992125984252. Comparing those exactly reports a change on every number ever written
 * down, which would make the re-check useless within a day. So a value is compared at the
 * precision at which it was stated, and no finer.
 */
export function statedPrecision(value: number): number {
  if (Number.isInteger(value)) {
    // A whole number that is a rate lost its decimals on the way through YAML: "1.000" and
    // "1" are the same value once parsed, so the precision cannot be read back. Rates get
    // three places, because "F1 is 1.000" is a strong claim that a recomputed 0.999 breaks,
    // and rounding it away would let a real regression pass as a match. A genuine count -
    // 25 aligned cases, 224,394 tokens - is compared as the whole number it is.
    return Math.abs(value) <= 1 ? RATE_PRECISION : 0;
  }
  const text = String(value);
  const dot = text.indexOf(".");
  if (dot < 0) return 0;
  // Exponential notation (1e-7) has no meaningful decimal count to read off.
  if (text.includes("e") || text.includes("E")) return 12;
  return text.length - dot - 1;
}

/** Decimal places assumed for a rate whose written precision could not be recovered. */
const RATE_PRECISION = 3;

/**
 * Compare a recorded number against one recomputed today.
 *
 * Two rules:
 *
 *   - **Compared at the precision it was written to.** 0.606 against a recomputed
 *     0.6062992125984252 is a match, because 0.606 is what the document claims. A recomputed
 *     0.612 is not.
 *   - **A value that could not be recomputed is `not_recomputable`, never silently "matches".**
 *     The runs behind a finding can be deleted - 25 of the runs the metrics database knows
 *     about already have no directory left - and a check that cannot run must say so rather
 *     than report success.
 */
export function compareEvidence(
  evidence: Evidence,
  recomputed: number | null,
  reason: string | null = null,
): RecheckResult {
  if (recomputed === null) {
    return {
      evidence,
      verdict: "not_recomputable",
      recomputed: null,
      reason: reason ?? "no recomputed value was produced",
      comparedAtPrecision: null,
    };
  }

  const places = statedPrecision(evidence.value);
  const factor = 10 ** places;
  const matches = Math.round(recomputed * factor) === Math.round(evidence.value * factor);

  return {
    evidence,
    verdict: matches ? "matches" : "changed",
    recomputed,
    reason: null,
    comparedAtPrecision: places,
  };
}
