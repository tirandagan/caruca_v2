# Caruca, full grammar where traced vs PaSh's own files, command by command

Built by `per_command_caruca.py caruca-main-all` from `full_run_caruca_all/` (86 scripts, 177 distinct parts, 609 command uses inside parts, 44 distinct commands). Counts only. Splits and parts are from the pass with the stand-in programs; times are medians of the three timed repeats. 'Said no split' and 'raised' are the files' answers to the words as PaSh passes them. A compiler stop is a part whose outcome is 'pash crash' under one set and not the other.

## 1. Per command (commands used inside parts)

| Command | Caruca has a file | PaSh's own has a file | Uses in parts | Split with PaSh's own | Split with Caruca | Caruca said no split | Caruca raised | PaSh's own said no split | Compiler stops (Caruca only / PaSh's own only) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| `cat` | yes | yes | 94 of 609 | 0 of 94 | 40 of 94 | 0 of 94 | 0 of 94 | 0 of 94 | 0 of 90 / 0 of 90 | `Caruca splits more` |
| `tr` | yes | yes | 75 of 609 | 29 of 75 | 27 of 75 | 33 of 75 | 0 of 75 | 0 of 75 | 0 of 50 / 0 of 50 | `Caruca splits less` |
| `grep` | yes | yes | 74 of 609 | 29 of 74 | 29 of 74 | 8 of 74 | 0 of 74 | 7 of 74 | 0 of 54 / 0 of 54 | `same` |
| `sort` | yes | yes | 67 of 609 | 25 of 67 | 0 of 67 | 67 of 67 | 0 of 67 | 9 of 67 | 0 of 46 / 0 of 46 | `Caruca splits less` |
| `cut` | yes | yes | 58 of 609 | 36 of 58 | 36 of 58 | 6 of 58 | 0 of 58 | 0 of 58 | 0 of 38 / 0 of 38 | `same` |
| `sed` | yes | yes | 37 of 609 | 6 of 37 | 24 of 37 | 3 of 37 | 0 of 37 | 24 of 37 | 0 of 25 / 0 of 25 | `Caruca splits more` |
| `mkdir` | no | no | 31 of 609 | 0 of 31 | 0 of 31 | 0 of 31 | 0 of 31 | 0 of 31 | 0 of 31 / 0 of 31 | `neither splits` |
| `echo` | yes | no | 30 of 609 | 0 of 30 | 0 of 30 | 30 of 30 | 0 of 30 | 0 of 30 | 0 of 26 / 0 of 26 | `Caruca only` |
| `uniq` | yes | yes | 30 of 609 | 0 of 30 | 2 of 30 | 24 of 30 | 0 of 30 | 0 of 30 | 0 of 30 / 0 of 30 | `Caruca splits more` |
| `awk` | yes | yes | 14 of 609 | 0 of 14 | 0 of 14 | 14 of 14 | 0 of 14 | 0 of 14 | 0 of 11 / 1 of 11 | `neither splits` |
| `export` | no | no | 13 of 609 | 0 of 13 | 0 of 13 | 0 of 13 | 0 of 13 | 0 of 13 | 0 of 13 / 0 of 13 | `neither splits` |
| `pure_func` | no | no | 12 of 609 | 0 of 12 | 0 of 12 | 0 of 12 | 0 of 12 | 0 of 12 | 0 of 12 / 0 of 12 | `neither splits` |
| `head` | yes | yes | 10 of 609 | 0 of 10 | 0 of 10 | 7 of 10 | 0 of 10 | 0 of 10 | 0 of 10 / 0 of 10 | `neither splits` |
| `wc` | yes | yes | 8 of 609 | 0 of 8 | 0 of 8 | 8 of 8 | 0 of 8 | 0 of 8 | 0 of 7 / 0 of 7 | `neither splits` |
| `comm` | yes | yes | 5 of 609 | 0 of 5 | 0 of 5 | 5 of 5 | 0 of 5 | 0 of 5 | 0 of 4 / 0 of 4 | `neither splits` |
| `samtools` | no | no | 5 of 609 | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 5 | 0 of 1 / 0 of 1 | `neither splits` |
| `[` | no | no | 4 of 609 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 4 | 0 of 3 / 0 of 3 | `neither splits` |
| `read` | yes | no | 4 of 609 | 0 of 4 | 0 of 4 | 4 of 4 | 0 of 4 | 0 of 4 | 0 of 3 / 0 of 3 | `Caruca only` |
| `join` | yes | no | 3 of 609 | 0 of 3 | 0 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | 0 of 1 / 0 of 1 | `Caruca only` |
| `rm` | yes | yes | 3 of 609 | 0 of 3 | 0 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | 0 of 3 / 0 of 3 | `neither splits` |
| `tail` | yes | yes | 3 of 609 | 0 of 3 | 0 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | 0 of 3 / 2 of 3 | `neither splits` |
| `[[` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 / 0 of 2 | `neither splits` |
| `cd` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 / 0 of 2 | `neither splits` |
| `dirname` | no | no | 2 of 609 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 | 0 of 2 / 0 of 2 | `neither splits` |
| `fmt` | yes | no | 2 of 609 | 0 of 2 | 0 of 2 | 2 of 2 | 0 of 2 | 0 of 2 | 2 of 2 / 0 of 2 | `Caruca only` |
| `mkfifo` | yes | yes | 2 of 609 | 0 of 2 | 0 of 2 | 2 of 2 | 0 of 2 | 0 of 2 | 0 of 2 / 0 of 2 | `neither splits` |
| `rev` | yes | no | 2 of 609 | 0 of 2 | 0 of 2 | 2 of 2 | 0 of 2 | 0 of 2 | 0 of 1 / 0 of 1 | `Caruca only` |
| `.` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `./crawl.sh` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `./index.sh` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `bigrams_aux` | no | yes | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `break` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `col` | yes | yes | 1 of 609 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `Caruca splits less` |
| `continue` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `diff` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `ffmpeg` | yes | no | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `Caruca only` |
| `find` | yes | no | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `Caruca only` |
| `gzip` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `mawk` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `mogrify` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `printf` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `python3` | no | no | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `seq` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |
| `xargs` | yes | yes | 1 of 609 | 0 of 1 | 0 of 1 | 1 of 1 | 0 of 1 | 0 of 1 | 0 of 1 / 0 of 1 | `neither splits` |

