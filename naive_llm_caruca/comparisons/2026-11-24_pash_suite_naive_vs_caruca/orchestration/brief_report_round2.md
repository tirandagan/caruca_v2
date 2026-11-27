# Brief: report round 2, restore Tiran's metrics and fix the reviewer's defects

You are a worker. The orchestrator gave you this brief on behalf of Tiran Dagan. Read
`orchestration/brief_report_refresh.md` first (paths, rules, build command); its rules still hold. Do not
commit. Edit only `report/report.html`, `report/report.css` (only if a rule must change), `report/README.md`,
and figure scripts/outputs under `figures_full/`. Records and `numbers_full.*` are read-only.

## 1. Why this round exists

Tiran's metrics spec (`orchestration/metrics_spec.md`) asks the write-up to report, per script and set:
parts parallelized of all parts with every cause listed (including **PaSh compiler crashes** and their
exception text), wall-clock median and min–max of 3, same as bash, exit code, crash count, and the
"no region parallelized" warning. The counting has all of it (`numbers_full.md` appendix sections A3,
A4, A5, A6 and the "Full run" sections), but the PDF's addendum lost those tables. Restore them. The body
stays short, but it must say how often PaSh's compiler crashed under each source and why.

## 2. Body changes (keep it brief)

- Table 1: add one row **"Parts where PaSh's compiler crashed"**: PaSh's own 4 of 177, naive 4 of 177,
  Caruca PaSh grammar 14 of 177, Caruca main 4 of 177 (sed v2: 1 of 139; check these against
  `numbers_full.md` A3 "pash crash", same-as-PaSh's-own + only-with-this-source), basis line "parts
  PaSh compiled, all repeats".
- After "Why the cells differ", a short block **"When PaSh itself failed"** (at most 6 sentences): the
  two exceptions seen, from the PaSh logs in the VM (`~/t024/out/logs/`, Lima VM `pash`; read, do not run
  anything): an `AssertionError` inside PaSh's compiler (find the asserting line in the installed
  pash_annotations package or PaSh's compiler and say in words what it checks; the orchestrator believes
  it is the annotation package's round-robin assertion, verify), and `NameError: name 'Arg' is not
  defined` (a PaSh import lost in its January 2026 refactor; issue binpash/pash#794 was filed on 20
  November). Say which scripts, how many parts per source, and that PaSh falls back to bash so the output
  stayed right. State plainly that under Caruca's PaSh grammar 10 more parts crash than under PaSh's own
  (`numbers_full.md` A3), and which commands' files are involved (from `regions.jsonl.gz`, reason text and
  the commands in the part).
- Mention in "What this does not show" that the naive LLM's files raised an error on 3 lines (wc, join)
  and the crash counts above are PaSh's compiler, not the files.

## 3. Addendum: restore the tables, renumber A1..A8 (no gaps)

A1 script (keep), A2 words (keep), A3 setup (keep, Figure 3 stays after its first paragraph), then:

- **A4. Why parts were not run in parallel.** From `numbers_full.md` A3: reasons (rows) by source
  (columns), distinct parts, each cell "same as under PaSh's own / only with this source" explained in the
  caption; then the per-execution version. Add a line per source: "PaSh crashes: parts, scripts, exception".
- **A5. Every script: what PaSh did and how long it took.** One row per script (86), columns: script;
  then for bash the median time; then for each of the four sources: parts run in parallel of parts
  compiled (distinct), crashes, median seconds with min–max in small text. Build it from `numbers_full.json`
  (A5 times, per-script parts from the "Full run" sections or the records; write a small helper script
  `report/make_a5_rows.py` that prints the HTML rows so it can be regenerated). Font 7.5 to 8 pt,
  `table.scripts` style, header repeats on every page. Mark with a footnote the scripts whose runs were
  redone after a Mac sleep and web-search's node redo.
- **A6. Every use whose result differs from PaSh's own.** From `numbers_full.md` A4 but **only rows where
  at least one source differs from PaSh's own** and with duplicate command lines within a script collapsed
  (loops): script, command line (shortened: replace the long input path with `IN`), result under each
  source. Expect about 100 rows; if more than 160, keep only the commands of Table 2 and say so.
- **A7. The scripts** (the current A5 list) and **A8. Records** (the current A6). Update every cross
  reference in the body ("A5 lists them", "(A6)").

## 4. Fix the reviewer's defects (all of them)

1. Addendum numbering gap (A4 missing): solved by section 3; check every "(A6)"-style reference.
2. p.5 Table 3 caption "102 lines ... left out": 178 − 102 ≠ 76 vs "99 of 113 lines". Recompute from
   `numbers_full.json` Table 4 data; make caption and cells agree.
3. p.2 "609 command uses inside parts" vs p.8 "849 of 850 uses": say what each counts (one source's
   uses vs summed over sources) or use one number.
4. p.5 top orphan paragraph "The slowest script, web-search…": merge into the previous paragraph.
5. Table 1 Caruca-PaSh basis line wraps leaving "−12" alone: non-breaking spaces; sed-v2 basis line has
   three facts: split into two short lines.
6. Table 2: naive column 2.5× wider: set equal widths for the four data columns.
7. Figure 3 (`figures_interim/setup_diagram.excalidraw` → png): lettering is mono throughout; DESIGN.md
   says sans for prose, mono only for command names. Re-letter in the sans face if the renderer allows
   (see `memory/reference_excalidraw_diagram_skill.md` for the renderer); if not feasible in this round,
   say so in your report and leave it. Sidebar text "five runs": change to "one bash run and four PaSh
   runs drawn; two more sets were run".
8. Table 3 last column cap mixes two sources under one orange cap: use no cap and a note, or two caps.
9. Figure 1: add a two-swatch key (solid = gained, hatched = lost) in the figure script.
10. p.10: NLP group heading + 2 rows at a page foot: keep heading with at least 4 rows (CSS on the
    group block, or a break-before).
11. p.1 "46 of 46": write "46 of the 46 scripts that have a stored answer".
12. "17 of the 17 scripts" → "17 of 17 scripts" (and "5 of the 5").
13. A8/A6 records text: describe `make_figures_interim.py` as "the figure script (written for the
    pilot, reused)".
14. Number the A7 script tables or say in A7's intro that its group lists are unnumbered (do the latter).
15. The p.8→9 three-line carry-over: resolves if 4 moves text; check after rebuild.

## 5. Build, look, report

Build, render every page (`pdftoppm -r 70 -png report/report.pdf /tmp/p2/pg`), look at each: no table
split mid-row without a repeated head, no heading alone at a page foot, no page more than a third empty
except the last. Two rounds at most. Update `report/README.md` (structure list: A1..A8, the helper
script). Reply in your pane, at most twelve lines: page count, the crash exception you found and where
it asserts, the A6 row count, any defect you could not fix and why.
