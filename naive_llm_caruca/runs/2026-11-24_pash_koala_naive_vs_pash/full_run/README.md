# PaSh's benchmark suite with three sources of annotation files (full run, 2026-11-24 to 25)

**What this is.** PaSh speeds up shell scripts by running parts of them as several copies at once on
pieces of the input ("splitting" a command) and joining the results. It decides what it may split from
*annotation files*: three small files per command saying what the command reads and writes and whether
it can be split. This run puts PaSh's published benchmark suite (Koala's current versions of it,
because the original inputs can no longer be downloaded) through PaSh with different sets of those
files, and compares each set with PaSh's own.

Every number below is copied from [numbers.md](numbers.md), which `summarise.py` builds from the records
here and only counts. The pilot on one script is in the folder above.

## What was run

**86 scripts** from nine Koala groups: oneliners 12, unixfun 34, covid 5, nlp 23, weather 2,
web-search 1, analytics 3 (port-scan left out), file-mod 5, bio 1 (`bio.sh`). Inputs at Koala's small
size (web-search and bio at the smallest, "min"). Each script was started exactly as Koala's own
launcher starts it (recorded, then replayed), inside the Lima virtual machine `pash` (8 cores, Ubuntu
24.04, PaSh commit `42a8b87`, annotation package 0.2.4), with 8 copies per split.

| Source (set of files) | Files loaded |
|---|---|
| Plain bash | none: the reference output and time |
| PaSh's own files | PaSh's own, for every command it has |
| Naive LLM's files | the naive LLM's, for all 82 commands it has (first campaign run of each, plus `tr`, `xargs`, `awk` added 2026-11-24); PaSh's own for the rest |
| Naive LLM, sed file v2 | the same, but `sed` from the campaign's second `sed` run. Run on the 12 oneliners/unixfun scripts that use `sed` and on all 40 scripts of the other groups (52) |
| Caruca's files, PaSh grammar | Caruca's, for its 8 commands (`cat cp cut grep rm sort split wc`), from its small PaSh grammars; PaSh's own for the rest |
| Caruca's files, main grammar | the same, from Caruca's main grammar where it has one (`cut`, `rm`, `sort`) |
| PaSh's own files, second copy | an identical copy of PaSh's own files, timed only: it shows how much times vary by chance |

All of a source's commands are swapped in at once (Tiran's decision), so a difference belongs to the
source as a whole, not to one command. Each script and source ran once with a stand-in program that
records every program start (to see what was split), and **three times timed** without it. Times are the
median of the three.

## What was found

**1. Every printed output was right.** Under every source, in every run, what the script printed
matched plain bash (86 of 86 scripts; 52 of 52 for the second sed file). For the 46 oneliners and
unixfun scripts it also matched Koala's stored answer (46 of 46). The other groups keep their answers in
a form this run did not check against.

This holds for printed output only. 32 scripts also write files. Of their 588 timed runs, 211 had files
the same as bash's; 352 could not be checked (the source ran before bash in its repeat, so there was no
bash run to compare with; see "Faults found and fixed"); 25 differ: web-search 19 and bio 6. Those 25
say nothing either way. web-search's files differ even between two runs of plain bash, and bio's check
recorded bash's own run as different from bash, so that check itself was broken.

**2. PaSh ran most of these scripts as plain bash, whatever the files.** It ran at least one part in
parallel in 41 of 86 scripts with its own files, 43 of 86 with the naive LLM's, 29 of 86 with
Caruca's PaSh-grammar files and 41 of 86 with Caruca's main-grammar files. Of the 177 distinct parts
the scripts send PaSh, it ran 41 in parallel with its own files. The rest fail for reasons that are the
same under every source: loops that PaSh's compiler does not handle ("not implemented"), commands nobody
has files for (a function the scripts define, `echo`, `read`, `[`), and a few compiler crashes.

**3. Against PaSh's own files, part by part** (177 distinct parts):

