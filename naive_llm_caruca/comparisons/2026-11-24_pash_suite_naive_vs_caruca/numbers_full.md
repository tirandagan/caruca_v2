# Numbers for the PaSh-suite report

Written by `count_report.py` from `full_run (via prep_full_records.py)`. Every rate is "a of b". Do not edit by hand; re-run the script.

- Scripts run: 86. Scripts whose plain-bash output is the same in every bash run (**N**): 86.
- Distinct parts sent to PaSh (**P**): 177. Command uses inside those parts (**U**): 609.
- Command uses that ran outside every part sent to PaSh (not in U): PaSh's own files 205, Naive LLM's files 205, Caruca's files, PaSh grammar 205, Caruca's files, main grammar 205.

## Table 1: What PaSh did with each source's files

| Source | Output same as bash | Scripts with any part run in parallel | Parts run in parallel | Command uses split | Faster than bash |
|---|---:|---:|---:|---:|---:|
| PaSh's own files (reference) | 86 of 86 | 41 of 86 | 41 of 177 | 126 of 609 | 12 of 86 (median speed-up 0.51x) |
| Naive LLM's files | 86 of 86 | 43 of 86 | 43 of 177 | 192 of 609 | 7 of 86 (median speed-up 0.49x) |
| Caruca's files, PaSh grammar | 86 of 86 | 29 of 86 | 29 of 177 | 94 of 609 | 3 of 86 (median speed-up 0.58x) |
| Caruca's files, main grammar | 86 of 86 | 41 of 86 | 41 of 177 | 142 of 609 | 6 of 86 (median speed-up 0.52x) |

## Table 2: Commands a source brings its own files for, and what PaSh did with them

| Source | Uses with the source's own files | … split with them | … the same uses split with PaSh's own files | Uses with PaSh's own files filled in | … result same as with PaSh's own | Uses with no files from anyone |
|---|---:|---:|---:|---:|---:|---:|
| Naive LLM's files | 523 of 609 | 192 of 523 | 126 of 523 | 1 of 609 | 1 of 1 | 85 of 609 |
| Caruca's files, PaSh grammar | 304 of 609 | 71 of 304 | 90 of 304 | 181 of 609 | 152 of 181 | 124 of 609 |
| Caruca's files, main grammar | 304 of 609 | 106 of 304 | 90 of 304 | 181 of 609 | 181 of 181 | 124 of 609 |

- Caruca's files, PaSh grammar: filled-in use with a different result: covid/1, `sed '"s/T..:..:..//"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/1, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/1, `awk '"{print $2,$1}"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/2, `sed '"s/T..:..:..//"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/2, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/2, `awk '"{print $2,$1}"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/3, `sed '"s/T\(..\):..:../,\1/"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/3, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/3, `awk '"{print $2,$1}"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/4, `sed '"s/T\(..\):..:../,\1/"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/4, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: covid/4, `awk '"{print $2,$1}"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/sort-sort, `tr A-Z a-z`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/top-n, `tr -c '"A-Za-z"' '"[\n*]"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/top-n, `tr A-Z a-z`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/top-n, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/top-n, `sed 100q`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/wf, `tr -c '"A-Za-z"' '"[\n*]"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/wf, `tr A-Z a-z`
- Caruca's files, PaSh grammar: filled-in use with a different result: oneliners/wf, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/10, `tr '" "' '"\n"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/10, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/11, `tr '" "' '"\n"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/11, `tr '"[a-z]"' '"P"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/11, `uniq -c`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/14, `awk '"{print $2, $0}"'`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/17, `uniq`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/17, `sed 's/$/"0s"/'`
- Caruca's files, PaSh grammar: filled-in use with a different result: unixfun/4, `uniq -c`

## Chart A data: the scripts' parts, compared with PaSh's own files

Reference, PaSh's own files: run in parallel 41 of 177; not 136 of 177.

| Source | Run in parallel with both | Only with this source | With neither | Only with PaSh's own files |
|---|---:|---:|---:|---:|
| Naive LLM's files | 41 of 177 | 2 of 177 | 134 of 177 | 0 of 177 |
| Caruca's files, PaSh grammar | 29 of 177 | 0 of 177 | 136 of 177 | 12 of 177 |
| Caruca's files, main grammar | 41 of 177 | 0 of 177 | 136 of 177 | 0 of 177 |

## Table 3: Every command where a source changed what PaSh did

| Command | Uses in the suite | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | Output |
|---|---:|---:|---:|---:|---:|---|
| `cat` | 94 | split 0 of 94 | **split 43 of 94** | **split 29 of 94** | **split 41 of 94** | all same as bash |
| `tr` | 75 | split 29 of 75 | **split 40 of 75** | **split 21 of 75** | split 29 of 75 | all same as bash |
| `grep` | 74 | split 29 of 74 | **split 30 of 74** | **split 22 of 74** | split 29 of 74 | all same as bash |
| `sort` | 67 | split 25 of 67 | **split 32 of 67** | **split 0 of 67** | **split 0 of 67** | all same as bash |
| `cut` | 58 | split 36 of 58 | **split 39 of 58** | **split 20 of 58** | split 36 of 58 | all same as bash |
| `sed` | 37 | split 6 of 37 | **split 1 of 37** | **split 1 of 37** | split 6 of 37 | all same as bash |
| `uniq` | 30 | split 0 of 30 | **split 0 of 30** | **split 0 of 30** | split 0 of 30 | all same as bash |
| `awk` | 14 | split 0 of 14 | **split 7 of 14** | **split 0 of 14** | split 0 of 14 | all same as bash |
| `head` | 10 | split 0 of 10 | **split 0 of 10** | split 0 of 10 | split 0 of 10 | all same as bash |
| `tail` | 3 | split 0 of 3 | **split 0 of 3** | split 0 of 3 | split 0 of 3 | all same as bash |
| `col` | 1 | split 1 of 1 | **split 0 of 1** | split 1 of 1 | split 1 of 1 | all same as bash |

The other 33 commands: every source gave the same result as PaSh's own files (mkdir, echo, export, pure_func, wc, comm, samtools, [, read, join, rm, [[, cd, dirname, fmt, mkfifo, rev, ., ./crawl.sh, ./index.sh, bigrams_aux, break, continue, diff, ffmpeg, find, gzip, mawk, mogrify, printf, python3, seq, xargs). Bold = differs from PaSh's own.

## Chart B data: time against PaSh's own files

