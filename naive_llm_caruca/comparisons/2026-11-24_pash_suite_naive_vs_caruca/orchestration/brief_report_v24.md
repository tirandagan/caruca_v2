# Brief: Draft 2.4, one Caruca column, and what the two grammar sets really are (2026-11-27)

Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`, editing `report/` and figure
scripts. Records read-only. Keep every rule in `report/README.md` (single set of results, every finding answers its
next question, live links, lettered notes, ACM look). Do not commit.

## Decision (Tiran, 2026-11-27)

The body shows **one Caruca column: Caruca as its paper ran it for PaSh, i.e. the small (PaSh) grammars**
(`caruca-pash-all`, 53 commands). Call it simply "Caruca" in the body. The full-grammar variant
(`caruca-main-all`) moves to one appendix part.

## Correct what the grammars are (facts, checked in Caruca's code and the paper)

- Both grammar sets used here are **hand-written**, not output of Caruca's LLM step: `syntax_specs/` is the
  human-written reference set (the paper's ground truth; ~120 commands), `pash_syntax_specs/` is a hand-trimmed
  version for PaSh's benchmark scripts (54 commands; for the 42 commands in both, 64 options against 923).
- The paper describes one grammar per command written by an LLM from the man page, and never mentions the reduced
  PaSh set; Caruca's code loads `pash_syntax_specs/` when run for PaSh, so the paper's PaSh results came from the
  small grammars (memory: `caruca_v1_class_combining_rule.md` fact 5; `caruca_paper_review_2026_11.md` Q2).
- So the comparison is: files written by a naive LLM from the goal, formats and examples, against files Caruca
  derived by tracing commands under **hand-written** grammars. Say this plainly in "How it was run" and in the
  threats section (if anything it favours Caruca). Fix every definition that calls the small grammar "written for
  PaSh's scripts" without saying it is hand-written, and remove any implication that Caruca's grammars came from an
  LLM here. Footnote 1 keeps the two repository paths.

## Consolidate

- Every body table and figure: four columns/series become three: PaSh's own files, the naive LLM, Caruca (small
  grammars). Keep the column order. Recount nothing; take the small-grammar numbers already in the records/numbers
  files (output 77 of 86 right, wrong in 9; splits 29 of 86 scripts, 29 of 177 parts; compiler stops 11; time 1.09 of
  PaSh's own; start-up removed 1.05 against bash; reads/writes and split-decision agreement from Table 5/numbers).
- Wrong-output section: lead with the 9 scripts under Caruca as run by its paper; one sentence that with full
  grammars where traceable it was 10 (8 shared), and point to the new appendix part. The callout under the title:
  "The naive LLM's files never changed PaSh's output; Caruca's changed it in 9 of 86 scripts." (short, as Tiran asked).
- New appendix part "Caruca with its full grammars" (one page): what differs (22 commands traced with the full
  grammar at up to 2 options per run, small grammar for the rest), a small table small vs full on every Table 1 row,
  and three sentences: full grammars split more (40 scripts against 29) and stop PaSh's compiler less (3 against 11,
  because the small grammar lacks options such as `sort -r`, `-n`), but do not fix correctness (10 wrong, 8 shared),
  because the wrong outputs come from how Caruca merges test results and from its test inputs, not from which options
  it knows. Link it from Table 1's Caruca header note and from section 2.
- Figures 2, 3, 4 and A.8 drop the full-grammar series (keep it only in the new appendix part, as a table, no figure
  needed). Figure scripts: add a flag rather than deleting code.
- Recheck every sentence that names "small" or "full" in the body; the body says "Caruca" only.

## Also
- Add `report/.page_labels.json` to `.gitignore` (repo root) or write it to /tmp instead.
- Version "Draft 2.4, 27 November 2026". Build, verify links and outline as last time, render every page, no page
  over a third empty before the last, Table 1 on page 1.
Reply in at most 8 lines: page count, link/outline counts, the Table 1 Caruca column as built, anything not done.
