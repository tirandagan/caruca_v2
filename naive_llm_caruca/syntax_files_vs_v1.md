# Naive LLM: the agent's syntax files against v1's (`rm`, `cut`, `sort`, `convert`)

**Version 0.1, 26 October 2026, draft.** Part of the "Naive LLM" set: every claim below rests on v1's
code, files or git history, the paper, the naive runs' own outputs, or a measurement made for this
document. Scripts, raw results and re-run instructions:
`naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/`.

## What is compared

A command's **syntax file** (also called its grammar) is the Python file that lists the command's
options, the kind of value each option takes, and the files the command operates on. Caruca uses it
to write the command lines it runs and traces, and to check whether real-world command lines fit the
command's known syntax.

For each of four commands there are three syntax files:

| Name used here | File | Who wrote it |
|---|---|---|
| **reference** | v1's `caruca/src/caruca/syntax_specs/<cmd>.py` | v1's authors, corrected by hand over many commits ("Fix ground truths"); v1 scores everything else against it. Last changed: `rm` and `cut` 2025-10-25, `sort` 2024-11-21, `convert` 2024-11-22 |
| **v1 model output** | v1's `outputs/llm-dsl-generation/<cmd>.py` | v1's language-model step, from the command's manual page (GPT-4o in the paper). Committed 2024-11-11 (`rm`) and 2024-12-09 (`cut`, `sort`, `convert`). The paper's syntax-accuracy section reports `sort` as "missing three flags related [to] batch size, compression program, and sorting key", which is exactly this file |
| **agent** | `naive_llm_caruca/runs/*_<cmd>_PROMPT_v1/output/<cmd>.py` | One general-purpose coding agent per command, given the goal, two format descriptions and four example files, with no method. Runs 5 (`rm`), 7 (`cut`), 8 (`convert`) and 9 (`sort`), 20 October 2026, Claude Fable 5.1 at medium effort, Ubuntu 24.04.4 (aarch64) with GNU coreutils 9.4 and ImageMagick 6.9.12-98. Cost $0.80, $1.25, $6.04 and $2.46 |

v1 is at commit `d80324073` throughout.

**`rm` is a copying test, not a discovery test.** The agent was shown v1's reference `rm.py` as one of
its four examples (byte for byte), and `rm` is also one of the four worked examples in v1's own model
prompt. The `rm` comparison therefore shows what the agent *changed*, not what it found unaided. The
other three commands had no example to copy.

All program behaviour quoted below was checked on the real programs: GNU coreutils 9.4 in the `pash`
VM, and ImageMagick 6.9.12-98 in a throwaway copy of the `naive-golden` VM (the version the agent ran).

## In brief

1. **The three files mostly agree on what the options are.** Read with GNU's own option-parsing rules,
   every one of them can read every valid real-world `cut` line (5,856) and `rm` line (24,195). For
   `sort`, the reference and the agent's file read all 5,010 valid lines; v1's model output cannot read
   831 of them (17%), because it leaves out `-k`, the sort-key option.
2. **Where they disagree, the agent's file is usually closer to the installed program.** It found 14
   real `convert` options that neither v1 file lists, avoided a misspelled one both v1 files copy from
   the manual, recorded that `cut` takes exactly one of `-b`/`-c`/`-f`, gave `sort`'s numeric options
   their real ranges, and listed real value sets taken from the program itself. Where it was wrong, it
   was mostly in how it wrote things down, not in what it found.
3. **"Which file is better" depends on which program reads it.** Four of v1's programs read a syntax
   file, and they reward different things:
   - **v1's matcher** (it checks real-world command lines; the paper's real-world reach figure comes from
     it) reports the reference as reading almost every `cut` and `sort` line. Checked word by word,
     though, almost all of those readings are wrong. Only 78 of 5,856 `cut` lines (1.3%) and 2,360 of
     5,010 `sort` lines (47%) are read correctly. The agent's file gets 2,522 (43%) and 4,455 (89%).
     Across the whole real-world collection, with v1's own files for every command, 267,070 of the
     665,631 lines (40%) are counted as read only by taking at least one word as an option it is not.
   - **v1's generator** (it writes the command lines Caruca traces) works best with the reference for
     `cut` and `rm`. It works worst with the agent's file for `cut` and `sort`, because the agent marked
     short options as taking `=`, a convention it copied from v1's own `uniq` example, and the programs
     reject `-b=1`. For `rm`, the agent's correct observation that `rm -f` needs no file makes the file
     optional, and the generator then leaves the file out of 62% of its command lines.
   - **v1's ShellCheck adapter** gets a useful "missing destination" warning for `convert` only from
     v1's model output.
   - **v1's scorer** (the tool behind the paper's syntax-accuracy figure) cannot see most of these
     differences. Seven of eight single-attribute changes we planted scored as a perfect match.
