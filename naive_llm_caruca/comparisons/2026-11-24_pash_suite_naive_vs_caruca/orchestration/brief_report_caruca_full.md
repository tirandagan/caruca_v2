# Brief: revise the report with Caruca at full reach (2026-11-27)

You are the report worker. Read first, in order: `report/README.md` (structure, framing, typography, build),
`orchestration/brief_report_round3.md` (style rules that still hold), `memory/feedback_greenberg_report_style.md`,
`memory/feedback_plain_language.md`, `memory/feedback_report_metrics_in_pdf.md`, `full_run_caruca_all/README.md`,
`full_run_caruca_all/numbers.md`, `full_run_caruca_all/per_command_caruca-*.md`, `caruca_conversion/README.md`.
Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`. Edit `report/` and the figure
scripts in `figures_interim/`; write new counts next to the existing ones (never overwrite `numbers_full.*` or the
first run's records). Do not commit.

## What changed

The first run gave Caruca files for 8 commands only (all that had been converted). Caruca has now been converted
for 53 commands (small grammars) and 22 (full grammars), and PaSh's suite was rerun on 2026-11-26/27 with
`bash`, `pash-own`, `pash-own-copy`, `caruca-pash-all`, `caruca-main-all` (records in `full_run_caruca_all/`).
The naive LLM's sets were not rerun. **Rule for time:** every source's time is a ratio to `pash-own` from its own
session (naive: first run; Caruca: rerun). Say so in the method and under every time figure. The rerun's
`pash-own` reproduced the first run's splits exactly (41 parts, 126 uses), which supports the cross-session
comparison of splits and correctness; say this too.

## Replace Caruca everywhere with the expanded sets

- "Caruca's small grammar" = `caruca-pash-all` (53 commands). "Caruca's full grammar" = `caruca-main-all`: label
  it "Caruca's full grammar where traced (22 commands; small grammar for the rest)" at first use, then "Caruca's
  full grammar". Remove every statement that Caruca has files for only 8 commands; the method section says the 8
  were the first conversion and why the rest followed (one paragraph, pointing at `caruca_conversion/README.md`,
  including the converter repair and the commands left out: `gzip`, full grammars of `comm join cp diff ls`).
- Correctness is now the first finding: naive LLM 86 of 86, PaSh's own 86 of 86, Caruca small 77 of 86, Caruca
  full 76 of 86 (Koala stored answer: 37 and 36 of 46). Use `full_run_caruca_all/wrong_outputs_verified.md` (an
  independent check being written now; wait for it, the orchestrator will tell you) for the causes: `sed` with a
  line address, `uniq`, `tr -d '\n'`. A new short section after section 1: "Where Caruca's files give wrong
  output", one table (script, command line, what Caruca's file allowed, why it is wrong, PaSh's own and the naive
  LLM's decision on the same line), and two sentences linking it to Caruca's rule of keeping the most
  parallelizable label when its traces disagree (if the check confirms it).
- Recount Table 1, Table 2 (head to head), Figure 2 (scorecard: `figures_interim/make_scorecard.py`, hand-fed
  values with sources in comments; add a row "Printed output same as bash" with the new fractions), Figure 3
  (split map), Figure 4 (time), Table 4 (next to the paper; recompute the agreement lines with `count_report.py`
  on the rerun records via `prep_full_records.py`, writing `numbers_caruca_all.md/.json`), Table A.4 (reasons),
  Table A.5 (compiler stops: Caruca's `fmt` file stops PaSh in 2 parts per the builder; verify from the records),
  Table A.6, Figure A.7 (per script: add the Caruca sets from the rerun records), Table A.8 (crash list), and the
  records table A.9 (add `full_run_caruca_all/`, `caruca_conversion/`, the Caruca commit `be33389a5` on
  `binpash/caruca` branch `pash-python-annotations`).
- Add Caruca's command-by-command comparison with PaSh's own files next to the naive LLM's Table 3 (from
  `per_command_caruca-main-all.md` and `-pash-all.md`): same columns, one combined table or a second table,
  whichever reads better; keep it to one page.
- Rewrite the title's finding line, the question paragraph if needed, "How it fared", and "What this does not show"
  for the new picture: the naive LLM was always correct; Caruca, at full reach, gives wrong output in about one
  script in eight; splits: naive 43, Caruca full 40, Caruca small 29 scripts; time: naive 1.15, Caruca 1.09 and
  1.10 against PaSh's own (each in its own session). Keep every rate "a of b", no jargon, sentences under 30 words.

## Build and check

Regenerate figures (`uv run --offline --with matplotlib --with numpy python ...`), build
(`npx tsx .../report/build.ts`), render every page, check no table/figure split, no orphan heading, no page over
a third empty before the last. Version line: "Draft 2.0, 27 November 2026". Update `report/README.md`.
Reply in your pane in at most 12 lines: page count, every headline number, and anything you could not do.
