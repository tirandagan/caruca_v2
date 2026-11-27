# Larger inputs: PaSh's suite with more data to divide (2026-11-27)

**Status: done.** 43 of 43 scripts, 08:10 to 09:14 (pilot 08:04 to 08:10), no runner errors, no redos. Every
number here is copied from `numbers.md` (made by `summarise.py`) or `overhead_adjusted.md`; both only count.
Plan: `../orchestration/plan_large_inputs.md`. Brief: `../orchestration/brief_large_inputs.md`.

## What was found

| | PaSh's own files | Naive LLM (sed file v2) | Caruca (PaSh grammars, as in its paper) |
|---|---|---|---|
| Output same as bash, group A (29) | 29 | 29 | 20 |
| Output same as bash, group B (14) | 14 | 14 | 13 |
| Compiler stops (distinct parts), A / B | 2 / 0 | 0 / 0 | 10 / 0 |
| Command uses whose files raised, A / B | 0 / 0 | 1 / 5 (`wc`) | 0 / 0 |
| Speed-up over bash, A / B | 1.30x / 0.47x | 0.97x / 0.30x | 0.85x / 0.38x |
| Time against PaSh's own, A / B (below 1 = faster) | 1.00 / 1.00 | 1.33 / 1.57 | 1.52 / 1.23 |
| Time against Caruca, A / B | 0.66 / 0.82 | 0.88 / 1.28 | 1.00 / 1.00 |

