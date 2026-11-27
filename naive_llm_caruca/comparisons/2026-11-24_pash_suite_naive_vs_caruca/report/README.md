# The report for Michael: how it is built and how to update it

The report is hand-authored HTML, not converted Markdown, so its layout can be exact: `report.html`
(content) and `report.css` (layout), rendered to `report.pdf` by `build.ts` with the repo's own brand
fonts and colour tokens (`scripts/md-to-pdf/tokens.ts`); the running head and foot are stamped on afterwards with pdf-lib in the brand face (Chromium's own header templates cannot load it), so it stays
one system with the other Caruca documents. The earlier Markdown draft (`report_draft.md`, 2026-11-24) was removed on 2026-11-26 and is in
git history; it is no longer the source.

## Build

```sh
cd <repo root>
npx tsx naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/report/build.ts
# optional second argument: the running-head title
```

It prints the page count. To look at the pages: `pdftoppm -r 70 -png report/report.pdf /tmp/p`.

## Structure (the "comparison board", chosen by Tiran on 2026-11-24; reworked in round 3, 2026-11-26)

The four annotation sources are four columns that run through every table: PaSh's own files (the
reference, dark grey; the only tinted column), the naive LLM's (blue), Caruca's small grammar (orange),
Caruca's full grammar (light orange). The same four colours are used in the figures. A cell that differs
from the reference is set in weight 600 with a 1 pt left rule in its source's colour, never tinted.

