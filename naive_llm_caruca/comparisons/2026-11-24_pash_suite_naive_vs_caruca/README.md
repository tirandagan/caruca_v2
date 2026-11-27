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

*Corrected 2026-11-24 after the checker's review (`orchestration/review_checker.md`): the `sed` and `tr`
explanations, the `sort` wording, the control sentence, the power and time-window statements, and the
number of repeats. The measurements are unchanged.*

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
- **The two faster sets are the two that split `sort`.** PaSh's own files and the naive LLM's both let
  PaSh sort 8 pieces and merge them. Which command made the time difference was not tested: all of a
  set's commands are swapped in at once. **Caruca's `sort` files allow no split for a bare `sort`**:
  Caruca's method only allows a split whose pieces can be joined end to end, and neither of its files
  has a branch for `sort` without options (the PaSh-grammar file has one only for `sort -m`; the
  main-grammar file has 34 option combinations, none of them empty).
- **The naive set loses `sed` and `col`.** The naive `col` file says `col` cannot be split. The naive
  `sed` file looks at the sed script itself. PaSh hands it the script with its double quotes still on
  (`"s/[^[:print:]]//g"`), and the file reads the opening quote as a sed command it does not know, so
  it allows no split. Given the script without quotes it would allow one. It cost nothing in
  correctness here, only speed.
- **Why only 2 of the 3 `tr` commands split, under every set.** All sets use PaSh's own `tr` files.
  PaSh hands them `tr -cs A-Za-z "\n"` with the quotes on, so the file sees that the command squeezes
  newlines, and then offers only a merge step that PaSh has not implemented. PaSh uses only recipes
  whose parts are all implemented, so it leaves that `tr` whole. `uniq` stays whole for the same reason
  (its only merge step, in PaSh's file and in the naive LLM's, is not implemented).
- **The naive set splits `cat`**, which PaSh's own files never do. Its cost was not measured here
  (the control that removes it ran once, untimed).

## Checks that the folder decides

Same script, one run each (outputs all right):

| Control | What changed from `naive` | Commands split |
|---|---|---|
| `naive` | – | cat, tr, sort |
| `naive-no-sort` | `sort`'s three files deleted | **none**: PaSh reported "InputOutputInformation for sort not provided" and ran the whole script as plain bash |
| `naive-col-pash-own` | PaSh's own `col` files instead of the naive LLM's | cat, **col**, tr, sort |
| `naive-cat-pash-own` | PaSh's own `cat` files | tr, sort (**cat** no longer split) |
| `naive-sed-pash-own` | PaSh's own `sed` files | cat, **sed**, tr, sort |

In the three controls that swap one command's files for PaSh's own, exactly that command changed. In the
control that deletes `sort`'s files, nothing split at all: PaSh ran the whole script as plain bash.
Either way PaSh is reading the folder it is given. The controls were run again after the method fix
below, at the start and at the end of a run of the script, with the same result.

## How splitting was judged

Not from the output or exit code (PaSh falls back to bash quietly and the output is then right).
Three signals per run: PaSh's debug log (each region sent, and whether a parallel version was saved);
the parallel script PaSh wrote (how many copies of each command it runs side by side); and a stand-in
program placed first on the search path that records every time a command starts. A command counts as
split when PaSh's script runs 2 or more copies of it **and** it started more often than under bash.
Each set's files are also asked for their answer, with errors recorded rather than hidden (PaSh hides
them). **Method fixed 2026-11-24:** the first version asked the files directly with the command line
rebuilt by us, which drops the double quotes PaSh keeps on quoted words. That gave a different answer
from PaSh's on 2 of the 9 command lines (`sed` under the naive set, `tr -cs` under all sets). The runner
now replays PaSh's own steps on the files PaSh keeps (its expansion of the script's variables and its
parsing of each command), so the files get exactly what they get inside PaSh. On the re-run, that answer
predicted whether PaSh split the command for all 180 command uses compared (every set, main and control
runs). Those records are in `validation_2026-11-24/`; the direct answers are kept beside them for
comparison.

Times come from separate runs without the stand-in program (it adds about 0.1 s to PaSh runs), run one
at a time and interleaved across sets, inside the Lima virtual machine `pash` (8 cores, Ubuntu 24.04,
PaSh commit `42a8b87`, its annotation package 0.2.4). The Mac was awake for every timed and control run:
the timed runs were 10:59:38–11:00:08 and the controls 10:59:29–10:59:38 and 11:01:04–11:01:16, and the
power log shows the last wake at 10:18 and no sleep after. Whether it was on mains power is not shown:
the battery status read at 10:49 said mains power, but the power log records no change of power source
after 10:18, when it was on battery. Each set was timed **3 times, not the 5 the first brief asked for**;
3 is Tiran's later decision (`orchestration/metrics_spec.md`).

## Files

| File | What it is |
|---|---|
| `run_koala.py` | the runner (runs inside the virtual machine; steps below) |
| `manifest.json` | commits (PaSh, Koala, Caruca's branch, this repo), package hashes, machine, and for every command in every set which source its files came from, with the naive run folder or Caruca folder and the three files' hashes |
| `invocations.jsonl` | how each of the 77 scripts in Koala's six groups is started, recorded from Koala's own launchers |
| `answers.jsonl` | each set's answer for each command line of `spell.sh`, asked directly (first method; see "How splitting was judged") |
| `commands.jsonl` | per command and set: the files' source (`ours`, `pash-own` or `none`) |
| `results.jsonl` | one row per set and repeat: state, commands split, copies, region outcomes, output hash, same as bash, Koala's hash, seconds, fallback reasons |
| `regions.jsonl` | one row per region, set and repeat: region text, its commands and their sources, outcome, reason |
| `controls.jsonl`, `controls_regions.jsonl` | the same for the control sets |
| `logs/` | PaSh's debug logs (first repeat of each set), compressed |
| `orchestration/` | the briefs this work was done from, and the checker's review |
| `validation_2026-11-24/` | the re-run with the fixed method and the records the report needs (one row per command use, a second copy of PaSh's own files for timing, and others; see its `NOTES.md`). Its times are not used: another worker was using the virtual machine |

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
- The other groups' scripts are recorded but not run. Weather's launcher ends with an error after
  recording its 2 scripts; the error comes from its last step (moving an empty `plots` folder), not from
  the scripts.
- The first method's direct answers did not match PaSh on 2 of 9 command lines (above). The fixed method
  replays PaSh's steps; it matched PaSh on all 180 command uses re-run, on this one script.
- Harness fault found and fixed during the pilot: the stand-in recorded a command started with no
  arguments as having one empty argument (so the direct check asked about `sort ''`). Fixed, and every
  record here comes from the rerun.
