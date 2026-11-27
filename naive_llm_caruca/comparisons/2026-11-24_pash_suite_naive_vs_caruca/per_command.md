# Naive LLM vs PaSh's Own Annotation Files, Command by Command

Built by `per_command.py` from `full_run/` (86 scripts, 177 distinct parts, 609 command uses inside parts across 44 distinct commands). Per-command and per-part counts use `phase == "main"` and `mode == "instrumented"`. Wall-clock numbers in Section 4 apply the same two fix-ups as `prep_full_records.py` and `full_run/numbers.md` (same-repeat bash comparison; 7 `web-search/engine` timed rows missing `node` dropped; 7 superseded rows replaced by redone repeats).

"File said 'no split'" and "raised an error" use `file_answer` (the file's answer to the words as PaSh passes them, matching what PaSh actually acted on). "Parts where the naive file made PaSh's compiler stop and PaSh's own did not (and the reverse)" counts distinct parts with `outcome == "pash crash"` under one set and not the other, attributed programmatically to the culprit command using `full_run/answers/*.jsonl.gz` (see footnote below Section 1).

## 1. Per-Command Comparison (Commands Used Inside Parts)

| Command | Naive LLM has a file | PaSh's own has a file | Uses in parts | Uses split with PaSh's own | Uses split with naive LLM | Naive file said "no split" | Naive file raised an error | PaSh's own file said "no split" | Parts: compiler stop (naive only / PaSh's own only) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| `cat` | yes | yes | 94 of 609 | 0 of 94 | 43 of 94 | 0 of 94 | 0 of 94 | 0 of 94 | naive: 0 of 90; PaSh's own: 0 of 90 | `naive splits more` |
| `tr` | yes | yes | 75 of 609 | 29 of 75 | 40 of 75 | 5 of 75 | 0 of 75 | 0 of 75 | naive: 0 of 50; PaSh's own: 0 of 50 | `naive splits more` |
| `grep` | yes | yes | 74 of 609 | 29 of 74 | 30 of 74 | 7 of 74 | 0 of 74 | 7 of 74 | naive: 0 of 54; PaSh's own: 0 of 54 | `naive splits more` |
| `sort` | yes | yes | 67 of 609 | 25 of 67 | 32 of 67 | 0 of 67 | 0 of 67 | 9 of 67 | naive: 0 of 46; PaSh's own: 0 of 46 | `naive splits more` |
| `cut` | yes | yes | 58 of 609 | 36 of 58 | 39 of 58 | 0 of 58 | 0 of 58 | 0 of 58 | naive: 0 of 38; PaSh's own: 0 of 38 | `naive splits more` |
| `sed` | yes | yes | 37 of 609 | 6 of 37 | 1 of 37 | 36 of 37 | 0 of 37 | 24 of 37 | naive: 0 of 25; PaSh's own: 0 of 25 | `naive splits less` |
| `mkdir` | yes | no | 31 of 609 | 0 of 31 | 0 of 31 | 31 of 31 | 0 of 31 | 0 of 31 | naive: 0 of 31; PaSh's own: 0 of 31 | `naive only` |
| `echo` | no | no | 30 of 609 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 30 | naive: 0 of 26; PaSh's own: 0 of 26 | `neither splits` |
| `uniq` | yes | yes | 30 of 609 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 30 | naive: 0 of 30; PaSh's own: 0 of 30 | `neither splits` |
| `awk` | yes | yes | 14 of 609 | 0 of 14 | 7 of 14 | 5 of 14 | 0 of 14 | 0 of 14 | naive: 0 of 11; PaSh's own: 0 of 11 | `naive splits more` |
| `export` | no | no | 13 of 609 | 0 of 13 | 0 of 13 | 0 of 13 | 0 of 13 | 0 of 13 | naive: 0 of 13; PaSh's own: 0 of 13 | `neither splits` |
| `pure_func` | no | no | 12 of 609 | 0 of 12 | 0 of 12 | 0 of 12 | 0 of 12 | 0 of 12 | naive: 0 of 12; PaSh's own: 0 of 12 | `neither splits` |
| `head` | yes | yes | 10 of 609 | 0 of 10 | 0 of 10 | 7 of 10 | 0 of 10 | 0 of 10 | naive: 0 of 10; PaSh's own: 0 of 10 | `neither splits` |
| `wc` | yes | yes | 8 of 609 | 0 of 8 | 0 of 8 | 0 of 8 | 8 of 8 | 0 of 8 | naive: 0 of 7; PaSh's own: 0 of 7 | `neither splits` |
| `comm` | yes | yes | 5 of 609 | 0 of 5 | 0 of 5 | 5 of 5 | 0 of 5 | 0 of 5 | naive: 0 of 4; PaSh's own: 0 of 4 | `neither splits` |
| `samtools` | no | no | 5 of 609 | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `[` | no | no | 4 of 609 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | naive: 0 of 3; PaSh's own: 0 of 3 | `neither splits` |
| `read` | no | no | 4 of 609 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | naive: 0 of 3; PaSh's own: 0 of 3 | `neither splits` |
| `join` | yes | no | 3 of 609 | 0 of 3 | 0 of 3 | 1 of 3 | 2 of 3 | 0 of 3 | naive: 0 of 1; PaSh's own: 0 of 1 | `naive only` |
| `rm` | yes | yes | 3 of 609 | 0 of 3 | 0 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | naive: 0 of 3; PaSh's own: 0 of 3 | `neither splits` |
| `tail` | yes | yes | 3 of 609 | 0 of 3 | 0 of 3 | 1 of 3 | 0 of 3 | 0 of 3 | naive: 0 of 3; PaSh's own: 2 of 3 | `neither splits` |
| `[[` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | naive: 0 of 2; PaSh's own: 0 of 2 | `neither splits` |
| `cd` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | naive: 0 of 2; PaSh's own: 0 of 2 | `neither splits` |
| `dirname` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | naive: 0 of 2; PaSh's own: 0 of 2 | `neither splits` |
| `fmt` | yes | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | naive: 2 of 2; PaSh's own: 0 of 2 | `naive only` |
| `mkfifo` | yes | yes | 2 of 609 | 0 of 2 | 0 of 2 | 2 of 2 | 0 of 2 | 0 of 2 | naive: 0 of 2; PaSh's own: 0 of 2 | `neither splits` |
| `rev` | yes | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | naive: 0 of 1; PaSh's own: 0 of 1 | `naive only` |
| `.` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `./crawl.sh` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `./index.sh` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `bigrams_aux` | no | yes | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `break` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `col` | yes | yes | 1 of 609 | 1 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `naive splits less` |
| `continue` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `diff` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `ffmpeg` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `find` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `gzip` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `mawk` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `mogrify` | yes | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `naive only` |
| `printf` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `python3` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `seq` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |
| `xargs` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | naive: 0 of 1; PaSh's own: 0 of 1 | `neither splits` |

