# Where the sources differ from PaSh's own files on `spell.sh`, and whose error each one is

Worker's answer to `brief_naive_fix_sed_cat.md`, 2026-11-24. It covers the six cells of the report's
Table 2 where a source made PaSh do something different from PaSh's own files: `cat` (naive LLM and both
Caruca sets), `sed` (naive LLM), `col` (naive LLM) and `sort` (both Caruca sets).

**Words used here.** *Split*: PaSh runs several copies of a command at once, each on a piece of the input,
and joins their outputs. *Whole*: PaSh runs one copy. *File*: one of the three small annotation files that
tell PaSh what a command reads and writes and whether it may be split. *Sources*: PaSh's own files (written
by PaSh's authors), the naive LLM's (an AI agent given only the binary, its manual and a format
description), and Caruca's (made by Caruca from what it saw when it ran the command).

## The short answer

| Command, source | The file says | What is true | Whose error | Kind | Output still right? | Being fixed? |
|---|---|---|---|---|---|---|
| `sed`, naive LLM | may split this script, but refuses it here | `sed 's/[^[:print:]]//g'` works on each line alone, so splitting it is safe | nobody's judgment: the file was never told PaSh keeps the quotes on the script | **instrument gap** (shows up as: file misreads its input) | yes | yes: format description repaired, `sed` re-run (section 1) |
| `col`, naive LLM | `col` can never be split | in general it can't: a reverse line feed near a piece boundary changes the output (tested). In `spell.sh` it is safe, because the `sed` before it has already removed those characters | none: the naive file is right about the command; PaSh's own file is the less careful one | **design choice** (a safe refusal, not a wrong claim) | yes | no |
| `cat`, naive LLM | a plain `cat FILE` may be split | splitting it gives the same output, but only adds work | none | **design choice** (correct, not useful) | yes | no |
| `cat`, Caruca (both sets) | the same | the same | none | **design choice**, made by Caruca's method rather than by judgment | yes | no |
| `sort`, Caruca PaSh grammar | a bare `sort` may not be split | it may, if the pieces are merged with `sort -m`, which is what PaSh's own file does | none | **design limitation of the method**: Caruca can only allow splits whose outputs are joined end to end | yes | no |
| `sort`, Caruca main grammar | the same | the same | none | the same | yes | no |

**So on this script none of the six differences is a wrong statement about a command.** One is a gap in
what the naive LLM was told (`sed`); five are choices or limits that cost speed but not correctness. The
report's Table 2 notes call `col` "a wrong judgment" ("it can [be split]"). That should change: the naive
`col` file is right in general and PaSh's own file is permissive (row 2 and section 3).

## 1. `sed`, naive LLM: an instrument gap, repaired

**The fault, reproduced.** I loaded the naive `sed` file (first Fig. 7 run,
`runs/2026-10-28_124823_naive-run-sed_sed_PROMPT_v1/output/annotation/`) and PaSh's own (pash-annotations
0.2.4) into private copies of the package and gave each one the script word in both forms, the way PaSh
gives it: as an object whose text is the word. Ways to split each file allows:

| Script word given to the file | naive LLM's file | PaSh's own file |
|---|---|---|
| `s/[^[:print:]]//g` (no quotes) | 2 | 2 |
| `"s/[^[:print:]]//g"` (quotes on, as PaSh gives it) | **0** | 2 |
| `s/d/x/` | 2 | 2 |
| `"s/d/x/"` | 0 | **0** |
| `/foo/d` | 2 | 0 |

This matches the checker's own record from inside PaSh (`~/t024-check/sed_debug.txt` in the `pash` VM:
`'"s/[^[:print:]]//g"' local=False`).

**The path, step by step** (PaSh commit `42a8b87` in the `pash` VM):

1. PaSh's parser turns the quoted word `'s/[^[:print:]]//g'` into a quoted-text node
   (`shasta.ast_node.QArgChar`).
2. `compiler/annotations_utils/util_parsing.py`, `parse_arg_list_to_command_invocation`: every operand
   becomes `Operand(Arg(...))` (line 121), still holding those nodes.
3. The file asks for the script with `get_first_operand_name_as_string()`, which returns
   `str(first_operand.get_name())` (pash-annotations, `Generator_Interface.py` line 31-35).
