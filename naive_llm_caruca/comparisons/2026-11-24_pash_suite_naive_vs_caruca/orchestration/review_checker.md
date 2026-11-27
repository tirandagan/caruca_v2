# Checker's review of the `spell.sh` pilot (2026-11-24)

I checked the raw records and re-ran things myself, using my own scripts in my own VM folder
(`~/t024-check/` in the Lima VM `pash`). I read the worker's README last. I did not edit any of the worker's files,
PaSh, the installed annotation package, or Koala. The VM was idle (load 0.00) when I started.

**Result: 5 of 7 checks pass.** The data are sound. All outputs are correct, the split counts are right, and the
right files were loaded. The two failures are in how the work was reported. Timing was repeated 3 times, not the 5
the brief asked for. The README has some unsupported or incomplete statements. The most important finding is a
fault in the method, not in the data. When the worker asks a command's annotation files directly, the files see a
quoted word without its quotes. Inside PaSh, the same files see the word with its quotes. So 2 of the script's
9 command lines get different answers in the two settings, and this explains both of the pilot's "unexplained"
results.

## 1. The right files were loaded: PASS

My script (`~/t024-check/check1.py`) hashed every file in every set folder. It compared each folder against:

- PaSh's installed package (107 files);
- the naive LLM's files, taken from the folder named in the `"repeat": 1` row of the Fig. 7 ledger. Each of the
  79 commands has exactly one such row;
- Caruca's files, taken from the `v1-pash` and `v1-main` rows of the task-021 `sides.jsonl`.

| Set | Files | Replaced files that match their source | Other files that match PaSh's package |
|---|---|---|---|
| `pash-own` | 107 | none replaced | 107 of 107 |
| `naive` | 304 | 237 of 237 (79 commands × 3) | all, except the name table |
| `caruca-pash` | 116 | 24 of 24 (8 commands × 3) | all, except the name table |
| `caruca-main` | 116 | 24 of 24 (main grammar for `cut`, `rm`, `sort`; the small PaSh grammar for the other 5, as Amendment 1 says) | all, except the name table |
| the 4 control sets | 301–304 | all match | all, except the name table and the command deliberately removed |

The only file that differs from PaSh's package in each set is the name table (`AnnotationGeneration.py`).
`diff` shows that it only adds lines: 2 names (`split`, `cp`) in the Caruca sets, and 62 names in the naive
sets. No line is removed or changed. No set contains a file that is neither PaSh's nor from a recorded source.

In `naive-no-sort`, `sort` has **no files at all**, not PaSh's own files. It is still listed in the name table.
The README says this correctly ("`sort`'s three files deleted").

## 2. PaSh really used the folder it was given: PASS

I re-ran `spell.sh` once with each of the four sets. I used my own start-counting wrappers, not the worker's
stand-in. I also made one control of my own, `ctl-no-tr`: a copy of `pash-own` in which `tr`'s split rules are
turned off (its `generate_info` returns at once).

| Set (my runs) | Regions sent / run in parallel | Starts: cat, sed, col, tr, sort |
|---|---|---|
| bash | – | 1, 1, 1, 3, 1 |
| `pash-own` | 1 / 1 | 1, 30, 30, 57, 15 |
| `naive` | 1 / 1 | 30, 1, 1, 57, 15 |
| `caruca-pash` | 1 / 1 | 30, 30, 30, 57, 1 |
| `caruca-main` | 1 / 1 | 30, 30, 30, 57, 1 |
| **my control `ctl-no-tr`** | 1 / 1 | 1, 30, 30, **3**, 15 |

Turning off `tr`'s rules took `tr` from 57 starts down to 3, the same as plain bash. Nothing else changed. So PaSh
reads the folder it is given.

The start counts leave out PaSh's own housekeeping calls, using the worker's rule. The `sort` count of 15 includes
PaSh's merge steps. Without the rule, `sort` has 8 starts under each set that splits it.

## 3. The splitting claims hold: PASS

- Reading the worker's 16 saved PaSh logs myself gives 1 region sent and 1 run in parallel for every set. The one
  exception is `naive-no-sort`: 1 sent, 0 run in parallel, and 1 exception, "InputOutputInformation for sort not
  provided so considered side-effectful".
- The parallel scripts PaSh wrote run these numbers of side-by-side copies:
  - `pash-own`: 8 each of sed and col, 8 + 8 + 1 of tr;
  - `naive`: 8 of cat, 8 + 8 + 1 of tr;
  - both Caruca sets: 8 each of cat, sed and col, 8 + 8 + 1 of tr;
  - `sort`: 8 copies plus the merge steps under `pash-own` and `naive`, and 1 copy under the Caruca sets.
- These match `results.jsonl`, `controls.jsonl` and my own re-runs (check 2). The table "Commands PaSh split" in
  the README is right for all 5 sets and all 5 controls.

## 4. The output claims hold: PASS (by re-running)

The worker's PaSh output files were not kept in the VM; only `answers_bash.out` is left. So I recomputed the
outputs by re-running:

- I ran each of the 4 main sets 3 times and the control once. All **13 of 13** PaSh outputs, and plain bash, have
  the hash `83a9657314b5…`. That equals Koala's stored hash (`hashes/small/spell.hash`).
- In the worker's records, 30 of 30 rows in `results.jsonl` and 12 of 12 in `controls.jsonl` have exit code 0,
  the same output as bash, the same output as Koala's hash, and no tracebacks.
