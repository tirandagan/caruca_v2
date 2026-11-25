# Numbers for the run (86 scripts)

Fix-ups applied when counting (records unchanged): output compared again against the same repeat's bash: rows compared again 1410, same as bash: changed 266, output files same as bash: changed 281. Timed runs left out because node was missing: 7.

Built by `summarise.py` from the records in this folder. It only counts.

Timed repeats per script and source: 1 repeat(s): 210, 3 repeat(s): 266. Times are medians over the repeats. The naive LLM's second sed file was run only on scripts that use sed.

## 1. Output and what PaSh did, per source (timed runs)

| Source | Scripts | Output same as bash | Same as Koala's stored answer (of scripts with one) | PaSh ran at least one part in parallel | Fell back to plain bash | Other state |
|---|---|---|---|---|---|---|
| PaSh's own files | 85 | 85 of 85 | 46 of 46 | 41 of 85 | 43 of 85 | compiled, nothing split: 1 |
| Naive LLM's files | 85 | 85 of 85 | 46 of 46 | 43 of 85 | 41 of 85 | compiled, nothing split: 1 |
| Naive LLM, sed file v2 | 51 | 51 of 51 | 12 of 12 | 14 of 51 | 37 of 51 | - |
| Caruca's files, PaSh grammar | 85 | 85 of 85 | 46 of 46 | 29 of 85 | 55 of 85 | compiled, nothing split: 1 |
| Caruca's files, main grammar | 85 | 85 of 85 | 46 of 46 | 41 of 85 | 43 of 85 | compiled, nothing split: 1 |
| PaSh's own files, second copy | 85 | 85 of 85 | 46 of 46 | 41 of 85 | 43 of 85 | compiled, nothing split: 1 |

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

## 6. Time (one timed run per source and script)

Ratios are bash time divided by the source's time (above 1 = faster than bash). Summaries are geometric means over the scripts. All of a source's commands are swapped in at once, so a time difference belongs to the source as a whole, not to any one command.

| Source | Scripts | Speed-up over bash (geometric mean) | Time vs PaSh's own (geometric mean; below 1 = faster) | Faster than PaSh's own by more than 10% | Slower by more than 10% |
|---|---|---|---|---|---|
| PaSh's own files | 85 | 0.42x | 1.00 | 0 of 85 | 0 of 85 |
| Naive LLM's files | 85 | 0.36x | 1.16 | 3 of 85 | 35 of 85 |
| Naive LLM, sed file v2 | 51 | 0.51x | 1.07 | 2 of 51 | 11 of 51 |
| Caruca's files, PaSh grammar | 85 | 0.40x | 1.05 | 8 of 85 | 20 of 85 |
| Caruca's files, main grammar | 85 | 0.40x | 1.07 | 7 of 85 | 27 of 85 |
| PaSh's own files, second copy | 85 | 0.42x | 1.00 | 4 of 85 | 4 of 85 |

Noise check: the second, identical copy of PaSh's own files took between 0.83 and 1.13 times as long as the first (median 1.00; 8 of 85 scripts differ by more than 10%). A difference smaller than that spread is not evidence of anything.


### Per script (seconds)

