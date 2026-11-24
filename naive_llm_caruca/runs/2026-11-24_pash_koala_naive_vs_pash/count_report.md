# Counting the numbers for the PaSh-suite report

Two scripts turn the builder's records into every number and chart in the report. Nothing in the report
is counted by hand: the numbers are copied from `numbers.md`, and the checker re-runs the scripts.

## How to run

```sh
cd naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash
python3 -I timing_check.py --windows <records>/run_windows.jsonl --out <records>/timing_check.jsonl   # on the Mac
python3 -I count_report.py --records <records> --out <folder>
uv run --with matplotlib==3.9.2 python make_charts.py --numbers <folder>/numbers.json
```

- `timing_check.py` runs on the Mac (standard library only). For each run window the builder recorded,
  it reads the Mac's power log and writes one line: the sleep and wake events inside the window, whether
  the Mac was asleep when it began, and the power source at its start and end (the last "using mains" or
  "using battery" entry the power log holds at or before that moment, with its time). Run it soon after
  the batch: macOS keeps only a few days of the power log. `--pmset-log <file>` re-checks against a saved
  copy of the log.

- `count_report.py` needs only Python's standard library. It writes `numbers.md` (for people) and
  `numbers.json` (for the chart script). By default it reads the records in this folder and writes here.
- `make_charts.py` writes `figures/chartA.png`, `chartB.png` and `chartC.png` beside `numbers.json`:
  6.5 inches wide (a portrait page), text 8 points or larger, 300 dots per inch. It counts nothing.
- If a record lacks something the count needs, the script stops and names the file, the line and the
  missing field. It never guesses a value.
- **A run window with a sleep or wake inside it, or not on mains power at both ends, or with no power
  check, fails.** `count_report.py` still writes its numbers (with a warning at the top of `numbers.md`
  naming the windows), then stops with an error listing them. Times from those windows must be re-run
  before they are used (report plan 5.3).
- `--tag pilot` names the output `numbers_pilot.md` / `.json`; the chart script then writes to
  `figures_pilot/`. `--timing-check <file>` points at a power check outside the records folder.

**Smoke test on the pilot** (`spell`, the re-run in `validation_2026-11-24/`, which has the amended
records). The output is in this folder: `timing_check_pilot.jsonl`, `numbers_pilot.md`,
`numbers_pilot.json` and `figures_pilot/`:

```sh
python3 -I timing_check.py --windows validation_2026-11-24/run_windows.jsonl --out timing_check_pilot.jsonl
python3 -I count_report.py --records validation_2026-11-24 --timing-check timing_check_pilot.jsonl --out . --tag pilot
uv run --with matplotlib==3.9.2 python make_charts.py --numbers numbers_pilot.json
```

