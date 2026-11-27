# Captions for the interim report's figures

All three figures are drawn by `make_figures_interim.py` (in this folder) from the records in
`../validation_2026-11-24/`, which are the records `numbers_pilot.json` was counted from. The script
checks its counts against `numbers_pilot.json` and stops if they disagree. Rebuild with:

    uv run --with matplotlib==3.9.2 python figures_interim/make_figures_interim.py

## Figure 1: `split_map.png`, which commands PaSh split

**Caption.** The `spell` script is one pipeline of nine commands, drawn left to right. Each row is one
source of annotation files. A filled box means PaSh ran several copies of that command at once, each on
a piece of its input; an empty box means it ran one copy. A small triangle marks the commands the source
brought its own files for; for the other commands PaSh's own files were used. The shaded columns are
where some source differs from PaSh's own files. The naive LLM's files and Caruca's files both let PaSh
split `cat`, which PaSh's own leave whole; the naive LLM's leave `sed` and `col` whole; and only PaSh's
own files and the naive LLM's split `sort`. Caruca's two grammars give the same picture.

**Supports:** "The sources differ in which commands inside the script PaSh split: of the script's 9
command uses, PaSh split 5 with its own files, 4 with the naive LLM's, and 5 with Caruca's, but not the
same 5" (opening paragraph), and the table "Where the sources differ from PaSh's own files".

**Drawn from:** `occurrences.jsonl`, the first instrumented repeat, uses inside the part PaSh compiled;
one box per command use, ordered by its place in the pipeline; filled from whether PaSh split it; the
triangle from whether the files came from the source or from PaSh's own set. The script checks that
repeats 2 and 3 split exactly the same uses. Command words for the column heads from the same rows,
checked against the pipeline text in `regions.jsonl`.

## Figure 2: `time_bars.png`, time to run the script

**Caption.** Seconds to run `spell` under plain bash and under PaSh with each source's files: the bar
is the median of three timed runs, the thin line runs from the fastest to the slowest of the three. The
number at the end of each bar is the speed-up against bash. With PaSh's own files the script ran 1.67
times faster than bash, with the naive LLM's 1.15 times faster, and with Caruca's files slightly slower
than bash (0.96 and 0.97 times). The runs of Caruca's main grammar overlap bash's (1.073 to 1.096 s
against 1.041 to 1.079 s), so "slightly slower" there is within the spread of three runs.

**Supports:** "So PaSh's own files ran the script 1.7 times faster than bash, the naive LLM's 1.2 times
faster, and Caruca's about as fast as bash" (opening paragraph), and the "Time" and "Against bash"
columns of the table under "What we saw".

**Drawn from:** `results.jsonl`, the plain (not instrumented) timed runs, three per source; seconds per
run; median, fastest and slowest per source; speed-up = bash median ÷ the source's median. The script
checks that every timed run's output was the same as bash's and that each median equals the one in
`numbers_pilot.json`. The second copy of PaSh's own files (median 0.637 s, the noise check) is left out
of the chart.

## Figure 3: `uses_split.png`, how the 9 command uses were run

**Caption.** For each source, the script's 9 command uses split three ways: split with the source's own
files (in the source's colour), split with PaSh's own files filled in where the source had none (dark
grey with stripes), and run whole (light grey). The naive LLM brought files for 6 of the 9 uses and PaSh
split 2 of those; Caruca brought files for 2 and PaSh split 1 (`cat`). Most of the splitting under
Caruca's files, 4 of its 5 splits, comes from PaSh's own files filled in.

**Supports:** "Here the naive LLM brought files for 6 of the 9 command uses (all but `tr`); Caruca for 2
(`cat`, `sort`)" (What we ran), and "Where a source had no files and PaSh's own were used, the result was
the same as PaSh's own on every such use" (the filled-in uses are split exactly where PaSh's own run
split them).

**Drawn from:** `occurrences.jsonl`, the first instrumented repeat, the same rows as figure 1; each use
counted once, by whether PaSh split it and whether its files came from the source or from PaSh's own
set. For PaSh's own files every use is "the source's own files".
