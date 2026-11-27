# Checker's review of the full run (86 scripts, 2026-11-25)

I checked the full run's raw records (`full_run/`) and re-ran parts of it myself. My scripts were my own, and
I ran them from my own VM folder (`~/t024-check/full/` in the Lima VM `pash`). I read the builder's README last.
I did not edit any record, any file under `full_run/`, the VM's `~/t024/`, PaSh, its installed annotation package,
or Koala. The VM was idle (load 0.00) when I started, and no batch was running.

**Result: 10 of 11 checks pass.** The records hold up. I recomputed every number I was asked to check, from the
raw rows and with my own script, and every one came out the same. PaSh's logs agree with the recorded splits in
396 of 396 runs. The one failure is check 7, the README. Its most important flaw is that "every output was
right" covers only the text the scripts print. The files the scripts write were compared in fewer than half
of the timed runs that write files. For web-search, the written files differ even between two runs of plain bash.

## 1. The right files were loaded: PASS

My script (`check1_full.py`, adapted from my pilot `check1.py`) hashed every file in all 10 set folders. It compared
each file with PaSh's installed package (107 files) and with the source recorded for it. For the naive LLM, the
source is the `"repeat": 1` row of the Fig. 7 ledger; for `naive-sed2`'s `sed`, it is the `"repeat": 2` row. For
Caruca, the sources are the `v1-pash` and `v1-main` rows of `sides.jsonl`.

| Set | Files replaced, matching their source | All other files |
|---|---|---|
| `pash-own`, `pash-own-copy` | none replaced | 107 of 107 equal PaSh's package |
| `naive` | 246 of 246 (82 commands × 3) | equal PaSh's package, except the name table |
| `naive-sed2` | 246 of 246; `sed` matches the ledger's repeat-2 run | same |
| `caruca-pash`, `caruca-main` | 24 of 24 (8 commands × 3; main grammar for `cut`, `rm`, `sort` in `caruca-main`) | same |
| 4 control sets | 243 of 243 | same; in `naive-no-sort`, `sort` has no files at all, as intended |

The name table (`AnnotationGeneration.py`) only gains lines. No line is removed. The naive sets add 62 lines and
the Caruca sets add 2. All 294 source files named in `manifest.json` still have the hashes it records.

**One gap.** The runner rebuilds the set folders each time it starts. The current folders were built at 13:54 on
11-24. The main runs of the first 46 scripts (oneliners and unixfun) took place from 13:10 to 13:50, on an
earlier build, and nothing records that build's contents. Two facts make an identical build very likely:

- all 294 source files were last changed before 13:10 (the newest at 12:01);
- the naive `awk` file, added that morning, was in use at 13:4x, because `awk` was split in `unixfun/14`.

Even so, no record shows it.

## 2. PaSh really used the folder it was given: PASS

I ran `unixfun/14` under every set myself, with Koala's own script and input. I added one control of my own,
`ctl-naive-no-awk`: a copy of `naive` in which `awk`'s split rules are turned off (`generate_info` returns at once).

| Set (my runs) | Parts sent / compiled to parallel | Side-by-side copies in PaSh's script | Output |
|---|---|---|---|
| `pash-own`, `pash-own-copy` | 1 / 1 | cut 8 | Koala's hash |
| `naive`, `naive-sed2` | 1 / 1 | awk 8, cat 8, cut 8 | Koala's hash |
| `caruca-pash` | 1 / 0 (compiler crash) | none | Koala's hash |
| `caruca-main` | 1 / 1 | cat 8, cut 8 | Koala's hash |
| **my control `ctl-naive-no-awk`** | 1 / 1 | **cat 8, cut 8 (awk gone)** | Koala's hash |

Turning off `awk`'s rules removed `awk`'s 8 copies and changed nothing else, so PaSh reads the folder it is
given. (`sort` does not appear in the copy column because PaSh does not start its copies through its wrapper.
The records show 15 `sort` starts under `pash-own` and `naive`.) These runs match the records for `unixfun/14`.

## 3. The splitting claims hold: PASS

