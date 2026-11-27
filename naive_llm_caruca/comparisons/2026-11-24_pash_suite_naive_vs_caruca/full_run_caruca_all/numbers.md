# Numbers for the run (86 scripts)

Fix-ups applied when counting (records unchanged): output compared again against the same repeat's bash: rows compared again 1290. Timed runs left out because node was missing: 0. Rows replaced by redone runs: 0.

Built by `summarise.py` from the records in this folder. It only counts.

Timed repeats per script and source: 3 repeat(s): 344. Times are medians over the repeats.

## 1. Output and what PaSh did, per source (timed runs)

| Source | Scripts | Output same as bash | Same as Koala's stored answer (of scripts with one) | PaSh ran at least one part in parallel | Fell back to plain bash | Other state |
|---|---|---|---|---|---|---|
| PaSh's own files | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 |
| Caruca's files, PaSh grammar (all converted) | 86 | 77 of 86 | 37 of 46 | 29 of 86 | 33 of 86 | compiled, nothing split: 24 |
| Caruca, full grammar where traced | 86 | 76 of 86 | 36 of 46 | 40 of 86 | 22 of 86 | compiled, nothing split: 24 |
| PaSh's own files, second copy | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 |

Plain bash itself matched Koala's stored answer in 46 of 46 scripts that have one.

Timed runs whose output differs from bash: oneliners/spell (caruca-pash-all), oneliners/top-n (caruca-main-all), unixfun/17 (caruca-main-all), unixfun/23 (caruca-pash-all), unixfun/23 (caruca-main-all), unixfun/26 (caruca-pash-all), unixfun/26 (caruca-main-all), unixfun/28 (caruca-pash-all), unixfun/28 (caruca-main-all), unixfun/29 (caruca-pash-all), unixfun/29 (caruca-main-all), unixfun/30 (caruca-pash-all), unixfun/30 (caruca-main-all), unixfun/31 (caruca-pash-all), unixfun/31 (caruca-main-all), unixfun/32 (caruca-pash-all), unixfun/32 (caruca-main-all), unixfun/33 (caruca-pash-all), unixfun/33 (caruca-main-all).

Runs with the stand-in programs whose output differs from bash: oneliners/spell (caruca-pash-all), oneliners/top-n (caruca-main-all), unixfun/17 (caruca-main-all), unixfun/23 (caruca-pash-all), unixfun/23 (caruca-main-all), unixfun/26 (caruca-pash-all), unixfun/26 (caruca-main-all), unixfun/28 (caruca-pash-all), unixfun/28 (caruca-main-all), unixfun/29 (caruca-pash-all), unixfun/29 (caruca-main-all), unixfun/30 (caruca-pash-all), unixfun/30 (caruca-main-all), unixfun/31 (caruca-pash-all), unixfun/31 (caruca-main-all), unixfun/32 (caruca-pash-all), unixfun/32 (caruca-main-all), unixfun/33 (caruca-pash-all), unixfun/33 (caruca-main-all).

## 2. Parts of the scripts (what PaSh compiles), per source (runs with the stand-in programs)

A part is one piece of a script that PaSh asks its compiler to handle. Every part not run in parallel counts against the source, whatever the cause (Tiran, 2026-11-24); the causes are listed.

| Source | Scripts | Parts sent (each time) | Run in parallel | Distinct parts | Distinct run in parallel | Causes, parts not run in parallel (each time) |
|---|---|---|---|---|---|---|
| PaSh's own files | 86 | 88900 | 41 of 88900 | 177 | 41 of 177 | missing annotation 33837, other 1009, pash crash 4, unsupported construct 54009 |
| Caruca's files, PaSh grammar (all converted) | 86 | 88900 | 29 of 88900 | 177 | 29 of 177 | missing annotation 27771, other 2057, pash crash 11, refused by annotation 24, unsupported construct 59008 |
| Caruca, full grammar where traced | 86 | 88900 | 40 of 88900 | 177 | 40 of 177 | missing annotation 27771, other 11053, pash crash 3, refused by annotation 24, unsupported construct 50009 |

## 3. Distinct parts compared with PaSh's own files

Paired by script and part text. 'Gained': run in parallel with this source but not with PaSh's own; 'lost': the reverse.

| Source | Distinct parts with both | Both in parallel | Gained | Lost | Neither |
|---|---|---|---|---|---|
| Caruca's files, PaSh grammar (all converted) | 177 | 29 | 0 | 12 | 136 |
| Caruca, full grammar where traced | 177 | 40 | 0 | 1 | 136 |

