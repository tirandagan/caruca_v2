/**
 * The per-command drill-down: what each side actually produced, item by item.
 *
 * §6.4 requires the drill-down to call the same modules `scripts/parity_diff.py` uses, "so the
 * console and the script cannot disagree". The strongest form of that is not to call the same
 * modules but to show the script's own output: `eval/parity_diffs/<command>.md` is written by
 * that script and already contains, per stage, the matched, missing and spurious items, the
 * field-by-field environment comparison, and what each side's trace saw.
 *
 * So this module reads and splits those documents rather than reimplementing any of it. The
 * console's numbers come from the ledgers; the *items behind* the numbers come from here; and
 * when they are regenerated, the console shows the new ones with no code change.
 *
 * **These documents quote v1's source verbatim**, which is why they carry their own warning
 * and why the console is local-only. `v1SourceWarning` surfaces that where a section is shown.
 */
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import type { Stage } from "./schema.js";
import { repoPaths } from "./paths.js";

export class ParityDiffMissingError extends Error {}

/** The heading each stage's section carries in the generated document. */
const STAGE_HEADING: Record<Stage, string> = {
  syntax_spec: "Stage 1",
  generate: "Stage 2",
  trace: "Stage 3",
  annotate: "Stage 4",
};

export interface ParityDiffSection {
  readonly stage: Stage;
  /** The section's own heading, as written. */
  readonly heading: string;
  /** The section body, Markdown, exactly as the script wrote it. */
  readonly body: string;
}

export interface ParityDiff {
  readonly command: string;
  readonly path: string;
  /** The preamble: v1's commit, the model, the temperature and the bounds each side ran at. */
  readonly provenance: string;
  readonly sections: ParityDiffSection[];
  /** True when the document says it quotes v1's source. */
  readonly v1SourceWarning: boolean;
}

export function parityDiffPath(command: string, root = repoPaths().parityDiffs): string {
  return join(root, `${command}.md`);
}

/** Commands for which a drill-down has been generated. */
export function listParityDiffs(root = repoPaths().parityDiffs): string[] {
  try {
    return readdirSync(root)
      .filter((name) => name.endsWith(".md"))
      .map((name) => name.replace(/\.md$/, ""))
      .sort();
  } catch {
    return [];
  }
}

export function parseParityDiff(text: string, command: string, path: string): ParityDiff {
  // Sections start at a level-2 heading; everything before the first one is provenance.
  const parts = text.split(/^## /m);
  const preamble = parts[0] ?? "";

  const sections: ParityDiffSection[] = [];
  for (const part of parts.slice(1)) {
    const newline = part.indexOf("\n");
    const heading = (newline < 0 ? part : part.slice(0, newline)).trim();
    const body = (newline < 0 ? "" : part.slice(newline + 1)).replace(/\n*---\s*$/, "").trim();

    const stage = (Object.keys(STAGE_HEADING) as Stage[]).find((candidate) =>
      heading.startsWith(STAGE_HEADING[candidate]),
    );
    if (stage) sections.push({ stage, heading, body });
  }

  return {
    command,
    path,
    provenance: preamble
      .split("\n")
      .filter((line) => line.trim().length > 0 && !line.startsWith("# "))
      .join("\n")
      .trim(),
    sections,
    v1SourceWarning: /Quotes v1 source verbatim/i.test(preamble),
  };
}

export function readParityDiff(command: string, root = repoPaths().parityDiffs): ParityDiff {
  const path = parityDiffPath(command, root);
  if (!existsSync(path) || !statSync(path).isFile()) {
    throw new ParityDiffMissingError(
      `No drill-down for ${command}. Generate one with: python scripts/parity_diff.py ${command}`,
    );
  }
  return parseParityDiff(readFileSync(path, "utf8"), command, path);
}

/** One stage's section, or null when the document has none for it. */
export function sectionFor(diff: ParityDiff, stage: Stage): ParityDiffSection | null {
  return diff.sections.find((section) => section.stage === stage) ?? null;
}