The README says the logs are under `~/t024/runs/<group>_<script>/`. They are not there: those folders hold only
bash's answer files. The full logs are in `~/t024/out/logs/` (888 files). I read the log of every run made with
the stand-in programs, 396 in all (86 scripts × 4 sources, plus 52 with the second sed file). For each one I
counted what PaSh received, what it compiled, and the copies in the script it wrote.

- **Parts sent:** the same as the record in 396 of 396 runs.
- **Parts compiled to parallel:** the same in 396 of 396.
- **Commands split** (2 or more copies): exactly the recorded `split_commands` in 396 of 396.
- **Start counts:** every recorded split command (481 of 481) has more program starts than under plain bash.

## 4. The output claims hold: PASS (for printed output)

- **Recomputed from the records.** I compared each run's output hash with the plain-bash run of the same script,
  pass and repeat. Every source matches bash in every timed repeat: 86 of 86 scripts, and 52 of 52 for the second
  sed file. Koala's stored answer matches in 46 of 46 scripts, for bash and for every source.
- **Recomputed by re-running.** I ran `oneliners/wf`, `unixfun/12`, `covid/1` (5 sources each) and `unixfun/14`
  (8 sources). All 23 PaSh outputs equal plain bash. All 20 of those 23 that are in the records equal the recorded
  hash, in both passes. `wf`, `12` and `14` equal Koala's stored hash.
- **Limit: files the scripts write.** 32 scripts write files as well as printing. The records give the result
  of comparing those files with bash's as follows:

  | File check in the timed runs | Rows |
  |---|---|
  | same as bash | 211 |
  | not checked (the source ran before bash in its repeat, so there was nothing to compare with) | 352 |
  | different from bash | 25 |

  The 25 "different" rows are web-search (19) and bio (6). For bio, the main repeat records bash's own run as
  different from bash, so that check itself was broken. For web-search, the two redone runs kept the files'
  hashes. The two plain-bash runs differ from each other (`b691bd…` against `ce3f38…`), and so do all six
  sources. So web-search's written files change from run to run, and this check cannot judge them. Section 1
  of `numbers.md` counts printed output only, and I confirm it on that basis.

## 5. The annotation answers are real: PASS

I wrote my own caller (`ans.py`). It loads each set's files in a fresh Python process, parses each recorded
command line, and runs both generators. It then sorts the answer into the runner's categories: no files, no
answer, says no split, allows only a split PaSh has not implemented, allows a split, or raised an error. I
checked all 9,395 rows in `full_run/answers/`.

- **Direct answers (quotes removed):** 6,386 of 6,386 agree.
- **"As PaSh passes them":** 3,001 of 3,009 agree. The 8 others are all the naive `head` file on `head -n N`, in
  6 unixfun scripts. The worker recorded "says no split". I got "only a split PaSh has not implemented".

The naive `head` file reads the `-n` value through attribute names. These names find the value when the
command line is parsed from text, but not, it seems, in the object PaSh passes. The worker replayed PaSh's own
objects; I parsed text, so its answer is the more faithful one. In both versions `head` is not split, which
agrees with PaSh's logs. The `wc` and `join` errors also reproduce:

- naive `wc`: 8 uses raise an error, in 7 scripts;
- naive `join`: raises in `weather/tuft-weather`.

## 6. Timings are honest: PASS

- **Repeats:** each of the 568 pairs of script and source has exactly 3 timed rows (repeats 1, 2 and 3), as the
  README says.
- **Sleeps:** the Mac's power log (`pmset -g log`) shows sleeps at 13:47, 15:26 (with re-sleeps at 15:47 and
  15:52), 17:26 and 08:21 inside the run's 13:10-to-12:52 span. These are the same sleeps as `sleep_events.jsonl`,
  and none is missing. Check 9 shows that no kept timed row overlaps one.
- **Medians and ratios:** recomputed exactly (check 10).
- **Not mentioned anywhere: a 61-second lid-closed "dark wake"** from 10:43:25 to 10:44:26 on 11-25, during
  web-search's redone repeat 1. The power log does not count it as sleep: the Mac was on mains power and
  `caffeinate` was holding off sleep. That repeat's times look normal (651 to 710 seconds).

