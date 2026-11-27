# Plan: a larger-input run where splitting has work to divide (2026-11-27)

## Goal

Tiran: show whether the naive LLM's extra splits pay off when scripts move real amounts of data, against PaSh's own
files and Caruca, and quantify it in time, splits, wrong outputs, compiler stops and file errors. The run must be
short (about an hour and a half), not another day.

## Ground rules (fixed before any run, so the result cannot be steered)

- The script list, input sizes, sources and metrics below are chosen by rules that do not look at any source's
  result. Everything measured is reported, including any metric where the naive LLM does worse.
- What input size can and cannot change: whether an output is right, which commands PaSh splits, where its compiler
  stops, and which annotation files fail to load are decided by the files on each command line, not by data size. They
  are re-measured but expected to match the small run (naive LLM: always right, 4 stops, `wc`/`join` files fail;
  Caruca: wrong where it splits `sed 1d`-style, `uniq`, `tr -d '\n'`; 11 stops). **Time is the metric that can move.**
  So "every metric improves" is not a possible outcome to design for; the question this run can answer is whether
  the naive LLM's extra splits turn into speed once there is work to divide.

## Scripts (rule: split decisions differ, measured in the existing records)

- **Group A, 29 scripts**: the naive LLM's files (with the fixed `sed` file) make PaSh split a different set of
  commands, beyond a plain `cat`, than PaSh's own files or Caruca's. COVID 1-4; Classics sort, sort-sort, spell, top-n,
  uniq-ips, wf; Unix50 2, 4, 10, 11, 12, 14, 16, 17, 19, 21, 24, 25, 26, 28-33.
  Where the naive LLM splits more than PaSh's own: extra `awk` (COVID 1-4, Unix50 14, 19), `tr` (24, 25),
  `cut`/`grep`/`sort`/`tr` (12, 16). More than Caruca: mostly `sort`, `cut`, `tr`, `grep`, `awk`, which Caruca's small
  grammars cannot split. Fewer than Caruca: `sed` with a line address (26, 28-33) and `col`/`uniq` (spell, uniq-ips),
  where Caruca's splits are the wrong ones.
- **Group B, 14 scripts, reported separately**: differ only by the naive LLM splitting a plain `cat` (Classics
  nfa-regex; Unix50 1, 3, 5-9, 13, 15, 18, 20, 23, 35). This measures what that habit costs at scale.

## Inputs (generated, no download)

- Each script's own small input, concatenated k times (COVID: data rows only, one header). No new data, same
  distribution, the way Koala builds its own sizes.
- k per script from a **bash-only** pilot: the smallest of 10 and 30 at which bash's time reaches 3 s, capped at 30
  (about 1 GB). Measured once per script under bash, before any PaSh run.
- Disk: the PaSh VM has 6.6 GB free, so each script's input is built, used by all sources, and deleted before the next
  script. Never more than one large input on disk.

## Sources (one session, so no pooling)

`bash`; PaSh's own files; the naive LLM's files with its second `sed` file (the repaired instrument); Caruca as its
paper ran it (small grammars, 53 commands); PaSh's own files again (noise). Caruca's full-grammar set is optional
(appendix only); include it if the pilot shows the run stays under two hours.

## Runs and metrics

Per script and source: one instrumented run (splits, parts, stops, file answers), then three timed runs, bash first in
every repeat, medians. Same metrics as the main run: output same as bash (hash) and Koala's answer where one exists;
parts and command uses split, per command; compiler stops with error text; files that fail; time against bash, against
PaSh's own and against Caruca, measured and with PaSh's start-up removed (`overhead_adjusted.py` model). Mac sleep and
power checks as before.

## Expectations, written down before running

- Against PaSh's own files: faster where the naive LLM adds `awk`, `tr`, `cut`, `sort` splits (Unix50 12, 14, 16, 19,
  24, 25; COVID 1-4 with the fixed `sed` file); about equal elsewhere in group A; slower in group B (the `cat` cost).
- Against Caruca: faster where Caruca cannot split `sort`, `cut`, `tr`; Caruca still wrong on its 9 scripts; on Unix50
  26 and 28-33 Caruca may be faster, but its output is wrong there, which the table will show side by side.
- If these do not hold, that is the finding, and the report says so.

## Time and people

Pilot (bash only, about 15 minutes), then about 29 + 14 scripts × 5 sources × 4 runs at seconds to about a minute each:
roughly 1 to 1.5 hours. Run by a builder pane (Claude, because it adapts the runner to scaled inputs and handles faults),
records in `full_run_large/`, an independent check of every wrong output, then a "Larger inputs" section in the report
with one table per group and the per-script figure.
