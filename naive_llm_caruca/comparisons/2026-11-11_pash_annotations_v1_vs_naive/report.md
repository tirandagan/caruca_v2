# v1 vs the naive LLM: PaSh annotations, first comparison (2026-11-11)

Commands: cat, cp, cut, grep, rm, sort, split, wc. **v1** means task 020's files, built from v1's split-mode
traces: `v1-pash` from v1's PaSh grammar, `v1-main` from its main grammar (cut, rm, sort only). **The
agent** means every collected naive-LLM run of the command (1-4 per command). **PaSh's own** means the
hand-written classes shipped with PaSh.

How this was made:

- **Counts:** [numbers.md](numbers.md), from the scorer, on 12,656 lines in total: benchmark lines, v1's
  traced lines and the agent's own test lines.
- **Judgements:** [assessments/](assessments/), written by Claude (`claude-opus-5-5`) under
  [rubric v1](rubric.md). The assessor saw the sides under random letters and was told not to run
  anything.

**Nothing below has been run under PaSh yet. Only one claim has been confirmed by running the command;
it is marked "confirmed".**

## Do the input/output sets differ, and how? (Greenberg's question)

**Where both sides give an answer, the sets are mostly the same.** For example, on `sort` with v1's main
grammar they are identical on 890 of the 1,145 lines v1 answers. The main difference is coverage. v1
answers only the exact situations it traced, which is 1-49% of lines depending on the command and
grammar. The agent answers 85-100% of lines. On a line v1 can't answer, PaSh gets nothing and treats the
command as side-effecting.

Where the sets do differ, there are five kinds of cause:

| Cause | Who is right | Examples |
|---|---|---|
| **v1 saw what the command really did** | v1 | `rm --help f`: only v1 (main grammar) says `f` is untouched and only help text is written. The agent and PaSh's own say `f` is removed. The same holds for `--help`/`--version` on cut and sort. |
| **v1's PaSh grammar lists too few flags**, so PaSh reads a flag as a file | the agent | `rm -f x` is read as removing a file named `-f`; `sort -n` as reading a file `-n`; `cat -s` as reading `-s`; `grep -n foo` as reading the pattern `foo` as a file. v1's PaSh grammar for rm lists no options at all, and sort's lists only `-m`. This comes from the grammar, not from the traces. |
| **v1's recorded files look wrong** | the agent (needs running) | cp: v1 says the source is written as well as read; this is in v1's own JSON, not added by the writer. split: v1 says standard input is read even when a file is given, and records no output files. sort `-o out`: v1 (main grammar) says standard output is written too. |
| **The agent knows something the traces never showed** | the agent | `sort -T dir`: the agent says the temporary-file folder is written. v1 never saw it used, because its inputs are small. `cp -i` and `cp -v`: the agent records standard input and standard output. |
| **Shared by every side, from PaSh's parser** | nobody | A value attached to its option (`cut -d: -f1`, `sort -k1n`, `--opt=value`) is read as a file name. That affects 17 of the 46 `cut` benchmark lines. Options whose value is optional (`--interactive`, `--backup`, `--color`) swallow the next word in the agent's and PaSh's own tables. No side records that `rm -i` reads standard input. |

## Splitting

- **v1 allows unsafe splits of `sort` (confirmed for one).** v1's main-grammar annotation marks `sort -n -u` safe to
  split and join. Run on GNU sort 9.4, `printf '2\n1\n' | sort -n -u` gives `1 2`, and the split version gives `2 1`.
  The same holds for `-n -s`, `-g -u`, `-h -s`, `-k … -u` and others (34 situations in all, most of them
  safe `-m` ones). Likely cause, not yet established: v1 keeps the most parallelizable label across its
  test inputs, and on its text inputs the numeric sorts see every key as equal.
- **The agent's `sort` classes crash on most lines in 3 of 4 runs.** They pair round-robin splitting with
  a custom merge, which PaSh's code refuses with an exception, so PaSh does not split those lines. The
  fourth run is the only side, of either kind, that the assessor rated both safe and wide.
- **cut:** the agent splits widely and safely. PaSh's own splits `-z`, which is unsafe. v1 splits only
  the few situations it traced.
- **grep:** the agent's two recent runs, and PaSh's own, split multi-file and recursive searches, which
  the assessor rated unsafe. PaSh's own also splits `-m`/`-A`/`-B`/`-C`. The oldest agent run is the
  careful one.
- **cat:** the agent splits widely, including `-n`, with a mapper it marks as not implemented. That is
  doubtful and needs running.
- **wc:** no side gives PaSh a split that works.

## Run to run, and the assessor

- **The agent's runs:** the four `cut` runs give identical answers on all 8,826 lines, though their code
  differs. The `sort` runs agree on inputs and outputs on 99% of lines, but on splitting on only 28-94%.
- **The assessor:** cut, sort and rm were assessed a second time with the letters redrawn, and 111 of 114
  rating fields came out the same ([unblinded.md](assessments/unblinded.md)).

## Next

1. **Run the checks the assessments list** (69 in total) in the Lima VM `caruca`, starting with v1's
   unsafe `sort` splits and cp's "source written".
2. **Real PaSh runs** on the benchmark lines with each side's files.
3. **Rubric v2:** name the output file as given, count "no answer" separately rather than as a difference
   type, and add a field per "better" verdict so that running can confirm or refute each one.
