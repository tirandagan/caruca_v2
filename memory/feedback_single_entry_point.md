---
name: feedback-single-entry-point
description: 2026-10-27 Tiran: the analysis/docs folders are confusing; naive LLM vs v1 is the primary focus; one entry point (naive_llm_caruca/README.md) and one dated findings list (naive_llm_caruca/latest_findings.md) must be kept current
metadata:
  type: feedback
---

**What Tiran said (2026-10-27):** "our analysis folder and docs folder are very confusing. i need your
help to sort what is important and what is dated. the most recent findings on naive llm vs v1 are the
primary focus … we need a much more structured organization and linking of the files in a single
'directory' approach." Earlier the same day: findings must be dated, "since we have been progressively
adding information", in one file with date, time, a plain-English synopsis and a link to the details.

**What exists as a result (2026-10-27):**
- `naive_llm_caruca/README.md`: the directory (top part; the operator notes and prompt-version log follow
  below it in the same file). Read first, where each answer lives, run table
  (every run's analysis, PDF and diagrams), the five diagram kinds, tools, background that still holds,
  and the dated September–October rebuild material.
- `naive_llm_caruca/observations.md`: the simple document (quality, speed, scores, file samples
  side by side, approaches alike/different).
- `naive_llm_caruca/latest_findings.md`: every finding, newest first, date + time it was written into its
  document (git blame; file save time if uncommitted), plain synopsis with number and total, link.
- `ai_docs/README.md` and `ai_docs/analysis/README.md` carry a "Start here" pointer to the directory.

**Why:** Tiran could not find the current material among Sept–Oct rebuild documents, and numbers drifted
between documents (a "numbers that disagree" table lives at the end of latest_findings.md).

**How to apply:**
- Every new naive-LLM finding goes into `latest_findings.md` (top of its day, with time and link) in the
  same turn, and any new document or diagram gets a row in the directory README.
- **Dating a finding:** this repo's commits are often bulk commits (many documents share 2026-10-13
  12:48), so a commit time says when text was *written up*, not when the finding was made. Give the date
  the document itself states for the finding, and the `git blame` time of the line as "written up";
  use the file's save time for uncommitted text.
- **Re-check a count against its primary source before restating it** in a summary, a diagram or chat.
  On 2026-10-27 "the agent overstated its testing in four runs" had to become six (the run analyses said
  six). Extracting findings across documents turned up about 30 places where two documents give different
  numbers for one quantity; the main ones are tabulated at the end of `latest_findings.md`.
- **The full reorganisation was done on 2026-10-27 (Tiran: "both").** Into `naive_llm_caruca/`: the
  addendum and its PDF, `syntax_files_vs_v1.md` (renamed from `naive_llm_syntax_files_vs_v1.md`),
  `latest_findings.md`, and `diagrams/003_…`. Into `ai_docs/archive_2026-09_rebuild/` (with its own
  README): the rebuild's analysis documents, status reports, v2 operating docs, the September handouts and
  the 001/002 diagrams. `ai_docs/analysis/` keeps E0, the `grep`/purpose case, PaSh scheduling and the
  console's `findings/` folder, which must NOT move: the console reads it by default
  (`console/src/data/paths.ts` line 106). 53 files' references were rewritten; the link check showed no new
  broken links against a pre-move baseline of 92 (all older). `CLAUDE.md` points at the new layout.

Related: [[feedback-plain-language]], [[project-naive-claude-code-arm]], [[feedback-naive-llm-standalone]].

**Moved 2026-10-27 (Tiran's call):** the start page and `observations.md` were first written to
`ai_docs/naive_llm_vs_v1/`; Tiran said that folder was "part of the mess of documents" and had them moved
into the experiment folder `naive_llm_caruca/`, the start page *merged into the top of* the existing
operator README (operator title became "Operator notes (for the experimenter)"; all its section headings
and anchors kept). All 201 links in the touched files were re-checked (0 broken). The agent never sees
either file: `sync_to_vm.sh` copies only `PROMPT_v*.md`, `formats/`, `samples/` by name. Keep the
documents about the naive experiment in `naive_llm_caruca/`, not under `ai_docs/`.