## 7. The README says only what the records support: FAIL

The counts and tables in the README match `numbers.md`, and both match my recount. Rates come with their
denominators. These statements need fixing:

1. **"Every output was right … the output matched plain bash."** This is true of the printed output only. Of
   the timed runs of the 32 scripts that also write files, 211 of 588 checked those files as the same as bash's.
   352 had nothing to compare with, and 25 differ. Web-search's files differ even between two runs of plain bash
   (check 4). The README says the file check is missing only for "repeat 2 of the slow groups". In fact it is
   also missing for every repeat-3 run that came before bash.
2. **"`wc` on `wc -l` (8 scripts)."** The records show 8 uses in 7 scripts (6 unixfun scripts and web-search).
3. **"That is where the 12 lost parts go"** (Caruca's PaSh-grammar files, compiler failures). In 10 of the 12 parts
   the compiler crashed. The other 2 are recorded as "other".
4. **The naive LLM's 2 gained parts** (`unixfun/12` and `unixfun/16`) are both parts where PaSh's own files
   crash PaSh's compiler (an `AssertionError` in `pipe_append`, which I saw in the log for `unixfun/12`). The
   gains for `tr` in item 4 and for `cat` in those scripts come from the naive files avoiding that crash. The
   README does not say so.
5. **Power: "All other timed runs were on mains power (17:31 to 08:21, with one 10-second switch at 22:03)."**
   The main runs from 13:10 to 17:31 are left out of that statement. The power log shows battery in that span at:
   - 13:46:57–13:50:16 (`unixfun/34`, `unixfun/35`);
   - 15:25:35–15:26:01, the last 26 seconds of `nlp/trigram_rec`;
   - 16:23:57–16:24:01 (`nlp/vowel_sequencies_gr_1K`);
   - 16:36:22–16:36:28 (`nlp/merge_upper`).

   The redone runs "on mains power (10:12 to 12:52, no sleep)" also had battery from 10:15:03 to 10:15:27, and
   the 61-second dark wake (check 6). These stretches are short, and none of the times affected looks unusual.
   Even so, the statement as written is wrong.
6. **`numbers.md` says "the naive LLM's second sed file was run only on scripts that use sed."** For 27 of its 52
   scripts, plain bash started no `sed` at all. The README's own description is the correct one: the 12
   oneliners and unixfun scripts that use `sed`, plus all 40 scripts of the other groups. Because of that, the
   second sed file's time ratios cover a different set of scripts from the other sources' 86. The table shows
   the script count, but the README does not warn that the rows cannot be compared directly.
7. **Minor:** a comment in `summarise.py` says bash's reference time comes from the main phase only. The code
   (rightly, and as the README says) takes the median of all 3 repeats.

## 8. The two recorder fix-ups: PASS

I counted from the raw rows with my own code.

**Fix-up 1 (compare with the same repeat's bash).**

- Each of the 1,854 rows that are not bash has a bash run of the same script, phase, pass and repeat.
- 482 rows are recorded "not same as bash". All 482 ran before bash in their repeat, and all 482 have the same
  output hash as that bash run. So 482 rows change from "not same" to "same", and no other row changes.
- No row whose bash ran first is recorded "not same".
- The output-file flag changes on 642 rows:
  - 290 from "different" to "same", by hash or because neither run wrote a file;
  - 197 from "different" to "not checked";
  - 155 from "same" to "not checked". These ran before bash, so their recorded "same" had no valid reference
    to compare with.

**Fix-up 2 (web-search without `node`, and the redone runs).**

- Exactly 7 rows contain "node … No such file". All 7 are web-search's timed repeat-1 rows from the main phase,
  bash included.
- The redone phases add 7 rows for repeat 1 and 7 for repeat 3. The 7 earlier repeat-3 rows (on battery, with
  the sleep) are the only other rows that a redone row replaces.
- So the count goes from 2,224 rows to 2,210. The 14 rows dropped are exactly those described, and nothing
  else is dropped.
- No (script, source, pass, phase, repeat) appears twice.

## 9. Mac sleeps against timed rows: PASS (none left in)

I compared every window in `run_windows.jsonl` with every sleep in `sleep_events.jsonl`, and with the power log.

- **`nlp/uppercase_by_type` and `nlp/sort_words_by_rhyming`** (hit at 15:26–16:00 and 17:26–17:31). Their main
  rows are the reruns from 23:08 to 23:30. There is one row per source, and the seconds match the VM's
  `batch_rerun.log` (for example, bash 28.553 s). The original rows and windows are gone from the records,
  replaced in place, and are now described only in `sleep_events.jsonl`.
- **web-search, repeats phase** (06:58:03–09:58:18, the window holding the 08:21:36–08:27:50 sleep). Repeat 3
  is left out and replaced by the redone repeat 3.
  - Repeat 2 ran first in that window. Adding up its seven run times places its end at about 08:21, just before
    the sleep. The whole window adds up too: repeat 2's 4,966 s, the 374 s of sleep and repeat 3's 5,457 s,
    plus a few seconds between runs, end at 09:58.
  - Repeat 2's plain-bash time, 638 s, is in line with the redone runs (640 s and 662 s).
  - So no repeat-2 row overlaps the sleep. Its last seconds may have fallen inside the battery switch at 08:21:33.
- **The 13:47 sleep** fell between `unixfun/34` and `unixfun/35`, and no run overlaps it.

No timed row that overlaps a sleep is left in.

## 10. Headline numbers recomputed independently: PASS (0 cells differ)

My own script (`recount.py`, written without `summarise.py`'s code) applied the two fix-ups as described and
recomputed:

- **Section 1, all 6 sources:** script counts, same as bash, same as Koala's answer, and the split, fell-back
  and other states. The state is also the same in all 3 repeats of every script.
- **Section 3:** both in parallel, gained, lost and neither, for 4 sources. The count of distinct parts in
  parallel also agrees between `regions.jsonl.gz` and the results rows.
- **Section 5:** all 19 command rows.
- **Section 6:** speed-up, time against PaSh's own, the faster and slower counts, and the noise band
  (0.83–1.13, median 0.99, 4 of 86).
- **The per-script table:** all 86 × 7 cells.

Every cell is the same. I also confirmed the README's counts of scripts where PaSh was more than 10% faster
than bash: 10, 6, 5 and 1 of 86. With any files, PaSh was slower than bash in 74 to 83 of 86 scripts.

## 11. Spot-check of five split claims in PaSh's logs: PASS

I counted copies in the parallel script PaSh wrote (`~/t024/out/logs/…__instrumented.log.gz`):

| Claim | PaSh's own | This source |
|---|---|---|
| naive splits `cat` in `oneliners/wf` | cat 0 copies | **naive: 8** |
| naive splits `awk` in `unixfun/14` | awk 1 line, not split | **naive: 8** |
| naive loses `sed` in `covid/1` | sed 8 copies | **naive: 1 line** |
| Caruca's main grammar never splits a plain `sort` (`oneliners/sort`) | sort 15 lines (8 copies + 7 merges) | **caruca-main: 1 line** |
| Caruca's PaSh grammar loses `cut` in `covid/1` | cut 16 copies (2 uses × 8) | **caruca-pash: compiler crash, 0 copies** |
| (extra) naive gains `tr` in `unixfun/12` | PaSh's own: compiler crash | **naive: tr 8 copies** |

All six agree with the records and with `numbers.md` section 5.

## What I left behind

In the VM under `~/t024-check/full/`:

- my scripts: `check1_full.py`, `ans.py`, `ans_drive.py`, `logall.py`;
- my control set: `sets/ctl-naive-no-awk`;
- my re-runs: `runs/` (`unixfun/14`) and `runs2/` (`wf`, `12`, `covid/1`).

Copies of my Mac-side scripts are there too: `recount.py`, which runs on the Mac against `full_run/`;
`logcount.py`; `rerun.sh` and `rerun2.sh`, which re-run the scripts; and `power.txt`, the power-source changes
taken from `pmset -g log`.