4. **For a program written outside v1** that reads the file by GNU's rules (a completion generator, a
   linter, a parser), the agent's file carries the most usable facts: standard input via `-`, which
   options repeat, real value ranges, real value lists, and `+` forms for `convert`. The reference adds
   one FreeBSD-only option that GNU rejects. v1's model output drops `sort -k`.

## 1. How the files differ

### 1.1 `rm`, `cut`, `sort`: every difference, checked on the program

Options on which all three files agree are not listed (`rm`: 10 of 13 entries; `cut`: 5 of 13;
`sort`: 19 of 32). "`=`" means the file marks the option as written `option=value`
(`flag_followed_by_equals=True`). v1's generator then writes `=` after whichever spelling it uses, and
it always uses the first spelling (section 2.2).

**`rm`**

| Entry | reference | v1 model output | agent | What `rm` 9.4 does | Closest to the program |
|---|---|---|---|---|---|
| `--interactive=` values | never, once, always | same | adds no, none, yes | all six accepted | agent |
| file operand | at least one | at least one | zero or more | `rm -f` with no file succeeds; `rm`, `rm -v`, `rm -i` with no file fail ("missing operand") | neither: the true rule is "at least one unless `-f`", which the format cannot state |
| `--preserve-root` | choices "" and "all", `=` | same | same | bare `--preserve-root` and `--preserve-root=all` accepted; `--preserve-root=` rejected ("unrecognized --preserve-root argument: ''") | all three share the same gap: the empty choice is meant as "bare", but the generator writes `--preserve-root=` |

v1's model output for `rm` is identical to the reference: `rm` is one of the worked examples in v1's
own prompt.

**`cut`**

| Entry | reference | v1 model output | agent | What `cut` 9.4 does | Closest to the program |
|---|---|---|---|---|---|
| how many of `-b`, `-c`, `-f` | any number, 0 to 3 | any number | exactly one (three alternative layouts, one per selector) | two given: "only one list may be specified"; none given: rejected | agent |
| `=` on `-b`, `-c`, `-f` | no | yes | yes | `-b=1` rejected ("invalid byte/character position '=1'"); `--bytes=1` and `-b 1` accepted | reference, for v1's generator |
| `-d` value kind | `Delimiter` (sample values `,` and a two-character newline+tab) | `Char` (a to e), `=` | `Char`, `=` | exactly one character ("the delimiter must be a single character"); `-d=a` rejected | v1 model output and agent on the kind; reference on the `=` |
| `--output-delimiter` | `Delimiter` | `String`, `=` | `Delimiter`, `=` | any string; the long spelling takes `=` | all acceptable |
| `-w` | listed ("# Only FreeBSD") | absent | absent | "invalid option -- 'w'" on GNU | v1 model output and agent, for GNU |
| `-` as a file | not stated | not stated | `-` means standard input | `cut -` reads standard input | agent adds a true fact |
| `-d` and `-s` need `-f` | not stated | not stated | not stated | both rejected without `-f` | none |

**`sort`**

