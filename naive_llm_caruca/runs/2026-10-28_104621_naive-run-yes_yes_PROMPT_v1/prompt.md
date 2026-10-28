# Task: describe the shell command `yes` for downstream tools

## Objective

Produce a machine-readable description of the shell command `yes` so that other programs can
understand it without ever running it themselves. Tools for reasoning about shell invocations need to
know two things about a command: its **argument syntax** (the options it accepts, the type of each
option's argument, and the types of its operands), and how a given invocation **behaves** with respect
to its inputs and outputs.

The command's binary is at `/usr/bin/yes`. Its manual page is at `/usr/share/man/man1/yes.1.gz`.

## Deliverable

Write the following into the `output/` directory of this folder.

1. **The syntax description**, `output/yes.py`: the options the command accepts, the type of
   argument each option takes, and the types of its operands. The format is specified in
   [formats/syntax_description.md](formats/syntax_description.md).

2. **The behaviour annotation**, in the form tools consume, under `output/annotation/`:
   - `yes.json`, a table of the command's flags and options;
   - `InputOutputInfoGenerator<Command>.py`, a Python class that, given a parsed invocation, decides
     which arguments are inputs, which are outputs, and whether standard input and output are used;
   - `ParallelizabilityInfoGenerator<Command>.py`, a Python class that, given a parsed invocation,
     decides whether and how its work can be split across parallel copies of the command.

   `<Command>` is the command's name with its first letter capitalised. The format of all three files
   is specified in [formats/annotation.md](formats/annotation.md).

## Examples of finished output

The `samples/` directory holds the complete set for four other commands:

| Command | Syntax description | Annotation |
|---|---|---|
| `tee`  | [samples/tee/tee.py](samples/tee/tee.py)     | [samples/tee/annotation/](samples/tee/annotation/)   |
| `uniq` | [samples/uniq/uniq.py](samples/uniq/uniq.py) | [samples/uniq/annotation/](samples/uniq/annotation/) |
| `grep` | [samples/grep/grep.py](samples/grep/grep.py) | [samples/grep/annotation/](samples/grep/annotation/) |
| `rm`   | [samples/rm/rm.py](samples/rm/rm.py)         | [samples/rm/annotation/](samples/rm/annotation/)     |

## What you may not use

Do not search the web or read anything online: no search engines, no websites, no code repositories.
Work from what is on this machine. Programs that need the network to do their job, such as a package
installer, may still use it.

## Scope

The command to describe in this session is `yes`. Please generate a correct specification
without my intervention, and be certain to test the binary against the specification you generate.
When the files are written, report what you did and anything you are unsure about.
