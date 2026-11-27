# Brief: refresh the report for Michael with the full-run numbers

You are a worker. The orchestrator gave you this brief on behalf of Tiran Dagan. Work only on it. Do not
commit. Do not edit anything under `full_run/`, `../../` (the naive experiment's other folders) or v1.

## Where things are (all paths relative to this run folder, `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`)

- `report/report.html`, `report/report.css`, `report/build.ts`, `report/README.md`: the hand-built report
  (read `report/README.md` first; it states the structure rules and the update steps). Build with
  `npx tsx naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/build.ts` from the repo root;
  render pages with `pdftoppm -r 70 -png report/report.pdf /tmp/p` and look at every page.
- `full_run/`: the complete records (86 scripts, six sources, three timed repeats): `results.jsonl.gz`,
  `regions.jsonl.gz`, `occurrences.jsonl.gz`, `run_windows.jsonl`, `sleep_events.jsonl`, the builder's
  `numbers.md` (made by `full_run/summarise.py`) and `full_run/README.md`.
- `orchestration/review_checker_full.md`: an independent check of the records (10 of 11 pass). Read its
  check 7 and check 4: the correctness claim holds for **printed output**; the files that 32 scripts write
  were compared in only 211 of 588 timed runs, 352 had no reference, 25 differ, and web-search's written
  files differ even between two plain-bash runs. The report must say this plainly.
- `count_report.py` (the orchestrator's counting script, used for the pilot: `numbers_pilot.md/.json`) and
  `figures_interim/make_figures_interim.py` (draws `split_map.png`, `time_bars.png`, `uses_split.png`
  from the records and checks itself against `numbers_pilot.json`), `figures_interim/captions.md`.
- `metrics_spec.md` (Tiran's metrics and decisions), `report_plan.md` (the report's plan).

## Steps

1. **Count independently.** Run `count_report.py` on the full records (gunzip them into a scratch folder
   first, or add `.gz` support to the reader, your choice) with `--tag full`, producing `numbers_full.md`
   and `numbers_full.json` in this folder. Compare its headline cells with `full_run/numbers.md` sections
   1, 3, 5 and 6. Apply the same two fix-ups the builder describes at the top of `numbers.md` (compare
   output against the same repeat's bash row; leave out the seven web-search rows that ran without node
   and use the redone rows). If a cell differs from the builder's, find out why before going on and write
   the reason in `numbers_full.md`; do not silently pick one.
2. **Figures.** Make `figures_interim/make_figures_interim.py` take the records folder and the numbers
   json as arguments (default: the pilot, so the old call still works) and write to
   `figures_full/` (new folder) for the full run. Keep the four source colours exactly
   (`SOURCE_COLOR` in the script = the CSS tokens in `report.css`). Add the second sed file as a fifth
   series only where the figure is per source; label it "Naive LLM, sed file v2 (52 scripts)". Fonts and
   sizes as the script already does. Check every figure at 100% for overlapping labels.
3. **Report text and tables.** Edit `report/report.html` only. Rules:
   - Keep the layout, the four columns, the numbering and the section order. Add rows, never columns.
     The second sed file is a labelled extra **row** ("Naive LLM, sed file v2, 52 scripts") where a table
     is per source, not a column.
   - Every number comes from `numbers_full.json` / `numbers_full.md`. Rates are written "a of b".
   - Version line: "Draft 1.0, 26 November 2026." Replace every "interim", "so far", "46 scripts",
     "staged to happen", "what remains" wording: the run is complete (86 scripts, three timed repeats,
     median). The summary on page 1 states the three-source design, that all of a source's commands are
     swapped in at once, and the headline per source.
   - Correctness wording: "printed output the same as bash in 86 of 86 scripts under every source; the
     files that 32 scripts write were checked in 211 of 588 timed runs and matched where checked, except
     web-search, whose files differ even between two bash runs" (take the exact counts from the checker's
     review and your own count).
   - "Where the sources differ" (Table 2, Figure 1, the vetted causes list): update the gained/lost
     commands per source from numbers section 5 (naive: cat 43, awk 6, tr 3, cut 2, sort 2, grep 1 gained;
     sed 5, col 1 lost; Caruca main: sort 17 lost; Caruca PaSh grammar: sort 17, cut 9, tr 5, sed 5, grep 4
     lost, cat 29 gained). Keep the vetted causes from `orchestration/judgment_errors.md`; add that the
     naive LLM's two gained parts are parts where PaSh's own files crash PaSh's compiler (checker, check 7,
     item 5) and that the sed v2 file did not recover the sed splits (0 gained of 5 lost).
   - Time (Figure 2 and text): medians of three; PaSh slower than bash under every source on these small
     inputs; the noise band from the second copy is 0.83 to 1.13 (4 of 86 scripts beyond 10%); naive 1.15
     times PaSh's own, 34 of 86 scripts slower by more than 10%; web-search 10 to 12 minutes per run, no
     part parallel under any source.
   - "What this does not show": small inputs only; written files partly unchecked; the Mac slept four
     times and the affected runs were redone (A3 gets one sentence on this and on the two instrument
     faults: the repeats recorder and web-search's node; records untouched, fixed in the counting).
   - A5 stays the list of all 86 scripts. A6 lists the full_run records and the checker's review.
   - Point the figure paths at `figures_full/`.
4. **Build and look.** Build the PDF, render every page, check: no table or figure split across pages, no
   heading alone at a page foot, no orphan caption, Table 1 on page 1 beside the summary and script. Fix
   in `report.css` only if a rule must change; prefer HTML order changes. Two rounds at most.
5. **Report back** in your pane, at most twelve lines: page count, any cell where your count differed
   from the builder's and why, the figures made, anything you could not fit, and the build command.
   Then stop; the orchestrator runs the design review.