| Entry | reference | v1 model output | agent | What `sort` 9.4 does | Closest to the program |
|---|---|---|---|---|---|
| `-k`, `--key` | six hand-picked sample keys (`1`, `1.2`, `1.2n`, …) | **absent** | free text, `=`, may repeat | `-k 1.2nr` accepted, repeated `-k` accepted; `-k=string` rejected | reference for the generator; agent for "may repeat"; v1 model output loses 831 of 5,010 real lines |
| `--batch-size` | whole number, `=`, sample values −1, 0, 1 | absent | whole number, `=`, minimum 2 | minimum is 2 ("minimum --batch-size argument is '2'") | agent as a description, but see section 2.2: v1's generator then never writes it |
| `--compress-program` | command name | absent | command name, `=` | accepted | reference, agent |
| `-c`, `-C`, `--check` | `-c` = `--check`; `-C` = `--check=quiet` or `--check=silent` | same, without `silent` | `-c`; `-C`; `--check` with an optional value: "", diagnose-first, quiet, silent | `--check` takes an optional value; `--check=` rejected ("ambiguous argument ''") | agent's shape is the program's; its empty choice produces a rejected line, as in `rm` |
| `-S` | whole number, `=` | size (`1k`, `1m`, …) | size, `=` | `-S 1k` accepted; `-S=1k` and `-S=1` rejected | v1 model output |
| `-t` | `Delimiter` | `Delimiter` | `Char`, `=` | one character ("multi-character tab"); `-t=a` is read as two characters | agent on the kind; reference and model output on the `=` |
| `-T` | file | file | file, `=`, may repeat | repeat accepted; `-T=d` silently uses a folder named `=d` | reference and model output for the generator; agent for "may repeat" |
| `-o` | file | file | file, `=` | `-o=out` silently writes a file named `=out`; given twice: "multiple output files specified" | reference and model output |
| `--parallel` | whole number, `=`, samples −1, 0, 1 | whole number, samples −1, 0, 1 | whole number, `=`, minimum 1 | 0 and −1 rejected | agent |
| `-y` | absent | absent | no-value flag | accepted (obsolete); a following all-digit word is swallowed (`sort -y 5` ignores `5`) | agent, approximately |
| `--random-source`, `--files0-from` | file | file | file, `=`; `-` means standard input for `--files0-from` | long spellings with `=` accepted | all acceptable; agent adds a true fact |

### 1.2 `convert`

| | reference | v1 model output | agent |
|---|---|---|---|
| Option entries | 252 (four options listed twice: `-clip`, `-clip-mask`, `-clip-path`, `-flatten`) | 252 (same four twice) | 426 |
| Distinct options (`-x` and `+x` counted once) | 248 | 248 | 261 |
| `+` forms | none | none | 261 (96 as alternative spellings, 165 as separate entries) |
| File operands | one or more files | exactly one, then exactly one | any number of inputs, then exactly one output |

- **Options only the agent lists (14):** `-average`, `-cache`, `-concurrent`, `-connected-components`,
  `-duration`, `-gaussian`, `-kuwahara`, `-linewidth`, `-local-contrast`, `-maximum`, `-minimum`,
  `-noop`, `-recolor`, `-rotational-blur`. All 14 exist in ImageMagick 6.9.12-98: none was reported as
  an unrecognized option. Ten were accepted outright; four failed only because the sample value v1's
  generator writes for a text value, the word `string`, is not a valid value.
- **Option only the v1 files list (1):** `-connected-component`, the manual's spelling. ImageMagick
  rejects it ("unrecognized option"); the agent's `-connected-components` is accepted.
- **`-view`:** both v1 files make it a no-value flag, so it takes the output file name as its value and
  the line fails. The agent's version, which takes a value, is accepted.
- **Kinds of value** differ on 108 of the 247 shared options, and value lists on 130 (counting the
  sample values each kind implies; see section 2.2, which measures what the differences do).
- **Two-argument options** (`-annotate`, `-distort`, `-evaluate`, `-morphology` and seven more): the
  format has no way to state a second argument. The agent noted this in a comment in its file and gave
  the first argument correctly; the v1 files give the word `string`. Section 2.2 shows that all three
  fail.

## 2. Four programs read these files

Four programs in v1 load a syntax file (found by searching v1 for every call that loads one):