Compiler stops under Caruca only: `unixfun/34` (AssertionError; Daemon:  WARNING: Exception caught:; culprit: fmt), `unixfun/36` (AssertionError; Daemon:  WARNING: Exception caught:; culprit: fmt).

Compiler stops under PaSh's own only: `covid/5` (culprit: awk), `unixfun/12` (culprit: tail), `unixfun/16` (culprit: tail).

## 2. Totals by who has a file

| Group | Commands (in parts) | Uses in parts | Split (PaSh's own) | Split (Caruca) | Compiler stops (Caruca only / PaSh's own only) | Uses whose file raised (Caruca / PaSh's own) |
|---|---|---|---|---|---|---|
| Both have files | 18 of 44 | 484 of 609 | 126 of 484 | 158 of 484 | 0 of 177 / 3 of 177 | 0 of 484 / 0 of 484 |
| Only Caruca has a file | 7 of 44 | 43 of 609 | 0 of 43 | 0 of 43 | 2 of 177 / 0 of 177 | 0 of 43 / 0 of 43 |
| Only PaSh's own has a file | 1 of 44 | 1 of 609 | 0 of 1 | 0 of 1 | 0 of 177 / 0 of 177 | 0 of 1 / 0 of 1 |
| Neither has a file (reconciliation) | 18 of 44 | 81 of 609 | 0 of 81 | 0 of 81 | 0 of 177 / 0 of 177 | 0 of 81 / 0 of 81 |

Files (`manifest.json`): Caruca 53 commands, PaSh's own 30; both 20; Caruca only 33 (in parts: `echo`, `ffmpeg`, `find`, `fmt`, `join`, `read`, `rev`; outside parts only: `convert`, `iconv`, `ls`, `mktemp`, `paste`; not called by any script: 23); PaSh's own only 10.

## 3. Wrong output

Scripts whose printed output under this set differs from plain bash's (same repeat), and the commands PaSh split with this set but not with its own files there.

| Script | Runs differing from bash | Split with Caruca, not with PaSh's own |
|---|---|---|
| `oneliners/top-n` | 4 of 4 | `cat`, `sed` |
| `unixfun/17` | 4 of 4 | `cat`, `uniq` |
| `unixfun/23` | 4 of 4 | `cat` |
| `unixfun/26` | 4 of 4 | `cat`, `sed` |
| `unixfun/28` | 4 of 4 | `cat`, `sed` |
| `unixfun/29` | 4 of 4 | `cat`, `sed` |
| `unixfun/30` | 4 of 4 | `cat`, `sed` |
| `unixfun/31` | 4 of 4 | `cat`, `sed` |
| `unixfun/32` | 4 of 4 | `cat`, `sed` |
| `unixfun/33` | 4 of 4 | `cat`, `sed` |

## 4. Time where exactly one command's split differs

All of a source's files are swapped in at once, so a time difference belongs to the source. Of 86 scripts, 45 split the same under both sets, 13 differ on one command and 28 on more than one. Noise (second copy of PaSh's own ÷ PaSh's own): 0.83 to 1.46, median 1.00.

| Command | Scripts | Time ratio Caruca ÷ PaSh's own, geometric mean (min-max) | Above the noise band | Below it |
|---|---|---|---|---|
| `cat` | 13 of 86 | 1.13 (0.94-1.28) | 0 of 13 | 0 of 13 |
