# What PaSh did with Caruca's annotation files and with the naive LLM's (task 022, 2026-11-19)

Every count here is in [numbers_pash.md](numbers_pash.md), built from the run records by a script that
only counts. The checks are in [controls.md](controls.md). PaSh's own faults are listed separately in
[pash_bugs_for_review.md](pash_bugs_for_review.md).

Words: **v1** is the original Caruca, on its branch `pash-python-annotations` (commit `4bf74dd9a`).
**The agent** is the naive LLM; each of its collected runs of a command is tried separately. **PaSh's
own** are the hand-written files shipped with PaSh. A **split** means PaSh ran 8 copies of the command
at once on pieces of the input and joined the results.

## The short answer

- **PaSh runs, and it reads the files it is given.** All checks pass, before and after the batch.
- **With either set loaded, PaSh really splits commands.** 2,377 PaSh runs: 382 command lines, each
  under every side.
- **v1's files:** every split they allow, PaSh carried out (139 of 139). They allow few. Output was right
  in every run with the files made from v1's PaSh grammar. The files made from v1's main grammar gave a
  **wrong answer on 7 `sort` lines**.
- **The agent's files:** they allow far more splits (655 of 1,013 runs), and PaSh carried out 423 of
  them. No split of the agent's gave a wrong answer where the command read the data that was split.
  But two of its three `grep` runs made PaSh return **nothing at all for 19 runs** (searching a folder,
  and `--color`), with exit code 0. PaSh's own `grep` files do the same.
- **PaSh itself is the largest source of trouble.** In 329 of the 2,377 runs its compiler raised an
  exception and the script ran as plain `bash`. PaSh's own files gave a wrong answer in 16 runs.
- **On whole benchmark scripts** (46 scripts, each set's eight commands loaded together) every output
  matched `bash`. PaSh split 35 scripts with the agent's set, 35 with PaSh's own, 35 with v1's
  main-grammar set and 27 with v1's PaSh-grammar set.

## 1. Is PaSh really running?

Yes. The checks, run before and after:

| Check | Result |
|---|---|
| A script known to split | split: 8 copies of `grep` started, output same as `bash` |
| The same script with grep's files removed from the folder | not split: 1 copy. So the folder we pass is what decides |
| Every side's folder, asked 84,193 questions inside the virtual machine | all 84,193 answers equal the ones recorded on the Mac |
| `sort -n -u` with v1's main-grammar files | split, and the output differs from `bash`. So a wrong answer is caught |
| This morning's script that came back right but unsplit | reproduced. Cause: `head -5`. With `head -n 5` it splits |
| A run where a side forbids a split and PaSh splits anyway | 0 of 2,377 |
| "No annotation" runs that split | 0 of 382 |
| Runs with no log, or whose two signals disagree | 0 |

## 2. The benchmark lines

220 command lines taken from PaSh's own benchmark scripts. For each, the number PaSh split.

| Command | Lines | v1, PaSh grammar | v1, main grammar | The agent, per run | PaSh's own |
|---|---|---|---|---|---|
| cat | 78 | 75 | (none made) | 75 | 0 |
| cut | 46 | 27 | 27 | 31, 31, 31, 31 | 31 |
| sort | 17 | 0 | 0 | 1, 10, 1, 1 | 9 |
| rm, cp, wc, split | 79 | 0 | 0 | 0 | 0 |

**Every output on these 220 lines matched `bash`, for every side.** For rm, cp and split the files left
behind matched too.

What is behind the numbers:

- **cut.** v1 answers only the exact situations it traced, so it has no answer for a file argument, for
  `-`, or for a value attached to its option (`cut -d' ' -f1`). That is 19 of the 46 lines. The agent allows all
  46, but PaSh's compiler failed on 15 of them (section 4), so it split 31.
- **sort.** v1 allows none of these 17. Three of the agent's four runs wrote a class that raises an
  exception on most lines, so PaSh gets no answer; the fourth run split 10, one more than PaSh's own.
- **cat.** v1 and the agent both let PaSh split `cat FILE`. PaSh's own files don't, and the timing shows
  why: split `cat` took 0.27 s against 0.03 s in `bash`.

## 3. Where the answers went wrong

The other 162 lines were picked because the sides disagree, or because task 021 flagged them. Every
run whose output differed from `bash` was re-run by hand (cut the input into pieces, run the command on
each, join) to find the cause.

| Side | Wrong outputs | What happened |
|---|---|---|
| v1, PaSh grammar | **0 of 382 runs** | |
| v1, main grammar | **7 of 223** | `sort -n -u`, `-n -s`, `-g -u`, `-h -s`, `-k 1 -u`, `-k 1 -s`, `-k 1,1 -u`. v1's files say the pieces can be joined end to end. PaSh did that and the result is not sorted. The hand-made split is wrong too, so the fault is in the annotation. Of the 8 `sort` lines these files let PaSh split, only `sort -m` came out right |
| The agent, all runs | **19 of 1,013** | all `grep`, in 2 of its 3 runs. `grep -r pattern folder`: the files call the folder an input stream, PaSh splits it, no data arrives, the output is empty. `grep --color pattern file`: the option table says `--color` takes the next word, so the pattern is swallowed. The oldest `grep` run has neither fault |
| PaSh's own | **16 of 377** | the same two `grep` faults (11 runs), `grep -m` and `grep -A` split (2), `cut -z` split (2), `sort --help` printed once per worker (1) |
| No annotation | 0 of 382 | |

Two things stand out:

- **Four of those seven `sort` lines are split correctly by all four of the agent's runs** (`-n -u`,
  `-n -s`, `-g -u`, `-h -s`), and the other three by one run (in the other three runs PaSh's compiler
  failed on them, so they ran unsplit). The agent tells PaSh to merge the sorted pieces with `sort -m`.
  v1's method can only say "join end to end" or "don't split", as the paper notes. PaSh's own files
  don't split any of the seven.