| Script | bash | PaSh's own files | Naive LLM's files | Naive LLM, sed file v2 | Caruca's files, PaSh grammar | Caruca's files, main grammar | PaSh's own files, second copy |
|---|---|---|---|---|---|---|---|
| analytics/nginx | 1.30 | 1.48 | 1.46 | 1.45 | 1.46 | 1.48 | 1.49 |
| analytics/pcaps | 124.14 | 122.51 | 121.14 | 128.28 | 138.01 | 122.44 | 136.32 |
| analytics/ray-tracing | 0.00 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.13 |
| bio/bio | 0.13 | 0.28 | 0.26 | 0.25 | 0.26 | 0.26 | 0.26 |
| covid/1 | 10.57 | 7.12 | 13.19 | 11.16 | 10.40 | 7.85 | 6.68 |
| covid/2 | 10.52 | 6.91 | 14.45 | 10.62 | 10.62 | 8.48 | 7.44 |
| covid/3 | 15.18 | 7.48 | 17.90 | 10.73 | 15.15 | 8.62 | 7.12 |
| covid/4 | 12.45 | 6.67 | 16.75 | 9.27 | 12.25 | 7.36 | 6.84 |
| covid/5 | 11.15 | 11.26 | 11.38 | 10.67 | 10.79 | 11.31 | 11.55 |
| file-mod/compress_files | 19.14 | 19.49 | 19.46 | 19.65 | 19.31 | 19.45 | 19.21 |
| file-mod/encrypt_files | 2.00 | 2.73 | 2.69 | 2.92 | 2.65 | 2.94 | 3.10 |
| file-mod/img_convert | 35.47 | 36.89 | 35.65 | 35.70 | 35.53 | 36.93 | 37.88 |
| file-mod/thumbnail_generation | 11.01 | 11.22 | 10.99 | 11.21 | 10.83 | 10.91 | 11.20 |
| file-mod/to_mp3 | 10.12 | 9.97 | 9.84 | 9.15 | 9.03 | 9.73 | 9.79 |
| nlp/bigrams | 49.48 | 69.41 | 68.66 | 68.23 | 68.66 | 68.32 | 71.02 |
| nlp/bigrams_appear_twice | 62.81 | 82.63 | 88.67 | 86.38 | 81.70 | 84.58 | 86.39 |
| nlp/compare_exodus_genesis | 87.99 | 108.91 | 117.16 | 120.91 | 120.50 | 124.95 | 120.15 |
| nlp/count_consonant_seq | 39.02 | 57.23 | 57.56 | 57.22 | 62.64 | 61.80 | 59.11 |
| nlp/count_morphs | 8.59 | 29.94 | 29.30 | 28.67 | 28.71 | 26.77 | 26.52 |
| nlp/count_trigrams | 55.62 | 74.53 | 78.88 | 79.17 | 76.99 | 79.81 | 81.43 |
| nlp/count_vowel_seq | 8.18 | 26.52 | 27.48 | 26.95 | 27.55 | 27.57 | 29.88 |
| nlp/count_words | 31.15 | 50.74 | 50.79 | 49.32 | 50.60 | 56.77 | 54.24 |
| nlp/find_anagrams | 41.94 | 61.78 | 66.47 | 56.92 | 57.24 | 55.99 | 56.78 |
| nlp/letter_words | 38.64 | 80.30 | 74.44 | 72.71 | 76.92 | 78.50 | 79.40 |
| nlp/merge_upper | 30.50 | 49.91 | 49.49 | 50.48 | 51.98 | 53.22 | 50.11 |
| nlp/sort | 33.46 | 51.50 | 51.66 | 53.32 | 56.17 | 53.33 | 52.03 |
| nlp/sort_words_by_folding | 34.36 | 54.88 | 56.23 | 56.77 | 53.89 | 55.07 | 53.22 |
| nlp/sort_words_by_num_of_syllables | 38.09 | 58.08 | 59.21 | 54.72 | 59.27 | 64.02 | 54.26 |
| nlp/sort_words_by_rhyming | 35.27 | 51.91 | 53.15 | 54.28 | 52.22 | 52.17 | 52.07 |
| nlp/syllable_words_1 | 17.97 | 38.13 | 44.39 | 36.79 | 36.16 | 36.40 | 36.23 |
| nlp/syllable_words_2 | 11.25 | 30.71 | 30.91 | 30.85 | 30.57 | 30.57 | 30.84 |
| nlp/trigram_rec | 14.41 | 53.11 | 52.90 | 47.52 | 45.19 | 45.51 | 45.45 |
| nlp/uppercase_by_token | 9.17 | 27.10 | 26.81 | 27.36 | 26.90 | 27.10 | 27.52 |
| nlp/uppercase_by_type | 28.55 | 45.57 | 45.29 | 45.47 | 45.23 | 45.26 | 45.11 |
| nlp/verses_2om_3om_2instances | 6.41 | 58.16 | 58.62 | 58.32 | 58.13 | 57.98 | 58.24 |
| nlp/vowel_sequencies_gr_1K | 30.55 | 49.89 | 53.65 | 48.83 | 55.20 | 59.88 | 49.53 |
| nlp/words_no_vowels | 10.29 | 29.09 | 29.23 | 29.32 | 29.25 | 29.17 | 29.80 |
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
| weather/temp-analytics | 4.33 | 4.36 | 4.40 | 4.41 | 4.38 | 4.35 | 4.50 |
| weather/tuft-weather | 443.19 | 452.41 | 482.80 | 444.57 | 442.62 | 441.09 | 441.77 |
| web-search/engine | - | - | - | - | - | - | - |
