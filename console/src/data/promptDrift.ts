/**
 * Has a run's prompt changed since the run was made?
 *
 * This matters because prompt files are edited. Task 009 rewrites stage 1's prompt outright,
 * and the generate prompt already changed after 2026-09-08. A run whose prompt file no longer
 * matches what it sent is a run whose numbers describe a system that no longer exists, and
 * reading today's file as if it were that run's prompt misattributes the result.
 *
 * **Neither obvious method works.**
 *
 *   - Comparing the file to the recorded prompt fails: the files are *templates* containing
 *     `{{invocation}}`-style placeholders, and the manifest records the *rendered* text. A
 *     direct comparison reports drift on every run ever made.
 *   - Comparing `prompt_hash` fails for the same reason: `prompting.py::hash_prompt` hashes
 *     the rendered system and user messages, not the templates. It distinguishes two prompts
 *     from each other; it cannot tell you whether a template was edited afterwards.
 *
 * So the check works on what a template and its output must share: **the literal text between
 * the placeholders.** Every such segment of today's template must appear, in order, in what
 * the run sent. If one is missing, the template's wording changed.
 *
 * The direction of error is deliberate. A changed template cannot escape detection, because
 * its new literal text cannot appear in an older rendering. A false alarm is possible only if
 * a substituted value happened to contain text that breaks the ordering, which placeholder
 * values do not do. Across the 135 runs on disk this reports drift for exactly one, and that
 * one is genuine.
 */
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { repoPaths } from "./paths.js";

export type DriftVerdict = "unchanged" | "changed" | "missing";

export interface PromptFileDrift {
  readonly file: string;
  readonly verdict: DriftVerdict;
  /** The first piece of today's template that is absent from what the run sent. */
  readonly firstMissingSegment: string | null;
  /**
   * Where the two actually diverge.
   *
   * Reporting the *start* of the changed segment is nearly useless: a segment usually begins
   * at the top of the file, so the quoted text looks identical to what the run sent and the
   * whole report reads as a false alarm. What a reader needs is the point at which today's
   * wording stops matching, with a little of the text that still agreed in front of it.
   */
  readonly divergence: PromptDivergence | null;
}

export interface PromptDivergence {
  /** The tail of the text that still matched, for orientation. */
  readonly matchedBefore: string;
  /** What today's template says from the point of divergence onwards. */
  readonly templateSays: string;
}

/** `{{ name }}` with any surrounding space. */
const PLACEHOLDER = /\{\{\s*[A-Za-z0-9_]+\s*\}\}/g;

/**
 * The literal text between placeholders.
 *
 * Whitespace-only pieces are dropped: two adjacent placeholders separated by a newline carry
 * no wording, and matching on whitespace alone would find a match anywhere.
 */
export function literalSegments(template: string): string[] {
  return template
    .split(PLACEHOLDER)
    .map((segment) => segment.trim())
    .filter((segment) => segment.length > 0);
}

const CONTEXT = 70;

/**
 * How much of `segment` can still be found in `rendered` from `position`.
 *
 * Findability is monotone - if a prefix of length n is present then so is every shorter one -
 * so this binary-searches rather than walking back a character at a time.
 */
function longestFindablePrefix(segment: string, rendered: string, position: number): number {
  let low = 0;
  let high = segment.length;
  while (low < high) {
    const middle = Math.ceil((low + high) / 2);
    if (rendered.indexOf(segment.slice(0, middle), position) >= 0) low = middle;
    else high = middle - 1;
  }
  return low;
}

function divergenceOf(segment: string, rendered: string, position: number): PromptDivergence {
  const shared = longestFindablePrefix(segment, rendered, position);
  return {
    matchedBefore: segment.slice(Math.max(0, shared - CONTEXT), shared).trimStart(),
    templateSays: segment.slice(shared, shared + CONTEXT),
  };
}

/** Every segment of `template` present, in order, in `rendered`. */
export function templateMatchesRendered(
  template: string,
  rendered: string,
): {
  matches: boolean;
  firstMissingSegment: string | null;
  divergence: PromptDivergence | null;
} {
  let position = 0;
  for (const segment of literalSegments(template)) {
    const found = rendered.indexOf(segment, position);
    if (found < 0) {
      return {
        matches: false,
        firstMissingSegment: segment,
        divergence: divergenceOf(segment, rendered, position),
      };
    }
    position = found + segment.length;
  }
  return { matches: true, firstMissingSegment: null, divergence: null };
}

/**
 * Check each of a run's prompt files against the prompt it actually sent.
 *
 * `promptFiles` is ordered `[system, user]` by `prompting.py::build`, which is why the
 * recorded messages are paired positionally rather than by filename.
 */
export function checkPromptDrift(
  promptFiles: readonly string[],
  system: string,
  user: string,
  root = repoPaths().root,
): PromptFileDrift[] {
  const rendered = [system, user];

  return promptFiles.map((file, index) => {
    const absolute = file.startsWith("/") ? file : join(root, file);
    if (!existsSync(absolute)) {
      return { file, verdict: "missing" as const, firstMissingSegment: null, divergence: null };
    }
    const recorded = rendered[index];
    if (recorded === undefined) {
      return { file, verdict: "missing" as const, firstMissingSegment: null, divergence: null };
    }
    const result = templateMatchesRendered(readFileSync(absolute, "utf8"), recorded);
    return {
      file,
      verdict: result.matches ? ("unchanged" as const) : ("changed" as const),
      firstMissingSegment: result.firstMissingSegment,
      divergence: result.divergence,
    };
  });
}
