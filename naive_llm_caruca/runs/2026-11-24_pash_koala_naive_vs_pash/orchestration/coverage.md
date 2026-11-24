# PaSh's published benchmark suite in Koala: what is there, who covers it, what it costs

Written 2026-11-24 from a read-only look at the Koala checkout in the `pash` VM (commit `ccf25a57`) and
the published suite's scripts in `~/pash/evaluation/benchmarks/`. Nothing was downloaded or run. File
sizes come from asking the Koala server for each file's size without fetching it. The per-script details
are in `coverage.jsonl` next to this file (one line per script).

## Short answer

- **All 12 published benchmark sets have a successor in Koala, spread over 10 Koala groups.** Those groups
  run 92 scripts in all. 82 of them are versions of a published script; the other 10 are new in Koala.
  Most of the published scripts made it across nearly unchanged: 37 of the 82 are identical apart from how
  the input file is passed in, and another 34 make only small edits.
- **The naive LLM's annotation files fully cover only 17 of the 92 scripts.** The main reason is three
  commands the LLM never wrote files for, because they were not among the 79 commands in the paper's
  figure 7: `tr`, which 54 of the 92 scripts use, `xargs` (24 scripts) and `awk` (18 scripts). PaSh's own
  files cover all three. Caruca's eight files fully cover 6 of the 92 scripts.
- **Six groups are ready to run now. Of the four not yet downloaded, three can run in the VM in part, and
  the genomics group's new part cannot run there at all.** That part needs about 15 GB of downloads, about
  33 GB of memory and programs built only for Intel processors. The VM has 17 GB of free disk and 8 GiB of
  memory, and its processor is ARM (aarch64).

"Covers a command" here means the source has an annotation file under that command's name. It says
nothing about whether the file is right, or whether PaSh will actually use it on a given line.

## 1. Which Koala group holds each published benchmark set

"Published scripts run" counts the scripts the 2022 suite's own runner (`run_all.sh`) actually executed.
"Koala scripts" counts the scripts Koala's runner for that group executes.