All three pilot windows (11:43:20–11:44:19 on 24 November) were valid: no sleep or wake inside, mains
power at both ends (the power log's last entry before them, at 11:40:20, says mains power). All 17 checks
pass. The failure path was tested too: windows made up to span this morning's sleep (10:03–10:18) or to
fall in a battery period were rejected by `timing_check.py`, and a power check marking the pilot's timed
window invalid made `count_report.py` stop with an error. Every table has one script, so most rates are
out of 1. The pilot's numbers agree with
the pilot README: PaSh split 5 of the script's 9 command uses with its own files, 4 with the naive LLM's
and 5 with each of Caruca's; every output was the same as bash.

## What each number means

The units are the report plan's (section 2). In short:

| Word | Meaning |
|---|---|
| script (N) | one benchmark script. A script that Koala's launcher starts more than once counts once; its output counts as right only if every start was right. N leaves out any script whose plain-bash output differs between bash's own runs (they are listed) |
| part (P) | a piece of a script PaSh's compiler is asked to handle (PaSh calls it a region), counted once per distinct text, from the first instrumented repeat. A loop's part counts once here; appendix A3 also counts each pass |
| command use (U) | one place in a part where a script calls a command; three calls of `tr` are three uses. Uses that ran outside every part sent to PaSh are counted separately, not in U |
| split | PaSh ran several copies of the command on pieces of its input and joined the results |
| own files / PaSh's own filled in / no files | for each use, whether the source brought its own files for that command, used PaSh's own because it had none, or nobody had files |

How each table is made:

- **Table 1.** *Output same as bash*: every run of the script with that source (both passes, all repeats)
  gave the same output and output files as bash, and none ran out of time. *Parts run in parallel* and
  *command uses split*: first instrumented repeat. *Faster than bash*: the median of the timed runs is
  below bash's median; the speed-up in brackets is the median over scripts of bash's time divided by the
  source's time.
- **Table 2 and chart A** pair each source with PaSh's own files: parts by script and part text, uses
  by script, part text and position. Chart A sorts every part into: run in parallel with both / only with
  this source / with neither / only with PaSh's own files.
- **Table 3** lists only the commands where some source split a different number of uses from PaSh's own,
  ordered by number of uses. Bold marks a cell that differs from PaSh's own.
- **Table 4, first row (agreement with PaSh's own files).** The unit is a distinct command line in the
  suite (the command and its arguments as PaSh passes them) for which the source has its own files.
  "Same inputs and outputs" compares what the two sets of files say the command reads and writes. "Same
  split decision" compares whether each allows a split PaSh can carry out. Lines where PaSh's own files
  give no answer are left out and counted separately. Also counted separately: lines where PaSh's own
  files split only with a special merge step (not by simply joining the pieces end to end) and the
  source says no split. The Caruca paper counted such a case as agreement; here it counts as a
  disagreement and is reported beside the rate (in the pilot: Caruca's files for a bare `sort`, both
  grammars).
- **Chart B** plots, per script, the median time with each source against the median with PaSh's own
  files. The grey points are the second, identical copy of PaSh's own files against the first: their
  spread is the noise. Larger points are scripts where the source's split choices differ.
- **Chart C** reads the commands of each script from the inventory and which source has files for each
  from the builder's per-command record. Caruca's two versions share one row when they have files for the
  same commands.
- **Appendix tables**: A1 lists every script in the inventory with its path in Koala, the 2022 script it
  stands for and whether it was run; A3 the reasons parts were not run in parallel, split into "the
  same under PaSh's own files" and "only with this source"; A4 every use whose result differs from PaSh's
  own, with its command line and the reason it was left whole, and each source's answer per command line;
  A5 the times; A6 what the records hold of the checks (the controls and the run windows).

## Checks the script makes on itself

Listed at the end of `numbers.md`, each passed or not. The script stops outright on the first three,
because pairing is impossible without them.

1. The distinct parts are the same (same texts, same number) under every source.
2. The command uses are the same (same part, same position) under every source.
3. Every answer row of a source has a matching answer row for PaSh's own files.
4. Each script sends PaSh the same sequence of part texts under every source.
5. The part count in the results record equals the parts listed in the parts record.
6. bash's own output is identical across all its runs.
7. The commands split per use match the commands split per script.
8. PaSh split a use exactly when its files allowed a split PaSh can carry out.
9. Every instrumented repeat split the same uses as the first.
10. A command line gets the same answer in every script that uses it.
11. The commands the inventory lists equal the commands seen starting, per script.
12. The controls that prove PaSh reads the given folder ran at the start and the end.
13. Koala's checkout did not change during any run.
14. The Mac was awake and on mains power in every run window (from `timing_check.py`; failing this one
    also stops the script, after writing).

On the pilot all pass.

## Pending on the full records

- **The power check's limit**: the power log notes the power source only at some events. On 24 November
  the entries saying mains power were at 10:18:45, 11:40:20 and 12:07:34, so there can be over an hour
  between them. A plug change between two entries is seen only at the next one. Each line records the
  time of the entry it relied on (`seen_at`), so a stale one can be spotted.
- **Clock check**: the windows use the VM's clock and the power log uses the Mac's. `timing_check.py`
  makes one read-only `date` call in the VM, records the offset on every line, and fails every window if
  it is over 5 s (pilot: +0.04 s; `--clock-offset` re-checks with an offset measured earlier). It is the
  offset when the check runs, not during the window, so run the check right after the batch.
- **Scripts started more than once** (ids ending in `#n`): the pooling code is written but untested, since
  `spell` is started once.
- **Parts not run in parallel** (appendix A3), **files that raise an error**, **filled-in uses whose result
  differs from PaSh's own**, **wrong outputs** and **uses outside every part**: none occur in the pilot, so
  those paths ran only on empty input. Re-read `numbers.md` by eye on the first full run.
- **Charts at full size** were checked with made-up numbers at the suite's scale (77 scripts, 120 parts,
  35 commands): readable at 6.5 inches. In chart A, a segment too narrow for its number stays unlabelled;
  in chart B, labels of the three points farthest from the diagonal can touch when points crowd.
- **One colour differs from the plan**: Caruca's main grammar is drawn in a lighter orange (`#f0b060`)
  than first planned, so it can be told from the PaSh-grammar orange (the chart skill's colour check).
  The two never appear without their names.