- **The agent's two `grep` faults are also in PaSh's own `grep` files**, which the agent was shown as
  an example. The agent's oldest `grep` run has neither fault, and splits almost nothing (1 of 48
  lines).

## 4. PaSh's own failures

In **329 of 2,377 runs** PaSh's compiler raised an exception. The script then ran as plain `bash`: right
output, exit code 0, nothing parallel. At its default settings PaSh prints at most a general warning
("No region was parallelized successfully", with a hint to check the annotations), and only when no
region of the script compiled. It is the same warning a script with nothing to parallelize gets. The
exception itself is only in the debug log.

*Corrected 2026-11-20: this paragraph first said there was no sign outside the debug log. Read in
`compiler/compilation_server.py` and seen in a run at default settings.*

| What PaSh tripped on | Runs | Example |
|---|---|---|
| The command after a pipe is believed to read a named file, not the pipe | 161 | `cut -d' ' -f1` (a value attached to its option is read as a file name); `sort -rn` with v1's PaSh-grammar files (the option isn't in the table) |
| A splittable command that PaSh sees as having two input files | 125 | `cat a b`, `grep x f1 f2` |
| A name used in PaSh's code and never imported | 34 | `grep -f patterns file` |
| A merge command with a value-taking option | 9 | the agent's `sort -m -k 1 -u` |

The agent lost 186 of the 655 splits its files allow this way, and PaSh's own files 63 of 178. v1 lost
none of its 139: it does not allow a split on such lines. **So over a quarter of what the agent's files
offer never reaches PaSh's workers, for reasons that are PaSh's.**

A separate state, 30 runs: PaSh set up a split with 8 workers, but the stream it split carried nothing,
so no copy ever started. These are the empty `grep` outputs in section 3.

## 5. Speed

- **The benchmark lines are too cheap to gain much.** On a 64 MB input, `cut` took 0.15 s in `bash` and
  0.23 s under PaSh, split or not. Of the 12 lines timed, 11 were slower split than in `bash`, and one
  (`sort -rn`) was 1.17 times faster. 54 timed combinations, 5 runs each, all outputs right.