Body, 4½ pages: page 1 = title, one-line finding, version line, the question, "How it was run" (the eight
words a reader needs, one sentence each) beside the `spell.sh` box and Figure 3, then Table 1 (the board)
with its two-sentence footer; "Where the sources differ" (Figure 1, the five vetted causes); "When PaSh
itself failed" (three sentences); "Time" (Figure 2, four one-sentence findings); "Next to the Caruca paper"
(Table 3, counting rule as the note beneath); "What this does not show (threats to validity)". Time has one
convention everywhere: time ÷ bash time (or ÷ PaSh's own), lower is better.

Addendum (starts after the body, no forced page break): A1 the script on page 1; A2 the words not defined
on page 1; A3 the setup for a reader new to PaSh; A4 why parts were not split (Table A4, distinct parts,
reasons split into "same as PaSh's own" / "only here"; the naive LLM's 31 parts named; the crash causes in
full); A5 the scripts (nine group blocks, two columns, kept whole); A6 where a source changed
what PaSh split, by command (Table A6 = the body's old Table 2 + a command-lines column);
A7 every script on one page (Figure A7, chart + crash list; starts a page); A8 records (a two-column table, incl. PaSh commit, worker
count and the pointers to the per-use list and the per-script min–max times in `numbers_full.md`).
A1–A9 are numbered without gaps; update every "(A…)" reference in the body when a section moves.

## Rules the layout follows

- Every table and figure is numbered and referred to by number in the text.
- Every finding answers its next question on the spot or points to where it is answered: each row of Tables 1 and 2
  and each body claim with more detail elsewhere names the section, table or appendix part ("(Table A.4)", "(section 5)").
- Every rate is written "a of b". No kicker/eyebrow labels, no coloured side stripes, no section numbers.
- One noun per concept: annotation files, source, part, split / whole, the naive LLM, Caruca's small grammar /
  Caruca's full grammar, the second sed file. Script codes, exception names and file paths only in the addendum.
- Page breaks: only `class="page-break"` sections force a new page (A7); everything else flows. Tables
  and figures do not break inside. Check that no page before the last is more than a third empty.
- Figures are referenced relative to this folder (`../figures_full/*.png`); regenerate them from the run folder with
  `uv run --with matplotlib==3.9.2 python figures_interim/make_figures_interim.py --records full_run --numbers numbers_full.json --out figures_full`
  and rebuild. That one call draws Figure 1 (`split_map.png`), Figure 2 (`time_bars.png`), Figure 3
  (`setup_diagram.png`), A7's chart (`a5_scripts.png`) and the unused `uses_split.png`, and checks its counts
  against the numbers json (it stops on a mismatch).
- Figure 3 is now drawn by the figure script at column width (2.9 in) in Lexend Deca, so it reads at the size
  it sits on page 1. The Excalidraw renderer (`.claude/skills/excalidraw-diagram/references/render_excalidraw.py`)
  only knows Excalidraw's built-in font families and cannot take Lexend Deca; the long-form drawing
  `../figures_full/setup_diagram.excalidraw` is kept as the record but no longer rendered into the report.
- `make_a5_rows.py` was deleted in round 3: A7 is a chart drawn by the figure script, and Table A6 has nine
  hand-written rows from `numbers_full.md` ("Full run: commands gained and lost", "Per command").

## How the full run was folded in (Draft 1.0, 2026-11-26)

Records in `../full_run/` (gzipped) are expanded by `../prep_full_records.py`, counted by `../count_report.py --tag full`
into `../numbers_full.md/.json`, drawn into `../figures_full/`, and every number in `report.html` was replaced from
that file; the sed v2 file is a labelled extra row, never a column. The independent check is
`../orchestration/review_checker_full.md`.

## Round 2 (2026-11-26)

Restored Tiran's metrics in the addendum (A4–A6), added the crash row to Table 1 and "When PaSh itself
failed" to the body, and fixed the design review's defects. The crash cause was read from PaSh's logs in the
`pash` VM (`~/t024/out/logs/`): every `AssertionError` is `compiler/ir.py:596` in `pipe_append`
(`assert not other_in is None`: the command after a `|` has no standard input in its file's answer), not
the annotation package's round-robin assertion; the `NameError` is `create_reduce_tree` (`ir.py:1454`).

## Updating again

1. Rebuild the records with `../count_report.py` and the figures with
   `../figures_interim/make_figures_interim.py`.
2. Replace the numbers in `report.html` from `numbers.md` (every number in the report comes from that
   file). Keep the four-column structure; add rows, never columns.
3. Bump the version line, rebuild, look at every page once, run the finish review (the impeccable skill's
   reviewer) on the page renders.

## Round 3 (2026-11-26, brief `orchestration/brief_report_round3.md`)

Rewritten for clarity after the design critique (`.impeccable/critique/2026-11-26T09-13-23Z__…md`): method
before results, one time convention, number strings moved into tables and figures, the addendum condensed
(A5, A6, A7 one page each). 23 pages became 10. Numbers added in this round, all from the records:
"without `cat`" scripts (41, 43, 27, 39 of 86; 14 of 52), from `full_run/occurrences.jsonl.gz` (scripts with a
split use of a command other than `cat`); time ÷ bash time = 1 / the speed-up geometric mean in
`numbers_full.json` (2.35, 2.70, 2.47, 2.49; 1.96 for the second sed file); distinct command lines per
command in Table A6, from `numbers_full.json` `A4`; and the naive LLM's 31 "other, not classified" parts,
read from `full_run/regions.jsonl.gz` (reason text): 30 single-`mkdir` parts and 1 single-`mogrify` part
whose naive files declare a non-stream output, which PaSh logs as "has outputs other than streaming".


Order fixed by the orchestrator after round 3 (2026-11-26): figures renumbered in reading order (setup = Figure 1,
splits = Figure 2, time = Figure 3); addendum order A4 reasons, A5 scripts, A6 by command, A7 chart, A8 records, so that
no appendix page is more than a third empty.

## Typography: ACM conference style (Tiran, 2026-11-26)

The PDF follows the ACM `acmart` class in its `acmsmall` form, which ISSTA requires (single column, serif text):
Libertinus Serif for text (the maintained Linux Libertine), Libertinus Sans bold for headings in black,
Inconsolata for code, 10 pt on 12 pt, justified with hyphenation, numbered sections (the addendum is appendix A,
parts A.1 to A.8), booktabs-style tables, captions in small sans with a bold "Figure n:" label. Fonts live in
`scripts/md-to-pdf/fonts/academic/` (OFL licences beside them). Chromium embeds CFF OpenType as Type 3, so
`build.ts` loads the TrueType conversions in `academic/ttf/` (made with fontTools: cu2qu for the Libertinus
files, `varLib.instancer` for a static Inconsolata); the running head and foot are stamped with the same
TrueType files, unsubsetted (pdf-lib garbles subsetted copies of these conversions). The figure script registers
Libertinus Sans and Inconsolata so figures match. The brand (Lexend Deca) rules in `report.css` remain above the
academic block and are overridden by it; remove the block to go back to the Caruca house style.
Regenerate figures with `uv run --with matplotlib --with numpy python figures_interim/make_figures_interim.py --records full_run --numbers numbers_full.json --out figures_full`.

## Framing (Tiran, 2026-11-26)

The report's one question is how the naive LLM's files fared against Caruca's, with PaSh's own files as the
yardstick for both. The title, the finding line under it, the question on page 1 and section 1 ("The naive LLM
against Caruca", Table 2 head to head: reach, uses decided, output, splits, compiler stops beyond PaSh's own, files
that failed to load, wrong decisions, agreement on reads and writes, time) all state it in those terms. Every
figure caption says why its items were chosen (Figure 2's eight commands are every command that differed under
any source). Keep this framing when numbers are refreshed.

**One set of results in the body (Tiran, 2026-11-27, Draft 2.1):** the body presents a single set of results across
the board—one number per source, no "first session / second session" split in tables, text, or Figure 4. Each
source's time is already normalised to bash and to PaSh's own files run alongside it; the two sessions are
described only in the method appendix (A.3) and the records table (A.9).

Figure 2 (`figures_full/scorecard.png`, drawn by `figures_interim/make_scorecard.py` from hand-fed values with their
sources in comments) is the Tufte-style summary: every metric as a fraction of PaSh's own files' result on one axis.
Table A.5 is the cause analysis of every compiler stop from PaSh's error text.

## Additions 2026-11-26 (afternoon)

- Section 2 "The naive LLM against PaSh's own files, command by command" with Table 3: the 18 commands both
  sources have files for, uses split under each (126 vs 192 of 484), "no split" answers, compiler stops; the 5
  naive-only commands that met a part in the caption. Counts from `../per_command.md/.json` (`../per_command.py`).
- Corrections from that count: the naive LLM's time gap to Caruca's full grammar is 9 % over 86 scripts; about
  two-fifths comes from splitting a plain `cat` (25 scripts where it is the only difference: 1.21×), about a
  quarter from the four COVID scripts. The fixed `sed` file is compared on the same 52 scripts only (8 % → 3 %).
- Footnote 1 on page 1 gives where Caruca's two grammars live in `binpash/caruca`.

## Draft 2.0 (2026-11-27): Caruca at full reach (brief `orchestration/brief_report_caruca_full.md`)

Caruca's two columns now come from the second session (`../full_run_caruca_all/`: Caruca's files for 53 commands,
full grammar for 22 of them); the naive LLM's from the first (`../full_run/`). Rule: every time is a ratio to PaSh's
own files of the same session; splits and output compare across sessions because PaSh's own files split the same 41
parts and the same 126 of 609 uses in both (checked per use by the figure script, which stops otherwise).

- Counts: `../prep_full_records.py --records full_run_caruca_all --out <scratch>` (it now skips the optional files
  the rerun lacks), then `../count_report.py --records <scratch> --tag caruca_all --sleep-events <empty file>` (no
  sleep in the window per `pmset -g log`; the Mac was on mains, `full_run_caruca_all/power_watch.tsv`) →
  `../numbers_caruca_all.md/.json`. 13 of 15 checks pass; the 2 failures are the inventory checks that also fail on
  the first run.
- Figures: `uv run --offline --with matplotlib --with numpy python figures_interim/make_figures_interim.py --records
  full_run --numbers numbers_full.json --caruca-records full_run_caruca_all --caruca-numbers numbers_caruca_all.json
  --out figures_full`. Figure 4 (time) now has two blocks, one per session, each with its own noise band; A.7 adds a
  cross for wrong output. Figure 2: `figures_interim/make_scorecard.py` (values and sources in its comments).
- New body section 2, "Where Caruca's files give wrong output" (Table 3), from
  `../full_run_caruca_all/wrong_outputs_verified.md`. Table 4 is now one combined command-by-command table for all
  three sources. Sections reordered: Time (Figure 4) before "Next to the Caruca paper" (Table 5), for page fill.
- Addendum: A.1 is now the word list and A.2 the suite (swapped so the page after the body fills); the
  wrong-output script list and Table A.8 (compiler stops) sit under A.6 so A.7's chart keeps its own page.
- `unixfun/23` (`tr -d '\n'` then `cut`), explained after the orchestrator's log check: the naive LLM's `tr` file offers
  only consecutive chunks when newlines may be touched (round robin regroups by line), so PaSh rejoined before `cut`;
  Caruca's file also offers round robin, so PaSh ran `tr` and `cut` per 1 MB block. Credited in "How it fared" and Table 3;
  recorded in the notes of `../numbers_caruca_all.md`.
- Review fixes: footnote 1 restored on page 1 (Table 1's notes moved into its title line to make room); Figure 2 redrawn
  4.6 → 3.7 in tall (same font sizes) so Table 3 fits under it on page 3.
- 14 pages (body 7, addendum 7).

## Draft 2.2 (2026-11-27, brief `orchestration/brief_report_v22.md`)

Tiran: "I have to hunt for information all over the place." Changes:
- Cross-references on every row of Tables 1 and 2 (small grey `.xref` after the label) and in the body paragraphs.
- Table 1's time row is one number per source, against PaSh's own files (1.00, 1.15, 1.09, 1.10); the × bash figures
  (2.3, 2.7, 2.5, 2.5) moved to section 5.
- New Table 5 in "When PaSh itself failed": the stopped parts by cause, ✕ per source, from both runs' `regions.jsonl.gz`
  (outcome "pash crash", instrumented, main, repeat 1). The paper table is now Table 6. Correction from the logs: the
  naive LLM's `unixfun/36` stop is `fmt -w1` (PaSh's log shows `-w1` taken as a file name; the second sed file stops
  there too), not its quoted `sed` script; Table 2, A.4 and Table A.5 were corrected.
- Section 5 opens with two paragraphs: why PaSh is slower than bash at these inputs (45 of 86 scripts under 1 s under
  bash; per-part start-up and compile; loops compile once per pass; splitting pays in the Classics regular-expression
  script, 8.2 s to 1.9 s, and the four COVID scripts, 10–15 s to about 7 s) and why the naive LLM's files are slower than
  PaSh's own (cheap `cat` splits, 1.21× where it is the only difference; the first sed file in the COVID scripts).
  Per-script seconds from `numbers_full.json` `A5`.
- New A.7 "Caruca's wrong outputs, side by side" (four examples from `full_run_caruca_all/wrong_output_examples/`);
  the chart is now A.8 (Figure A.8), records stay A.9. A.7 sits after Table A.8 so that page fills.
- `h2.paper` no longer forces a page; the records table is set tighter (`table.recs`) so it stays under its heading.
- 15 pages.

## Draft 2.2, second pass (2026-11-27, orchestrator)

- Time: Table 1 has two time rows (÷ PaSh's own; ÷ bash with PaSh's start-up removed, one-pass scripts) and section 5
  has the overhead model and Table 6 from `../overhead_adjusted.md` (`../overhead_adjusted.py`); the paper table is now
  Table 7. Web search: 7,003 parts sent, so the model gives about 42 s of overhead (0.11 s + 6 ms × 7,003), not 36 s.
- Live cross-references: every section heading (`sec-n`), appendix part (`a-n`), table caption (`tab-…`) and figure
  (`fig-…`) has an id; Tables 1 and 2 use numbered footnotes (`fn1`–`fn19`, one document-wide sequence, Table 1's notes
  share the block with footnote 1); every "Table n", "Figure n", "section n" and "A.n" in running text is an
  `<a class="xr">` (ink colour, no underline). The links were added by a one-off script (kept in the session scratchpad,
  not the repo); when adding text, write the `<a class="xr" href="#…">` by hand. Check after a build with pypdf:
  count `/Link` annotations and confirm every `/Dest` is a named destination.

## Draft 2.3 (2026-11-27, brief `orchestration/brief_report_v23.md`, critiques `orchestration/critique_2026-11-27_*.md`)

Conventions now in force (keep them when editing):
- **Links look clickable.** Every internal link (`a.xr`), table-note mark (`a.tn`), body footnote mark and back-link is
  `--link` #3B3F99 with a 0.5 pt dotted underline (offset 1.5 pt); marks are bold. Write new cross-references as
  `<a class="xr" href="#id">Table 4</a>`; ids: `sec-n`, `a-n`, `tab-n`/`tab-aN`, `fig-n`/`fig-aN`, `app`, `run`,
  Table 1 rows `t1r-*`.
- **Page numbers in references are added by the build** (two passes): pass 1 renders with links to every id appended
  after the document, reads each id's page from the PDF's named destinations, then adds ", p. N" after every `a.xr`
  whose target is on another page (not in the contents line or the records table); the build repeats until the labels
  stop changing (normally pass 2), then renders without the appended links. `.page_labels.json` (git-ignorable) keeps
  the last labels and positions.
- **Lettered table notes**: `<a class="tn" href="#note-id"></a>` in a cell or label, and `<ol class="tnotes"><li id="note-id">…</li></ol>`
  under the table; the build sets the letters (a, b, … restarting per table) and adds a ↩ back-link to the first mark.
  Body footnotes stay numbered (`sup.fnref`, `#fn1`).
- **Outline**: built with pdf-lib from h2 (level 1), h3 and table/figure captions (level 2/3) at the measured
  positions; the PDF opens with the outline shown. **Running head** = the current section (page 1: the short title),
  drawn in pieces around fi/ff/fl because pdf-lib mis-spaces those ligatures; **foot** = "Page n of N" only.
  **PDF title** = `<title>`.
- **Source order everywhere**: PaSh's own, the naive LLM, Caruca's small grammar, Caruca full where traced (tables,
  legends, figure rows). "Caruca, full where traced" is the column name (note a explains 22 full grammars + small rest).
- **Table 1** is the only summary table: verdict marks ▲/▼ in the source colour against PaSh's own files, ↑/↓ in row
  labels, a "Behind the result" block (the old Table 2's rows that were not duplicates: commands with files, load
  failures, agreement on reads/writes and on split decisions) and a "Reading" row. The old Table 2's "uses decided by
  own files" row was not carried over (Table 3 has the per-command uses; Figure 1 plots it). Tables renumbered 3→2 … 7→6.
- **Figure 1 (setup) was moved, not dropped**: it is now Figure A.3 at 72 % width in A.3; body figures renumbered
  (scorecard = Figure 1, split map = 2, time = 3). Figure A.8 is two images (`a5_scripts_1.png`, `_2.png`) on two pages
  at 7 pt or more. Each appendix part opens with a "Supports:" line linking back to the body.
- Per-session numbers live only in A.3 ("Pooling").
- Verify after a build: pypdf — every `/Link` has a `/Dest` that is a named destination; outline entries > 0; every
  ", p. N" equals the target's page (compare `.page_labels.json` with the final named destinations).

## Draft 2.4 (2026-11-27, brief `orchestration/brief_report_v24.md`): one Caruca column

- **Decision (Tiran):** the body shows one Caruca, as its paper ran it for PaSh: files traced under the hand-trimmed
  grammars for PaSh's scripts (`caruca-pash-all`, 53 commands), called simply "Caruca". The full-grammar variant
  (`caruca-main-all`) is appendix part A.8 (Table A.6, small vs full on every Table 1 row). Body tables, Figures 1–3
  and Figure A.9 have three sources; the figure scripts take `--no-caruca-full` (code for the full series kept).
- **Grammar facts stated in "How it was run" and the threats:** both of Caruca's grammar sets are hand-written
  (`syntax_specs/` = the reference set its paper scores its LLM against; `pash_syntax_specs/` = trimmed by hand, 54
  commands, 64 options against 923 for the 42 in both); Caruca's code loads the trimmed set for PaSh; the paper
  describes LLM-written grammars and never mentions the trimmed set.
- Numbers: Caruca's `cat`-only time is **1.14 on 13 scripts** (`full_run_caruca_all/per_command_caruca-pash-all.md`
  section 4); earlier drafts had the small/full values (1.14/1.13) the wrong way round.
- Appendix renumbered: A.8 Caruca with its full grammars (new, flows after A.7), A.9 every script (Figure A.9),
  A.10 records. Appendix tables now numbered in order of appearance: A.1 suite, A.2 reasons, A.3 compiler-stop
  errors, A.4 by command, A.5 compiler-stop scripts, A.6 small vs full, A.7 records.
- `report/.page_labels.json` is git-ignored (repo `.gitignore`).
