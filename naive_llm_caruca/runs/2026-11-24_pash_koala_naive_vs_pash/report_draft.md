# PaSh's benchmark suite, with three sources of annotation files

**Interim draft 0.3.** One script measured and checked; the rest of the suite is running.
<div style="float:right; width:40%; margin:0 0 0.8em 1.4em"><div style="font-size:0.78em; color:#555; margin-bottom:0.3em"><strong>spell.sh</strong> (Koala, one-liners)</div><pre style="font-size:0.8em; line-height:1.4; background:#f6f6f4; padding:0.6em; border-radius:4px; white-space:pre"># Count misspelled words in a text

dict=&#36;SUITE&#95;DIR/inputs/dict.txt

cat &#36;1 |
    sed &#x27;s/&#91;^&#91;:print:&#93;&#93;//g&#x27; |
    col -bx |
    tr -cs A-Za-z &#x27;\n&#x27; |
    tr A-Z a-z |
    tr -d &#x27;&#91;:punct:&#93;&#x27; |
    sort |
    uniq |
    comm -23 - &#36;dict</pre></div>
<div style="font-size:1.12em; line-height:1.45">
<p><strong>What we ran.</strong> One script from PaSh's benchmark suite: <code>spell</code>, which finds misspelled words in a text. It is a single pipeline of nine commands (shown on the right), run on a 30 MB input.</p>
<p><strong>How.</strong> We ran it under plain bash, and then under PaSh four times, each time with a different source of annotation files: PaSh's own, the naive LLM's, and Caruca's (two versions). The annotation files tell PaSh which commands it may split into parallel copies. Nothing was generated; the files already existed.</p>
<p><strong>What we saw.</strong> The output was right in every run. The sources differ in <em>which of the nine commands</em> PaSh split: 5 with its own files, 4 with the naive LLM's, 5 with Caruca's, but not the same 5. The split that pays is <code>sort</code>; PaSh's own files and the naive LLM's allow it, Caruca's do not. So the script ran 1.7× faster than bash with PaSh's own files, 1.2× faster with the naive LLM's, and about as fast as bash with Caruca's.</p>
<p><strong>What remains.</strong> The other 72 scripts of the suite are running now, about 10 hours. This draft's numbers will be replaced by theirs; the structure stays.</p>
</div>
<div style="clear:both"></div>


<!-- pagebreak -->

## What we ran

PaSh decides what it may run in parallel from three small files per command, its *annotation files*: what
the command reads and writes, and whether its input can be cut into pieces and the results joined. We gave
PaSh three sources of these files and compared each with plain bash.

- **The script.** `spell`, from the "Classics" set of the 2022 PaSh paper's benchmark suite, in the version
  kept in Koala (the suite's current home). One pipeline of nine commands: `cat`, `sed`, `col`, `tr` (three
  times), `sort`, `uniq`, `comm`, on a 30 MB text. Small input.
- **The four ways it ran under PaSh**, each with 8 workers:

  **Table 1.** The four sources of annotation files PaSh was given.

  | Source | Files PaSh used |
  |---|---|
  | PaSh's own | the files that ship with PaSh |
  | Naive LLM | files written by an off-the-shelf coding agent, given only the goal, PaSh's file format and four examples; it never ran PaSh |
  | Caruca, PaSh grammar | files Caruca generated from its traces, using the small grammar it keeps for PaSh |
  | Caruca, main grammar | the same, from Caruca's full grammar where it has one |

- Where a source has no files for a command, PaSh used its own. Each run swapped in all of a source's files
  at once, so a difference belongs to the source as a whole, or to the commands it swapped in, never to one
  command alone. Here the naive LLM brought files for 6 of the 9 command uses (all but `tr`); Caruca for 2
  (`cat`, `sort`).
- Three timed runs of each; we report the median.

![Which commands each source has its own files for](/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/figures_interim/files_grid.png)

*Figure 1. Which of the script's seven commands each source has its own annotation files for. A filled box means the source brought its own files for that command; an empty box means PaSh's own files were used in its place. The naive LLM has files for every command but `tr`; Caruca for `cat` and `sort` only.*

<!-- pagebreak -->

## What we saw

Table 2 and Figure 2 give the result for the one script; Figure 1 (previous page) shows which commands each source has its own files for.

**Table 2.** What PaSh did with each source's files on the `spell` script (output, splits, time).

