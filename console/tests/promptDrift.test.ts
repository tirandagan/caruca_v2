/**
 * The prompt-drift check.
 *
 * The first version of this check compared the prompt file to the recorded prompt directly and
 * reported drift on all 135 runs, because the files are templates and the manifests record
 * rendered text. These tests exist mostly to keep that mistake from coming back: the first two
 * pin the two ways of being wrong, and the last two run the check over every run on disk.
 */
import { describe, expect, it } from "vitest";
import {
  checkPromptDrift,
  literalSegments,
  templateMatchesRendered,
} from "../src/data/promptDrift.js";
import { listRuns, loadRun } from "../src/data/runs.js";

const TEMPLATE = "## Command\n\n`{{command}}`\n\nEvery `stdin` value must be one of: {{values}}\n";
const RENDERED = "## Command\n\n`grep`\n\nEvery `stdin` value must be one of: a, b\n";

describe("template matching", () => {
  it("does not call a substituted placeholder a change", () => {
    // The whole point: `{{command}}` becoming `grep` is not drift.
    expect(templateMatchesRendered(TEMPLATE, RENDERED).matches).toBe(true);
  });

  it("catches wording added to the template after the run", () => {
    const older = "## Command\n\n`grep`\n";
    const result = templateMatchesRendered(TEMPLATE, older);
    expect(result.matches).toBe(false);
    expect(result.firstMissingSegment).toContain("stdin");
  });

  it("points at where the wording actually diverges, not at the start of the segment", () => {
    // Reporting the start of the changed segment is nearly useless: a segment usually begins
    // at the top of the file, so the quoted text looks identical to what was sent and the
    // report reads as a false alarm.
    const today = "Describe the command.\nBe exhaustive about flags.\n";
    const asSent = "Describe the command.\n";
    const result = templateMatchesRendered(today, asSent);

    expect(result.matches).toBe(false);
    expect(result.divergence?.matchedBefore).toContain("Describe the command.");
    expect(result.divergence?.templateSays).toContain("Be exhaustive about flags.");
    // And the divergence marker does not simply repeat the whole segment back.
    expect(result.divergence?.templateSays.startsWith("Describe")).toBe(false);
  });

  it("reports the divergence on the real drifted run, not the file's opening words", () => {
    const drift = checkPromptDrift(
      ["prompts/generate/system.md"],
      loadRun(
        listRuns().runs.find((r) => r.runId === "2026-09-08T201630Z_grep_48518d16")!.dir,
      ).manifest.prompt_system,
      "",
    );
    const divergence = drift[0]!.divergence!;
    expect(divergence.matchedBefore.length).toBeGreaterThan(0);
    expect(divergence.templateSays.length).toBeGreaterThan(0);
    // The two genuinely share their opening, so a useful report must begin further in.
    expect(divergence.templateSays.startsWith("You are given")).toBe(false);
  });

  it("requires the segments in order, so a reshuffled template is a change", () => {
    const reordered = "Every `stdin` value must be one of: a, b\n\n## Command\n\n`grep`\n";
    expect(templateMatchesRendered(TEMPLATE, reordered).matches).toBe(false);
  });

  it("ignores whitespace-only gaps between adjacent placeholders", () => {
    // Two placeholders with only a newline between them carry no wording to match on.
    expect(literalSegments("{{a}}\n{{b}}")).toEqual([]);
    expect(templateMatchesRendered("{{a}}\n{{b}}", "anything at all").matches).toBe(true);
  });
});

describe("against the runs on disk", () => {
  const runs = listRuns().runs;

  it("reports no drift for the great majority of runs", () => {
    // If this starts failing wholesale, the check has reverted to comparing rendered text to
    // a template, which is always false.
    const drifted = runs.filter((summary) => {
      const m = loadRun(summary.dir).manifest;
      return checkPromptDrift(m.prompt_files, m.prompt_system, m.prompt_user).some(
        (check) => check.verdict === "changed",
      );
    });
    expect(drifted.length).toBeLessThan(runs.length * 0.05);
  });

  it("still catches the one run whose prompt genuinely changed afterwards", () => {
    // prompts/generate/ gained a sentence constraining `stdin` values after 2026-09-08.
    const run = loadRun(
      runs.find((summary) => summary.runId === "2026-09-08T201630Z_grep_48518d16")!.dir,
    );
    const drift = checkPromptDrift(
      run.manifest.prompt_files,
      run.manifest.prompt_system,
      run.manifest.prompt_user,
    );
    expect(drift.every((check) => check.verdict === "changed")).toBe(true);
    expect(drift.some((check) => check.firstMissingSegment !== null)).toBe(true);
  });

  it("reports a prompt file that is no longer on disk as missing, not as unchanged", () => {
    const drift = checkPromptDrift(["prompts/gone/system.md"], "x", "y");
    expect(drift[0]!.verdict).toBe("missing");
  });
});
