# Numbers for the larger-input run

Built by `summarise.py` from the records in this folder. It only counts. Timed repeats per script and source: 3 repeat(s): 172. Times are medians over the repeats. Rows replaced by redone runs: 0.

## 0. Input size per script (bash-only pilot, `scale.jsonl`)

| Group | Script | k | Input (MB) | Bash at k=10 (s) | Bash at k=30 (s) | Note |
|---|---|---:|---:|---:|---:|---|
| A | covid/1 | 1 | 3590 | - | - | not scaled: k=10 would need 35.9 GB (VM disk has 6.6 GB free); its own input is used (k=1) |
| A | covid/2 | 1 | 3590 | - | - | not scaled: k=10 would need 35.9 GB (VM disk has 6.6 GB free); its own input is used (k=1) |
| A | covid/3 | 1 | 3590 | - | - | not scaled: k=10 would need 35.9 GB (VM disk has 6.6 GB free); its own input is used (k=1) |
| A | covid/4 | 1 | 3590 | - | - | not scaled: k=10 would need 35.9 GB (VM disk has 6.6 GB free); its own input is used (k=1) |
| A | oneliners/sort | 10 | 308 | 3.891 | - |  |
| A | oneliners/sort-sort | 30 | 924 | 2.458 | 13.005 |  |
| A | oneliners/spell | 10 | 308 | 12.25 | - |  |
| A | oneliners/top-n | 10 | 308 | 10.27 | - |  |
| A | oneliners/uniq-ips | 30 | 213 | 0.958 | 2.822 |  |
| A | oneliners/wf | 10 | 308 | 10.087 | - |  |
| A | unixfun/2 | 10 | 315 | 3.212 | - |  |
| A | unixfun/4 | 30 | 944 | 2.718 | 9.716 |  |
| A | unixfun/10 | 30 | 944 | 0.582 | 1.743 |  |
| A | unixfun/11 | 30 | 944 | 0.608 | 2.026 |  |
| A | unixfun/12 | 30 | 944 | 2.627 | 8.908 |  |
| A | unixfun/14 | 10 | 315 | 7.499 | - |  |
| A | unixfun/16 | 30 | 944 | 1.749 | 5.796 |  |
| A | unixfun/17 | 30 | 944 | 1.775 | 5.346 |  |
| A | unixfun/19 | 30 | 914 | 0.216 | 0.622 |  |
| A | unixfun/21 | 10 | 305 | 10.448 | - |  |
| A | unixfun/24 | 30 | 944 | 0.707 | 2.115 |  |
| A | unixfun/25 | 30 | 944 | 0.711 | 2.199 |  |
| A | unixfun/26 | 30 | 944 | 0.691 | 2.151 |  |
| A | unixfun/28 | 30 | 944 | 0.583 | 1.855 |  |
| A | unixfun/29 | 30 | 944 | 0.574 | 1.764 |  |
| A | unixfun/30 | 30 | 944 | 0.933 | 2.742 |  |
| A | unixfun/31 | 30 | 944 | 0.956 | 2.941 |  |
| A | unixfun/32 | 30 | 942 | 0.373 | 1.167 |  |
| A | unixfun/33 | 30 | 942 | 0.366 | 1.14 |  |
| B | oneliners/nfa-regex | 10 | 103 | 86.422 | - |  |
| B | unixfun/1 | 30 | 944 | 0.672 | 2.046 |  |
| B | unixfun/3 | 30 | 944 | 0.006 | 0.002 |  |
| B | unixfun/5 | 30 | 943 | 0.365 | 1.142 |  |
| B | unixfun/6 | 30 | 944 | 0.672 | 2.171 |  |
| B | unixfun/7 | 30 | 944 | 0.823 | 2.525 |  |
| B | unixfun/8 | 30 | 944 | 0.304 | 1.02 |  |
| B | unixfun/9 | 30 | 944 | 0.388 | 0.94 |  |
| B | unixfun/13 | 30 | 944 | 0.372 | 1.039 |  |
| B | unixfun/15 | 30 | 944 | 0.551 | 1.73 |  |
| B | unixfun/18 | 30 | 914 | 0.29 | 0.859 |  |
| B | unixfun/20 | 30 | 914 | 0.006 | 0.003 |  |
| B | unixfun/23 | 30 | 944 | 0.609 | 1.931 |  |
| B | unixfun/35 | 30 | 943 | 0.139 | 0.437 |  |

