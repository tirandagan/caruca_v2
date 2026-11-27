# Brief: report round 3, rewrite for clarity and simplicity (critique of 2026-11-26)

You are a worker. The orchestrator gave you this brief on behalf of Tiran Dagan. Read, in this order:
`report/README.md`, `orchestration/brief_report_refresh.md` (paths, build command, rules that still hold),
the critique `.impeccable/critique/2026-11-26T09-13-23Z__11-24-pash-koala-naive-vs-pash-report-report-html.md`
(repo root), `DESIGN.md` (repo root), `memory/feedback_plain_language.md`, `memory/feedback_greenberg_report_style.md`.
Edit only `report/report.html`, `report/report.css`, `report/README.md`, `report/make_a5_rows.py`,
`figures_interim/make_figures_interim.py` and its outputs in `figures_full/`. Records and `numbers_full.*`
are read-only. Do not commit.

## Tiran's decisions (2026-11-26)

1. Appendix A5, A6, A7: **condense to one page each**; every metric stays visible in compact form.
2. Timing stays in the body with **one convention: time ÷ bash time, lower is better**, slower/faster
   spelled out. The number-string paragraphs shrink to one sentence each.
3. The naive LLM's headline gain: **show both counts**, the full count and "without cat" beneath it.

## The standard

Tiran: "concise, clear, visually well documented, at the level of a publishable academic paper"; Michael
wants very simple, human prose, clean numbered tables and charts. Rules: every rate "a of b"; no word a
first-time reader has not been given; one noun per concept throughout (use exactly: **annotation files**,
**source** (whose files), **part** (a piece PaSh compiles), **split / whole**, **the naive LLM**, **Caruca's
small grammar / Caruca's full grammar**, **the second sed file**); script codes, exception names, file paths
and commit hashes only in the addendum; no sentence over 30 words; no paragraph with more than three
numbers unless it is a list; no section numbers (DESIGN.md); the four-column board stays.

## Body (target 5 pages)

1. **Page 1, before Table 1: "How it was run"**, about 100 words plus Figure 3 at half width (regenerate
   `figures_full/setup_diagram.png` at the smaller size if needed; keep its content). It must define, in
   this order and in one plain sentence each: Koala (the PaSh team's current benchmark suite, successor of
   the 2022 suite); annotation files; source; part; split and whole; Caruca's small and full grammar; the
   naive LLM (an off-the-shelf coding agent, Claude Code, given only the goal, the file formats and four
   examples); the second sed file (one fix to the agent's sed file after the pilot; where it changes a
   number both are shown). Then one line: what was recorded per run (output, which commands were split,
   seconds).
2. **A one-sentence question** at the very top of the summary ("Does the source of PaSh's annotation
   files change what PaSh does on its own benchmark suite?") and a **one-line finding under the title**
   ("Output was always correct; the sources differ in which commands were split and by 5 to 15 % in time").
3. **Table 1**: rows Printed output same as bash; Scripts with a part split (full count, and beneath it
   "without cat: n of 86" for every column); Parts split of parts compiled, written "gained n, lost n
   against PaSh's own"; PaSh compiler stopped (crashes), "n of 177 parts"; Time, written "n.n × bash time
   (lower is better)" with beneath it "n.nn × PaSh's own". The second sed file is a labelled row named
   exactly "Naive LLM, second sed file (52 scripts)". Caption defines gained/lost. Footer line split into two
   sentences. Keep it on page 1 beside the script box.
4. **Page 2 "Where the sources differ"**: opener cut to three sentences, no more than three numbers; Table 2
   moves to the addendum (becomes A6); Figure 1 stays, with PaSh's own count added as a grey label at each
   row ("PaSh's own: 17 of 44"), bar labels at caption size, panel titles not wrapping, the key kept.
   "Why the cells differ" becomes "Why they differ": keep the five vetted causes, each with its plain-clause
   label and at most three sentences; no script codes (say "two Unix50 scripts", "the four COVID scripts").
5. **"When PaSh itself failed"**: three sentences. "PaSh's own compiler stopped in 4 parts under its own
   files and in 14 under Caruca's small grammar; the 10 extra all come from Caruca's sort file. Both failures
   are PaSh bugs, one of which we reported. In every case PaSh ran the part as plain bash, so the output
   stayed right (details in A4)."
6. **Time**: Figure 2 first, then one sentence per finding (four at most). Add to Figure 2's right-hand
   column "slower than bash: n of 86" per source, so those numbers leave the prose. Axis label already
   correct; make the figure's noise-band label read "noise band (same files run twice)".
7. **"Next to the Caruca paper" (Table 3)**: caption in three short sentences; the counting rule goes to a
   footnote under the table; cells with one fact each (split "54 of 70 lines; 7 of the 16 others..." into
   two lines); the last column gets no colour cap and a note. Let it start on page 5 under Figure 2 if it
   fits with heading and head row repeated, otherwise keep it whole.
8. **"What this does not show (threats to validity)"**: keep, retitle so; four bullets, plain; commit hash
   and worker count move to A8.

## Addendum (target 7 pages)

- **A1 script, A2 words, A3 setup**: keep; A2 shrinks to the words not already defined on page 1.
- **A4 Why parts were not run in parallel**: merge A4a/A4b into one table (distinct parts; one line noting
  the per-execution totals differ only in the "other" row). Explain the "a / b" cells in the column head,
  not as a code. **Name what the naive LLM's 31 "other, not classified" parts are**: read
  `full_run/regions.jsonl.gz` (reason text, commands, script) for set `naive`, outcome other, and classify
  them in one sentence (and a one-line table if there are two or three kinds). The crash paragraph moves
  here in full (exceptions, PaSh source line, scripts, issue 794).
- **A5 Every script, one page**: a chart, not a table: one row per script, grouped by suite group, dots
  for time ÷ bash time under each source (same colours), a hollow marker where a crash occurred, two columns
  of 43 rows on one Letter page; add a six-line crash list beneath (script, source, exception). Keep
  `make_a5_rows.py` only if it feeds the chart; otherwise delete it and say so in the README.
- **A6 Where a source changed what PaSh split, by command**: Table 2 (from the body) plus one column with
  the number of distinct command lines behind each count; the 135-row per-use list goes to a pointer
  (`numbers_full.md` section "every use") in A8.
- **A7 The scripts, one page**: nine group blocks, each: group name, folder path in the VM, count, then the
  script file names in a run-in list (comma separated, mono), with "edited"/"new"/"rewritten" marked by a
  superscript letter and a key; the 2022 originals column goes to the inventory file (`orchestration/coverage.md`),
  referenced once. Every script's folder and file name must still be on the page (Tiran's requirement).
- **A8 Records**: a two-column table (what, file), not a paragraph; include the PaSh commit, worker count,
  and the pointer to the per-use list.

## Visual fixes

h1 uses the ink token (detector finding); one tint rule: tint = reference column only, "differs" cells
get weight 600 plus a 1 pt left rule in the source colour (no tint); no page more than a third empty before
the last; no heading alone at a page foot; no caption split; A7 blocks do not break inside. Figure 3
lettering: if the excalidraw renderer can take a sans font, re-letter prose in Lexend Deca and keep mono for
command names; if not, leave it and say so.

## Finish

Build; render every page at 70 dpi; look at each; fix in one batch; rebuild once more; stop. Run a
humanizing pass on the body prose (read it aloud in your head: no "machine-made" rhythm, no positional
number lists). Update `report/README.md` (structure A1..A8, scripts). Reply in your pane in at most twelve
lines: page count, what the 31 "other" parts are, anything in this brief you could not do and why.