| Source | Output same as bash | Command uses with this source's own files (of 9) | … of those, split | Time, median of 3 (min–max) | Against bash |
|---|---|---:|---:|---:|---:|
| PaSh's own files | yes | 9 | 5 | 0.61 s (0.60–0.62) | 1.69× faster |
| Naive LLM's files | yes | 6 | 2 | 0.89 s (0.89–0.91) | 1.15× faster |
| Caruca's files, PaSh grammar | yes | 2 | 1 | 1.07 s (1.07–1.13) | 0.96× (slightly slower) |
| Caruca's files, main grammar | yes | 2 | 1 | 1.07 s (1.06–1.13) | 0.96× (slightly slower) |

Plain bash: 1.03 s (1.02–1.03). Where a source has no files for a command, PaSh used its own; those uses
are not counted for the source. The times are for the whole run, with all of a source's files in place.

![Seconds to run the script under plain bash and under PaSh with each source's files: the bar is the median of three timed runs, the thin line the fastest to slowest; the number is the speed-up against bash.](/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/figures_pilot/time_bars_pilot_times.png)

*Figure 2. Seconds to run the script under plain bash and under PaSh with each source's files. The bar is the median of three timed runs; the thin line runs from the fastest to the slowest; the number is the speed-up against bash.*

## Where the sources differ from PaSh's own files

Table 3 lists the commands where a source changed what PaSh did; Figure 3 shows the same on the pipeline, and Figure 4 the nine command uses by who supplied the files.

**Table 3.** Every command where a source's own files changed what PaSh did (the other three, `tr`, `comm`, `uniq`, came out the same with every source). "PaSh's own files used" marks a command the source has no file for; those cells say nothing about the source.

| Command | PaSh's own | Naive LLM | Caruca (both grammars) |
|---|---|---|---|
| `cat` | whole | **split** | **split** |
| `sed` | split | **whole** | PaSh's own files used |
| `col` | split | **whole** | PaSh's own files used |
| `sort` | split | split | **whole** |

![Which of the nine command uses PaSh split under each source. Filled: split into pieces; empty: run whole. A triangle marks the commands the source brought its own files for; elsewhere PaSh's own files were used. Shaded columns are where a source differs from PaSh's own files.](/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/figures_interim/split_map.png)

*Figure 3. Which of the nine command uses PaSh split under each source. Filled: PaSh ran several copies of the command at once on pieces of its input; empty: it ran one copy. A triangle marks the commands the source brought its own files for; elsewhere PaSh's own files were used. The shaded columns are where a source differs from PaSh's own files.*

- **The naive LLM's files** let PaSh split `cat`, which PaSh's own files leave whole; they keep `sort`, the
  split both faster runs share. They leave `col` whole (the file says it cannot be split) and `sed` whole (the file
  rejects the sed script because PaSh hands it over with its quotes on). The outputs stayed right.
- **Caruca's files** also split `cat`, but leave a plain `sort` whole: Caruca's method only allows a split it
  observed joining correctly, and neither of its `sort` files allows that for a plain `sort` (the
  PaSh-grammar file allows it only for `sort -m`). Its set ran slightly slower than bash; which split
  caused that was not tested, because all of a source's files were swapped in at once.
- Where a source had no files and PaSh's own were used, the result was the same as PaSh's own on every such
  use (3 of 3 for the naive LLM, 7 of 7 for Caruca), as expected.

![For each source, the nine command uses split three ways: split with the source's own files, split with PaSh's own files filled in where the source had none, and run whole.](/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/figures_interim/uses_split.png)

*Figure 4. For each source, the nine command uses split three ways: split with the source's own files, split with PaSh's own files filled in where the source had none, and run whole.*

## Next to the Caruca paper

The paper compared Caruca's files with PaSh's hand-written ones by hand on the suite's own command lines
and found them to agree on 52 of 52 commands, counting a "no split" answer as agreement when PaSh's split
needs a special merge step. On this script's command lines, Caruca's files agree with PaSh's own on what
the commands read and write (2 of 2 lines) and differ on the split decision for `sort` (0 of 1), which is
exactly that merge-step case. The naive LLM's files agree on reads and writes (6 of 6) and on the split
decision for 2 of 4 lines (`sed` and `col` differ). The paper did not report how much PaSh ran in parallel,
or time; both are new here.

## What this does not show

- One script, one input, at Koala's small size. The rest of the suite (73 scripts from 10 of the paper's 12
  sets) is running now; this draft will be rebuilt from those records.
- Times at small inputs mostly show PaSh's start-up cost; the scripts run for about a second.
- One PaSh version (commit `42a8b87`) and one setting (8 workers).

<!-- pagebreak -->

## Addendum

**A1. The script.** `oneliners/scripts/spell.sh` in Koala (commit `ccf25a57`), the successor of
`evaluation/benchmarks/oneliners/spell.sh` in the 2022 suite (one edit: `sed` in place of `iconv`). Input:
`oneliners/inputs/30M.txt`.