- The script PaSh ran (`~/t024/shadow/oneliners/scripts/spell.sh`) is identical to Koala's. The input it reads
  goes through a link to Koala's `30M.txt`, and the two files have the same hash.

## 5. The annotation answers are real: PASS, with an important limit

I wrote my own caller, `~/t024-check/check5.py`. It loads each set's package and asks its two generators about
each of the 9 command lines. In the 4 main sets my answers match `answers.jsonl` on **36 of 36** lines: the same
split recipes, the same "no class" cases, and no exceptions. I did not re-check the 4 control sets this way.

**The limit, which I established myself.** Asking the files directly is not the same as PaSh asking them. PaSh
gives the files a quoted word with its quotes still on. I showed this with two copies of sets in my own folder,
each with one line added that writes down what the file is given. In both, PaSh's output was still correct.

- The naive `sed` file, inside PaSh, was given the sed script `"s/[^[:print:]]//g"`, *with the double quotes*.
  Its checker reads the opening `"` as an unknown sed command, so it allows no split. Asked directly, the file is
  given the script without quotes and allows a split. **This is the reason the README calls "not established".**
- PaSh's own `tr` file, inside PaSh, was given `"\n"` for `tr -cs A-Za-z '\n'`. It treats that as squeezing
  newlines, and has no split for that case. Asked directly, it allows a split. **This is why only 2 of the 3
  `tr` commands split under every set.** The README reports the 2 of 3 but does not say why.

So the direct answers differ from what PaSh does on 2 of the 9 command lines. One is the naive file for `sed`; the
other is PaSh's own file for `tr -cs`, which is in every set. The answers in `answers.jsonl` are real, but they are
not what PaSh gets. To fix the method for the full suite, pass each operand to the files the way PaSh does (keep
the quotes), or record what the files are given inside PaSh, as I did.

## 6. Timings are honest: FAIL (3 repeats, not 5)

- **Sleep: none.** The Mac's power log shows the last wake at 10:18:07 and no sleep after it. The timed runs took
  place from 10:59:38 to 11:00:08, and the controls from 10:59:29 and 11:01:04 to 11:01:16 (`run_windows.jsonl`).
- **Medians recompute correctly** from the `plain` rows. Examples: `pash-own` 0.598 / 0.610 / 0.622 seconds gives
  a median of 0.61; bash's median is 1.028; 1.028 / 0.61 = 1.69 times faster. The other ratios and ranges match.
  My own re-runs had similar times (bash 1.08 s; `pash-own` 0.66–0.91 s; `naive` 0.90–0.98 s; Caruca sets
  1.11–1.17 s), but they were not done under timing conditions.
- **Failed:** the brief asks for each timed run to be repeated **5 times**. Each set was run **3 times**. The
  README says "median of 3" honestly but does not say that this goes against the brief.
- **Not supported:** the README says the Mac was "on mains power for the whole window". The power log's last
  entry before the window reads "Using BATT (Charge:71%)" at 10:18, and the log has no entry showing the power
  source changing after that. The battery is charged and on AC power now, so the Mac was probably plugged in.
  The log does not show it.

## 7. The README says only what the records support: FAIL

What is right: the main table, the output claims, the region counts (1 of 1), the control table's split
columns, the file list, and the honest "median of 3". Each rate has its denominator, and the terms are explained.

What needs fixing:

1. **`sed`, "Why is not established":** it is established now (check 5). PaSh gives the file the script with its
   double quotes, and the naive checker rejects the quote character.
2. **The `tr` result (2 of 3) is not explained.** The README also says the direct answers failed to predict
   PaSh's behaviour only for the naive `sed` file. They also failed for PaSh's own `tr -cs` file, in every set.
3. **"Each change of one command's files changed exactly that command"** is wrong for `naive-no-sort`. Removing
   `sort` stopped every command from splitting, because PaSh then ran the whole script as plain bash.
4. **"Splitting `sort` is what pays"** says which command caused the time difference, but no run tested that. The
   README itself says a time difference "belongs to the set as a whole". The only run that changes `sort` alone
   (`naive-no-sort`) turns off PaSh for the whole script. Say "the two faster sets are the two that split
   `sort`" instead.
5. **"Caruca's `sort` file … has a branch only for `sort -m`"** is true of the small PaSh grammar file. The
   main-grammar file used by `caruca-main` has 34 flag combinations, none of them a bare `sort`. The conclusion
   (no split for a bare `sort`) holds for both files. The wording fits only one of them.
6. **"Splitting a plain `cat` of one file is pure overhead"** was not measured here. The `naive-cat-pash-own`
   control has one untimed run.
7. **"on mains power"**: not shown in the power log (check 6).
8. **The time window "10:57–11:00"** leaves out the second control batch (11:01:04–11:01:16), whose
   results are in the README's control table. There was no sleep then either.
9. **The departure from 5 repeats** should be stated as a departure from the brief (check 6).

## What I left behind

My work is in `~/t024-check/` in the VM: `check1.py`, `check5.py`, `myrun.sh`, and my runs and logs under
`runs/`. My test sets are under `sets/`: `ctl-no-tr`, `naive-sed-debug` and `tr-debug`. The last two are copies
with one added line that writes down what the file is given; their records are in `sed_debug.txt` and
`tr_debug.txt`. Nothing in the worker's folder or the VM's `~/t024/` was changed.