# Group A (29 of 29 scripts with records)

## 1. Output, splits, compiler stops, files that raised

| Source | Output same as bash (timed, every repeat) | Same with stand-ins | Written files same as bash | Scripts with a part run in parallel | Parts run in parallel / sent (distinct) | Compiler stops (distinct parts) | Command uses whose files raised |
|---|---|---|---|---|---|---|---|
| PaSh's own files | 29 of 29 | 29 of 29 | 29 of 29 | 27 of 29 | 27 / 29 | 2 | 0 |
| Naive LLM (sed file v2) | 29 of 29 | 29 of 29 | 29 of 29 | 29 of 29 | 29 / 29 | 0 | 1 |
| Caruca (PaSh grammars, as in its paper) | 20 of 29 | 20 of 29 | 29 of 29 | 15 of 29 | 15 / 29 | 10 | 0 |
| PaSh's own files, second copy | 29 of 29 | (timed only) | 29 of 29 | - | - | - | - |

Wrong output (timed runs; repeats same as bash / repeats): oneliners/spell (Caruca (PaSh grammars, as in its paper), 0/3), oneliners/uniq-ips (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/26 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/28 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/29 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/30 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/31 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/32 (Caruca (PaSh grammars, as in its paper), 0/3), unixfun/33 (Caruca (PaSh grammars, as in its paper), 0/3).

Wrong output with the stand-in programs: oneliners/spell (Caruca (PaSh grammars, as in its paper)), oneliners/uniq-ips (Caruca (PaSh grammars, as in its paper)), unixfun/26 (Caruca (PaSh grammars, as in its paper)), unixfun/28 (Caruca (PaSh grammars, as in its paper)), unixfun/29 (Caruca (PaSh grammars, as in its paper)), unixfun/30 (Caruca (PaSh grammars, as in its paper)), unixfun/31 (Caruca (PaSh grammars, as in its paper)), unixfun/32 (Caruca (PaSh grammars, as in its paper)), unixfun/33 (Caruca (PaSh grammars, as in its paper)).

Compiler stops per script: covid/1 (Caruca (PaSh grammars, as in its paper): 1), covid/4 (Caruca (PaSh grammars, as in its paper): 1), oneliners/sort-sort (Caruca (PaSh grammars, as in its paper): 1), oneliners/top-n (Caruca (PaSh grammars, as in its paper): 1), oneliners/wf (Caruca (PaSh grammars, as in its paper): 1), unixfun/4 (Caruca (PaSh grammars, as in its paper): 1), unixfun/10 (Caruca (PaSh grammars, as in its paper): 1), unixfun/11 (Caruca (PaSh grammars, as in its paper): 1), unixfun/12 (PaSh's own files: 1), unixfun/14 (Caruca (PaSh grammars, as in its paper): 1), unixfun/16 (PaSh's own files: 1), unixfun/17 (Caruca (PaSh grammars, as in its paper): 1).

Files that raised: wc (Naive LLM (sed file v2)): AssertionError: .

## 2. Commands split, per script (runs with the stand-in programs)

| Script | PaSh's own files | Naive LLM (sed file v2) | Caruca (PaSh grammars, as in its paper) |
|---|---|---|---|
| covid/1 | cut, sed, sort | awk, cat, cut, sed, sort | - |
| covid/2 | cut, sed, sort | awk, cat, cut, sed, sort | - |
| covid/3 | cut, sed, sort | awk, cat, cut, sed, sort | - |
| covid/4 | cut, sed, sort | awk, cat, cut, sed, sort | - |
| oneliners/sort | sort | cat, sort | cat |
| oneliners/sort-sort | sort, tr | cat, sort, tr | - |
| oneliners/spell | col, sed, sort, tr | cat, sed, sort, tr | cat, col, sed, tr, uniq |
| oneliners/top-n | grep, sort, tr | cat, grep, sort, tr | - |
| oneliners/uniq-ips | sort | cat, sort | cat, uniq |
| oneliners/wf | grep, sort, tr | cat, grep, sort, tr | - |
| unixfun/2 | cut, sort | cat, cut, sort | cat, cut |
| unixfun/4 | cut, sort | cat, cut, sort | - |
| unixfun/10 | cut, grep, sort, tr | cat, cut, grep, sort, tr | - |
| unixfun/11 | cut, grep, sort, tr | cat, cut, grep, sort, tr | - |
| unixfun/12 | - | cat, cut, grep, sort, tr | - |
| unixfun/14 | cut, sort | awk, cat, cut, sort | - |
| unixfun/16 | - | cat, cut, sort | - |
| unixfun/17 | cut, sed, sort | cat, cut, sed, sort | - |
| unixfun/19 | cut, grep | awk, cat, cut, grep | cat, cut, grep |
| unixfun/21 | sort, tr | cat, sort, tr | cat |
| unixfun/24 | cut | cat, cut, tr | cat, cut, tr |
| unixfun/25 | cut | cat, cut, tr | cat, cut, tr |
| unixfun/26 | cut, grep, tr | cat, cut, grep, tr | cat, cut, grep, sed, tr |
| unixfun/28 | grep, tr | cat, grep, tr | cat, grep, sed, tr |
| unixfun/29 | tr | cat, tr | cat, sed, tr |
| unixfun/30 | grep, tr | cat, grep, tr | cat, grep, sed, tr |
| unixfun/31 | grep, tr | cat, grep, tr | cat, grep, sed, tr |
| unixfun/32 | cut, grep | cat, cut, grep | cat, cut, grep, sed |
| unixfun/33 | cut, grep | cat, cut, grep | cat, cut, grep, sed |

Naive LLM (sed file v2) against PaSh's own, per command (scripts gained / lost): `awk` 6/0, `cat` 29/0, `col` 0/1, `cut` 2/0, `grep` 1/0, `sort` 2/0, `tr` 3/0.

Caruca (PaSh grammars, as in its paper) against PaSh's own, per command (scripts gained / lost): `cat` 15/0, `cut` 0/9, `grep` 0/4, `sed` 7/5, `sort` 0/17, `tr` 2/6, `uniq` 2/0.

Naive LLM against Caruca, per command (scripts split by the naive LLM only / by Caruca only): `awk` 6/0, `cat` 14/0, `col` 0/1, `cut` 11/0, `grep` 5/0, `sed` 5/7, `sort` 19/0, `tr` 7/0, `uniq` 0/2.

## 3. Time

Speed-up = bash time / source time (above 1 = faster than bash). 'Against X' = source time / X's time (below 1 = faster than X). Geometric means over the group's scripts. 'Start-up removed': each PaSh time minus 0.11 s and 6 ms per part compiled; the cost of the split copies is kept.

| Source | Scripts | Speed-up over bash | Against PaSh's own | Against Caruca | Faster / slower than PaSh's own by >10% | Speed-up, start-up removed | Against PaSh's own, start-up removed |
|---|---|---|---|---|---|---|---|
| PaSh's own files | 29 | 1.30x | 1.00 | 0.66 | 0 / 0 | 1.36x | 1.00 |
| Naive LLM (sed file v2) | 29 | 0.97x | 1.33 | 0.88 | 3 / 25 | 1.01x | 1.35 |
| Caruca (PaSh grammars, as in its paper) | 29 | 0.85x | 1.52 | 1.00 | 2 / 21 | 0.88x | 1.54 |
| PaSh's own files, second copy | 29 | 1.26x | 1.03 | 0.68 | 1 / 4 | 1.32x | 1.03 |

Noise: the second copy of PaSh's own files took 0.89 to 1.18 times as long as the first (median 1.03; 5 of 29 scripts beyond 10%).


### Per script (median seconds; ratios: naive LLM / PaSh's own, naive LLM / Caruca)

| Script | k | bash | PaSh's own files | Naive LLM (sed file v2) | Caruca (PaSh grammars, as in its paper) | PaSh's own files, second copy | Naive / PaSh's own | Naive / Caruca | Same, start-up removed: naive / PaSh's own | naive / Caruca |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| covid/1 | 1 | 10.36 | 7.24 | 10.56 | 10.53 | 6.66 | 1.46 | 1.00 | 1.47 | 1.00 |
| covid/2 | 1 | 10.59 | 7.54 | 11.09 | 10.87 | 7.91 | 1.47 | 1.02 | 1.48 | 1.02 |
| covid/3 | 1 | 15.27 | 8.14 | 10.12 | 15.79 | 8.01 | 1.24 | 0.64 | 1.25 | 0.64 |
| covid/4 | 1 | 13.22 | 7.25 | 10.10 | 12.74 | 7.02 | 1.39 | 0.79 | 1.40 | 0.79 |
| oneliners/sort | 10 | 1.28 | 0.86 | 1.20 | 1.47 | 0.89 | 1.39 | 0.81 | 1.45 | 0.80 |
| oneliners/sort-sort | 30 | 8.89 | 5.67 | 5.86 | 7.69 | 6.54 | 1.03 | 0.76 | 1.03 | 0.76 |
| oneliners/spell | 10 | 11.20 | 4.26 | 6.98 | 10.19 ✗ | 4.21 | 1.64 | 0.68 | 1.65 | 0.68 |
| oneliners/top-n | 10 | 9.58 | 2.98 | 3.66 | 9.65 | 3.05 | 1.23 | 0.38 | 1.24 | 0.37 |
| oneliners/uniq-ips | 30 | 2.65 | 1.06 | 1.19 | 2.83 ✗ | 1.07 | 1.12 | 0.42 | 1.14 | 0.40 |
| oneliners/wf | 10 | 9.54 | 2.98 | 3.61 | 9.60 | 3.01 | 1.21 | 0.38 | 1.22 | 0.37 |
| unixfun/2 | 10 | 3.12 | 1.34 | 1.53 | 2.80 | 1.46 | 1.14 | 0.55 | 1.15 | 0.53 |
| unixfun/4 | 30 | 9.83 | 3.95 | 4.68 | 9.63 | 4.08 | 1.19 | 0.49 | 1.19 | 0.48 |
| unixfun/10 | 30 | 1.73 | 2.68 | 4.67 | 1.96 | 2.78 | 1.74 | 2.38 | 1.78 | 2.46 |
| unixfun/11 | 30 | 1.87 | 2.42 | 4.53 | 2.01 | 2.75 | 1.87 | 2.26 | 1.91 | 2.33 |
| unixfun/12 | 30 | 8.81 | 8.84 | 6.24 | 8.79 | 8.95 | 0.71 | 0.71 | 0.70 | 0.71 |
| unixfun/14 | 10 | 7.24 | 4.34 | 2.84 | 7.60 | 4.38 | 0.65 | 0.37 | 0.64 | 0.36 |
| unixfun/16 | 30 | 5.58 | 5.28 | 3.14 | 5.46 | 5.32 | 0.59 | 0.57 | 0.59 | 0.57 |
| unixfun/17 | 30 | 5.49 | 2.53 | 3.05 | 5.47 | 2.94 | 1.20 | 0.56 | 1.21 | 0.55 |
| unixfun/19 | 30 | 0.64 | 1.22 | 1.79 | 1.66 | 1.08 | 1.47 | 1.08 | 1.52 | 1.09 |
| unixfun/21 | 10 | 10.29 | 3.79 | 4.38 | 10.57 | 3.92 | 1.15 | 0.41 | 1.16 | 0.41 |
| unixfun/24 | 30 | 2.14 | 1.29 | 2.33 | 1.71 | 1.36 | 1.81 | 1.36 | 1.89 | 1.38 |
| unixfun/25 | 30 | 2.17 | 1.35 | 2.66 | 1.84 | 1.33 | 1.97 | 1.45 | 2.06 | 1.48 |
| unixfun/26 | 30 | 2.08 | 3.01 | 6.06 | 2.73 ✗ | 3.06 | 2.01 | 2.22 | 2.05 | 2.27 |
| unixfun/28 | 30 | 1.84 | 3.09 | 7.05 | 3.35 ✗ | 3.20 | 2.28 | 2.10 | 2.33 | 2.14 |
| unixfun/29 | 30 | 1.70 | 2.28 | 3.29 | 2.74 ✗ | 2.37 | 1.44 | 1.20 | 1.46 | 1.21 |
| unixfun/30 | 30 | 2.68 | 4.44 | 7.70 | 4.63 ✗ | 4.35 | 1.74 | 1.66 | 1.76 | 1.68 |
| unixfun/31 | 30 | 3.03 | 4.26 | 7.94 | 4.77 ✗ | 4.38 | 1.86 | 1.66 | 1.89 | 1.68 |
| unixfun/32 | 30 | 1.08 | 1.89 | 2.22 | 2.02 ✗ | 1.95 | 1.17 | 1.10 | 1.19 | 1.11 |
| unixfun/33 | 30 | 1.15 | 2.12 | 2.83 | 2.99 ✗ | 2.50 | 1.33 | 0.95 | 1.35 | 0.95 |

✗ = output differs from bash in at least one timed repeat.


# Group B (14 of 14 scripts with records)

## 1. Output, splits, compiler stops, files that raised

| Source | Output same as bash (timed, every repeat) | Same with stand-ins | Written files same as bash | Scripts with a part run in parallel | Parts run in parallel / sent (distinct) | Compiler stops (distinct parts) | Command uses whose files raised |
|---|---|---|---|---|---|---|---|
| PaSh's own files | 14 of 14 | 14 of 14 | 14 of 14 | 14 of 14 | 14 / 14 | 0 | 0 |
| Naive LLM (sed file v2) | 14 of 14 | 14 of 14 | 14 of 14 | 14 of 14 | 14 / 14 | 0 | 5 |
| Caruca (PaSh grammars, as in its paper) | 13 of 14 | 13 of 14 | 14 of 14 | 14 of 14 | 14 / 14 | 0 | 0 |
| PaSh's own files, second copy | 14 of 14 | (timed only) | 14 of 14 | - | - | - | - |

Wrong output (timed runs; repeats same as bash / repeats): unixfun/23 (Caruca (PaSh grammars, as in its paper), 0/3).

Wrong output with the stand-in programs: unixfun/23 (Caruca (PaSh grammars, as in its paper)).

Compiler stops per script: none.

Files that raised: wc (Naive LLM (sed file v2)): AssertionError: .

## 2. Commands split, per script (runs with the stand-in programs)

| Script | PaSh's own files | Naive LLM (sed file v2) | Caruca (PaSh grammars, as in its paper) |
|---|---|---|---|
| oneliners/nfa-regex | grep, tr | cat, grep, tr | cat, grep, tr |
| unixfun/1 | cut | cat, cut | cat, cut |
| unixfun/3 | cut | cat, cut | cat, cut |
| unixfun/5 | cut, tr | cat, cut, tr | cat, cut, tr |
| unixfun/6 | cut, tr | cat, cut, tr | cat, cut, tr |
| unixfun/7 | grep, tr | cat, grep, tr | cat, grep, tr |
| unixfun/8 | grep, tr | cat, grep, tr | cat, grep, tr |
| unixfun/9 | cut, grep, tr | cat, cut, grep, tr | cat, cut, grep, tr |
| unixfun/13 | cut, grep | cat, cut, grep | cat, cut, grep |
| unixfun/15 | cut, grep | cat, cut, grep | cat, cut, grep |
| unixfun/18 | grep, tr | cat, grep, tr | cat, grep, tr |
| unixfun/20 | cut, grep | cat, cut, grep | cat, cut, grep |
| unixfun/23 | cut, grep, tr | cat, cut, grep, tr | cat, cut, grep, tr |
| unixfun/35 | cut, grep | cat, cut, grep | cat, cut, grep |

Naive LLM (sed file v2) against PaSh's own, per command (scripts gained / lost): `cat` 14/0.

Caruca (PaSh grammars, as in its paper) against PaSh's own, per command (scripts gained / lost): `cat` 14/0.

Naive LLM against Caruca, per command (scripts split by the naive LLM only / by Caruca only): no difference.

## 3. Time

Speed-up = bash time / source time (above 1 = faster than bash). 'Against X' = source time / X's time (below 1 = faster than X). Geometric means over the group's scripts. 'Start-up removed': each PaSh time minus 0.11 s and 6 ms per part compiled; the cost of the split copies is kept.

| Source | Scripts | Speed-up over bash | Against PaSh's own | Against Caruca | Faster / slower than PaSh's own by >10% | Speed-up, start-up removed | Against PaSh's own, start-up removed |
|---|---|---|---|---|---|---|---|
| PaSh's own files | 14 | 0.47x | 1.00 | 0.82 | 0 / 0 | 0.63x | 1.00 |
| Naive LLM (sed file v2) | 14 | 0.30x | 1.57 | 1.28 | 0 / 12 | 0.37x | 1.69 |
| Caruca (PaSh grammars, as in its paper) | 14 | 0.38x | 1.23 | 1.00 | 0 / 12 | 0.48x | 1.31 |
| PaSh's own files, second copy | 14 | 0.48x | 0.99 | 0.81 | 1 / 1 | 0.64x | 0.98 |

Noise: the second copy of PaSh's own files took 0.90 to 1.13 times as long as the first (median 1.00; 2 of 14 scripts beyond 10%).


### Per script (median seconds; ratios: naive LLM / PaSh's own, naive LLM / Caruca)

| Script | k | bash | PaSh's own files | Naive LLM (sed file v2) | Caruca (PaSh grammars, as in its paper) | PaSh's own files, second copy | Naive / PaSh's own | Naive / Caruca | Same, start-up removed: naive / PaSh's own | naive / Caruca |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oneliners/nfa-regex | 10 | 84.90 | 12.72 | 12.65 | 12.76 | 12.67 | 0.99 | 0.99 | 0.99 | 0.99 |
| unixfun/1 | 30 | 1.86 | 1.34 | 1.81 | 1.78 | 1.34 | 1.36 | 1.02 | 1.39 | 1.02 |
| unixfun/3 | 30 | 0.00 | 0.14 | 0.17 | 0.17 | 0.14 | 1.20 | 0.99 | 2.12 | 0.98 |
| unixfun/5 | 30 | 1.10 | 1.17 | 1.69 | 1.65 | 1.18 | 1.44 | 1.03 | 1.48 | 1.03 |
| unixfun/6 | 30 | 2.12 | 1.70 | 2.94 | 2.00 | 1.72 | 1.73 | 1.47 | 1.78 | 1.50 |
| unixfun/7 | 30 | 2.51 | 1.80 | 3.87 | 2.36 | 1.62 | 2.15 | 1.64 | 2.23 | 1.68 |
| unixfun/8 | 30 | 0.91 | 1.49 | 3.35 | 1.90 | 1.35 | 2.25 | 1.77 | 2.36 | 1.82 |
| unixfun/9 | 30 | 0.93 | 1.91 | 3.68 | 2.28 | 1.84 | 1.93 | 1.61 | 1.99 | 1.65 |
| unixfun/13 | 30 | 1.01 | 1.79 | 2.02 | 2.00 | 1.73 | 1.13 | 1.01 | 1.14 | 1.01 |
| unixfun/15 | 30 | 1.67 | 1.63 | 1.94 | 1.99 | 1.68 | 1.19 | 0.98 | 1.21 | 0.98 |
| unixfun/18 | 30 | 0.86 | 1.28 | 3.09 | 1.78 | 1.45 | 2.41 | 1.74 | 2.55 | 1.79 |
| unixfun/20 | 30 | 0.00 | 0.15 | 0.16 | 0.16 | 0.16 | 1.05 | 1.00 | 1.18 | 1.00 |
| unixfun/23 | 30 | 1.85 | 2.14 | 5.93 | 2.51 ✗ | 2.06 | 2.78 | 2.37 | 2.88 | 2.43 |
| unixfun/35 | 30 | 0.43 | 1.11 | 1.67 | 1.58 | 1.11 | 1.50 | 1.05 | 1.55 | 1.06 |

✗ = output differs from bash in at least one timed repeat.

