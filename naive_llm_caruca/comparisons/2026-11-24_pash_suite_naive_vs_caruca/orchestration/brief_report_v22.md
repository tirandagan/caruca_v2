# Brief: report Draft 2.2, answer the reader's questions where they arise (2026-11-27)

You are the report worker. Read `report/README.md` (framing, typography, rules), `memory/feedback_single_results.md`,
`memory/feedback_report_metrics_in_pdf.md`, `memory/feedback_greenberg_report_style.md`, then the current
`report/report.html` (Draft 2.1). Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`.
Edit `report/` (and a figure script only if needed). Records are read-only. Do not commit.

Tiran's reading of Draft 2.1 (2026-11-27): "I have to hunt for information all over the place. This should be
easier to read." Every finding must answer its obvious next question on the spot or point to exactly where the
detail is. Rules for this round:

1. **Cross-reference everywhere detail exists.** Every Table 1 row, every Table 2 row and every body claim that has
   more detail in a section or appendix part names it ("(Table A.5)", "(A.7)", "(section 5)"). Check every
   paragraph of the body for this.

2. **Table 1, Time row: one number per source.** Use time against PaSh's own files: PaSh's own `1.00`, sub
   "the reference"; naive `1.15`; Caruca small `1.09`; Caruca full `1.10`; row label "Time, against PaSh's own
   files (lower is better)", with "(section 5)". No second line in the cells. The ×bash figures move to section 5.

3. **Compiler stops: show the overlap in the body.** In "When PaSh itself failed", add a small table (rows = the
   stopped parts grouped by cause, columns = the four sources, ✕ or –, last column the cause), taken from this
   count over both runs' `regions.jsonl.gz` (outcome "pash crash", instrumented, main, repeat 1):

   | Stopped part | PaSh's own | Naive | Caruca small | Caruca full | Cause |
   |---|---|---|---|---|---|
   | oneliners/bi-grams | ✕ | ✕ | ✕ | ✕ | PaSh bug, NameError (issue 794) |
   | covid/5 | ✕ | ✕ | – | – | awk program text read as a file |
   | unixfun/12, unixfun/16 | ✕ | – | – | – | PaSh's own `tail -n 1` file |
   | unixfun/34, unixfun/36 | – | ✕ | – | ✕ | `fmt -w1`: the value read as a file name (check 36 in the logs: the earlier draft also named the naive LLM's quoted sed script; use what the records say) |
   | 10 parts: top-n, wf, sort-sort, unixfun/4, 10, 11, 14, 17, covid/1, 4 | – | – | ✕ | – | `sort -r`/`-n` missing from the small grammar, read as file names |
   | Total | 4 | 4 | 11 | 3 | |

   Then two sentences: the naive LLM shares 2 of its 4 stops with PaSh's own files, avoids PaSh's own 2 (its `tail`
   file is right) and adds 2 of its own (`fmt`), the same 2 as Caruca's full grammar; every stop ran as plain
   bash, so no stop changed an output. Point to Table A.5 (error text) and Table A.8 (scripts).

4. **Explain the time, in the body (section 5), before the figure.** Two short paragraphs, numbers from the
   records (`full_run/numbers.md`, `full_run_caruca_all/numbers.md`, `numbers_full.json`, per-script table):
   (a) Why PaSh is slower than bash here at all (2.3 × bash with its own files): Koala's small inputs make most
   scripts run in under a second under bash (give the count, e.g. "n of 86 under 1 s"), while PaSh pays a start-up
   and a compile for every part, and the natural-language scripts call PaSh's compiler once per loop pass; give
   two scripts where splitting does pay (e.g. oneliners/nfa-regex 8.2 s to 1.9 s; the COVID scripts with PaSh's own
   files) and say parallelism pays only when the work per piece outweighs that overhead, so these times say little
   about larger inputs (threats). (b) Why the naive LLM's files are slower than PaSh's own (1.15): not because they
   are "more comprehensive" in general, but because they split cheap commands PaSh's own files leave whole: a plain
   `cat` (25 scripts where it is the only difference: 1.21×), and the COVID scripts where its first sed file left
   sed whole. Caruca: same overhead, fewer extra splits (1.09/1.10). Point to Figure 4 and Figure A.7 for the
   per-script picture.

5. **New appendix part: "Caruca's wrong outputs, side by side"** (place it right after A.4 or as a new A part,
   renumber, and reference it from section 2 and Table 3). Use `full_run_caruca_all/wrong_output_examples/`
   (`summary.json`, `*.out`, `*.diff`): four outputs re-generated with the batch's own runner, each identical (by
   checksum) to the wrong output the batch recorded. For each of the four, a compact block: the pipeline (one
   line), the command Caruca let split, then a concise diff view in mono (bash on the left or first, Caruca after;
   at most 8 lines each; mark removed/added lines with − and +), and one sentence saying what went wrong:
   - unixfun/23 (`tr -d '\n' | cut -c 1-4`): bash prints 4 letters (5 bytes); Caruca's prints 31 lines of 4
     letters (155 bytes), one per 1 MB block.
   - oneliners/top-n (`… | sort -rn | sed 100q`, full grammar): bash 100 lines; Caruca 800 lines, the top 100
     of each of 8 pieces.
   - oneliners/spell (`… | sort | uniq | comm -23 - dict`, small grammar): bash 1,234 lines; Caruca 1,261: words
     repeated where pieces meet (show 3 to 4 diff lines from the .diff).
   - unixfun/26 (`… | sed 4d | cut … | tr -d '\n'`): one line either way, 3,044,246 vs 3,044,195 bytes: bash
     deletes the 4th line of the whole stream, Caruca's split deletes the 4th line of every piece (51 bytes, 7 more
     short fields, lost). Say it in words; a byte diff is not needed.
   Add the folder to the records table.

6. Keep everything else. Version "Draft 2.2, 27 November 2026". Build, render every page, keep Table 1 on page 1,
   no page before the last more than a third empty, no split tables. Update `report/README.md` with the rule:
   "every finding answers its next question on the spot or points to where it is answered".
Reply in your pane in at most 8 lines: page count, the new tables/parts and their numbers, anything not done.
