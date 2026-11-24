# Numbers for the run (46 scripts)

Built by `summarise.py` from the records in this folder. It only counts.

Timed repeats per script and source: 1 repeat(s): 231. Times are medians over the repeats. The naive LLM's second sed file was run only on scripts that use sed.

## 1. Output and what PaSh did, per source (timed runs)

| Source | Scripts | Output same as bash | Same as Koala's stored answer (of scripts with one) | PaSh ran at least one part in parallel | Fell back to plain bash | Other state |
|---|---|---|---|---|---|---|
| PaSh's own files | 46 | 46 of 46 | 46 of 46 | 37 of 46 | 8 of 46 | compiled, nothing split: 1 |
| Naive LLM's files | 46 | 46 of 46 | 46 of 46 | 39 of 46 | 6 of 46 | compiled, nothing split: 1 |
| Naive LLM, sed file v2 | 1 | 1 of 1 | 1 of 1 | 1 of 1 | 0 of 1 | - |
| Caruca's files, PaSh grammar | 46 | 46 of 46 | 46 of 46 | 29 of 46 | 16 of 46 | compiled, nothing split: 1 |
| Caruca's files, main grammar | 46 | 46 of 46 | 46 of 46 | 37 of 46 | 8 of 46 | compiled, nothing split: 1 |
| PaSh's own files, second copy | 46 | 46 of 46 | 46 of 46 | 37 of 46 | 8 of 46 | compiled, nothing split: 1 |

Plain bash itself matched Koala's stored answer in 46 of 46 scripts that have one.

Timed runs whose output differs from bash: none.

Runs with the stand-in programs whose output differs from bash: none.

## 2. Parts of the scripts (what PaSh compiles), per source (runs with the stand-in programs)

A part is one piece of a script that PaSh asks its compiler to handle. Every part not run in parallel counts against the source, whatever the cause (Tiran, 2026-11-24); the causes are listed.

| Source | Parts sent (each time) | Run in parallel | Distinct parts | Distinct run in parallel | Causes, parts not run in parallel (each time) |
|---|---|---|---|---|---|
| PaSh's own files | 51 | 37 of 51 | 51 | 37 of 51 | missing annotation 4, other 5, pash crash 3, unsupported construct 2 |
| Naive LLM's files | 51 | 39 of 51 | 51 | 39 of 51 | missing annotation 2, other 4, pash crash 3, refused by annotation 1, unsupported construct 2 |
| Naive LLM, sed file v2 | 2 | 2 of 2 | 2 | 2 of 2 | - |
| Caruca's files, PaSh grammar | 51 | 29 of 51 | 51 | 29 of 51 | missing annotation 4, other 5, pash crash 11, unsupported construct 2 |
| Caruca's files, main grammar | 51 | 37 of 51 | 51 | 37 of 51 | missing annotation 4, other 5, pash crash 3, unsupported construct 2 |

## 3. Distinct parts compared with PaSh's own files

Paired by script and part text. 'Gained': run in parallel with this source but not with PaSh's own; 'lost': the reverse.

| Source | Distinct parts with both | Both in parallel | Gained | Lost | Neither |
|---|---|---|---|---|---|
| Naive LLM's files | 51 | 37 | 2 | 0 | 12 |
| Naive LLM, sed file v2 | 1 | 1 | 0 | 0 | 0 |
| Caruca's files, PaSh grammar | 51 | 29 | 0 | 8 | 14 |
| Caruca's files, main grammar | 51 | 37 | 0 | 0 | 14 |

## 4. Command uses, by who supplied the files (runs with the stand-in programs)

A command use is one place a script calls a command, in one distinct part. 'Ours' means the source's own files (naive LLM's or Caruca's); 'PaSh's own' means the source has none for that command, so PaSh's own files were used.

| Source | Whose files | Uses in parts PaSh ran in parallel | Split | Not split: file says no | Not split: only a split PaSh has not implemented | Not split: no answer / no files / raised | Not split: allowed but not split | Uses in parts not run in parallel | Uses outside every part |
|---|---|---|---|---|---|---|---|---|---|
| PaSh's own files | pash-own | 196 | 108 | 19 | 18 | 51 | 0 | 60 | 5 |
| PaSh's own files | none | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 |
| Naive LLM's files | ours | 214 | 166 | 30 | 12 | 6 | 0 | 43 | 6 |
| Naive LLM's files | pash-own | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Naive LLM's files | none | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| Naive LLM, sed file v2 | ours | 8 | 6 | 1 | 1 | 0 | 0 | 0 | 0 |
| Caruca's files, PaSh grammar | ours | 82 | 71 | 11 | 0 | 0 | 0 | 70 | 1 |
| Caruca's files, PaSh grammar | pash-own | 60 | 23 | 18 | 12 | 7 | 0 | 44 | 4 |
| Caruca's files, PaSh grammar | none | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 |
| Caruca's files, main grammar | ours | 119 | 94 | 25 | 0 | 0 | 0 | 33 | 1 |
| Caruca's files, main grammar | pash-own | 77 | 32 | 19 | 18 | 8 | 0 | 27 | 4 |
| Caruca's files, main grammar | none | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 |

