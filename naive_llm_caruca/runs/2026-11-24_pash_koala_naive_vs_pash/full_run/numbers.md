# Numbers for the run (86 scripts)

Fix-ups applied when counting (records unchanged): output compared again against the same repeat's bash: rows compared again 1854, same as bash: changed 482, output files same as bash: changed 642. Timed runs left out because node was missing: 7. Rows replaced by redone runs: 7.

Built by `summarise.py` from the records in this folder. It only counts.

Timed repeats per script and source: 3 repeat(s): 482. Times are medians over the repeats. The naive LLM's second sed file was run on the 12 oneliners and unixfun scripts that use sed and on all 40 scripts of the other groups (52; in 27 of them bash starts no sed), so its time ratios cover a different set of scripts from the other sources' 86.

## 1. Output and what PaSh did, per source (timed runs)

| Source | Scripts | Output same as bash | Same as Koala's stored answer (of scripts with one) | PaSh ran at least one part in parallel | Fell back to plain bash | Other state |
|---|---|---|---|---|---|---|
| PaSh's own files | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 |
| Naive LLM's files | 86 | 86 of 86 | 46 of 46 | 43 of 86 | 42 of 86 | compiled, nothing split: 1 |
| Naive LLM, sed file v2 | 52 | 52 of 52 | 12 of 12 | 14 of 52 | 38 of 52 | - |
| Caruca's files, PaSh grammar | 86 | 86 of 86 | 46 of 46 | 29 of 86 | 56 of 86 | compiled, nothing split: 1 |
| Caruca's files, main grammar | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 |
| PaSh's own files, second copy | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 |

Plain bash itself matched Koala's stored answer in 46 of 46 scripts that have one.

Timed runs whose output differs from bash: none.

Runs with the stand-in programs whose output differs from bash: none.

## 2. Parts of the scripts (what PaSh compiles), per source (runs with the stand-in programs)

A part is one piece of a script that PaSh asks its compiler to handle. Every part not run in parallel counts against the source, whatever the cause (Tiran, 2026-11-24); the causes are listed.

| Source | Scripts | Parts sent (each time) | Run in parallel | Distinct parts | Distinct run in parallel | Causes, parts not run in parallel (each time) |
|---|---|---|---|---|---|---|
| PaSh's own files | 86 | 88900 | 41 of 88900 | 177 | 41 of 177 | missing annotation 33837, other 1009, pash crash 4, unsupported construct 54009 |
| Naive LLM's files | 86 | 88900 | 43 of 88900 | 177 | 43 of 177 | missing annotation 30804, other 1039, pash crash 4, refused by annotation 1, unsupported construct 57009 |
| Naive LLM, sed file v2 | 52 | 88862 | 14 of 88862 | 139 | 14 of 139 | missing annotation 30803, other 1035, pash crash 3, unsupported construct 57007 |
| Caruca's files, PaSh grammar | 86 | 88900 | 29 of 88900 | 177 | 29 of 177 | missing annotation 33837, other 1011, pash crash 14, unsupported construct 54009 |
| Caruca's files, main grammar | 86 | 88900 | 41 of 88900 | 177 | 41 of 177 | missing annotation 33837, other 1009, pash crash 4, unsupported construct 54009 |

## 3. Distinct parts compared with PaSh's own files

Paired by script and part text. 'Gained': run in parallel with this source but not with PaSh's own; 'lost': the reverse.

| Source | Distinct parts with both | Both in parallel | Gained | Lost | Neither |
|---|---|---|---|---|---|
| Naive LLM's files | 177 | 41 | 2 | 0 | 134 |
| Naive LLM, sed file v2 | 139 | 14 | 0 | 0 | 125 |
| Caruca's files, PaSh grammar | 177 | 29 | 0 | 12 | 136 |
| Caruca's files, main grammar | 177 | 41 | 0 | 0 | 136 |

## 4. Command uses, by who supplied the files (runs with the stand-in programs)

A command use is one place a script calls a command, in one distinct part. 'Ours' means the source's own files (naive LLM's or Caruca's); 'PaSh's own' means the source has none for that command, so PaSh's own files were used.