- **A `grep` that works hard on every line** (16 MB input, 5 runs each):

  | Script | `bash` | v1, PaSh grammar | Agent, 20 Oct run | Agent, 28 Oct run | Agent, 13 Oct run | PaSh's own |
  |---|---|---|---|---|---|---|
  | input piped in, no options | 14.2 s | **2.2 s (6.4x)** | 2.3 s (6.3x) | 2.3 s (6.1x) | 14.3 s, not split | 2.3 s (6.1x) |
  | one option (`-i`) and a file argument | 17.8 s | 17.8 s, no answer | 14.8 s (1.2x) | 14.8 s (1.2x) | 17.9 s, not split | 14.8 s (1.2x) |

  When v1 has an answer, PaSh is as fast with it as with anyone's. One added option and a file argument,
  and v1 has no answer. Why the second line gains only 1.2x when split is not established; this
  pattern's speed depends heavily on how the input reaches `grep`.

## 6. Whole benchmark scripts

46 of PaSh's benchmark scripts (`oneliners` and `unix50`), run unchanged, with each side's files for all
eight commands loaded at once. Their own inputs could not be downloaded (the server did not answer), so
they read this task's 4 MB text instead.

| Set loaded | PaSh split | Not split | PaSh error | Output same as `bash` |
|---|---|---|---|---|
| v1, PaSh grammar | 27 | 6 | 13 | 46 of 46 |
| v1, main grammar (cut, rm, sort) | 35 | 6 | 5 | 46 of 46 |
| The agent (first campaign run of each command) | 35 | 5 | 6 | 46 of 46 |
| PaSh's own | 35 | 5 | 6 | 46 of 46 |
| No annotation | 0 | 46 | 0 | 46 of 46 |

- **The agent's set behaves like PaSh's own** on all 46 scripts: the same 35 split, with `sort`, `cut`
  and `grep` running as 8 copies in the same scripts. It also splits `cat`.
- **v1's sets never split `sort`** (0 scripts, against 11 for the agent's and PaSh's own). With the
  main-grammar set the rest of each pipeline still splits.
- **v1's PaSh-grammar set loses 8 whole scripts.** Its `sort` option table lists only `-m`, so
  `sort -rn` is read as a file named `-rn`, PaSh's compiler fails, and the entire script runs as `bash`.
- 6 scripts failed under PaSh's own files too: `tail -n 1` (2), `head -15` and `cut -d: -f1` (1), input
  redirection (2), and a second missing import in PaSh (1).

## 7. What this suggests

These are my reading of the numbers above, not measurements.

- **v1's files are the careful ones.** What v1 saw in a trace, PaSh could use. The cost is reach: a
  different flag, a file argument or an attached value, and v1 has no answer.
- **v1's one unsafe answer has a clear shape.** It is `sort` with a second option that changes what
  "equal" means. This matches task 021's reading of the files; here it is confirmed under PaSh on 7
  lines.
- **The agent's files reach as far as PaSh's hand-written ones**, and carry two of the same faults.
- **Half of this story is PaSh.** Its compiler failed on 15 of the 46 `cut` benchmark lines, with the
  agent's files and with its own alike.

## 8. Corrections made during the run

The first pass had three faults in my harness. All were found from the "unknown" state or a control,
fixed, and **the whole pass was run again from scratch**. The first pass is kept in `first_pass.tar.gz`.

| Fault | How it showed | Fix |
|---|---|---|
| Worker copies given a pipe as their file argument were counted as PaSh housekeeping | 65 runs marked "unknown" | count them; 35 became "split" |
| For `cat` lines, the script fed input with `cat`, which the side's `cat` files also governed | 1 run split though its side forbade it | feed those lines with `tail -n +1 FILE` |
| The `bash` reference ran the real program, the PaSh run a stand-in, and `--help` prints the program's name | "no annotation" runs with different output | the reference run uses the stand-in too |

The 30 runs still "unknown" after the first fix turned out to be real (section 4, last paragraph) and got
their own state.

## 9. Limits

- **Eight commands, 382 lines.** 162 of the lines were chosen because the sides differ, so pooled counts
  overstate how often they differ. Section 2 is the unbiased part.
- **One input.** A wrong split shows only on input that exercises it. A line that came out right here is
  not proved safe.
- **The disagreement lines had their file names replaced** with prepared files; options are unchanged.
- **Whole scripts ran on our text, not their own data,** so nothing is said about their speed.
- **Timings were taken with the Mac on battery power.**
- **One PaSh revision** (`42a8b87`, with `pash-annotations` 0.2.4).
- Not done: PaSh at other worker counts; v1's files for more than these eight commands.