| Program | What it uses the file for | Where in v1 |
|---|---|---|
| matcher (`caruca oracle`) | checks whether a real-world command line fits the syntax; the paper's real-world reach figure | `oracle.py`, `ir/syntax.py` (`could_match`) |
| generator (`caruca generate`, used by `caruca trace`) | writes the command lines Caruca runs and traces | `cli/generate.py`, `ir/syntax.py` (`syntax`, `to_concrete_string`) |
| ShellCheck adapter (`caruca annotate shellcheck`) | decides whether to emit a "missing destination" check | `annotator/__init__.py`, lines 60–106 (added 2025-12-21) |
| scorer (`eval/cmp_specs.py`) | scores a model-written file against the reference; the paper's syntax-accuracy method | `eval/cmp_specs.py` |

PaSh does not read this file; it reads the separate behaviour annotation.

### 2.1 The matcher: reading real-world command lines

**What we ran.** v1's matcher over every line of v1's real-world collection
(`eval/user-scripts/invocations.txt`: 665,628 lines, which v1's matcher reads as 665,631 because three
of them contain a carriage return) whose first word is `rm`, `cut` or `sort`
(24,260, 5,909 and 5,011 lines; the collection has no `convert` lines), once with each file. With the
reference files our run gives exactly v1's committed results (24,094, 5,890 and 5,011 lines fully read,
and the same counts at every guessing level), so it is a faithful replay.

**How the matcher treats a file.** Four behaviours, read in `ir/syntax.py` and `oracle.py` and seen in
the runs:

1. An option that takes a value and is **not** marked `=` accepts *any* word as its own spelling. The
   word does not have to be the option, or start with it. The matcher records this as a "string" guess
   and moves on. So with the reference, `sort -u` is read as `sort --random-source`, and
   `cut -d ' ' -f 2` is read as `-b`, then `-c`, then `-d`, then `-f`, one option per word.
2. An option marked `=` takes its value only when the value is attached (`-d,` or `-d=,`). With a space
   (`-d ,`) the option is read as having no value, and the value is left behind and read as a file.
3. A value given after `=` must be one of the value kind's few sample values. So `cut --fields=2` is not
   read, because 2 is not among `1`, `1-`, `1-2`, `-2`, `1,3`.