## 4. Command uses, by who supplied the files (runs with the stand-in programs)

A command use is one place a script calls a command, in one distinct part. 'Ours' means the source's own files (naive LLM's or Caruca's); 'PaSh's own' means the source has none for that command, so PaSh's own files were used.

| Source | Whose files | Uses in parts PaSh ran in parallel | Split | Not split: file says no | Not split: only a split PaSh has not implemented | Not split: no answer / no files / raised | Not split: allowed but not split | Uses in parts not run in parallel | Uses outside every part |
|---|---|---|---|---|---|---|---|---|---|
| PaSh's own files | pash-own | 230 | 126 | 23 | 22 | 59 | 0 | 255 | 121 |
| PaSh's own files | none | 0 | 0 | 0 | 0 | 0 | 0 | 124 | 84 |
| Caruca's files, PaSh grammar (all converted) | ours | 165 | 116 | 49 | 0 | 0 | 0 | 362 | 166 |
| Caruca's files, PaSh grammar (all converted) | pash-own | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Caruca's files, PaSh grammar (all converted) | none | 0 | 0 | 0 | 0 | 0 | 0 | 81 | 39 |
| Caruca, full grammar where traced | ours | 244 | 158 | 86 | 0 | 0 | 0 | 283 | 166 |
| Caruca, full grammar where traced | pash-own | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Caruca, full grammar where traced | none | 0 | 0 | 0 | 0 | 0 | 0 | 81 | 39 |

Files that raised an error when PaSh's words were passed to them: none.

