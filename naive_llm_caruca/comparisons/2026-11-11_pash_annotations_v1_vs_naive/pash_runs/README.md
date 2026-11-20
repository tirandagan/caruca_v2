# Real PaSh runs with each side's annotation files (task 022)

Task: `ai_docs/tasks/022_pash_runs_v1_vs_naive.md`. **Start with [observations.md](observations.md).**
Every count is in [numbers_pash.md](numbers_pash.md).

## What was done

Each command line is turned into a one-line script, run once under plain `bash`, then once under PaSh
for every side, with 8 workers. A side is one source of annotation files for one command: v1's (from
its PaSh grammar, or its main grammar), each naive LLM run, PaSh's own hand-written files, and "no
annotation" (the command's files removed). A second part runs whole benchmark scripts with a side's
files for all eight commands loaded at once.

Everything runs inside the Lima virtual machine `pash` (PaSh at commit `42a8b87`, `pash-annotations`
0.2.4, GNU coreutils 9.4, 8 cores). PaSh's install and source are not changed: each side is a private
copy of PaSh's annotation package, chosen for one run with PaSh's `--local-annotations-dir` option.

## Files

| File | What it is |
|---|---|
| [observations.md](observations.md) | what was observed, in plain words, with the examples |
| [numbers_pash.md](numbers_pash.md) | every table, built by `count_runs.py` from the records |
| [controls.md](controls.md) | the checks that PaSh is really running and really reading each side's files |
| `run_pash.py` | the runner (runs inside the virtual machine) |
| `count_runs.py` | builds `numbers_pash.md`. It only counts |
| `lines_run.jsonl` | the command lines that were run, and which set each belongs to |
| `pash_runs.jsonl.gz` | one row per line and side: PaSh's state, both signals, outputs compared with `bash` |
| `causes.jsonl` | every run whose output differed from `bash`, re-run by hand-made splitting to find the cause |
| `timing.jsonl`, `timing_heavy.jsonl` | five repeats on a larger input: benchmark lines that split with the right output, and two `grep` lines that work hard on every input line |
| `scripts.jsonl` | the whole-script part |
| `results_page.html` | the source of the shareable results page, published at https://claude.ai/artifact/GEaB1mBP3VJo6ddCVcWJ5c (2026-11-20). To change the page, edit this file and publish it again to that address |
| [pash_bugs_for_review.md](pash_bugs_for_review.md) | faults found in PaSh itself. One went upstream on 2026-11-20 at Tiran's request (issue binpash/pash#794, pull request #795); the rest are still for review; `pash_bug_repros.sh` reproduces each on PaSh as installed, `pash_bug_repros.out` is its output |
| `manifest.json`, `controls_before.json`, `controls_after.json`, `answers_check.json`, `build.json` | machine, versions, commits, file hashes and the raw check results |
| `logs.tar.gz` | PaSh's own log of every run, and the first 4,000 bytes of both outputs wherever they differed |
| `first_pass.tar.gz` | the first pass, kept for the record. Three faults in the harness were corrected and the whole pass run again ([observations.md](observations.md), section 8) |

## How a run is judged

Nothing is inferred from the exit code or the output alone. Two signals are recorded for every run:
PaSh's log (does the script it generated contain split steps and worker copies?), and a stand-in
program placed first on the search path, which writes one line each time the command is started and
then runs the real command.

| State | Evidence |
|---|---|
| split | split steps in the log, and more than one copy of the command started |
| split set up, workers got no input | the generated script holds several worker copies, but the stream PaSh split carried no data, so the copies never started |
| not split | no split steps, one copy started; the log's reason is kept |
| PaSh error | PaSh's compiler raised an exception and the script ran as plain `bash` |
| unknown | no log, or the signals disagree |

## How to run it again

```sh
R=<this folder>/run_pash.py          # the Mac's home folder is mounted read-only inside the VM
limactl shell pash -- bash -lc "python3 $R build && python3 $R controls && python3 $R answers \
  && python3 $R select && python3 $R run && python3 $R causes && python3 $R timing && python3 $R heavy \
  && python3 $R scripts"
# results are written to ~/t022/out in the VM; copy them out with `limactl copy`, then on the Mac:
python3 count_runs.py
```

The line-by-line pass takes about six minutes, and everything together under an hour. This PaSh version
ignores its round-robin switch, so there is one PaSh run per line and side, not two.