Noise (PaSh's own files, second copy against the first copy): largest difference 17.1% over 86 scripts.

| Source | Script | Median s, PaSh's own files | Median s, this source | Output same as bash | Split choices differ |
|---|---|---:|---:|---|---|
| Naive LLM's files | analytics/nginx | 1.48 | 1.46 | yes | no |
| Naive LLM's files | analytics/pcaps | 106.15 | 101.38 | yes | no |
| Naive LLM's files | analytics/ray-tracing | 0.12 | 0.12 | yes | no |
| Naive LLM's files | bio/bio | 0.28 | 0.26 | yes | no |
| Naive LLM's files | covid/1 | 6.73 | 13.19 | yes | yes |
| Naive LLM's files | covid/2 | 7.14 | 14.45 | yes | yes |
| Naive LLM's files | covid/3 | 7.50 | 17.90 | yes | yes |
| Naive LLM's files | covid/4 | 6.67 | 16.75 | yes | yes |
| Naive LLM's files | covid/5 | 11.13 | 11.38 | yes | no |
| Naive LLM's files | file-mod/compress_files | 19.49 | 19.45 | yes | no |
| Naive LLM's files | file-mod/encrypt_files | 2.73 | 2.69 | yes | no |
| Naive LLM's files | file-mod/img_convert | 35.81 | 35.51 | yes | no |
| Naive LLM's files | file-mod/thumbnail_generation | 11.22 | 10.99 | yes | no |
| Naive LLM's files | file-mod/to_mp3 | 9.34 | 9.31 | yes | no |
| Naive LLM's files | nlp/bigrams | 69.41 | 74.10 | yes | no |
| Naive LLM's files | nlp/bigrams_appear_twice | 79.45 | 78.62 | yes | no |
| Naive LLM's files | nlp/compare_exodus_genesis | 108.74 | 109.87 | yes | no |
| Naive LLM's files | nlp/count_consonant_seq | 65.05 | 60.30 | yes | no |
| Naive LLM's files | nlp/count_morphs | 25.07 | 26.93 | yes | no |
| Naive LLM's files | nlp/count_trigrams | 74.53 | 78.88 | yes | no |
| Naive LLM's files | nlp/count_vowel_seq | 26.52 | 25.65 | yes | no |
| Naive LLM's files | nlp/count_words | 47.92 | 47.52 | yes | no |
| Naive LLM's files | nlp/find_anagrams | 63.43 | 66.47 | yes | no |
| Naive LLM's files | nlp/letter_words | 76.58 | 74.44 | yes | no |
| Naive LLM's files | nlp/merge_upper | 48.16 | 48.87 | yes | no |
| Naive LLM's files | nlp/sort | 51.50 | 51.14 | yes | no |
| Naive LLM's files | nlp/sort_words_by_folding | 51.30 | 50.94 | yes | no |
| Naive LLM's files | nlp/sort_words_by_num_of_syllables | 58.08 | 57.99 | yes | no |
| Naive LLM's files | nlp/sort_words_by_rhyming | 52.19 | 53.27 | yes | no |
| Naive LLM's files | nlp/syllable_words_1 | 36.06 | 35.04 | yes | no |
| Naive LLM's files | nlp/syllable_words_2 | 30.55 | 29.79 | yes | no |
| Naive LLM's files | nlp/trigram_rec | 53.11 | 45.58 | yes | no |
| Naive LLM's files | nlp/uppercase_by_token | 27.10 | 26.55 | yes | no |
| Naive LLM's files | nlp/uppercase_by_type | 46.16 | 45.63 | yes | no |
| Naive LLM's files | nlp/verses_2om_3om_2instances | 56.36 | 54.03 | yes | no |
| Naive LLM's files | nlp/vowel_sequencies_gr_1K | 49.89 | 49.02 | yes | no |
| Naive LLM's files | nlp/words_no_vowels | 27.42 | 27.45 | yes | no |
| Naive LLM's files | oneliners/bi-grams | 1.30 | 1.30 | yes | no |
| Naive LLM's files | oneliners/comm | 0.13 | 0.14 | yes | no |
| Naive LLM's files | oneliners/diff | 0.43 | 0.41 | yes | no |
| Naive LLM's files | oneliners/nfa-regex | 1.94 | 1.90 | yes | yes |
| Naive LLM's files | oneliners/opt-parallel | 0.25 | 0.20 | yes | no |
| Naive LLM's files | oneliners/set-diff | 0.35 | 0.36 | yes | no |
| Naive LLM's files | oneliners/sort | 0.24 | 0.25 | yes | yes |
| Naive LLM's files | oneliners/sort-sort | 0.36 | 0.40 | yes | yes |
| Naive LLM's files | oneliners/spell | 0.63 | 0.91 | yes | yes |
| Naive LLM's files | oneliners/top-n | 0.59 | 0.70 | yes | yes |
| Naive LLM's files | oneliners/uniq-ips | 0.18 | 0.21 | yes | yes |
| Naive LLM's files | oneliners/wf | 0.50 | 0.62 | yes | yes |
| Naive LLM's files | unixfun/1 | 0.20 | 0.21 | yes | yes |
| Naive LLM's files | unixfun/10 | 0.33 | 0.47 | yes | yes |
| Naive LLM's files | unixfun/11 | 0.37 | 0.51 | yes | yes |
| Naive LLM's files | unixfun/12 | 0.41 | 0.60 | yes | yes |
| Naive LLM's files | unixfun/13 | 0.23 | 0.28 | yes | yes |
| Naive LLM's files | unixfun/14 | 0.63 | 0.57 | yes | yes |
| Naive LLM's files | unixfun/15 | 0.19 | 0.21 | yes | yes |
| Naive LLM's files | unixfun/16 | 0.28 | 0.35 | yes | yes |
| Naive LLM's files | unixfun/17 | 0.35 | 0.36 | yes | yes |
| Naive LLM's files | unixfun/18 | 0.19 | 0.33 | yes | yes |
| Naive LLM's files | unixfun/19 | 0.21 | 0.22 | yes | yes |
| Naive LLM's files | unixfun/2 | 0.28 | 0.30 | yes | yes |
| Naive LLM's files | unixfun/20 | 0.17 | 0.17 | yes | yes |
| Naive LLM's files | unixfun/21 | 0.55 | 0.64 | yes | yes |
| Naive LLM's files | unixfun/23 | 0.27 | 0.55 | yes | yes |
| Naive LLM's files | unixfun/24 | 0.18 | 0.26 | yes | yes |
| Naive LLM's files | unixfun/25 | 0.17 | 0.25 | yes | yes |
| Naive LLM's files | unixfun/26 | 0.32 | 0.51 | yes | yes |
| Naive LLM's files | unixfun/28 | 0.38 | 0.60 | yes | yes |
| Naive LLM's files | unixfun/29 | 0.29 | 0.36 | yes | yes |
| Naive LLM's files | unixfun/3 | 0.13 | 0.17 | yes | yes |
| Naive LLM's files | unixfun/30 | 0.33 | 0.54 | yes | yes |
| Naive LLM's files | unixfun/31 | 0.33 | 0.51 | yes | yes |
| Naive LLM's files | unixfun/32 | 0.23 | 0.26 | yes | yes |
| Naive LLM's files | unixfun/33 | 0.20 | 0.25 | yes | yes |
| Naive LLM's files | unixfun/34 | 0.12 | 0.11 | yes | no |
| Naive LLM's files | unixfun/35 | 0.18 | 0.21 | yes | yes |
| Naive LLM's files | unixfun/36 | 0.19 | 0.16 | yes | no |
| Naive LLM's files | unixfun/4 | 0.34 | 0.37 | yes | yes |
| Naive LLM's files | unixfun/5 | 0.18 | 0.20 | yes | yes |
| Naive LLM's files | unixfun/6 | 0.23 | 0.32 | yes | yes |
| Naive LLM's files | unixfun/7 | 0.19 | 0.31 | yes | yes |
| Naive LLM's files | unixfun/8 | 0.20 | 0.31 | yes | yes |
| Naive LLM's files | unixfun/9 | 0.22 | 0.35 | yes | yes |
| Naive LLM's files | weather/temp-analytics | 4.58 | 4.44 | yes | no |
| Naive LLM's files | weather/tuft-weather | 465.99 | 470.08 | yes | no |
| Naive LLM's files | web-search/engine | 710.06 | 706.69 | yes | no |
| Caruca's files, PaSh grammar | analytics/nginx | 1.48 | 1.46 | yes | no |
| Caruca's files, PaSh grammar | analytics/pcaps | 106.15 | 100.33 | yes | no |
| Caruca's files, PaSh grammar | analytics/ray-tracing | 0.12 | 0.12 | yes | no |
| Caruca's files, PaSh grammar | bio/bio | 0.28 | 0.26 | yes | no |
| Caruca's files, PaSh grammar | covid/1 | 6.73 | 10.37 | yes | yes |
| Caruca's files, PaSh grammar | covid/2 | 7.14 | 10.62 | yes | yes |
| Caruca's files, PaSh grammar | covid/3 | 7.50 | 14.83 | yes | yes |
| Caruca's files, PaSh grammar | covid/4 | 6.67 | 12.49 | yes | yes |
| Caruca's files, PaSh grammar | covid/5 | 11.13 | 10.97 | yes | no |
| Caruca's files, PaSh grammar | file-mod/compress_files | 19.49 | 19.22 | yes | no |
| Caruca's files, PaSh grammar | file-mod/encrypt_files | 2.73 | 2.65 | yes | no |
| Caruca's files, PaSh grammar | file-mod/img_convert | 35.81 | 35.57 | yes | no |
| Caruca's files, PaSh grammar | file-mod/thumbnail_generation | 11.22 | 11.04 | yes | no |
| Caruca's files, PaSh grammar | file-mod/to_mp3 | 9.34 | 9.02 | yes | no |
| Caruca's files, PaSh grammar | nlp/bigrams | 69.41 | 71.97 | yes | no |
| Caruca's files, PaSh grammar | nlp/bigrams_appear_twice | 79.45 | 78.75 | yes | no |
| Caruca's files, PaSh grammar | nlp/compare_exodus_genesis | 108.74 | 109.14 | yes | no |
| Caruca's files, PaSh grammar | nlp/count_consonant_seq | 65.05 | 62.05 | yes | no |
| Caruca's files, PaSh grammar | nlp/count_morphs | 25.07 | 25.78 | yes | no |
| Caruca's files, PaSh grammar | nlp/count_trigrams | 74.53 | 79.49 | yes | no |
| Caruca's files, PaSh grammar | nlp/count_vowel_seq | 26.52 | 27.55 | yes | no |
| Caruca's files, PaSh grammar | nlp/count_words | 47.92 | 47.18 | yes | no |
| Caruca's files, PaSh grammar | nlp/find_anagrams | 63.43 | 63.86 | yes | no |
| Caruca's files, PaSh grammar | nlp/letter_words | 76.58 | 76.92 | yes | no |
| Caruca's files, PaSh grammar | nlp/merge_upper | 48.16 | 47.72 | yes | no |
| Caruca's files, PaSh grammar | nlp/sort | 51.50 | 51.01 | yes | no |
| Caruca's files, PaSh grammar | nlp/sort_words_by_folding | 51.30 | 50.62 | yes | no |
| Caruca's files, PaSh grammar | nlp/sort_words_by_num_of_syllables | 58.08 | 58.79 | yes | no |
| Caruca's files, PaSh grammar | nlp/sort_words_by_rhyming | 52.19 | 51.97 | yes | no |
| Caruca's files, PaSh grammar | nlp/syllable_words_1 | 36.06 | 34.69 | yes | no |
| Caruca's files, PaSh grammar | nlp/syllable_words_2 | 30.55 | 29.06 | yes | no |
| Caruca's files, PaSh grammar | nlp/trigram_rec | 53.11 | 45.19 | yes | no |
| Caruca's files, PaSh grammar | nlp/uppercase_by_token | 27.10 | 26.90 | yes | no |
| Caruca's files, PaSh grammar | nlp/uppercase_by_type | 46.16 | 45.33 | yes | no |
| Caruca's files, PaSh grammar | nlp/verses_2om_3om_2instances | 56.36 | 58.13 | yes | no |
| Caruca's files, PaSh grammar | nlp/vowel_sequencies_gr_1K | 49.89 | 48.63 | yes | no |
| Caruca's files, PaSh grammar | nlp/words_no_vowels | 27.42 | 27.50 | yes | no |
| Caruca's files, PaSh grammar | oneliners/bi-grams | 1.30 | 1.31 | yes | no |
| Caruca's files, PaSh grammar | oneliners/comm | 0.13 | 0.12 | yes | no |
| Caruca's files, PaSh grammar | oneliners/diff | 0.43 | 0.40 | yes | no |
| Caruca's files, PaSh grammar | oneliners/nfa-regex | 1.94 | 1.87 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/opt-parallel | 0.25 | 0.21 | yes | no |
| Caruca's files, PaSh grammar | oneliners/set-diff | 0.35 | 0.35 | yes | no |
| Caruca's files, PaSh grammar | oneliners/sort | 0.24 | 0.23 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/sort-sort | 0.36 | 0.28 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/spell | 0.63 | 1.11 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/top-n | 0.59 | 0.98 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/uniq-ips | 0.18 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/wf | 0.50 | 0.99 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/1 | 0.20 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/10 | 0.33 | 0.17 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/11 | 0.37 | 0.17 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/12 | 0.41 | 0.39 | yes | no |
| Caruca's files, PaSh grammar | unixfun/13 | 0.23 | 0.26 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/14 | 0.63 | 0.94 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/15 | 0.19 | 0.22 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/16 | 0.28 | 0.28 | yes | no |
| Caruca's files, PaSh grammar | unixfun/17 | 0.35 | 0.27 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/18 | 0.19 | 0.21 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/19 | 0.21 | 0.23 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/2 | 0.28 | 0.39 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/20 | 0.17 | 0.17 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/21 | 0.55 | 1.11 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/23 | 0.27 | 0.27 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/24 | 0.18 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/25 | 0.17 | 0.19 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/26 | 0.32 | 0.29 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/28 | 0.38 | 0.39 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/29 | 0.29 | 0.28 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/3 | 0.13 | 0.17 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/30 | 0.33 | 0.34 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/31 | 0.33 | 0.34 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/32 | 0.23 | 0.24 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/33 | 0.20 | 0.25 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/34 | 0.12 | 0.11 | yes | no |
| Caruca's files, PaSh grammar | unixfun/35 | 0.18 | 0.19 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/36 | 0.19 | 0.16 | yes | no |
| Caruca's files, PaSh grammar | unixfun/4 | 0.34 | 0.36 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/5 | 0.18 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/6 | 0.23 | 0.27 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/7 | 0.19 | 0.22 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/8 | 0.20 | 0.20 | yes | yes |
| Caruca's files, PaSh grammar | unixfun/9 | 0.22 | 0.23 | yes | yes |
| Caruca's files, PaSh grammar | weather/temp-analytics | 4.58 | 4.53 | yes | no |
| Caruca's files, PaSh grammar | weather/tuft-weather | 465.99 | 463.27 | yes | no |
| Caruca's files, PaSh grammar | web-search/engine | 710.06 | 697.52 | yes | no |
| Caruca's files, main grammar | analytics/nginx | 1.48 | 1.48 | yes | no |
| Caruca's files, main grammar | analytics/pcaps | 106.15 | 100.46 | yes | no |
| Caruca's files, main grammar | analytics/ray-tracing | 0.12 | 0.12 | yes | no |
| Caruca's files, main grammar | bio/bio | 0.28 | 0.26 | yes | no |
| Caruca's files, main grammar | covid/1 | 6.73 | 7.76 | yes | yes |
| Caruca's files, main grammar | covid/2 | 7.14 | 8.21 | yes | yes |
| Caruca's files, main grammar | covid/3 | 7.50 | 8.38 | yes | yes |
| Caruca's files, main grammar | covid/4 | 6.67 | 7.36 | yes | yes |
| Caruca's files, main grammar | covid/5 | 11.13 | 11.31 | yes | no |
| Caruca's files, main grammar | file-mod/compress_files | 19.49 | 19.20 | yes | no |
| Caruca's files, main grammar | file-mod/encrypt_files | 2.73 | 2.94 | yes | no |
| Caruca's files, main grammar | file-mod/img_convert | 35.81 | 35.96 | yes | no |
| Caruca's files, main grammar | file-mod/thumbnail_generation | 11.22 | 10.91 | yes | no |
| Caruca's files, main grammar | file-mod/to_mp3 | 9.34 | 8.95 | yes | no |
| Caruca's files, main grammar | nlp/bigrams | 69.41 | 74.63 | yes | no |
| Caruca's files, main grammar | nlp/bigrams_appear_twice | 79.45 | 78.43 | yes | no |
| Caruca's files, main grammar | nlp/compare_exodus_genesis | 108.74 | 109.21 | yes | no |
| Caruca's files, main grammar | nlp/count_consonant_seq | 65.05 | 63.84 | yes | no |
| Caruca's files, main grammar | nlp/count_morphs | 25.07 | 26.15 | yes | no |
| Caruca's files, main grammar | nlp/count_trigrams | 74.53 | 74.53 | yes | no |
| Caruca's files, main grammar | nlp/count_vowel_seq | 26.52 | 26.46 | yes | no |
| Caruca's files, main grammar | nlp/count_words | 47.92 | 48.44 | yes | no |
| Caruca's files, main grammar | nlp/find_anagrams | 63.43 | 65.02 | yes | no |
| Caruca's files, main grammar | nlp/letter_words | 76.58 | 78.50 | yes | no |
| Caruca's files, main grammar | nlp/merge_upper | 48.16 | 47.90 | yes | no |
| Caruca's files, main grammar | nlp/sort | 51.50 | 53.33 | yes | no |
| Caruca's files, main grammar | nlp/sort_words_by_folding | 51.30 | 50.68 | yes | no |
| Caruca's files, main grammar | nlp/sort_words_by_num_of_syllables | 58.08 | 61.45 | yes | no |
| Caruca's files, main grammar | nlp/sort_words_by_rhyming | 52.19 | 52.05 | yes | no |
| Caruca's files, main grammar | nlp/syllable_words_1 | 36.06 | 34.82 | yes | no |
| Caruca's files, main grammar | nlp/syllable_words_2 | 30.55 | 29.73 | yes | no |
| Caruca's files, main grammar | nlp/trigram_rec | 53.11 | 45.33 | yes | no |
| Caruca's files, main grammar | nlp/uppercase_by_token | 27.10 | 27.10 | yes | no |
| Caruca's files, main grammar | nlp/uppercase_by_type | 46.16 | 45.72 | yes | no |
| Caruca's files, main grammar | nlp/verses_2om_3om_2instances | 56.36 | 55.80 | yes | no |
| Caruca's files, main grammar | nlp/vowel_sequencies_gr_1K | 49.89 | 48.66 | yes | no |
| Caruca's files, main grammar | nlp/words_no_vowels | 27.42 | 27.81 | yes | no |
| Caruca's files, main grammar | oneliners/bi-grams | 1.30 | 1.32 | yes | no |
| Caruca's files, main grammar | oneliners/comm | 0.13 | 0.12 | yes | no |
| Caruca's files, main grammar | oneliners/diff | 0.43 | 0.40 | yes | no |
| Caruca's files, main grammar | oneliners/nfa-regex | 1.94 | 1.88 | yes | yes |
| Caruca's files, main grammar | oneliners/opt-parallel | 0.25 | 0.20 | yes | no |
| Caruca's files, main grammar | oneliners/set-diff | 0.35 | 0.35 | yes | no |
| Caruca's files, main grammar | oneliners/sort | 0.24 | 0.27 | yes | yes |
| Caruca's files, main grammar | oneliners/sort-sort | 0.36 | 0.32 | yes | yes |
| Caruca's files, main grammar | oneliners/spell | 0.63 | 1.09 | yes | yes |
| Caruca's files, main grammar | oneliners/top-n | 0.59 | 1.00 | yes | yes |
| Caruca's files, main grammar | oneliners/uniq-ips | 0.18 | 0.19 | yes | yes |
| Caruca's files, main grammar | oneliners/wf | 0.50 | 0.92 | yes | yes |
| Caruca's files, main grammar | unixfun/1 | 0.20 | 0.22 | yes | yes |
| Caruca's files, main grammar | unixfun/10 | 0.33 | 0.26 | yes | yes |
| Caruca's files, main grammar | unixfun/11 | 0.37 | 0.29 | yes | yes |
| Caruca's files, main grammar | unixfun/12 | 0.41 | 0.39 | yes | no |
| Caruca's files, main grammar | unixfun/13 | 0.23 | 0.26 | yes | yes |
| Caruca's files, main grammar | unixfun/14 | 0.63 | 1.20 | yes | yes |
| Caruca's files, main grammar | unixfun/15 | 0.19 | 0.22 | yes | yes |
| Caruca's files, main grammar | unixfun/16 | 0.28 | 0.28 | yes | no |
| Caruca's files, main grammar | unixfun/17 | 0.35 | 0.37 | yes | yes |
| Caruca's files, main grammar | unixfun/18 | 0.19 | 0.21 | yes | yes |
| Caruca's files, main grammar | unixfun/19 | 0.21 | 0.22 | yes | yes |
| Caruca's files, main grammar | unixfun/2 | 0.28 | 0.39 | yes | yes |
| Caruca's files, main grammar | unixfun/20 | 0.17 | 0.17 | yes | yes |
| Caruca's files, main grammar | unixfun/21 | 0.55 | 1.11 | yes | yes |
| Caruca's files, main grammar | unixfun/23 | 0.27 | 0.28 | yes | yes |
| Caruca's files, main grammar | unixfun/24 | 0.18 | 0.20 | yes | yes |
| Caruca's files, main grammar | unixfun/25 | 0.17 | 0.18 | yes | yes |
| Caruca's files, main grammar | unixfun/26 | 0.32 | 0.29 | yes | yes |
| Caruca's files, main grammar | unixfun/28 | 0.38 | 0.40 | yes | yes |
| Caruca's files, main grammar | unixfun/29 | 0.29 | 0.32 | yes | yes |
| Caruca's files, main grammar | unixfun/3 | 0.13 | 0.17 | yes | yes |
| Caruca's files, main grammar | unixfun/30 | 0.33 | 0.34 | yes | yes |
| Caruca's files, main grammar | unixfun/31 | 0.33 | 0.33 | yes | yes |
| Caruca's files, main grammar | unixfun/32 | 0.23 | 0.27 | yes | yes |
| Caruca's files, main grammar | unixfun/33 | 0.20 | 0.25 | yes | yes |
| Caruca's files, main grammar | unixfun/34 | 0.12 | 0.11 | yes | no |
| Caruca's files, main grammar | unixfun/35 | 0.18 | 0.20 | yes | yes |
| Caruca's files, main grammar | unixfun/36 | 0.19 | 0.15 | yes | no |
| Caruca's files, main grammar | unixfun/4 | 0.34 | 0.42 | yes | yes |
| Caruca's files, main grammar | unixfun/5 | 0.18 | 0.20 | yes | yes |
| Caruca's files, main grammar | unixfun/6 | 0.23 | 0.26 | yes | yes |
| Caruca's files, main grammar | unixfun/7 | 0.19 | 0.22 | yes | yes |
| Caruca's files, main grammar | unixfun/8 | 0.20 | 0.22 | yes | yes |
| Caruca's files, main grammar | unixfun/9 | 0.22 | 0.26 | yes | yes |
| Caruca's files, main grammar | weather/temp-analytics | 4.58 | 4.53 | yes | no |
| Caruca's files, main grammar | weather/tuft-weather | 465.99 | 463.59 | yes | no |
| Caruca's files, main grammar | web-search/engine | 710.06 | 686.76 | yes | no |

## Chart C data: which of the suite's commands each source has files for

- PaSh's own files: 19 of 45 commands (cat, tr, sort, grep, uniq, cut, head, sed, xargs, awk, rm, tail, wc, comm, mkfifo, tee, col, diff, seq)
- Naive LLM's files: 28 of 45 commands (cat, tr, sort, grep, uniq, cut, head, mkdir, sed, xargs, ls, awk, rm, mktemp, tail, wc, comm, mkfifo, fmt, rev, tee, col, convert, diff, iconv, join, mogrify, seq)
- Caruca's files (both grammars): 6 of 45 commands (cat, sort, grep, cut, rm, wc)
- Files from nobody: 17 of 45 (basename, paste,         if (!(key in max) || $3 > max[key]) max[key] = $3;
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
    },    PROCINFO["sorted_in"] = "@ind_str_asc"
   for (d in day)
     printf("\t%s", d);
   printf("\n");
   for (b in bus) {
     printf("%s", b);
     for (d in day)
       printf("\t%s", hours[d b]);
     printf("\n");
   }
}, bigrams_aux, dirname, egrep, ffmpeg, find, git, gzip, mawk, node, openssl, python3, samtools, tcpdump)
- Scripts using each command (of 86): cat 80, tr 50, sort 48, grep 47, uniq 37, cut 35, head 32, mkdir 31, basename 29, sed 25, xargs 24, ls 23, awk 14, rm 13, mktemp 10, tail 8, paste 6, wc 6, comm 4, mkfifo 3, fmt 2, rev 2, tee 2,         if (!(key in max) || $3 > max[key]) max[key] = $3;
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
    } 1,    PROCINFO["sorted_in"] = "@ind_str_asc"
   for (d in day)
     printf("\t%s", d);
   printf("\n");
   for (b in bus) {
     printf("%s", b);
     for (d in day)
       printf("\t%s", hours[d b]);
     printf("\n");
   }
} 1, bigrams_aux 1, col 1, convert 1, diff 1, dirname 1, egrep 1, ffmpeg 1, find 1, git 1, gzip 1, iconv 1, join 1, mawk 1, mogrify 1, node 1, openssl 1, python3 1, samtools 1, seq 1, tcpdump 1

## Table 4: Next to the Caruca paper's PaSh check