Geometric means over each group's scripts; times are medians of three timed runs. Noise (second copy of PaSh's
own files): median 1.03 in A (5 of 29 scripts beyond 10%), 1.00 in B (2 of 14). Removing PaSh's start-up
changes the ratios by at most 0.12 (naive against PaSh's own: 1.35 in A, 1.69 in B; `numbers.md` section 3).

1. **More data did not turn the naive LLM's extra splits into speed.** Against PaSh's own files the naive LLM's
   files were faster by more than 10% in 3 of 29 group-A scripts (Unix50 12, 14, 16: 0.71, 0.65, 0.59) and slower
   by more than 10% in 25. PaSh's own files were the fastest source in both groups.
2. **The naive LLM's files were never wrong (43 of 43); Caruca's were wrong in 10.** Caruca's wrong scripts:
   `sed` with a line number (Unix50 26, 28-33), `uniq` and `col` (spell), `uniq` (uniq-ips), `tr -d` + `cut`
   (Unix50 23). **uniq-ips is new**: its output was right in the small run and wrong at 30 times the input in
   all 4 runs. A split `uniq` is wrong only when a repeated line falls on a join between pieces, so whether it
   shows depends on the data. The plan's ground rule (data size cannot change correctness) does not hold for
   this case.
3. **Against Caruca the naive LLM's files were faster in group A (0.88) and slower in group B (1.28).** In A,
   Caruca's small grammars cannot split `sort` (0 of 19 scripts where the naive LLM split it) and its `sort`
   file stops PaSh's compiler in 10 parts. The naive LLM's files were 0.37 to 0.81 times Caruca's time in 14
   scripts. In B both split exactly the same commands in every script, yet the naive LLM's files were slower
   in 6 scripts (Unix50 6-9, 18, 23: 1.47 to 2.37) and equal (0.98-1.06) in the other 8.
4. **What the slow scripts share (observed, not tested):** the naive LLM's `tr` file offers PaSh only the
   consecutive-chunks split, where PaSh's own and Caruca's offer round robin too (`occurrences.jsonl`,
   recipes). Every script where the naive LLM's files were more than 1.4 times Caruca's time has such a `tr`
   use (A: Unix50 10, 11, 25, 26, 28, 30, 31; B: 6-9, 18, 23). None of the 8 group-B scripts where they were equal does. Whether
   this recipe is the cause would need a run with only the `tr` file swapped.
5. **Splitting `cat` costs about the same as before:** in group B, where the naive LLM's files differ from
   PaSh's own only by a `cat` split, they took 1.57 times as long; Caruca's (which split `cat` too, in all 14)
   1.23. The small run gave 1.21 (naive) and 1.14 (Caruca) for the same comparison.

## The plan's expectations against the result

| Expectation (plan, written before running) | Result | Held? |
|---|---|---|
| Faster than PaSh's own where the naive LLM adds `awk`, `tr`, `cut`, `sort` splits: Unix50 12, 14, 16, 19, 24, 25; COVID 1-4 | 12: 0.71, 14: 0.65, 16: 0.59; 19: 1.47, 24: 1.81, 25: 1.97; COVID 1-4: 1.46, 1.47, 1.24, 1.39 | 3 of 10 |
| About equal to PaSh's own elsewhere in group A | of the other 19 scripts: 18 slower by more than 10%, 1 within 10% (sort-sort, 1.03), 0 faster | no |
| Slower than PaSh's own in group B (the `cat` cost) | 1.57; 12 of 14 slower by more than 10%, 0 faster | yes |
| Faster than Caruca where Caruca cannot split `sort`, `cut`, `tr` | faster in 14 scripts (0.37-0.81); equal in COVID 1, 2 (1.00, 1.02); slower in Unix50 10, 11 (2.38, 2.26), where Caruca's `sort` file stops the compiler and the part runs as plain bash | mostly |
| Caruca still wrong on its 9 scripts | wrong on the same 9 plus uniq-ips (10) | yes, and one more |
| Unix50 26, 28-33: Caruca may be faster, but wrong | Caruca faster in 6 of 7 (naive / Caruca 1.10-2.22; 33: 0.95), wrong in 7 of 7 | yes |
| Splits, stops and failing files the same as the small run (naive 4 stops, `wc`/`join` fail; Caruca 11 stops) | these 43 scripts: naive 0 stops, `wc` raises (no `join` in them); Caruca 10 stops; PaSh's own 2 (Unix50 12, 16) | same as the small run on these scripts (its other stops are in scripts outside A and B) |

## What ran

| | |
|---|---|
| Scripts | group A, 29 (COVID 1-4; Classics sort, sort-sort, spell, top-n, uniq-ips, wf; Unix50 2, 4, 10, 11, 12, 14, 16, 17, 19, 21, 24, 25, 26, 28-33); group B, 14 (Classics nfa-regex; Unix50 1, 3, 5-9, 13, 15, 18, 20, 23, 35); lists in `ids_group_a.txt`, `ids_group_b.txt` |
| Sets | `bash`; `pash-own`; `naive-sed2` (the naive LLM's files for 82 commands with the second `sed` file); `caruca-pash-all` (Caruca's small-grammar files, 53 commands); `pash-own-copy` (noise, timed only). Sets reused from the earlier runs, package hashes unchanged (pash-own 77625cbdbe5c0ed7, naive-sed2 70ba170c6300dc88, caruca-pash-all 279fcffc47f6b5e9) |
| `caruca-main-all` | left out: the pilot projected 127 minutes with it, over the plan's 2 hours (110 without) |
| Passes | per script and set: one run with the stand-in programs, then three timed runs, bash first in every repeat |
| Inputs | each script's own small input concatenated k times into `~/t024/big/` in the VM, the argument and `BENCHMARK_INPUT_FILE` pointed at it, deleted after the script; never more than one on disk |
| Koala's answer | not compared: Koala has none for a scaled input, and none is recorded for COVID |
| Machine | Lima VM `pash` (8 CPUs, 7 GB), PaSh width 8, as in the earlier runs |

### k per script (bash-only pilot; rule: the smaller of 10 and 30 at which bash reaches 3 s, capped at 30)

| k | Scripts (bash seconds at that k in the pilot) |
|---|---|
| 1 | COVID 1-4 (10.8, 10.5, 15.9, 13.0); **departure from the plan**: their own input is already 3.6 GB with no header line, so k=10 would need 36 GB and the VM has 6.6 GB free |
| 10 | sort 3.9, spell 12.3, top-n 10.3, wf 10.1, Unix50 2 3.2, 14 7.5, 21 10.4, nfa-regex 86.4 |
| 30 | sort-sort 13.0, uniq-ips 2.8, Unix50 4 9.7, 12 8.9, 16 5.8, 17 5.3, 1 2.0, 6 2.2, 7 2.5, 10 1.7, 11 2.0, 15 1.7, 23 1.9, 24 2.1, 25 2.2, 26 2.2, 28 1.9, 29 1.8, 30 2.7, 31 2.9, 5 1.1, 8 1.0, 9 0.9, 13 1.0, 18 0.9, 19 0.6, 32 1.2, 33 1.1, 35 0.4, 3 0.00, 20 0.00 |

Most Unix50 scripts stay under 3 s even at k=30 (the cap). Unix50 3 and 20 stop reading early, so their time
does not grow with the input.

## Faults, power, redos

- No runner errors (`batch_A.log.gz`, `batch_B.log.gz`); no `batch_errors.jsonl`.
- Power: mains for the whole pilot and batch (`power_watch.tsv`, once a minute, 08:07 to 09:15, no battery
  minutes). `pmset -g log` has no sleep or wake from 08:00 to 09:15. No timed run was redone.
- Disk: 6.6 GB free before and after; `~/t024/big` removed at the end.

## Files

| File | What it is |
|---|---|
| `../run_koala_large.py` | the runner: a copy of `../run_koala_caruca_all.py`, changes marked `large` (scaling, `pilot`, `prep`, sets, output folder `~/t024/out_large`) |
| `scale.jsonl`, `pilot.log` | the pilot: k, input bytes and bash seconds per k for each script |
| `batch.sh`, `copy_out.sh`, `power_watch.sh`, `power_watch.tsv` | the batch per group, the copier, the power log |
| `results.jsonl.gz`, `regions.jsonl.gz`, `occurrences.jsonl.gz`, `run_windows.jsonl`, `batch_progress.txt` | the records, as in the earlier runs, plus `k` and `input_bytes` on every row; each row keeps `bash_out_sha256`, so a wrong output can be made again |
| `logs/` | PaSh's logs of repeat 1 per script, set and pass |
| `summarise.py`, `numbers.md` | the counts (copy of `../full_run_caruca_all/summarise.py`, adapted: one session, groups A and B, time against PaSh's own and Caruca, start-up removed) |
| `overhead_adjusted.py`, `overhead_adjusted.md` | the start-up model of `../overhead_adjusted.py` (fitted on the first run) applied to these records |

Answers of each set's files for each command line were copied from the earlier runs (`prep`: direct answers
from `~/t024/out` and `~/t024/out_caruca_all`); this run added its own answers as PaSh passes the words
(VM: `~/t024/out_large/answers/`). No independent check of the wrong outputs was done here (the plan assigns
it to a separate checker).
