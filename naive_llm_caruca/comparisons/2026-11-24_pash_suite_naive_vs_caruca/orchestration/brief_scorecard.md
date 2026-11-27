# Brief: one chart that answers "how did the naive LLM fare?" (2026-11-26)

You are a worker. Write a new script `figures_interim/make_scorecard.py` in this run folder
(`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`) that draws `figures_full/scorecard.png`.
Run it with `uv run --offline --with matplotlib --with numpy python figures_interim/make_scorecard.py`
(drop `--offline` if it fails). Do not edit any other file. Do not commit.

## The idea (Tufte's Challenger chart)

Many tables hide the answer. Put every metric on ONE axis with ONE direction: each source's result as a
fraction of PaSh's own files' result, right of 1.0 = better than PaSh's own, left = worse. Rows are the
metrics; each row has one dot per source. The reader sees at once where the naive LLM stands against Caruca.

## Data (hand-fed; provenance = numbers_full.md, the report's Table 2; write the values in the script with
## a comment giving each source line)

Sources and colours (same as the other figures): naive LLM `#2563EB`; naive LLM with the fixed sed file
`#93b4f5` (light blue, only on the rows marked *); Caruca full grammar `#f0b060`; Caruca small grammar
`#e8622b`; PaSh's own files second copy, grey `#9a9a9a` (only on the time row). The reference, PaSh's own
files = 1.0, is a vertical black line.

Rows, top to bottom, with x values (naive, Caruca full, Caruca small; extra dots noted):
1. Commands covered by its own files (82 and 8 of the commands used, against PaSh's own 30): 2.73, 0.27, 0.27
2. Command uses decided by its own files, of 609 (523, 304, 304; PaSh's own 485): 1.08, 0.63, 0.63
3. Printed output same as bash (86 of 86 each): 1.00, 1.00, 1.00
4. Scripts with a part split (43, 41, 29 of 86; PaSh's own 41): 1.05, 1.00, 0.71
5. Parts split (43, 41, 29 of 177; PaSh's own 41): 1.05, 1.00, 0.71
6. Compiler stops, fewer is better (4, 4, 14 parts; PaSh's own 4; plotted as own/source): 1.00, 1.00, 0.29
7. Files that load without error (80 of 82, 8 of 8, 8 of 8; plotted as fraction): 0.98, 1.00, 1.00
8. Agreement with PaSh's own on what a command reads and writes (172 of 178, 101 of 110, 93 of 110): 0.97, 0.92, 0.85
9. Wall-clock, faster is better (plotted as own time / source time; geometric means): 0.87, 0.94, 0.95;
   extra dots*: fixed sed file 0.94 (light blue), PaSh's own second copy 1.01 (grey)

Row 1 is off the scale on the right for the naive LLM: use a log x axis from 0.25 to 3 so it fits, with ticks
at 0.25, 0.5, 1, 2, 3, and label the naive dot with its value (2.7×) as well.

## Drawing rules

Width 6.3 in (full text width), height to fit nine rows with air (about 4.6 in), 300 dpi. Fonts: register
Libertinus Sans and Inconsolata from `../../../../scripts/md-to-pdf/fonts/academic/` as
`make_figures_interim.py` does (copy those lines). Smallest text 7.5 pt at printed size. Row labels on the
left in plain words as given above (short form, two lines allowed). A light grey horizontal guide per row. Dots
9 pt, with a thin white edge so overlapping dots stay visible; when two sources share a value, offset them
vertically by a little. Legend across the top in one line. Axis title: "Result as a fraction of PaSh's own
files (right of the line = better)". Shade the band 0.87 to 1.13 on the time row only, labelled "noise", to
show how far an identical second copy strayed. No title inside the figure (the caption carries it). No grid
except the guides.

Reply in your pane in at most five lines: the file written, its size in inches and the smallest font size.