| Source | Whose files | Uses in parts PaSh ran in parallel | Split | Not split: file says no | Not split: only a split PaSh has not implemented | Not split: no answer / no files / raised | Not split: allowed but not split | Uses in parts not run in parallel | Uses outside every part |
|---|---|---|---|---|---|---|---|---|---|
| PaSh's own files | pash-own | 230 | 126 | 23 | 22 | 59 | 0 | 255 | 121 |
| PaSh's own files | none | 0 | 0 | 0 | 0 | 0 | 0 | 124 | 84 |
| Naive LLM's files | ours | 248 | 192 | 34 | 16 | 6 | 0 | 275 | 160 |
| Naive LLM's files | pash-own | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Naive LLM's files | none | 0 | 0 | 0 | 0 | 0 | 0 | 85 | 45 |
| Naive LLM, sed file v2 | ours | 107 | 77 | 22 | 7 | 1 | 0 | 247 | 160 |
| Naive LLM, sed file v2 | pash-own | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Naive LLM, sed file v2 | none | 0 | 0 | 0 | 0 | 0 | 0 | 83 | 44 |
| Caruca's files, PaSh grammar | ours | 82 | 71 | 11 | 0 | 0 | 0 | 222 | 36 |
| Caruca's files, PaSh grammar | pash-own | 60 | 23 | 18 | 12 | 7 | 0 | 121 | 85 |
| Caruca's files, PaSh grammar | none | 0 | 0 | 0 | 0 | 0 | 0 | 124 | 84 |
| Caruca's files, main grammar | ours | 141 | 106 | 35 | 0 | 0 | 0 | 163 | 36 |
| Caruca's files, main grammar | pash-own | 89 | 36 | 19 | 22 | 12 | 0 | 92 | 85 |
| Caruca's files, main grammar | none | 0 | 0 | 0 | 0 | 0 | 0 | 124 | 84 |

Files that raised an error when PaSh's words were passed to them: join (naive): ; join (naive): Exception: join requires exactly two operands (FILE1 FILE2); join (naive-sed2): ; join (naive-sed2): Exception: join requires exactly two operands (FILE1 FILE2); wc (naive): AssertionError: ; wc (naive-sed2): AssertionError: .