Agreement with PaSh's own files on the suite's own command lines (each distinct command line for which the source has its own files and PaSh's own files exist):

| Source | Command lines | Same inputs and outputs | Same split decision | Commands with every line agreeing | Lines where PaSh's own files give no split answer (left out) | Of the disagreements: PaSh's own split only with a special merge step, source says no split | Lines where the source's files raised an error |
|---|---:|---:|---:|---:|---:|---:|---:|
| Naive LLM's files | 215 | 172 of 178 | 99 of 113 | 3 of 8 | 102 | 0 | 3 |
| Caruca's files, PaSh grammar | 110 | 93 of 110 | 54 of 70 | 0 of 3 | 40 | 7 | 0 |
| Caruca's files, main grammar | 110 | 101 of 110 | 54 of 70 | 0 of 3 | 40 | 7 | 0 |

| What was checked | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| Suite output identical with the files swapped in | 86 of 86 | 86 of 86 | 86 of 86 | 86 of 86 |
| Parts PaSh ran in parallel | 41 of 177 | 43 of 177 | 29 of 177 | 41 of 177 |
| Median speed-up against bash | 0.51x | 0.49x | 0.58x | 0.52x |

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

| Reason | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| missing annotation | 95 / 0 | 61 / 0 | 95 / 0 | 95 / 0 |
| other: not classified | 9 / 0 | 9 / 31 | 7 / 0 | 7 / 0 |
| other: nothing in this part can be split under this source's files | 1 / 0 | 0 / 0 | 1 / 0 | 1 / 0 |
| other: the source has files for a command, but they gave no answer | 0 / 0 | 0 / 0 | 0 / 4 | 0 / 2 |
| pash crash | 4 / 0 | 2 / 2 | 4 / 10 | 4 / 0 |
| refused by annotation | 0 / 0 | 0 / 1 | 0 / 0 | 0 / 0 |
| unsupported construct | 27 / 0 | 27 / 1 | 27 / 0 | 27 / 0 |
| parts considered | 177 | 177 | 177 | 177 |

Per execution (a loop's part counts once per pass). Each cell: the same under PaSh's own files / only with this source.

| Reason | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| missing annotation | 95 / 0 | 61 / 0 | 95 / 0 | 95 / 0 |
| other | 10 / 0 | 9 / 31 | 10 / 2 | 10 / 0 |
| pash crash | 4 / 0 | 2 / 2 | 4 / 10 | 4 / 0 |
| refused by annotation | 0 / 0 | 0 / 1 | 0 / 0 | 0 / 0 |
| unsupported construct | 27 / 0 | 27 / 1 | 27 / 0 | 27 / 0 |
| parts considered | 177 | 177 | 177 | 177 |

## Appendix A4: every use whose result differs from PaSh's own

| Script | Command line | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | Output same as bash |
|---|---|---|---|---|---|---|
| covid/1 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `sed '"s/T..:..:..//"'` | split | whole | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `cut -d '","' -f 1,3` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `sort -u` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `cut -d '","' -f 1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/1 | `awk '"{print $2,$1}"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `sed '"s/T..:..:..//"'` | split | whole | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `cut -d '","' -f 3,1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `sort -u` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `cut -d '","' -f 2` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `sort -k 1 -n` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/2 | `awk '"{print $2,$1}"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `sed '"s/T\(..\):..:../,\1/"'` | split | whole | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `cut -d '","' -f 1,2,4` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `sort -u` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `cut -d '","' -f 3` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `sort -k 1 -n` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/3 | `awk '"{print $2,$1}"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `sed '"s/T\(..\):..:../,\1/"'` | split | whole | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `cut -d '","' -f 1,2` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `sort -u` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `cut -d '","' -f 1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| covid/4 | `awk '"{print $2,$1}"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/nfa-regex | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort-sort | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort-sort | `tr A-Z a-z` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort-sort | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/sort-sort | `sort -r` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `sed '"s/[^[:print:]]//g"'` | split | whole | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `col -bx` | split | whole | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `tr -c '"A-Za-z"' '"[\n*]"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `grep -v '"^\s*$"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `tr A-Z a-z` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `sort -rn` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/top-n | `sed 100q` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/uniq-ips | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/uniq-ips | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `tr -c '"A-Za-z"' '"[\n*]"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `grep -v '"^\s*$"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `tr A-Z a-z` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/wf | `sort -rn` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/1 | `cat ./inputs/1_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `cat ./inputs/4_30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `tr '" "' '"\n"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `grep '"x"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `grep '"\."'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `cut -d '"."' -f 2` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `grep '"[KQRBN]"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `cut -c 1-1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/10 | `sort -nr` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `cat ./inputs/4_30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `tr '" "' '"\n"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `grep '"x"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `grep '"\."'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `cut -d '"."' -f 2` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `cut -c 1-1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `tr '"[a-z]"' '"P"'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/11 | `sort -nr` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `cat ./inputs/4_30M.txt` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `tr '" "' '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `grep '"\."'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `cut -d '"."' -f 2` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `cut -c 1-1` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `tr '"[a-z]"' '"P"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `sort -r` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `uniq` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `head -n 3` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/12 | `tail -n 1` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/13 | `cat ./inputs/5_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/14 | `cat ./inputs/6_30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/14 | `awk '"{print $2, $0}"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/14 | `sort -nr` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/14 | `cut -d '" "' -f 2` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/15 | `cat ./inputs/7_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `cat ./inputs/7_30M.txt` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `cut -f 2` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `sort -n` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `sort -nr` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `head -n 1` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `tr -s '" "' '"\n"'` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/16 | `tail -n 1` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `cat ./inputs/7_30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `cut -f 4` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `sort -n` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `cut -c 3-3` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `uniq` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/17 | `sed 's/$/"0s"/'` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/18 | `cat ./inputs/8_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/19 | `cat ./inputs/8_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/19 | `awk '"length <= 45"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/19 | `awk '"{$1=$1};1"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/2 | `cat ./inputs/1_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/2 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/20 | `cat ./inputs/8_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/21 | `cat ./inputs/8_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/21 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/23 | `cat ./inputs/9.1_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/23 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/24 | `cat ./inputs/9.2_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/24 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/25 | `cat ./inputs/9.3_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/25 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/26 | `cat ./inputs/9.4_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/26 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/28 | `cat ./inputs/9.6_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/28 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/29 | `cat ./inputs/9.7_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/29 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/3 | `cat ./inputs/1_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/30 | `cat ./inputs/9.8_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/30 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/31 | `cat ./inputs/9.9_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/31 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/32 | `cat ./inputs/10_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/33 | `cat ./inputs/10_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/35 | `cat ./inputs/11_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/4 | `cat ./inputs/1_30M.txt` | whole | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/4 | `cut -d '" "' -f 1` | split | split | whole | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/4 | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/4 | `uniq -c` | whole | whole | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/4 | `sort -r` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/5 | `cat ./inputs/2_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/6 | `cat ./inputs/3_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/6 | `tr -d '"\n"'` | whole | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/7 | `cat ./inputs/4_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/8 | `cat ./inputs/4_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| unixfun/9 | `cat ./inputs/4_30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |

Why the use was left whole, where it was:

- covid/1 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/1 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `sed '"s/T..:..:..//"'`, Naive LLM's files: file says no split
- covid/1 `sed '"s/T..:..:..//"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `cut -d '","' -f 1,3`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `sort -u`, PaSh's own files: file says no split
- covid/1 `sort -u`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `sort -u`, Caruca's files, main grammar: file says no split
- covid/1 `cut -d '","' -f 1`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `sort`, Caruca's files, main grammar: file says no split
- covid/1 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/1 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- covid/1 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- covid/1 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/1 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/1 `awk '"{print $2,$1}"'`, Caruca's files, main grammar: no answer
- covid/2 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/2 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sed '"s/T..:..:..//"'`, Naive LLM's files: file says no split
- covid/2 `sed '"s/T..:..:..//"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `cut -d '","' -f 3,1`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sort -u`, PaSh's own files: file says no split
- covid/2 `sort -u`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sort -u`, Caruca's files, main grammar: file says no split
- covid/2 `cut -d '","' -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sort`, Caruca's files, main grammar: file says no split
- covid/2 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/2 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- covid/2 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- covid/2 `sort -k 1 -n`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `sort -k 1 -n`, Caruca's files, main grammar: file says no split
- covid/2 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/2 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/2 `awk '"{print $2,$1}"'`, Caruca's files, main grammar: no answer
- covid/3 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/3 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sed '"s/T\(..\):..:../,\1/"'`, Naive LLM's files: file says no split
- covid/3 `sed '"s/T\(..\):..:../,\1/"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `cut -d '","' -f 1,2,4`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sort -u`, PaSh's own files: file says no split
- covid/3 `sort -u`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sort -u`, Caruca's files, main grammar: file says no split
- covid/3 `cut -d '","' -f 3`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sort`, Caruca's files, main grammar: file says no split
- covid/3 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/3 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- covid/3 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- covid/3 `sort -k 1 -n`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `sort -k 1 -n`, Caruca's files, main grammar: file says no split
- covid/3 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/3 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/3 `awk '"{print $2,$1}"'`, Caruca's files, main grammar: no answer
- covid/4 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, PaSh's own files: no answer
- covid/4 `cat '"~/t024/shadow/covid/inputs/in_small.csv"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `sed '"s/T\(..\):..:../,\1/"'`, Naive LLM's files: file says no split
- covid/4 `sed '"s/T\(..\):..:../,\1/"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `cut -d '","' -f 1,2`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `sort -u`, PaSh's own files: file says no split
- covid/4 `sort -u`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `sort -u`, Caruca's files, main grammar: file says no split
- covid/4 `cut -d '","' -f 1`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `sort`, Caruca's files, main grammar: file says no split
- covid/4 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- covid/4 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- covid/4 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- covid/4 `awk '"{print $2,$1}"'`, PaSh's own files: no answer
- covid/4 `awk '"{print $2,$1}"'`, Caruca's files, PaSh grammar: part not run in parallel
- covid/4 `awk '"{print $2,$1}"'`, Caruca's files, main grammar: no answer
- oneliners/nfa-regex `cat ~/t024/shadow/oneliners/inputs/10M.txt`, PaSh's own files: no answer
- oneliners/sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/sort `sort`, Caruca's files, PaSh grammar: file says no split
- oneliners/sort `sort`, Caruca's files, main grammar: file says no split
- oneliners/sort-sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/sort-sort `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/sort-sort `tr A-Z a-z`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/sort-sort `sort`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/sort-sort `sort`, Caruca's files, main grammar: file says no split
- oneliners/sort-sort `sort -r`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/sort-sort `sort -r`, Caruca's files, main grammar: file says no split
- oneliners/spell `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/spell `sed '"s/[^[:print:]]//g"'`, Naive LLM's files: file says no split
- oneliners/spell `col -bx`, Naive LLM's files: file says no split
- oneliners/spell `sort`, Caruca's files, PaSh grammar: file says no split
- oneliners/spell `sort`, Caruca's files, main grammar: file says no split
- oneliners/top-n `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/top-n `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `grep -v '"^\s*$"'`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `tr A-Z a-z`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `sort`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `sort`, Caruca's files, main grammar: file says no split
- oneliners/top-n `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/top-n `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- oneliners/top-n `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- oneliners/top-n `sort -rn`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `sort -rn`, Caruca's files, main grammar: file says no split
- oneliners/top-n `sed 100q`, PaSh's own files: file says no split
- oneliners/top-n `sed 100q`, Naive LLM's files: file says no split
- oneliners/top-n `sed 100q`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/top-n `sed 100q`, Caruca's files, main grammar: file says no split
- oneliners/uniq-ips `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'`, PaSh's own files: no answer
- oneliners/uniq-ips `sort`, Caruca's files, PaSh grammar: file says no split
- oneliners/uniq-ips `sort`, Caruca's files, main grammar: file says no split
- oneliners/wf `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/wf `cat ~/t024/shadow/oneliners/inputs/30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `tr -c '"A-Za-z"' '"[\n*]"'`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `grep -v '"^\s*$"'`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `tr A-Z a-z`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `sort`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `sort`, Caruca's files, main grammar: file says no split
- oneliners/wf `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- oneliners/wf `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- oneliners/wf `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- oneliners/wf `sort -rn`, Caruca's files, PaSh grammar: part not run in parallel
- oneliners/wf `sort -rn`, Caruca's files, main grammar: file says no split
- unixfun/1 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/10 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/10 `cat ./inputs/4_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `tr '" "' '"\n"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `grep '"x"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `grep '"\."'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `cut -d '"."' -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `grep '"[KQRBN]"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `cut -c 1-1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `sort`, Caruca's files, main grammar: file says no split
- unixfun/10 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/10 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/10 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/10 `sort -nr`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/10 `sort -nr`, Caruca's files, main grammar: file says no split
- unixfun/11 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/11 `cat ./inputs/4_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `tr '" "' '"\n"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `grep '"x"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `grep '"\."'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `cut -d '"."' -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `cut -c 1-1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `tr '"[a-z]"' '"P"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `sort`, Caruca's files, main grammar: file says no split
- unixfun/11 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/11 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/11 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/11 `sort -nr`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/11 `sort -nr`, Caruca's files, main grammar: file says no split
- unixfun/12 `cat ./inputs/4_30M.txt`, PaSh's own files: part not run in parallel
- unixfun/12 `cat ./inputs/4_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `cat ./inputs/4_30M.txt`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `tr '" "' '"\n"'`, PaSh's own files: part not run in parallel
- unixfun/12 `tr '" "' '"\n"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `tr '" "' '"\n"'`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `grep '"\."'`, PaSh's own files: part not run in parallel
- unixfun/12 `grep '"\."'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `grep '"\."'`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `cut -d '"."' -f 2`, PaSh's own files: part not run in parallel
- unixfun/12 `cut -d '"."' -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `cut -d '"."' -f 2`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `cut -c 1-1`, PaSh's own files: part not run in parallel
- unixfun/12 `cut -c 1-1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `cut -c 1-1`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `tr '"[a-z]"' '"P"'`, PaSh's own files: part not run in parallel
- unixfun/12 `tr '"[a-z]"' '"P"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `tr '"[a-z]"' '"P"'`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `sort -r`, PaSh's own files: part not run in parallel
- unixfun/12 `sort -r`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `sort -r`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `uniq`, PaSh's own files: part not run in parallel
- unixfun/12 `uniq`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/12 `uniq`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `uniq`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `head -n 3`, PaSh's own files: part not run in parallel
- unixfun/12 `head -n 3`, Naive LLM's files: file says no split
- unixfun/12 `head -n 3`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `head -n 3`, Caruca's files, main grammar: part not run in parallel
- unixfun/12 `tail -n 1`, PaSh's own files: part not run in parallel
- unixfun/12 `tail -n 1`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/12 `tail -n 1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/12 `tail -n 1`, Caruca's files, main grammar: part not run in parallel
- unixfun/13 `cat ./inputs/5_30M.txt`, PaSh's own files: no answer
- unixfun/14 `cat ./inputs/6_30M.txt`, PaSh's own files: no answer
- unixfun/14 `cat ./inputs/6_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/14 `awk '"{print $2, $0}"'`, PaSh's own files: no answer
- unixfun/14 `awk '"{print $2, $0}"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/14 `awk '"{print $2, $0}"'`, Caruca's files, main grammar: no answer
- unixfun/14 `sort -nr`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/14 `sort -nr`, Caruca's files, main grammar: file says no split
- unixfun/14 `cut -d '" "' -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/15 `cat ./inputs/7_30M.txt`, PaSh's own files: no answer
- unixfun/16 `cat ./inputs/7_30M.txt`, PaSh's own files: part not run in parallel
- unixfun/16 `cat ./inputs/7_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `cat ./inputs/7_30M.txt`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `cut -f 2`, PaSh's own files: part not run in parallel
- unixfun/16 `cut -f 2`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `cut -f 2`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `sort -n`, PaSh's own files: part not run in parallel
- unixfun/16 `sort -n`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `sort -n`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `uniq -c`, PaSh's own files: part not run in parallel
- unixfun/16 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/16 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `uniq -c`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `sort -nr`, PaSh's own files: part not run in parallel
- unixfun/16 `sort -nr`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `sort -nr`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `head -n 1`, PaSh's own files: part not run in parallel
- unixfun/16 `head -n 1`, Naive LLM's files: file says no split
- unixfun/16 `head -n 1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `head -n 1`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `tr -s '" "' '"\n"'`, PaSh's own files: part not run in parallel
- unixfun/16 `tr -s '" "' '"\n"'`, Naive LLM's files: file says no split
- unixfun/16 `tr -s '" "' '"\n"'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `tr -s '" "' '"\n"'`, Caruca's files, main grammar: part not run in parallel
- unixfun/16 `tail -n 1`, PaSh's own files: part not run in parallel
- unixfun/16 `tail -n 1`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/16 `tail -n 1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/16 `tail -n 1`, Caruca's files, main grammar: part not run in parallel
- unixfun/17 `cat ./inputs/7_30M.txt`, PaSh's own files: no answer
- unixfun/17 `cat ./inputs/7_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/17 `cut -f 4`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/17 `sort -n`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/17 `sort -n`, Caruca's files, main grammar: file says no split
- unixfun/17 `cut -c 3-3`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/17 `uniq`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/17 `uniq`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/17 `uniq`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/17 `uniq`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/17 `sed 's/$/"0s"/'`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/18 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/19 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/19 `awk '"length <= 45"'`, PaSh's own files: no answer
- unixfun/19 `awk '"length <= 45"'`, Caruca's files, PaSh grammar: no answer
- unixfun/19 `awk '"length <= 45"'`, Caruca's files, main grammar: no answer
- unixfun/19 `awk '"{$1=$1};1"'`, PaSh's own files: no answer
- unixfun/19 `awk '"{$1=$1};1"'`, Caruca's files, PaSh grammar: no answer
- unixfun/19 `awk '"{$1=$1};1"'`, Caruca's files, main grammar: no answer
- unixfun/2 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/2 `sort`, Caruca's files, PaSh grammar: file says no split
- unixfun/2 `sort`, Caruca's files, main grammar: file says no split
- unixfun/20 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/21 `cat ./inputs/8_30M.txt`, PaSh's own files: no answer
- unixfun/21 `sort`, Caruca's files, PaSh grammar: file says no split
- unixfun/21 `sort`, Caruca's files, main grammar: file says no split
- unixfun/23 `cat ./inputs/9.1_30M.txt`, PaSh's own files: no answer
- unixfun/23 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/23 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/23 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/24 `cat ./inputs/9.2_30M.txt`, PaSh's own files: no answer
- unixfun/24 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/24 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/24 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/25 `cat ./inputs/9.3_30M.txt`, PaSh's own files: no answer
- unixfun/25 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/25 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/25 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/26 `cat ./inputs/9.4_30M.txt`, PaSh's own files: no answer
- unixfun/26 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/26 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/26 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/28 `cat ./inputs/9.6_30M.txt`, PaSh's own files: no answer
- unixfun/28 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/28 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/28 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/29 `cat ./inputs/9.7_30M.txt`, PaSh's own files: no answer
- unixfun/29 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/29 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/29 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/3 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/30 `cat ./inputs/9.8_30M.txt`, PaSh's own files: no answer
- unixfun/30 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/30 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/30 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/31 `cat ./inputs/9.9_30M.txt`, PaSh's own files: no answer
- unixfun/31 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/31 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/31 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/32 `cat ./inputs/10_30M.txt`, PaSh's own files: no answer
- unixfun/33 `cat ./inputs/10_30M.txt`, PaSh's own files: no answer
- unixfun/35 `cat ./inputs/11_30M.txt`, PaSh's own files: no answer
- unixfun/4 `cat ./inputs/1_30M.txt`, PaSh's own files: no answer
- unixfun/4 `cat ./inputs/1_30M.txt`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/4 `cut -d '" "' -f 1`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/4 `sort`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/4 `sort`, Caruca's files, main grammar: file says no split
- unixfun/4 `uniq -c`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/4 `uniq -c`, Naive LLM's files: file allows only a split PaSh has not implemented
- unixfun/4 `uniq -c`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/4 `uniq -c`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/4 `sort -r`, Caruca's files, PaSh grammar: part not run in parallel
- unixfun/4 `sort -r`, Caruca's files, main grammar: file says no split
- unixfun/5 `cat ./inputs/2_30M.txt`, PaSh's own files: no answer
- unixfun/6 `cat ./inputs/3_30M.txt`, PaSh's own files: no answer
- unixfun/6 `tr -d '"\n"'`, PaSh's own files: file allows only a split PaSh has not implemented
- unixfun/6 `tr -d '"\n"'`, Caruca's files, PaSh grammar: file allows only a split PaSh has not implemented
- unixfun/6 `tr -d '"\n"'`, Caruca's files, main grammar: file allows only a split PaSh has not implemented
- unixfun/7 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/8 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer
- unixfun/9 `cat ./inputs/4_30M.txt`, PaSh's own files: no answer

The files' answers on each command line the source has its own files for:

| Source | Command line | Same inputs and outputs | Source's answer | PaSh's own answer |
|---|---|---|---|---|
| Naive LLM's files | `awk '"$1 >= 1000"'` | yes | says no split | no answer |
| Naive LLM's files | `awk '"length <= 45"'` | yes | allows a split | no answer |
| Naive LLM's files | `awk '"length >= 16"'` | yes | says no split | no answer |
| Naive LLM's files | `awk '"{
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
| Naive LLM's files | `awk '"{ printf "%02d-%02d %s %s\n", $1, $2, $3, $4 }"'` | yes | allows a split | no answer |
| Naive LLM's files | `awk '"{ total += $1; count++ } END { print total/count }"'` | yes | says no split | no answer |
| Naive LLM's files | `awk '"{$1=$1};1"'` | yes | says no split | no answer |
| Naive LLM's files | `awk '"{print $2, $0}"'` | yes | allows a split | no answer |
| Naive LLM's files | `awk '"{print $2,$1}"'` | yes | allows a split | no answer |
| Naive LLM's files | `awk -F '"\t"' '"{print $6}"' '"~/t024/shadow/weather/inputs/tuft_weather.small.txt"'` | **no** | allows a split | no answer |
| Naive LLM's files | `awk -F, '"
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
}"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"${OUT}/urls.txt"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"${OUT}/visited.txt"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"${formatted}"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"${input}"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small"/*.INFO'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small/1.INFO"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/analytics/outputs/ray_tracing_small/rays.csv"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/file-mod/inputs/jpg_small/jpg/119901.jpg"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '"~/t024/shadow/weather/inputs/temperatures.small.txt"'` | yes | allows a split | no answer |
| Naive LLM's files | `cat '~/t024/shadow/file-mod/inputs/wav_small/file_example_WAV_5MG.wav.~9~'` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/10_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/11_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/1_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/2_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/3_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/4_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/5_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/6_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/7_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/8_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.1_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.2_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.3_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.4_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.6_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.7_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.8_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ./inputs/9.9_30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat inputs/bio-min/input_min.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/analytics/inputs/nginx-logs_small/log7` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/analytics/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/file-mod/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/nlp/inputs/pg-small/ynkgt10.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `col -bx` | yes | says no split | allows a split |
| Naive LLM's files | `comm '"~/t024/shadow/oneliners/inputs/comm_small/file1"' '"~/t024/shadow/oneliners/inputs/comm_small/file2"'` | yes | says no split | no answer |
| Naive LLM's files | `comm -12 '"${yr_txt}"' -` | yes | says no split | no answer |
| Naive LLM's files | `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt` | yes | says no split | no answer |
| Naive LLM's files | `comm -23 s1 s2` | yes | says no split | no answer |
| Naive LLM's files | `cut '-d" "' -f1,2 '"${processed}"'` | yes | allows a split | allows a split |
| Naive LLM's files | `cut '-d" "' -f1,3` | yes | allows a split | allows a split |
| Naive LLM's files | `cut '-d" "' -f1,3 '"${processed}"'` | yes | allows a split | allows a split |
| Naive LLM's files | `cut '-d" "' -f2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 1-1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 1-12` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 1-2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 1-4` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 3-3` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 7-` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -c 89-92` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '" "' -f 1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '" "' -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '" "' -f 4` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '"""' -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '"("' -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '")"' -f 1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 1,2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 1,2,4` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 1,3` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 3` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '","' -f 3,1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -d '"."' -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -f 1` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -f 1 -d '" "'` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -f 2` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -f 2 ./Gene_locs.txt` | yes | allows a split | allows a split |
| Naive LLM's files | `cut -f 4` | yes | allows a split | allows a split |
| Naive LLM's files | `diff -B s1 s2` | yes | says no split | no answer |
| Naive LLM's files | `fmt -w1` | – | allows a split | no files |
| Naive LLM's files | `grep '" ${year}"' '"${formatted}"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"""'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"${city}"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"("'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"AT&T"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"And he said"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"Bell"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"UNIX"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"[A-Z]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"[KQRBN]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"\."'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"\[RAY\]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"light.\*light"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"print"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"the land of"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep '"x"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -c '"^....$"'` | yes | says no split | says no split |
| Naive LLM's files | `grep -c '"^[A-Z]"'` | yes | says no split | says no split |
| Naive LLM's files | `grep -c '"light.\*light"'` | yes | says no split | says no split |
| Naive LLM's files | `grep -c '"light.\*light.\*light"'` | yes | says no split | says no split |
| Naive LLM's files | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*$"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]$"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v '"NA"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v '"[KQRBN]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v '"\-99"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v '"^\s*$"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v 999` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -v pathID` | yes | allows a split | allows a split |
| Naive LLM's files | `grep -vc '"light.\*light.\*light"'` | yes | says no split | says no split |
| Naive LLM's files | `grep -vi '"[aeiou]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `grep 1969` | yes | allows a split | allows a split |
| Naive LLM's files | `head -n 1` | yes | says no split | no answer |
| Naive LLM's files | `head -n 2` | yes | says no split | no answer |
| Naive LLM's files | `head -n 3` | yes | says no split | no answer |
| Naive LLM's files | `head -n1` | yes | allows only a split PaSh has not implemented | no answer |
| Naive LLM's files | `head -n1 '"${formatted}"'` | yes | says no split | no answer |
| Naive LLM's files | `join -1 1 -2 1 -e '"NA"' '"${processed}"' '"${j2}"'` | – | says no split | no files |
| Naive LLM's files | `join -a1 -a2 -e '"-99"' -o '"0,1.2,1.3,2.2"' '"${j1}"' '"${max_y}"'` | – | raised | no files |
| Naive LLM's files | `join -a1 -a2 -e '"-99"' -o '"0,1.2,2.2"' '"${yr_txt}"' '"${min_y}"'` | – | raised | no files |
| Naive LLM's files | `mkdir -p '"./outputs/bigrams/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/bigrams_appear_twice/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/count_consonant_seq/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/count_morphs/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/count_trigrams/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/count_vowel_seq/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/count_words/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/find_anagrams/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/letter_words/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/merge_upper/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/sort/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/sort_words_by_folding/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/sort_words_by_num_of_syllables/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/sort_words_by_rhyming/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/syllable_words_1/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/syllable_words_2/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/trigram_rec/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/uppercase_by_token/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/uppercase_by_type/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/verses_2om_3om_2instances/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/vowel_sequencies_gr_1K/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"./outputs/words_no_vowels/"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"outputs"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p '"plots/${safe}"' '"${tmp_dir}"'` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ./outputs/compare_exodus_genesis/` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/analytics/outputs/nginx_small` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/analytics/outputs/pcaps_small` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/file-mod/outputs/compress_files.small` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/file-mod/outputs/encrypt_files.small` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/file-mod/outputs/img_convert.small` | – | says no split | no files |
| Naive LLM's files | `mkdir -p ~/t024/shadow/file-mod/outputs/to_mp3.small` | – | says no split | no files |
| Naive LLM's files | `mkfifo s1 s2` | yes | says no split | no answer |
| Naive LLM's files | `mogrify -format gif -path '"~/t024/shadow/file-mod/outputs/thumbnail.small"' -thumbnail 100x100 '~/t024/shadow/file-mod/inputs/jpg_small/jpg/*.jpg'` | – | allows a split | no files |
| Naive LLM's files | `rev` | – | allows a split | no files |
| Naive LLM's files | `rm -f '"${yr_txt}"' '"${max_y}"' '"${min_y}"' '"${j1}"' '"${j2}"'` | yes | says no split | no answer |
| Naive LLM's files | `rm s1 s2` | yes | says no split | no answer |
| Naive LLM's files | `sed '"s/ .*//g"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed '"s/-99/NaN/g"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed '"s/T..:..:..//"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed '"s/T\(..\):..:../,\1/"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed '"s/T\(..\):..:../,\1/"' '"~/t024/shadow/covid/inputs/in_small.csv"'` | **no** | says no split | allows a split |
| Naive LLM's files | `sed '"s/[^[:print:]]//g"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed '"s/ly$/-ly/g"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed 's/$/"0s"/'` | yes | allows a split | allows a split |
| Naive LLM's files | `sed -e '"s/SN:\([0-9XY]\)/SN:chr\1/"' -e '"s/SN:MT/SN:chrM/"'` | **no** | says no split | allows a split |
| Naive LLM's files | `sed -e '"s|^\./||"' '"~/t024/shadow/web-search/inputs/index_min.txt"'` | **no** | says no split | allows a split |
| Naive LLM's files | `sed -n '"/^590432,/p"'` | yes | says no split | allows a split |
| Naive LLM's files | `sed 100q` | yes | says no split | says no split |
| Naive LLM's files | `sed 1d` | yes | says no split | says no split |
| Naive LLM's files | `sed 2d` | yes | says no split | says no split |
| Naive LLM's files | `sed 3d` | yes | says no split | says no split |
| Naive LLM's files | `sed 4d` | yes | says no split | says no split |
| Naive LLM's files | `sed 5d` | yes | says no split | says no split |
| Naive LLM's files | `sed 5q` | yes | says no split | says no split |
| Naive LLM's files | `seq '"${START_YEAR}"' '"${END_YEAR}"'` | yes | says no split | no answer |
| Naive LLM's files | `sort` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -f` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -k 1 -n` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -n` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -nr` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -r` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -rn` | yes | allows a split | allows a split |
| Naive LLM's files | `sort -u` | yes | allows a split | says no split |
| Naive LLM's files | `tail -n 1` | **no** | allows only a split PaSh has not implemented | no answer |
| Naive LLM's files | `tail -n1 '"${formatted}"'` | yes | says no split | no answer |
| Naive LLM's files | `tr '" "' '"\n"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '" /"' '"__"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[:lower:]"' '"[:upper:]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[:upper:]"' '"[:lower:]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[A-Z]"' '"[a-z]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[a-z]"' '"P"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[a-z]"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"[a-z]"' '"\n"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr '"a-z"' '"[A-Z]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -c '"A-Za-z"' '"[\n*]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -c '"[A-Z]"' '"\n"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -c '"[a-z][A-Z]"' '"\n"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -cs A-Za-z '"\n"'` | yes | says no split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr -d '","'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -d '"[:punct:]"'` | yes | allows a split | allows a split |
| Naive LLM's files | `tr -d '"\n"'` | yes | allows a split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr -s '" "' '"\n"'` | yes | says no split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr -sc '"AEIOU"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr -sc '"AEIOUaeiou"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr -sc '"BCDFGHJKLMNPQRSTVWXYZ"' '"[\012*]"'` | yes | says no split | allows only a split PaSh has not implemented |
| Naive LLM's files | `tr A-Z a-z` | yes | allows a split | allows a split |
| Naive LLM's files | `uniq` | yes | allows only a split PaSh has not implemented | allows only a split PaSh has not implemented |
| Naive LLM's files | `uniq -c` | yes | allows only a split PaSh has not implemented | allows only a split PaSh has not implemented |
| Naive LLM's files | `wc -l` | yes | raised | no answer |
| Naive LLM's files | `xargs -0 -n4 -P4 mawk '"/Result/ { split($0, a, "-"); res = substr(a[1], length(a[1]), 1); if (res == 1) white++; if (res == 0) black++; if (res == 2) draw++ } END { print white+black+draw, white, black, draw }"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cat '"${OUT}/urls.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"${OUT}/visited.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"${formatted}"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"${input}"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small"/*.INFO'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small/1.INFO"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/analytics/outputs/ray_tracing_small/rays.csv"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/file-mod/inputs/jpg_small/jpg/119901.jpg"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '"~/t024/shadow/weather/inputs/temperatures.small.txt"'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat '~/t024/shadow/file-mod/inputs/wav_small/file_example_WAV_5MG.wav.~9~'` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/10_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/11_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/5_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ./inputs/9.9_30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat inputs/bio-min/input_min.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/analytics/inputs/nginx-logs_small/log7` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/analytics/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/file-mod/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/nlp/inputs/pg-small/ynkgt10.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `cut '-d" "' -f1,2 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cut '-d" "' -f1,3` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cut '-d" "' -f1,3 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cut '-d" "' -f2` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 1-1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 1-12` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 1-2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 1-4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 3-3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 7-` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -c 89-92` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '" "' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '" "' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '" "' -f 4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '"""' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '"("' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '")"' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 1,2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 1,2,4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 1,3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 3` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '","' -f 3,1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -d '"."' -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -f 1` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -f 1 -d '" "'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -f 2` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `cut -f 2 ./Gene_locs.txt` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `cut -f 4` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '" ${year}"' '"${formatted}"'` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar | `grep '"""'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"${city}"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"("'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"AT&T"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"And he said"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"Bell"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"UNIX"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"\."'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"\[RAY\]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"light.\*light"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"print"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"the land of"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep '"x"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -c '"^....$"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar | `grep -c '"^[A-Z]"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar | `grep -c '"light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar | `grep -c '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*$"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]$"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `grep -v '"NA"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -v '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -v '"\-99"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -v '"^\s*$"'` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -v 999` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -v pathID` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `grep -vc '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, PaSh grammar | `grep -vi '"[aeiou]"'` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `grep 1969` | yes | allows a split | allows a split |
| Caruca's files, PaSh grammar | `rm -f '"${yr_txt}"' '"${max_y}"' '"${min_y}"' '"${j1}"' '"${j2}"'` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar | `rm s1 s2` | **no** | says no split | no answer |
| Caruca's files, PaSh grammar | `sort` | yes | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -f` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -k 1 -n` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -n` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -nr` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -r` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -rn` | **no** | says no split | allows a split |
| Caruca's files, PaSh grammar | `sort -u` | **no** | says no split | says no split |
| Caruca's files, PaSh grammar | `wc -l` | yes | says no split | no answer |
| Caruca's files, main grammar | `cat '"${OUT}/urls.txt"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"${OUT}/visited.txt"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"${formatted}"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"${input}"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small"/*.INFO'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/analytics/inputs/ray_tracing_small/1.INFO"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/analytics/outputs/ray_tracing_small/rays.csv"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/covid/inputs/in_small.csv"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/file-mod/inputs/jpg_small/jpg/119901.jpg"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/oneliners/inputs/logs-popcount-org_small.txt"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '"~/t024/shadow/weather/inputs/temperatures.small.txt"'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat '~/t024/shadow/file-mod/inputs/wav_small/file_example_WAV_5MG.wav.~9~'` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/10_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/11_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/5_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.1_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.2_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.3_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.4_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.6_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.7_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.8_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ./inputs/9.9_30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat inputs/bio-min/input_min.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/analytics/inputs/nginx-logs_small/log7` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/analytics/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/file-mod/inputs/pcaps_small/wlan-ipadstartstop101.pcapng` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/nlp/inputs/pg-small/ynkgt10.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/oneliners/inputs/10M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `cut '-d" "' -f1,2 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `cut '-d" "' -f1,3` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `cut '-d" "' -f1,3 '"${processed}"'` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `cut '-d" "' -f2` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `cut -c 1-1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 1-12` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 1-2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 1-4` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 3-3` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 7-` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -c 89-92` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '" "' -f 1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '" "' -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '" "' -f 4` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '"""' -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '"("' -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '")"' -f 1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 1,2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 1,2,4` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 1,3` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 3` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '","' -f 3,1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -d '"."' -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -f 1` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -f 1 -d '" "'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -f 2` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `cut -f 2 ./Gene_locs.txt` | yes | says no split | allows a split |
| Caruca's files, main grammar | `cut -f 4` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '" ${year}"' '"${formatted}"'` | yes | says no split | allows a split |
| Caruca's files, main grammar | `grep '"""'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"${city}"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"("'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"AT&T"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"And he said"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"Bell"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"UNIX"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"[A-Z]"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"\."'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"\[RAY\]"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"light.\*light"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"print"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"the land of"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep '"x"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -c '"^....$"'` | yes | says no split | says no split |
| Caruca's files, main grammar | `grep -c '"^[A-Z]"'` | yes | says no split | says no split |
| Caruca's files, main grammar | `grep -c '"light.\*light"'` | yes | says no split | says no split |
| Caruca's files, main grammar | `grep -c '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, main grammar | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*$"'` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `grep -i '"^[^aeiou]*[aeiou][^aeiou]*[aeiou][^aeiou]$"'` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `grep -v '"NA"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -v '"[KQRBN]"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -v '"\-99"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -v '"^\s*$"'` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -v 999` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -v pathID` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `grep -vc '"light.\*light.\*light"'` | yes | says no split | says no split |
| Caruca's files, main grammar | `grep -vi '"[aeiou]"'` | **no** | says no split | allows a split |
| Caruca's files, main grammar | `grep 1969` | yes | allows a split | allows a split |
| Caruca's files, main grammar | `rm -f '"${yr_txt}"' '"${max_y}"' '"${min_y}"' '"${j1}"' '"${j2}"'` | **no** | says no split | no answer |
| Caruca's files, main grammar | `rm s1 s2` | **no** | says no split | no answer |
| Caruca's files, main grammar | `sort` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -f` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -k 1 -n` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -n` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -nr` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -r` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -rn` | yes | says no split | allows a split |
| Caruca's files, main grammar | `sort -u` | yes | says no split | says no split |
| Caruca's files, main grammar | `wc -l` | yes | says no split | no answer |

## Appendix A5: times per script (seconds, median and min–max)

| Script | Plain bash | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | PaSh's own files, second copy |
|---|---:|---:|---:|---:|---:|---:|
| analytics/nginx | 1.30 (1.22–1.35, 3 runs) | 1.48 (1.39–1.70, 3 runs) | 1.46 (1.45–1.48, 3 runs) | 1.46 (1.40–1.48, 3 runs) | 1.48 (1.38–1.50, 3 runs) | 1.49 (1.40–1.54, 3 runs) |
| analytics/pcaps | 97.54 (97.06–124.14, 3 runs) | 106.15 (96.57–122.51, 3 runs) | 101.38 (96.25–121.14, 3 runs) | 100.33 (96.27–138.01, 3 runs) | 100.46 (97.17–122.44, 3 runs) | 101.44 (96.24–136.32, 3 runs) |
| analytics/ray-tracing | 0.00 (0.00–0.00, 3 runs) | 0.12 (0.10–0.13, 3 runs) | 0.12 (0.12–0.14, 3 runs) | 0.12 (0.10–0.13, 3 runs) | 0.12 (0.10–0.14, 3 runs) | 0.13 (0.12–0.13, 3 runs) |
| bio/bio | 0.13 (0.12–0.14, 3 runs) | 0.28 (0.23–0.32, 3 runs) | 0.26 (0.24–0.28, 3 runs) | 0.26 (0.22–0.27, 3 runs) | 0.26 (0.23–0.27, 3 runs) | 0.26 (0.22–0.27, 3 runs) |
| covid/1 | 10.01 (9.93–10.57, 3 runs) | 6.73 (6.45–7.12, 3 runs) | 13.19 (13.18–14.16, 3 runs) | 10.37 (10.13–10.40, 3 runs) | 7.76 (7.37–7.85, 3 runs) | 6.68 (6.21–6.85, 3 runs) |
| covid/2 | 10.12 (10.09–10.52, 3 runs) | 7.14 (6.91–8.08, 3 runs) | 14.45 (14.13–14.48, 3 runs) | 10.62 (10.46–10.67, 3 runs) | 8.21 (7.74–8.48, 3 runs) | 6.45 (6.33–7.44, 3 runs) |
| covid/3 | 14.84 (14.64–15.18, 3 runs) | 7.50 (7.48–7.69, 3 runs) | 17.90 (17.62–17.91, 3 runs) | 14.83 (14.80–15.15, 3 runs) | 8.38 (8.02–8.62, 3 runs) | 7.26 (7.12–7.54, 3 runs) |
| covid/4 | 12.15 (12.15–12.45, 3 runs) | 6.67 (6.54–7.07, 3 runs) | 16.75 (16.34–16.79, 3 runs) | 12.49 (12.25–12.73, 3 runs) | 7.36 (7.26–7.76, 3 runs) | 6.65 (6.55–6.84, 3 runs) |
| covid/5 | 11.15 (10.87–11.29, 3 runs) | 11.13 (11.11–11.26, 3 runs) | 11.38 (11.26–11.56, 3 runs) | 10.97 (10.79–13.39, 3 runs) | 11.31 (10.74–12.67, 3 runs) | 11.36 (11.25–11.55, 3 runs) |
| file-mod/compress_files | 18.75 (18.44–19.14, 3 runs) | 19.49 (18.82–20.28, 3 runs) | 19.45 (19.35–19.46, 3 runs) | 19.22 (19.06–19.31, 3 runs) | 19.20 (18.89–19.45, 3 runs) | 19.25 (19.21–19.27, 3 runs) |
| file-mod/encrypt_files | 2.00 (1.92–2.05, 3 runs) | 2.73 (2.43–9.41, 3 runs) | 2.69 (2.48–3.46, 3 runs) | 2.65 (2.54–3.82, 3 runs) | 2.94 (2.63–4.54, 3 runs) | 3.10 (3.05–3.17, 3 runs) |
| file-mod/img_convert | 32.36 (32.33–35.47, 3 runs) | 35.81 (35.27–36.89, 3 runs) | 35.51 (35.48–35.65, 3 runs) | 35.57 (35.53–35.59, 3 runs) | 35.96 (35.46–36.93, 3 runs) | 35.42 (35.35–37.88, 3 runs) |
| file-mod/thumbnail_generation | 11.01 (10.62–11.08, 3 runs) | 11.22 (10.60–17.52, 3 runs) | 10.99 (10.57–11.44, 3 runs) | 11.04 (10.83–11.23, 3 runs) | 10.91 (10.66–10.91, 3 runs) | 10.76 (10.51–11.20, 3 runs) |
| file-mod/to_mp3 | 8.62 (8.48–10.12, 3 runs) | 9.34 (8.89–9.97, 3 runs) | 9.31 (8.89–9.84, 3 runs) | 9.02 (8.96–9.03, 3 runs) | 8.95 (8.93–9.73, 3 runs) | 9.02 (8.96–9.79, 3 runs) |
| nlp/bigrams | 49.48 (49.34–52.86, 3 runs) | 69.41 (68.45–94.22, 3 runs) | 74.10 (68.66–80.62, 3 runs) | 71.97 (68.66–73.24, 3 runs) | 74.63 (68.32–75.03, 3 runs) | 71.02 (68.11–75.33, 3 runs) |
| nlp/bigrams_appear_twice | 60.02 (59.62–62.81, 3 runs) | 79.45 (78.31–82.63, 3 runs) | 78.62 (77.81–88.67, 3 runs) | 78.75 (78.06–81.70, 3 runs) | 78.43 (78.24–84.58, 3 runs) | 78.35 (77.26–86.39, 3 runs) |
| nlp/compare_exodus_genesis | 89.11 (87.99–89.72, 3 runs) | 108.74 (107.67–108.91, 3 runs) | 109.87 (108.72–117.16, 3 runs) | 109.14 (107.56–120.50, 3 runs) | 109.21 (107.79–124.95, 3 runs) | 109.36 (107.62–120.15, 3 runs) |
| nlp/count_consonant_seq | 41.59 (39.02–46.26, 3 runs) | 65.05 (57.23–72.65, 3 runs) | 60.30 (57.56–62.50, 3 runs) | 62.05 (61.03–62.64, 3 runs) | 63.84 (61.80–70.22, 3 runs) | 62.59 (59.11–76.49, 3 runs) |
| nlp/count_morphs | 8.51 (8.28–8.59, 3 runs) | 25.07 (25.05–29.94, 3 runs) | 26.93 (26.16–29.30, 3 runs) | 25.78 (24.61–28.71, 3 runs) | 26.15 (25.11–26.77, 3 runs) | 26.52 (24.81–27.47, 3 runs) |
| nlp/count_trigrams | 55.62 (53.15–56.31, 3 runs) | 74.53 (71.09–78.25, 3 runs) | 78.88 (76.81–80.61, 3 runs) | 79.49 (76.99–81.07, 3 runs) | 74.53 (72.31–79.81, 3 runs) | 74.81 (73.98–81.43, 3 runs) |
| nlp/count_vowel_seq | 7.90 (7.83–8.18, 3 runs) | 26.52 (24.60–26.57, 3 runs) | 25.65 (25.52–27.48, 3 runs) | 27.55 (25.22–29.46, 3 runs) | 26.46 (24.51–27.57, 3 runs) | 25.36 (24.60–29.88, 3 runs) |
| nlp/count_words | 30.30 (30.25–31.15, 3 runs) | 47.92 (47.67–50.74, 3 runs) | 47.52 (47.35–50.79, 3 runs) | 47.18 (47.05–50.60, 3 runs) | 48.44 (47.14–56.77, 3 runs) | 47.73 (47.36–54.24, 3 runs) |
| nlp/find_anagrams | 42.12 (41.94–46.58, 3 runs) | 63.43 (61.78–69.04, 3 runs) | 66.47 (61.51–67.44, 3 runs) | 63.86 (57.24–65.53, 3 runs) | 65.02 (55.99–71.00, 3 runs) | 65.88 (56.78–69.72, 3 runs) |
| nlp/letter_words | 38.64 (38.09–39.23, 3 runs) | 76.58 (71.27–80.30, 3 runs) | 74.44 (71.39–76.06, 3 runs) | 76.92 (70.62–80.64, 3 runs) | 78.50 (70.31–80.73, 3 runs) | 77.28 (74.59–79.40, 3 runs) |
| nlp/merge_upper | 30.48 (30.20–30.50, 3 runs) | 48.16 (47.61–49.91, 3 runs) | 48.87 (47.99–49.49, 3 runs) | 47.72 (47.64–51.98, 3 runs) | 47.90 (47.90–53.22, 3 runs) | 47.67 (47.62–50.11, 3 runs) |
| nlp/sort | 33.46 (33.38–33.48, 3 runs) | 51.50 (50.77–52.66, 3 runs) | 51.14 (50.88–51.66, 3 runs) | 51.01 (50.69–56.17, 3 runs) | 53.33 (51.05–53.98, 3 runs) | 52.03 (51.16–57.40, 3 runs) |
| nlp/sort_words_by_folding | 33.22 (33.08–34.36, 3 runs) | 51.30 (50.61–54.88, 3 runs) | 50.94 (50.65–56.23, 3 runs) | 50.62 (50.49–53.89, 3 runs) | 50.68 (50.65–55.07, 3 runs) | 50.97 (50.87–53.22, 3 runs) |
| nlp/sort_words_by_num_of_syllables | 38.09 (37.79–38.58, 3 runs) | 58.08 (56.40–59.07, 3 runs) | 57.99 (56.42–59.21, 3 runs) | 58.79 (55.38–59.27, 3 runs) | 61.45 (55.76–64.02, 3 runs) | 54.95 (54.26–56.98, 3 runs) |
| nlp/sort_words_by_rhyming | 35.40 (35.27–35.45, 3 runs) | 52.19 (51.91–53.06, 3 runs) | 53.27 (53.15–53.48, 3 runs) | 51.97 (51.94–52.22, 3 runs) | 52.05 (51.97–52.17, 3 runs) | 52.07 (51.97–52.28, 3 runs) |
| nlp/syllable_words_1 | 16.96 (16.89–17.97, 3 runs) | 36.06 (34.88–38.13, 3 runs) | 35.04 (34.72–44.39, 3 runs) | 34.69 (34.57–36.16, 3 runs) | 34.82 (34.56–36.40, 3 runs) | 34.89 (34.64–36.23, 3 runs) |
| nlp/syllable_words_2 | 10.98 (10.84–11.25, 3 runs) | 30.55 (29.19–30.71, 3 runs) | 29.79 (29.33–30.91, 3 runs) | 29.06 (28.62–30.57, 3 runs) | 29.73 (28.90–30.57, 3 runs) | 29.31 (29.11–30.84, 3 runs) |
| nlp/trigram_rec | 13.46 (13.02–14.41, 3 runs) | 53.11 (45.69–53.17, 3 runs) | 45.58 (45.12–52.90, 3 runs) | 45.19 (44.84–45.28, 3 runs) | 45.33 (45.25–45.51, 3 runs) | 45.45 (45.38–45.59, 3 runs) |
| nlp/uppercase_by_token | 9.39 (9.17–9.42, 3 runs) | 27.10 (26.62–28.19, 3 runs) | 26.55 (26.54–26.81, 3 runs) | 26.90 (26.58–27.79, 3 runs) | 27.10 (26.41–27.38, 3 runs) | 27.52 (26.03–30.20, 3 runs) |
| nlp/uppercase_by_type | 28.53 (28.53–28.55, 3 runs) | 46.16 (45.57–46.44, 3 runs) | 45.63 (45.29–46.65, 3 runs) | 45.33 (45.23–47.64, 3 runs) | 45.72 (45.26–46.52, 3 runs) | 45.60 (45.11–45.73, 3 runs) |
| nlp/verses_2om_3om_2instances | 6.41 (6.27–6.54, 3 runs) | 56.36 (54.06–58.16, 3 runs) | 54.03 (53.05–58.62, 3 runs) | 58.13 (53.05–60.92, 3 runs) | 55.80 (53.71–57.98, 3 runs) | 58.24 (54.31–59.41, 3 runs) |
| nlp/vowel_sequencies_gr_1K | 30.55 (30.45–30.56, 3 runs) | 49.89 (48.42–50.10, 3 runs) | 49.02 (48.70–53.65, 3 runs) | 48.63 (48.31–55.20, 3 runs) | 48.66 (48.55–59.88, 3 runs) | 48.74 (48.55–49.53, 3 runs) |
| nlp/words_no_vowels | 10.23 (10.18–10.29, 3 runs) | 27.42 (27.29–29.09, 3 runs) | 27.45 (27.11–29.23, 3 runs) | 27.50 (27.14–29.25, 3 runs) | 27.81 (27.39–29.17, 3 runs) | 28.09 (27.17–29.80, 3 runs) |
| oneliners/bi-grams | 1.18 (1.18–1.19, 3 runs) | 1.30 (1.27–1.32, 3 runs) | 1.30 (1.28–1.34, 3 runs) | 1.31 (1.30–1.32, 3 runs) | 1.32 (1.31–1.36, 3 runs) | 1.30 (1.28–1.34, 3 runs) |
| oneliners/comm | 0.03 (0.03–0.04, 3 runs) | 0.13 (0.13–0.15, 3 runs) | 0.14 (0.14–0.15, 3 runs) | 0.12 (0.12–0.16, 3 runs) | 0.12 (0.12–0.15, 3 runs) | 0.12 (0.12–0.15, 3 runs) |
| oneliners/diff | 0.26 (0.26–0.30, 3 runs) | 0.43 (0.37–0.43, 3 runs) | 0.41 (0.38–0.41, 3 runs) | 0.40 (0.37–0.41, 3 runs) | 0.40 (0.37–0.42, 3 runs) | 0.39 (0.36–0.42, 3 runs) |
| oneliners/nfa-regex | 8.23 (8.14–8.53, 3 runs) | 1.94 (1.87–2.11, 3 runs) | 1.90 (1.89–1.92, 3 runs) | 1.87 (1.87–2.03, 3 runs) | 1.88 (1.86–1.94, 3 runs) | 1.88 (1.87–1.93, 3 runs) |
| oneliners/opt-parallel | 0.10 (0.09–0.12, 3 runs) | 0.25 (0.22–0.33, 3 runs) | 0.20 (0.20–0.23, 3 runs) | 0.21 (0.20–0.23, 3 runs) | 0.20 (0.19–0.53, 3 runs) | 0.21 (0.18–0.27, 3 runs) |
| oneliners/set-diff | 0.24 (0.24–0.27, 3 runs) | 0.35 (0.35–0.39, 3 runs) | 0.36 (0.36–0.41, 3 runs) | 0.35 (0.34–0.41, 3 runs) | 0.35 (0.35–0.39, 3 runs) | 0.35 (0.34–0.41, 3 runs) |
| oneliners/sort | 0.12 (0.11–0.14, 3 runs) | 0.24 (0.22–0.25, 3 runs) | 0.25 (0.25–0.26, 3 runs) | 0.23 (0.23–0.30, 3 runs) | 0.27 (0.26–0.29, 3 runs) | 0.23 (0.21–0.23, 3 runs) |
| oneliners/sort-sort | 0.17 (0.17–0.23, 3 runs) | 0.36 (0.34–0.37, 3 runs) | 0.40 (0.39–0.41, 3 runs) | 0.28 (0.28–0.29, 3 runs) | 0.32 (0.31–0.33, 3 runs) | 0.36 (0.34–0.39, 3 runs) |
| oneliners/spell | 1.05 (1.02–1.23, 3 runs) | 0.63 (0.61–0.75, 3 runs) | 0.91 (0.89–1.05, 3 runs) | 1.11 (1.10–1.11, 3 runs) | 1.09 (1.05–1.11, 3 runs) | 0.66 (0.61–0.68, 3 runs) |
| oneliners/top-n | 0.92 (0.90–0.93, 3 runs) | 0.59 (0.57–0.68, 3 runs) | 0.70 (0.70–0.72, 3 runs) | 0.98 (0.98–1.05, 3 runs) | 1.00 (0.95–1.03, 3 runs) | 0.54 (0.51–0.61, 3 runs) |
| oneliners/uniq-ips | 0.07 (0.07–0.08, 3 runs) | 0.18 (0.17–0.20, 3 runs) | 0.21 (0.21–0.22, 3 runs) | 0.20 (0.19–0.23, 3 runs) | 0.19 (0.19–0.49, 3 runs) | 0.18 (0.18–0.32, 3 runs) |
| oneliners/wf | 0.86 (0.86–0.90, 3 runs) | 0.50 (0.48–0.54, 3 runs) | 0.62 (0.60–0.64, 3 runs) | 0.99 (0.97–1.13, 3 runs) | 0.92 (0.91–1.07, 3 runs) | 0.50 (0.48–0.57, 3 runs) |
| unixfun/1 | 0.07 (0.06–0.07, 3 runs) | 0.20 (0.18–0.45, 3 runs) | 0.21 (0.20–0.42, 3 runs) | 0.21 (0.20–0.46, 3 runs) | 0.22 (0.19–0.26, 3 runs) | 0.20 (0.16–0.23, 3 runs) |
| unixfun/10 | 0.06 (0.05–0.06, 3 runs) | 0.33 (0.32–0.39, 3 runs) | 0.47 (0.45–0.56, 3 runs) | 0.17 (0.15–0.18, 3 runs) | 0.26 (0.26–0.30, 3 runs) | 0.36 (0.32–0.36, 3 runs) |
| unixfun/11 | 0.06 (0.06–0.06, 3 runs) | 0.37 (0.33–0.38, 3 runs) | 0.51 (0.45–0.51, 3 runs) | 0.17 (0.15–0.17, 3 runs) | 0.29 (0.27–0.35, 3 runs) | 0.38 (0.37–0.40, 3 runs) |
| unixfun/12 | 0.28 (0.25–0.29, 3 runs) | 0.41 (0.36–0.42, 3 runs) | 0.60 (0.48–0.69, 3 runs) | 0.39 (0.37–0.40, 3 runs) | 0.39 (0.37–0.44, 3 runs) | 0.36 (0.36–0.38, 3 runs) |
| unixfun/13 | 0.04 (0.04–0.04, 3 runs) | 0.23 (0.21–0.28, 3 runs) | 0.28 (0.23–0.29, 3 runs) | 0.26 (0.24–0.28, 3 runs) | 0.26 (0.24–0.30, 3 runs) | 0.23 (0.22–0.23, 3 runs) |
| unixfun/14 | 0.73 (0.72–0.80, 3 runs) | 0.63 (0.63–0.67, 3 runs) | 0.57 (0.47–0.69, 3 runs) | 0.94 (0.81–1.17, 3 runs) | 1.20 (0.92–1.28, 3 runs) | 0.66 (0.61–1.01, 3 runs) |
| unixfun/15 | 0.06 (0.06–0.06, 3 runs) | 0.19 (0.17–0.22, 3 runs) | 0.21 (0.21–0.23, 3 runs) | 0.22 (0.21–0.22, 3 runs) | 0.22 (0.21–0.22, 3 runs) | 0.19 (0.19–0.27, 3 runs) |
| unixfun/16 | 0.17 (0.16–0.17, 3 runs) | 0.28 (0.26–0.30, 3 runs) | 0.35 (0.33–0.37, 3 runs) | 0.28 (0.28–0.30, 3 runs) | 0.28 (0.27–0.33, 3 runs) | 0.29 (0.29–0.29, 3 runs) |
| unixfun/17 | 0.16 (0.16–0.16, 3 runs) | 0.35 (0.33–0.38, 3 runs) | 0.36 (0.35–0.37, 3 runs) | 0.27 (0.26–0.29, 3 runs) | 0.37 (0.37–0.42, 3 runs) | 0.35 (0.34–0.38, 3 runs) |
| unixfun/18 | 0.03 (0.03–0.04, 3 runs) | 0.19 (0.19–0.23, 3 runs) | 0.33 (0.33–0.34, 3 runs) | 0.21 (0.21–0.24, 3 runs) | 0.21 (0.21–0.23, 3 runs) | 0.19 (0.19–0.21, 3 runs) |
| unixfun/19 | 0.02 (0.02–0.03, 3 runs) | 0.21 (0.21–0.24, 3 runs) | 0.22 (0.21–0.22, 3 runs) | 0.23 (0.23–0.23, 3 runs) | 0.22 (0.22–0.23, 3 runs) | 0.21 (0.21–0.21, 3 runs) |
| unixfun/2 | 0.29 (0.29–0.33, 3 runs) | 0.28 (0.28–0.31, 3 runs) | 0.30 (0.30–0.31, 3 runs) | 0.39 (0.39–0.40, 3 runs) | 0.39 (0.37–0.41, 3 runs) | 0.28 (0.28–0.32, 3 runs) |
| unixfun/20 | 0.00 (0.00–0.00, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.17 (0.17–0.17, 3 runs) | 0.17 (0.16–0.18, 3 runs) | 0.17 (0.17–0.19, 3 runs) |
| unixfun/21 | 0.97 (0.96–1.00, 3 runs) | 0.55 (0.54–0.55, 3 runs) | 0.64 (0.64–0.65, 3 runs) | 1.11 (1.11–1.12, 3 runs) | 1.11 (1.08–1.12, 3 runs) | 0.57 (0.53–0.58, 3 runs) |
| unixfun/23 | 0.06 (0.06–0.06, 3 runs) | 0.27 (0.26–0.28, 3 runs) | 0.55 (0.54–0.57, 3 runs) | 0.27 (0.27–0.30, 3 runs) | 0.28 (0.27–0.29, 3 runs) | 0.27 (0.26–0.28, 3 runs) |
| unixfun/24 | 0.07 (0.07–0.07, 3 runs) | 0.18 (0.17–0.19, 3 runs) | 0.26 (0.24–0.26, 3 runs) | 0.20 (0.18–0.20, 3 runs) | 0.20 (0.20–0.24, 3 runs) | 0.18 (0.17–0.20, 3 runs) |
| unixfun/25 | 0.07 (0.07–0.07, 3 runs) | 0.17 (0.16–0.19, 3 runs) | 0.25 (0.25–0.27, 3 runs) | 0.19 (0.18–0.19, 3 runs) | 0.18 (0.18–0.19, 3 runs) | 0.18 (0.17–0.18, 3 runs) |
| unixfun/26 | 0.07 (0.07–0.07, 3 runs) | 0.32 (0.29–0.32, 3 runs) | 0.51 (0.48–0.56, 3 runs) | 0.29 (0.28–0.30, 3 runs) | 0.29 (0.28–0.30, 3 runs) | 0.31 (0.30–0.31, 3 runs) |
| unixfun/28 | 0.06 (0.06–0.08, 3 runs) | 0.38 (0.37–0.70, 3 runs) | 0.60 (0.57–0.64, 3 runs) | 0.39 (0.36–0.42, 3 runs) | 0.40 (0.37–0.40, 3 runs) | 0.38 (0.36–0.47, 3 runs) |
| unixfun/29 | 0.06 (0.06–0.07, 3 runs) | 0.29 (0.23–0.31, 3 runs) | 0.36 (0.31–0.44, 3 runs) | 0.28 (0.27–0.31, 3 runs) | 0.32 (0.30–0.33, 3 runs) | 0.28 (0.23–0.28, 3 runs) |
| unixfun/3 | 0.00 (0.00–0.00, 3 runs) | 0.13 (0.13–0.15, 3 runs) | 0.17 (0.17–0.18, 3 runs) | 0.17 (0.16–0.17, 3 runs) | 0.17 (0.15–0.17, 3 runs) | 0.13 (0.13–0.14, 3 runs) |
| unixfun/30 | 0.10 (0.09–0.10, 3 runs) | 0.33 (0.32–0.35, 3 runs) | 0.54 (0.49–0.58, 3 runs) | 0.34 (0.32–0.35, 3 runs) | 0.34 (0.34–0.35, 3 runs) | 0.34 (0.32–0.35, 3 runs) |
| unixfun/31 | 0.10 (0.09–0.10, 3 runs) | 0.33 (0.33–0.34, 3 runs) | 0.51 (0.50–0.52, 3 runs) | 0.34 (0.33–0.34, 3 runs) | 0.33 (0.32–0.35, 3 runs) | 0.33 (0.32–0.33, 3 runs) |
| unixfun/32 | 0.04 (0.04–0.04, 3 runs) | 0.23 (0.21–0.23, 3 runs) | 0.26 (0.24–0.26, 3 runs) | 0.24 (0.24–0.26, 3 runs) | 0.27 (0.24–0.28, 3 runs) | 0.22 (0.22–0.22, 3 runs) |
| unixfun/33 | 0.04 (0.04–0.04, 3 runs) | 0.20 (0.20–0.23, 3 runs) | 0.25 (0.24–0.27, 3 runs) | 0.25 (0.24–0.26, 3 runs) | 0.25 (0.24–0.26, 3 runs) | 0.22 (0.21–0.23, 3 runs) |
| unixfun/34 | 0.00 (0.00–0.00, 3 runs) | 0.12 (0.09–0.13, 3 runs) | 0.11 (0.11–0.12, 3 runs) | 0.11 (0.11–0.11, 3 runs) | 0.11 (0.10–0.12, 3 runs) | 0.11 (0.09–0.12, 3 runs) |
| unixfun/35 | 0.02 (0.01–0.02, 3 runs) | 0.18 (0.18–0.20, 3 runs) | 0.21 (0.20–0.22, 3 runs) | 0.19 (0.18–0.20, 3 runs) | 0.20 (0.19–0.21, 3 runs) | 0.18 (0.18–0.19, 3 runs) |
| unixfun/36 | 0.06 (0.06–0.09, 3 runs) | 0.19 (0.15–0.19, 3 runs) | 0.16 (0.16–0.17, 3 runs) | 0.16 (0.15–0.17, 3 runs) | 0.15 (0.15–0.16, 3 runs) | 0.17 (0.16–0.17, 3 runs) |
| unixfun/4 | 0.28 (0.26–0.29, 3 runs) | 0.34 (0.32–0.35, 3 runs) | 0.37 (0.34–0.37, 3 runs) | 0.36 (0.35–0.39, 3 runs) | 0.42 (0.37–0.43, 3 runs) | 0.33 (0.32–0.37, 3 runs) |
| unixfun/5 | 0.04 (0.04–0.04, 3 runs) | 0.18 (0.17–0.23, 3 runs) | 0.20 (0.20–0.26, 3 runs) | 0.20 (0.18–0.21, 3 runs) | 0.20 (0.20–0.21, 3 runs) | 0.18 (0.17–0.20, 3 runs) |
| unixfun/6 | 0.07 (0.07–0.07, 3 runs) | 0.23 (0.23–0.31, 3 runs) | 0.32 (0.30–0.35, 3 runs) | 0.27 (0.25–0.28, 3 runs) | 0.26 (0.26–0.27, 3 runs) | 0.24 (0.24–0.25, 3 runs) |
| unixfun/7 | 0.08 (0.08–0.09, 3 runs) | 0.19 (0.19–0.21, 3 runs) | 0.31 (0.30–0.34, 3 runs) | 0.22 (0.20–0.28, 3 runs) | 0.22 (0.21–0.23, 3 runs) | 0.20 (0.18–0.20, 3 runs) |
| unixfun/8 | 0.03 (0.03–0.03, 3 runs) | 0.20 (0.18–0.22, 3 runs) | 0.31 (0.31–0.35, 3 runs) | 0.20 (0.20–0.23, 3 runs) | 0.22 (0.21–0.23, 3 runs) | 0.20 (0.19–0.21, 3 runs) |
| unixfun/9 | 0.03 (0.03–0.03, 3 runs) | 0.22 (0.22–0.25, 3 runs) | 0.35 (0.33–0.36, 3 runs) | 0.23 (0.22–0.25, 3 runs) | 0.26 (0.22–0.27, 3 runs) | 0.23 (0.21–0.24, 3 runs) |
| weather/temp-analytics | 4.35 (4.33–4.84, 3 runs) | 4.58 (4.36–7.96, 3 runs) | 4.44 (4.40–4.88, 3 runs) | 4.53 (4.38–4.91, 3 runs) | 4.53 (4.35–5.16, 3 runs) | 4.53 (4.50–4.85, 3 runs) |
| weather/tuft-weather | 462.70 (443.19–464.61, 3 runs) | 465.99 (452.41–491.60, 3 runs) | 470.08 (465.24–482.80, 3 runs) | 463.27 (442.62–470.70, 3 runs) | 463.59 (441.09–469.75, 3 runs) | 463.74 (441.77–464.08, 3 runs) |
| web-search/engine | 640.36 (638.05–662.31, 3 runs) | 710.06 (685.38–735.30, 3 runs) | 706.69 (688.96–729.65, 3 runs) | 697.52 (677.38–749.76, 3 runs) | 686.76 (685.25–715.37, 3 runs) | 680.36 (672.36–696.17, 3 runs) |

## Appendix A6 (from the records): controls and run windows

| When | Control | Commands split | Output same as bash |
|---|---|---|---|
| after-46 | Naive LLM's files | cat, sort, tr | yes |
| after-46 | Control: naive LLM's files, sort's files removed | none | yes |
| after-46 | Control: naive LLM's files, PaSh's own col files | cat, col, sort, tr | yes |
| after-46 | Control: naive LLM's files, PaSh's own cat files | sort, tr | yes |
| after-46 | Control: naive LLM's files, PaSh's own sed files | cat, sed, sort, tr | yes |
| end | Naive LLM's files | cat, sort, tr | yes |
| end | Control: naive LLM's files, sort's files removed | none | yes |
| end | Control: naive LLM's files, PaSh's own col files | cat, col, sort, tr | yes |
| end | Control: naive LLM's files, PaSh's own cat files | sort, tr | yes |
| end | Control: naive LLM's files, PaSh's own sed files | cat, sed, sort, tr | yes |

| Record | When | Script | Start | End | VM load at start | VM load at end | Koala changed | Mac power check |
|---|---|---|---|---|---|---|---|---|
| results.jsonl | main | oneliners/nfa-regex | 2026-11-24 13:10:15 -0500 | 2026-11-24 13:10:55 -0500 | 0.71, 0.26, 0.50 | 1.52, 0.53, 0.58 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/sort | 2026-11-24 13:12:07 -0500 | 2026-11-24 13:12:11 -0500 | 1.15, 0.64, 0.62 | 1.78, 0.78, 0.66 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/top-n | 2026-11-24 13:13:17 -0500 | 2026-11-24 13:13:27 -0500 | 1.31, 0.84, 0.69 | 1.49, 0.89, 0.71 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/wf | 2026-11-24 13:14:17 -0500 | 2026-11-24 13:14:28 -0500 | 1.27, 0.93, 0.74 | 1.23, 0.93, 0.74 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/spell | 2026-11-24 13:15:30 -0500 | 2026-11-24 13:15:42 -0500 | 1.14, 0.96, 0.76 | 1.67, 1.08, 0.80 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/diff | 2026-11-24 13:16:36 -0500 | 2026-11-24 13:16:42 -0500 | 1.43, 1.11, 0.83 | 1.48, 1.13, 0.84 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/bi-grams | 2026-11-24 13:17:26 -0500 | 2026-11-24 13:17:41 -0500 | 1.22, 1.11, 0.85 | 1.33, 1.14, 0.86 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/set-diff | 2026-11-24 13:18:30 -0500 | 2026-11-24 13:18:34 -0500 | 1.14, 1.11, 0.87 | 1.29, 1.14, 0.88 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/sort-sort | 2026-11-24 13:19:26 -0500 | 2026-11-24 13:19:31 -0500 | 1.11, 1.12, 0.89 | 1.43, 1.18, 0.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/uniq-ips | 2026-11-24 13:20:20 -0500 | 2026-11-24 13:20:23 -0500 | 1.20, 1.15, 0.92 | 1.26, 1.17, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/comm | 2026-11-24 13:21:04 -0500 | 2026-11-24 13:21:06 -0500 | 1.12, 1.14, 0.93 | 1.12, 1.14, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | oneliners/opt-parallel | 2026-11-24 13:22:05 -0500 | 2026-11-24 13:22:08 -0500 | 1.04, 1.11, 0.94 | 1.04, 1.11, 0.94 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/1 | 2026-11-24 13:23:51 -0500 | 2026-11-24 13:23:54 -0500 | 0.81, 0.97, 0.90 | 0.83, 0.97, 0.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/2 | 2026-11-24 13:24:48 -0500 | 2026-11-24 13:24:53 -0500 | 0.93, 0.97, 0.91 | 2.30, 1.26, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/3 | 2026-11-24 13:25:33 -0500 | 2026-11-24 13:25:36 -0500 | 1.66, 1.22, 1.00 | 1.61, 1.22, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/4 | 2026-11-24 13:26:23 -0500 | 2026-11-24 13:26:28 -0500 | 1.29, 1.19, 1.00 | 1.26, 1.18, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/5 | 2026-11-24 13:27:39 -0500 | 2026-11-24 13:27:42 -0500 | 1.07, 1.14, 1.00 | 1.07, 1.14, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/6 | 2026-11-24 13:28:43 -0500 | 2026-11-24 13:28:47 -0500 | 1.02, 1.11, 1.00 | 1.02, 1.11, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/7 | 2026-11-24 13:29:18 -0500 | 2026-11-24 13:29:22 -0500 | 1.01, 1.10, 1.00 | 1.01, 1.10, 1.00 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/8 | 2026-11-24 13:29:59 -0500 | 2026-11-24 13:30:03 -0500 | 1.52, 1.20, 1.04 | 1.40, 1.18, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/9 | 2026-11-24 13:30:46 -0500 | 2026-11-24 13:30:50 -0500 | 1.19, 1.15, 1.03 | 1.19, 1.15, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/10 | 2026-11-24 13:31:24 -0500 | 2026-11-24 13:31:28 -0500 | 1.05, 1.12, 1.02 | 1.13, 1.13, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/11 | 2026-11-24 13:32:19 -0500 | 2026-11-24 13:32:23 -0500 | 1.10, 1.12, 1.02 | 1.10, 1.12, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/12 | 2026-11-24 13:32:47 -0500 | 2026-11-24 13:32:52 -0500 | 1.06, 1.11, 1.02 | 1.06, 1.11, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/13 | 2026-11-24 13:33:30 -0500 | 2026-11-24 13:33:33 -0500 | 1.03, 1.09, 1.02 | 1.03, 1.09, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/14 | 2026-11-24 13:34:21 -0500 | 2026-11-24 13:34:29 -0500 | 1.09, 1.09, 1.02 | 1.15, 1.11, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/15 | 2026-11-24 13:35:16 -0500 | 2026-11-24 13:35:19 -0500 | 1.11, 1.11, 1.02 | 1.43, 1.17, 1.05 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/16 | 2026-11-24 13:35:57 -0500 | 2026-11-24 13:36:00 -0500 | 1.24, 1.15, 1.04 | 1.22, 1.15, 1.04 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/17 | 2026-11-24 13:36:27 -0500 | 2026-11-24 13:36:31 -0500 | 1.13, 1.13, 1.04 | 1.13, 1.13, 1.04 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/18 | 2026-11-24 13:37:23 -0500 | 2026-11-24 13:37:26 -0500 | 1.05, 1.11, 1.03 | 1.05, 1.11, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/19 | 2026-11-24 13:38:12 -0500 | 2026-11-24 13:38:15 -0500 | 1.02, 1.09, 1.03 | 1.02, 1.09, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/20 | 2026-11-24 13:38:52 -0500 | 2026-11-24 13:38:54 -0500 | 1.01, 1.08, 1.02 | 1.01, 1.08, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/21 | 2026-11-24 13:39:37 -0500 | 2026-11-24 13:39:47 -0500 | 1.00, 1.06, 1.02 | 1.00, 1.06, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/23 | 2026-11-24 13:40:23 -0500 | 2026-11-24 13:40:27 -0500 | 1.00, 1.05, 1.02 | 1.00, 1.05, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/24 | 2026-11-24 13:40:56 -0500 | 2026-11-24 13:40:58 -0500 | 1.00, 1.05, 1.01 | 1.00, 1.05, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/25 | 2026-11-24 13:41:26 -0500 | 2026-11-24 13:41:29 -0500 | 1.00, 1.04, 1.01 | 1.00, 1.04, 1.01 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/26 | 2026-11-24 13:42:08 -0500 | 2026-11-24 13:42:12 -0500 | 1.00, 1.03, 1.01 | 1.32, 1.10, 1.03 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/28 | 2026-11-24 13:42:39 -0500 | 2026-11-24 13:42:44 -0500 | 1.19, 1.09, 1.02 | 1.18, 1.08, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/29 | 2026-11-24 13:43:22 -0500 | 2026-11-24 13:43:25 -0500 | 1.10, 1.07, 1.02 | 1.09, 1.07, 1.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/30 | 2026-11-24 13:44:03 -0500 | 2026-11-24 13:44:08 -0500 | 1.04, 1.06, 1.02 | 1.92, 1.24, 1.08 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/31 | 2026-11-24 13:44:51 -0500 | 2026-11-24 13:44:55 -0500 | 1.66, 1.26, 1.09 | 1.61, 1.26, 1.09 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/32 | 2026-11-24 13:45:47 -0500 | 2026-11-24 13:45:50 -0500 | 1.32, 1.23, 1.09 | 1.32, 1.23, 1.09 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/33 | 2026-11-24 13:46:24 -0500 | 2026-11-24 13:46:27 -0500 | 1.17, 1.20, 1.08 | 1.16, 1.20, 1.08 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/34 | 2026-11-24 13:46:57 -0500 | 2026-11-24 13:46:58 -0500 | 1.10, 1.18, 1.08 | 1.10, 1.18, 1.08 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/35 | 2026-11-24 13:49:59 -0500 | 2026-11-24 13:50:06 -0500 | 1.05, 1.15, 1.08 | 1.12, 1.16, 1.08 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | unixfun/36 | 2026-11-24 13:50:40 -0500 | 2026-11-24 13:50:42 -0500 | 1.07, 1.14, 1.08 | 1.07, 1.14, 1.08 | no | not checked per window here (see the sleep list) |
| controls.jsonl | after-46 | oneliners/spell | 2026-11-24 13:53:19 -0500 | 2026-11-24 13:53:31 -0500 | 0.26, 0.74, 0.93 | 2.31, 1.17, 1.07 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | oneliners/top-n | 2026-11-24 13:57:02 -0500 | 2026-11-24 13:57:05 -0500 | 0.59, 0.78, 0.93 | 0.63, 0.78, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | oneliners/spell | 2026-11-24 13:57:05 -0500 | 2026-11-24 13:57:09 -0500 | 0.63, 0.78, 0.93 | 0.66, 0.79, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | oneliners/bi-grams | 2026-11-24 13:57:09 -0500 | 2026-11-24 13:57:14 -0500 | 0.66, 0.79, 0.93 | 0.68, 0.79, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/17 | 2026-11-24 13:57:14 -0500 | 2026-11-24 13:57:15 -0500 | 0.68, 0.79, 0.93 | 0.68, 0.79, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/26 | 2026-11-24 13:57:15 -0500 | 2026-11-24 13:57:16 -0500 | 0.68, 0.79, 0.93 | 0.68, 0.79, 0.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/28 | 2026-11-24 13:57:16 -0500 | 2026-11-24 13:57:18 -0500 | 0.68, 0.79, 0.93 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/29 | 2026-11-24 13:57:18 -0500 | 2026-11-24 13:57:19 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/30 | 2026-11-24 13:57:19 -0500 | 2026-11-24 13:57:20 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/31 | 2026-11-24 13:57:20 -0500 | 2026-11-24 13:57:22 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/32 | 2026-11-24 13:57:22 -0500 | 2026-11-24 13:57:22 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/33 | 2026-11-24 13:57:22 -0500 | 2026-11-24 13:57:23 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | sed2 | unixfun/36 | 2026-11-24 13:57:23 -0500 | 2026-11-24 13:57:24 -0500 | 1.03, 0.86, 0.95 | 1.03, 0.86, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/ray-tracing | 2026-11-24 13:57:48 -0500 | 2026-11-24 13:57:51 -0500 | 0.68, 0.79, 0.92 | 0.68, 0.79, 0.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | bio/bio | 2026-11-24 13:57:51 -0500 | 2026-11-24 13:57:56 -0500 | 0.68, 0.79, 0.92 | 0.70, 0.80, 0.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/nginx | 2026-11-24 13:57:56 -0500 | 2026-11-24 13:58:15 -0500 | 0.70, 0.80, 0.92 | 1.14, 0.89, 0.95 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/encrypt_files | 2026-11-24 13:58:15 -0500 | 2026-11-24 13:59:02 -0500 | 1.14, 0.89, 0.95 | 1.49, 1.01, 0.99 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | weather/temp-analytics | 2026-11-24 13:59:02 -0500 | 2026-11-24 14:00:00 -0500 | 1.49, 1.01, 0.99 | 1.96, 1.23, 1.07 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/to_mp3 | 2026-11-24 14:00:00 -0500 | 2026-11-24 14:02:03 -0500 | 1.96, 1.23, 1.07 | 1.21, 1.25, 1.09 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_vowel_seq | 2026-11-24 14:02:04 -0500 | 2026-11-24 14:08:13 -0500 | 1.21, 1.25, 1.09 | 1.67, 1.51, 1.28 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/verses_2om_3om_2instances | 2026-11-24 14:08:13 -0500 | 2026-11-24 14:20:56 -0500 | 1.67, 1.51, 1.28 | 1.22, 1.39, 1.34 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/uppercase_by_token | 2026-11-24 14:20:57 -0500 | 2026-11-24 14:26:58 -0500 | 1.22, 1.39, 1.34 | 1.74, 1.64, 1.48 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_morphs | 2026-11-24 14:26:58 -0500 | 2026-11-24 14:33:10 -0500 | 1.74, 1.64, 1.48 | 1.65, 1.63, 1.54 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/words_no_vowels | 2026-11-24 14:33:10 -0500 | 2026-11-24 14:39:34 -0500 | 1.65, 1.63, 1.54 | 2.30, 2.04, 1.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/thumbnail_generation | 2026-11-24 14:39:34 -0500 | 2026-11-24 14:42:00 -0500 | 2.30, 2.04, 1.76 | 1.28, 1.68, 1.66 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/2 | 2026-11-24 14:42:00 -0500 | 2026-11-24 14:44:21 -0500 | 1.28, 1.68, 1.66 | 5.29, 3.09, 2.19 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/1 | 2026-11-24 14:44:21 -0500 | 2026-11-24 14:46:32 -0500 | 5.29, 3.09, 2.19 | 5.37, 3.77, 2.55 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/syllable_words_2 | 2026-11-24 14:46:33 -0500 | 2026-11-24 14:53:21 -0500 | 5.37, 3.77, 2.55 | 2.64, 2.76, 2.49 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/4 | 2026-11-24 14:53:21 -0500 | 2026-11-24 14:55:50 -0500 | 2.64, 2.76, 2.49 | 5.67, 3.85, 2.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/5 | 2026-11-24 14:55:50 -0500 | 2026-11-24 14:58:17 -0500 | 5.67, 3.85, 2.93 | 2.19, 3.05, 2.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | covid/3 | 2026-11-24 14:58:17 -0500 | 2026-11-24 15:00:58 -0500 | 2.19, 3.05, 2.76 | 4.58, 3.62, 3.02 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/compress_files | 2026-11-24 15:00:58 -0500 | 2026-11-24 15:05:17 -0500 | 4.58, 3.62, 3.02 | 1.29, 2.29, 2.60 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/syllable_words_1 | 2026-11-24 15:05:18 -0500 | 2026-11-24 15:14:04 -0500 | 1.29, 2.29, 2.60 | 1.77, 1.99, 2.33 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/trigram_rec | 2026-11-24 15:14:08 -0500 | 2026-11-24 15:26:01 -0500 | 1.77, 1.99, 2.33 | 1.92, 1.83, 2.07 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_words | 2026-11-24 16:09:26 -0500 | 2026-11-24 16:20:46 -0500 | 1.20, 1.49, 1.75 | 1.33, 1.37, 1.54 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/vowel_sequencies_gr_1K | 2026-11-24 16:20:46 -0500 | 2026-11-24 16:32:28 -0500 | 1.33, 1.37, 1.54 | 1.51, 1.64, 1.63 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/merge_upper | 2026-11-24 16:32:29 -0500 | 2026-11-24 16:43:48 -0500 | 1.51, 1.64, 1.63 | 1.54, 1.50, 1.56 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | file-mod/img_convert | 2026-11-24 16:43:48 -0500 | 2026-11-24 16:52:06 -0500 | 1.54, 1.50, 1.56 | 3.49, 2.99, 2.23 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_folding | 2026-11-24 16:52:07 -0500 | 2026-11-24 17:04:14 -0500 | 3.49, 2.99, 2.23 | 1.65, 1.61, 1.81 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort | 2026-11-24 17:04:14 -0500 | 2026-11-24 17:16:12 -0500 | 1.65, 1.61, 1.81 | 1.41, 1.46, 1.59 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/letter_words | 2026-11-24 17:32:32 -0500 | 2026-11-24 17:49:09 -0500 | 1.85, 1.63, 1.63 | 1.09, 1.31, 1.46 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_num_of_syllables | 2026-11-24 17:49:10 -0500 | 2026-11-24 18:02:01 -0500 | 1.09, 1.31, 1.46 | 1.54, 1.48, 1.46 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_consonant_seq | 2026-11-24 18:02:02 -0500 | 2026-11-24 18:14:52 -0500 | 1.54, 1.48, 1.46 | 1.25, 1.42, 1.44 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/find_anagrams | 2026-11-24 18:14:53 -0500 | 2026-11-24 18:28:09 -0500 | 1.23, 1.41, 1.44 | 1.20, 1.23, 1.32 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/bigrams | 2026-11-24 18:28:10 -0500 | 2026-11-24 18:44:10 -0500 | 1.20, 1.23, 1.32 | 1.58, 1.72, 1.61 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/count_trigrams | 2026-11-24 18:44:11 -0500 | 2026-11-24 19:02:03 -0500 | 1.58, 1.72, 1.61 | 1.46, 1.37, 1.46 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/bigrams_appear_twice | 2026-11-24 19:02:05 -0500 | 2026-11-24 19:21:34 -0500 | 1.46, 1.37, 1.46 | 1.53, 1.43, 1.39 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/compare_exodus_genesis | 2026-11-24 19:21:35 -0500 | 2026-11-24 19:46:59 -0500 | 1.49, 1.42, 1.39 | 1.44, 1.35, 1.36 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | analytics/pcaps | 2026-11-24 19:47:00 -0500 | 2026-11-24 20:14:33 -0500 | 1.44, 1.35, 1.36 | 1.72, 1.67, 1.62 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | weather/tuft-weather | 2026-11-24 20:14:36 -0500 | 2026-11-24 21:55:28 -0500 | 1.72, 1.67, 1.62 | 1.48, 1.49, 1.44 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | web-search/engine | 2026-11-24 21:55:33 -0500 | 2026-11-24 23:07:46 -0500 | 1.44, 1.48, 1.44 | 1.42, 1.62, 1.69 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/uppercase_by_type | 2026-11-24 23:08:39 -0500 | 2026-11-24 23:18:48 -0500 | 0.79, 1.41, 1.61 | 1.60, 1.59, 1.62 | no | not checked per window here (see the sleep list) |
| results.jsonl | main | nlp/sort_words_by_rhyming | 2026-11-24 23:18:48 -0500 | 2026-11-24 23:30:20 -0500 | 1.60, 1.59, 1.62 | 2.55, 1.97, 1.79 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/nfa-regex | 2026-11-24 23:32:15 -0500 | 2026-11-24 23:32:51 -0500 | 0.59, 1.42, 1.60 | 1.74, 1.64, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/sort | 2026-11-24 23:32:51 -0500 | 2026-11-24 23:32:54 -0500 | 1.74, 1.64, 1.67 | 1.68, 1.63, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/wf | 2026-11-24 23:32:54 -0500 | 2026-11-24 23:33:03 -0500 | 1.68, 1.63, 1.67 | 1.79, 1.65, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/diff | 2026-11-24 23:33:03 -0500 | 2026-11-24 23:33:08 -0500 | 1.79, 1.65, 1.67 | 1.74, 1.64, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/set-diff | 2026-11-24 23:33:08 -0500 | 2026-11-24 23:33:13 -0500 | 1.74, 1.64, 1.67 | 1.74, 1.64, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/sort-sort | 2026-11-24 23:33:13 -0500 | 2026-11-24 23:33:17 -0500 | 1.74, 1.64, 1.67 | 1.68, 1.63, 1.67 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/uniq-ips | 2026-11-24 23:33:17 -0500 | 2026-11-24 23:33:20 -0500 | 1.68, 1.63, 1.67 | 2.67, 1.84, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/comm | 2026-11-24 23:33:20 -0500 | 2026-11-24 23:33:22 -0500 | 2.67, 1.84, 1.73 | 2.67, 1.84, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/opt-parallel | 2026-11-24 23:33:22 -0500 | 2026-11-24 23:33:25 -0500 | 2.67, 1.84, 1.73 | 2.53, 1.83, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/1 | 2026-11-24 23:33:25 -0500 | 2026-11-24 23:33:28 -0500 | 2.53, 1.83, 1.73 | 2.41, 1.81, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/2 | 2026-11-24 23:33:28 -0500 | 2026-11-24 23:33:33 -0500 | 2.41, 1.81, 1.73 | 2.41, 1.81, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/3 | 2026-11-24 23:33:33 -0500 | 2026-11-24 23:33:35 -0500 | 2.41, 1.81, 1.73 | 2.30, 1.80, 1.72 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/4 | 2026-11-24 23:33:35 -0500 | 2026-11-24 23:33:39 -0500 | 2.30, 1.80, 1.72 | 2.19, 1.78, 1.72 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/5 | 2026-11-24 23:33:39 -0500 | 2026-11-24 23:33:42 -0500 | 2.19, 1.78, 1.72 | 2.19, 1.78, 1.72 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/6 | 2026-11-24 23:33:42 -0500 | 2026-11-24 23:33:45 -0500 | 2.19, 1.78, 1.72 | 2.42, 1.84, 1.74 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/7 | 2026-11-24 23:33:45 -0500 | 2026-11-24 23:33:48 -0500 | 2.42, 1.84, 1.74 | 2.42, 1.84, 1.74 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/8 | 2026-11-24 23:33:48 -0500 | 2026-11-24 23:33:51 -0500 | 2.42, 1.84, 1.74 | 2.70, 1.91, 1.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/9 | 2026-11-24 23:33:51 -0500 | 2026-11-24 23:33:54 -0500 | 2.70, 1.91, 1.76 | 2.89, 1.96, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/10 | 2026-11-24 23:33:54 -0500 | 2026-11-24 23:33:57 -0500 | 2.89, 1.96, 1.78 | 2.89, 1.96, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/11 | 2026-11-24 23:33:57 -0500 | 2026-11-24 23:34:01 -0500 | 2.89, 1.96, 1.78 | 2.74, 1.94, 1.77 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/12 | 2026-11-24 23:34:01 -0500 | 2026-11-24 23:34:07 -0500 | 2.74, 1.94, 1.77 | 2.60, 1.93, 1.77 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/13 | 2026-11-24 23:34:07 -0500 | 2026-11-24 23:34:10 -0500 | 2.60, 1.93, 1.77 | 2.47, 1.91, 1.76 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/14 | 2026-11-24 23:34:10 -0500 | 2026-11-24 23:34:21 -0500 | 2.47, 1.91, 1.76 | 2.24, 1.88, 1.75 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/15 | 2026-11-24 23:34:21 -0500 | 2026-11-24 23:34:24 -0500 | 2.24, 1.88, 1.75 | 2.62, 1.97, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/16 | 2026-11-24 23:34:24 -0500 | 2026-11-24 23:34:28 -0500 | 2.62, 1.97, 1.78 | 2.62, 1.97, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/18 | 2026-11-24 23:34:28 -0500 | 2026-11-24 23:34:31 -0500 | 2.62, 1.97, 1.78 | 2.57, 1.97, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/19 | 2026-11-24 23:34:31 -0500 | 2026-11-24 23:34:33 -0500 | 2.57, 1.97, 1.78 | 2.57, 1.97, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/20 | 2026-11-24 23:34:33 -0500 | 2026-11-24 23:34:35 -0500 | 2.57, 1.97, 1.78 | 2.45, 1.95, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/21 | 2026-11-24 23:34:36 -0500 | 2026-11-24 23:34:46 -0500 | 2.45, 1.95, 1.78 | 2.30, 1.94, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/23 | 2026-11-24 23:34:46 -0500 | 2026-11-24 23:34:50 -0500 | 2.30, 1.94, 1.78 | 2.36, 1.95, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/24 | 2026-11-24 23:34:50 -0500 | 2026-11-24 23:34:52 -0500 | 2.36, 1.95, 1.78 | 2.36, 1.95, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/25 | 2026-11-24 23:34:52 -0500 | 2026-11-24 23:34:55 -0500 | 2.36, 1.95, 1.78 | 2.25, 1.94, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/34 | 2026-11-24 23:34:55 -0500 | 2026-11-24 23:34:57 -0500 | 2.25, 1.94, 1.78 | 2.25, 1.94, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/35 | 2026-11-24 23:34:57 -0500 | 2026-11-24 23:34:59 -0500 | 2.25, 1.94, 1.78 | 2.15, 1.92, 1.77 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/top-n | 2026-11-24 23:34:59 -0500 | 2026-11-24 23:35:10 -0500 | 2.15, 1.92, 1.77 | 1.97, 1.89, 1.77 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/spell | 2026-11-24 23:35:10 -0500 | 2026-11-24 23:35:24 -0500 | 1.97, 1.89, 1.77 | 3.18, 2.16, 1.86 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | oneliners/bi-grams | 2026-11-24 23:35:24 -0500 | 2026-11-24 23:35:43 -0500 | 3.18, 2.16, 1.86 | 3.26, 2.23, 1.89 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/17 | 2026-11-24 23:35:43 -0500 | 2026-11-24 23:35:48 -0500 | 3.26, 2.23, 1.89 | 3.08, 2.21, 1.88 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/26 | 2026-11-24 23:35:48 -0500 | 2026-11-24 23:35:53 -0500 | 3.08, 2.21, 1.88 | 3.23, 2.26, 1.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/28 | 2026-11-24 23:35:53 -0500 | 2026-11-24 23:36:00 -0500 | 3.23, 2.26, 1.90 | 2.89, 2.22, 1.89 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/29 | 2026-11-24 23:36:00 -0500 | 2026-11-24 23:36:04 -0500 | 2.89, 2.22, 1.89 | 2.74, 2.20, 1.88 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/30 | 2026-11-24 23:36:05 -0500 | 2026-11-24 23:36:10 -0500 | 2.74, 2.20, 1.88 | 2.92, 2.24, 1.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/31 | 2026-11-24 23:36:10 -0500 | 2026-11-24 23:36:16 -0500 | 2.92, 2.24, 1.90 | 3.33, 2.34, 1.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/32 | 2026-11-24 23:36:16 -0500 | 2026-11-24 23:36:19 -0500 | 3.33, 2.34, 1.93 | 3.14, 2.32, 1.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/33 | 2026-11-24 23:36:19 -0500 | 2026-11-24 23:36:23 -0500 | 3.14, 2.32, 1.93 | 3.14, 2.32, 1.93 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | unixfun/36 | 2026-11-24 23:36:23 -0500 | 2026-11-24 23:36:26 -0500 | 3.14, 2.32, 1.93 | 2.97, 2.29, 1.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | analytics/ray-tracing | 2026-11-24 23:36:26 -0500 | 2026-11-24 23:36:28 -0500 | 2.97, 2.29, 1.92 | 2.97, 2.29, 1.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | bio/bio | 2026-11-24 23:36:28 -0500 | 2026-11-24 23:36:34 -0500 | 2.97, 2.29, 1.92 | 2.74, 2.27, 1.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | analytics/nginx | 2026-11-24 23:36:34 -0500 | 2026-11-24 23:36:56 -0500 | 2.74, 2.27, 1.92 | 2.24, 2.18, 1.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | file-mod/encrypt_files | 2026-11-24 23:36:56 -0500 | 2026-11-24 23:38:02 -0500 | 2.24, 2.18, 1.90 | 1.96, 2.12, 1.90 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | weather/temp-analytics | 2026-11-24 23:38:02 -0500 | 2026-11-24 23:39:12 -0500 | 1.96, 2.12, 1.90 | 2.26, 2.14, 1.92 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | file-mod/to_mp3 | 2026-11-24 23:39:12 -0500 | 2026-11-24 23:41:19 -0500 | 2.26, 2.14, 1.92 | 1.20, 1.76, 1.81 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/count_vowel_seq | 2026-11-24 23:41:19 -0500 | 2026-11-24 23:47:02 -0500 | 1.20, 1.76, 1.81 | 1.58, 1.71, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/verses_2om_3om_2instances | 2026-11-24 23:47:02 -0500 | 2026-11-24 23:58:56 -0500 | 1.58, 1.71, 1.78 | 1.67, 1.52, 1.61 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/uppercase_by_token | 2026-11-24 23:58:56 -0500 | 2026-11-25 00:04:57 -0500 | 1.67, 1.52, 1.61 | 1.45, 1.51, 1.57 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/count_morphs | 2026-11-25 00:04:57 -0500 | 2026-11-25 00:10:38 -0500 | 1.45, 1.51, 1.57 | 1.60, 1.57, 1.57 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/words_no_vowels | 2026-11-25 00:10:38 -0500 | 2026-11-25 00:16:44 -0500 | 1.60, 1.57, 1.57 | 1.98, 1.86, 1.69 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | file-mod/thumbnail_generation | 2026-11-25 00:16:44 -0500 | 2026-11-25 00:19:23 -0500 | 1.98, 1.86, 1.69 | 1.13, 1.55, 1.60 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | covid/2 | 2026-11-25 00:19:23 -0500 | 2026-11-25 00:21:42 -0500 | 1.13, 1.55, 1.60 | 4.63, 2.84, 2.08 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | covid/1 | 2026-11-25 00:21:42 -0500 | 2026-11-25 00:23:52 -0500 | 4.63, 2.84, 2.08 | 5.09, 3.70, 2.51 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/syllable_words_2 | 2026-11-25 00:23:53 -0500 | 2026-11-25 00:30:27 -0500 | 5.09, 3.70, 2.51 | 2.02, 2.75, 2.50 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | covid/4 | 2026-11-25 00:30:27 -0500 | 2026-11-25 00:32:51 -0500 | 2.02, 2.75, 2.50 | 5.08, 3.73, 2.91 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | covid/5 | 2026-11-25 00:32:52 -0500 | 2026-11-25 00:35:34 -0500 | 5.08, 3.73, 2.91 | 2.01, 2.92, 2.72 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | covid/3 | 2026-11-25 00:35:34 -0500 | 2026-11-25 00:38:17 -0500 | 2.01, 2.92, 2.72 | 4.81, 4.02, 3.19 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | file-mod/compress_files | 2026-11-25 00:38:17 -0500 | 2026-11-25 00:42:50 -0500 | 4.81, 4.02, 3.19 | 1.50, 2.45, 2.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/syllable_words_1 | 2026-11-25 00:42:51 -0500 | 2026-11-25 00:50:41 -0500 | 1.50, 2.45, 2.73 | 2.03, 2.21, 2.51 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/trigram_rec | 2026-11-25 00:50:44 -0500 | 2026-11-25 01:00:50 -0500 | 2.03, 2.21, 2.51 | 2.20, 2.04, 2.23 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/uppercase_by_type | 2026-11-25 01:00:50 -0500 | 2026-11-25 01:11:17 -0500 | 2.20, 2.04, 2.23 | 1.35, 1.55, 1.87 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/count_words | 2026-11-25 01:11:18 -0500 | 2026-11-25 01:22:07 -0500 | 1.35, 1.55, 1.87 | 1.50, 1.66, 1.78 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/vowel_sequencies_gr_1K | 2026-11-25 01:22:08 -0500 | 2026-11-25 01:33:13 -0500 | 1.50, 1.66, 1.78 | 1.74, 1.85, 1.83 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/merge_upper | 2026-11-25 01:33:14 -0500 | 2026-11-25 01:44:09 -0500 | 1.74, 1.85, 1.83 | 1.81, 1.69, 1.73 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | file-mod/img_convert | 2026-11-25 01:44:09 -0500 | 2026-11-25 01:52:26 -0500 | 1.81, 1.69, 1.73 | 3.18, 2.95, 2.33 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/sort_words_by_folding | 2026-11-25 01:52:26 -0500 | 2026-11-25 02:04:03 -0500 | 3.18, 2.95, 2.33 | 1.29, 1.57, 1.88 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/sort | 2026-11-25 02:04:03 -0500 | 2026-11-25 02:15:52 -0500 | 1.29, 1.57, 1.88 | 1.39, 1.58, 1.71 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/sort_words_by_rhyming | 2026-11-25 02:15:53 -0500 | 2026-11-25 02:27:52 -0500 | 1.39, 1.58, 1.71 | 1.89, 1.69, 1.70 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/letter_words | 2026-11-25 02:27:52 -0500 | 2026-11-25 02:44:38 -0500 | 1.89, 1.69, 1.70 | 1.60, 1.47, 1.54 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/sort_words_by_num_of_syllables | 2026-11-25 02:44:39 -0500 | 2026-11-25 02:57:40 -0500 | 1.60, 1.47, 1.54 | 1.20, 1.28, 1.39 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/count_consonant_seq | 2026-11-25 02:57:40 -0500 | 2026-11-25 03:12:32 -0500 | 1.20, 1.28, 1.39 | 1.08, 1.24, 1.33 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/find_anagrams | 2026-11-25 03:12:37 -0500 | 2026-11-25 03:27:33 -0500 | 1.07, 1.24, 1.33 | 1.45, 1.51, 1.44 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/bigrams | 2026-11-25 03:27:36 -0500 | 2026-11-25 03:45:01 -0500 | 1.41, 1.50, 1.44 | 1.42, 1.50, 1.47 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/count_trigrams | 2026-11-25 03:45:03 -0500 | 2026-11-25 04:03:03 -0500 | 1.46, 1.51, 1.48 | 1.26, 1.39, 1.42 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/bigrams_appear_twice | 2026-11-25 04:03:05 -0500 | 2026-11-25 04:21:00 -0500 | 1.26, 1.39, 1.42 | 1.28, 1.39, 1.43 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | nlp/compare_exodus_genesis | 2026-11-25 04:21:01 -0500 | 2026-11-25 04:45:57 -0500 | 1.28, 1.39, 1.43 | 1.31, 1.42, 1.39 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | analytics/pcaps | 2026-11-25 04:45:58 -0500 | 2026-11-25 05:08:54 -0500 | 1.31, 1.42, 1.39 | 1.79, 1.77, 1.69 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | weather/tuft-weather | 2026-11-25 05:08:55 -0500 | 2026-11-25 06:58:02 -0500 | 1.79, 1.77, 1.69 | 1.54, 1.34, 1.38 | no | not checked per window here (see the sleep list) |
| results.jsonl | repeats | web-search/engine | 2026-11-25 06:58:08 -0500 | 2026-11-25 09:58:18 -0500 | 1.45, 1.33, 1.37 | 1.28, 1.37, 1.50 | no | not checked per window here (see the sleep list) |
| controls.jsonl | end | oneliners/spell | 2026-11-25 09:58:19 -0500 | 2026-11-25 09:58:39 -0500 | 1.25, 1.36, 1.50 | 1.69, 1.45, 1.52 | no | not checked per window here (see the sleep list) |
| results.jsonl | redo-r1 | web-search/engine | 2026-11-25 10:12:31 -0500 | 2026-11-25 11:32:06 -0500 | 0.08, 0.10, 0.61 | 1.39, 1.63, 1.65 | no | not checked per window here (see the sleep list) |
| results.jsonl | redo-r3 | web-search/engine | 2026-11-25 11:32:08 -0500 | 2026-11-25 12:51:54 -0500 | 1.39, 1.63, 1.65 | 1.36, 1.57, 1.58 | no | not checked per window here (see the sleep list) |

## Full run: output, what PaSh did, files written (timed repeats)

Printed output: every run of the script (timed and with the stand-in programs) the same as bash's run of the same repeat. State: what PaSh did in the first timed repeat. File check: timed rows of the 32 scripts that write files (bash wrote at least one).

| Source | Scripts | Printed output same as bash | Same as Koala's stored answer | PaSh ran a part in parallel | Fell back to plain bash | Other state | File check: same / not checked / different |
|---|---:|---:|---:|---:|---:|---|---|
| PaSh's own files | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 | 61 / 32 / 3 |
| Naive LLM's files | 86 | 86 of 86 | 46 of 46 | 43 of 86 | 42 of 86 | compiled, nothing split: 1 | 30 / 63 / 3 |
| Caruca's files, PaSh grammar | 86 | 86 of 86 | 46 of 46 | 29 of 86 | 56 of 86 | compiled, nothing split: 1 | 30 / 63 / 3 |
| Caruca's files, main grammar | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 | 30 / 63 / 3 |
| Naive LLM, sed file v2 | 52 | 52 of 52 | 12 of 12 | 14 of 52 | 38 of 52 | - | 30 / 63 / 3 |
| PaSh's own files, second copy | 86 | 86 of 86 | 46 of 46 | 41 of 86 | 44 of 86 | compiled, nothing split: 1 | 30 / 63 / 3 |

All sources together, file check on timed rows: same 211, not checked 347, different 18, of 576. Different, by script: bio/bio 6, web-search/engine 12.
Plain bash matched Koala's stored answer in 46 of 46 scripts that have one.
Scripts whose recorded state differs between timed repeats: none.

## Full run: parts paired with PaSh's own files, the partial source

- Naive LLM, sed file v2: 139 distinct parts in 52 scripts; both in parallel 14, gained 0, lost 0, neither 125. Command uses in its parts: 438; with its own files 354, split with them 77; split with PaSh's own files filled in 0.

## Full run: commands gained and lost, per script (from the per-use records)

| Source | Command | Gained (scripts) | Lost (scripts) |
|---|---|---:|---:|
| Naive LLM's files | `awk` | 6 | 0 |
| Naive LLM's files | `cat` | 43 | 0 |
| Naive LLM's files | `col` | 0 | 1 |
| Naive LLM's files | `cut` | 2 | 0 |
| Naive LLM's files | `grep` | 1 | 0 |
| Naive LLM's files | `sed` | 0 | 5 |
| Naive LLM's files | `sort` | 2 | 0 |
| Naive LLM's files | `tr` | 3 | 0 |
| Caruca's files, PaSh grammar | `cat` | 29 | 0 |
| Caruca's files, PaSh grammar | `cut` | 0 | 9 |
| Caruca's files, PaSh grammar | `grep` | 0 | 4 |
| Caruca's files, PaSh grammar | `sed` | 0 | 5 |
| Caruca's files, PaSh grammar | `sort` | 0 | 17 |
| Caruca's files, PaSh grammar | `tr` | 0 | 5 |
| Caruca's files, main grammar | `cat` | 41 | 0 |
| Caruca's files, main grammar | `sort` | 0 | 17 |
| Naive LLM, sed file v2 | `awk` | 4 | 0 |
| Naive LLM, sed file v2 | `cat` | 14 | 0 |
| Naive LLM, sed file v2 | `col` | 0 | 1 |

Per command (all commands used inside a part): scripts using it, and scripts where PaSh's own files had it split: . 1/0, ./crawl.sh 1/0, ./index.sh 1/0, [ 2/0, [[ 1/0, awk 11/0, bigrams_aux 1/0, break 1/0, cat 82/0, cd 2/0, col 1/1, comm 4/0, continue 1/0, cut 35/26, diff 1/0, dirname 2/0, echo 25/0, export 12/0, ffmpeg 1/0, find 1/0, fmt 2/0, grep 47/21, gzip 1/0, head 9/0, join 1/0, mawk 1/0, mkdir 31/0, mkfifo 2/0, mogrify 1/0, printf 1/0, pure_func 11/0, python3 1/0, read 3/0, rev 1/0, rm 3/0, samtools 1/0, sed 24/6, seq 1/0, sort 44/17, tail 3/0, tr 49/20, uniq 30/0, wc 7/0, xargs 1/0.

Naive LLM, sed file v2 against Naive LLM's files: of the scripts where Naive LLM's files lost a command, `col`: split again in 0 of 1 (it ran on 1 of them); `sed`: split again in 5 of 5 (it ran on 5 of them).

## Full run: time (median of the timed repeats; geometric means over scripts)

| Source | Scripts | Speed-up over bash | Time vs PaSh's own | Faster than PaSh's own by >10% | Slower than PaSh's own by >10% | Faster than bash by >10% | Slower than bash |
|---|---:|---:|---:|---:|---:|---:|---:|
| PaSh's own files | 86 | 0.42x | 1.00 | 0 of 86 | 0 of 86 | 10 of 86 | 74 of 86 |
| Naive LLM's files | 86 | 0.37x | 1.15 | 4 of 86 | 34 of 86 | 6 of 86 | 79 of 86 |
| Caruca's files, PaSh grammar | 86 | 0.41x | 1.05 | 8 of 86 | 17 of 86 | 1 of 86 | 83 of 86 |
| Caruca's files, main grammar | 86 | 0.40x | 1.06 | 6 of 86 | 23 of 86 | 5 of 86 | 80 of 86 |
| Naive LLM, sed file v2 | 52 | 0.51x | 1.07 | 2 of 52 | 10 of 52 | 4 of 52 | 46 of 52 |
| PaSh's own files, second copy | 86 | 0.43x | 0.99 | 3 of 86 | 1 of 86 | 10 of 86 | 74 of 86 |

Noise band (PaSh's own files, second copy against the first copy): 0.83 to 1.13, median 0.99; 4 of 86 scripts beyond 10%.

## Run windows that overlap a Mac sleep

| Window | Sleep | Note in sleep_events.jsonl |
|---|---|---|
| results.jsonl repeats web-search/engine 2026-11-25 06:58:08 -0500 to 2026-11-25 09:58:18 -0500 | 2026-11-25 08:21:36 -0500 to 2026-11-25 08:27:50 -0500 | during web-search/engine repeat 3 (repeats phase), first run after bash repeat 2 ended; web-search repeat 3 is redone after step 4 |

## Checks the script made on the records

| Check | Result | Detail |
|---|---|---|
| bash's own output is identical across all its runs | passed | 86 of 86 scripts; varying: none |
| the distinct parts are the same for every source (same texts, same count) | passed | PaSh's own files: 177; Naive LLM's files: 177; Caruca's files, PaSh grammar: 177; Caruca's files, main grammar: 177 |
| each script sends the same sequence of part texts to PaSh under every source (repeat 1) | passed |  |
| the part count in results.jsonl equals the parts listed in regions.jsonl | passed |  |
| the command uses are the same for every source (same part, same position) | passed | PaSh's own files: 609; Naive LLM's files: 609; Caruca's files, PaSh grammar: 609; Caruca's files, main grammar: 609 |
| a use that appears in more than one launch of a script has the same result in each | passed | 0 differ |
| the commands split per use match the commands split per script in results.jsonl | passed |  |
| PaSh split a use exactly when its files allowed a split PaSh can carry out | **not passed** | 849 of 850 uses in parts run in parallel agree; 1 differ: Naive LLM's files awk '"{$1=$1};1"' |
| every instrumented repeat split the same uses as repeat 1 | passed | 2436 uses x sources, up to 1 repeats each; 0 vary |
| Naive LLM's files: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| Caruca's files, PaSh grammar: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| Caruca's files, main grammar: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| every script run is in the inventory | **not passed** | weather/temp-analytics, web-search/engine |
| the commands the inventory lists equal the commands seen starting, per script | **not passed** | listed, not seen: [('analytics/ray-tracing', 'cut'), ('analytics/ray-tracing', 'sed'), ('covid/5', 'sed'), ('oneliners/bi-grams', 'bigrams_aux')]; seen, not listed: [('covid/5', '   PROCINFO["sorted_in"] = "@ind_str_asc"\n   for (d in day)\n     printf("\\t%s", d);\n   printf("\\n");\n   for (b in bus) {\n     printf("%s", b);\n     for (d in day)\n       printf("\\t%s", hours[d b]);\n     printf("\\n");\n   }\n}'), ('weather/temp-analytics', 'cat'), ('weather/temp-analytics', 'cut'), ('weather/temp-analytics', 'grep'), ('weather/temp-analytics', 'sort'), ('weather/tuft-weather', '        if (!(key in max) || $3 > max[key]) max[key] = $3;\n        if (!(key in min) || $3 < min[key]) min[key] = $3;\n    } \n    END {\n        for (key in max) {\n            mean = sum[key] / count[key];\n            variance = (sum_sq[key] / count[key]) - (mean * mean);\n            stddev = (variance > 0) ? sqrt(variance) : 0;\n            confidence_delta = 1.96 * stddev / sqrt(count[key]);\n            normal_range_low = mean - confidence_delta;\n            normal_range_high = mean + confidence_delta;\n            printf "%s %s %s %.2f %.2f\\n", key, min[key], max[key], normal_range_low, normal_range_high;\n        }\n    }'), ('web-search/engine', 'awk'), ('web-search/engine', 'cat'), ('web-search/engine', 'cut'), ('web-search/engine', 'dirname'), ('web-search/engine', 'grep'), ('web-search/engine', 'iconv'), ('web-search/engine', 'mkfifo'), ('web-search/engine', 'mktemp'), ('web-search/engine', 'node'), ('web-search/engine', 'paste'), ('web-search/engine', 'rm'), ('web-search/engine', 'sed'), ('web-search/engine', 'sort'), ('web-search/engine', 'tail')] |
| the folder-decides controls were run at the start and the end | **not passed** | phases found: ['after-46', 'end']; sets: 6 |
| Koala's checkout did not change during any run window | passed |  |
| no kept run window overlaps a Mac sleep, except windows whose affected rows were redone | passed | 1 of 188 windows overlap a sleep: results.jsonl repeats web-search/engine 2026-11-25 06:58:08 -0500 to 2026-11-25 09:58:18 -0500 (sleep 2026-11-25 08:21:36 -0500 to 2026-11-25 08:27:50 -0500) |
| Naive LLM, sed file v2: every distinct part it was sent is also a part under PaSh's own files | passed | 139 parts; 0 not found |

## Comparison with the builder's `full_run/numbers.md` (written by hand, 2026-11-26)

How this file was made: `prep_full_records.py` copied the records in `full_run/` into a scratch folder in
the shape `count_report.py` reads, applying the builder's two fix-ups in its own code (compare against the
same repeat's bash row; leave out the 7 web-search rows without `node` and replace the 7 rows that have
redone runs). Its log matches the builder's header: 1854 rows compared again, 482 printed-output flags
changed, 642 output-file flags changed, 7 left out, 7 replaced. Then:

    python3 -I prep_full_records.py --records full_run --out <scratch>
    python3 -I count_report.py --records <scratch> --tag full --sleep-events <scratch>/sleep_events.jsonl \
        --out . --notes numbers_full_notes.md

| `numbers.md` section | Cells compared | Same | Differ |
|---|---|---|---|
| 1. Output and what PaSh did (6 sources: scripts, output same as bash, same as Koala's answer, ran a part in parallel, fell back, other state) | 36 | 36 | 0 |
| 3. Distinct parts against PaSh's own files (4 sources × 5 cells) | 20 | 20 | 0 |
| 5. Commands gained and lost (19 rows) | 38 | 38 | 0 |
| 6. Time (6 sources × 5 cells, and the noise band) | 34 | 34 | 0 |

This count reached section 5 by a different route from the builder's: per script, from the per-use
records (`occurrences`), not from each run's `split_commands` list. The two agree on every row.

Where a number here looks different, it measures something else. None of these is a disagreement:

- **"Faster than bash" in Table 1 above** (12, 7, 3 and 6 of 86) counts scripts faster by any margin, and
  its "median speed-up" is a median of ratios. `numbers.md` uses geometric means and a 10% margin. The
  "Full run: time" table above gives the 10% counts: 10, 6, 1 and 5 of 86. These are the same as the
  checker's (check 10) and the builder's README.
- **The method check**: here, 849 of 850 distinct uses in parts PaSh ran in parallel, under the four
  full-coverage sources. `numbers.md` says 956 of 957, because it also counts the 107 uses of the second
  sed file's runs (850 + 107 = 957). The one exception is the same in both: the naive LLM's `awk` in
  `unixfun/19`, two uses whose copies cannot be told apart.
- **Written files**: here, 211 same, 347 not checked and 18 different, of 576 timed rows of the 32
  scripts that write files. The checker's review (check 4) says 211, 352 and 25, of 588. The difference
  is the 12 web-search rows that fix-up 2 leaves out (7 different, 5 not checked; recounted from the raw
  rows). The checker counted before fix-up 2. Of the 18 "different" rows, 12 are web-search, whose files
  differ even between two bash runs, and 6 are bio, where the check itself was broken (checker, check 4).
- **The second sed file** (52 scripts) cannot be paired with PaSh's own files on every part, so it is
  counted in its own block: 139 distinct parts in its 52 scripts, 14 in parallel with both, 0 gained,
  0 lost. These are the same as `numbers.md`. `numbers.md`'s header says this file "was run only on scripts
  that use sed". That sentence is out of date: in 27 of the 52, bash starts no `sed` (checker, check 7,
  item 6). The current `summarise.py` already says so, but `numbers.md` has not been rebuilt since.

Three of this script's own checks fail for reasons that do not touch any number in the report:

- **Inventory names.** The inventory calls two scripts `weather/max-temp` and `web-search/web-index`;
  the records call them `weather/temp-analytics` and `web-search/engine`. And the stand-in programs record
  awk program text and helper functions (`bigrams_aux`) as command names.
- **Controls.** The controls' phases are named `after-46` and `end`, not `start` and `end`.
- **Sleep overlap.** One run window overlaps a Mac sleep: web-search's repeats window, 08:21 sleep. That
  window's repeat 3 is replaced by the redone rows. The checker (check 9) shows that its repeat 2 ended
  before the sleep.