**A2. Words used.** *Annotation files*: the three files per command PaSh reads to decide what it may run
in parallel. *Source*: whose files PaSh used. *Command use*: one place in a script where a command is called.
*Split*: PaSh ran several copies of the command at once, each on a piece of its input, and joined the
results. *Whole*: PaSh ran one copy.

**A3. The checks.** An independent check re-ran every source and confirmed: the right files were loaded
(every file hashed against its origin); PaSh read the folder it was given (turning off one command's rules
changed only that command); all outputs matched bash and Koala's stored answer (13 of 13 re-runs); the
Mac was awake for every timed run (power log). Review: `orchestration/review_checker.md`.

**A4. How the experiment was set up, for a reader new to PaSh.**

*What PaSh does.* PaSh takes an ordinary shell script and, without changing what it computes, runs parts
of it in parallel. A command such as `sort` that reads a stream of lines can be given eight pieces of its
input at once, eight copies run side by side, and the eight results are joined. PaSh must know, for every
command, whether that is safe and how to join the pieces. That knowledge lives in three small files per
command, the *annotation files*; PaSh ships with its own, hand-written set. Where PaSh has no files for a
command, or the files say "cannot be split", it runs that part of the script as plain bash. It does this
quietly, and the output is then still correct, so a right answer alone never shows what PaSh did.

*What we compared.* Nothing new was generated during the experiment. The annotation files already
existed: PaSh's own; the naive LLM's, written weeks earlier by an off-the-shelf coding agent for 79
commands (plus `tr`, `xargs` and `awk`, added on 24 November because they appear in most suite
scripts); and Caruca's, generated from its traces for 8 commands. For each source we made a private copy of
PaSh's annotation package with that source's files swapped in for the commands it has, and PaSh's own
files for the rest, and pointed PaSh at that copy for the run. PaSh itself was not changed.

*Which scripts.* The 2022 PaSh paper evaluated PaSh on 12 sets of real scripts. Their original input
data can no longer be downloaded, so we used Koala, the same group's current benchmark suite, which keeps
updated versions of those scripts and their inputs. Ten of the twelve sets have a successor there; the
genomics set's new scripts and the package-building set need downloads, memory or Intel-only tools this
machine lacks. Every script is listed with its path in A1.

![How each script was run: once under plain bash, and once under PaSh with each of four sets of annotation files, each set being PaSh's own package with one source's files swapped in for the commands that source has. Three things are recorded per run.](/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/figures_interim/setup_diagram.png)

*Figure 5. How each script was run: once under plain bash, and once under PaSh with each of four sets of annotation files; each set is PaSh's own package with one source's files swapped in for the commands that source has. Three things are recorded per run.*

*How each script was run* (Figure 5). Once under plain bash, which gives the reference output and time; then once
under PaSh with each source's files. Every run's output was compared byte for byte with bash's, and with
Koala's stored reference answer. PaSh was given 8 workers (the machine has 8 processor cores).

*How we know what PaSh did.* Three records per run: PaSh's own log, which says which parts of the script
it compiled and which it ran in parallel; the parallel script PaSh wrote, which shows how many copies of
each command it started; and a small stand-in program placed ahead of every command, which notes each
time the command starts. A command counts as split only when PaSh's script runs two or more copies of it
and it started more often than under bash. Each source's files were also asked directly, outside PaSh,
what they would answer for every command line in the script, with the command's words passed exactly as
PaSh passes them.

*Why it takes hours.* No annotations are produced during the batch; the time is the scripts themselves
running. A one-liner takes about a second, but the natural-language scripts loop over thousands of books
and take 30 seconds to 3 minutes each, the weather script 7 minutes, and the web-search script 10
minutes. Each script runs six ways (bash and five PaSh sources, one being a second copy of PaSh's own
files to measure run-to-run noise), and timed runs are repeated. That multiplies to several hours, most of
it in three script groups.

*Timing conditions.* Timed runs were made one at a time with nothing else running in the machine, and
the Mac's power log was checked for every timed window: it was awake throughout (the machine is a Linux
virtual machine on a Mac, and a sleeping Mac would have stretched the recorded times).

*Independent check.* A separate reviewer, given the records and not the write-up, re-ran the script with
every source, hashed every file in every annotation set against its origin, turned off one command's
rules to confirm PaSh reads the folder it is given, and recomputed every number.

**A5. Records.** `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`: `results.jsonl` (per
run; the times in Table 2 and Figure 2 are its `plain` rows), `regions.jsonl` (per part), `answers.jsonl`
(each source's direct answer per command line), `manifest.json` (commits, file hashes, which source
supplied each command's files), `numbers_pilot.md` (every other number above, written by
`count_report.py`; its times come from a later re-run made while the machine was busy, and are not used).