4. `str()` of an `Arg` is `format_arg_chars(...)` (`ir_defs/arg.py` line 15-16), and a quoted node formats
   itself as `'"{}"'.format(...)` (`QArgChar.format`): **double quotes added, whatever quotes the script
   used**.
5. The naive file's script reader (`_Checker.check` in its `ParallelizabilityInfoGeneratorSed.py`) reads
   the first character as the sed command, finds `"`, which is not a sed command it knows, and returns
   "not line-local" (`return False  # unknown command`). No split is offered.

PaSh's own file passes for a different reason, not because it handles quotes: its rule is "first word
starts with `-` or `s`, or contains neither `d` nor `q`". With the quote on, the `s` test fails, but this
script has no `d` or `q`, so the last test lets it through. With a `d` anywhere in the script (`"s/d/x/"`),
PaSh's own file also refuses.

**Could the agent have known? No.** Everything it was given about operands:

- `formats/annotation.md`: `get_first_operand_name_as_string()` returns "the first operand's text". Nothing
  says the text keeps the quotes.
- The samples (`samples/{grep,rm,tee,uniq}/annotation/`): none looks at an operand's text.
- The prompt (`PROMPT_v1.md`): nothing on how PaSh passes words.
- The installed package the agent read (its log shows it opened the two interface files): the method is
  `str(first_operand_arg)`, which says nothing about what the object's text is. That is decided in PaSh's
  compiler, which is not on the agent's machine.

So no reading of what it had would give a right answer here. That is an instrument defect, under the
project rule (`memory/feedback_instrument_defect_vs_tuning.md`).

**Repair.** One sentence added to `formats/annotation.md`, below the table of inspection calls, nothing else
changed:

> Operands and option arguments arrive as PaSh passes them: a quoted word keeps its quotes, written as
> double quotes, so the script word in `sed 's/a/b/' file` arrives as `"s/a/b/"`, with the `"` characters
> part of the text.

The example uses a different script from `spell.sh`'s, so it does not hand over the answer to the
benchmark.

**Re-run.** See "Re-run of `sed`" at the end.

## 2. `cat`: who is right?

### What each file says