| Published set (OSDI'22 Table 1) | Koala group | Published scripts run | Koala scripts | How close |
|---|---|---|---|---|
| Classics (one-liners) | `oneliners` | 10 | 12 | 9 kept: 5 unchanged, 4 lightly edited (an empty-line filter added; `spell` swaps `iconv` for `sed`). `shortest-scripts` dropped. 3 new: `comm`, `uniq-ips`, `opt-parallel` |
| Unix50 | `unixfun` | 36 (2 of them, 22 and 27, contain no command) | 34 | All 34 unchanged except for input wiring; Koala drops the two empty ones |
| COVID-mts | `covid` | 4 (the 5th was marked "not working yet") | 5 | All 5 use the same commands; small option spellings changed (for example `sort -k1n` became `sort -k 1 -n`) |
| NLP | `nlp` | 21 (2 commented out) | 23 | Renamed (for example `6_4.sh` became `syllable_words_1.sh`). 4 unchanged, 19 lightly edited (mostly an added empty-line filter, some words handled per book). Koala runs the 2 the published suite skipped |
| AvgTemp | `weather` | 1 | 2 | `temp-analytics.sh` has the same analysis with its download step removed. `tuft-weather.sh` is new |
| WebIndex | `web-search` | 1 | 1 | Rewritten: a crawl-then-index loop with Node.js helper programs |
| MediaConv | `file-mod` | 2 | 2 (+1 new) | Same tools and settings (`convert`, `ffmpeg`); they now read standard input. `thumbnail_generation.sh` is new |
| ProgInf | `pkg` | 1 | 1 | Same analysis program (`mir-sa`); the package list now comes from an index file |
| LogAnalysis | `analytics` | 2 | 2 (+2 new) | `nginx` and `pcaps` keep the same pipelines (`pcaps` adds one query). `port-scan` and `ray-tracing` are new |
| Genomics | `bio` | 1 | 1 (+3 new) | `bio.sh` keeps the same `samtools` steps. Three TERA-Seq scripts are new |
| AurPkg | `pkg` | 1 | 1 | Same idea (fetch a package build file, build it with `makedeb`); fetches from Koala's server and also fetches signing keys |
| FileEnc | `file-mod` | 2 | 2 | `encrypt_files` keeps `openssl` with the same settings. `compress_files` is rewritten: `gzip` instead of `zip` |

Totals: 82 published scripts were run (80 that contain commands). Koala's ten groups run 92 scripts, 82 of
them with a published original.

## 2. Commands per script, and who has files for them

I listed commands by parsing every script with the shell parser bundled with PaSh, then checked the
output by hand. The lists include commands called inside helper scripts that a script runs or loads
(`bi-gram.aux.sh`, the `web-search` helpers, `bio`'s settings file), and commands that `xargs` or
`runuser` start. Shell built-ins (`echo`, `cd`, `read`, `[`, and the like) are left out. So are functions
a script defines for itself, with one exception: `bigrams_aux` stays in, because PaSh's own list has an
entry under that name. Bookkeeping commands such as `mkdir`, `ls` and `basename` are counted too.

Annotation sources: the naive LLM (79 commands, one per command, taken from the first run of each),
Caruca (`cat cp cut grep rm sort split wc`), and PaSh's own (the 30 names its annotation package looks
up).

| Koala group | Scripts | Distinct commands | Naive LLM has | Caruca has | PaSh's own has | Scripts fully covered by naive LLM | Scripts fully covered by naive LLM and PaSh's own together | Commands nobody covers |
|---|---|---|---|---|---|---|---|---|
| `unixfun` | 34 | 12 | 10 | 5 | 11 | 12 of 34 | 34 of 34 | none |
| `oneliners` | 12 | 20 | 14 | 5 | 16 | 3 of 12 | 10 of 12 | `paste`, `find`, `mawk` |
| `covid` | 5 | 6 | 5 | 3 | 6 | 0 of 5 | 5 of 5 | none |
| `nlp` | 23 | 17 | 12 | 4 | 11 | 0 of 23 | 0 of 23 | `basename` (all 23), `paste` |
| `weather` | 2 | 16 | 12 | 5 | 12 | 0 of 2 | 1 of 2 | `git`, `python3` |
| `web-search` | 1 | 18 | 13 | 6 | 13 | 0 of 1 | 0 of 1 | `node`, `paste`, `dirname` |
| `file-mod` | 5 | 8 | 4 | 1 | 1 | 1 of 5 | 1 of 5 | `gzip`, `openssl`, `ffmpeg`, `basename` |
| `pkg` | 2 | 13 | 5 | 1 | 3 | 0 of 2 | 0 of 2 | `makedeb`, `mir-sa`, `curl`, `gpg`, `runuser`, `dirname`, `realpath` |
| `analytics` | 4 | 19 | 12 | 5 | 11 | 1 of 4 | 1 of 4 | `tcpdump`, `egrep`, `jq`, `zannotate`, `basename` |
| `bio` | 4 | 51 | 14 | 6 | 12 | 0 of 4 | 0 of 4 | 35, mostly genomics programs (`samtools`, `minimap2`, `STAR`, …) |
| **All** | **92** | **86** | **31** | **6** | **21** | **17 of 92** | **52 of 92** | **51 of 86 commands** |

What stands out:

- **The naive LLM lacks `tr`, `xargs` and `awk`.** These are the most-used commands it has no file for:
  `tr` appears in 54 of the 92 scripts, `xargs` in 24 and `awk` in 18. For 35 of the 92 scripts, these
  three (plus the `bigrams_aux` function) are the only commands the LLM is missing. Adding them to its
  set would raise its full-coverage count from 17 toward 52.
- **Where the two overlap, PaSh's own and the naive LLM share 17 commands.** Those are the ones on which
  a file-for-file comparison is possible: `cat col comm cut diff grep head mkfifo mv rm sed seq sort tail
  tee uniq wc`. The naive LLM alone has 14 commands that appear here (`convert`, `mogrify`, `fmt`, `join`,
  `pr`, `rev`, `iconv`, `ls`, `mkdir`, `mktemp`, `ln`, `touch`, `chown`, `uname`). PaSh's own alone has
  4 (`tr`, `xargs`, `awk`, `bigrams_aux`).
- **Caruca's eight files cover 6 commands used here** (`cat cut grep rm sort wc`), but those six are the
  core of most text pipelines: 87 of the 92 scripts use `cat`, and `sort`, `grep` and `cut` each appear in
  40 or more.
- **Nobody covers `basename` (29 scripts) or `paste` (9 scripts).** In `nlp`, `basename` runs only in the
  loop that picks the input books, so the gap there matters little. `paste` does sit inside the bigram
  pipelines.

## 3. What it would take to run the four groups not yet downloaded

The VM has 8 CPUs, 8 GiB of memory and 17 GB of free disk. Its processor is ARM (aarch64), and the
installers can use `sudo`. Koala's "min" size is a few test files; "small" is the size used for earlier
runs. Download sizes are what Koala's fetch script asks for at that size.

| Group | Download at min | Download at small | What the installer needs | Can the VM run it? |
|---|---|---|---|---|
| `analytics` | about 80 MB (a routing table for `port-scan`; the other inputs ship with Koala) | about 730 MB (pcap captures 552 MB, port-scan logs 78 MB, routing table 79 MB, ray-tracing logs 12 MB, web logs 9 MB) | `tcpdump` and `jq` (both already in the VM). `port-scan` also needs `zannotate`, which the installer builds with a Go toolchain downloaded **for Intel processors** and then fetches from the internet | `nginx`, `pcaps`, `ray-tracing`: yes. `port-scan`: not until Go and `zannotate` are installed for ARM by hand |
| `file-mod` | about 17 MB (audio files; images and captures ship with Koala) | about 1.3 GB (images 773 MB, captures 552 MB, audio 17 MB; the audio is copied 10 times after unpacking) | Builds ImageMagick 6.9.11, libjpeg, libpng and FFmpeg 5.1.9 from source with `sudo`. Nothing in it is Intel-only | Yes. The source builds are the slow part |
| `pkg` | about 540 MB at **every** size (npm packages 532 MB plus the analysis tool 9 MB) | the same 540 MB; at small, 100 npm packages and 10 Linux packages are used | A long list of system packages (including Qt and a Java kit) plus `makedeb` from an outside package server. `pacaur` downloads package recipes, signing keys and source code **while it runs**, and compiles them | `proginf`: probably (Node.js for ARM is already in Koala's tools folder). `pacaur`: technically possible, but its time is spent on network and compiling, and it has no pipeline PaSh could split |
| `bio` | none (a 1 MB synthetic file ships with Koala); only `bio.sh` runs at this size | about 3.6 GB of BAM files for `bio.sh`, **plus** the fetch script then fetches the TERA-Seq data at full size whatever size you ask for: 13.2 GB of sequencing reads and 1.7 GB of human and mouse genomes, before the smaller reference files | `samtools` and `minimap2` built from source (fine on ARM). TERA-Seq also needs R, Perl and Java tool stacks, plus `STAR`, `seqkit` and `liftOver`, which the installer downloads **as Intel-only binaries** | `bio.sh` at min: yes. Small: no. The fetch alone (over 18 GB) exceeds the free disk, the script that builds the reference data (`data.sh`) needs about 33 GB of memory for `STAR` (its own comment says so), and three of the tools will not run on ARM |

Two notes on the six downloaded groups, from reading the scripts: `weather`'s `tuft-weather.sh` calls
`python3` for a plotting script that needs matplotlib, and the VM's system Python does not have it (PaSh's
own Python does, so it depends on which `python3` is found first). `web-search` uses the ARM Node.js in
Koala's tools folder, which is present.

## 4. Proposed order

1. **`unixfun` (34 scripts).** Its scripts are identical to the published ones, and PaSh's own and the
   naive LLM's files together cover every command in it. 12 scripts can run on the naive LLM's files
   alone, which gives the cleanest three-way comparison.
2. **`oneliners` (12).** The classic set, already downloaded. 10 of 12 have no gap. It is also where
   `bigrams_aux`, a PaSh-only entry, shows up.
3. **`covid` (5).** Same scripts as published, no gaps. Every script needs `awk` from PaSh's own files.
4. **`nlp` (23).** The largest text set. The only commands nobody covers (`basename`, and `paste` in the
   bigram scripts) sit outside or beside the main pipelines.
5. **`weather`, then `web-search` (3).** Already downloaded. Run `temp-analytics.sh` first, which is the
   published AvgTemp script. Check `tuft-weather.sh`'s Python first. `web-search` is a single long loop,
   so expect long runs that tell you little per script.
6. **`analytics` at small, minus `port-scan` (3 scripts).** A download of about 730 MB, and no new
   installs. Text pipelines over web logs and captures, so PaSh has something to split.
7. **`file-mod` at min, then at small (5).** Cheap to download but slow to install. Useful mainly for the
   naive LLM's `convert` and `mogrify` files, which PaSh's own set does not have. The other commands
   (`gzip`, `openssl`, `ffmpeg`) have no file from anyone, so for those PaSh will just run the script as
   is.
8. **`bio.sh` at min only (1).** Keeps the Genomics row represented. Only `cut`, `sort`, `uniq` and `sed`
   in it have files from anyone.

Leave out, and why:

- **`bio`'s three TERA-Seq scripts.** Not in the published suite, and they cannot run in this VM (disk,
  memory and Intel-only tools, as described above).
- **`bio.sh` at small.** Only because Koala's fetch script ties it to the TERA-Seq download. Running it
  would mean fetching the 15 BAM files some other way.
- **`pkg` (`pacaur` and `proginf`).** Neither script has a command that any of the three sources could let
  PaSh split, so all three would produce the same result as plain bash. `pacaur` also depends on outside
  servers while it runs. Run each once at min, if at all, to show that the AurPkg and ProgInf rows were
  attempted.
- **`analytics/port-scan`.** It needs `zannotate` installed for ARM, and it is not in the published suite.