| Source | Run in parallel with both | Gained (only with this source) | Lost (only with PaSh's own) |
|---|---|---|---|
| Naive LLM's files | 41 | 2 | 0 |
| Caruca's files, PaSh grammar | 29 | 0 | 12 |
| Caruca's files, main grammar | 41 | 0 | 0 |

The second sed file was run on 139 of these parts: 14 in parallel with both, none gained, none lost.

**4. What changed, command by command** (scripts in which the command was split with this source but
not with PaSh's own, and the reverse):

| Source | Split more often | Split less often |
|---|---|---|
| Naive LLM's files | `cat` 43 scripts, `awk` 6, `tr` 3, `cut` 2, `sort` 2, `grep` 1 | `sed` 5, `col` 1 |
| Naive LLM, sed file v2 | `cat` 14, `awk` 4 | `col` 1 (no `sed` lost) |
| Caruca's files, PaSh grammar | `cat` 29 | `sort` 17, `cut` 9, `sed` 5, `tr` 5, `grep` 4 |
| Caruca's files, main grammar | `cat` 41 | `sort` 17 |

- **Caruca's files never split a plain `sort`** (17 scripts). Caruca's method only allows a split whose
  pieces are joined end to end, and `sort` needs a merge. With the PaSh-grammar files, options missing
  from Caruca's small option tables also made PaSh's compiler fail on whole parts (14 compiler failures
  against 4 with PaSh's own files). Of the 12 lost parts, 10 are compiler crashes and 2 are recorded
  as "other".
- **The naive LLM's 2 gained parts** (`unixfun/12`, `unixfun/16`) are parts where PaSh's own files crash
  PaSh's compiler (an `AssertionError` in `pipe_append`). The naive LLM's files avoid that crash, and that
  is where its gains for `tr`, and for `cat` in those scripts, come from.
- **The naive LLM's first `sed` file loses `sed` in 5 scripts**: PaSh hands it the sed script with its
  quotes on, and the file reads the quote as an unknown command. Its second `sed` file does not.
- **Two naive LLM files raise an error inside PaSh**, which PaSh hides and treats as "no annotation":
  `wc` on `wc -l` (8 uses in 7 scripts: 6 unixfun scripts and web-search) and `join` (weather). The outputs stayed right.
- **Splitting `cat` of one file**, which the naive LLM's and Caruca's files all allow and PaSh's own
  never do, is the most common difference.

**5. Time.** Speed-up over plain bash, geometric mean over the scripts (above 1 = faster than bash):

| Source | Scripts | Speed-up over bash | Time against PaSh's own (below 1 = faster) |
|---|---|---|---|
| PaSh's own files | 86 | 0.42x | 1.00 |
| Naive LLM's files | 86 | 0.37x | 1.15 |
| Naive LLM, sed file v2 | 52 | 0.51x | 1.07 |
| Caruca's files, PaSh grammar | 86 | 0.41x | 1.05 |
| Caruca's files, main grammar | 86 | 0.40x | 1.06 |
| PaSh's own files, second copy | 86 | 0.43x | 0.99 |

- At these input sizes **PaSh is slower than plain bash on most scripts with any files**: its start-up
  and compile cost is larger than the work. With its own files it was more than 10% faster than bash in
  10 of 86 scripts; with the naive LLM's in 6, with Caruca's main-grammar files in 5, with Caruca's
  PaSh-grammar files in 1.
- **The noise check**: the identical second copy of PaSh's own files took 0.83 to 1.13 times as long as
  the first (median 0.99; 4 of 86 scripts differ by more than 10%). Differences inside that band say
  nothing.
- **The second sed file's row cannot be compared directly with the others**: it covers 52 scripts, not
  86 (the 12 oneliners and unixfun scripts that use `sed`, and all 40 of the other groups; in 27 of the 52
  bash starts no `sed` at all).
- The naive LLM's files are 15% slower than PaSh's own overall. They are slower by more than 10% in 34 of
  86 scripts, faster in 4 (from `numbers.md`, section 6).
- **web-search** (the slowest script, about 11 minutes) gained nothing from PaSh: no part ran in parallel
  under any source. Its medians: bash 640 s, PaSh's own files 710 s, naive LLM 707 s, Caruca 698 s and
  687 s, second copy 680 s. Its repeats 1 and 3 are redone runs (see "Faults found and fixed").

**6. The method check.** For every command use in a part PaSh ran in parallel, the files' answer (asked
with the words PaSh gives them) was compared with what PaSh did: 956 of 957 agree. The one exception is
a counting limit, not a disagreement: two `awk` uses in one part (unixfun/19) whose copies could not be
told apart in PaSh's script.

## Faults found and fixed during the run

| When | Fault | Effect | Fix |
|---|---|---|---|
| 13:22 | unixfun scripts are started by a relative path, which my runner read from the wrong folder | all 34 failed in the runner (nothing ran) | read the script relative to its own folder; the 34 were run again |
| 13:50 | the answers file held every command line of every loop (1.4 GB) | slow, too big to keep | one file per script; here, loops' direct answers are grouped (count + one example); the full files are in the VM |
| 21:00 | uses "outside every part" were matched to bash's starts by full command line; in loops the rebuilt line lacks the loop's variable values | 1,174,718 false rows | counted per command instead (starts under bash minus uses in all parts); records repaired by `fix_records.py`, report in `fix_records_report.json`; the runner fixed |
| 21:00 | when two uses in a part share command and options, copies were shared out evenly | 178 uses with wrong copy counts | matched by exact words where PaSh's script allows (174); 4 left; no split result changed |
| 23:40 | **recorder fault**: in the repeats the order of sources rotated bash out of first place, so sources run before bash had no reference and were recorded as "not same as bash" | 482 rows recorded wrong (all were in fact identical to their repeat's bash); 642 rows' output-file flag recorded wrong | the summary compares against the same repeat's bash hash (records unchanged); the runner now runs bash first in every repeat and keeps both hashes. For scripts that write files, the file check is missing ("not checked") for repeat 2 of the slow groups and for every repeat-3 run that came before bash |
| 23:40 | **web-search had no `node` in its timed runs**: its launcher finds `node` under the top folder's `.tools`, which my shadow copy lacked (the stand-in programs had supplied it) | its repeat-1 timed runs stopped at 18-54 s | linked `.tools`; its repeats 2 and 3 ran with `node`; repeat 1 redone on 2026-11-25 (651-710 s, outputs same as bash); the 7 broken rows are left out |

**The Mac slept** four times during runs (lid closed), listed in `sleep_events.jsonl`. Two scripts that
it hit (`nlp/uppercase_by_type`, `nlp/sort_words_by_rhyming`) were run again. On 2026-11-25 from 08:21
the Mac ran on battery, which slowed web-search's repeat 3 by about 10%. That repeat was redone, and the 7
battery rows are left out.

**Short battery stretches and one dark wake** are left in, because none of the times they touch looks
unusual (from the Mac's power log, `pmset -g log`):

| When | What | Runs touched |
|---|---|---|
| 11-24 13:46:57–13:50:16 | battery, 3 min 19 s (holds the 13:47 sleep, which fell between runs) | `unixfun/34`, `unixfun/35` |
| 11-24 15:25:35–15:26:01 | battery, 26 s | the last 26 s of `nlp/trigram_rec` |
| 11-24 16:23:57–16:24:01 | battery, 4 s | `nlp/vowel_sequencies_gr_1K` |
| 11-24 16:36:22–16:36:28 | battery, 6 s | `nlp/merge_upper` |
| 11-24 22:03:28–22:03:38 | battery, 10 s | web-search, main phase (its timed rows from that phase were replaced by the redo) |
| 11-25 10:15:03–10:15:27 | battery, 24 s | web-search, redone repeat 1 (plain bash) |
| 11-25 10:43:25–10:44:26 | a 61-second "dark wake" with the lid closed, on mains power; `caffeinate` held off sleep, and the power log does not count it as sleep | web-search, redone repeat 1 (651 to 710 s, in line with the other repeats) |

Every other timed run was on mains power with the Mac awake.

## Files

| File | What it is |
|---|---|
| `numbers.md`, `summarise.py` | every count, and the script that makes them (only counts; applies the fix-ups listed above) |
| `results.jsonl.gz` | one row per script, source, pass and repeat: what PaSh did, outputs, time |
| `regions.jsonl.gz` | one row per distinct part, source and pass: its text, commands, sources, outcome, reason |
| `occurrences.jsonl.gz` | one row per command use (repaired): whose files, their answer, copies, split or why not |
| `answers/` | per script: each source's answer for each command line (loops grouped, see above) |
| `commands.jsonl.gz` | per script, command and source: whose files |
| `controls*.jsonl` | the checks that the folder decides, on `spell`, before and after the batches |
| `run_windows.jsonl`, `sleep_events.jsonl` | time window and VM load for every script; the Mac's sleeps |
| `invocations.jsonl`, `manifest.json`, `sets.json` | how each script is started; versions, file hashes and the source of every command's files; display names |
| `logs/` | PaSh's logs (first run of each source; long logs cut to their first 2,000 and last 500 lines) |
| `fix_records.py`, `fix_records_report.json` | the one-off repair of the per-use records |
| `copy_out*.sh`, `*.log` | the scripts that copied records out of the VM as each script finished |

The runner is `../run_koala.py`. Full answers stay in the VM under `~/t024/out/answers/`, full logs under `~/t024/out/logs/`.
