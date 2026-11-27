# PaSh's suite rerun with Caruca's expanded annotation files (2026-11-26)

**Status: done.** Batch 2026-11-26 15:15 to 2026-11-27 04:37, 86 of 86 scripts, no runner errors. Every number
here is copied from `numbers.md` (made by `summarise.py`) or `per_command_caruca-*.md` (made by
`per_command_caruca.py`); both only count.

## What was found

**1. Caruca's expanded files make PaSh print wrong output in 9 of 86 scripts (PaSh grammar) and 10 of 86 (full grammar); 11 distinct scripts.** With PaSh's own files (both
copies) every printed output matched plain bash (86 of 86). With Caruca's: 77 of 86 for the PaSh-grammar set and
76 of 86 for the full-grammar set. The wrong output is the same in all 4 runs of each (1 with the stand-in programs,
3 timed). In the first run, when Caruca had files for only 8 commands, every output was right.

| Cause | Scripts | Sets |
|---|---|---|
| `sed` with a line number (`sed 1d`, `sed 4d`, `sed 100q`): Caruca's file allows a split, so each piece gets "line N" | unixfun/26, 28, 29, 30, 31, 32, 33; oneliners/top-n | both (top-n: full grammar only) |
| `uniq` split with the pieces joined end to end: a repeated line that falls at a join survives | oneliners/spell (PaSh grammar), unixfun/17 (full grammar) | one each |
| `tr -d '\n'` split (PaSh's own file allows only a split PaSh has not implemented, which ends the parallel chain): PaSh feeds the 8 copies' output straight into 8 copies of `cut -c 1-4`, each piece is one line with no newline, and each copy prints its own first 4 characters (155 bytes instead of 5) | unixfun/23 | both |

Every case is a file allowing a split that changes the result, not a crash. PaSh did exactly what the files said:
in 639 of 639 command uses in parts PaSh ran in parallel, it split the use exactly when the file (asked with PaSh's
words) allowed a split PaSh can carry out.

**2. Parallel parts.** PaSh ran at least one part in parallel in 41 of 86 scripts with its own files, 29 with
Caruca's PaSh-grammar files, 40 with its full-grammar files. Of the 177 distinct parts: PaSh's own 41 in parallel;
PaSh-grammar set 29 (0 gained, 12 lost); full-grammar set 40 (0 gained, 1 lost).

| Set | Split more often than with PaSh's own (scripts) | Split less often (scripts) |
|---|---|---|
| Caruca, PaSh grammar (all) | `cat` 29, `sed` 7, `tr` 2, `uniq` 2 | `sort` 17, `cut` 9, `tr` 6, `sed` 5, `grep` 4 |
| Caruca, full grammar where traced | `cat` 40, `sed` 8, `tr` 2, `uniq` 2 | `sort` 17, `tr` 2, `sed` 1, `col` 1 |

- `sort` is never split by either Caruca set (67 of 67 uses "no split"), as in the first run.
- Caruca's `fmt` file makes PaSh's compiler stop in 2 parts (unixfun/34, 36; PaSh's own has no `fmt` file);
  PaSh's own files stop it in 3 parts where Caruca's do not (covid/5 `awk`, unixfun/12 and 16 `tail`).
- Commands only Caruca has files for and that sit in parts: `echo`, `ffmpeg`, `find`, `fmt`, `join`, `read`,
  `rev` (43 uses; none split).

**3. Time** (speed-up over bash, geometric mean over 86 scripts; small inputs, mostly PaSh's start-up cost):

| Set | Speed-up over bash | Time against PaSh's own (below 1 = faster) | Slower by more than 10% / faster |
|---|---|---|---|
| PaSh's own files | 0.44x | 1.00 | - |
| Caruca, PaSh grammar (all) | 0.41x | 1.09 | 30 / 5 of 86 |
| Caruca, full grammar where traced | 0.40x | 1.10 | 32 / 3 of 86 |
| PaSh's own files, second copy | 0.44x | 1.00 | 3 / 1 of 86 |

Noise: the second copy took 0.83 to 1.46 times as long as the first (median 1.00; 4 of 86 scripts beyond 10%;
the 1.46 is `file-mod/encrypt_files`, 2.9 s against 4.2 s). For comparison across sessions, use only ratios to
`pash-own` of the same session: the naive LLM's files were 1.15 (first run), Caruca's 8-command sets 1.05 and 1.06
(first run).

**Power and sleep.** The Mac was on mains power for the whole batch (`power_watch.tsv`, once a minute, no
battery minutes) and `pmset -g log` has no sleep or wake in the window, so no timed run was redone. VM load at
the end of a script's runs was at most 5.7 (`run_windows.jsonl`).

Brief: `../orchestration/brief_caruca_expanded_rerun.md`. Runner: `../run_koala_caruca_all.py`, a copy of the
first run's `../run_koala.py` with two new sets added. Records go to `~/t024/out_caruca_all` in the VM, so the
first run's records are left alone. Every change in the copy is marked `caruca-all`.

## What runs

The same 86 scripts, small inputs and passes as `../full_run/`: answers (each set's files called directly with
PaSh's words), one pass with the stand-in programs, and three timed repeats with bash first in every repeat.

| Set | Files loaded |
|---|---|
| `bash` | none (reference) |
| `pash-own` | PaSh's own files |
| `caruca-pash-all` | Caruca's small-grammar files for 53 commands (every command converted except `gzip`, whose conversion failed); PaSh's own elsewhere |
| `caruca-main-all` ("Caruca, full grammar where traced") | Caruca's full-grammar files for 22 commands (`awk cat col cut echo fmt grep head iconv mkfifo mktemp paste rev rm sed seq sort split tail tr uniq wc`), its small-grammar files for the other 31; PaSh's own elsewhere |
| `pash-own-copy` | a second, byte-identical copy of PaSh's own files (timed only; the noise check) |

Files are copied byte for byte from `~/dev/stevens/caruca/caruca/save_pash_py/<cmd>/<grammar>_grammar/trace_1/`.
Their hashes, and the grammar used for each command, are in `manifest.json` (`caruca` → `caruca-pash-all`,
`caruca-main-all`, `caruca-main-all_grammar_per_command`).

**The naive LLM's sets (`naive`, `naive-sed2`) were not rerun.** Their times are compared as ratios to `pash-own`
from their own session (`../full_run/`). Times from different sessions are compared only as those ratios.

No folder-decides controls were run on `spell`. The first run's controls stand, and the brief asks for none.

## Faults and repairs

| When | What | Effect | What was done |
|---|---|---|---|
| about 14:25 | Three new Caruca files failed to compile with a TabError: `paste` small grammar, `paste` full grammar, `awk` full grammar. Caruca's converter had written a traced example containing a newline and a tab into a comment | PaSh imports every generator in its name table at start-up, so one such file stops its compiler server and **no script runs at all** (rc 1, no output; `broken_set_test.txt`) | First recorded and left out. Then the orchestrator repaired the converter as a fault of the instrument, not of Caruca's method (`caruca/src/caruca/annotator/pash_py.py` `_comment()` now escapes newline, tab and carriage return; converter tests 14 passed). The three files were regenerated from their existing traces (no retrace); only the comment changed |
| about 15:10 | After the repair | | Sets rebuilt with the three regenerated files (new hashes in `manifest.json`; `left_out_not_loadable` is now empty). Load check: 106 of 106 files load (`load_check.jsonl`). One-line test (`cat \| tr \| sort`): rc 0, output right, 1 part sent and 1 run in parallel under `pash-own`, `caruca-pash-all` and `caruca-main-all`. The direct answers for both Caruca sets were redone for the 19 scripts that start `awk` or `paste` (`answers --add-sets`, from the saved bash start records) |

## Files

| File | What it is |
|---|---|
| `check_load.py`, `load_check.jsonl` | the load check: byte copies, JSON parses, both generator classes import, command in PaSh's name table |
| `broken_set_test.txt` | PaSh with the unrepaired `paste` file: its compiler server does not start |
| `batch.sh`, `copy_out.sh`, `power_watch.sh`, `power_watch.tsv` | the batch, the copier (every 10 scripts), the once-a-minute power log |
| `numbers.md`, `summarise.py` | every count; the counting script (copy of `../full_run/summarise.py`, set names changed) |
| `per_command_caruca-main-all.md/.json`, `per_command_caruca-pash-all.md/.json` | per command, Caruca against PaSh's own; made by `../per_command_caruca.py <set>` (copy of `../per_command.py`: set names changed, naive-specific notes replaced by counts, a wrong-output table added; PaSh's-own self-checks from the first run still pass: 41 parallel parts, 126 split uses, 4 compiler stops) |
| `results.jsonl.gz`, `regions.jsonl.gz`, `occurrences.jsonl.gz`, `commands.jsonl.gz` | the records, as in `../full_run/` |
| `answers/`, `logs/`, `pack.py` | answers per script (direct answers grouped, as in the first run) and PaSh's logs (cut to first 2,000 and last 500 lines); full files in the VM under `~/t024/out_caruca_all/` |
| `invocations.jsonl`, `manifest.json`, `sets.json`, `run_windows.jsonl`, `answers_bash_runs.jsonl`, `standin_vs_inventory.jsonl` | as in `../full_run/` |

## Runner fault before the batch

| When | What | Effect | What was done |
|---|---|---|---|
| 15:14 | The copy ran the pass with the stand-in programs three times per script (the first run ran it once; only timed runs repeat) | about 60% more run time; no wrong records | stopped during the first script (`oneliners/nfa-regex`); its rows moved to `~/t024/rerun/aborted_1514/` in the VM and the 9 "as PaSh passes them" answer rows it appended removed; the copy fixed (instrumented pass = repeat 1 only); batch restarted 15:15 from the first script |
