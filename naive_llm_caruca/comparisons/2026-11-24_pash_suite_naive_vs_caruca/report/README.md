# The report for Michael: how it is built and how to update it

The report is hand-authored HTML, not converted Markdown, so its layout can be exact: `report.html`
(content) and `report.css` (layout), rendered to `report.pdf` by `build.ts` with the repo's own brand
fonts and colour tokens (`scripts/md-to-pdf/tokens.ts`); the running head and foot are stamped on afterwards with pdf-lib in the brand face (Chromium's own header templates cannot load it), so it stays
one system with the other Caruca documents. The earlier Markdown draft (`../report_draft.md`) is kept
for the record and is no longer the source.

## Build

```sh
cd <repo root>
npx tsx naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/build.ts
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
A1–A8 are numbered without gaps; update every "(A…)" reference in the body when a section moves.

## Rules the layout follows

- Every table and figure is numbered and referred to by number in the text.
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

1. Rebuild the records with `../count_report.py` and the figures with `../make_charts.py` /
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
