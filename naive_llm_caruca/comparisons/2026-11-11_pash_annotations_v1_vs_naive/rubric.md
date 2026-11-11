# Rubric for the qualitative assessment

**Version 1, 2026-11-11.** Any change gets a new version number, a date and a line in the change log
at the end. Each assessment says which version it used.

## What you are assessing

PaSh is a tool that runs shell scripts in parallel. For each command it needs an *annotation*: three
files telling it how to read the command line and what the command does.

1. **`<cmd>.json`, the parser table:** which words are flags (no value) and which are options (take a
   value), and, for options whose value is a file, how that file is used.
2. **`InputOutputInfoGenerator<Cmd>.py`, the input/output class:** for a parsed command line, which
   operands are files the command reads, which are files it writes, which are plain words, and whether it
   reads standard input and writes standard output. If it sets `self.input_output_info = None`, PaSh gets
   no answer and treats the command as having side effects, so it never runs it in parallel.
3. **`ParallelizabilityInfoGenerator<Cmd>.py`, the parallelizability class:** the ways PaSh may split
   the command's input and recombine the outputs. An empty list means "do not split". PaSh refuses to
   build a round-robin split unless the merge step simply joins outputs in order (`concatenate`,
   `adj_lines_*`). If a class breaks that rule, it raises an `AssertionError`, and the decision table
   shows "exception".

Several independent sides wrote these files for the same command, by different methods. They are
labelled A, B, C… at random, so the labels tell you nothing about the method. **Side R** is different:
it is PaSh's own hand-written annotation, written by PaSh's authors. Use R as an informed second
opinion, not as ground truth: it can be wrong or incomplete.

The packet folder holds, for each side, its three files (comments and docstrings removed), and
`decision_table.md`. The decision table groups command lines on which every side gives the same answer,
with the groups where the sides differ first. Files are named by position, such as "operand 1" or
"value of -o". The lines come from benchmark scripts and from the lines each side was tested on.

## Rules

- Read only the packet folder you were given and this rubric. Do not open other files or folders, and do
  not try to find out which side is which.
- **Do not run commands.** The machine you are on may not have the same version of the command. Where a
  claim can only be settled by running the command, write it under "Checks to run".
- Judge by what the command actually does (GNU coreutils behaviour on Linux), as far as you know it
  reliably. When unsure, say so and mark the point as a check to run, rather than guessing.
- Be concrete: cite a group from the decision table or a line of a side's code for every claim.
- Say "same" when sides behave the same, even if their code looks different.

## What to write

One file per command, `assessment.md`, in the folder you are told to write to. Start with this front
matter (YAML), filled in:

```yaml
---
command: <cmd>
rubric: 1
assessor_model: <your model ID>
date: <YYYY-MM-DD>
equivalent_groups: [[A, C], [B], ...]   # sides whose answers are the same on every decision-table group
ratings:                                 # one entry per side, R included
  A:
    io_correct: high | medium | low      # how often its read/written answers match the real command
    io_complete: high | medium | low     # how often it gives an answer at all
    split_safe: safe | unsafe | none_offered | broken   # broken = its class raises an exception
    split_coverage: high | medium | low | none          # how much safe splitting it allows
    parser_table: good | gaps | wrong
    confidence: high | medium | low
io_difference_types: [ ... ]             # from the list below, every type you found
needs_running: <number of checks listed>
---
```

Input/output difference types, one per element that differs between two sides:
`operand direction differs`, `operand used by one side only`, `standard input differs`,
`standard output differs`, `option value typed differently`, `kind only` (same direction, a different
PaSh kind such as stream versus other). Add a new type only if none fits, and name it plainly.

Then these sections, in plain language, short:

1. **How each side is built.** One or two sentences per side (or per equivalent group). Is it general
   rules that cover any command line, or a list of specific situations with no answer outside them?
   Does it have a catch-all? What does this mean for lines it was never tested on?
2. **Input/output sets.** For every difference: what it is, which sides are on each side of it, an
   example line, and which side matches the real command, and why. This is the most important section.
3. **Splitting.** Which sides allow splitting where, whether each is safe (output still identical),
   where safe speed is left unused, and any class that breaks PaSh's rule.
4. **Parser table.** Missing or wrongly typed flags and options that change how a line is read, with an
   example of a line read wrongly because of it.
5. **Completeness.** What each side leaves out. Say whether the gap looks like a limit of its method
   (it only answers for situations it saw) or a choice it made.
6. **Checks to run.** Each claim to confirm by running, as a command line, with what each side predicts.
7. **Summary.** Three sentences at most.

## Change log

- v1 (2026-11-11): first version.
