# Report plan: the PaSh suite experiment, for Michael Greenberg

Written 2026-11-24 by the report-ideation agent, from the four briefs in this folder, the inventory
(`coverage.md`, `coverage.jsonl`), the builder's runner (`run_koala.py`), the pilot's first records in the
VM (`~/t024/out/controls*.jsonl`, `answers.jsonl`), the earlier PaSh write-ups, and the Caruca paper's
section 7.1 and Table 1. Nothing was run or changed except this file.

The brief lists seven items. Item 5 (changes to the running agents' work) comes first here because the
orchestrator acts on it; the rest follow in the brief's order.

Two facts shape everything below:

- **Michael co-authored the PaSh paper whose suite this is** (the OSDI 2022 PaSh paper, which PaSh's
  README cites with Greenberg among its authors), as well as Caruca. So the framing rule covers PaSh too.
  State PaSh's compiler failures plainly and once, as facts about this PaSh version. Do not write "PaSh
  is the largest source of trouble", as the 19 November write-ups did.
- **The pilot shows the differences are inside a part of a script, not between parts.** `spell` is
  one part (PaSh's word is "region"), and PaSh ran it in parallel under every source tried. The sources
  differ in *which commands inside it* PaSh split. With the naive LLM's files PaSh split `cat`, `sort`
  and `tr`. With PaSh's own files for `col` or for `sed` swapped back in, it also split `col` or `sed`,
  even though the naive LLM's `sed` file allows a split. A count of parts alone would show the sources
  as identical. (Source: pilot controls, one repeat each, in the VM.)

---

## 5. Changes needed in the running agents' records and runs (do these first)

In order of importance. Each item says what to change, who does it, and why.

### 5.1 Record each command use, not just each part (builder; most important)

Add `occurrences.jsonl` to the instrumented passes: **one row per group, script, source, repeat, part
and command use.** A command use is one place where a script calls a command. `spell` calls `tr` three
times, so it has three uses of `tr`. Fields:

| Field | Content |
|---|---|
| `group`, `script`, `id`, `set`, `repeat` | as in `regions.jsonl` |
| `region`, `region_text_sha` | the part it sits in |
| `position` | its order among the commands of that part, counting repeats of a command |
| `command`, `invocation` | the command and its arguments as PaSh saw them, home folder written as `~` |
| `answer_ref` | the matching `answers.jsonl` row (`id`, `position`), or null if there is no match |
| `source`, `source_detail` | ours / pash-own / none, as in `commands.jsonl` |
| `file_answer` | one of: allows a split / says no split / no answer / raised (with the exception) / no files |
| `copies` | copies of this use in PaSh's parallel script; null if the part was not run in parallel |
| `copies_attributed` | "by command line" or "by name only" (when two uses of one command can't be told apart) |
| `split` | true / false / null |
| `why_not_split` | part not run in parallel / file says no split / no answer / raised / no files / **allowed by the file, not split by PaSh** (with any log text) |

Also add one row per use that **ran outside every part sent to PaSh**: started under bash, per the
stand-in record, but in no part's command list. Mark these with `outside_pash: true`, so the report can
give its denominator honestly.

**Why.** Tiran's case split, "commands only PaSh has files for" against "commands the naive LLM or
Caruca has files for", is per command use. Today's `regions.jsonl` lists each command once per part, by
name. Its `split_commands` and `worker_copies` are also per name: `tr` shows 17 copies for 3 uses, so the
record cannot say which uses were split. And "allowed by the file but not split" (the naive LLM's `sed`
in the pilot) has no place at all, though it is the clearest kind of difference. How to get it: the
region helper already prints each command's arguments (`s_arg`); match them to `answers.jsonl` by
invocation text, and count copies in the parallel script by full command line, not by name.

### 5.2 Add a same-files timing control (builder)

Add a source `pash-own-copy`: a second, byte-identical copy of PaSh's own package in its own folder. Run
it in the timed (plain) pass only, 3 repeats, interleaved with the others. Record it in `results.jsonl`
like any other source.

**Why.** The metrics spec uses scripts in which every command keeps PaSh's own files as the noise
control. In the six groups, that is **1 of 77 scripts for the naive LLM and 3 of 77 for Caruca**
(counted from `coverage.jsonl`), so that control barely exists. The pilot's differences are 0.1 to 0.3 s
on a script of about 1 s. Without two identical copies timed side by side, nobody can tell a real
difference from noise. Cost: about 3 extra PaSh runs per script. Also rotate the order of sources from
repeat to repeat, so that no source always runs right after bash. It is cheap.

### 5.3 Write down that every timed window is valid (orchestrator, from the Mac side)

For each line of `run_windows.jsonl`, write one line to `timing_check.jsonl`: the window, sleep and wake
events in it (from the Mac's power log), whether the Mac was on mains power at the start and end (from
its battery status), and the VM's load average at the start and end of each script's timed runs (one
`uptime` per script, which the builder adds). Any window with a sleep, or on battery, is re-run before
its times are used.

**Why.** Times measured inside the Lima VM include any time the Mac slept. The last report had to admit
"timings were taken with the Mac on battery power". The report should say "the Mac was awake and on mains
power for every timed run" and point to the record that shows it.

### 5.4 Pair every source with PaSh's own files, in a counting script (new small task, after the runs)

A count-only script (`count_report.py`) reads the records and writes `numbers.md`. Every number in the
report is copied from `numbers.md`, and the checker re-runs the script. It must:

- **Pair parts** across sources by (`id`, `region_text_sha`) and label each part for each source:
  run in parallel with both / only with this source (gained) / only with PaSh's own (lost) / with
  neither.
- **Pair uses** the same way, by (`id`, `region_text_sha`, `position`).
- **Split the reasons** a part was not run in parallel into "the same under PaSh's own files" (shared)
  and "only with this source".
- **Count agreement with PaSh's own files**, for the comparison with the paper, from `answers.jsonl`.
  The unit is each distinct command line in the suite for which the source has its own files and PaSh's
  own files exist. Count "same inputs and outputs" and "same split decision" separately. Leave out
  command lines where PaSh's own files don't exist, and count those separately as "answers PaSh's own
  files don't give". Also count separately the cases where PaSh's own files split only with a special
  merge step and the source says no split: the paper counted such cases as agreement.
- **Pool repeated launches.** A script that Koala's launcher starts more than once (ids ending in `#n`)
  counts once. Its output is right only if every launch is right; its parts are counted once by text.

**Why.** "Whether and how the results differ" is a comparison with PaSh's own files, item by item. The
records allow it, but only if the pairing is done the same way every time and checked. The sources cover
different commands, so totals alone would mislead.

### 5.5 Smaller changes (builder unless noted)

| Change | Why |
|---|---|
| Add `source` (ours / pash-own / none) to every `answers.jsonl` row; today only the text `files_from` is there | the agreement count filters on it |
| Add each script's input size in bytes to `invocations.jsonl` | the time chart needs the scale; the small inputs are small |
| Start the stand-in programs for every command in `coverage.jsonl`, not only words found in the scripts' own folder; then list the commands seen in one record and not the other | the inventory found commands started inside helper scripts. A command started but not watched has no answer row and no use row |
| When a part is "other", start its reason with a fixed label for each state found, for example "allowed by the files, not split by PaSh" or "nothing in this part can be split under any source" | keeps "other" small and explainable without changing Tiran's list of outcomes |
| Checker: confirm that each script's sequence of part texts is identical across the sources (repeat 1) | if it isn't, pairing by text breaks and must fall back to order |
| Checker: confirm that bash's own output is identical across its runs; scripts where it varies leave the correctness count and are listed | otherwise a script that differs from run to run reads as a wrong answer |
| Run the "the folder decides" controls once at the start of the full batch and once at the end, on `spell` | shows nothing drifted during the batch, as task 022 did |
| One display-name map (in `manifest.json` or a `sets.json`), used by every table and chart: pash-own → "PaSh's own files", naive → "Naive LLM's files", caruca-pash → "Caruca's files, PaSh grammar", caruca-main → "Caruca's files, main grammar", pash-own-copy → "PaSh's own files, second copy" | one name per thing, everywhere |
| Optional, if the batch runs long: one instrumented repeat per source instead of three, with stability checked on a sample of 10 scripts | the instrumented passes double the run count; split choices have been stable so far |

### 5.6 Facts for the orchestrator to record in memory

This agent was told to change nothing but this file, so these are left for the orchestrator:

- Michael Greenberg is a co-author of the OSDI 2022 PaSh paper ("Practically correct, Just-in-Time
  shell script parallelization"; read from the citation in PaSh's README, `~/dev/stevens/pash/README.md`,
  2026-11-24). It belongs in `memory/project_key_people.md`.
- In the six Koala groups (77 scripts), only 1 script has no command with naive LLM files, and only 3
  have no command with Caruca files (from `coverage.jsonl`, 2026-11-24). So the noise control needs its
  own source.
- `spell` is a single part, and the sources differ only in which commands inside it are split (pilot
  controls, 2026-11-24).

---

## 1. Shape of the report

Target: **a body of about three printed pages, most of it tables and charts** (four tables, three
charts, about 600 words of prose), then an appendix of no more than four pages. Section by section:

| # | Section | What Michael learns there | Length |
|---|---|---|---|
| 0 | In short | the answer in five sentences: outputs, what differs, the paper comparison | 1 paragraph |
| 1 | What we ran | which scripts (by their 2022 names), the five ways each was run, which commands each source has files for | 6 lines + chart C |
| 2 | What we saw | the at-a-glance table, one row per source | table 1 + 3 bullets |
| 3 | Where the sources differ from PaSh's own files | the case split, the per-part picture, every command where a source changed what PaSh did, what each adds | table 2, chart A, table 3, 2–4 bullets |
| 4 | Time | one chart against PaSh's own files, and how big the noise is | chart B + 2 sentences |
| 5 | Next to the Caruca paper | the paper's PaSh check beside ours | table 4 + 2 sentences |
| 6 | What this does not show | limits, 3–4 bullets | 4 lines |
| A | Appendix | words used; the script map; reasons per part; every difference with its command line; the checks; records | ≤ 4 pages |

---

## 2. Every table and chart

Common rules: every rate written as "a of b"; numbers right-aligned; PaSh's own files always the first
row or panel, marked as the reference; one color per source, the same in every chart (PaSh's own dark
grey, naive LLM blue, Caruca PaSh grammar orange, Caruca main grammar light orange). Load the `dataviz`
skill before drawing. Draw charts at portrait page width (6.5 in), with 8 pt or larger text, and export
PNG at 300 dpi. "Repeat 1" below means the first instrumented repeat. The other repeats are used only to
confirm stability.

### Table 1: What PaSh did with each source's files

*Exists to support:* "With every source PaSh's output matched bash in [x of N] scripts; the sources differ
in how much PaSh ran in parallel, not in whether the output was right."

| Source | Output same as bash | Scripts with any part run in parallel | Parts run in parallel | Command uses split | Faster than bash |
|---|---|---|---|---|---|
| PaSh's own files | a of N | b of N | c of P | d of U | e of N |
| Naive LLM's files | | | | | |
| Caruca's files, PaSh grammar | | | | | |
| Caruca's files, main grammar | | | | | |

- **N** = scripts whose bash output is identical across all of bash's runs (5.5).
  *Output same as bash* = every PaSh run of that script and source, both passes and all repeats, has
  `same_as_bash` and `output_files_same_as_bash` true, and none timed out. From `results.jsonl`.
- *Scripts with any part run in parallel* = `region_outcomes.per_distinct.parallelized` ≥ 1, from
  `results.jsonl` (instrumented, repeat 1).
- **P** = distinct parts summed over scripts (`region_outcomes.distinct_regions`). It is the same for
  every source; the counting script must check that. *Parts run in parallel* =
  `per_distinct.parallelized`. The count per execution, which counts a loop's part once per pass, goes
  to appendix table A3.
- **U** = command uses inside parts sent to PaSh (`occurrences.jsonl`, repeat 1, `outside_pash` false).
  *Split* = `split` true.
- *Faster than bash* = the median of 3 timed runs is below bash's median (`results.jsonl`, plain mode).
  Give the median speed-up in brackets.
- At a glance: four rows of numbers in one format. Any wrong output is shown in red with its count. No
  other emphasis.

### Table 2: Commands a source brings its own files for, and what PaSh did with them

*Exists to support Tiran's case split:* "Where a source brings its own files, PaSh split [s of u] of
those uses with them, against [p of u] with its own files on the same uses. Where PaSh's own files were
filled in, the result matched the PaSh's-own run on [z of w] uses."

| Source | Uses with the source's own files | … split with them | … the same uses split with PaSh's own files | Uses with PaSh's own files filled in | … result same as with PaSh's own | Uses with no files from anyone |
|---|---|---|---|---|---|---|
| Naive LLM | u of U | s of u | p of u | w of U | z of w | n of U |
| Caruca, PaSh grammar | | | | | | |
| Caruca, main grammar | | | | | | |

- From `occurrences.jsonl` repeat 1, paired with PaSh's own (5.4). "Same result" means `split` is equal.
  A difference among the filled-in uses can only come from a neighbouring command in the same part. Name
  it in the appendix.
- At a glance: three rows. The two "split" columns sit side by side, so the gain or loss reads in one
  look.

### Chart A: The scripts' parts, compared with PaSh's own files

*Exists to support:* "Most parts come out the same under every source; [g] parts were run in parallel
only with the naive LLM's files, and [l] only with PaSh's own."

- Horizontal bars, 100% stacked, one bar per source (naive LLM, Caruca PaSh grammar, Caruca main
  grammar), plus a thin reference bar on top for PaSh's own files (run in parallel / not).
- Four segments: run in parallel with both (blue); only with this source (teal); with neither (light
  grey); only with PaSh's own files (orange). Print the count inside each segment ("41 of 120"), and
  leave a segment unlabelled only when it is too narrow for its number.
- Data: `regions.jsonl` repeat 1, distinct parts, paired by (`id`, `region_text_sha`).
- At a glance: three almost entirely blue-and-grey bars, with any teal or orange plain to see.

### Table 3: Every command where a source changed what PaSh did

*Exists to support "how they differ", one command at a time.*

| Command | Uses in the suite | PaSh's own | Naive LLM | Caruca, PaSh grammar | Caruca, main grammar | Output |
|---|---|---|---|---|---|---|
| `cat` | [n] | split [0] | split [k] | split [k] | split [k] | all same as bash |
| … | | | | | | |

- Rows: only commands for which at least one source's `split` differs from PaSh's own on at least one
  use. Order: by number of uses. Each cell: "split k" out of the row's uses. Grey text where the cell
  equals PaSh's own, bold where it differs. The last column says "all same as bash", or names how many
  scripts went wrong.
- Caption: "The other [K] commands: every source gave the same result as PaSh's own files."
- Under the table, 2–4 one-line bullets on what each source adds, for example "The naive LLM's files let
  PaSh split `cat`, which PaSh's own files leave whole." Every command line behind a bullet goes in
  appendix table A4, not in the body. (The `cat` row above is an illustration, not a result.)

### Chart B: Time with each source's files, against PaSh's own files

*Exists to support:* "Times differ from PaSh's own files only where the split choices differ, and by no
more than [x]% elsewhere, which is the size of the noise."

- Small multiples, three panels side by side at portrait width: naive LLM, Caruca PaSh grammar, Caruca
  main grammar. Each is a scatter, log–log. x = median seconds with PaSh's own files; y = median seconds
  with this source's files; one point per script; a diagonal line where the two are equal.
- In every panel, grey points show the second copy of PaSh's own files against the first. Their spread
  is the noise (5.2).
- Filled point = output same as bash; red cross = not. Points whose split choices differ from PaSh's
  own are drawn larger. Label only the 2–3 points farthest from the diagonal, by script name.
- Data: `results.jsonl` plain mode, 3 repeats, median per script and source. The min–max range goes to
  appendix table A5, not to error bars, which would clutter the chart.
- At a glance: points on the diagonal, a grey cloud showing the noise, and the few points off it named.

### Chart C: Which of the suite's commands each source has files for

*Exists to support the case split:* "The naive LLM has files for [23] of the [35] commands these
scripts use, Caruca for [6], PaSh's own for [20]; [8] have files from nobody."

- A grid: one column per command, sorted by the number of scripts using it (most used on the left,
  names turned 90°), with a thin bar above each giving the number of scripts (of N). Three rows: PaSh's
  own, naive LLM, Caruca. A filled square means the source has files for the command.
- Data: `coverage.jsonl` (commands read from the scripts), reconciled with `commands.jsonl` (commands
  seen starting; 5.5). The bracketed numbers are the inventory's counts; recount them from the records.
- At a glance: `tr`, `xargs` and `awk` empty in the naive LLM's row, and Caruca's six squares at the
  most used end.

### Table 4: Next to the Caruca paper's PaSh check

*Exists to let Michael put the numbers beside Table 1 and section 7.1 of the paper.*

| What was checked | Caruca paper (PaSh's suite as of 2022) | Caruca's files here | Naive LLM's files here |
|---|---|---|---|
| Files agree with PaSh's hand-written files on the suite's own command lines | 52 of 52 commands, compared by hand | inputs and outputs: a of b command lines; split decision: c of b; all lines agree for d of e commands | same, for its commands |
| Suite output identical with the files swapped in | yes, by hash (number of scripts not given) | x of N scripts | y of N |
| Parts of the scripts PaSh ran in parallel | not reported | c of P (PaSh's own: c0 of P) | |
| Time against bash | not reported | median speed-up | |

- Row 1 from `answers.jsonl`, counted as in 5.4. Row 2 from table 1. Rows 3–4 from table 1 and chart B.
- Caption, plain and short. The paper's 52 are the 52 PaSh commands it had hand-written files for; here
  Caruca has files for 8 commands, 6 of which these scripts use. The suite is Koala's version and runs
  on its small inputs. The paper counted Caruca right when it found a command pure, whether or not PaSh
  could split that command with a merge step; the cases this affects are counted separately in footnote
  [n]. One sentence on how the paper's
  Caruca files and these were made, taken from task 020's README.

### Appendix tables (not in the body)

| Table | Content | Records |
|---|---|---|
| A1 | The scripts: 2022 set name, Koala group, scripts run, how close to the published scripts; sets not run and why | `coverage.jsonl`, `coverage.md` |
| A2 | Words used (the glossary below) | — |
| A3 | Why parts were not run in parallel, by reason (rows) and source (columns), as distinct parts and per execution, with "shared with PaSh's own" and "only with this source" kept apart | `regions.jsonl`, 5.4 |
| A4 | Every use whose result differs from PaSh's own: script, command line, PaSh's own result, each source's result, output same as bash | `occurrences.jsonl`, `results.jsonl` |
| A5 | Times per script: bash and each source, median and min–max of 3 | `results.jsonl` plain |
| A6 | The checks: the folder decides (before and after the batch), the right files loaded, repeats agree, Mac awake and on mains power, the checker's results | `controls.jsonl`, `timing_check.jsonl`, `review_checker.md` |
| A7 | Records and how to rebuild every number | file list with permalinks |
| (chart) | Chart C at full size with all commands, if the body version is cut down | |

---

## 3. The headline

**Order.** Output first (a parallel run that changes the answer matters more than any speed), then "do
the sources differ, and how", then the paper comparison. Never rank the sources by a single
score: they have files for different commands, so a ranking would compare unlike things.

**Wording rules for the headline and the whole body.**

- Lead every sentence with what was seen. Give every rate as "a of b", with b named the first time
  ("of the 120 parts PaSh was asked to compile").
- Gains are what a source *adds* ("the naive LLM's files let PaSh split `cat`"). Losses are stated as
  what happened, without blame: "with Caruca's PaSh-grammar files PaSh ran `sort` whole". Same for PaSh:
  "PaSh's compiler stopped on [k] parts under every source, and ran them as plain bash". Not "PaSh
  failed".
- Say it once, plainly: **"Each run swapped in all of a source's files at once. A difference belongs to
  the source as a whole, or to the commands it swapped in that script; we did not swap one command at a
  time."**
- Say once why the naive LLM has no files for `tr`, `xargs` and `awk`: its files exist only for the 79
  commands in the Caruca paper's Fig. 7, and those three are not among them.

**Draft headline paragraph (placeholders in brackets):**

> We ran [77] scripts of PaSh's benchmark suite, in the versions kept in Koala, under plain bash and
> under PaSh with three sources of annotation files: PaSh's own, the naive LLM's and Caruca's. PaSh's
> output matched bash's in [77 of 77] scripts with every source. The sources differ in how much PaSh ran
> in parallel. Of the [U] places where the scripts call a command, PaSh split [d0] with its own files,
> [d1] with the naive LLM's and [d2] with Caruca's. On the uses where a source brings its own files,
> PaSh split [s of u] with them, against [p of u] with its own. Where a source had no files and PaSh's
> own were used, the result was the same as PaSh's own on [z of w] uses, as expected. Beside the paper's
> check: on the suite's own command lines, Caruca's files give the same split decision as PaSh's
> hand-written files on [c of b] lines, against the paper's 52 of 52 commands compared by hand.

If any output was wrong, the first sentence names it instead: "With [source]'s files PaSh gave a wrong
answer on [k of N] scripts ([what])."

---

## 4. What to leave out of the body

Michael would find these too much in the 19 November write-ups, and they go to the appendix or the
records:

- **Changing units.** The earlier write-ups mixed runs, lines and scripts within one paragraph ("655 of
  1,013 runs … 423 … 186 … 19"), and counted each naive LLM run of a command separately. Here each table
  uses one unit, named in its title.
- **Internal states and coined names.** "Split set up, no data arrived", "side", "allowed, not split",
  "organic", "ours", "fell back". Say what happened in words; the few states needed are defined in A2.
- **The method.** The stand-in programs, the log lines counted, the folder option, the two passes,
  package hashes, folder names: all to A6 and A7. The body gets one line: "We checked that PaSh used the
  files we gave it and that every timed run was valid (appendix A6)."
- **The harness's own corrections.** Section 8 of the earlier observations; corrections noted inline
  in the text.
- **PaSh's faults as a list.** One line and a link. One of the faults found earlier has been reported
  to PaSh's authors; the rest wait for Tiran's review.
- **Opinion sections** ("What this suggests"). At most one sentence, marked as a reading.
- **Detailed recipes.** Round robin, consecutive chunks, merge-step names, class names, option names,
  command lines. Command names such as `sort` stay; command lines go to A4.
- **Per-execution counts, min–max times, repeat stability, the five control sources.** Appendix.
- **The word "coverage", and "covers".** In this project the word means how much of a command's
  real-world use a description reaches. Say "has files for".
- **The earlier task 022 results.** One link, in A7.
- **A styled web page.** The 19 November page had a masthead, an eyebrow line, ten sections and
  hover tips. A page for Michael should read like a short note (see 7).

---

## 6. Skeleton of the report

Location: `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report.md`, with the attribution
notice the other analysis documents carry, at the top. Square brackets mark placeholders, all filled
from `numbers.md`.

```markdown
# PaSh's benchmark suite, with three sources of annotation files

**To:** Michael Greenberg · **From:** Tiran Dagan · **Date:** [date] · Draft

**In short.** [The headline paragraph from section 3 of the plan.]

## What we ran

PaSh decides what it may run in parallel from three small files per command, its annotation files: what
the command reads and writes, and whether its input can be cut into pieces and the results joined. We
gave PaSh three sources of these files and compared each with plain bash.

- **The scripts.** [77] scripts from PaSh's benchmark suite, in the versions kept in Koala, because the
  2022 inputs can no longer be downloaded. They stand for six of the twelve sets in the 2022 PaSh
  paper's Table 1: Classics, Unix50, COVID-mts, NLP, AvgTemp and WebIndex. [71 of 77] are the published
  scripts, unchanged or lightly edited; the rest are new in Koala. Small inputs. (Appendix A1.)
- **The five ways each script ran.** Plain bash, which gives the reference output and time, and PaSh
  with 8 workers and:

  | Source | Files PaSh used |
  |---|---|
  | PaSh's own | the files that ship with PaSh |
  | Naive LLM | files written by an off-the-shelf coding agent for the 79 commands of the Caruca paper's Fig. 7, given only the goal, PaSh's file format and four examples; it never ran PaSh |
  | Caruca, PaSh grammar | files Caruca generated from its traces for its 8 PaSh commands, using the small grammar it keeps for PaSh |
  | Caruca, main grammar | the same, from Caruca's full grammar where it has one (`cut`, `rm`, `sort`) |

- Where a source has no files for a command, PaSh used its own. Each run swapped in all of a source's
  files at once, so a difference belongs to the source, or to the commands it swapped in that script,
  never to one command alone.
- Three timed runs of each; we report the median.

[Chart C: which of the suite's commands each source has files for.]

## What we saw

[Table 1]

- [Output: with every source, PaSh's output matched bash in a of N scripts. / Or the wrong ones, first.]
- [Parts: PaSh ran c of P parts in parallel with its own files; the other sources within ±k.]
- [Uses: the sources differ most in which commands inside a part PaSh split: d0 / d1 / d2 of U.]

## Where the sources differ from PaSh's own files

[Table 2: the case split]

[Chart A: parts gained, kept and lost against PaSh's own files]

[Table 3: every command where a source changed what PaSh did]

- [What the naive LLM's files add, one line per point, e.g. "let PaSh split `cat` in k of n uses;
  outputs stayed the same as bash".]
- [What Caruca's files add or where they leave a command whole, one line per point.]
- [Shared: on k parts PaSh's compiler stopped under every source and ran them as plain bash.]

## Time

[Chart B]

[Two sentences. Example shape: "At these input sizes most scripts take about [1] s in bash, and two
identical copies of PaSh's own files differ by up to [x]% from run to run. Beyond that, the sources
differ in time only on the [k] scripts where their split choices differ (labelled)."]

## Next to the Caruca paper

[Table 4]

[Two sentences: what matches the paper's check, and what this run adds that the paper did not report
(how much PaSh ran in parallel, and time).]

## What this does not show

- One input per script, at Koala's small size: a split that came out right here is not proved right on
  every input.
- Six of the twelve 2022 sets; the other six need downloads or machines we do not have (appendix A1).
- One PaSh version ([commit]) and one setting (8 workers).
- The naive LLM's files are its first run for each command; its runs differ from one another (appendix
  A7 links the repeat study).

---

## Appendix
A1 The scripts · A2 Words used · A3 Why parts were not run in parallel · A4 Every difference, with its
command line · A5 Times · A6 The checks · A7 Records
```

**Words used (appendix A2; each is also defined in the body the first time it appears):**

| Word | Meaning |
|---|---|
| annotation files | the three files per command PaSh reads to decide what it may run in parallel |
| source | whose files PaSh used: PaSh's own, the naive LLM's, or Caruca's (two versions) |
| part | a piece of the script PaSh's compiler is asked to handle, usually one pipeline (PaSh calls it a region); a loop sends its part once per pass, and the body counts each part once |
| run in parallel (a part) | PaSh produced a parallel version of the part and ran it |
| split (a command use) | PaSh ran several copies of the command at once, each on a piece of its input, and joined the results |
| command use | one place in a script where a command is called; three calls of `tr` are three uses |
| output same as bash | the same bytes on standard output and the same output files as plain bash |
| PaSh's own files filled in | the source has no files for the command, so PaSh's own were used |
| naive LLM | an off-the-shelf coding agent (Claude Code, model Claude Fable 5.1) given only the goal, the formats and four examples |

---

## 7. Delivery

**Recommendation: a PDF from Markdown, sent with a two-line email. No results page for Michael.**

- Build `report.md` → `report.pdf` with the repo's converter (`npm run convert`, Letter, portrait).
  Reference the chart PNGs by absolute path, so the converter does not shrink them to 1,600 px; restore
  relative paths afterwards and check with `cmp`. Put a page break before the appendix, and design every
  chart for portrait width: wide charts print too small to read.
- Name documents without their file extension in the text, following the handout rule, and list in an
  assembly note what goes in the package: the report PDF, plus `coverage` if Tiran wants the script map
  in full.
- A results page adds nothing Michael asked for, and the last one is the kind of length he dislikes. If
  Tiran later wants a link to share, publish the same body as a plain page: the same tables and charts,
  no extra sections.
- Add one dated bullet to `naive_llm_caruca/latest_findings.md` when the report is done, linking to it.

**Build order:** finish the runs (with 5.1–5.3) → checker passes → `count_report.py` writes
`numbers.md` → charts script writes `figures/*.png` from `numbers.md`'s data → `report.md` written from
the skeleton → checker re-runs the count and compares every number in the report → PDF.

---

## Open question for Tiran

At Koala's small inputs, the pilot script takes about one second in plain bash, and the differences
between sources were 0.1 to 0.3 seconds. Much of that second is PaSh starting up, so the time chart may
show little beyond noise. Should we also time a handful of scripts at Koala's next larger input size,
which needs a new download, or report time at the small size only and say why?