**Notes on Section 1:**
- **Compiler-stop attribution:** Across the 177 distinct parts, PaSh's compiler stopped (`outcome == "pash crash"`) in 4 parts under PaSh's own files and 4 parts under the naive LLM's files. Two stops are shared under both sets (`covid/5` `AssertionError`; `oneliners/bi-grams` `NameError: name 'Arg' is not defined`). Two stops occur **only under the naive LLM**: `unixfun/34` and `unixfun/36`, both `AssertionError` in `pipe_append` because naive's `fmt` file misparsed `-w1` as a filename operand (`stdin: False` in a non-first pipeline stage; PaSh's own has no `fmt` file, so those parts stopped with `missing annotation`). Two stops occur **only under PaSh's own**: `unixfun/12` and `unixfun/16`, both `AssertionError` in `pipe_append` because PaSh's own `tail` file misparsed `-n 1` as a filename operand `1` (`stdin: False`; naive's `tail` file parsed `-n 1` with `stdin: True`, so both parts ran in parallel). Attributing each differential stop to the unique non-first command reporting `stdin: False` in `full_run/answers/*.jsonl.gz` assigns `2 of 2` parts to `fmt` (naive only) and `2 of 3` parts to `tail` (PaSh's own only). Co-occurring command counts for those parts are also recorded in `per_command.json`.
- **Why `tr`, `sort`, `cut`, `grep` split more under naive:** In `unixfun/12` and `unixfun/16`, avoiding PaSh's own `tail` crash accounts for all of naive's gains on `cut` (+3 uses) and `grep` (+1 use), 3 of 7 gained uses on `sort`, and 2 of 11 gained uses on `tr`. The remaining gains come directly from the commands' own files: `cat` (+43 single-file splits), `tr` (+9 `tr -d '\n'` uses where PaSh's own allows only an unimplemented split), `awk` (+7 uses where PaSh's own gives `no answer`), and `sort` (+4 `sort -u` uses in `covid/1`–`4` where PaSh's own says `no split`).
- **`file_answer` vs `direct_file_answer`:** For naive, `sed` says `no split` in 36 of 37 uses as PaSh passes the arguments (quotes kept on the script argument) vs 24 of 37 directly with quotes removed; `head` says `no split` in 7 of 10 uses as PaSh passes them vs 1 of 10 directly (the other 6 return an unimplemented split directly). PaSh's own files never raised an error (`0 of 609`).