Files that raised an error when PaSh's words were passed to them: wc (naive): AssertionError: .

Check of the method: in 755 of 756 uses in parts PaSh ran in parallel, PaSh split the use exactly when the files (asked with PaSh's words) allowed a split PaSh can carry out.

## 5. Commands where the source's own files changed what PaSh split

Per command: in how many scripts the command was split with this source and not with PaSh's own (gained), and the reverse (lost). Counted per script.

| Source | Command | Gained (scripts) | Lost (scripts) |
|---|---|---|---|
| Naive LLM's files | awk | 2 | 0 |
| Naive LLM's files | cat | 39 | 0 |
| Naive LLM's files | col | 0 | 1 |
| Naive LLM's files | cut | 2 | 0 |
| Naive LLM's files | grep | 1 | 0 |
| Naive LLM's files | sed | 0 | 1 |
| Naive LLM's files | sort | 2 | 0 |
| Naive LLM's files | tr | 3 | 0 |
| Naive LLM, sed file v2 | cat | 2 | 0 |
| Naive LLM, sed file v2 | col | 0 | 1 |
| Naive LLM, sed file v2 | cut | 0 | 22 |
| Naive LLM, sed file v2 | grep | 0 | 20 |
| Naive LLM, sed file v2 | sed | 0 | 1 |
| Naive LLM, sed file v2 | sort | 0 | 11 |
| Naive LLM, sed file v2 | tr | 0 | 18 |
| Caruca's files, PaSh grammar | cat | 29 | 0 |
| Caruca's files, PaSh grammar | cut | 0 | 5 |
| Caruca's files, PaSh grammar | grep | 0 | 4 |
| Caruca's files, PaSh grammar | sed | 0 | 1 |
| Caruca's files, PaSh grammar | sort | 0 | 13 |
| Caruca's files, PaSh grammar | tr | 0 | 5 |
| Caruca's files, main grammar | cat | 37 | 0 |
| Caruca's files, main grammar | sort | 0 | 13 |

## 6. Time (one timed run per source and script)

Ratios are bash time divided by the source's time (above 1 = faster than bash). Summaries are geometric means over the scripts. All of a source's commands are swapped in at once, so a time difference belongs to the source as a whole, not to any one command.

| Source | Scripts | Speed-up over bash (geometric mean) | Time vs PaSh's own (geometric mean; below 1 = faster) | Faster than PaSh's own by more than 10% | Slower by more than 10% |
|---|---|---|---|---|---|
| PaSh's own files | 46 | 0.31x | 1.00 | 0 of 46 | 0 of 46 |
| Naive LLM's files | 46 | 0.25x | 1.22 | 2 of 46 | 30 of 46 |
| Naive LLM, sed file v2 | 1 | 1.48x | 1.06 | 0 of 1 | 0 of 1 |
| Caruca's files, PaSh grammar | 46 | 0.29x | 1.06 | 6 of 46 | 17 of 46 |
| Caruca's files, main grammar | 46 | 0.28x | 1.11 | 6 of 46 | 20 of 46 |
| PaSh's own files, second copy | 46 | 0.30x | 1.01 | 4 of 46 | 4 of 46 |

Noise check: the second, identical copy of PaSh's own files took between 0.64 and 1.57 times as long as the first (median 1.01; 8 of 46 scripts differ by more than 10%). A difference smaller than that spread is not evidence of anything.


### Per script (seconds)

| Script | bash | PaSh's own files | Naive LLM's files | Naive LLM, sed file v2 | Caruca's files, PaSh grammar | Caruca's files, main grammar | PaSh's own files, second copy |
|---|---|---|---|---|---|---|---|
| oneliners/bi-grams | 1.19 | 1.32 | 1.34 | - | 1.31 | 1.32 | 1.34 |
| oneliners/comm | 0.04 | 0.15 | 0.15 | - | 0.16 | 0.15 | 0.15 |
| oneliners/diff | 0.30 | 0.43 | 0.41 | - | 0.40 | 0.42 | 0.42 |
| oneliners/nfa-regex | 8.53 | 2.11 | 1.92 | - | 2.03 | 1.94 | 1.93 |
| oneliners/opt-parallel | 0.10 | 0.33 | 0.23 | - | 0.20 | 0.20 | 0.21 |
| oneliners/set-diff | 0.27 | 0.39 | 0.41 | - | 0.41 | 0.39 | 0.41 |
| oneliners/sort | 0.14 | 0.24 | 0.26 | - | 0.30 | 0.29 | 0.23 |
| oneliners/sort-sort | 0.23 | 0.37 | 0.41 | - | 0.28 | 0.32 | 0.39 |
| oneliners/spell | 1.23 | 0.75 | 1.05 | - | 1.11 | 1.11 | 0.66 |
| oneliners/top-n | 0.93 | 0.59 | 0.70 | 0.62 | 1.05 | 1.00 | 0.61 |
| oneliners/uniq-ips | 0.08 | 0.20 | 0.22 | - | 0.23 | 0.49 | 0.32 |
| oneliners/wf | 0.90 | 0.54 | 0.64 | - | 1.13 | 1.07 | 0.57 |
| unixfun/1 | 0.06 | 0.18 | 0.20 | - | 0.21 | 0.22 | 0.20 |
| unixfun/10 | 0.06 | 0.39 | 0.56 | - | 0.18 | 0.30 | 0.36 |
| unixfun/11 | 0.06 | 0.37 | 0.51 | - | 0.17 | 0.27 | 0.37 |
| unixfun/12 | 0.25 | 0.36 | 0.48 | - | 0.37 | 0.44 | 0.36 |
| unixfun/13 | 0.04 | 0.21 | 0.28 | - | 0.26 | 0.24 | 0.23 |
| unixfun/14 | 0.72 | 0.63 | 0.47 | - | 0.81 | 0.92 | 0.61 |
| unixfun/15 | 0.06 | 0.17 | 0.21 | - | 0.22 | 0.22 | 0.27 |
| unixfun/16 | 0.16 | 0.26 | 0.37 | - | 0.30 | 0.27 | 0.29 |
| unixfun/17 | 0.16 | 0.33 | 0.36 | - | 0.27 | 0.37 | 0.34 |
| unixfun/18 | 0.03 | 0.19 | 0.34 | - | 0.21 | 0.21 | 0.19 |
| unixfun/19 | 0.02 | 0.21 | 0.21 | - | 0.23 | 0.22 | 0.21 |
| unixfun/2 | 0.33 | 0.28 | 0.30 | - | 0.39 | 0.37 | 0.28 |
| unixfun/20 | 0.00 | 0.17 | 0.17 | - | 0.17 | 0.16 | 0.17 |
| unixfun/21 | 1.00 | 0.54 | 0.64 | - | 1.11 | 1.08 | 0.58 |
| unixfun/23 | 0.06 | 0.27 | 0.55 | - | 0.30 | 0.27 | 0.26 |
| unixfun/24 | 0.07 | 0.17 | 0.24 | - | 0.18 | 0.20 | 0.18 |
| unixfun/25 | 0.07 | 0.19 | 0.27 | - | 0.19 | 0.18 | 0.18 |
| unixfun/26 | 0.07 | 0.29 | 0.48 | - | 0.28 | 0.28 | 0.31 |
| unixfun/28 | 0.06 | 0.37 | 0.57 | - | 0.36 | 0.37 | 0.36 |
| unixfun/29 | 0.06 | 0.23 | 0.31 | - | 0.27 | 0.33 | 0.23 |
| unixfun/3 | 0.00 | 0.15 | 0.17 | - | 0.17 | 0.17 | 0.14 |
| unixfun/30 | 0.09 | 0.32 | 0.49 | - | 0.32 | 0.34 | 0.32 |
| unixfun/31 | 0.10 | 0.34 | 0.52 | - | 0.33 | 0.32 | 0.33 |
| unixfun/32 | 0.04 | 0.21 | 0.26 | - | 0.24 | 0.24 | 0.22 |
| unixfun/33 | 0.04 | 0.20 | 0.25 | - | 0.25 | 0.26 | 0.21 |
| unixfun/34 | 0.00 | 0.09 | 0.11 | - | 0.11 | 0.10 | 0.12 |
| unixfun/35 | 0.01 | 0.18 | 0.21 | - | 0.18 | 0.19 | 0.19 |
| unixfun/36 | 0.06 | 0.15 | 0.16 | - | 0.16 | 0.16 | 0.17 |
| unixfun/4 | 0.28 | 0.35 | 0.37 | - | 0.39 | 0.43 | 0.37 |
| unixfun/5 | 0.04 | 0.23 | 0.26 | - | 0.21 | 0.21 | 0.20 |
| unixfun/6 | 0.07 | 0.31 | 0.35 | - | 0.28 | 0.27 | 0.24 |
| unixfun/7 | 0.09 | 0.21 | 0.34 | - | 0.22 | 0.21 | 0.20 |
| unixfun/8 | 0.03 | 0.22 | 0.35 | - | 0.23 | 0.23 | 0.20 |
| unixfun/9 | 0.03 | 0.25 | 0.36 | - | 0.25 | 0.27 | 0.24 |
