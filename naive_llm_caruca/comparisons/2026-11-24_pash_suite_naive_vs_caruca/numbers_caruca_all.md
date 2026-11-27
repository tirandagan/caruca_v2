# Numbers for the PaSh-suite report

Written by `count_report.py` from `/private/tmp/claude-501/-Users-tirandagan-dev-stevens-caruca-v2/c5935e79-a4e0-4396-a992-6ff133c8267a/scratchpad/rec_caruca_all`. Every rate is "a of b". Do not edit by hand; re-run the script.

- Scripts run: 86. Scripts whose plain-bash output is the same in every bash run (**N**): 86.
- Distinct parts sent to PaSh (**P**): 177. Command uses inside those parts (**U**): 609.
- Command uses that ran outside every part sent to PaSh (not in U): PaSh's own files 205, Caruca's files, PaSh grammar (all converted commands) 205, Caruca, full grammar where traced 205.

## Table 1: What PaSh did with each source's files

| Source | Output same as bash | Scripts with any part run in parallel | Parts run in parallel | Command uses split | Faster than bash |
|---|---|---:|---:|---:|---:|
| PaSh's own files (reference) | 86 of 86 | 41 of 86 | 41 of 177 | 126 of 609 | 13 of 86 (median speed-up 0.56x) |
| Caruca's files, PaSh grammar (all converted commands) | 77 of 86 — **wrong: oneliners/spell, unixfun/23, unixfun/26, unixfun/28, unixfun/29, unixfun/30, unixfun/31, unixfun/32, unixfun/33** | 29 of 86 | 29 of 177 | 116 of 609 | 4 of 86 (median speed-up 0.59x) |
| Caruca, full grammar where traced | 76 of 86 — **wrong: oneliners/top-n, unixfun/17, unixfun/23, unixfun/26, unixfun/28, unixfun/29, unixfun/30, unixfun/31, unixfun/32, unixfun/33** | 40 of 86 | 40 of 177 | 158 of 609 | 6 of 86 (median speed-up 0.55x) |

## Table 2: Commands a source brings its own files for, and what PaSh did with them

| Source | Uses with the source's own files | … split with them | … the same uses split with PaSh's own files | Uses with PaSh's own files filled in | … result same as with PaSh's own | Uses with no files from anyone |
|---|---:|---:|---:|---:|---:|---:|
| Caruca's files, PaSh grammar (all converted commands) | 527 of 609 | 116 of 527 | 126 of 527 | 1 of 609 | 1 of 1 | 81 of 609 |
| Caruca, full grammar where traced | 527 of 609 | 158 of 527 | 126 of 527 | 1 of 609 | 1 of 1 | 81 of 609 |


## Chart A data: the scripts' parts, compared with PaSh's own files

Reference, PaSh's own files: run in parallel 41 of 177; not 136 of 177.

| Source | Run in parallel with both | Only with this source | With neither | Only with PaSh's own files |
|---|---:|---:|---:|---:|
| Caruca's files, PaSh grammar (all converted commands) | 29 of 177 | 0 of 177 | 136 of 177 | 12 of 177 |
| Caruca, full grammar where traced | 40 of 177 | 0 of 177 | 136 of 177 | 1 of 177 |

## Table 3: Every command where a source changed what PaSh did

| Command | Uses in the suite | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced | Output |
|---|---:|---:|---:|---:|---|
| `cat` | 94 | split 0 of 94 | **split 29 of 94** | **split 40 of 94** | Caruca's files, PaSh grammar (all converted commands): wrong in 9 scripts; Caruca, full grammar where traced: wrong in 10 scripts |
| `tr` | 75 | split 29 of 75 | **split 23 of 75** | **split 27 of 75** | Caruca's files, PaSh grammar (all converted commands): wrong in 7 scripts; Caruca, full grammar where traced: wrong in 7 scripts |
| `grep` | 74 | split 29 of 74 | **split 22 of 74** | split 29 of 74 | Caruca's files, PaSh grammar (all converted commands): wrong in 7 scripts; Caruca, full grammar where traced: wrong in 8 scripts |
| `sort` | 67 | split 25 of 67 | **split 0 of 67** | **split 0 of 67** | Caruca's files, PaSh grammar (all converted commands): wrong in 1 scripts; Caruca, full grammar where traced: wrong in 2 scripts |
| `cut` | 58 | split 36 of 58 | **split 20 of 58** | split 36 of 58 | Caruca's files, PaSh grammar (all converted commands): wrong in 4 scripts; Caruca, full grammar where traced: wrong in 5 scripts |
| `sed` | 37 | split 6 of 37 | **split 19 of 37** | **split 24 of 37** | Caruca's files, PaSh grammar (all converted commands): wrong in 8 scripts; Caruca, full grammar where traced: wrong in 9 scripts |
| `echo` | 30 | split 0 of 30 | **split 0 of 30** | **split 0 of 30** | all same as bash |
| `uniq` | 30 | split 0 of 30 | **split 2 of 30** | **split 2 of 30** | Caruca's files, PaSh grammar (all converted commands): wrong in 1 scripts; Caruca, full grammar where traced: wrong in 2 scripts |
| `awk` | 14 | split 0 of 14 | **split 0 of 14** | split 0 of 14 | all same as bash |
| `comm` | 5 | split 0 of 5 | split 0 of 5 | **split 0 of 5** | Caruca's files, PaSh grammar (all converted commands): wrong in 1 scripts |
| `col` | 1 | split 1 of 1 | split 1 of 1 | **split 0 of 1** | Caruca's files, PaSh grammar (all converted commands): wrong in 1 scripts |

The other 33 commands: every source gave the same result as PaSh's own files (mkdir, export, pure_func, head, wc, samtools, [, read, join, rm, tail, [[, cd, dirname, fmt, mkfifo, rev, ., ./crawl.sh, ./index.sh, bigrams_aux, break, continue, diff, ffmpeg, find, gzip, mawk, mogrify, printf, python3, seq, xargs). Bold = differs from PaSh's own.

## Chart B data: time against PaSh's own files

