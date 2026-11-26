# Brief: fix two figures after the font change (2026-11-26)

You are a worker. Edit only `figures_interim/make_figures_interim.py` in this run folder
(`naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`) and regenerate its outputs into `figures_full/`
with exactly this command, run from the run folder:

    uv run --with matplotlib --with numpy python figures_interim/make_figures_interim.py --records full_run --numbers numbers_full.json --out figures_full

The script now registers Libertinus Sans and Inconsolata (ACM-style fonts) instead of Lexend Deca; the font
metrics changed and two figures broke. Do not change colours, data, or what the figures show. Do not commit.

## 1. `figures_full/a5_scripts.png` (the per-script chart, "Figure A.7" in the report)

Open the PNG at full size and fix:
- The legend at the top overlaps the column headings ("bash", "parts split"): move the legend above the
  headings with clear space, or into its own band.
- The x-axis title "time ÷ bash time (lower is better)" under both panels is cut off at the bottom edge:
  add bottom margin (bbox_inches='tight' with pad, or a taller figure).
- Row labels and numbers render at about 5 pt on a Letter page at 6.3 in width: raise the smallest text to at
  least 6.5 pt at the printed size (the figure is printed at 6.3 in wide; compute the font size from the figure
  width in inches), even if the figure grows taller; it has a whole page.
- Script names truncated with an ellipsis (bigrams_appear_twi…, compare_exodus_gen…, sort_words_by_fold…,
  thumbnail_generati…): widen the label column or shorten with the full name kept readable
  (e.g. allow 28 characters).

## 2. `figures_full/time_bars.png` ("Figure 3")

The right-hand label for Caruca's small grammar may read "1.03 · 17 of 86 slower by >10%" while
`numbers_full.json` and the report say 1.05 (geometric mean of time ÷ PaSh's own). Check what the script prints
for that label and where the number comes from; if it is not the geometric mean over the 86 scripts from
`numbers_full.json`, make it so, and make sure every row's number matches the report's Table 1 (naive 1.15,
second sed file 1.07, Caruca small 1.05, Caruca full 1.06, PaSh's own second copy 0.99). Also raise the
smallest text in this figure to at least 7 pt at a printed width of 5.4 in.

## 3. Report back

Regenerate, open both PNGs at full size and confirm the fixes visually. Reply in your pane, in at most eight
lines: what the Figure 3 label number was and is, the smallest font sizes now, and the command you ran.