## 2. Totals by File-Ownership Group

Totals over the 44 commands used inside parts (the 3 ownership groups with at least one file, plus the "Neither has a file" group so all counts reconcile to 44 commands and 609 uses). Only **1 of 44** commands in parts (`bigrams_aux`, 1 use in `oneliners/bi-grams`) has a file only in PaSh's own package — near none, because PaSh's other 9 PaSh-only files in `manifest.json` are internal benchmark helpers and test stubs (`alt_bigram_aux_reduce`, `alt_bigrams_aux`, `bigram_aux_map`, `bigram_aux_reduce`, `custom_sort`, `custom_tr`, `set_diff`, `test_one`, `test_two`) that do not appear in the suite's parts.

| Group | Commands (in parts) | Uses in parts | Uses split (PaSh's own) | Uses split (naive LLM) | Compiler stops (naive only / PaSh's own only) | Files raising (naive / PaSh's own) |
|---|---|---|---|---|---|---|
| Both have files | 18 of 44 | 484 of 609 | 126 of 484 | 192 of 484 | naive: 0 of 177; PaSh's own: 2 of 177 | naive: 8 of 484 (`wc`); PaSh's own: 0 of 484 |
| Only the naive LLM has a file | 5 of 44 | 39 of 609 | 0 of 39 | 0 of 39 | naive: 2 of 177; PaSh's own: 0 of 177 | naive: 2 of 39 (`join`); PaSh's own: 0 of 39 |
| Only PaSh's own has a file | 1 of 44 | 1 of 609 | 0 of 1 | 0 of 1 | naive: 0 of 177; PaSh's own: 0 of 177 | naive: 0 of 1; PaSh's own: 0 of 1 |
| Neither has a file (reconciliation) | 20 of 44 | 85 of 609 | 0 of 85 | 0 of 85 | naive: 0 of 177; PaSh's own: 0 of 177 | naive: 0 of 85; PaSh's own: 0 of 85 |

**Full package inventory (`manifest.json`):** The naive LLM wrote files for 82 commands and PaSh's own package has 30: 20 overlap (18 in parts; `tee` only outside parts; `mv` unused), 62 are naive-only (5 in parts; 4 outside parts only: `convert`, `iconv`, `ls`, `mktemp`; 53 unused in the 86 scripts), and 10 are PaSh-only (1 in parts: `bigrams_aux`; 9 unused).

## 3. What the Naive LLM Adds (Commands Where Only the Naive LLM Has a File)

Without a file, PaSh splits none of these commands, so any split here would be a pure gain. In practice, **0 of 39** uses of the 5 naive-only commands inside parts were split by PaSh: `mkdir` (31 uses) was rightly marked non-splittable; `join` (3 uses) rightly refused 1 use and raised an argument-parser exception on 2; `rev` (2 uses) was rightly marked splittable but its part hit an unrelated `NotImplementedError` on a redirection; `mogrify` (1 use) was marked `INDIV_FILES` splittable but rejected by PaSh as non-streaming output (`OTHER_OUTPUT`); and `fmt` (2 uses) was wrongly parsed and marked splittable, turning 2 `missing annotation` parts into PaSh compiler stops (`pash crash`).

### 3.1 Commands Used Inside Parts (5 commands, 39 uses)

| Command | Uses in parts | Naive file said | Split in PaSh | What happened to parts | Answer right in general? | Notes |
|---|---|---|---|---|---|---|
| `mkdir` | 31 of 609 | says no split: 31 of 31 | 0 of 31 | missing annotation -> other (30), other -> other (1) | **right** | `mkdir` creates directories (filesystem side effects, not a data stream), so refusing to split is right. |
| `join` | 3 of 609 | raised: 2 of 3, says no split: 1 of 3 | 0 of 3 | other -> other (1) | **mixed (no-split right; raises wrong)** | The 1 'no split' answer is right for `join` in general under PaSh's stream-splitting model (joining two sorted inputs on a key requires key-partitioned co-shuffling, which PaSh does not implement). The 2 exceptions (`join requires exactly two operands`) are bugs in the naive file's argument parser. |
| `fmt` | 2 of 609 | allows a split: 2 of 2 | 0 of 2 | missing annotation -> pash crash (2) | **wrong** | `fmt` reflows paragraphs across line boundaries (and across multiple input files when there is no blank line between them), so splitting arbitrarily or per file does not preserve exact output in general. In addition, the naive file misparsed `-w1` as a filename operand (`stdin: False`), which triggered a PaSh compiler stop (`AssertionError` in `pipe_append`) in both parts that use it. |
| `rev` | 2 of 609 | allows a split: 2 of 2 | 0 of 2 | missing annotation -> unsupported construct (1) | **right** | `rev` reverses characters within each line independently, so splitting by line chunks and concatenating outputs preserves exact output. |
| `mogrify` | 1 of 609 | allows a split: 1 of 1 | 0 of 1 | missing annotation -> other (1) | **not sure** | Not sure: `mogrify` transforms each input image file independently, so per-file parallelism (`INDIV_FILES`) is semantically valid when output paths do not collide; however, `mogrify` writes files directly rather than streaming stdin to stdout, so PaSh cannot split it as a streaming stage (and rejected the part because of `OTHER_OUTPUT`). |

### 3.2 Commands Exercised Only Outside Parts (4 commands in `commands.jsonl.gz` / `answers/`)

Four additional naive-only commands ran in the suite only outside PaSh parts (so PaSh never compiled them, though `full_run/answers/*.jsonl.gz` recorded the naive files' direct answers). The other 53 naive-only files were not called by any script.

| Command | Scripts | Naive file direct answer | Answer right in general? | Notes |
|---|---|---|---|---|
| `convert` | 1 of 86 | no split: 1 of 1 | **right** | `convert -resize 70% - -` transforms a binary image stream on stdin/stdout; it cannot be split on line boundaries, so 'no split' is right. |
| `iconv` | 1 of 86 | allows a split: 1 of 1 | **not sure** | Not sure: `iconv` returned `INDIV_FILES -> CONCATENATE`; per-file transcoding is valid for independent files in stateless encodings (such as UTF-8/ASCII here), but can fail in general for stateful encodings (e.g. ISO-2022) or BOM handling across concatenated outputs. |
| `ls` | 23 of 86 | no split: 23 of 23 | **right** | `ls` lists directory entries with no input stream to split and global sorting of entries, so 'no split' is right. |
| `mktemp` | 11 of 86 | no split: 17 of 17 | **right** | `mktemp` creates a unique temporary file or directory (filesystem side effect, no input stream), so 'no split' is right. |

## 4. Wall-Clock Time

Per-command wall-clock time cannot be separated because all of a source's annotation files were swapped in at once (Tiran's decision, 2026-11-24), so any script-level timing difference belongs to the source as a whole. The only per-command time evidence in this run comes from scripts where exactly one command's split differed between the naive LLM's files and PaSh's own.

Across all 86 scripts, 43 of 86 have identical splits under both sets, 18 of 86 differ on 2 to 5 commands, and **25 of 86** differ on exactly one command — in **all 25**, that command is `cat` (1 single-file `cat` use split under naive and left unsplit under PaSh's own). No other command has a single-command-differing script.

Across those 25 `cat`-only scripts, the naive ÷ PaSh's own time ratio has geometric mean **1.21** (median **1.15**, range 0.98–1.74; above 1 means naive is slower). For reference, the identical second copy of PaSh's own files ranged from 0.83 to 1.13 (median 0.99); 15 of 25 `cat`-only scripts are slower than that upper noise bound and 0 of 25 are faster than the lower bound.

| Script | Sole differing command (naive vs PaSh's own) | PaSh's own median (s) | Naive LLM median (s) | Time ratio (naive ÷ PaSh's own) |
|---|---|---|---|---|
| `oneliners/nfa-regex` | `cat` (+1 / -0) | 1.94 | 1.90 | 0.98 |
| `oneliners/sort` | `cat` (+1 / -0) | 0.24 | 0.25 | 1.04 |
| `oneliners/sort-sort` | `cat` (+1 / -0) | 0.36 | 0.40 | 1.12 |
| `oneliners/top-n` | `cat` (+1 / -0) | 0.59 | 0.70 | 1.19 |
| `oneliners/uniq-ips` | `cat` (+1 / -0) | 0.18 | 0.21 | 1.15 |
| `oneliners/wf` | `cat` (+1 / -0) | 0.50 | 0.62 | 1.23 |
| `unixfun/1` | `cat` (+1 / -0) | 0.20 | 0.21 | 1.05 |
| `unixfun/10` | `cat` (+1 / -0) | 0.33 | 0.47 | 1.43 |
| `unixfun/11` | `cat` (+1 / -0) | 0.37 | 0.51 | 1.38 |
| `unixfun/13` | `cat` (+1 / -0) | 0.23 | 0.28 | 1.21 |
| `unixfun/15` | `cat` (+1 / -0) | 0.19 | 0.21 | 1.15 |
| `unixfun/17` | `cat` (+1 / -0) | 0.35 | 0.36 | 1.03 |
| `unixfun/18` | `cat` (+1 / -0) | 0.19 | 0.33 | 1.74 |
| `unixfun/2` | `cat` (+1 / -0) | 0.28 | 0.30 | 1.07 |
| `unixfun/20` | `cat` (+1 / -0) | 0.17 | 0.17 | 0.98 |
| `unixfun/21` | `cat` (+1 / -0) | 0.55 | 0.64 | 1.17 |
| `unixfun/3` | `cat` (+1 / -0) | 0.13 | 0.17 | 1.30 |
| `unixfun/32` | `cat` (+1 / -0) | 0.23 | 0.26 | 1.14 |
| `unixfun/33` | `cat` (+1 / -0) | 0.20 | 0.25 | 1.22 |
| `unixfun/35` | `cat` (+1 / -0) | 0.18 | 0.21 | 1.13 |
| `unixfun/4` | `cat` (+1 / -0) | 0.34 | 0.37 | 1.06 |
| `unixfun/5` | `cat` (+1 / -0) | 0.18 | 0.20 | 1.11 |
| `unixfun/7` | `cat` (+1 / -0) | 0.19 | 0.31 | 1.59 |
| `unixfun/8` | `cat` (+1 / -0) | 0.20 | 0.31 | 1.57 |
| `unixfun/9` | `cat` (+1 / -0) | 0.22 | 0.35 | 1.56 |
