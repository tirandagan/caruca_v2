# Numbers for the PaSh-suite report

Written by `count_report.py` from `validation_2026-11-24`. Every rate is "a of b". Do not edit by hand; re-run the script.

- Scripts run: 1. Scripts whose plain-bash output is the same in every bash run (**N**): 1.
- Distinct parts sent to PaSh (**P**): 1. Command uses inside those parts (**U**): 9.
- Command uses that ran outside every part sent to PaSh (not in U): PaSh's own files 0, Naive LLM's files 0, Caruca's files, PaSh grammar 0, Caruca's files, main grammar 0.

## Table 1: What PaSh did with each source's files

| Source | Output same as bash | Scripts with any part run in parallel | Parts run in parallel | Command uses split | Faster than bash |
|---|---:|---:|---:|---:|---:|
| PaSh's own files (reference) | 1 of 1 | 1 of 1 | 1 of 1 | 5 of 9 | 1 of 1 (median speed-up 1.67x) |
| Naive LLM's files | 1 of 1 | 1 of 1 | 1 of 1 | 4 of 9 | 1 of 1 (median speed-up 1.15x) |
| Caruca's files, PaSh grammar | 1 of 1 | 1 of 1 | 1 of 1 | 5 of 9 | 0 of 1 (median speed-up 0.96x) |
| Caruca's files, main grammar | 1 of 1 | 1 of 1 | 1 of 1 | 5 of 9 | 0 of 1 (median speed-up 0.97x) |

## Table 2: Commands a source brings its own files for, and what PaSh did with them

| Source | Uses with the source's own files | … split with them | … the same uses split with PaSh's own files | Uses with PaSh's own files filled in | … result same as with PaSh's own | Uses with no files from anyone |
|---|---:|---:|---:|---:|---:|---:|
| Naive LLM's files | 6 of 9 | 2 of 6 | 3 of 6 | 3 of 9 | 3 of 3 | 0 of 9 |
| Caruca's files, PaSh grammar | 2 of 9 | 1 of 2 | 1 of 2 | 7 of 9 | 7 of 7 | 0 of 9 |
| Caruca's files, main grammar | 2 of 9 | 1 of 2 | 1 of 2 | 7 of 9 | 7 of 7 | 0 of 9 |


## Chart A data: the scripts' parts, compared with PaSh's own files

Reference, PaSh's own files: run in parallel 1 of 1; not 0 of 1.

| Source | Run in parallel with both | Only with this source | With neither | Only with PaSh's own files |
|---|---:|---:|---:|---:|
| Naive LLM's files | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 |
| Caruca's files, PaSh grammar | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 |
| Caruca's files, main grammar | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 |

## Table 3: Every command where a source changed what PaSh did

| Command | Uses in the suite | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | Output |
|---|---:|---:|---:|---:|---:|---|
| `cat` | 1 | split 0 of 1 | **split 1 of 1** | **split 1 of 1** | **split 1 of 1** | all same as bash |
| `col` | 1 | split 1 of 1 | **split 0 of 1** | split 1 of 1 | split 1 of 1 | all same as bash |
| `sed` | 1 | split 1 of 1 | **split 0 of 1** | split 1 of 1 | split 1 of 1 | all same as bash |
| `sort` | 1 | split 1 of 1 | split 1 of 1 | **split 0 of 1** | **split 0 of 1** | all same as bash |

The other 3 commands: every source gave the same result as PaSh's own files (tr, comm, uniq). Bold = differs from PaSh's own.

## Chart B data: time against PaSh's own files