Check of the method: in 956 of 957 uses in parts PaSh ran in parallel, PaSh split the use exactly when the files (asked with PaSh's words) allowed a split PaSh can carry out.

## 5. Commands where the source's own files changed what PaSh split

Per command: in how many scripts the command was split with this source and not with PaSh's own (gained), and the reverse (lost). Counted per script.

| Source | Command | Gained (scripts) | Lost (scripts) |
|---|---|---|---|
| Naive LLM's files | awk | 6 | 0 |
| Naive LLM's files | cat | 43 | 0 |
| Naive LLM's files | col | 0 | 1 |
| Naive LLM's files | cut | 2 | 0 |
| Naive LLM's files | grep | 1 | 0 |
| Naive LLM's files | sed | 0 | 5 |
| Naive LLM's files | sort | 2 | 0 |
| Naive LLM's files | tr | 3 | 0 |
| Naive LLM, sed file v2 | awk | 4 | 0 |
| Naive LLM, sed file v2 | cat | 14 | 0 |
| Naive LLM, sed file v2 | col | 0 | 1 |
| Caruca's files, PaSh grammar | cat | 29 | 0 |
| Caruca's files, PaSh grammar | cut | 0 | 9 |
| Caruca's files, PaSh grammar | grep | 0 | 4 |
| Caruca's files, PaSh grammar | sed | 0 | 5 |
| Caruca's files, PaSh grammar | sort | 0 | 17 |
| Caruca's files, PaSh grammar | tr | 0 | 5 |
| Caruca's files, main grammar | cat | 41 | 0 |
| Caruca's files, main grammar | sort | 0 | 17 |

## 6. Time (median of three timed runs per source and script)

Ratios are bash time divided by the source's time (above 1 = faster than bash). Summaries are geometric means over the scripts. All of a source's commands are swapped in at once, so a time difference belongs to the source as a whole, not to any one command.

| Source | Scripts | Speed-up over bash (geometric mean) | Time vs PaSh's own (geometric mean; below 1 = faster) | Faster than PaSh's own by more than 10% | Slower by more than 10% |
|---|---|---|---|---|---|
| PaSh's own files | 86 | 0.42x | 1.00 | 0 of 86 | 0 of 86 |
| Naive LLM's files | 86 | 0.37x | 1.15 | 4 of 86 | 34 of 86 |
| Naive LLM, sed file v2 | 52 | 0.51x | 1.07 | 2 of 52 | 10 of 52 |
| Caruca's files, PaSh grammar | 86 | 0.41x | 1.05 | 8 of 86 | 17 of 86 |
| Caruca's files, main grammar | 86 | 0.40x | 1.06 | 6 of 86 | 23 of 86 |
| PaSh's own files, second copy | 86 | 0.43x | 0.99 | 3 of 86 | 1 of 86 |

Noise check: the second, identical copy of PaSh's own files took between 0.83 and 1.13 times as long as the first (median 0.99; 4 of 86 scripts differ by more than 10%). A difference smaller than that spread is not evidence of anything.


### Per script (seconds)

| Script | bash | PaSh's own files | Naive LLM's files | Naive LLM, sed file v2 | Caruca's files, PaSh grammar | Caruca's files, main grammar | PaSh's own files, second copy |
|---|---|---|---|---|---|---|---|
| analytics/nginx | 1.30 | 1.48 | 1.46 | 1.45 | 1.46 | 1.48 | 1.49 |
| analytics/pcaps | 97.54 | 106.15 | 101.38 | 97.32 | 100.33 | 100.46 | 101.44 |
| analytics/ray-tracing | 0.00 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.13 |
| bio/bio | 0.13 | 0.28 | 0.26 | 0.25 | 0.26 | 0.26 | 0.26 |
| covid/1 | 10.01 | 6.73 | 13.19 | 10.61 | 10.37 | 7.76 | 6.68 |
| covid/2 | 10.12 | 7.14 | 14.45 | 11.05 | 10.62 | 8.21 | 6.45 |
| covid/3 | 14.84 | 7.50 | 17.90 | 10.73 | 14.83 | 8.38 | 7.26 |
| covid/4 | 12.15 | 6.67 | 16.75 | 9.27 | 12.49 | 7.36 | 6.65 |
| covid/5 | 11.15 | 11.13 | 11.38 | 11.65 | 10.97 | 11.31 | 11.36 |
| file-mod/compress_files | 18.75 | 19.49 | 19.45 | 19.46 | 19.22 | 19.20 | 19.25 |
| file-mod/encrypt_files | 2.00 | 2.73 | 2.69 | 2.92 | 2.65 | 2.94 | 3.10 |
| file-mod/img_convert | 32.36 | 35.81 | 35.51 | 35.58 | 35.57 | 35.96 | 35.42 |
| file-mod/thumbnail_generation | 11.01 | 11.22 | 10.99 | 10.91 | 11.04 | 10.91 | 10.76 |
| file-mod/to_mp3 | 8.62 | 9.34 | 9.31 | 9.21 | 9.02 | 8.95 | 9.02 |
| nlp/bigrams | 49.48 | 69.41 | 74.10 | 69.88 | 71.97 | 74.63 | 71.02 |
| nlp/bigrams_appear_twice | 60.02 | 79.45 | 78.62 | 78.84 | 78.75 | 78.43 | 78.35 |
| nlp/compare_exodus_genesis | 89.11 | 108.74 | 109.87 | 110.61 | 109.14 | 109.21 | 109.36 |
| nlp/count_consonant_seq | 41.59 | 65.05 | 60.30 | 61.03 | 62.05 | 63.84 | 62.59 |
| nlp/count_morphs | 8.51 | 25.07 | 26.93 | 25.27 | 25.78 | 26.15 | 26.52 |
| nlp/count_trigrams | 55.62 | 74.53 | 78.88 | 80.61 | 79.49 | 74.53 | 74.81 |
| nlp/count_vowel_seq | 7.90 | 26.52 | 25.65 | 26.79 | 27.55 | 26.46 | 25.36 |
| nlp/count_words | 30.30 | 47.92 | 47.52 | 47.47 | 47.18 | 48.44 | 47.73 |
| nlp/find_anagrams | 42.12 | 63.43 | 66.47 | 59.77 | 63.86 | 65.02 | 65.88 |
| nlp/letter_words | 38.64 | 76.58 | 74.44 | 72.71 | 76.92 | 78.50 | 77.28 |
| nlp/merge_upper | 30.48 | 48.16 | 48.87 | 47.93 | 47.72 | 47.90 | 47.67 |
| nlp/sort | 33.46 | 51.50 | 51.14 | 50.91 | 51.01 | 53.33 | 52.03 |
| nlp/sort_words_by_folding | 33.22 | 51.30 | 50.94 | 51.00 | 50.62 | 50.68 | 50.97 |
| nlp/sort_words_by_num_of_syllables | 38.09 | 58.08 | 57.99 | 57.68 | 58.79 | 61.45 | 54.95 |
| nlp/sort_words_by_rhyming | 35.40 | 52.19 | 53.27 | 53.40 | 51.97 | 52.05 | 52.07 |
| nlp/syllable_words_1 | 16.96 | 36.06 | 35.04 | 34.65 | 34.69 | 34.82 | 34.89 |
| nlp/syllable_words_2 | 10.98 | 30.55 | 29.79 | 29.70 | 29.06 | 29.73 | 29.31 |
| nlp/trigram_rec | 13.46 | 53.11 | 45.58 | 47.52 | 45.19 | 45.33 | 45.45 |
| nlp/uppercase_by_token | 9.39 | 27.10 | 26.55 | 27.36 | 26.90 | 27.10 | 27.52 |
| nlp/uppercase_by_type | 28.53 | 46.16 | 45.63 | 45.62 | 45.33 | 45.72 | 45.60 |
| nlp/verses_2om_3om_2instances | 6.41 | 56.36 | 54.03 | 55.51 | 58.13 | 55.80 | 58.24 |
| nlp/vowel_sequencies_gr_1K | 30.55 | 49.89 | 49.02 | 48.83 | 48.63 | 48.66 | 48.74 |
| nlp/words_no_vowels | 10.23 | 27.42 | 27.45 | 27.26 | 27.50 | 27.81 | 28.09 |
| oneliners/bi-grams | 1.18 | 1.30 | 1.30 | 1.29 | 1.31 | 1.32 | 1.30 |
| oneliners/comm | 0.03 | 0.13 | 0.14 | - | 0.12 | 0.12 | 0.12 |
| oneliners/diff | 0.26 | 0.43 | 0.41 | - | 0.40 | 0.40 | 0.39 |
| oneliners/nfa-regex | 8.23 | 1.94 | 1.90 | - | 1.87 | 1.88 | 1.88 |
| oneliners/opt-parallel | 0.10 | 0.25 | 0.20 | - | 0.21 | 0.20 | 0.21 |
| oneliners/set-diff | 0.24 | 0.35 | 0.36 | - | 0.35 | 0.35 | 0.35 |
| oneliners/sort | 0.12 | 0.24 | 0.25 | - | 0.23 | 0.27 | 0.23 |
| oneliners/sort-sort | 0.17 | 0.36 | 0.40 | - | 0.28 | 0.32 | 0.36 |
| oneliners/spell | 1.05 | 0.63 | 0.91 | 0.91 | 1.11 | 1.09 | 0.66 |
| oneliners/top-n | 0.92 | 0.59 | 0.70 | 0.63 | 0.98 | 1.00 | 0.54 |
| oneliners/uniq-ips | 0.07 | 0.18 | 0.21 | - | 0.20 | 0.19 | 0.18 |
| oneliners/wf | 0.86 | 0.50 | 0.62 | - | 0.99 | 0.92 | 0.50 |
| unixfun/1 | 0.07 | 0.20 | 0.21 | - | 0.21 | 0.22 | 0.20 |
| unixfun/10 | 0.06 | 0.33 | 0.47 | - | 0.17 | 0.26 | 0.36 |
| unixfun/11 | 0.06 | 0.37 | 0.51 | - | 0.17 | 0.29 | 0.38 |
| unixfun/12 | 0.28 | 0.41 | 0.60 | - | 0.39 | 0.39 | 0.36 |
| unixfun/13 | 0.04 | 0.23 | 0.28 | - | 0.26 | 0.26 | 0.23 |
| unixfun/14 | 0.73 | 0.63 | 0.57 | - | 0.94 | 1.20 | 0.66 |
| unixfun/15 | 0.06 | 0.19 | 0.21 | - | 0.22 | 0.22 | 0.19 |
| unixfun/16 | 0.17 | 0.28 | 0.35 | - | 0.28 | 0.28 | 0.29 |
| unixfun/17 | 0.16 | 0.35 | 0.36 | 0.35 | 0.27 | 0.37 | 0.35 |
| unixfun/18 | 0.03 | 0.19 | 0.33 | - | 0.21 | 0.21 | 0.19 |
| unixfun/19 | 0.02 | 0.21 | 0.22 | - | 0.23 | 0.22 | 0.21 |
| unixfun/2 | 0.29 | 0.28 | 0.30 | - | 0.39 | 0.39 | 0.28 |
| unixfun/20 | 0.00 | 0.17 | 0.17 | - | 0.17 | 0.17 | 0.17 |
| unixfun/21 | 0.97 | 0.55 | 0.64 | - | 1.11 | 1.11 | 0.57 |
| unixfun/23 | 0.06 | 0.27 | 0.55 | - | 0.27 | 0.28 | 0.27 |
| unixfun/24 | 0.07 | 0.18 | 0.26 | - | 0.20 | 0.20 | 0.18 |
| unixfun/25 | 0.07 | 0.17 | 0.25 | - | 0.19 | 0.18 | 0.18 |
| unixfun/26 | 0.07 | 0.32 | 0.51 | 0.48 | 0.29 | 0.29 | 0.31 |
| unixfun/28 | 0.06 | 0.38 | 0.60 | 0.57 | 0.39 | 0.40 | 0.38 |
| unixfun/29 | 0.06 | 0.29 | 0.36 | 0.31 | 0.28 | 0.32 | 0.28 |
| unixfun/3 | 0.00 | 0.13 | 0.17 | - | 0.17 | 0.17 | 0.13 |
| unixfun/30 | 0.10 | 0.33 | 0.54 | 0.52 | 0.34 | 0.34 | 0.34 |
| unixfun/31 | 0.10 | 0.33 | 0.51 | 0.50 | 0.34 | 0.33 | 0.33 |
| unixfun/32 | 0.04 | 0.23 | 0.26 | 0.24 | 0.24 | 0.27 | 0.22 |
| unixfun/33 | 0.04 | 0.20 | 0.25 | 0.25 | 0.25 | 0.25 | 0.22 |
| unixfun/34 | 0.00 | 0.12 | 0.11 | - | 0.11 | 0.11 | 0.11 |
| unixfun/35 | 0.02 | 0.18 | 0.21 | - | 0.19 | 0.20 | 0.18 |
| unixfun/36 | 0.06 | 0.19 | 0.16 | 0.17 | 0.16 | 0.15 | 0.17 |
| unixfun/4 | 0.28 | 0.34 | 0.37 | - | 0.36 | 0.42 | 0.33 |
| unixfun/5 | 0.04 | 0.18 | 0.20 | - | 0.20 | 0.20 | 0.18 |
| unixfun/6 | 0.07 | 0.23 | 0.32 | - | 0.27 | 0.26 | 0.24 |
| unixfun/7 | 0.08 | 0.19 | 0.31 | - | 0.22 | 0.22 | 0.20 |
| unixfun/8 | 0.03 | 0.20 | 0.31 | - | 0.20 | 0.22 | 0.20 |
| unixfun/9 | 0.03 | 0.22 | 0.35 | - | 0.23 | 0.26 | 0.23 |
| weather/temp-analytics | 4.35 | 4.58 | 4.44 | 4.41 | 4.53 | 4.53 | 4.53 |
| weather/tuft-weather | 462.70 | 465.99 | 470.08 | 462.73 | 463.27 | 463.59 | 463.74 |
| web-search/engine | 640.36 | 710.06 | 706.69 | 683.77 | 697.52 | 686.76 | 680.36 |