Check of the method: in 639 of 639 uses in parts PaSh ran in parallel, PaSh split the use exactly when the files (asked with PaSh's words) allowed a split PaSh can carry out.

## 5. Commands where the source's own files changed what PaSh split

Per command: in how many scripts the command was split with this source and not with PaSh's own (gained), and the reverse (lost). Counted per script.

| Source | Command | Gained (scripts) | Lost (scripts) |
|---|---|---|---|
| Caruca's files, PaSh grammar (all converted) | cat | 29 | 0 |
| Caruca's files, PaSh grammar (all converted) | cut | 0 | 9 |
| Caruca's files, PaSh grammar (all converted) | grep | 0 | 4 |
| Caruca's files, PaSh grammar (all converted) | sed | 7 | 5 |
| Caruca's files, PaSh grammar (all converted) | sort | 0 | 17 |
| Caruca's files, PaSh grammar (all converted) | tr | 2 | 6 |
| Caruca's files, PaSh grammar (all converted) | uniq | 2 | 0 |
| Caruca, full grammar where traced | cat | 40 | 0 |
| Caruca, full grammar where traced | col | 0 | 1 |
| Caruca, full grammar where traced | sed | 8 | 1 |
| Caruca, full grammar where traced | sort | 0 | 17 |
| Caruca, full grammar where traced | tr | 2 | 2 |
| Caruca, full grammar where traced | uniq | 2 | 0 |

## 6. Time (median of three timed runs per source and script)

Ratios are bash time divided by the source's time (above 1 = faster than bash). Summaries are geometric means over the scripts. All of a source's commands are swapped in at once, so a time difference belongs to the source as a whole, not to any one command.

| Source | Scripts | Speed-up over bash (geometric mean) | Time vs PaSh's own (geometric mean; below 1 = faster) | Faster than PaSh's own by more than 10% | Slower by more than 10% |
|---|---|---|---|---|---|
| PaSh's own files | 86 | 0.44x | 1.00 | 0 of 86 | 0 of 86 |
| Caruca's files, PaSh grammar (all converted) | 86 | 0.41x | 1.09 | 5 of 86 | 30 of 86 |
| Caruca, full grammar where traced | 86 | 0.40x | 1.10 | 3 of 86 | 32 of 86 |
| PaSh's own files, second copy | 86 | 0.44x | 1.00 | 1 of 86 | 3 of 86 |

Noise check: the second, identical copy of PaSh's own files took between 0.83 and 1.46 times as long as the first (median 1.00; 4 of 86 scripts differ by more than 10%). A difference smaller than that spread is not evidence of anything.


### Per script (seconds)

| Script | bash | PaSh's own files | Caruca's files, PaSh grammar (all converted) | Caruca, full grammar where traced | PaSh's own files, second copy |
|---|---|---|---|---|---|
| analytics/nginx | 1.29 | 1.47 | 1.43 | 1.52 | 1.44 |
| analytics/pcaps | 100.25 | 101.54 | 102.47 | 100.71 | 101.42 |
| analytics/ray-tracing | 0.00 | 0.10 | 0.12 | 0.12 | 0.11 |
| bio/bio | 0.12 | 0.23 | 0.24 | 0.24 | 0.23 |
| covid/1 | 10.26 | 6.52 | 10.35 | 7.43 | 5.89 |
| covid/2 | 10.25 | 6.67 | 10.21 | 7.95 | 7.21 |
| covid/3 | 15.14 | 8.29 | 15.35 | 8.92 | 7.97 |
| covid/4 | 12.54 | 6.74 | 12.72 | 7.82 | 6.78 |
| covid/5 | 12.22 | 12.08 | 12.17 | 12.17 | 12.31 |
| file-mod/compress_files | 18.62 | 19.17 | 19.19 | 19.15 | 19.22 |
| file-mod/encrypt_files | 2.10 | 2.86 | 2.66 | 2.81 | 4.18 |
| file-mod/img_convert | 32.35 | 35.61 | 35.80 | 35.90 | 35.70 |
| file-mod/thumbnail_generation | 11.11 | 10.90 | 10.98 | 11.18 | 10.76 |
| file-mod/to_mp3 | 8.62 | 8.97 | 8.95 | 8.96 | 8.95 |
| nlp/bigrams | 45.85 | 63.15 | 63.39 | 63.89 | 63.10 |
| nlp/bigrams_appear_twice | 58.67 | 76.06 | 75.96 | 76.40 | 75.89 |
| nlp/compare_exodus_genesis | 87.05 | 104.77 | 104.69 | 104.96 | 104.52 |
| nlp/count_consonant_seq | 39.78 | 57.70 | 57.22 | 56.08 | 57.62 |
| nlp/count_morphs | 8.21 | 25.56 | 24.96 | 25.46 | 25.39 |
| nlp/count_trigrams | 51.33 | 68.48 | 68.16 | 68.79 | 68.06 |
| nlp/count_vowel_seq | 7.97 | 25.10 | 25.08 | 23.80 | 25.61 |
| nlp/count_words | 30.49 | 48.33 | 47.97 | 48.98 | 48.48 |
| nlp/find_anagrams | 38.76 | 55.72 | 55.68 | 56.07 | 55.78 |
| nlp/letter_words | 37.33 | 71.50 | 71.30 | 73.10 | 72.05 |
| nlp/merge_upper | 30.52 | 48.61 | 48.30 | 49.12 | 48.72 |
| nlp/sort | 34.08 | 52.78 | 52.07 | 52.49 | 51.90 |
| nlp/sort_words_by_folding | 34.13 | 53.65 | 53.87 | 52.68 | 55.47 |
| nlp/sort_words_by_num_of_syllables | 38.06 | 58.66 | 55.69 | 59.88 | 55.57 |
| nlp/sort_words_by_rhyming | 36.57 | 53.31 | 55.43 | 54.60 | 53.35 |
| nlp/syllable_words_1 | 17.09 | 35.39 | 34.99 | 35.95 | 35.44 |
| nlp/syllable_words_2 | 10.87 | 29.45 | 28.71 | 29.95 | 29.30 |
| nlp/trigram_rec | 13.48 | 49.82 | 49.41 | 48.13 | 47.24 |
| nlp/uppercase_by_token | 9.35 | 28.35 | 28.41 | 28.42 | 27.71 |
| nlp/uppercase_by_type | 29.70 | 48.44 | 51.12 | 50.45 | 49.41 |
| nlp/verses_2om_3om_2instances | 6.21 | 54.48 | 56.24 | 57.67 | 62.56 |
| nlp/vowel_sequencies_gr_1K | 31.21 | 51.82 | 49.83 | 48.42 | 51.68 |
| nlp/words_no_vowels | 10.19 | 27.92 | 28.00 | 29.53 | 28.14 |
| oneliners/bi-grams | 1.14 | 1.30 | 1.26 | 1.27 | 1.25 |
| oneliners/comm | 0.03 | 0.12 | 0.14 | 0.14 | 0.12 |
| oneliners/diff | 0.27 | 0.38 | 0.44 | 0.42 | 0.37 |
| oneliners/nfa-regex | 8.38 | 1.90 | 1.95 | 1.91 | 1.89 |
| oneliners/opt-parallel | 0.09 | 0.19 | 0.19 | 0.19 | 0.18 |
| oneliners/set-diff | 0.25 | 0.36 | 0.36 | 0.36 | 0.37 |
| oneliners/sort | 0.12 | 0.21 | 0.26 | 0.25 | 0.21 |
| oneliners/sort-sort | 0.17 | 0.34 | 0.28 | 0.30 | 0.34 |
| oneliners/spell | 1.02 | 0.58 | 1.08 | 1.12 | 0.60 |
| oneliners/top-n | 0.87 | 0.50 | 0.97 | 1.01 | 0.49 |
| oneliners/uniq-ips | 0.07 | 0.18 | 0.24 | 0.23 | 0.18 |
| oneliners/wf | 0.87 | 0.49 | 0.97 | 0.97 | 0.49 |
| unixfun/1 | 0.06 | 0.16 | 0.19 | 0.19 | 0.16 |
| unixfun/10 | 0.06 | 0.32 | 0.16 | 0.27 | 0.32 |
| unixfun/11 | 0.06 | 0.32 | 0.16 | 0.27 | 0.32 |
| unixfun/12 | 0.25 | 0.34 | 0.34 | 0.35 | 0.34 |
| unixfun/13 | 0.04 | 0.18 | 0.21 | 0.21 | 0.18 |
| unixfun/14 | 0.70 | 0.60 | 0.81 | 0.91 | 0.60 |
| unixfun/15 | 0.06 | 0.17 | 0.20 | 0.20 | 0.17 |
| unixfun/16 | 0.16 | 0.25 | 0.26 | 0.26 | 0.25 |
| unixfun/17 | 0.16 | 0.31 | 0.26 | 0.35 | 0.31 |
| unixfun/18 | 0.03 | 0.17 | 0.20 | 0.20 | 0.17 |
| unixfun/19 | 0.02 | 0.18 | 0.23 | 0.22 | 0.19 |
| unixfun/2 | 0.28 | 0.27 | 0.39 | 0.39 | 0.27 |
| unixfun/20 | 0.00 | 0.15 | 0.16 | 0.16 | 0.15 |
| unixfun/21 | 0.94 | 0.52 | 1.06 | 1.06 | 0.54 |
| unixfun/23 | 0.06 | 0.25 | 0.24 | 0.24 | 0.26 |
| unixfun/24 | 0.07 | 0.17 | 0.20 | 0.20 | 0.17 |
| unixfun/25 | 0.07 | 0.16 | 0.21 | 0.20 | 0.16 |
| unixfun/26 | 0.07 | 0.27 | 0.24 | 0.25 | 0.28 |
| unixfun/28 | 0.06 | 0.34 | 0.34 | 0.34 | 0.34 |
| unixfun/29 | 0.06 | 0.20 | 0.26 | 0.26 | 0.20 |
| unixfun/3 | 0.00 | 0.13 | 0.16 | 0.16 | 0.13 |
| unixfun/30 | 0.09 | 0.30 | 0.37 | 0.36 | 0.30 |
| unixfun/31 | 0.09 | 0.30 | 0.40 | 0.39 | 0.32 |
| unixfun/32 | 0.04 | 0.19 | 0.21 | 0.21 | 0.19 |
| unixfun/33 | 0.04 | 0.19 | 0.21 | 0.21 | 0.20 |
| unixfun/34 | 0.00 | 0.09 | 0.10 | 0.10 | 0.09 |
| unixfun/35 | 0.02 | 0.17 | 0.20 | 0.19 | 0.17 |
| unixfun/36 | 0.06 | 0.15 | 0.16 | 0.18 | 0.17 |
| unixfun/4 | 0.25 | 0.31 | 0.36 | 0.37 | 0.32 |
| unixfun/5 | 0.04 | 0.20 | 0.19 | 0.19 | 0.17 |
| unixfun/6 | 0.07 | 0.21 | 0.22 | 0.22 | 0.22 |
| unixfun/7 | 0.08 | 0.18 | 0.21 | 0.21 | 0.17 |
| unixfun/8 | 0.03 | 0.18 | 0.21 | 0.21 | 0.18 |
| unixfun/9 | 0.03 | 0.21 | 0.23 | 0.23 | 0.21 |
| weather/temp-analytics | 4.22 | 4.37 | 4.40 | 4.40 | 4.37 |
| weather/tuft-weather | 464.57 | 467.07 | 466.58 | 465.65 | 465.25 |
| web-search/engine | 617.47 | 661.24 | 656.96 | 661.30 | 660.27 |