Noise (PaSh's own files, second copy against the first copy): largest difference 0.2% over 1 scripts.

| Source | Script | Median s, PaSh's own files | Median s, this source | Output same as bash | Split choices differ |
|---|---|---:|---:|---|---|
| Naive LLM's files | oneliners/spell | 0.64 | 0.93 | yes | yes |
| Caruca's files, PaSh grammar | oneliners/spell | 0.64 | 1.10 | yes | yes |
| Caruca's files, main grammar | oneliners/spell | 0.64 | 1.09 | yes | yes |

## Chart C data: which of the suite's commands each source has files for

- PaSh's own files: 7 of 7 commands (cat, col, comm, sed, sort, tr, uniq)
- Naive LLM's files: 6 of 7 commands (cat, col, comm, sed, sort, uniq)
- Caruca's files (both grammars): 2 of 7 commands (cat, sort)
- Files from nobody: 0 of 7 ()
- Scripts using each command (of 1): cat 1, col 1, comm 1, sed 1, sort 1, tr 1, uniq 1

## Table 4: Next to the Caruca paper's PaSh check

Agreement with PaSh's own files on the suite's own command lines (each distinct command line for which the source has its own files and PaSh's own files exist):

| Source | Command lines | Same inputs and outputs | Same split decision | Commands with every line agreeing | Lines where PaSh's own files give no split answer (left out) | Of the disagreements: PaSh's own split only with a special merge step, source says no split | Lines where the source's files raised an error |
|---|---:|---:|---:|---:|---:|---:|---:|
| Naive LLM's files | 6 | 6 of 6 | 2 of 4 | 2 of 4 | 2 | 0 | 0 |
| Caruca's files, PaSh grammar | 2 | 2 of 2 | 0 of 1 | 0 of 1 | 1 | 1 | 0 |
| Caruca's files, main grammar | 2 | 2 of 2 | 0 of 1 | 0 of 1 | 1 | 1 | 0 |

| What was checked | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| Suite output identical with the files swapped in | 1 of 1 | 1 of 1 | 1 of 1 | 1 of 1 |
| Parts PaSh ran in parallel | 1 of 1 | 1 of 1 | 1 of 1 | 1 of 1 |
| Median speed-up against bash | 1.67x | 1.15x | 0.96x | 0.97x |

## Appendix A1: the scripts

| 2022 set | Koala group | Script | Path in Koala | Stands for | How close | Run here | Input bytes |
|---|---|---|---|---|---|---|---:|
| Classics | oneliners | nfa-regex | `~/koala/oneliners/scripts/nfa-regex.sh` | `~/pash/evaluation/benchmarks/oneliners/nfa-regex.sh` | same | no | 10270030 |
| Classics | oneliners | sort | `~/koala/oneliners/scripts/sort.sh` | `~/pash/evaluation/benchmarks/oneliners/sort.sh` | same | no | 30810090 |
| Classics | oneliners | top-n | `~/koala/oneliners/scripts/top-n.sh` | `~/pash/evaluation/benchmarks/oneliners/top-n.sh` | light edit: same pipeline with a stage added or swapped | no | 30810090 |
| Classics | oneliners | wf | `~/koala/oneliners/scripts/wf.sh` | `~/pash/evaluation/benchmarks/oneliners/wf.sh` | light edit: same pipeline with a stage added or swapped | no | 30810090 |
| Classics | oneliners | spell | `~/koala/oneliners/scripts/spell.sh` | `~/pash/evaluation/benchmarks/oneliners/spell.sh` | light edit: same pipeline with a stage added or swapped | yes | 30810090 |
| Classics | oneliners | diff | `~/koala/oneliners/scripts/diff.sh` | `~/pash/evaluation/benchmarks/oneliners/diff.sh` | same commands; input wiring or option spelling changed | no | 30810090 |
| Classics | oneliners | bi-grams | `~/koala/oneliners/scripts/bi-grams.sh` | `~/pash/evaluation/benchmarks/oneliners/bi-grams.sh` | light edit: same pipeline with a stage added or swapped | no | 30810090 |
| Classics | oneliners | set-diff | `~/koala/oneliners/scripts/set-diff.sh` | `~/pash/evaluation/benchmarks/oneliners/set-diff.sh` | same commands; input wiring or option spelling changed | no | 30810090 |
| Classics | oneliners | sort-sort | `~/koala/oneliners/scripts/sort-sort.sh` | `~/pash/evaluation/benchmarks/oneliners/sort-sort.sh` | same | no | 30810090 |
| – | oneliners | uniq-ips | `~/koala/oneliners/scripts/uniq-ips.sh` | – | new in Koala (no published original) | no | 7096110 |
| – | oneliners | comm | `~/koala/oneliners/scripts/comm.sh` | – | new in Koala (no published original) | no | 11432645 |
| – | oneliners | opt-parallel | `~/koala/oneliners/scripts/opt-parallel.sh` | – | new in Koala (no published original) | no | 112699617 |
| Unix50 | unixfun | 1 | `~/koala/unixfun/scripts/1.sh` | `~/pash/evaluation/benchmarks/unix50/1.sh` | same | no | 31450500 |
| Unix50 | unixfun | 2 | `~/koala/unixfun/scripts/2.sh` | `~/pash/evaluation/benchmarks/unix50/2.sh` | same | no | 31450500 |
| Unix50 | unixfun | 3 | `~/koala/unixfun/scripts/3.sh` | `~/pash/evaluation/benchmarks/unix50/3.sh` | same | no | 31450500 |
| Unix50 | unixfun | 4 | `~/koala/unixfun/scripts/4.sh` | `~/pash/evaluation/benchmarks/unix50/4.sh` | same | no | 31450500 |
| Unix50 | unixfun | 5 | `~/koala/unixfun/scripts/5.sh` | `~/pash/evaluation/benchmarks/unix50/5.sh` | same | no | 31435500 |
| Unix50 | unixfun | 6 | `~/koala/unixfun/scripts/6.sh` | `~/pash/evaluation/benchmarks/unix50/6.sh` | same | no | 31456920 |
| Unix50 | unixfun | 7 | `~/koala/unixfun/scripts/7.sh` | `~/pash/evaluation/benchmarks/unix50/7.sh` | same | no | 31450200 |
| Unix50 | unixfun | 8 | `~/koala/unixfun/scripts/8.sh` | `~/pash/evaluation/benchmarks/unix50/8.sh` | same | no | 31450200 |
| Unix50 | unixfun | 9 | `~/koala/unixfun/scripts/9.sh` | `~/pash/evaluation/benchmarks/unix50/9.sh` | same | no | 31450200 |
| Unix50 | unixfun | 10 | `~/koala/unixfun/scripts/10.sh` | `~/pash/evaluation/benchmarks/unix50/10.sh` | same | no | 31450200 |
| Unix50 | unixfun | 11 | `~/koala/unixfun/scripts/11.sh` | `~/pash/evaluation/benchmarks/unix50/11.sh` | same | no | 31450200 |
| Unix50 | unixfun | 12 | `~/koala/unixfun/scripts/12.sh` | `~/pash/evaluation/benchmarks/unix50/12.sh` | same | no | 31450200 |
| Unix50 | unixfun | 13 | `~/koala/unixfun/scripts/13.sh` | `~/pash/evaluation/benchmarks/unix50/13.sh` | same | no | 31457250 |
| Unix50 | unixfun | 14 | `~/koala/unixfun/scripts/14.sh` | `~/pash/evaluation/benchmarks/unix50/14.sh` | same | no | 31456590 |
| Unix50 | unixfun | 15 | `~/koala/unixfun/scripts/15.sh` | `~/pash/evaluation/benchmarks/unix50/15.sh` | same | no | 31452780 |
| Unix50 | unixfun | 16 | `~/koala/unixfun/scripts/16.sh` | `~/pash/evaluation/benchmarks/unix50/16.sh` | same | no | 31452780 |
| Unix50 | unixfun | 17 | `~/koala/unixfun/scripts/17.sh` | `~/pash/evaluation/benchmarks/unix50/17.sh` | same | no | 31452780 |
| Unix50 | unixfun | 18 | `~/koala/unixfun/scripts/18.sh` | `~/pash/evaluation/benchmarks/unix50/18.sh` | same | no | 30451500 |
| Unix50 | unixfun | 19 | `~/koala/unixfun/scripts/19.sh` | `~/pash/evaluation/benchmarks/unix50/19.sh` | same | no | 30451500 |
| Unix50 | unixfun | 20 | `~/koala/unixfun/scripts/20.sh` | `~/pash/evaluation/benchmarks/unix50/20.sh` | same | no | 30451500 |
| Unix50 | unixfun | 21 | `~/koala/unixfun/scripts/21.sh` | `~/pash/evaluation/benchmarks/unix50/21.sh` | same | no | 30451500 |
| Unix50 | unixfun | 23 | `~/koala/unixfun/scripts/23.sh` | `~/pash/evaluation/benchmarks/unix50/23.sh` | same | no | 31456080 |
| Unix50 | unixfun | 24 | `~/koala/unixfun/scripts/24.sh` | `~/pash/evaluation/benchmarks/unix50/24.sh` | same | no | 31455600 |
| Unix50 | unixfun | 25 | `~/koala/unixfun/scripts/25.sh` | `~/pash/evaluation/benchmarks/unix50/25.sh` | same | no | 31457160 |
| Unix50 | unixfun | 26 | `~/koala/unixfun/scripts/26.sh` | `~/pash/evaluation/benchmarks/unix50/26.sh` | same | no | 31457250 |
| Unix50 | unixfun | 28 | `~/koala/unixfun/scripts/28.sh` | `~/pash/evaluation/benchmarks/unix50/28.sh` | same | no | 31457280 |
| Unix50 | unixfun | 29 | `~/koala/unixfun/scripts/29.sh` | `~/pash/evaluation/benchmarks/unix50/29.sh` | same | no | 31454130 |
| Unix50 | unixfun | 30 | `~/koala/unixfun/scripts/30.sh` | `~/pash/evaluation/benchmarks/unix50/30.sh` | same | no | 31457250 |
| Unix50 | unixfun | 31 | `~/koala/unixfun/scripts/31.sh` | `~/pash/evaluation/benchmarks/unix50/31.sh` | same | no | 31457250 |
| Unix50 | unixfun | 32 | `~/koala/unixfun/scripts/32.sh` | `~/pash/evaluation/benchmarks/unix50/32.sh` | same | no | 31393080 |
| Unix50 | unixfun | 33 | `~/koala/unixfun/scripts/33.sh` | `~/pash/evaluation/benchmarks/unix50/33.sh` | same | no | 31393080 |
| Unix50 | unixfun | 34 | `~/koala/unixfun/scripts/34.sh` | `~/pash/evaluation/benchmarks/unix50/34.sh` | same | no | 31393080 |
| Unix50 | unixfun | 35 | `~/koala/unixfun/scripts/35.sh` | `~/pash/evaluation/benchmarks/unix50/35.sh` | same | no | 31425810 |
| Unix50 | unixfun | 36 | `~/koala/unixfun/scripts/36.sh` | `~/pash/evaluation/benchmarks/unix50/36.sh` | same | no | 31425810 |
| COVID-mts | covid | 1 | `~/koala/covid/scripts/1.sh` | `~/pash/evaluation/benchmarks/analytics-mts/1.sh` | same commands; input wiring or option spelling changed | no | 3589542298 |
| COVID-mts | covid | 2 | `~/koala/covid/scripts/2.sh` | `~/pash/evaluation/benchmarks/analytics-mts/2.sh` | same commands; input wiring or option spelling changed | no | 3589542298 |
| COVID-mts | covid | 3 | `~/koala/covid/scripts/3.sh` | `~/pash/evaluation/benchmarks/analytics-mts/3.sh` | same commands; input wiring or option spelling changed | no | 3589542298 |
| COVID-mts | covid | 4 | `~/koala/covid/scripts/4.sh` | `~/pash/evaluation/benchmarks/analytics-mts/4.sh` | same commands; input wiring or option spelling changed | no | 3589542298 |
| COVID-mts | covid | 5 | `~/koala/covid/scripts/5.sh` | `~/pash/evaluation/benchmarks/analytics-mts/5.sh` | same commands; input wiring or option spelling changed | no | 3589542298 |
| NLP | nlp | syllable_words_1 | `~/koala/nlp/scripts/syllable_words_1.sh` | `~/pash/evaluation/benchmarks/nlp/6_4.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | syllable_words_2 | `~/koala/nlp/scripts/syllable_words_2.sh` | `~/pash/evaluation/benchmarks/nlp/6_5.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | letter_words | `~/koala/nlp/scripts/letter_words.sh` | `~/pash/evaluation/benchmarks/nlp/6_2.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | bigrams_appear_twice | `~/koala/nlp/scripts/bigrams_appear_twice.sh` | `~/pash/evaluation/benchmarks/nlp/8.2_2.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | bigrams | `~/koala/nlp/scripts/bigrams.sh` | `~/pash/evaluation/benchmarks/nlp/4_3.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | compare_exodus_genesis | `~/koala/nlp/scripts/compare_exodus_genesis.sh` | `~/pash/evaluation/benchmarks/nlp/8.3_3.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | count_consonant_seq | `~/koala/nlp/scripts/count_consonant_seq.sh` | `~/pash/evaluation/benchmarks/nlp/7_2.sh` | same commands; input wiring or option spelling changed | no | 1118570034 |
| NLP | nlp | count_morphs | `~/koala/nlp/scripts/count_morphs.sh` | `~/pash/evaluation/benchmarks/nlp/7_1.sh` | same commands; input wiring or option spelling changed | no | 1118570034 |
| NLP | nlp | count_trigrams | `~/koala/nlp/scripts/count_trigrams.sh` | `~/pash/evaluation/benchmarks/nlp/4_3b.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | count_vowel_seq | `~/koala/nlp/scripts/count_vowel_seq.sh` | `~/pash/evaluation/benchmarks/nlp/2_2.sh` | same commands; input wiring or option spelling changed | no | 1118570034 |
| NLP | nlp | count_words | `~/koala/nlp/scripts/count_words.sh` | `~/pash/evaluation/benchmarks/nlp/1_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | find_anagrams | `~/koala/nlp/scripts/find_anagrams.sh` | `~/pash/evaluation/benchmarks/nlp/8.3_2.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | merge_upper | `~/koala/nlp/scripts/merge_upper.sh` | `~/pash/evaluation/benchmarks/nlp/2_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | sort | `~/koala/nlp/scripts/sort.sh` | `~/pash/evaluation/benchmarks/nlp/3_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | sort_words_by_folding | `~/koala/nlp/scripts/sort_words_by_folding.sh` | `~/pash/evaluation/benchmarks/nlp/3_2.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | sort_words_by_num_of_syllables | `~/koala/nlp/scripts/sort_words_by_num_of_syllables.sh` | `~/pash/evaluation/benchmarks/nlp/8_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | sort_words_by_rhyming | `~/koala/nlp/scripts/sort_words_by_rhyming.sh` | `~/pash/evaluation/benchmarks/nlp/3_3.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | trigram_rec | `~/koala/nlp/scripts/trigram_rec.sh` | `~/pash/evaluation/benchmarks/nlp/6_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | uppercase_by_token | `~/koala/nlp/scripts/uppercase_by_token.sh` | `~/pash/evaluation/benchmarks/nlp/6_1_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | uppercase_by_type | `~/koala/nlp/scripts/uppercase_by_type.sh` | `~/pash/evaluation/benchmarks/nlp/6_1_2.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | verses_2om_3om_2instances | `~/koala/nlp/scripts/verses_2om_3om_2instances.sh` | `~/pash/evaluation/benchmarks/nlp/6_7.sh` | same commands; input wiring or option spelling changed | no | 1118570034 |
| NLP | nlp | vowel_sequencies_gr_1K | `~/koala/nlp/scripts/vowel_sequencies_gr_1K.sh` | `~/pash/evaluation/benchmarks/nlp/8.2_1.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| NLP | nlp | words_no_vowels | `~/koala/nlp/scripts/words_no_vowels.sh` | `~/pash/evaluation/benchmarks/nlp/6_3.sh` | light edit: same pipeline with a stage added or swapped | no | 1118570034 |
| AvgTemp | weather | max-temp | `~/koala/weather/scripts/temp-analytics.sh` | `~/pash/evaluation/benchmarks/max-temp/temp-analytics.sh` | same analysis; the download step (curl, gunzip) removed, input is a prepared file | no | – |
| – | weather | tuft-weather | `~/koala/weather/scripts/tuft-weather.sh` | – | new in Koala (no published original) | no | 936125600 |
| WebIndex | web-search | web-index | `~/koala/web-search/scripts/engine.sh` | `~/pash/evaluation/benchmarks/web-index/web-index.sh` | rewritten: a crawl-and-index loop with Node.js helpers instead of one pipeline | no | – |
| FileEnc | file-mod | compress_files | `~/koala/file-mod/scripts/compress_files.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/compress_files.sh` | rewritten: gzip from standard input instead of zip on a file | no | – |
| FileEnc | file-mod | encrypt_files | `~/koala/file-mod/scripts/encrypt_files.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/encrypt_files.sh` | same tool and settings; reads standard input instead of a named file | no | – |
| MediaConv | file-mod | img_convert | `~/koala/file-mod/scripts/img_convert.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/img_convert.sh` | same tool and settings; reads standard input instead of a named file | no | – |
| MediaConv | file-mod | to_mp3 | `~/koala/file-mod/scripts/to_mp3.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/to_mp3.sh` | same tool and settings; reads standard input instead of a named file | no | – |
| – | file-mod | thumbnail_generation | `~/koala/file-mod/scripts/thumbnail_generation.sh` | – | new in Koala (no published original) | no | – |
| AurPkg | pkg | pacaur | `~/koala/pkg/scripts/pacaur.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/pacaur.sh` | same idea (fetch build file, build with makedeb); fetch source moved to Koala server, adds key fetch | no | – |
| ProgInf | pkg | proginf | `~/koala/pkg/scripts/proginf.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/proginf.sh` | same tool (mir-sa); package list now read from an index file | no | – |
| LogAnalysis | analytics | nginx | `~/koala/analytics/scripts/nginx.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/nginx.sh` | same pipelines; log now read from standard input through a temporary file | no | – |
| LogAnalysis | analytics | pcaps | `~/koala/analytics/scripts/pcaps.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/pcap.sh` | same pipelines plus one more tcpdump query; capture read from standard input | no | – |
| – | analytics | port-scan | `~/koala/analytics/scripts/port-scan.sh` | – | new in Koala (no published original) | no | – |
| – | analytics | ray-tracing | `~/koala/analytics/scripts/ray-tracing.sh` | – | new in Koala (no published original) | no | – |
| Genomics | bio | bio | `~/koala/bio/scripts/bio.sh` | `~/pash/evaluation/benchmarks/dependency_untangling/genomics.sh` | same samtools steps; restructured loop, system samtools instead of a bundled one | no | – |
| – | bio | data | `~/koala/bio/scripts/data.sh` | – | new in Koala (TERA-Seq reference preparation) | no | – |
| – | bio | run_dRNASeq | `~/koala/bio/scripts/run_dRNASeq.sh` | – | new in Koala (TERA-Seq) | no | – |
| – | bio | run_5TERA | `~/koala/bio/scripts/run_5TERA.sh` | – | new in Koala (TERA-Seq) | no | – |

## Appendix A3: why parts were not run in parallel

Distinct parts. Each cell: the same under PaSh's own files / only with this source.

| Reason | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| parts considered | 1 | 1 | 1 | 1 |

Per execution (a loop's part counts once per pass). Each cell: the same under PaSh's own files / only with this source.

| Reason | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar |
|---|---:|---:|---:|---:|
| parts considered | 1 | 1 | 1 | 1 |

## Appendix A4: every use whose result differs from PaSh's own

| Script | Command line | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | Output same as bash |
|---|---|---|---|---|---|---|
| oneliners/spell | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | whole | split | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `sed '"s/[^[:print:]]//g"'` | split | whole | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `col -bx` | split | whole | split | split | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |
| oneliners/spell | `sort` | split | split | whole | whole | Naive LLM's files: yes, Caruca's files, PaSh grammar: yes, Caruca's files, main grammar: yes |

Why the use was left whole, where it was:

- oneliners/spell `cat ~/t024/shadow/oneliners/inputs/30M.txt`, PaSh's own files: no answer
- oneliners/spell `sed '"s/[^[:print:]]//g"'`, Naive LLM's files: file says no split
- oneliners/spell `col -bx`, Naive LLM's files: file says no split
- oneliners/spell `sort`, Caruca's files, PaSh grammar: file says no split
- oneliners/spell `sort`, Caruca's files, main grammar: file says no split

The files' answers on each command line the source has its own files for:

| Source | Command line | Same inputs and outputs | Source's answer | PaSh's own answer |
|---|---|---|---|---|
| Naive LLM's files | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Naive LLM's files | `col -bx` | yes | says no split | allows a split |
| Naive LLM's files | `comm -23 - ~/t024/shadow/oneliners/inputs/dict.txt` | yes | says no split | no answer |
| Naive LLM's files | `sed '"s/[^[:print:]]//g"'` | yes | says no split | allows a split |
| Naive LLM's files | `sort` | yes | allows a split | allows a split |
| Naive LLM's files | `uniq` | yes | allows only a split PaSh has not implemented | allows only a split PaSh has not implemented |
| Caruca's files, PaSh grammar | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca's files, PaSh grammar | `sort` | yes | says no split | allows a split |
| Caruca's files, main grammar | `cat ~/t024/shadow/oneliners/inputs/30M.txt` | yes | allows a split | no answer |
| Caruca's files, main grammar | `sort` | yes | says no split | allows a split |

## Appendix A5: times per script (seconds, median and min–max)

| Script | Plain bash | PaSh's own files | Naive LLM's files | Caruca's files, PaSh grammar | Caruca's files, main grammar | PaSh's own files, second copy |
|---|---:|---:|---:|---:|---:|---:|
| oneliners/spell | 1.06 (1.04–1.08, 3 runs) | 0.64 (0.61–0.67, 3 runs) | 0.93 (0.89–0.96, 3 runs) | 1.10 (1.10–1.11, 3 runs) | 1.09 (1.07–1.10, 3 runs) | 0.64 (0.63–0.67, 3 runs) |

## Appendix A6 (from the records): controls and run windows

| When | Control | Commands split | Output same as bash |
|---|---|---|---|
| start | Naive LLM's files | cat, sort, tr | yes |
| start | Control: naive LLM's files, sort's files removed | none | yes |
| start | Control: naive LLM's files, PaSh's own col files | cat, col, sort, tr | yes |
| start | Control: naive LLM's files, PaSh's own cat files | sort, tr | yes |
| start | Control: naive LLM's files, PaSh's own sed files | cat, sed, sort, tr | yes |
| end | Naive LLM's files | cat, sort, tr | yes |
| end | Control: naive LLM's files, sort's files removed | none | yes |
| end | Control: naive LLM's files, PaSh's own col files | cat, col, sort, tr | yes |
| end | Control: naive LLM's files, PaSh's own cat files | sort, tr | yes |
| end | Control: naive LLM's files, PaSh's own sed files | cat, sed, sort, tr | yes |

| Record | When | Script | Start | End | VM load at start | VM load at end | Koala changed | Mac power check |
|---|---|---|---|---|---|---|---|---|
| controls.jsonl | start | oneliners/spell | 2026-11-24 11:43:20 -0500 | 2026-11-24 11:43:32 -0500 | 0.31, 1.18, 0.89 | 1.06, 1.31, 0.94 | no | awake, on mains power |
| results.jsonl | main | oneliners/spell | 2026-11-24 11:43:32 -0500 | 2026-11-24 11:44:05 -0500 | 1.06, 1.31, 0.94 | 3.09, 1.72, 1.09 | no | awake, on mains power |
| controls.jsonl | end | oneliners/spell | 2026-11-24 11:44:06 -0500 | 2026-11-24 11:44:19 -0500 | 3.09, 1.72, 1.09 | 3.23, 1.82, 1.13 | no | awake, on mains power |

## Checks the script made on the records

| Check | Result | Detail |
|---|---|---|
| bash's own output is identical across all its runs | passed | 1 of 1 scripts; varying: none |
| the distinct parts are the same for every source (same texts, same count) | passed | PaSh's own files: 1; Naive LLM's files: 1; Caruca's files, PaSh grammar: 1; Caruca's files, main grammar: 1 |
| each script sends the same sequence of part texts to PaSh under every source (repeat 1) | passed |  |
| the part count in results.jsonl equals the parts listed in regions.jsonl | passed |  |
| the command uses are the same for every source (same part, same position) | passed | PaSh's own files: 9; Naive LLM's files: 9; Caruca's files, PaSh grammar: 9; Caruca's files, main grammar: 9 |
| a use that appears in more than one launch of a script has the same result in each | passed | 0 differ |
| the commands split per use match the commands split per script in results.jsonl | passed |  |
| PaSh split a use exactly when its files allowed a split PaSh can carry out | passed | 0 uses where the answer and PaSh differ |
| every instrumented repeat split the same uses as repeat 1 | passed | 36 uses x sources, up to 3 repeats each; 0 vary |
| Naive LLM's files: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| Caruca's files, PaSh grammar: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| Caruca's files, main grammar: a command line gets the same answer in every script that uses it | passed | 0 lines differ |
| every script run is in the inventory | passed |  |
| the commands the inventory lists equal the commands seen starting, per script | passed | listed, not seen: []; seen, not listed: [] |
| the folder-decides controls were run at the start and the end | passed | phases found: ['end', 'start']; sets: 6 |
| Koala's checkout did not change during any run window | passed |  |
| the Mac was awake and on mains power in every run window | passed | 3 of 3 windows; from timing_check_pilot.jsonl |