Noise (PaSh's own files, second copy against the first copy): largest difference 46.2% over 86 scripts.

| Source | Script | Median s, PaSh's own files | Median s, this source | Output same as bash | Split choices differ |
|---|---|---:|---:|---|---|
| Caruca's files, PaSh grammar (all converted commands) | analytics/nginx | 1.47 | 1.43 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | analytics/pcaps | 101.54 | 102.47 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | analytics/ray-tracing | 0.10 | 0.12 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | bio/bio | 0.23 | 0.24 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | covid/1 | 6.52 | 10.35 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | covid/2 | 6.67 | 10.21 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | covid/3 | 8.29 | 15.35 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | covid/4 | 6.74 | 12.72 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | covid/5 | 12.08 | 12.17 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | file-mod/compress_files | 19.17 | 19.19 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | file-mod/encrypt_files | 2.86 | 2.66 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | file-mod/img_convert | 35.61 | 35.80 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | file-mod/thumbnail_generation | 10.90 | 10.98 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | file-mod/to_mp3 | 8.97 | 8.95 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | nlp/bigrams | 63.15 | 63.39 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/bigrams_appear_twice | 76.06 | 75.96 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/compare_exodus_genesis | 104.77 | 104.69 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/count_consonant_seq | 57.70 | 57.22 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/count_morphs | 25.56 | 24.96 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/count_trigrams | 68.48 | 68.16 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/count_vowel_seq | 25.10 | 25.08 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/count_words | 48.33 | 47.97 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/find_anagrams | 55.72 | 55.68 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/letter_words | 71.50 | 71.30 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/merge_upper | 48.61 | 48.30 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/sort | 52.78 | 52.07 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/sort_words_by_folding | 53.65 | 53.87 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/sort_words_by_num_of_syllables | 58.66 | 55.69 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/sort_words_by_rhyming | 53.31 | 55.43 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/syllable_words_1 | 35.39 | 34.99 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/syllable_words_2 | 29.45 | 28.71 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/trigram_rec | 49.82 | 49.41 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/uppercase_by_token | 28.35 | 28.41 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/uppercase_by_type | 48.44 | 51.12 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/verses_2om_3om_2instances | 54.48 | 56.24 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/vowel_sequencies_gr_1K | 51.82 | 49.83 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | nlp/words_no_vowels | 27.92 | 28.00 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/bi-grams | 1.30 | 1.26 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/comm | 0.12 | 0.14 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/diff | 0.38 | 0.44 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/nfa-regex | 1.90 | 1.95 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/opt-parallel | 0.19 | 0.19 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/set-diff | 0.36 | 0.36 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/sort | 0.21 | 0.26 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/sort-sort | 0.34 | 0.28 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/spell | 0.58 | 1.08 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/top-n | 0.50 | 0.97 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/uniq-ips | 0.18 | 0.24 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | oneliners/wf | 0.49 | 0.97 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/1 | 0.16 | 0.19 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/10 | 0.32 | 0.16 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/11 | 0.32 | 0.16 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/12 | 0.34 | 0.34 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/13 | 0.18 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/14 | 0.60 | 0.81 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/15 | 0.17 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/16 | 0.25 | 0.26 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/17 | 0.31 | 0.26 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/18 | 0.17 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/19 | 0.18 | 0.23 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/2 | 0.27 | 0.39 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/20 | 0.15 | 0.16 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/21 | 0.52 | 1.06 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/23 | 0.25 | 0.24 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/24 | 0.17 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/25 | 0.16 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/26 | 0.27 | 0.24 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/28 | 0.34 | 0.34 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/29 | 0.20 | 0.26 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/3 | 0.13 | 0.16 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/30 | 0.30 | 0.37 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/31 | 0.30 | 0.40 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/32 | 0.19 | 0.21 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/33 | 0.19 | 0.21 | **no** | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/34 | 0.09 | 0.10 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/35 | 0.17 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/36 | 0.15 | 0.16 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/4 | 0.31 | 0.36 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/5 | 0.20 | 0.19 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/6 | 0.21 | 0.22 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/7 | 0.18 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/8 | 0.18 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | unixfun/9 | 0.21 | 0.23 | yes | yes |
| Caruca's files, PaSh grammar (all converted commands) | weather/temp-analytics | 4.37 | 4.40 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | weather/tuft-weather | 467.07 | 466.58 | yes | no |
| Caruca's files, PaSh grammar (all converted commands) | web-search/engine | 661.24 | 656.96 | yes | no |
| Caruca, full grammar where traced | analytics/nginx | 1.47 | 1.52 | yes | no |
| Caruca, full grammar where traced | analytics/pcaps | 101.54 | 100.71 | yes | no |
| Caruca, full grammar where traced | analytics/ray-tracing | 0.10 | 0.12 | yes | no |
| Caruca, full grammar where traced | bio/bio | 0.23 | 0.24 | yes | no |
| Caruca, full grammar where traced | covid/1 | 6.52 | 7.43 | yes | yes |
| Caruca, full grammar where traced | covid/2 | 6.67 | 7.95 | yes | yes |
| Caruca, full grammar where traced | covid/3 | 8.29 | 8.92 | yes | yes |
| Caruca, full grammar where traced | covid/4 | 6.74 | 7.82 | yes | yes |
| Caruca, full grammar where traced | covid/5 | 12.08 | 12.17 | yes | no |
| Caruca, full grammar where traced | file-mod/compress_files | 19.17 | 19.15 | yes | no |
| Caruca, full grammar where traced | file-mod/encrypt_files | 2.86 | 2.81 | yes | no |
| Caruca, full grammar where traced | file-mod/img_convert | 35.61 | 35.90 | yes | no |
| Caruca, full grammar where traced | file-mod/thumbnail_generation | 10.90 | 11.18 | yes | no |
| Caruca, full grammar where traced | file-mod/to_mp3 | 8.97 | 8.96 | yes | no |
| Caruca, full grammar where traced | nlp/bigrams | 63.15 | 63.89 | yes | yes |
| Caruca, full grammar where traced | nlp/bigrams_appear_twice | 76.06 | 76.40 | yes | yes |
| Caruca, full grammar where traced | nlp/compare_exodus_genesis | 104.77 | 104.96 | yes | yes |
| Caruca, full grammar where traced | nlp/count_consonant_seq | 57.70 | 56.08 | yes | yes |
| Caruca, full grammar where traced | nlp/count_morphs | 25.56 | 25.46 | yes | yes |
| Caruca, full grammar where traced | nlp/count_trigrams | 68.48 | 68.79 | yes | yes |
| Caruca, full grammar where traced | nlp/count_vowel_seq | 25.10 | 23.80 | yes | yes |
| Caruca, full grammar where traced | nlp/count_words | 48.33 | 48.98 | yes | yes |
| Caruca, full grammar where traced | nlp/find_anagrams | 55.72 | 56.07 | yes | yes |
| Caruca, full grammar where traced | nlp/letter_words | 71.50 | 73.10 | yes | yes |
| Caruca, full grammar where traced | nlp/merge_upper | 48.61 | 49.12 | yes | yes |
| Caruca, full grammar where traced | nlp/sort | 52.78 | 52.49 | yes | yes |
| Caruca, full grammar where traced | nlp/sort_words_by_folding | 53.65 | 52.68 | yes | yes |
| Caruca, full grammar where traced | nlp/sort_words_by_num_of_syllables | 58.66 | 59.88 | yes | yes |
| Caruca, full grammar where traced | nlp/sort_words_by_rhyming | 53.31 | 54.60 | yes | yes |
| Caruca, full grammar where traced | nlp/syllable_words_1 | 35.39 | 35.95 | yes | yes |
| Caruca, full grammar where traced | nlp/syllable_words_2 | 29.45 | 29.95 | yes | yes |
| Caruca, full grammar where traced | nlp/trigram_rec | 49.82 | 48.13 | yes | yes |
| Caruca, full grammar where traced | nlp/uppercase_by_token | 28.35 | 28.42 | yes | yes |
| Caruca, full grammar where traced | nlp/uppercase_by_type | 48.44 | 50.45 | yes | yes |
| Caruca, full grammar where traced | nlp/verses_2om_3om_2instances | 54.48 | 57.67 | yes | yes |
| Caruca, full grammar where traced | nlp/vowel_sequencies_gr_1K | 51.82 | 48.42 | yes | yes |
| Caruca, full grammar where traced | nlp/words_no_vowels | 27.92 | 29.53 | yes | yes |
| Caruca, full grammar where traced | oneliners/bi-grams | 1.30 | 1.27 | yes | no |
| Caruca, full grammar where traced | oneliners/comm | 0.12 | 0.14 | yes | no |
| Caruca, full grammar where traced | oneliners/diff | 0.38 | 0.42 | yes | no |
| Caruca, full grammar where traced | oneliners/nfa-regex | 1.90 | 1.91 | yes | yes |
| Caruca, full grammar where traced | oneliners/opt-parallel | 0.19 | 0.19 | yes | no |
| Caruca, full grammar where traced | oneliners/set-diff | 0.36 | 0.36 | yes | no |
| Caruca, full grammar where traced | oneliners/sort | 0.21 | 0.25 | yes | yes |
| Caruca, full grammar where traced | oneliners/sort-sort | 0.34 | 0.30 | yes | yes |
| Caruca, full grammar where traced | oneliners/spell | 0.58 | 1.12 | yes | yes |
| Caruca, full grammar where traced | oneliners/top-n | 0.50 | 1.01 | **no** | yes |
| Caruca, full grammar where traced | oneliners/uniq-ips | 0.18 | 0.23 | yes | yes |
| Caruca, full grammar where traced | oneliners/wf | 0.49 | 0.97 | yes | yes |
| Caruca, full grammar where traced | unixfun/1 | 0.16 | 0.19 | yes | yes |
| Caruca, full grammar where traced | unixfun/10 | 0.32 | 0.27 | yes | yes |
| Caruca, full grammar where traced | unixfun/11 | 0.32 | 0.27 | yes | yes |
| Caruca, full grammar where traced | unixfun/12 | 0.34 | 0.35 | yes | no |
| Caruca, full grammar where traced | unixfun/13 | 0.18 | 0.21 | yes | yes |
| Caruca, full grammar where traced | unixfun/14 | 0.60 | 0.91 | yes | yes |
| Caruca, full grammar where traced | unixfun/15 | 0.17 | 0.20 | yes | yes |
| Caruca, full grammar where traced | unixfun/16 | 0.25 | 0.26 | yes | no |
| Caruca, full grammar where traced | unixfun/17 | 0.31 | 0.35 | **no** | yes |
| Caruca, full grammar where traced | unixfun/18 | 0.17 | 0.20 | yes | yes |
| Caruca, full grammar where traced | unixfun/19 | 0.18 | 0.22 | yes | yes |
| Caruca, full grammar where traced | unixfun/2 | 0.27 | 0.39 | yes | yes |
| Caruca, full grammar where traced | unixfun/20 | 0.15 | 0.16 | yes | yes |
| Caruca, full grammar where traced | unixfun/21 | 0.52 | 1.06 | yes | yes |
| Caruca, full grammar where traced | unixfun/23 | 0.25 | 0.24 | **no** | yes |
| Caruca, full grammar where traced | unixfun/24 | 0.17 | 0.20 | yes | yes |
| Caruca, full grammar where traced | unixfun/25 | 0.16 | 0.20 | yes | yes |
| Caruca, full grammar where traced | unixfun/26 | 0.27 | 0.25 | **no** | yes |
| Caruca, full grammar where traced | unixfun/28 | 0.34 | 0.34 | **no** | yes |
| Caruca, full grammar where traced | unixfun/29 | 0.20 | 0.26 | **no** | yes |
| Caruca, full grammar where traced | unixfun/3 | 0.13 | 0.16 | yes | yes |
| Caruca, full grammar where traced | unixfun/30 | 0.30 | 0.36 | **no** | yes |
| Caruca, full grammar where traced | unixfun/31 | 0.30 | 0.39 | **no** | yes |
| Caruca, full grammar where traced | unixfun/32 | 0.19 | 0.21 | **no** | yes |
| Caruca, full grammar where traced | unixfun/33 | 0.19 | 0.21 | **no** | yes |
| Caruca, full grammar where traced | unixfun/34 | 0.09 | 0.10 | yes | no |
| Caruca, full grammar where traced | unixfun/35 | 0.17 | 0.19 | yes | yes |
| Caruca, full grammar where traced | unixfun/36 | 0.15 | 0.18 | yes | no |
| Caruca, full grammar where traced | unixfun/4 | 0.31 | 0.37 | yes | yes |
| Caruca, full grammar where traced | unixfun/5 | 0.20 | 0.19 | yes | yes |
| Caruca, full grammar where traced | unixfun/6 | 0.21 | 0.22 | yes | yes |
| Caruca, full grammar where traced | unixfun/7 | 0.18 | 0.21 | yes | yes |
| Caruca, full grammar where traced | unixfun/8 | 0.18 | 0.21 | yes | yes |
| Caruca, full grammar where traced | unixfun/9 | 0.21 | 0.23 | yes | yes |
| Caruca, full grammar where traced | weather/temp-analytics | 4.37 | 4.40 | yes | no |
| Caruca, full grammar where traced | weather/tuft-weather | 467.07 | 465.65 | yes | no |
| Caruca, full grammar where traced | web-search/engine | 661.24 | 661.30 | yes | no |

## Chart C data: which of the suite's commands each source has files for

- PaSh's own files: 19 of 43 commands (cat, tr, sort, grep, uniq, cut, head, sed, xargs, awk, rm, tail, wc, comm, mkfifo, tee, col, diff, seq)
- Caruca's files (both grammars): 29 of 43 commands (cat, tr, sort, grep, uniq, cut, head, sed, xargs, ls, awk, rm, mktemp, tail, paste, wc, comm, mkfifo, fmt, rev, tee, col, convert, diff, ffmpeg, find, iconv, join, seq)
- Files from nobody: 14 of 43 (mkdir, basename, bigrams_aux, dirname, egrep, git, gzip, mawk, mogrify, node, openssl, python3, samtools, tcpdump)
- Scripts using each command (of 86): cat 80, tr 50, sort 48, grep 47, uniq 37, cut 35, head 32, mkdir 31, basename 29, sed 25, xargs 24, ls 23, awk 14, rm 13, mktemp 10, tail 8, paste 6, wc 6, comm 4, mkfifo 3, fmt 2, rev 2, tee 2, bigrams_aux 1, col 1, convert 1, diff 1, dirname 1, egrep 1, ffmpeg 1, find 1, git 1, gzip 1, iconv 1, join 1, mawk 1, mogrify 1, node 1, openssl 1, python3 1, samtools 1, seq 1, tcpdump 1

## Table 4: Next to the Caruca paper's PaSh check

Agreement with PaSh's own files on the suite's own command lines (each distinct command line for which the source has its own files and PaSh's own files exist):

| Source | Command lines | Same inputs and outputs | Same split decision | Commands with every line agreeing | Lines where PaSh's own files give no split answer (left out) | Of the disagreements: PaSh's own split only with a special merge step, source says no split | Lines where the source's files raised an error |
|---|---:|---:|---:|---:|---:|---:|---:|
| Caruca's files, PaSh grammar (all converted commands) | 196 | 147 of 178 | 79 of 113 | 1 of 8 | 83 | 7 | 0 |
| Caruca, full grammar where traced | 196 | 155 of 178 | 83 of 113 | 1 of 8 | 83 | 7 | 0 |

| What was checked | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced |
|---|---:|---:|---:|
| Suite output identical with the files swapped in | 86 of 86 | 77 of 86 | 76 of 86 |
| Parts PaSh ran in parallel | 41 of 177 | 29 of 177 | 40 of 177 |
| Median speed-up against bash | 0.56x | 0.59x | 0.55x |

## Appendix A1: the scripts

| 2022 set | Koala group | Script | Path in Koala | Stands for | How close | Run here | Input bytes |
|---|---|---|---|---|---|---|---:|
| Classics | oneliners | nfa-regex | `~/koala/oneliners/scripts/nfa-regex.sh` | `~/pash/evaluation/benchmarks/oneliners/nfa-regex.sh` | same | yes | 10270030 |
| Classics | oneliners | sort | `~/koala/oneliners/scripts/sort.sh` | `~/pash/evaluation/benchmarks/oneliners/sort.sh` | same | yes | 30810090 |
| Classics | oneliners | top-n | `~/koala/oneliners/scripts/top-n.sh` | `~/pash/evaluation/benchmarks/oneliners/top-n.sh` | light edit: same pipeline with a stage added or swapped | yes | 30810090 |
| Classics | oneliners | wf | `~/koala/oneliners/scripts/wf.sh` | `~/pash/evaluation/benchmarks/oneliners/wf.sh` | light edit: same pipeline with a stage added or swapped | yes | 30810090 |
| Classics | oneliners | spell | `~/koala/oneliners/scripts/spell.sh` | `~/pash/evaluation/benchmarks/oneliners/spell.sh` | light edit: same pipeline with a stage added or swapped | yes | 30810090 |
| Classics | oneliners | diff | `~/koala/oneliners/scripts/diff.sh` | `~/pash/evaluation/benchmarks/oneliners/diff.sh` | same commands; input wiring or option spelling changed | yes | 30810090 |
| Classics | oneliners | bi-grams | `~/koala/oneliners/scripts/bi-grams.sh` | `~/pash/evaluation/benchmarks/oneliners/bi-grams.sh` | light edit: same pipeline with a stage added or swapped | yes | 30810090 |
| Classics | oneliners | set-diff | `~/koala/oneliners/scripts/set-diff.sh` | `~/pash/evaluation/benchmarks/oneliners/set-diff.sh` | same commands; input wiring or option spelling changed | yes | 30810090 |
| Classics | oneliners | sort-sort | `~/koala/oneliners/scripts/sort-sort.sh` | `~/pash/evaluation/benchmarks/oneliners/sort-sort.sh` | same | yes | 30810090 |
| – | oneliners | uniq-ips | `~/koala/oneliners/scripts/uniq-ips.sh` | – | new in Koala (no published original) | yes | 7096110 |
| – | oneliners | comm | `~/koala/oneliners/scripts/comm.sh` | – | new in Koala (no published original) | yes | 11432645 |
| – | oneliners | opt-parallel | `~/koala/oneliners/scripts/opt-parallel.sh` | – | new in Koala (no published original) | yes | 112699617 |
| Unix50 | unixfun | 1 | `~/koala/unixfun/scripts/1.sh` | `~/pash/evaluation/benchmarks/unix50/1.sh` | same | yes | 31450500 |
| Unix50 | unixfun | 2 | `~/koala/unixfun/scripts/2.sh` | `~/pash/evaluation/benchmarks/unix50/2.sh` | same | yes | 31450500 |
| Unix50 | unixfun | 3 | `~/koala/unixfun/scripts/3.sh` | `~/pash/evaluation/benchmarks/unix50/3.sh` | same | yes | 31450500 |
| Unix50 | unixfun | 4 | `~/koala/unixfun/scripts/4.sh` | `~/pash/evaluation/benchmarks/unix50/4.sh` | same | yes | 31450500 |
| Unix50 | unixfun | 5 | `~/koala/unixfun/scripts/5.sh` | `~/pash/evaluation/benchmarks/unix50/5.sh` | same | yes | 31435500 |
| Unix50 | unixfun | 6 | `~/koala/unixfun/scripts/6.sh` | `~/pash/evaluation/benchmarks/unix50/6.sh` | same | yes | 31456920 |
| Unix50 | unixfun | 7 | `~/koala/unixfun/scripts/7.sh` | `~/pash/evaluation/benchmarks/unix50/7.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 8 | `~/koala/unixfun/scripts/8.sh` | `~/pash/evaluation/benchmarks/unix50/8.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 9 | `~/koala/unixfun/scripts/9.sh` | `~/pash/evaluation/benchmarks/unix50/9.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 10 | `~/koala/unixfun/scripts/10.sh` | `~/pash/evaluation/benchmarks/unix50/10.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 11 | `~/koala/unixfun/scripts/11.sh` | `~/pash/evaluation/benchmarks/unix50/11.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 12 | `~/koala/unixfun/scripts/12.sh` | `~/pash/evaluation/benchmarks/unix50/12.sh` | same | yes | 31450200 |
| Unix50 | unixfun | 13 | `~/koala/unixfun/scripts/13.sh` | `~/pash/evaluation/benchmarks/unix50/13.sh` | same | yes | 31457250 |
| Unix50 | unixfun | 14 | `~/koala/unixfun/scripts/14.sh` | `~/pash/evaluation/benchmarks/unix50/14.sh` | same | yes | 31456590 |
| Unix50 | unixfun | 15 | `~/koala/unixfun/scripts/15.sh` | `~/pash/evaluation/benchmarks/unix50/15.sh` | same | yes | 31452780 |
| Unix50 | unixfun | 16 | `~/koala/unixfun/scripts/16.sh` | `~/pash/evaluation/benchmarks/unix50/16.sh` | same | yes | 31452780 |
| Unix50 | unixfun | 17 | `~/koala/unixfun/scripts/17.sh` | `~/pash/evaluation/benchmarks/unix50/17.sh` | same | yes | 31452780 |
| Unix50 | unixfun | 18 | `~/koala/unixfun/scripts/18.sh` | `~/pash/evaluation/benchmarks/unix50/18.sh` | same | yes | 30451500 |
| Unix50 | unixfun | 19 | `~/koala/unixfun/scripts/19.sh` | `~/pash/evaluation/benchmarks/unix50/19.sh` | same | yes | 30451500 |
| Unix50 | unixfun | 20 | `~/koala/unixfun/scripts/20.sh` | `~/pash/evaluation/benchmarks/unix50/20.sh` | same | yes | 30451500 |
| Unix50 | unixfun | 21 | `~/koala/unixfun/scripts/21.sh` | `~/pash/evaluation/benchmarks/unix50/21.sh` | same | yes | 30451500 |
| Unix50 | unixfun | 23 | `~/koala/unixfun/scripts/23.sh` | `~/pash/evaluation/benchmarks/unix50/23.sh` | same | yes | 31456080 |
| Unix50 | unixfun | 24 | `~/koala/unixfun/scripts/24.sh` | `~/pash/evaluation/benchmarks/unix50/24.sh` | same | yes | 31455600 |
| Unix50 | unixfun | 25 | `~/koala/unixfun/scripts/25.sh` | `~/pash/evaluation/benchmarks/unix50/25.sh` | same | yes | 31457160 |
| Unix50 | unixfun | 26 | `~/koala/unixfun/scripts/26.sh` | `~/pash/evaluation/benchmarks/unix50/26.sh` | same | yes | 31457250 |
| Unix50 | unixfun | 28 | `~/koala/unixfun/scripts/28.sh` | `~/pash/evaluation/benchmarks/unix50/28.sh` | same | yes | 31457280 |
| Unix50 | unixfun | 29 | `~/koala/unixfun/scripts/29.sh` | `~/pash/evaluation/benchmarks/unix50/29.sh` | same | yes | 31454130 |
| Unix50 | unixfun | 30 | `~/koala/unixfun/scripts/30.sh` | `~/pash/evaluation/benchmarks/unix50/30.sh` | same | yes | 31457250 |
| Unix50 | unixfun | 31 | `~/koala/unixfun/scripts/31.sh` | `~/pash/evaluation/benchmarks/unix50/31.sh` | same | yes | 31457250 |
| Unix50 | unixfun | 32 | `~/koala/unixfun/scripts/32.sh` | `~/pash/evaluation/benchmarks/unix50/32.sh` | same | yes | 31393080 |
| Unix50 | unixfun | 33 | `~/koala/unixfun/scripts/33.sh` | `~/pash/evaluation/benchmarks/unix50/33.sh` | same | yes | 31393080 |
| Unix50 | unixfun | 34 | `~/koala/unixfun/scripts/34.sh` | `~/pash/evaluation/benchmarks/unix50/34.sh` | same | yes | 31393080 |
| Unix50 | unixfun | 35 | `~/koala/unixfun/scripts/35.sh` | `~/pash/evaluation/benchmarks/unix50/35.sh` | same | yes | 31425810 |
| Unix50 | unixfun | 36 | `~/koala/unixfun/scripts/36.sh` | `~/pash/evaluation/benchmarks/unix50/36.sh` | same | yes | 31425810 |
| COVID-mts | covid | 1 | `~/koala/covid/scripts/1.sh` | `~/pash/evaluation/benchmarks/analytics-mts/1.sh` | same commands; input wiring or option spelling changed | yes | 3589542298 |
| COVID-mts | covid | 2 | `~/koala/covid/scripts/2.sh` | `~/pash/evaluation/benchmarks/analytics-mts/2.sh` | same commands; input wiring or option spelling changed | yes | 3589542298 |
| COVID-mts | covid | 3 | `~/koala/covid/scripts/3.sh` | `~/pash/evaluation/benchmarks/analytics-mts/3.sh` | same commands; input wiring or option spelling changed | yes | 3589542298 |
| COVID-mts | covid | 4 | `~/koala/covid/scripts/4.sh` | `~/pash/evaluation/benchmarks/analytics-mts/4.sh` | same commands; input wiring or option spelling changed | yes | 3589542298 |
| COVID-mts | covid | 5 | `~/koala/covid/scripts/5.sh` | `~/pash/evaluation/benchmarks/analytics-mts/5.sh` | same commands; input wiring or option spelling changed | yes | 3589542298 |
| NLP | nlp | syllable_words_1 | `~/koala/nlp/scripts/syllable_words_1.sh` | `~/pash/evaluation/benchmarks/nlp/6_4.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | syllable_words_2 | `~/koala/nlp/scripts/syllable_words_2.sh` | `~/pash/evaluation/benchmarks/nlp/6_5.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | letter_words | `~/koala/nlp/scripts/letter_words.sh` | `~/pash/evaluation/benchmarks/nlp/6_2.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | bigrams_appear_twice | `~/koala/nlp/scripts/bigrams_appear_twice.sh` | `~/pash/evaluation/benchmarks/nlp/8.2_2.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | bigrams | `~/koala/nlp/scripts/bigrams.sh` | `~/pash/evaluation/benchmarks/nlp/4_3.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | compare_exodus_genesis | `~/koala/nlp/scripts/compare_exodus_genesis.sh` | `~/pash/evaluation/benchmarks/nlp/8.3_3.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | count_consonant_seq | `~/koala/nlp/scripts/count_consonant_seq.sh` | `~/pash/evaluation/benchmarks/nlp/7_2.sh` | same commands; input wiring or option spelling changed | yes | 1118570034 |
| NLP | nlp | count_morphs | `~/koala/nlp/scripts/count_morphs.sh` | `~/pash/evaluation/benchmarks/nlp/7_1.sh` | same commands; input wiring or option spelling changed | yes | 1118570034 |
| NLP | nlp | count_trigrams | `~/koala/nlp/scripts/count_trigrams.sh` | `~/pash/evaluation/benchmarks/nlp/4_3b.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | count_vowel_seq | `~/koala/nlp/scripts/count_vowel_seq.sh` | `~/pash/evaluation/benchmarks/nlp/2_2.sh` | same commands; input wiring or option spelling changed | yes | 1118570034 |
| NLP | nlp | count_words | `~/koala/nlp/scripts/count_words.sh` | `~/pash/evaluation/benchmarks/nlp/1_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | find_anagrams | `~/koala/nlp/scripts/find_anagrams.sh` | `~/pash/evaluation/benchmarks/nlp/8.3_2.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | merge_upper | `~/koala/nlp/scripts/merge_upper.sh` | `~/pash/evaluation/benchmarks/nlp/2_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | sort | `~/koala/nlp/scripts/sort.sh` | `~/pash/evaluation/benchmarks/nlp/3_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | sort_words_by_folding | `~/koala/nlp/scripts/sort_words_by_folding.sh` | `~/pash/evaluation/benchmarks/nlp/3_2.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | sort_words_by_num_of_syllables | `~/koala/nlp/scripts/sort_words_by_num_of_syllables.sh` | `~/pash/evaluation/benchmarks/nlp/8_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | sort_words_by_rhyming | `~/koala/nlp/scripts/sort_words_by_rhyming.sh` | `~/pash/evaluation/benchmarks/nlp/3_3.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | trigram_rec | `~/koala/nlp/scripts/trigram_rec.sh` | `~/pash/evaluation/benchmarks/nlp/6_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | uppercase_by_token | `~/koala/nlp/scripts/uppercase_by_token.sh` | `~/pash/evaluation/benchmarks/nlp/6_1_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | uppercase_by_type | `~/koala/nlp/scripts/uppercase_by_type.sh` | `~/pash/evaluation/benchmarks/nlp/6_1_2.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | verses_2om_3om_2instances | `~/koala/nlp/scripts/verses_2om_3om_2instances.sh` | `~/pash/evaluation/benchmarks/nlp/6_7.sh` | same commands; input wiring or option spelling changed | yes | 1118570034 |
| NLP | nlp | vowel_sequencies_gr_1K | `~/koala/nlp/scripts/vowel_sequencies_gr_1K.sh` | `~/pash/evaluation/benchmarks/nlp/8.2_1.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| NLP | nlp | words_no_vowels | `~/koala/nlp/scripts/words_no_vowels.sh` | `~/pash/evaluation/benchmarks/nlp/6_3.sh` | light edit: same pipeline with a stage added or swapped | yes | 1118570034 |
| AvgTemp | weather | max-temp | `~/koala/weather/scripts/temp-analytics.sh` | `~/pash/evaluation/benchmarks/max-temp/temp-analytics.sh` | same analysis; the download step (curl, gunzip) removed, input is a prepared file | no | – |
| – | weather | tuft-weather | `~/koala/weather/scripts/tuft-weather.sh` | – | new in Koala (no published original) | yes | 936125600 |
| WebIndex | web-search | web-index | `~/koala/web-search/scripts/engine.sh` | `~/pash/evaluation/benchmarks/web-index/web-index.sh` | rewritten: a crawl-and-index loop with Node.js helpers instead of one pipeline | no | – |
| FileEnc | file-mod | compress_files | `~/koala/file-mod/scripts/compress_files.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/compress_files.sh` | rewritten: gzip from standard input instead of zip on a file | yes | 1368377609 |
| FileEnc | file-mod | encrypt_files | `~/koala/file-mod/scripts/encrypt_files.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/encrypt_files.sh` | same tool and settings; reads standard input instead of a named file | yes | 1368377609 |
| MediaConv | file-mod | img_convert | `~/koala/file-mod/scripts/img_convert.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/img_convert.sh` | same tool and settings; reads standard input instead of a named file | yes | 815602884 |
| MediaConv | file-mod | to_mp3 | `~/koala/file-mod/scripts/to_mp3.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/to_mp3.sh` | same tool and settings; reads standard input instead of a named file | yes | 188528880 |
| – | file-mod | thumbnail_generation | `~/koala/file-mod/scripts/thumbnail_generation.sh` | – | new in Koala (no published original) | yes | 815602884 |
| AurPkg | pkg | pacaur | `~/koala/pkg/scripts/pacaur.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/pacaur.sh` | same idea (fetch build file, build with makedeb); fetch source moved to Koala server, adds key fetch | no | – |
| ProgInf | pkg | proginf | `~/koala/pkg/scripts/proginf.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/proginf.sh` | same tool (mir-sa); package list now read from an index file | no | – |
| LogAnalysis | analytics | nginx | `~/koala/analytics/scripts/nginx.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/nginx.sh` | same pipelines; log now read from standard input through a temporary file | yes | 127701176 |
| LogAnalysis | analytics | pcaps | `~/koala/analytics/scripts/pcaps.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/pcap.sh` | same pipelines plus one more tcpdump query; capture read from standard input | yes | 1368377609 |
| – | analytics | port-scan | `~/koala/analytics/scripts/port-scan.sh` | – | new in Koala (no published original) | no | – |
| – | analytics | ray-tracing | `~/koala/analytics/scripts/ray-tracing.sh` | – | new in Koala (no published original) | yes | 63953451 |
| Genomics | bio | bio | `~/koala/bio/scripts/bio.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/genomics.sh` | same samtools steps; restructured loop, system samtools instead of a bundled one | yes | 1027186 |
| – | bio | data | `~/koala/bio/scripts/data.sh` | – | new in Koala (TERA-Seq reference preparation) | no | – |
| – | bio | run_dRNASeq | `~/koala/bio/scripts/run_dRNASeq.sh` | – | new in Koala (TERA-Seq) | no | – |
| – | bio | run_5TERA | `~/koala/bio/scripts/run_5TERA.sh` | – | new in Koala (TERA-Seq) | no | – |

## Appendix A3: why parts were not run in parallel

Distinct parts. Each cell: the same under PaSh's own files / only with this source.

| Reason | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced |
|---|---:|---:|---:|
| missing annotation | 95 / 0 | 64 / 0 | 64 / 0 |
| other: not classified | 9 / 0 | 5 / 0 | 5 / 0 |
| other: nothing in this part can be split under this source's files | 1 / 0 | 0 / 0 | 0 / 0 |
| other: the source has files for a command, but they gave no answer | 0 / 0 | 0 / 15 | 0 / 14 |
| pash crash | 4 / 0 | 1 / 10 | 1 / 2 |
| refused by annotation | 0 / 0 | 0 / 24 | 0 / 24 |
| unsupported construct | 27 / 0 | 26 / 3 | 24 / 3 |
| parts considered | 177 | 177 | 177 |

Per execution (a loop's part counts once per pass). Each cell: the same under PaSh's own files / only with this source.

| Reason | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced |
|---|---:|---:|---:|
| missing annotation | 95 / 0 | 64 / 0 | 64 / 0 |
| other | 10 / 0 | 9 / 11 | 9 / 10 |
| pash crash | 4 / 0 | 1 / 10 | 1 / 2 |
| refused by annotation | 0 / 0 | 0 / 24 | 0 / 24 |
| unsupported construct | 27 / 0 | 26 / 3 | 24 / 3 |
| parts considered | 177 | 177 | 177 |

## Appendix A4: every use whose result differs from PaSh's own

| Script | Command line | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced | Output same as bash |
|---|---|---|---|---|---|
| covid/1 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `sed '"s/T..:..:..//"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `cut -d '","' -f 1,3` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `sort -u` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `cut -d '","' -f 1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/1 | `awk '"{print $2,$1}"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `sed '"s/T..:..:..//"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `cut -d '","' -f 3,1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `sort -u` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `cut -d '","' -f 2` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `sort -k 1 -n` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/2 | `awk '"{print $2,$1}"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `sed '"s/T\(..\):..:../,\1/"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `cut -d '","' -f 1,2,4` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `sort -u` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `cut -d '","' -f 3` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `sort -k 1 -n` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/3 | `awk '"{print $2,$1}"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `sed '"s/T\(..\):..:../,\1/"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `cut -d '","' -f 1,2` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `sort -u` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `cut -d '","' -f 1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| covid/4 | `awk '"{print $2,$1}"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/bigrams | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/bigrams_appear_twice | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/compare_exodus_genesis | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/count_consonant_seq | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/count_morphs | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/count_trigrams | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/count_vowel_seq | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/count_words | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/find_anagrams | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/letter_words | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/merge_upper | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/sort | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/sort_words_by_folding | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/sort_words_by_num_of_syllables | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/sort_words_by_rhyming | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/syllable_words_1 | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/syllable_words_2 | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/trigram_rec | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/uppercase_by_token | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/uppercase_by_type | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/verses_2om_3om_2instances | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/vowel_sequencies_gr_1K | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| nlp/words_no_vowels | `echo '"done"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/nfa-regex | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort-sort | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort-sort | `tr A-Z a-z` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort-sort | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/sort-sort | `sort -r` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/spell | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `sed '"s/[^[:print:]]//g"'` | split | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `col -bx` | split | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `tr -cs A-Za-z '"\n"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `tr A-Z a-z` | split | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `tr -d '"[:punct:]"'` | split | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `uniq` | whole | split | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/spell | `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: yes |
| oneliners/top-n | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `tr -c '"A-Za-z"' '"[\n*]"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `grep -v '"^\s*$"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `tr A-Z a-z` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `sort -rn` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/top-n | `sed 100q` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| oneliners/uniq-ips | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/uniq-ips | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/uniq-ips | `uniq` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `tr -c '"A-Za-z"' '"[\n*]"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `grep -v '"^\s*$"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `tr A-Z a-z` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| oneliners/wf | `sort -rn` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/1 | `cat ./inputs/1_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `cat ./inputs/4_30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `tr '" "' '"\n"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `grep '"x"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `grep '"\."'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `cut -d '"."' -f 2` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `grep '"[KQRBN]"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `cut -c 1-1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/10 | `sort -nr` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `cat ./inputs/4_30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `tr '" "' '"\n"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `grep '"x"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `grep '"\."'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `cut -d '"."' -f 2` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `cut -c 1-1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `tr '"[a-z]"' '"P"'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/11 | `sort -nr` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/13 | `cat ./inputs/5_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/14 | `cat ./inputs/6_30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/14 | `awk '"{print $2, $0}"'` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/14 | `sort -nr` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/14 | `cut -d '" "' -f 2` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/15 | `cat ./inputs/7_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/17 | `cat ./inputs/7_30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/17 | `cut -f 4` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/17 | `sort -n` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/17 | `cut -c 3-3` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/17 | `uniq` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/17 | `sed 's/$/"0s"/'` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: **no** |
| unixfun/18 | `cat ./inputs/8_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/19 | `cat ./inputs/8_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/2 | `cat ./inputs/1_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/2 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/20 | `cat ./inputs/8_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/21 | `cat ./inputs/8_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/21 | `tr -c '"[a-z][A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/21 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/23 | `cat ./inputs/9.1_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/23 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/24 | `cat ./inputs/9.2_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/24 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/25 | `cat ./inputs/9.3_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/25 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/26 | `cat ./inputs/9.4_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/26 | `sed 4d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/26 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `cat ./inputs/9.6_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `sed 3d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `sed 3d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `sed 3d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `tr -c '"[A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/28 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/29 | `cat ./inputs/9.7_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/29 | `sed 2d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/29 | `sed 2d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/29 | `tr -c '"[A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/29 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/3 | `cat ./inputs/1_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/30 | `cat ./inputs/9.8_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `tr -c '"[a-z][A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `sed 2d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `sed 3d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `sed 4d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `tr -c '"[A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/30 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `cat ./inputs/9.9_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `tr -c '"[a-z][A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `sed 2d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `sed 3d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `sed 5d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `tr -c '"[A-Z]"' '"\n"'` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/31 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/32 | `cat ./inputs/10_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/32 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/33 | `cat ./inputs/10_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/33 | `sed 1d` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): **no**, Caruca, full grammar where traced: **no** |
| unixfun/35 | `cat ./inputs/11_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/4 | `cat ./inputs/1_30M.txt` | whole | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/4 | `cut -d '" "' -f 1` | split | whole | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/4 | `sort` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/4 | `uniq -c` | whole | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/4 | `sort -r` | split | whole | whole | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/5 | `cat ./inputs/2_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/6 | `cat ./inputs/3_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/6 | `tr -d '"\n"'` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/7 | `cat ./inputs/4_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/8 | `cat ./inputs/4_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |
| unixfun/9 | `cat ./inputs/4_30M.txt` | whole | split | split | Caruca's files, PaSh grammar (all converted commands): yes, Caruca, full grammar where traced: yes |

Why the use was left whole, where it was:

- covid/1 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/1 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `sed '"s/T..:..:..//"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `cut -d '","' -f 1,3`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `sort -u`, PaSh's own files: file says no split
- covid/1 `sort -u`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `sort -u`, Caruca, full grammar where traced: file says no split
- covid/1 `cut -d '","' -f 1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `sort`, Caruca, full grammar where traced: file says no split
- covid/1 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/1 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `uniq -c`, Caruca, full grammar where traced: file says no split
- covid/1 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/1 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/1 `awk '"{print $2,$1}"'`, Caruca, full grammar where traced: file says no split
- covid/2 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/2 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sed '"s/T..:..:..//"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `cut -d '","' -f 3,1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sort -u`, PaSh's own files: file says no split
- covid/2 `sort -u`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sort -u`, Caruca, full grammar where traced: file says no split
- covid/2 `cut -d '","' -f 2`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sort`, Caruca, full grammar where traced: file says no split
- covid/2 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/2 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `uniq -c`, Caruca, full grammar where traced: file says no split
- covid/2 `sort -k 1 -n`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `sort -k 1 -n`, Caruca, full grammar where traced: file says no split
- covid/2 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/2 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/2 `awk '"{print $2,$1}"'`, Caruca, full grammar where traced: file says no split
- covid/3 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/3 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sed '"s/T\(..\):..:../,\1/"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `cut -d '","' -f 1,2,4`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sort -u`, PaSh's own files: file says no split
- covid/3 `sort -u`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sort -u`, Caruca, full grammar where traced: file says no split
- covid/3 `cut -d '","' -f 3`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sort`, Caruca, full grammar where traced: file says no split
- covid/3 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/3 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `uniq -c`, Caruca, full grammar where traced: file says no split
- covid/3 `sort -k 1 -n`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `sort -k 1 -n`, Caruca, full grammar where traced: file says no split
- covid/3 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/3 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/3 `awk '"{print $2,$1}"'`, Caruca, full grammar where traced: file says no split
- covid/4 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/4 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `sed '"s/T\(..\):..:../,\1/"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `cut -d '","' -f 1,2`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `sort -u`, PaSh's own files: file says no split
- covid/4 `sort -u`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `sort -u`, Caruca, full grammar where traced: file says no split
- covid/4 `cut -d '","' -f 1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `sort`, Caruca, full grammar where traced: file says no split
- covid/4 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/4 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `uniq -c`, Caruca, full grammar where traced: file says no split
- covid/4 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/4 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- covid/4 `awk '"{print $2,$1}"'`, Caruca, full grammar where traced: file says no split
- nlp/bigrams `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/bigrams `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/bigrams `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/bigrams_appear_twice `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/bigrams_appear_twice `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/bigrams_appear_twice `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/compare_exodus_genesis `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/compare_exodus_genesis `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/compare_exodus_genesis `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/count_consonant_seq `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/count_consonant_seq `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/count_consonant_seq `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/count_morphs `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/count_morphs `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/count_morphs `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/count_trigrams `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/count_trigrams `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/count_trigrams `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/count_vowel_seq `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/count_vowel_seq `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/count_vowel_seq `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/count_words `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/count_words `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/count_words `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/find_anagrams `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/find_anagrams `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/find_anagrams `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/letter_words `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/letter_words `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/letter_words `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/merge_upper `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/merge_upper `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/merge_upper `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/sort `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/sort `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/sort `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/sort_words_by_folding `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/sort_words_by_folding `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/sort_words_by_folding `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/sort_words_by_num_of_syllables `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/sort_words_by_num_of_syllables `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/sort_words_by_num_of_syllables `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/sort_words_by_rhyming `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/sort_words_by_rhyming `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/sort_words_by_rhyming `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/syllable_words_1 `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/syllable_words_1 `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/syllable_words_1 `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/syllable_words_2 `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/syllable_words_2 `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/syllable_words_2 `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/trigram_rec `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/trigram_rec `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/trigram_rec `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/uppercase_by_token `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/uppercase_by_token `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/uppercase_by_token `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/uppercase_by_type `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/uppercase_by_type `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/uppercase_by_type `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/verses_2om_3om_2instances `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/verses_2om_3om_2instances `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/verses_2om_3om_2instances `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/vowel_sequencies_gr_1K `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/vowel_sequencies_gr_1K `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/vowel_sequencies_gr_1K `echo '"done"'`, Caruca, full grammar where traced: file says no split
- nlp/words_no_vowels `echo '"done"'`, PaSh's own files: part not run in parallel
- nlp/words_no_vowels `echo '"done"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- nlp/words_no_vowels `echo '"done"'`, Caruca, full grammar where traced: file says no split
- oneliners/nfa-regex `cat ~/t024/shadow/oneliners/inputs/10M.txt`, PaSh's own files: no answer
- oneliners/sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/sort `sort`, Caruca's files, PaSh grammar (all converted commands): file says no split
- oneliners/sort `sort`, Caruca, full grammar where traced: file says no split
- oneliners/sort-sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/sort-sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/sort-sort `tr A-Z a-z`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/sort-sort `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/sort-sort `sort`, Caruca, full grammar where traced: file says no split
- oneliners/sort-sort `sort -r`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/sort-sort `sort -r`, Caruca, full grammar where traced: file says no split
- oneliners/spell `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/spell `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `sed '"s/[^[:print:]]//g"'`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `col -bx`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `tr -cs A-Za-z '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/spell `tr -cs A-Za-z '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- oneliners/spell `tr -cs A-Za-z '"\n"'`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `tr A-Z a-z`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `tr -d '"[:punct:]"'`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `sort`, Caruca's files, PaSh grammar (all converted commands): file says no split
- oneliners/spell `sort`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `uniq`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/spell `uniq`, Caruca, full grammar where traced: part not run in parallel
- oneliners/spell `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt`, PaSh's own files: no answer
- oneliners/spell `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt`, Caruca's files, PaSh grammar (all converted commands): file says no split
- oneliners/spell `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt`, Caruca, full grammar where traced: part not run in parallel
- oneliners/top-n `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/top-n `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca, full grammar where traced: file says no split
- oneliners/top-n `grep -v '"^\s*$"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `tr A-Z a-z`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `sort`, Caruca, full grammar where traced: file says no split
- oneliners/top-n `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/top-n `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `uniq -c`, Caruca, full grammar where traced: file says no split
- oneliners/top-n `sort -rn`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/top-n `sort -rn`, Caruca, full grammar where traced: file says no split
- oneliners/top-n `sed 100q`, PaSh's own files: file says no split
- oneliners/top-n `sed 100q`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/uniq-ips `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'`, PaSh's own files: no answer
- oneliners/uniq-ips `sort`, Caruca's files, PaSh grammar (all converted commands): file says no split
- oneliners/uniq-ips `sort`, Caruca, full grammar where traced: file says no split
- oneliners/uniq-ips `uniq`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/wf `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/wf `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca, full grammar where traced: file says no split
- oneliners/wf `grep -v '"^\s*$"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `tr A-Z a-z`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `sort`, Caruca, full grammar where traced: file says no split
- oneliners/wf `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/wf `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `uniq -c`, Caruca, full grammar where traced: file says no split
- oneliners/wf `sort -rn`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- oneliners/wf `sort -rn`, Caruca, full grammar where traced: file says no split
- unixfun/1 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/10 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/10 `cat ./inputs/4_30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `tr '" "' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `grep '"x"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `grep '"\."'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `cut -d '"."' -f 2`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `grep '"[KQRBN]"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `cut -c 1-1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `sort`, Caruca, full grammar where traced: file says no split
- unixfun/10 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/10 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `uniq -c`, Caruca, full grammar where traced: file says no split
- unixfun/10 `sort -nr`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/10 `sort -nr`, Caruca, full grammar where traced: file says no split
- unixfun/11 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/11 `cat ./inputs/4_30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `tr '" "' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `grep '"x"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `grep '"\."'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `cut -d '"."' -f 2`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `cut -c 1-1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `tr '"[a-z]"' '"P"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `sort`, Caruca, full grammar where traced: file says no split
- unixfun/11 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/11 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `uniq -c`, Caruca, full grammar where traced: file says no split
- unixfun/11 `sort -nr`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/11 `sort -nr`, Caruca, full grammar where traced: file says no split
- unixfun/13 `cat ./inputs/5_30M.txt`, PaSh's own files: no answer
- unixfun/14 `cat ./inputs/6_30M.txt`, PaSh's own files: no answer
- unixfun/14 `cat ./inputs/6_30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/14 `awk '"{print $2, $0}"'`, PaSh's own files: no answer
- unixfun/14 `awk '"{print $2, $0}"'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/14 `awk '"{print $2, $0}"'`, Caruca, full grammar where traced: file says no split
- unixfun/14 `sort -nr`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/14 `sort -nr`, Caruca, full grammar where traced: file says no split
- unixfun/14 `cut -d '" "' -f 2`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/15 `cat ./inputs/7_30M.txt`, PaSh's own files: no answer
- unixfun/17 `cat ./inputs/7_30M.txt`, PaSh's own files: no answer
- unixfun/17 `cat ./inputs/7_30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/17 `cut -f 4`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/17 `sort -n`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/17 `sort -n`, Caruca, full grammar where traced: file says no split
- unixfun/17 `cut -c 3-3`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/17 `uniq`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/17 `uniq`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/17 `sed 's/$/"0s"/'`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/18 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/19 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/2 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/2 `sort`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/2 `sort`, Caruca, full grammar where traced: file says no split
- unixfun/20 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/21 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/21 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/21 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/21 `sort`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/21 `sort`, Caruca, full grammar where traced: file says no split
- unixfun/23 `cat ./inputs/9.1_30M.txt`, PaSh's own files: no answer
- unixfun/23 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/24 `cat ./inputs/9.2_30M.txt`, PaSh's own files: no answer
- unixfun/24 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/25 `cat ./inputs/9.3_30M.txt`, PaSh's own files: no answer
- unixfun/25 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/26 `cat ./inputs/9.4_30M.txt`, PaSh's own files: no answer
- unixfun/26 `sed 4d`, PaSh's own files: file says no split
- unixfun/26 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/28 `cat ./inputs/9.6_30M.txt`, PaSh's own files: no answer
- unixfun/28 `sed 1d`, PaSh's own files: file says no split
- unixfun/28 `sed 3d`, PaSh's own files: file says no split
- unixfun/28 `sed 3d`, PaSh's own files: file says no split
- unixfun/28 `sed 3d`, PaSh's own files: file says no split
- unixfun/28 `tr -c '"[A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/28 `tr -c '"[A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/28 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/29 `cat ./inputs/9.7_30M.txt`, PaSh's own files: no answer
- unixfun/29 `sed 2d`, PaSh's own files: file says no split
- unixfun/29 `sed 2d`, PaSh's own files: file says no split
- unixfun/29 `tr -c '"[A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/29 `tr -c '"[A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/29 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/3 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/30 `cat ./inputs/9.8_30M.txt`, PaSh's own files: no answer
- unixfun/30 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/30 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/30 `sed 1d`, PaSh's own files: file says no split
- unixfun/30 `sed 2d`, PaSh's own files: file says no split
- unixfun/30 `sed 3d`, PaSh's own files: file says no split
- unixfun/30 `sed 4d`, PaSh's own files: file says no split
- unixfun/30 `tr -c '"[A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/30 `tr -c '"[A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/30 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/31 `cat ./inputs/9.9_30M.txt`, PaSh's own files: no answer
- unixfun/31 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/31 `tr -c '"[a-z][A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/31 `sed 1d`, PaSh's own files: file says no split
- unixfun/31 `sed 1d`, PaSh's own files: file says no split
- unixfun/31 `sed 2d`, PaSh's own files: file says no split
- unixfun/31 `sed 3d`, PaSh's own files: file says no split
- unixfun/31 `sed 5d`, PaSh's own files: file says no split
- unixfun/31 `tr -c '"[A-Z]"' '"\n"'`, Caruca's files, PaSh grammar (all converted commands): file says no split
- unixfun/31 `tr -c '"[A-Z]"' '"\n"'`, Caruca, full grammar where traced: file says no split
- unixfun/31 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/32 `cat ./inputs/10_30M.txt`, PaSh's own files: no answer
- unixfun/32 `sed 1d`, PaSh's own files: file says no split
- unixfun/33 `cat ./inputs/10_30M.txt`, PaSh's own files: no answer
- unixfun/33 `sed 1d`, PaSh's own files: file says no split
- unixfun/35 `cat ./inputs/11_30M.txt`, PaSh's own files: no answer
- unixfun/4 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/4 `cat ./inputs/1_30M.txt`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/4 `cut -d '" "' -f 1`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/4 `sort`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/4 `sort`, Caruca, full grammar where traced: file says no split
- unixfun/4 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/4 `uniq -c`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/4 `uniq -c`, Caruca, full grammar where traced: file says no split
- unixfun/4 `sort -r`, Caruca's files, PaSh grammar (all converted commands): part not run in parallel
- unixfun/4 `sort -r`, Caruca, full grammar where traced: file says no split
- unixfun/5 `cat ./inputs/2_30M.txt`, PaSh's own files: no answer
- unixfun/6 `cat ./inputs/3_30M.txt`, PaSh's own files: no answer
- unixfun/6 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/7 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/8 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/9 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer

The files' answers on each command line the source has its own files for:

| Source | Command line | Same inputs and outputs | Source's answer | PaSh's own answer |
|---|---|---|---|---|
| Caruca's files, PaSh grammar (all converted commands) | `awk '"$1 >= 1000"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"length <= 45"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"length >= 16"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{
        key = sprintf("%s", $1);
        count[key]++;
        sum[key] += $3;
        sum_sq[key] += $3 * $3;
        if (!(key in max) || $3 > max[key]) max[key] = $3;
        if (!(key in min) || $3 < min[key]) min[key] = $3;
    } 
    END {
        for (key in max) {
            mean = sum[key] / count[key];
            variance = (sum_sq[key] / count[key]) - (mean * mean);
            stddev = (variance > 0) ? sqrt(variance) : 0;
            confidence_delta = 1.96 * stddev / sqrt(count[key]);
            normal_range_low = mean - confidence_delta;
            normal_range_high = mean + confidence_delta;
            printf "%s %s %s %.2f %.2f\n", key, min[key], max[key], normal_range_low, normal_range_high;
        }
    }"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{ printf "%02d-%02d %s %s\n", $1, $2, $3, $4 }"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{ total += $1; count++ } END { print total/count }"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{$1=$1};1"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{print $2, $0}"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk '"{print $2,$1}"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk -F '"\t"' '"{print $6}"' '"~/t024/shadow/weather/inputs/tuft_weather.small.txt"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `awk -F, '"
!seen[$1 $2 $4] { seen[$1 $2 $4] = 1; hours[$1 $4]++; bus[$4] = 1; day[$1] = 1; }
END {
   PROCINFO["sorted_in"] = "@ind_str_asc"
   for (d in day)
     printf("\t%s", d);
   printf("\n");
   for (b in bus) {
     printf("%s", b);
     for (d in day)
       printf("\t%s", hours[d b]);
     printf("\n");
   }
}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"${OUT}/urls.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"${OUT}/visited.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"${formatted}"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"${input}"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small"/*.INFO'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small/1.INFO"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/analytics/outputs/ray_tracing_small/rays.csv"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/file-mod/inputs/jpg_small/jpg/119901.jpg"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '"~/t024/shadow/weather/inputs/temperatures.small.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat '~/t024/shadow/file-mod/inputs/wav_small/file_example_WAV_5MG.wav.~9~'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/10_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/11_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/5_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ./inputs/9.9_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat inputs/bio-min/input_min.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/analytics/inputs/nginx-logs_small/log7` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/analytics/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/file-mod/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/nlp/inputs/pg-small/ynkgt10.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `col -bx` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `comm '"~/t024/shadow/oneliners/inputs/comm_small/file1"' '"~/t024/shadow/oneliners/inputs/comm_small/file2"'` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `comm -12 '"${yr_txt}"' -` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `comm -23 s1 s2` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `cut '-d" "' -f1,2 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut '-d" "' -f1,3` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut '-d" "' -f1,3 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut '-d" "' -f2` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 1-1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 1-12` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 1-2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 1-4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 3-3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 7-` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -c 89-92` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '" "' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '" "' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '" "' -f 4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '"""' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '"("' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '")"' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 1,2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 1,2,4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 1,3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '","' -f 3,1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -d '"."' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -f 1 -d '" "'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -f 2 ./Gene_locs.txt` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `cut -f 4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `diff -B s1 s2` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"Indexing Sample "${pop}"_"${OUT}/${sample}" "'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"Isolating Chromosome "${chr}" from sample "${OUT}/${sample}",  "'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"Processing Sample ${sample}"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"[engine] crawling 0/0/6/Image~0069.JPG_c66f.html"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"[engine] indexing 0/0/6/Image~0069.JPG_c66f.html"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '"done"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `echo '${s_line}'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `ffmpeg -y -i pipe:0 -f mp3 -ab 192000 pipe:1` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `find ~/t024/shadow/oneliners/inputs/chessdata_small -type f -name '"*.pgn"' -print0` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `fmt -w1` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `grep '" ${year}"' '"${formatted}"'` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"""'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"${city}"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"("'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"AT&T"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"And he said"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"Bell"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"UNIX"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"\."'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"\[RAY\]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"light.\*light"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"print"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"the land of"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep '"x"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -c '"^....$"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -c '"^[A-Z]"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -c '"light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -c '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*$"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]$"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v '"NA"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v '"\-99"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v '"^\s*$"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v 999` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -v pathID` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -vc '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `grep -vi '"[aeiou]"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `grep 1969` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `head -n 1` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `head -n 2` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `head -n 3` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `head -n1` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `head -n1 '"${formatted}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `join -1 1 -2 1 -e '"NA"' '"${processed}"' '"${j2}"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `join -a1 -a2 -e '"-99"' -o '"0,1.2,1.3,2.2"' '"${j1}"' '"${max_y}"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `join -a1 -a2 -e '"-99"' -o '"0,1.2,2.2"' '"${yr_txt}"' '"${min_y}"'` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `mkfifo s1 s2` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `read -r city` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `read -r url` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `read chr` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `read s_line` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `rev` | – | says no split | no files |
| Caruca's files, PaSh grammar (all converted commands) | `rm -f '"${yr_txt}"' '"${max_y}"' '"${min_y}"' '"${j1}"' '"${j2}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `rm s1 s2` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/ .*//g"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/-99/NaN/g"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/T..:..:..//"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/T\(..\):..:../,\1/"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/T\(..\):..:../,\1/"' '"~/t024/shadow/covid/inputs/in_small.csv"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/[^[:print:]]//g"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed '"s/ly$/-ly/g"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 's/$/"0s"/'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed -e '"s/SN:\([0-9XY]\)/SN:chr\1/"' -e '"s/SN:MT/SN:chrM/"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed -e '"s|^\./||"' '"~/t024/shadow/web-search/inputs/index_min.txt"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed -n '"/^590432,/p"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 100q` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 1d` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 2d` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 3d` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 4d` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 5d` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `sed 5q` | yes | allows a split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `seq '"${START_YEAR}"' '"${END_YEAR}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `sort` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -f` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -k 1 -n` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -n` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -nr` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -r` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -rn` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `sort -u` | **no** | says no split | says no split |
| Caruca's files, PaSh grammar (all converted commands) | `tail -n 1` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `tail -n1 '"${formatted}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `tr '" "' '"\n"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '" /"' '"__"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[:lower:]"' '"[:upper:]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[:upper:]"' '"[:lower:]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[A-Z]"' '"[a-z]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[a-z]"' '"P"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[a-z]"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"[a-z]"' '"\n"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr '"a-z"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -c '"A-Za-z"' '"[\n*]"'` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -c '"[A-Z]"' '"\n"'` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -c '"[a-z][A-Z]"' '"\n"'` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -cs A-Za-z '"\n"'` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr -d '","'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -d '"[:punct:]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `tr -d '"\n"'` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr -s '" "' '"\n"'` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr -sc '"AEIOU"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr -sc '"AEIOUaeiou"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr -sc '"BCDFGHJKLMNPQRSTVWXYZ"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `tr A-Z a-z` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar (all converted commands) | `uniq` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `uniq -c` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar (all converted commands) | `wc -l` | yes | says no split | no answer |
| Caruca's files, PaSh grammar (all converted commands) | `xargs -0 -n4 -P4 mawk '"/Result/ { split($0, a, "-"); res = substr(a[1], length(a[1]), 1); if (res == 1) white++; if (res == 0) black++; if (res == 2) draw++ } END { print white+black+draw, white, black, draw }"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `awk '"$1 >= 1000"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"length <= 45"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"length >= 16"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{
        key = sprintf("%s", $1);
        count[key]++;
        sum[key] += $3;
        sum_sq[key] += $3 * $3;
        if (!(key in max) || $3 > max[key]) max[key] = $3;
        if (!(key in min) || $3 < min[key]) min[key] = $3;
    } 
    END {
        for (key in max) {
            mean = sum[key] / count[key];
            variance = (sum_sq[key] / count[key]) - (mean * mean);
            stddev = (variance > 0) ? sqrt(variance) : 0;
            confidence_delta = 1.96 * stddev / sqrt(count[key]);
            normal_range_low = mean - confidence_delta;
            normal_range_high = mean + confidence_delta;
            printf "%s %s %s %.2f %.2f\n", key, min[key], max[key], normal_range_low, normal_range_high;
        }
    }"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{ printf "%02d-%02d %s %s\n", $1, $2, $3, $4 }"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{ total += $1; count++ } END { print total/count }"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{$1=$1};1"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{print $2, $0}"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk '"{print $2,$1}"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `awk -F '"\t"' '"{print $6}"' '"~/t024/shadow/weather/inputs/tuft_weather.small.txt"'` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `awk -F, '"
!seen[$1 $2 $4] { seen[$1 $2 $4] = 1; hours[$1 $4]++; bus[$4] = 1; day[$1] = 1; }
END {
   PROCINFO["sorted_in"] = "@ind_str_asc"
   for (d in day)
     printf("\t%s", d);
   printf("\n");
   for (b in bus) {
     printf("%s", b);
     for (d in day)
       printf("\t%s", hours[d b]);
     printf("\n");
   }
}"'` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `cat '"${OUT}/urls.txt"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"${OUT}/visited.txt"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"${formatted}"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"${input}"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small"/*.INFO'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small/1.INFO"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/analytics/outputs/ray_tracing_small/rays.csv"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/file-mod/inputs/jpg_small/jpg/119901.jpg"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '"~/t024/shadow/weather/inputs/temperatures.small.txt"'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat '~/t024/shadow/file-mod/inputs/wav_small/file_example_WAV_5MG.wav.~9~'` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/10_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/11_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/1_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/2_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/3_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/4_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/5_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/6_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/7_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/8_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.1_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.2_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.3_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.4_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.6_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.7_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.8_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ./inputs/9.9_30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat inputs/bio-min/input_min.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/analytics/inputs/nginx-logs_small/log7` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/analytics/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/file-mod/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/nlp/inputs/pg-small/ynkgt10.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `col -bx` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `comm '"~/t024/shadow/oneliners/inputs/comm_small/file1"' '"~/t024/shadow/oneliners/inputs/comm_small/file2"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `comm -12 '"${yr_txt}"' -` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt` | yes | says no split | no answer |
| Caruca, full grammar where traced | `comm -23 s1 s2` | yes | says no split | no answer |
| Caruca, full grammar where traced | `cut '-d" "' -f1,2 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `cut '-d" "' -f1,3` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `cut '-d" "' -f1,3 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `cut '-d" "' -f2` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `cut -c 1-1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 1-12` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 1-2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 1-4` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 3-3` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 7-` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -c 89-92` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '" "' -f 1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '" "' -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '" "' -f 4` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '"""' -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '"("' -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '")"' -f 1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 1,2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 1,2,4` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 1,3` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 3` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '","' -f 3,1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -d '"."' -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -f 1` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -f 1 -d '" "'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -f 2` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `cut -f 2 ./Gene_locs.txt` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `cut -f 4` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `diff -B s1 s2` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `echo '"Indexing Sample "${pop}"_"${OUT}/${sample}" "'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '"Isolating Chromosome "${chr}" from sample "${OUT}/${sample}",  "'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '"Processing Sample ${sample}"'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '"[engine] crawling 0/0/6/Image~0069.JPG_c66f.html"'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '"[engine] indexing 0/0/6/Image~0069.JPG_c66f.html"'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '"done"'` | – | says no split | no files |
| Caruca, full grammar where traced | `echo '${s_line}'` | – | says no split | no files |
| Caruca, full grammar where traced | `ffmpeg -y -i pipe:0 -f mp3 -ab 192000 pipe:1` | – | says no split | no files |
| Caruca, full grammar where traced | `find ~/t024/shadow/oneliners/inputs/chessdata_small -type f -name '"*.pgn"' -print0` | – | says no split | no files |
| Caruca, full grammar where traced | `fmt -w1` | – | says no split | no files |
| Caruca, full grammar where traced | `grep '" ${year}"' '"${formatted}"'` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `grep '"""'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"${city}"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"("'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"AT&T"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"And he said"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"Bell"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"UNIX"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"\."'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"\[RAY\]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"light.\*light"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"print"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"the land of"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep '"x"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -c '"^....$"'` | yes | says no split | says no split |
| Caruca, full grammar where traced | `grep -c '"^[A-Z]"'` | yes | says no split | says no split |
| Caruca, full grammar where traced | `grep -c '"light.\*light"'` | yes | says no split | says no split |
| Caruca, full grammar where traced | `grep -c '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca, full grammar where traced | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*$"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]$"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v '"NA"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v '"\-99"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v '"^\s*$"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v 999` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -v pathID` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep -vc '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca, full grammar where traced | `grep -vi '"[aeiou]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `grep 1969` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `head -n 1` | yes | says no split | no answer |
| Caruca, full grammar where traced | `head -n 2` | yes | says no split | no answer |
| Caruca, full grammar where traced | `head -n 3` | yes | says no split | no answer |
| Caruca, full grammar where traced | `head -n1` | yes | allows a split | no answer |
| Caruca, full grammar where traced | `head -n1 '"${formatted}"'` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `join -1 1 -2 1 -e '"NA"' '"${processed}"' '"${j2}"'` | – | says no split | no files |
| Caruca, full grammar where traced | `join -a1 -a2 -e '"-99"' -o '"0,1.2,1.3,2.2"' '"${j1}"' '"${max_y}"'` | – | says no split | no files |
| Caruca, full grammar where traced | `join -a1 -a2 -e '"-99"' -o '"0,1.2,2.2"' '"${yr_txt}"' '"${min_y}"'` | – | says no split | no files |
| Caruca, full grammar where traced | `mkfifo s1 s2` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `read -r city` | – | says no split | no files |
| Caruca, full grammar where traced | `read -r url` | – | says no split | no files |
| Caruca, full grammar where traced | `read chr` | – | says no split | no files |
| Caruca, full grammar where traced | `read s_line` | – | says no split | no files |
| Caruca, full grammar where traced | `rev` | – | says no split | no files |
| Caruca, full grammar where traced | `rm -f '"${yr_txt}"' '"${max_y}"' '"${min_y}"' '"${j1}"' '"${j2}"'` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `rm s1 s2` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `sed '"s/ .*//g"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed '"s/-99/NaN/g"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed '"s/T..:..:..//"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed '"s/T\(..\):..:../,\1/"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed '"s/T\(..\):..:../,\1/"' '"~/t024/shadow/covid/inputs/in_small.csv"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `sed '"s/[^[:print:]]//g"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed '"s/ly$/-ly/g"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed 's/$/"0s"/'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `sed -e '"s/SN:\([0-9XY]\)/SN:chr\1/"' -e '"s/SN:MT/SN:chrM/"'` | **no** | allows a split | allows a split |
| Caruca, full grammar where traced | `sed -e '"s|^\./||"' '"~/t024/shadow/web-search/inputs/index_min.txt"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `sed -n '"/^590432,/p"'` | **no** | says no split | allows a split |
| Caruca, full grammar where traced | `sed 100q` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 1d` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 2d` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 3d` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 4d` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 5d` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `sed 5q` | yes | allows a split | says no split |
| Caruca, full grammar where traced | `seq '"${START_YEAR}"' '"${END_YEAR}"'` | yes | says no split | no answer |
| Caruca, full grammar where traced | `sort` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -f` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -k 1 -n` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -n` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -nr` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -r` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -rn` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `sort -u` | yes | says no split | says no split |
| Caruca, full grammar where traced | `tail -n 1` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `tail -n1 '"${formatted}"'` | **no** | says no split | no answer |
| Caruca, full grammar where traced | `tr '" "' '"\n"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '" /"' '"__"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[:lower:]"' '"[:upper:]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[:upper:]"' '"[:lower:]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[A-Z]"' '"[a-z]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[a-z]"' '"P"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[a-z]"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"[a-z]"' '"\n"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr '"a-z"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr -c '"A-Za-z"' '"[\n*]"'` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `tr -c '"[A-Z]"' '"\n"'` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `tr -c '"[a-z][A-Z]"' '"\n"'` | yes | says no split | allows a split |
| Caruca, full grammar where traced | `tr -cs A-Za-z '"\n"'` | **no** | says no split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr -d '","'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr -d '"[:punct:]"'` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `tr -d '"\n"'` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr -s '" "' '"\n"'` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr -sc '"AEIOU"' '"[\012*]"'` | **no** | says no split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr -sc '"AEIOUaeiou"' '"[\012*]"'` | **no** | says no split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr -sc '"BCDFGHJKLMNPQRSTVWXYZ"' '"[\012*]"'` | **no** | says no split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `tr A-Z a-z` | yes | allows a split | allows a split |
| Caruca, full grammar where traced | `uniq` | yes | allows a split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `uniq -c` | yes | says no split | allows only a split PaSh has not implemented |
| Caruca, full grammar where traced | `wc -l` | yes | says no split | no answer |
| Caruca, full grammar where traced | `xargs -0 -n4 -P4 mawk '"/Result/ { split($0, a, "-"); res = substr(a[1], length(a[1]), 1); if (res == 1) white++; if (res == 0) black++; if (res == 2) draw++ } END { print white+black+draw, white, black, draw }"'` | **no** | says no split | allows a split |

## Appendix A5: times per script (seconds, median and min–max)

| Script | Plain bash | PaSh's own files | Caruca's files, PaSh grammar (all converted commands) | Caruca, full grammar where traced | PaSh's own files, second copy |
|---|---:|---:|---:|---:|---:|
| analytics/nginx | 1.29 (1.28–1.30, 3 runs) | 1.47 (1.41–1.50, 3 runs) | 1.43 (1.41–1.44, 3 runs) | 1.52 (1.49–1.54, 3 runs) | 1.44 (1.41–1.66, 3 runs) |
| analytics/pcaps | 100.25 (100.10–100.88, 3 runs) | 101.54 (101.48–102.26, 3 runs) | 102.47 (100.69–102.79, 3 runs) | 100.71 (100.58–103.30, 3 runs) | 101.42 (100.57–102.72, 3 runs) |
| analytics/ray-tracing | 0.00 (0.00–0.00, 3 runs) | 0.10 (0.10–0.11, 3 runs) | 0.12 (0.12–0.12, 3 runs) | 0.12 (0.12–0.12, 3 runs) | 0.11 (0.10–0.11, 3 runs) |
| bio/bio | 0.12 (0.12–0.12, 3 runs) | 0.23 (0.22–0.23, 3 runs) | 0.24 (0.23–0.25, 3 runs) | 0.24 (0.24–0.26, 3 runs) | 0.23 (0.22–0.24, 3 runs) |
| covid/1 | 10.26 (10.09–10.27, 3 runs) | 6.52 (6.45–6.99, 3 runs) | 10.35 (10.29–10.57, 3 runs) | 7.43 (7.08–7.45, 3 runs) | 5.89 (5.68–6.49, 3 runs) |
| covid/2 | 10.25 (10.19–10.43, 3 runs) | 6.67 (6.46–6.81, 3 runs) | 10.21 (10.16–10.21, 3 runs) | 7.95 (7.10–8.50, 3 runs) | 7.21 (6.84–7.34, 3 runs) |
| covid/3 | 15.14 (15.07–15.34, 3 runs) | 8.29 (7.75–8.38, 3 runs) | 15.35 (14.98–15.62, 3 runs) | 8.92 (8.12–8.96, 3 runs) | 7.97 (7.33–8.18, 3 runs) |
| covid/4 | 12.54 (12.50–12.63, 3 runs) | 6.74 (5.87–7.80, 3 runs) | 12.72 (12.70–12.77, 3 runs) | 7.82 (7.36–8.71, 3 runs) | 6.78 (5.89–7.08, 3 runs) |
| covid/5 | 12.22 (12.21–12.51, 3 runs) | 12.08 (12.07–12.37, 3 runs) | 12.17 (12.10–12.42, 3 runs) | 12.17 (11.65–12.19, 3 runs) | 12.31 (11.51–12.33, 3 runs) |
| file-mod/compress_files | 18.62 (18.61–18.76, 3 runs) | 19.17 (19.16–19.24, 3 runs) | 19.19 (19.06–19.32, 3 runs) | 19.15 (19.14–19.40, 3 runs) | 19.22 (19.07–19.25, 3 runs) |
| file-mod/encrypt_files | 2.10 (1.96–2.38, 3 runs) | 2.86 (2.51–2.95, 3 runs) | 2.66 (2.48–2.73, 3 runs) | 2.81 (2.64–2.86, 3 runs) | 4.18 (2.91–4.28, 3 runs) |
| file-mod/img_convert | 32.35 (32.22–32.59, 3 runs) | 35.61 (35.54–35.70, 3 runs) | 35.80 (35.78–35.80, 3 runs) | 35.90 (35.48–35.93, 3 runs) | 35.70 (35.62–35.93, 3 runs) |
| file-mod/thumbnail_generation | 11.11 (11.06–11.50, 3 runs) | 10.90 (10.87–11.06, 3 runs) | 10.98 (10.84–11.03, 3 runs) | 11.18 (10.78–11.25, 3 runs) | 10.76 (10.75–10.99, 3 runs) |
| file-mod/to_mp3 | 8.62 (8.57–8.66, 3 runs) | 8.97 (8.91–8.98, 3 runs) | 8.95 (8.93–9.03, 3 runs) | 8.96 (8.92–8.98, 3 runs) | 8.95 (8.90–8.95, 3 runs) |
| nlp/bigrams | 45.85 (45.76–46.36, 3 runs) | 63.15 (63.04–63.43, 3 runs) | 63.39 (63.24–63.40, 3 runs) | 63.89 (63.35–64.25, 3 runs) | 63.10 (62.98–63.23, 3 runs) |
| nlp/bigrams_appear_twice | 58.67 (58.64–58.80, 3 runs) | 76.06 (75.82–76.16, 3 runs) | 75.96 (75.81–76.00, 3 runs) | 76.40 (76.30–76.46, 3 runs) | 75.89 (75.83–75.95, 3 runs) |
| nlp/compare_exodus_genesis | 87.05 (86.83–87.30, 3 runs) | 104.77 (104.76–108.35, 3 runs) | 104.69 (104.66–104.79, 3 runs) | 104.96 (104.88–104.97, 3 runs) | 104.52 (104.51–104.59, 3 runs) |
| nlp/count_consonant_seq | 39.78 (39.72–39.83, 3 runs) | 57.70 (57.64–57.71, 3 runs) | 57.22 (57.22–57.23, 3 runs) | 56.08 (56.02–56.28, 3 runs) | 57.62 (57.40–57.79, 3 runs) |
| nlp/count_morphs | 8.21 (8.14–8.25, 3 runs) | 25.56 (25.43–25.70, 3 runs) | 24.96 (24.94–25.29, 3 runs) | 25.46 (25.25–25.50, 3 runs) | 25.39 (25.15–25.76, 3 runs) |
| nlp/count_trigrams | 51.33 (50.78–51.51, 3 runs) | 68.48 (67.80–68.53, 3 runs) | 68.16 (67.51–68.42, 3 runs) | 68.79 (68.49–69.12, 3 runs) | 68.06 (68.00–68.25, 3 runs) |
| nlp/count_vowel_seq | 7.97 (7.97–8.00, 3 runs) | 25.10 (24.94–27.36, 3 runs) | 25.08 (24.96–25.34, 3 runs) | 23.80 (23.73–25.76, 3 runs) | 25.61 (25.01–28.44, 3 runs) |
| nlp/count_words | 30.49 (30.48–30.60, 3 runs) | 48.33 (48.17–48.48, 3 runs) | 47.97 (47.86–48.01, 3 runs) | 48.98 (48.78–49.08, 3 runs) | 48.48 (48.45–49.39, 3 runs) |
| nlp/find_anagrams | 38.76 (38.51–38.87, 3 runs) | 55.72 (55.59–55.78, 3 runs) | 55.68 (55.64–56.66, 3 runs) | 56.07 (56.03–56.68, 3 runs) | 55.78 (55.68–55.78, 3 runs) |
| nlp/letter_words | 37.33 (37.14–37.43, 3 runs) | 71.50 (71.32–71.84, 3 runs) | 71.30 (71.24–71.86, 3 runs) | 73.10 (73.02–73.24, 3 runs) | 72.05 (71.79–72.14, 3 runs) |
| nlp/merge_upper | 30.52 (30.50–30.57, 3 runs) | 48.61 (48.58–48.83, 3 runs) | 48.30 (48.27–48.38, 3 runs) | 49.12 (48.91–49.16, 3 runs) | 48.72 (48.67–48.98, 3 runs) |
| nlp/sort | 34.08 (33.80–34.23, 3 runs) | 52.78 (52.13–52.98, 3 runs) | 52.07 (51.73–54.15, 3 runs) | 52.49 (52.47–52.67, 3 runs) | 51.90 (51.89–54.06, 3 runs) |
| nlp/sort_words_by_folding | 34.13 (34.00–35.46, 3 runs) | 53.65 (53.61–54.27, 3 runs) | 53.87 (53.21–54.24, 3 runs) | 52.68 (52.22–53.96, 3 runs) | 55.47 (51.28–56.79, 3 runs) |
| nlp/sort_words_by_num_of_syllables | 38.06 (37.23–38.36, 3 runs) | 58.66 (53.85–61.91, 3 runs) | 55.69 (55.05–62.21, 3 runs) | 59.88 (54.36–62.28, 3 runs) | 55.57 (53.80–58.95, 3 runs) |
| nlp/sort_words_by_rhyming | 36.57 (35.75–37.09, 3 runs) | 53.31 (52.69–55.96, 3 runs) | 55.43 (53.48–55.97, 3 runs) | 54.60 (54.30–55.83, 3 runs) | 53.35 (52.99–57.84, 3 runs) |
| nlp/syllable_words_1 | 17.09 (17.00–17.20, 3 runs) | 35.39 (35.20–35.41, 3 runs) | 34.99 (34.98–35.00, 3 runs) | 35.95 (35.87–36.12, 3 runs) | 35.44 (35.28–35.56, 3 runs) |
| nlp/syllable_words_2 | 10.87 (10.85–10.92, 3 runs) | 29.45 (29.34–29.47, 3 runs) | 28.71 (28.67–29.09, 3 runs) | 29.95 (29.87–30.13, 3 runs) | 29.30 (29.27–30.05, 3 runs) |
| nlp/trigram_rec | 13.48 (12.93–13.82, 3 runs) | 49.82 (47.49–52.26, 3 runs) | 49.41 (47.23–49.76, 3 runs) | 48.13 (47.59–59.51, 3 runs) | 47.24 (45.77–51.11, 3 runs) |
| nlp/uppercase_by_token | 9.35 (9.12–9.53, 3 runs) | 28.35 (27.96–28.64, 3 runs) | 28.41 (26.01–28.75, 3 runs) | 28.42 (26.64–29.84, 3 runs) | 27.71 (26.02–28.44, 3 runs) |
| nlp/uppercase_by_type | 29.70 (29.10–30.78, 3 runs) | 48.44 (48.30–50.79, 3 runs) | 51.12 (47.58–51.85, 3 runs) | 50.45 (48.87–52.79, 3 runs) | 49.41 (48.45–49.93, 3 runs) |
| nlp/verses_2om_3om_2instances | 6.21 (6.16–6.41, 3 runs) | 54.48 (53.55–61.48, 3 runs) | 56.24 (54.83–59.95, 3 runs) | 57.67 (55.66–60.79, 3 runs) | 62.56 (54.55–63.23, 3 runs) |
| nlp/vowel_sequencies_gr_1K | 31.21 (31.03–31.45, 3 runs) | 51.82 (51.17–52.74, 3 runs) | 49.83 (49.20–55.89, 3 runs) | 48.42 (47.75–52.46, 3 runs) | 51.68 (48.70–52.40, 3 runs) |
| nlp/words_no_vowels | 10.19 (10.19–10.27, 3 runs) | 27.92 (27.92–27.96, 3 runs) | 28.00 (27.73–28.02, 3 runs) | 29.53 (28.43–29.79, 3 runs) | 28.14 (27.96–28.24, 3 runs) |
| oneliners/bi-grams | 1.14 (1.13–1.20, 3 runs) | 1.30 (1.24–1.35, 3 runs) | 1.26 (1.25–1.29, 3 runs) | 1.27 (1.27–1.29, 3 runs) | 1.25 (1.24–1.31, 3 runs) |
| oneliners/comm | 0.03 (0.03–0.04, 3 runs) | 0.12 (0.12–0.12, 3 runs) | 0.14 (0.13–0.14, 3 runs) | 0.14 (0.13–0.14, 3 runs) | 0.12 (0.12–0.12, 3 runs) |
| oneliners/diff | 0.27 (0.26–0.28, 3 runs) | 0.38 (0.37–0.39, 3 runs) | 0.44 (0.38–0.46, 3 runs) | 0.42 (0.36–0.45, 3 runs) | 0.37 (0.37–0.41, 3 runs) |
| oneliners/nfa-regex | 8.38 (8.37–8.41, 3 runs) | 1.90 (1.89–1.92, 3 runs) | 1.95 (1.89–1.96, 3 runs) | 1.91 (1.90–1.94, 3 runs) | 1.89 (1.88–1.89, 3 runs) |
| oneliners/opt-parallel | 0.09 (0.09–0.09, 3 runs) | 0.19 (0.18–0.19, 3 runs) | 0.19 (0.19–0.19, 3 runs) | 0.19 (0.18–0.21, 3 runs) | 0.18 (0.18–0.22, 3 runs) |
| oneliners/set-diff | 0.25 (0.25–0.25, 3 runs) | 0.36 (0.35–0.38, 3 runs) | 0.36 (0.35–0.37, 3 runs) | 0.36 (0.36–0.36, 3 runs) | 0.37 (0.36–0.37, 3 runs) |
| oneliners/sort | 0.12 (0.11–0.14, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.26 (0.24–0.26, 3 runs) | 0.25 (0.25–0.26, 3 runs) | 0.21 (0.21–0.22, 3 runs) |
| oneliners/sort-sort | 0.17 (0.17–0.19, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.28 (0.27–0.30, 3 runs) | 0.30 (0.30–0.32, 3 runs) | 0.34 (0.34–0.34, 3 runs) |
| oneliners/spell | 1.02 (1.01–1.03, 3 runs) | 0.58 (0.58–0.59, 3 runs) | 1.08 (1.08–1.09, 3 runs) | 1.12 (1.11–1.12, 3 runs) | 0.60 (0.58–0.60, 3 runs) |
| oneliners/top-n | 0.87 (0.87–0.89, 3 runs) | 0.50 (0.49–0.52, 3 runs) | 0.97 (0.96–0.97, 3 runs) | 1.01 (1.00–1.01, 3 runs) | 0.49 (0.49–0.50, 3 runs) |
| oneliners/uniq-ips | 0.07 (0.07–0.07, 3 runs) | 0.18 (0.17–0.18, 3 runs) | 0.24 (0.24–0.24, 3 runs) | 0.23 (0.23–0.24, 3 runs) | 0.18 (0.17–0.19, 3 runs) |
| oneliners/wf | 0.87 (0.87–0.87, 3 runs) | 0.49 (0.49–0.52, 3 runs) | 0.97 (0.97–0.98, 3 runs) | 0.97 (0.96–0.98, 3 runs) | 0.49 (0.48–0.52, 3 runs) |
| unixfun/1 | 0.06 (0.06–0.06, 3 runs) | 0.16 (0.16–0.18, 3 runs) | 0.19 (0.19–0.19, 3 runs) | 0.19 (0.18–0.19, 3 runs) | 0.16 (0.16–0.16, 3 runs) |
| unixfun/10 | 0.06 (0.06–0.06, 3 runs) | 0.32 (0.32–0.34, 3 runs) | 0.16 (0.16–0.16, 3 runs) | 0.27 (0.27–0.28, 3 runs) | 0.32 (0.32–0.34, 3 runs) |
| unixfun/11 | 0.06 (0.06–0.06, 3 runs) | 0.32 (0.32–0.32, 3 runs) | 0.16 (0.15–0.17, 3 runs) | 0.27 (0.27–0.28, 3 runs) | 0.32 (0.32–0.32, 3 runs) |
| unixfun/12 | 0.25 (0.25–0.26, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.35 (0.35–0.36, 3 runs) | 0.34 (0.33–0.37, 3 runs) |
| unixfun/13 | 0.04 (0.03–0.04, 3 runs) | 0.18 (0.18–0.20, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.18 (0.18–0.18, 3 runs) |
| unixfun/14 | 0.70 (0.70–0.70, 3 runs) | 0.60 (0.58–0.61, 3 runs) | 0.81 (0.81–0.82, 3 runs) | 0.91 (0.90–0.95, 3 runs) | 0.60 (0.60–0.62, 3 runs) |
| unixfun/15 | 0.06 (0.06–0.06, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.20 (0.20–0.22, 3 runs) | 0.20 (0.20–0.20, 3 runs) | 0.17 (0.17–0.18, 3 runs) |
| unixfun/16 | 0.16 (0.16–0.16, 3 runs) | 0.25 (0.25–0.25, 3 runs) | 0.26 (0.26–0.26, 3 runs) | 0.26 (0.26–0.26, 3 runs) | 0.25 (0.25–0.25, 3 runs) |
| unixfun/17 | 0.16 (0.15–0.16, 3 runs) | 0.31 (0.30–0.32, 3 runs) | 0.26 (0.26–0.26, 3 runs) | 0.35 (0.34–0.39, 3 runs) | 0.31 (0.30–0.33, 3 runs) |
| unixfun/18 | 0.03 (0.03–0.03, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.20 (0.20–0.21, 3 runs) | 0.20 (0.19–0.20, 3 runs) | 0.17 (0.16–0.17, 3 runs) |
| unixfun/19 | 0.02 (0.02–0.02, 3 runs) | 0.18 (0.18–0.19, 3 runs) | 0.23 (0.21–0.23, 3 runs) | 0.22 (0.22–0.22, 3 runs) | 0.19 (0.18–0.19, 3 runs) |
| unixfun/2 | 0.28 (0.28–0.31, 3 runs) | 0.27 (0.27–0.28, 3 runs) | 0.39 (0.39–0.39, 3 runs) | 0.39 (0.39–0.39, 3 runs) | 0.27 (0.27–0.27, 3 runs) |
| unixfun/20 | 0.00 (0.00–0.00, 3 runs) | 0.15 (0.15–0.16, 3 runs) | 0.16 (0.16–0.16, 3 runs) | 0.16 (0.16–0.17, 3 runs) | 0.15 (0.15–0.17, 3 runs) |
| unixfun/21 | 0.94 (0.92–0.94, 3 runs) | 0.52 (0.52–0.53, 3 runs) | 1.06 (1.06–1.07, 3 runs) | 1.06 (1.06–1.06, 3 runs) | 0.54 (0.51–0.55, 3 runs) |
| unixfun/23 | 0.06 (0.06–0.06, 3 runs) | 0.25 (0.24–0.25, 3 runs) | 0.24 (0.24–0.25, 3 runs) | 0.24 (0.24–0.25, 3 runs) | 0.26 (0.25–0.26, 3 runs) |
| unixfun/24 | 0.07 (0.07–0.07, 3 runs) | 0.17 (0.16–0.17, 3 runs) | 0.20 (0.19–0.20, 3 runs) | 0.20 (0.19–0.24, 3 runs) | 0.17 (0.16–0.17, 3 runs) |
| unixfun/25 | 0.07 (0.07–0.07, 3 runs) | 0.16 (0.16–0.16, 3 runs) | 0.21 (0.20–0.25, 3 runs) | 0.20 (0.20–0.20, 3 runs) | 0.16 (0.16–0.18, 3 runs) |
| unixfun/26 | 0.07 (0.07–0.07, 3 runs) | 0.27 (0.27–0.29, 3 runs) | 0.24 (0.24–0.25, 3 runs) | 0.25 (0.24–0.26, 3 runs) | 0.28 (0.27–0.28, 3 runs) |
| unixfun/28 | 0.06 (0.06–0.06, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.34 (0.33–0.34, 3 runs) | 0.34 (0.33–0.34, 3 runs) |
| unixfun/29 | 0.06 (0.06–0.06, 3 runs) | 0.20 (0.20–0.21, 3 runs) | 0.26 (0.24–0.27, 3 runs) | 0.26 (0.26–0.28, 3 runs) | 0.20 (0.20–0.20, 3 runs) |
| unixfun/3 | 0.00 (0.00–0.00, 3 runs) | 0.13 (0.13–0.13, 3 runs) | 0.16 (0.15–0.16, 3 runs) | 0.16 (0.16–0.26, 3 runs) | 0.13 (0.13–0.13, 3 runs) |
| unixfun/30 | 0.09 (0.09–0.09, 3 runs) | 0.30 (0.29–0.32, 3 runs) | 0.37 (0.36–0.37, 3 runs) | 0.36 (0.35–0.36, 3 runs) | 0.30 (0.30–0.32, 3 runs) |
| unixfun/31 | 0.09 (0.09–0.09, 3 runs) | 0.30 (0.30–0.32, 3 runs) | 0.40 (0.39–0.43, 3 runs) | 0.39 (0.39–0.39, 3 runs) | 0.32 (0.31–0.34, 3 runs) |
| unixfun/32 | 0.04 (0.04–0.04, 3 runs) | 0.19 (0.19–0.20, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.19 (0.19–0.20, 3 runs) |
| unixfun/33 | 0.04 (0.04–0.04, 3 runs) | 0.19 (0.19–0.19, 3 runs) | 0.21 (0.20–0.21, 3 runs) | 0.21 (0.21–0.23, 3 runs) | 0.20 (0.19–0.22, 3 runs) |
| unixfun/34 | 0.00 (0.00–0.00, 3 runs) | 0.09 (0.09–0.09, 3 runs) | 0.10 (0.09–0.10, 3 runs) | 0.10 (0.10–0.11, 3 runs) | 0.09 (0.09–0.10, 3 runs) |
| unixfun/35 | 0.02 (0.01–0.02, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.20 (0.19–0.20, 3 runs) | 0.19 (0.19–0.20, 3 runs) | 0.17 (0.17–0.18, 3 runs) |
| unixfun/36 | 0.06 (0.06–0.06, 3 runs) | 0.15 (0.14–0.16, 3 runs) | 0.16 (0.15–0.16, 3 runs) | 0.18 (0.16–0.20, 3 runs) | 0.17 (0.14–0.18, 3 runs) |
| unixfun/4 | 0.25 (0.24–0.28, 3 runs) | 0.31 (0.30–0.32, 3 runs) | 0.36 (0.36–0.37, 3 runs) | 0.37 (0.37–0.37, 3 runs) | 0.32 (0.31–0.34, 3 runs) |
| unixfun/5 | 0.04 (0.04–0.04, 3 runs) | 0.20 (0.17–0.20, 3 runs) | 0.19 (0.18–0.20, 3 runs) | 0.19 (0.18–0.20, 3 runs) | 0.17 (0.17–0.17, 3 runs) |
| unixfun/6 | 0.07 (0.07–0.07, 3 runs) | 0.21 (0.20–0.22, 3 runs) | 0.22 (0.22–0.22, 3 runs) | 0.22 (0.21–0.22, 3 runs) | 0.22 (0.21–0.24, 3 runs) |
| unixfun/7 | 0.08 (0.08–0.08, 3 runs) | 0.18 (0.17–0.19, 3 runs) | 0.21 (0.20–0.22, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.17 (0.17–0.17, 3 runs) |
| unixfun/8 | 0.03 (0.03–0.03, 3 runs) | 0.18 (0.18–0.18, 3 runs) | 0.21 (0.21–0.21, 3 runs) | 0.21 (0.21–0.23, 3 runs) | 0.18 (0.18–0.18, 3 runs) |
| unixfun/9 | 0.03 (0.03–0.03, 3 runs) | 0.21 (0.20–0.21, 3 runs) | 0.23 (0.23–0.23, 3 runs) | 0.23 (0.23–0.23, 3 runs) | 0.21 (0.21–0.22, 3 runs) |
| weather/temp-analytics | 4.22 (4.21–4.25, 3 runs) | 4.37 (4.34–4.40, 3 runs) | 4.40 (4.33–4.40, 3 runs) | 4.40 (4.36–4.42, 3 runs) | 4.37 (4.33–4.45, 3 runs) |
| weather/tuft-weather | 464.57 (460.59–471.56, 3 runs) | 467.07 (466.69–468.54, 3 runs) | 466.58 (466.33–474.37, 3 runs) | 465.65 (461.70–478.79, 3 runs) | 465.25 (460.52–469.19, 3 runs) |
| web-search/engine | 617.47 (617.40–617.54, 3 runs) | 661.24 (655.33–670.71, 3 runs) | 656.96 (654.66–670.86, 3 runs) | 661.30 (657.12–667.35, 3 runs) | 660.27 (656.62–667.26, 3 runs) |

## Appendix A6 (from the records): controls and run windows

| Record | When | Script | Start | End | VM load at start | VM load at end | Koala changed | Mac power check |
|---|---|---|---|---|---|---|---|---|
| results.jsonl | main | oneliners/nfa-regex | 2026-11-26 15:15:50 -0500 | 2026-11-26 15:16:53 -0500 | 1.15, 0.53, 0.59 | 1.89, 0.90, 0.72 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/sort | 2026-11-26 15:16:53 -0500 | 2026-11-26 15:16:59 -0500 | 1.89, 0.90, 0.72 | 2.14, 0.96, 0.74 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/top-n | 2026-11-26 15:16:59 -0500 | 2026-11-26 15:17:15 -0500 | 2.14, 0.96, 0.74 | 1.88, 0.98, 0.75 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/wf | 2026-11-26 15:17:15 -0500 | 2026-11-26 15:17:30 -0500 | 1.88, 0.98, 0.75 | 1.69, 0.99, 0.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/spell | 2026-11-26 15:17:30 -0500 | 2026-11-26 15:17:48 -0500 | 1.69, 0.99, 0.76 | 1.91, 1.07, 0.79 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/diff | 2026-11-26 15:17:49 -0500 | 2026-11-26 15:17:57 -0500 | 1.91, 1.07, 0.79 | 1.85, 1.08, 0.80 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/bi-grams | 2026-11-26 15:17:57 -0500 | 2026-11-26 15:18:21 -0500 | 1.85, 1.08, 0.80 | 1.80, 1.13, 0.82 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/set-diff | 2026-11-26 15:18:22 -0500 | 2026-11-26 15:18:29 -0500 | 1.80, 1.13, 0.82 | 1.74, 1.12, 0.82 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/sort-sort | 2026-11-26 15:18:29 -0500 | 2026-11-26 15:18:35 -0500 | 1.74, 1.12, 0.82 | 2.98, 1.40, 0.91 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/uniq-ips | 2026-11-26 15:18:35 -0500 | 2026-11-26 15:18:40 -0500 | 2.98, 1.40, 0.91 | 2.82, 1.39, 0.91 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/comm | 2026-11-26 15:18:40 -0500 | 2026-11-26 15:18:43 -0500 | 2.82, 1.39, 0.91 | 2.82, 1.39, 0.91 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/opt-parallel | 2026-11-26 15:18:43 -0500 | 2026-11-26 15:18:47 -0500 | 2.82, 1.39, 0.91 | 2.67, 1.39, 0.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/1 | 2026-11-26 15:18:47 -0500 | 2026-11-26 15:18:50 -0500 | 2.67, 1.39, 0.92 | 2.86, 1.45, 0.94 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/2 | 2026-11-26 15:18:51 -0500 | 2026-11-26 15:18:58 -0500 | 2.86, 1.45, 0.94 | 2.63, 1.42, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/3 | 2026-11-26 15:18:58 -0500 | 2026-11-26 15:19:01 -0500 | 2.63, 1.42, 0.93 | 2.42, 1.40, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/4 | 2026-11-26 15:19:01 -0500 | 2026-11-26 15:19:08 -0500 | 2.42, 1.40, 0.93 | 2.47, 1.43, 0.94 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/5 | 2026-11-26 15:19:08 -0500 | 2026-11-26 15:19:12 -0500 | 2.47, 1.43, 0.94 | 2.35, 1.42, 0.94 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/6 | 2026-11-26 15:19:12 -0500 | 2026-11-26 15:19:16 -0500 | 2.35, 1.42, 0.94 | 2.80, 1.53, 0.98 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/7 | 2026-11-26 15:19:16 -0500 | 2026-11-26 15:19:20 -0500 | 2.80, 1.53, 0.98 | 2.58, 1.50, 0.97 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/8 | 2026-11-26 15:19:20 -0500 | 2026-11-26 15:19:24 -0500 | 2.58, 1.50, 0.97 | 2.58, 1.50, 0.97 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/9 | 2026-11-26 15:19:24 -0500 | 2026-11-26 15:19:29 -0500 | 2.58, 1.50, 0.97 | 2.45, 1.49, 0.97 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/10 | 2026-11-26 15:19:29 -0500 | 2026-11-26 15:19:34 -0500 | 2.45, 1.49, 0.97 | 2.25, 1.47, 0.97 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/11 | 2026-11-26 15:19:34 -0500 | 2026-11-26 15:19:39 -0500 | 2.25, 1.47, 0.97 | 2.39, 1.51, 0.98 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/12 | 2026-11-26 15:19:39 -0500 | 2026-11-26 15:19:46 -0500 | 2.39, 1.51, 0.98 | 2.47, 1.56, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/13 | 2026-11-26 15:19:46 -0500 | 2026-11-26 15:19:50 -0500 | 2.47, 1.56, 1.00 | 2.36, 1.55, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/14 | 2026-11-26 15:19:50 -0500 | 2026-11-26 15:20:05 -0500 | 2.36, 1.55, 1.00 | 2.12, 1.54, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/15 | 2026-11-26 15:20:05 -0500 | 2026-11-26 15:20:09 -0500 | 2.12, 1.54, 1.01 | 2.12, 1.54, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/16 | 2026-11-26 15:20:09 -0500 | 2026-11-26 15:20:14 -0500 | 2.12, 1.54, 1.01 | 2.03, 1.53, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/17 | 2026-11-26 15:20:14 -0500 | 2026-11-26 15:20:21 -0500 | 1.95, 1.52, 1.01 | 1.87, 1.51, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/18 | 2026-11-26 15:20:21 -0500 | 2026-11-26 15:20:24 -0500 | 1.87, 1.51, 1.01 | 1.87, 1.51, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/19 | 2026-11-26 15:20:24 -0500 | 2026-11-26 15:20:28 -0500 | 1.96, 1.54, 1.02 | 1.96, 1.54, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/20 | 2026-11-26 15:20:29 -0500 | 2026-11-26 15:20:32 -0500 | 1.96, 1.54, 1.02 | 1.81, 1.51, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/21 | 2026-11-26 15:20:32 -0500 | 2026-11-26 15:20:49 -0500 | 1.81, 1.51, 1.01 | 1.70, 1.50, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/23 | 2026-11-26 15:20:49 -0500 | 2026-11-26 15:20:53 -0500 | 1.70, 1.50, 1.02 | 1.64, 1.49, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/24 | 2026-11-26 15:20:54 -0500 | 2026-11-26 15:20:57 -0500 | 1.64, 1.49, 1.02 | 1.59, 1.49, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/25 | 2026-11-26 15:20:57 -0500 | 2026-11-26 15:21:01 -0500 | 1.59, 1.49, 1.02 | 1.62, 1.49, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/26 | 2026-11-26 15:21:01 -0500 | 2026-11-26 15:21:07 -0500 | 1.62, 1.49, 1.02 | 1.57, 1.49, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/28 | 2026-11-26 15:21:07 -0500 | 2026-11-26 15:21:13 -0500 | 1.57, 1.49, 1.02 | 1.53, 1.48, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/29 | 2026-11-26 15:21:13 -0500 | 2026-11-26 15:21:18 -0500 | 1.53, 1.48, 1.02 | 1.64, 1.50, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/30 | 2026-11-26 15:21:18 -0500 | 2026-11-26 15:21:24 -0500 | 1.64, 1.50, 1.03 | 2.65, 1.73, 1.11 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/31 | 2026-11-26 15:21:25 -0500 | 2026-11-26 15:21:31 -0500 | 2.65, 1.73, 1.11 | 2.44, 1.70, 1.10 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/32 | 2026-11-26 15:21:32 -0500 | 2026-11-26 15:21:36 -0500 | 2.44, 1.70, 1.10 | 2.32, 1.69, 1.10 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/33 | 2026-11-26 15:21:36 -0500 | 2026-11-26 15:21:40 -0500 | 2.32, 1.69, 1.10 | 2.22, 1.68, 1.10 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/34 | 2026-11-26 15:21:40 -0500 | 2026-11-26 15:21:42 -0500 | 2.22, 1.68, 1.10 | 2.22, 1.68, 1.10 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/35 | 2026-11-26 15:21:42 -0500 | 2026-11-26 15:21:45 -0500 | 2.22, 1.68, 1.10 | 2.28, 1.70, 1.11 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/36 | 2026-11-26 15:21:45 -0500 | 2026-11-26 15:21:49 -0500 | 2.28, 1.70, 1.11 | 2.28, 1.70, 1.11 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/1 | 2026-11-26 15:21:49 -0500 | 2026-11-26 15:24:39 -0500 | 2.28, 1.70, 1.11 | 5.72, 3.21, 1.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/2 | 2026-11-26 15:24:39 -0500 | 2026-11-26 15:27:22 -0500 | 5.72, 3.21, 1.76 | 4.70, 3.78, 2.22 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/3 | 2026-11-26 15:27:22 -0500 | 2026-11-26 15:30:58 -0500 | 4.70, 3.78, 2.22 | 5.22, 4.39, 2.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/4 | 2026-11-26 15:30:58 -0500 | 2026-11-26 15:34:01 -0500 | 5.22, 4.39, 2.78 | 5.72, 4.87, 3.24 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/5 | 2026-11-26 15:34:01 -0500 | 2026-11-26 15:37:53 -0500 | 5.72, 4.87, 3.24 | 1.90, 3.17, 2.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/syllable_words_1 | 2026-11-26 15:37:53 -0500 | 2026-11-26 15:48:34 -0500 | 1.90, 3.17, 2.90 | 2.06, 2.22, 2.50 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/syllable_words_2 | 2026-11-26 15:48:34 -0500 | 2026-11-26 15:57:17 -0500 | 2.06, 2.22, 2.50 | 2.29, 2.34, 2.40 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/letter_words | 2026-11-26 15:57:17 -0500 | 2026-11-26 16:18:53 -0500 | 2.29, 2.34, 2.40 | 1.96, 1.95, 1.99 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/bigrams_appear_twice | 2026-11-26 16:18:53 -0500 | 2026-11-26 16:42:43 -0500 | 1.96, 1.95, 1.99 | 1.53, 1.61, 1.69 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/bigrams | 2026-11-26 16:42:44 -0500 | 2026-11-26 17:03:12 -0500 | 1.53, 1.61, 1.69 | 1.80, 1.80, 1.79 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/compare_exodus_genesis | 2026-11-26 17:03:12 -0500 | 2026-11-26 17:36:01 -0500 | 1.80, 1.80, 1.79 | 1.20, 1.32, 1.38 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_consonant_seq | 2026-11-26 17:36:01 -0500 | 2026-11-26 17:53:30 -0500 | 1.20, 1.32, 1.38 | 1.30, 1.43, 1.44 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_morphs | 2026-11-26 17:53:30 -0500 | 2026-11-26 18:01:00 -0500 | 1.30, 1.43, 1.44 | 2.14, 1.91, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_trigrams | 2026-11-26 18:01:01 -0500 | 2026-11-26 18:23:09 -0500 | 2.05, 1.89, 1.66 | 1.72, 1.64, 1.62 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_vowel_seq | 2026-11-26 18:23:09 -0500 | 2026-11-26 18:30:30 -0500 | 1.72, 1.64, 1.62 | 1.99, 1.82, 1.71 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_words | 2026-11-26 18:30:30 -0500 | 2026-11-26 18:45:14 -0500 | 1.99, 1.82, 1.71 | 1.64, 1.57, 1.59 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/find_anagrams | 2026-11-26 18:45:15 -0500 | 2026-11-26 19:02:28 -0500 | 1.64, 1.57, 1.59 | 1.38, 1.55, 1.60 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/merge_upper | 2026-11-26 19:02:28 -0500 | 2026-11-26 19:17:17 -0500 | 1.38, 1.55, 1.60 | 1.68, 1.61, 1.61 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort | 2026-11-26 19:17:17 -0500 | 2026-11-26 19:33:19 -0500 | 1.68, 1.61, 1.61 | 1.48, 1.44, 1.51 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_folding | 2026-11-26 19:33:20 -0500 | 2026-11-26 19:49:38 -0500 | 1.48, 1.44, 1.51 | 1.56, 1.49, 1.48 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_num_of_syllables | 2026-11-26 19:49:38 -0500 | 2026-11-26 20:07:10 -0500 | 1.56, 1.49, 1.48 | 1.29, 1.42, 1.45 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_rhyming | 2026-11-26 20:07:10 -0500 | 2026-11-26 20:23:52 -0500 | 1.29, 1.42, 1.45 | 1.76, 1.73, 1.60 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/trigram_rec | 2026-11-26 20:23:54 -0500 | 2026-11-26 20:38:50 -0500 | 1.76, 1.73, 1.60 | 1.70, 1.74, 1.64 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/uppercase_by_token | 2026-11-26 20:38:50 -0500 | 2026-11-26 20:47:07 -0500 | 1.70, 1.74, 1.64 | 1.58, 1.64, 1.63 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/uppercase_by_type | 2026-11-26 20:47:08 -0500 | 2026-11-26 21:02:18 -0500 | 1.58, 1.64, 1.63 | 1.00, 1.25, 1.42 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/verses_2om_3om_2instances | 2026-11-26 21:02:18 -0500 | 2026-11-26 21:19:23 -0500 | 1.00, 1.25, 1.42 | 1.40, 1.26, 1.30 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/vowel_sequencies_gr_1K | 2026-11-26 21:19:23 -0500 | 2026-11-26 21:34:43 -0500 | 1.40, 1.26, 1.30 | 1.59, 1.54, 1.46 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/words_no_vowels | 2026-11-26 21:34:43 -0500 | 2026-11-26 21:43:07 -0500 | 1.59, 1.54, 1.46 | 1.86, 1.73, 1.59 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | weather/temp-analytics | 2026-11-26 21:43:07 -0500 | 2026-11-26 21:44:32 -0500 | 1.86, 1.73, 1.59 | 1.70, 1.72, 1.60 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | weather/tuft-weather | 2026-11-26 21:44:33 -0500 | 2026-11-27 00:13:06 -0500 | 1.70, 1.72, 1.60 | 1.42, 1.41, 1.41 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | web-search/engine | 2026-11-27 00:13:06 -0500 | 2026-11-27 03:39:59 -0500 | 1.42, 1.41, 1.41 | 1.40, 1.49, 1.49 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/nginx | 2026-11-27 03:39:59 -0500 | 2026-11-27 03:40:28 -0500 | 1.40, 1.49, 1.49 | 1.64, 1.54, 1.51 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/pcaps | 2026-11-27 03:40:28 -0500 | 2026-11-27 04:12:35 -0500 | 1.64, 1.54, 1.51 | 1.80, 1.74, 1.70 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/ray-tracing | 2026-11-27 04:12:35 -0500 | 2026-11-27 04:12:37 -0500 | 1.80, 1.74, 1.70 | 1.80, 1.74, 1.70 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/compress_files | 2026-11-27 04:12:37 -0500 | 2026-11-27 04:18:50 -0500 | 1.80, 1.74, 1.70 | 1.56, 1.53, 1.62 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/encrypt_files | 2026-11-27 04:18:50 -0500 | 2026-11-27 04:20:01 -0500 | 1.56, 1.53, 1.62 | 1.71, 1.57, 1.62 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/img_convert | 2026-11-27 04:20:01 -0500 | 2026-11-27 04:31:17 -0500 | 1.71, 1.57, 1.62 | 2.22, 2.26, 1.99 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/to_mp3 | 2026-11-27 04:31:17 -0500 | 2026-11-27 04:34:07 -0500 | 2.22, 2.26, 1.99 | 1.08, 1.72, 1.82 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/thumbnail_generation | 2026-11-27 04:34:07 -0500 | 2026-11-27 04:37:38 -0500 | 1.08, 1.72, 1.82 | 1.04, 1.39, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | bio/bio | 2026-11-27 04:37:38 -0500 | 2026-11-27 04:37:44 -0500 | 1.04, 1.39, 1.67 | 1.03, 1.38, 1.66 | no | not checked per window here (see the sleep list) |

## Full run: output, what PaSh did, files written (timed repeats)

Printed output: every run of the script (timed and with the stand-in programs) the same as bash's run of the same repeat. State: what PaSh did in the first timed repeat. File check: timed rows of the 32 scripts that write files (bash wrote at least one).

| Source | Scripts | Printed output same as bash | Same as Koala's stored answer | PaSh ran a part in parallel | Fell back to plain bash | Other state | File check: same / not checked / different |
|---|---:|---:|---:|---:|---:|---|---|
| PaSh's own files | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 | 93 / 0 / 3 |
| Caruca's files, PaSh grammar (all converted commands) | 86 | 77 of 86 | 37 of 46 | 29 of 86 | 33 of 86 | compiled, nothing split: 24 | 93 / 0 / 3 |
| Caruca, full grammar where traced | 86 | 76 of 86 | 36 of 46 | 40 of 86 | 22 of 86 | compiled, nothing split: 24 | 93 / 0 / 3 |
| PaSh's own files, second copy | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 | 93 / 0 / 3 |

All sources together, file check on timed rows: same 372, not checked 0, different 12, of 384. Different, by script: web-search/engine 12.
Plain bash matched Koala's stored answer in 46 of 46 scripts that have one.
Scripts whose recorded state differs between timed repeats: none.

## Full run: parts paired with PaSh's own files, the partial source


## Full run: commands gained and lost, per script (from the per-use records)

| Source | Command | Gained (scripts) | Lost (scripts) |
|---|---|---:|---:|
| Caruca's files, PaSh grammar (all converted commands) | `cat` | 29 | 0 |
| Caruca's files, PaSh grammar (all converted commands) | `cut` | 0 | 9 |
| Caruca's files, PaSh grammar (all converted commands) | `grep` | 0 | 4 |
| Caruca's files, PaSh grammar (all converted commands) | `sed` | 7 | 5 |
| Caruca's files, PaSh grammar (all converted commands) | `sort` | 0 | 17 |
| Caruca's files, PaSh grammar (all converted commands) | `tr` | 2 | 6 |
| Caruca's files, PaSh grammar (all converted commands) | `uniq` | 2 | 0 |
| Caruca, full grammar where traced | `cat` | 40 | 0 |
| Caruca, full grammar where traced | `col` | 0 | 1 |
| Caruca, full grammar where traced | `sed` | 8 | 1 |
| Caruca, full grammar where traced | `sort` | 0 | 17 |
| Caruca, full grammar where traced | `tr` | 2 | 2 |
| Caruca, full grammar where traced | `uniq` | 2 | 0 |

Per command (all commands used inside a part): scripts using it, and scripts where PaSh's own files had it split: . 1/0, ./crawl.sh 1/0, ./index.sh 1/0, [ 2/0, [[ 1/0, awk 11/0, bigrams_aux 1/0, break 1/0, cat 82/0, cd 2/0, col 1/1, comm 4/0, continue 1/0, cut 35/26, diff 1/0, dirname 2/0, echo 25/0, export 12/0, ffmpeg 1/0, find 1/0, fmt 2/0, grep 47/21, gzip 1/0, head 9/0, join 1/0, mawk 1/0, mkdir 31/0, mkfifo 2/0, mogrify 1/0, printf 1/0, pure_func 11/0, python3 1/0, read 3/0, rev 1/0, rm 3/0, samtools 1/0, sed 24/6, seq 1/0, sort 44/17, tail 3/0, tr 49/20, uniq 30/0, wc 7/0, xargs 1/0.

## Full run: time (median of the timed repeats; geometric means over scripts)

| Source | Scripts | Speed-up over bash | Time vs PaSh's own | Faster than PaSh's own by >10% | Slower than PaSh's own by >10% | Faster than bash by >10% | Slower than bash |
|---|---:|---:|---:|---:|---:|---:|---:|
| PaSh's own files | 86 | 0.44x | 1.00 | 0 of 86 | 0 of 86 | 10 of 86 | 73 of 86 |
| Caruca's files, PaSh grammar (all converted commands) | 86 | 0.41x | 1.09 | 5 of 86 | 30 of 86 | 1 of 86 | 82 of 86 |
| Caruca, full grammar where traced | 86 | 0.40x | 1.10 | 3 of 86 | 32 of 86 | 5 of 86 | 80 of 86 |
| PaSh's own files, second copy | 86 | 0.44x | 1.00 | 1 of 86 | 3 of 86 | 10 of 86 | 74 of 86 |

Noise band (PaSh's own files, second copy against the first copy): 0.83 to 1.46, median 1.00; 4 of 86 scripts beyond 10%.

## Checks the script made on the records

| Check | Result | Detail |
|---|---|---|
| bash's own output is identical across all its runs | passed | 86 of 86 scripts; varying: none |
| the distinct parts are the same for every source (same texts, same count) | passed | PaSh's own files: 177; Caruca's files, PaSh grammar (all converted commands): 177; Caruca, full grammar where traced: 177 |
| each script sends the same sequence of part texts to PaSh under every source (repeat 1) | passed |  |
| the part count in results.jsonl equals the parts listed in regions.jsonl | passed |  |
| the command uses are the same for every source (same part, same position) | passed | PaSh's own files: 609; Caruca's files, PaSh grammar (all converted commands): 609; Caruca, full grammar where traced: 609 |
| a use that appears in more than one launch of a script has the same result in each | passed | 0 differ |
| the commands split per use match the commands split per script in results.jsonl | passed |  |
| PaSh split a use exactly when its files allowed a split PaSh can carry out | passed | 639 of 639 uses in parts run in parallel agree; 0 differ |
| every instrumented repeat split the same uses as repeat 1 | passed | 1827 uses x sources, up to 1 repeats each; 0 vary |
| Caruca's files, PaSh grammar (all converted commands): a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| Caruca, full grammar where traced: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| every script run is in the inventory | **not passed** | weather/temp-analytics, web-search/engine |
| the commands the inventory lists equal the commands seen starting, per script | **not passed** | listed, not seen: [('analytics/ray-tracing', 'cut'), ('analytics/ray-tracing', 'sed'), ('oneliners/bi-grams', 'bigrams_aux')]; seen, not listed: [('weather/temp-analytics', 'cat'), ('weather/temp-analytics', 'cut'), ('weather/temp-analytics', 'grep'), ('weather/temp-analytics', 'sort'), ('web-search/engine', 'awk'), ('web-search/engine', 'cat'), ('web-search/engine', 'cut'), ('web-search/engine', 'dirname'), ('web-search/engine', 'grep'), ('web-search/engine', 'iconv'), ('web-search/engine', 'mkfifo'), ('web-search/engine', 'mktemp'), ('web-search/engine', 'node'), ('web-search/engine', 'paste'), ('web-search/engine', 'rm'), ('web-search/engine', 'sed'), ('web-search/engine', 'sort'), ('web-search/engine', 'tail'), ('web-search/engine', 'tee'), ('web-search/engine', 'tr')] |
| Koala's checkout did not change during any run window | passed |  |
| no kept run window overlaps a Mac sleep, except windows whose affected rows were redone | passed | 0 of 86 windows overlap a sleep:  |


## Notes (added by hand to the counting, 2026-11-27)

- **`unixfun/23`, `tr -d '\n'` then `cut -c 1-4`.** The naive LLM's files (first session) and Caruca's (this session) both allow
  `tr -d '\n'` to split, but only Caruca's give wrong output. The naive LLM's `tr` file
  (`naive_llm_caruca/pash_annotations_latest/tr/ParallelizabilityInfoGeneratorTr.py`, comment lines 9-13) offers only the
  consecutive-chunks recipe when the operands may touch the newline, because round robin regroups output by line. Caruca's
  converted file (`save_pash_py/tr/pash_grammar/trace_1/ParallelizabilityInfoGeneratorTr.py`, lines 30-31) offers both
  consecutive chunks and round robin. PaSh's logs: `~/t024/out/logs/unixfun_23__naive__instrumented.log.gz` (tr not run per
  block) vs `~/t024/out_caruca_all/logs/unixfun_23__caruca-pash-all__instrumented.log.gz` (all 7 commands run per 1 MB block;
  `cut` prints 4 characters per block, 155 bytes instead of 5). Checked by the orchestrator against the logs; the recipe lines
  were re-read 2026-11-27.
- Sleep check: this run had no per-window power check; `--sleep-events` was given an empty file because `pmset -g log`
  shows no sleep or wake from 2026-11-26 15:10 to 2026-11-27 04:45 and `power_watch.tsv` shows mains power throughout.
