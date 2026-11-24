# PaSh on Koala's `spell.sh` with three sources of annotation files (pilot, 2026-11-24)

**What this is.** PaSh is a tool that speeds up shell scripts by running parts of them as several
copies at once on pieces of the input ("splitting" a command), then joining the results. It decides
what it may split from *annotation files*: three small files per command describing what the command
reads and writes and whether it can be split. This pilot runs one benchmark script under PaSh with
three different sources of those files and checks the output and the time.

**Sources compared** (a *set* is one folder of annotation files handed to PaSh for a run):

| Set | Files used |
|---|---|
| `bash` | no PaSh at all: plain bash, the reference output and time |
| `pash-own` | PaSh's own hand-written files, unchanged |
| `naive` | the naive LLM's files for every command it has (79 commands), PaSh's own for the rest |
| `caruca-pash` | Caruca's files made from its small PaSh grammars, for its 8 commands; PaSh's own for the rest |
| `caruca-main` | the same, but Caruca's main grammar where a command has one (`cut`, `rm`, `sort`) |

Naive files are the first run of each command in the Fig. 7 campaign. **All of a set's commands are
swapped in at once**; there were no runs swapping one command at a time. So a time difference belongs to
the set as a whole (to the swapped commands named below), not to any one command.

**The script.** Koala's `oneliners/spell.sh` (Koala is the benchmark suite that replaces PaSh's own
published one, whose input server is down), at Koala's small size (a 30 MB text). It is one pipeline:
`cat | sed | col | tr | tr | tr | sort | uniq | comm`. Which set supplies each command's files:

| Command | `naive` | `caruca-pash`, `caruca-main` |
|---|---|---|
| cat, sort | naive LLM | Caruca |
| sed, col, uniq, comm | naive LLM | PaSh's own |
| tr | PaSh's own (the naive LLM has no `tr` files) | PaSh's own |