4. Positions are read once, in order: options first, then files. Once a word has been read as a file,
   the matcher does not go back to the options. Alternative layouts are walked one after another as
   one long list, not tried one at a time, so a rule expressed by alternatives (the agent's "exactly
   one of `-b`, `-c`, `-f`") is not used. In this collection only two lines break that rule
   (`cut -d' ' -f4 -f6`, twice), and the matcher accepts them with every file.
5. A lone `-` (standard input) is never accepted as a file, whatever the file says about `-`.

**Is a "fully read" line read correctly?** We recorded which entry of the file consumed which word,
and compared that with how the program itself reads the line. The program's reading was computed by
emulating GNU's option parser (the `getopt_long` routine coreutils uses), with each command's coreutils
9.4 option table. Lines the program's parser rejects are left out of the count below: 19 `cut` lines
that cannot be split into words, 34 `cut` lines using FreeBSD's `-w`, 1 `sort` line and 65 `rm` lines.

| Lines GNU's parser accepts | reference | v1 model output | agent |
|---|---|---|---|
| **`cut`, 5,856 lines**: read correctly | **78 (1.3%)** | 2,524 (43.1%) | 2,522 (43.1%) |
| read, but wrongly | 5,778 | 695 | 2,522 |
| not read | 0 | 2,637 | 812 |
| **`sort`, 5,010 lines**: read correctly | 2,360 (47.1%) | 2,668 (53.3%) | **4,455 (88.9%)** |
| read, but wrongly | 2,650 | 2,342 | 402 |
| not read | 0 | 0 | 153 |
| **`rm`, 24,195 lines**: read correctly | 24,094 (99.6%) | 24,094 | 24,094 |
| not read | 101 | 101 | 101 |

"Read correctly" means the same options with the same values, and the same files in the same order,
as the program's own reading. The 101 unread `rm` lines are the same for all three files; 75 of them use
`--` (end of options), which none of the files describes.

What goes wrong, by file:

- **Reference:** almost every wrong reading comes from behaviour 1. For `cut`, all 5,778 wrong readings
  rely on it, and so do all 2,650 for `sort`.
- **v1 model output and agent:** behaviour 2. `cut -f 1` is read as "`-f` with no value, and a file
  called `1`"; `cut -d "." -f1` as "`-d` with no value, and a file called `.`". In the agent's `sort`
  file, 382 of the 402 wrong readings are `-k` read this way (`sort -k 2` → "`-k` with no value, file
  `2`").
- **Unread lines** combine behaviours 2 and 4. For `cut`, 690 lines stop at a `-d` written after
  `-f 1`: the `1` was read as a file, so the matcher has moved on to files and cannot go back for `-d`
  (example: `cut -f 1-2 -d '.'`). Both v1's model output and the agent lose these same 690 lines. Then
  76 agent lines contain a lone `-` (behaviour 5), and the remaining 46 have a value starting with `-`
  (`cut -b -2`) or a long option whose value is not a sample value (`--delimiter=';'`, behaviour 3).
  v1's model output also leaves 1,833 lines unread at `-f`, which in its file has no layout to fall back
  to. The agent's 153 unread `sort` lines stop at `-k` (84), a lone `-` (25), `-t` (16), `-o` (11) and
  others (17).

**What the files themselves know.** To separate the files from the matcher, we read the same lines a
second way: with GNU's parsing rules, but taking the list of options, and whether each takes a value,
from each file in turn.

| Lines GNU's parser accepts | reference | v1 model output | agent |
|---|---|---|---|
| `cut`, 5,856 | 5,856 | 5,856 | 5,856 |
| `sort`, 5,010 | 5,010 | 4,179 (831 unreadable: every one uses `-k` or `--key`) | 5,010 |
| `rm`, 24,195 | 24,195 | 24,195 | 24,195 |

So the gaps in the first table come from how the matcher interprets the files, not from what the files
know. The one real gap in knowledge is v1's model output missing `-k`.

**Across the whole collection.** With v1's own files for every command, the matcher fully reads 650,890
of the 665,631 lines. At the level the paper calls string normalization it reads 631,937, and before that
level 123,174. The paper's figures are 651,733, 632,780 and 122,816, on a collection 840 lines larger. Of
the 631,937, **267,070 (42%; 40% of all lines) are read only by taking at least one word as an option it
is not** (behaviour 1). This can be told apart mechanically, because the matcher records the option's
spelling for this guess and a value list for an unknown-value guess. The paper describes string
normalization only as the second kind ("the rest of the arguments for which Caruca only has a string
type"). The largest contributors are `test` (193,623 lines), `mkdir` (15,008), `cp` (12,861), `cut`
(5,812), `mv` (4,953), `ls` (3,939) and `sort` (2,651). For `cut` and `sort` we checked every such
line against the program's own reading, and all were wrong. For the other commands we did not build the
program's reading, so we can say only that each such line has at least one word assigned to the wrong
option.

### 2.2 The generator: writing command lines to trace

**What we ran.** Each option entry of each file, rendered exactly as v1's generator writes it (v1's own
code, one value per option, plain paths), placed in the smallest command line the program accepts, and
run once on the real program in a fresh temporary folder. For example, `cut -f 1 <option> in.txt` for a
non-selector option of `cut`, and `convert in.jpg <option> out.png` with v1's own sample image. A form
counts as accepted when the program exits with 0.

| Rendered forms accepted | reference | v1 model output | agent |
|---|---|---|---|
| `rm` | 14 of 15 | 14 of 15 | 17 of 18 |
| `cut` | **24 of 26** | 7 of 27 | 8 of 28 |
| `sort` | **44 of 53** | 41 of 44 | 37 of 53 (40 exit with 0, but 3 of those silently use the wrong file, see below) |
| `convert` | 438 of 526 (83%) | 460 of 566 (81%) | 998 of 1,207 (83%) |

What decides these results:

- **`=` after a short spelling.** v1's generator writes `=` after the first spelling, so `-b=1`,
  `-d=a`, `-t=a`, `-S=1k`, `-k=string`. GNU programs read the `=` as part of the value and reject
  the line. For `-o=file` and `-T=dir` they do not reject it but silently use a file or folder whose
  name starts with `=`. This one convention accounts for all 20 rejected agent forms in `cut`, and for
  11 of its 13 rejected `sort` forms (`-o`, five `-S`, five `-t`) plus the 3 silent ones. Of the other
  two, `-k=string` also has an invalid sample value and `--check=` is an empty choice (below). v1's
  model output uses the convention in `cut`, and the reference uses it on `sort -S`. The agent took the convention from its examples: v1's reference
  `uniq.py`, one of the four, marks `-f`, `-s` and `-w` this way.
- **Sample values.** v1's generator writes a few fixed values per kind, so the kind chosen decides the
  test values:

  | Kind | Sample values |
  |---|---|
  | `Delimiter` | `,` and a two-character newline+tab (rejected by `cut -d` and `sort -t`) |
  | `Char` | `a` to `e` |
  | whole number | −1, 0, 1 (all three rejected by `--batch-size`) |
  | `Geometry` | `50%`, `100x100` |
  | `String` | the literal word `string` |

  In `convert`, for the 93 shared options whose results differ between files, the agent's file does as
  well as the reference on 76, better on 11 and worse on 6. It does better than v1's model output on 57
  and worse on 34. The agent wins where it listed real values taken from the program (`-list` with 74
  values, `-evaluate-sequence` 37, `-debug` 20, `-layers` 16). It loses where it gave a numeric option
  the `String` kind (`-delay`, `-pointsize`, `-kerning`), which the v1 files typed as numbers. Against
  the reference, v1's model output does better on 30 options, where it typed as numbers what the
  reference left as text (`-rotate`, `-gamma`, `-fuzz`). It does worse on 49, mostly size or geometry
  options that it typed as text (`-resize string` is rejected).
- **A minimum with no maximum.** The agent's `--batch-size` says "minimum 2". v1's default maximum is
  1, so the range of sample values is empty and v1's generator never writes the option at all.
- **An empty choice meaning "no value".** Used for `rm --preserve-root` (by all three files) and the
  agent's `sort --check`. v1's generator writes it as `--preserve-root=` and `--check=`, both rejected.
- **Two-argument options** (11 in `convert`): all fail in all three files. The program takes the output
  file name as the missing second argument (`invalid argument for option '-evaluate': out.png`).
  Another 29 shared `convert` options fail in all three files for other reasons: they need a second
  image or other setup (`-composite`, `-clut`, `-clip`), or every file gives an invalid sample value
  (`-affine string`).

**An optional file shares the per-line budget.** v1's generator limits how many optional entries go on
one command line (its `--max-count` setting), and an optional file counts against that limit just as
an option does. The agent made `rm`'s file optional (correctly, since `rm -f` needs none), and the
generator then leaves the file out of most lines:

| `rm`, distinct generated lines | reference | v1 model output | agent | agent lines with no file |
|---|---|---|---|---|
| 1 option per line | 32 | 32 | 21 | 19 (90%) |
| 2 | 234 | 234 | 194 | 156 (80%) |
| 3 | 1,044 | 1,044 | 1,068 | 756 (70%) |
| 4 (v1's shipped setting) | 3,204 | 3,204 | 3,978 | 2,466 (62%) |

A line with no file deletes nothing. At one option per line we ran all 19 on `rm`. Sixteen fail (15
with "missing operand", one on the empty `--preserve-root=` value), and the other three (`--help`,
`--version`, `-f`) succeed without removing anything.

Whole command lines, measured earlier on these same files (addendum on the naive-LLM runs, sections 3.3
and 4.5): at four options per line, `cut` command lines that do real work number 360 for the reference
and 0 for both v1's model output and the agent. At two options per line, 70%, 85% and 53% of `sort` lines
are accepted. For `convert` at one option per line, lines with both an input and an output number 0 of
1,052 for the reference, 2,272 of 2,272 for v1's model output and 4 of 2,422 for the agent.

### 2.3 The ShellCheck adapter

v1's newest commit (2025-12-21) adds a ShellCheck check that warns when a command is given too few files,
as in `cp a` with no destination. v1 builds it from the syntax file: a layout needs at least two separate
file entries that together require two or more files. Applying v1's own rule to all twelve files, only
v1's model-written `convert` file qualifies (exactly one input, then exactly one output). The reference
(one entry, one or more files) and the agent's file (any number of inputs, then one output, so only one
file required) produce no check. On the program, `convert in.jpg` with one file and no options fails
and only prints the version banner, so the check would be a correct warning that the other two files
lose. For `rm`, `cut` and `sort`, no file produces the check.

### 2.4 The scorer

v1's scorer (`eval/cmp_specs.py`, current since its 2024-11-10 rewrite) on the real files, scoring each
against the reference:

| Differences counted | `rm` | `cut` | `sort` | `convert` |
|---|---|---|---|---|
| v1 model output | 0 | 3 | 3 | 63 |
| agent | 1 | 4 | 4 | 228 |

**What the scorer can see.** We changed one attribute at a time in copies of the reference and scored
each copy:

| Change | Counted? |
|---|---|
| file operand from "at least one" to "zero or more" | no |
| an alternative spelling removed (`--force`) | no |
| `=` marker switched off (`--interactive`) | no |
| a whole number becomes a size (`sort -S`) | no |
| a minimum added (`--batch-size`) | no |
| a whole number becomes a file (`--parallel`) | no |
| a no-value flag becomes an option taking a file (`rm -v`) | no |
| a file operand becomes free text | yes (1) |

The scorer counts a missing or extra option, and a value list whose contents differ. It never reaches
the line that would compare the other attributes. That line sits after a check that skips it
whenever no difference has been found yet (lines 119–121), and no earlier step sets that flag except
the value-list comparison. It also pairs the two files' layouts in order and stops at the shorter list,
so the agent's three-layout `cut` file is scored on its first layout only: `-c` and `-f` are reported
"missing". Four of the agent's "missing" `convert` options are the reference's second copies of
options it lists twice, and the fifth is the misspelled `-connected-component`. The October 2024
version of the scorer compared every attribute, but it paired options by position and also compared
each entry's random internal identifier, so it was unreliable in another way.

The scorer's numbers above are therefore not a guide to which file is closer to the program. Nearly
all of the differences in section 1 are invisible to it.

## 3. Which is better?

**As a description of the installed program,** the agent's files are the most accurate of the three for
`cut`, `sort` and `convert`, and its `rm` changes are all true to the program. It got this from asking
the programs themselves, not only their manuals. Its mistakes are of two kinds:

- *Conventions copied from v1's examples that v1's own programs handle badly:* `=` on short
  spellings (from `uniq.py`), an empty choice for "no value" (from `rm.py`), and a minimum with no
  maximum (the format document mentions both, but not the default maximum of 1).
- *A few kind choices:* `String` for some of `convert`'s numeric options, and plain text for `sort -k`.

v1's reference has the opposite profile. It is weaker as a description (FreeBSD's `-w` in a GNU file,
a two-character delimiter sample, no "exactly one selector" rule, `-connected-component`, `-view` as a
flag) but tuned to v1's generator: no `=` on short spellings in `cut`, hand-picked valid `-k` keys.
v1's model output sits between them, and is the only one of the three missing a real `sort` option.

**As input to each of v1's programs:**

| Program | Best file | Why |
|---|---|---|
| matcher | agent (`sort`); agent = v1 model output (`cut`); all equal (`rm`) | the reference "reads" the most lines but almost all of its readings are wrong |
| generator | reference (`cut`, `rm`); mixed (`sort`); agent ≈ reference (`convert` options) | `=` on short spellings, empty choices, and an optional file sharing the line budget cost the agent |
| ShellCheck adapter | v1 model output (`convert`) | its two required files trigger a correct missing-destination warning |
| scorer | (not meaningful) | the scorer cannot see most attributes |

**Where a program reading each file would struggle:**

- *Reference:* a parser that trusts it would accept FreeBSD's `cut -w` and the misspelled
  `-connected-component`, treat `-view` as taking no value, and never learn that `cut` needs exactly one
  selector or that `-` means standard input. v1's own matcher reads it leniently, so its reach figures
  overstate how much of the real world it actually reads.
- *v1 model output:* cannot read any `sort` line with a sort key (17% of real `sort` lines), and its
  `=` on `cut`'s short options produces only rejected test lines.
- *Agent:* a reader that follows v1's `=` convention literally will write `-b=1` and misread `-d ' '`;
  its `rm` file lets test generators drop the file; its `--batch-size` disappears from v1's
  generator; and a consumer that reads the file as data rather than running it has more work to do,
  since its `cut` file builds the three layouts with helper functions.

## 4. What this suggests

Each item extends something Caruca already has.

1. **Matcher:** let a value-taking option match only its own spellings, accept both attached and
   separate values whatever the `=` marker says, allow options after files, accept `-` where the file
   says it means standard input, try alternative layouts one at a time, and check required files. Report the reach figure together with a check of the readings against the
   program's own parsing, as done here for three commands.
2. **Scorer:** compare every attribute, and every layout, so that differences like those in section 1
   count.
3. **Generator:** write `=` only with a long spelling; count optional files separately from options;
   when only a minimum is given, take values from the minimum upward.
4. **Format:** add a way to say "at least one file unless `-f`", "this option takes two values", and
   "this option's value is optional and attached with `=`" (as `--check[=WORD]`). Without them, all
   three authors, human and model alike, write workarounds that v1's programs then mishandle.

## 5. What this does not claim

- One run per command, with one model and prompt version 1. Not repeated, so nothing here measures
  run-to-run variation.
- `rm` was shown to the agent as an example, so its `rm` file is a copy with changes, not a discovery.
- The program's reading of each real-world line comes from an emulation of GNU's option parser over the
  coreutils 9.4 option tables. It does not apply rules beyond option syntax (such as `cut`'s
  one-selector rule), and it treats shell variables (`$file`) as literal words.
- The generator test runs each option alone in one small context. A form that "exits with 0" may still
  misbehave (three silent cases found and counted). Options needing a second image fail for every file
  and say nothing about the files.
- The whole-collection count of 267,070 lines says each of those lines has at least one word assigned to
  the wrong option. Whether a correct reading would still match a command line Caruca explored was
  checked only for `cut`, `sort` and `rm`.
- Nothing here re-scores the paper's syntax-accuracy figure. Section 2.4 says what the current scorer
  can and cannot see.

## Evidence

- Scripts, results, and how to re-run: `naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/`
  (`README.md` there). Key results: `three_way_alignment.txt`, `matcher_read_correctness.txt`,
  `gnu_rules_reading.txt`, `matcher_levels.txt`, `corpus_split.json`, `probe_core.jsonl`,
  `probe_convert.jsonl`, `scorer_results.txt`, `scorer_blind_spots/`.
- v1 at `d80324073`. Files: `caruca/src/caruca/syntax_specs/`, `outputs/llm-dsl-generation/`,
  `caruca/src/caruca/oracle.py`, `caruca/src/caruca/ir/syntax.py` (value kinds and sample values, lines
  263–421), `caruca/src/caruca/ir/mixin.py` (line 24, the `=`), `caruca/src/caruca/annotator/__init__.py`
  (lines 60–106), `eval/cmp_specs.py` (lines 82–129), `eval/user-scripts/invocations.txt`,
  `oracle_results.txt`, `command_counts/`.
- Agent files: `naive_llm_caruca/runs/2026-10-20_121932_naive-run-rm_rm_PROMPT_v1/`,
  `…_135253_naive-run-cut_cut_PROMPT_v1/`, `…_160340_naive-run-sort_sort_PROMPT_v1/`,
  `…_135842_naive-run-convert_convert_PROMPT_v1/`; each run's `analysis/analysis.md` covers how the
  agent worked.
- Programs: GNU coreutils 9.4 on Ubuntu 24.04.4 (aarch64, `pash` VM); ImageMagick 6.9.12-98 Q16
  (aarch64, a clone of `naive-golden`, deleted after use). v1's Python 3.12.9 virtual environment on
  the Mac for the matcher, generator and scorer.
- Paper: `ai_docs/refs/caruca_white_paper.md`, the syntax-accuracy section (the three missing `sort`
  options) and the real-world reach section (figures and the description of string normalization).