| Source | File | Says about `cat FILE` (no options, one file) | Why |
|---|---|---|---|
| PaSh's own | input/output file only; **no** split file | runs whole (when the split file is absent, PaSh does not split) | not written down in the file. PaSh's older JSON annotation (in v1's `benchmarks/annotations/pash/cat.json`) did call plain `cat` splittable ("stateless"). Why the current package leaves it out is not established |
| Naive LLM | `runs/2026-10-28_100411_naive-run-cat_cat_PROMPT_v1/output/annotation/ParallelizabilityInfoGeneratorCat.py` | split: by file, by consecutive pieces, or by lines dealt in turn, then join in order | its comment: "cat is a per-line transformation". It also handles `-n`, `-b` and `-s` carefully (numbering and squeezing across pieces), refusing or using a boundary fix |
| Caruca, both sets | `caruca/save_pash_py/cat/pash_grammar/trace_1/` (task 021's `sides.jsonl`; Caruca has no main grammar for `cat`, so both sets use this file) | split by consecutive pieces or lines dealt in turn, then join in order; only with no options and 0 or 1 files | Caruca ran `cat` on input cut into pieces and saw the joined outputs equal the whole output ("stateless") |

### Is splitting `cat FILE` correct? Yes.

`cat` of one file copies it unchanged. Copying each piece and joining the copies in order gives the same
bytes. Evidence: every PaSh run with split `cat` matched bash, in this pilot (all runs of the naive and
Caruca sets, same hash as bash and as Koala's stored answer) and in task 022 (75 of 75 `cat` lines split by
the naive and Caruca files, output identical; `comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/observations.md`).

### Is it useful? No.

`cat` does no work on the data except copying it, so there is nothing to share out. What PaSh does with a
split `cat` in this script (from the parallel script in the pilot's naive log,
`logs/oneliners_spell__naive__instrumented.log.gz`):

1. a splitter (`r_split`) reads the 30 MB file and deals it out in 1 MB blocks to 8 pipes;
2. 8 copies of `r_wrap bash -c 'cat'` each take their blocks, strip PaSh's block labels, copy the data and
   label it again: 8 more `bash` processes and 8 `cat`s;
3. a merger (`r_merge`) reads the 8 pipes and puts the blocks back in order, then hands the stream to `sed`,
   which runs whole in the naive set.

So every byte is copied about three more times and passes through about 17 more processes, and no work is
saved. Existing measurements:

- **Task 022, on the line alone** (`pash_runs/timing.jsonl`, 64 MB input, 5 repeats, medians):

  | Line | bash | PaSh, `cat` whole | PaSh, `cat` split (naive LLM) | PaSh, `cat` split (Caruca) |
  |---|---|---|---|---|
  | `cat` (reads standard input) | 0.03 s | 0.11 s | 0.23 s | 0.24 s |
  | `cat WIKI/ARG0` | 0.02 s | 0.10 s | 0.27 s | 0.29 s |
  | `cat data_file` | 0.03 s | 0.10 s | 0.27 s | 0.27 s |

  Splitting more than doubled PaSh's time on its own.
- **This pilot, inside the whole script**: the naive set took 0.89 s (median of 3; 0.89-0.91) and the
  control with PaSh's own `cat` files took 0.877 s in **one** run. A 0.01 s difference from one run is
  inside the naive set's own spread, so in `spell.sh` the cost of the split `cat` was **not measurable**
  here. The `cat` step is not where this pipeline spends its time.

**A timed test, to run later (when the `pash` VM is free).** Inside the VM, from this folder:

```sh
python3 run_koala.py run --script oneliners/spell --sets bash pash-own naive naive-cat-pash-own --repeats 5
```

The `run` step accepts any set from `sets_wanted()`, which includes the control sets (read in
`run_koala.py`; not tried). Compare the medians of `naive` and `naive-cat-pash-own`.

### Verdict

- **Naive LLM: design choice, not a judgment error.** Its claim about `cat` is true; it chose to allow a
  split that is correct but not worth making. The agent was not told what PaSh does with a split, so it
  could not weigh the cost, and the format description says nothing about cost. Not an instrument gap in
  the sense of the rule above: a right answer (allow the split) was possible and is what it gave.
- **Caruca: design choice made by the method.** Caruca allows every split it saw joining correctly. It has
  no notion of whether a split pays. Its claim is true too.
- **PaSh's own file: also right.** Leaving `cat` whole is the better choice for speed. Whether PaSh's authors
  left the split file out for that reason is not written anywhere I found.

## 3. `col`, naive LLM: the naive file is right, and PaSh's own is the permissive one

The naive file (`runs/2026-10-28_093614_naive-run-col_col_PROMPT_v1/output/annotation/`) allows no split, and
says why: reverse line feeds move later text onto earlier lines, and character-set shifts carry from line
to line, so a piece's output can depend on the next piece. PaSh's own file allows a split always, with no
condition.

**Checked by running** `col -bx` (util-linux 2.39.3, in the `pash` VM, a few bytes of input, no timing):

| Input | `col -bx` on the whole | on the two pieces, joined |
|---|---|---|
| piece 1 `one\ntwo\n`, piece 2 `\vX\nthree\n` (`\v` is a reverse line feed) | `one` / `Xwo` / `three` | `one` / `two` / `X` / `three` |

So splitting `col` changes the output when a reverse line feed falls just after a piece boundary. (The
manual also lists `ESC 7` as a reverse line feed; this `col` ignored it in my test, and `\v` worked.)

In `spell.sh` the split is safe: the `sed` before `col` deletes every non-printing character, `\v` and `ESC`
included, so `col` never sees one. A file looks at one command at a time and cannot know that.

**Verdict: naive LLM, design choice (a safe refusal); no error. PaSh's own file is wrong in general, right on
this script.**

## 4. `sort`, Caruca: a limit of the method

Both Caruca `sort` files allow no split for a bare `sort`. The PaSh-grammar file has one branch, for
`sort -m` alone; the main-grammar file has 34 option combinations, none of them empty (checker, check 7
item 5, re-read here). PaSh's own file splits `sort` and joins the pieces with `sort -m`, a merge.

The fact: splitting `sort` is correct only with a merge; joining sorted pieces end to end is wrong. Caruca's
method decides "splittable" by running the command on pieces and checking whether the outputs **joined end
to end** equal the whole output. For `sort` they don't, so Caruca rightly refuses the only kind of split it
can express. It has no way to discover or express "split, then merge".

**Verdict: Caruca, design limitation of the method. Not a wrong claim.** It costs the most speed of any cell
here, because `sort` is where this script spends its time. Output right.

## 5. Are the two sources' errors the same kind?

**No.** The naive LLM's files *reason about the command* and can go wrong in what they reason from: in
`sed` it wrote a careful, correct reader of sed scripts, but it read text that was not what it expected,
because nobody told it how PaSh hands the words over. Its other two differences (`cat`, `col`) are choices:
one generous (allow a useless but harmless split), one cautious (refuse a split that is unsafe in general).
Caruca's files *record what it observed*: they never claim more than the runs showed, so they make no
wrong claims here, but they cannot reach a split that needs anything beyond joining end to end (`sort`),
and they cannot tell a useful split from a useless one (`cat`). The naive LLM can know more than it has
tested and can misjudge; Caruca cannot misjudge what it tested but cannot go past it.

## 6. Is any of PaSh's own files wrong on this script?

**No.** On `spell.sh` every PaSh's-own answer is safe and its output was right. Two of its files are
permissive in general, which this script does not exercise:

- **`col`**: splits always; wrong when a reverse line feed sits at a piece boundary (section 3).
- **`sed`**: its rule lets through any script without `d` or `q`. I gave it `N;s/\n/ /` (join each pair of
  lines): it allows 2 splits, with or without quotes. Run on pieces, that script pairs the wrong lines:
  `1 2` / `3 4` on the whole of `1..4`, but `1` / `2 3` / `4` when cut after line 1 (run in the `pash` VM,
  GNU sed 4.9). The naive `sed` file refuses this script (it treats `N` as unsafe). Its rule also tests the
  quoted text and so refuses splittable scripts that contain a `d` (`"s/d/x/"`).

PaSh's own `tr` file is the third quote case (the checker's finding): it reads `"\n"` with the quotes and
leaves `tr -cs A-Za-z '\n'` whole under every set. That loses speed, not correctness, and is the same for
all sources, so it is not in Table 2.

## Not established

- Why the current PaSh package has no split file for `cat` when its older JSON annotation called `cat`
  splittable.
- Whether the split `cat` costs any time inside `spell.sh` (one untimed control run; the timed test above
  would settle it).
- Why `col` ignored `ESC 7` in my test.

## Re-run of `sed`

- **Folder:** `runs/2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1/` (under `naive_llm_caruca/`). Ledger row: `"repeat": 2`,
  `"billing": "requesty"`, `"note": "after format repair 2026-11-24: operands arrive as PaSh passes them (quotes kept)"`.
- **How:** exactly as the campaign: PROMPT_v1, fresh clone of `naive-golden`, Fable 5.1 at medium effort, through
  `fig7_campaign/run_campaign.py` (two options added to it for this: `--repeat`, `--note`). 634 s, 23 turns,
  969 program runs logged; **$4.64** by Claude Code's own figure (budget $5; run 1 cost $2.60).
- **What changed in the file:** it now removes one pair of surrounding quotes before reading the script
  (`_strip_quotes`, with the comment "PaSh hands over quoted words with their (double) quotes still
  attached"). The session read the new sentence.
- **The files load:** the syntax file imports under v1's grammar code; the parser table loads; both PaSh
  classes import and answer.
- **Asked directly, operand as PaSh passes it** (`"s/[^[:print:]]//g"`): **2 ways to split** (run 1: 0).
  **Unquoted** (`s/[^[:print:]]//g`): **2** (run 1: 2). It still refuses `"N;s/\n/ /"` (right) and
  allows `"/foo/d"` (right).
- **Not done:** PaSh has not been run with it; the orchestrator reruns the benchmark. One run only.
- I deleted the `__pycache__` folders the run left in `output/` (compiled copies, not the agent's files);
  run 1's folder still has its own.