(The naive LLM was shown PaSh's own `uniq` files as an example when it wrote its files.)

## What was found

| Set | Commands PaSh split | Output same as bash, and as Koala's stored answer | Seconds, median of 3 (min–max) | vs bash |
|---|---|---|---|---|
| `bash` | – | (reference) | 1.03 (1.02–1.03) | – |
| `pash-own` | sed, col, tr (2 of 3), sort | yes, 3 of 3 runs | **0.61** (0.60–0.62) | 1.69x faster |
| `naive` | cat, tr (2 of 3), sort | yes, 3 of 3 | 0.89 (0.89–0.91) | 1.15x faster |
| `caruca-pash` | cat, sed, col, tr (2 of 3) | yes, 3 of 3 | 1.07 (1.07–1.13) | 1.04x slower |
| `caruca-main` | cat, sed, col, tr (2 of 3) | yes, 3 of 3 | 1.07 (1.06–1.13) | 1.04x slower |

- **Every output was right**: 12 of 12 timed PaSh runs (and 12 more with the program-start counter, below)
  matched plain bash byte for byte and matched Koala's stored hash. Exit code 0 in all.
- **PaSh never fell back to plain bash with these four sets.** The script is one *region* (the piece
  PaSh's compiler is asked to handle); it was parallelized in 1 of 1 regions for every set, every run.
  No compiler exceptions, no "No region was parallelized" warning.
- **Splitting `sort` is what pays.** PaSh's own files and the naive LLM's both let PaSh sort 8 pieces
  and merge them. **Caruca's `sort` file allows no split for a bare `sort`**: Caruca's method only
  allows a split it can join end to end, and the file has a branch only for `sort -m`. Without the
  `sort` split, the Caruca sets split four cheap commands and end up slightly slower than bash.
- **The naive set loses `sed` and `col`.** The naive `col` file says `col` cannot be split. The naive
  `sed` file says it can (asked directly, it answers exactly as PaSh's own does), yet inside PaSh
  `sed` stays a single copy; with PaSh's own `sed` files in the naive set, `sed` splits (control below).
  So the naive `sed` file answers differently when PaSh calls it than when we call it. Why is **not
  established**; the file reads the sed script from the command's first word and checks it character by
  character, which is where the two calls could differ. It cost nothing in correctness here, only speed.
- **The naive set splits `cat`**, which PaSh's own files never do. Splitting a plain `cat` of one file
  is pure overhead; task 022 measured the same.

## Checks that the folder decides

Same script, one run each (outputs all right):

| Control | What changed from `naive` | Commands split |
|---|---|---|
| `naive` | – | cat, tr, sort |
| `naive-no-sort` | `sort`'s three files deleted | **none**: PaSh reported "InputOutputInformation for sort not provided" and ran the whole script as plain bash |
| `naive-col-pash-own` | PaSh's own `col` files instead of the naive LLM's | cat, **col**, tr, sort |
| `naive-cat-pash-own` | PaSh's own `cat` files | tr, sort (**cat** no longer split) |
| `naive-sed-pash-own` | PaSh's own `sed` files | cat, **sed**, tr, sort |

Each change of one command's files changed exactly that command, so PaSh is reading the folder given.

## How splitting was judged

Not from the output or exit code (PaSh falls back to bash quietly and the output is then right).
Three signals per run: PaSh's debug log (each region sent, and whether a parallel version was saved);
the parallel script PaSh wrote (how many copies of each command it runs side by side); and a stand-in
program placed first on the search path that records every time a command starts. A command counts as
split when PaSh's script runs 2 or more copies of it **and** it started more often than under bash.
Each set's files were also called directly, outside PaSh, for every command line of the script, and
their answers and any errors recorded (`answers.jsonl`); none raised an error.

Times come from separate runs without the stand-in program (it adds about 0.1 s to PaSh runs), run one
at a time and interleaved across sets, inside the Lima virtual machine `pash` (8 cores, Ubuntu 24.04,
PaSh commit `42a8b87`, its annotation package 0.2.4). The Mac was awake and on mains power for the whole
window (10:57–11:00; the power log shows the last wake at 10:18 and no sleep after).

## Files

| File | What it is |
|---|---|
| `run_koala.py` | the runner (runs inside the virtual machine; steps below) |
| `manifest.json` | commits (PaSh, Koala, Caruca's branch, this repo), package hashes, machine, and for every command in every set which source its files came from, with the naive run folder or Caruca folder and the three files' hashes |
| `invocations.jsonl` | how each of the 77 scripts in Koala's six groups is started, recorded from Koala's own launchers |
| `answers.jsonl` | each set's direct answer for each command line of `spell.sh` |
| `commands.jsonl` | per command and set: the files' source (`ours`, `pash-own` or `none`) |
| `results.jsonl` | one row per set and repeat: state, commands split, copies, region outcomes, output hash, same as bash, Koala's hash, seconds, fallback reasons |
| `regions.jsonl` | one row per region, set and repeat: region text, its commands and their sources, outcome, reason |
| `controls.jsonl`, `controls_regions.jsonl` | the same for the control sets |
| `logs/` | PaSh's debug logs (first repeat of each set), compressed |
| `orchestration/` | the briefs this work was done from |

To run again (inside the VM; the Mac's home folder is visible there read-only):

```sh
R=<this folder>/run_koala.py
python3 $R build && python3 $R discover && python3 $R answers --script oneliners/spell \
  && python3 $R controls --script oneliners/spell && python3 $R run --script oneliners/spell
# results are in ~/t024/out in the VM; copy them out with `limactl copy`
```

Any of the 77 recorded scripts can be given as `--script <group>/<name>` (e.g. `unixfun/3`); only
`spell` has been run.

## Limits

- One script, one input size, 8 workers. One region, so every rate here is out of 1.
- The other groups' scripts are recorded but not run. Weather's launcher stopped with an error after
  recording its 2 scripts; not looked into.
- The direct-call answers did not predict PaSh's behaviour for the naive `sed` file (above), so for the
  full suite those answers are a check, not proof.
- Harness fault found and fixed during the pilot: the stand-in recorded a command started with no
  arguments as having one empty argument (so the direct check asked about `sort ''`). Fixed, and every
  record here comes from the rerun.
