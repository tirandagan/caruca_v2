<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!-- caruca_v2 analysis document. Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
     Licensed under the PolyForm Noncommercial License 1.0.0
     https://polyformproject.org/licenses/noncommercial/1.0.0
     Noncommercial use only. Commercial use is prohibited. -->
<!-- ATTRIBUTION-NOTICE:END -->

# Latest findings

**What this is.** One dated list of what the project has found so far, newest first. Each bullet says
what was found in plain words, gives the number together with what it is out of, and links to the
document that holds the details and the evidence. When a later finding corrects an earlier one, both
stay, and the earlier one says so.

**How the dates work.** The heading date is the day the finding was made: a run, a measurement, or a
reading of the code. The time in each bullet is when the finding was written into the linked document,
taken from git. "Not yet committed" means the file's last save time instead. Where a finding was written
up on a later day than it was made, the bullet gives both dates.

**The four areas, as tagged on each bullet:**

- **Caruca (v1):** the original tool (Lamprou et al., arXiv:2510.14279) at commit `d80324073`. These
  findings are about its code, its files and its paper.
- **v2 pipeline:** this project's rebuild of Caruca's four steps (write the syntax description,
  generate test command lines, run and trace them, write the behaviour description), each step done
  by a prompted language model (GPT-4o). Run in September 2026; those runs are archived in
  `eval/_archive/2026-10-13_parity/`.
- **Naive LLM:** a general-purpose coding agent (Claude Code, model Claude Fable 5.1) given only the
  goal, two format descriptions and four finished examples, run once per command in a throwaway
  virtual machine, from October 2026.
- **PaSh:** the shell-script parallelizer that reads Caruca's behaviour descriptions.

**Adding to this file.** Put each new finding at the top of its day's section, with the time it was
written into its document and a link to the section that holds the evidence. Never edit an old bullet
to change its number: add a new bullet and mark the old one "corrected on <date>".

## 2026-10-27

- **13:03, not yet committed · Naive LLM · running time.** Caruca's paper projects runs of up to
  123.7 days (`test`) and about 75 years (`convert`) at four options per command line, because Caruca
  traces every combination of options, sample values and file situations, with repeats.
  - Counted with Caruca's own code and answer key, at up to four options per line: `sort` needs
    7,814,222 test runs and `convert` 229,656,055,750.
  - The agent ran each program 27 (`rm`) to about 6,800 (`convert`) times, in sessions of 1 to 21.5
    minutes of active time. It chooses its tests instead of enumerating them.
  - The speed is the method's, not the file's: Caruca fed the agent's `convert` file would need about
    3.5 trillion runs.
  - The agent also tests far less and records no file activity. →
  [Observations, "Running time"](../../naive_llm_caruca/observations.md#running-time-why-carucas-projections-reach-months-and-the-agent-takes-minutes)
- **12:24 (scored), not yet committed · Naive LLM · accuracy.** Checked fact by fact against the real
  program, the agent's syntax files are about level with Caruca's, slightly ahead on `cut`.
  - `cut`: the agent gets 68 of 76 facts right (89%), Caruca's answer key 61 of 72 (85%), Caruca's GPT-4o
    63 of 76 (83%).
  - `sort`: 181 of 230 (79%), 172 of 220 (78%) and 157 of 204 (77%).
  - `rm`: 58 of 60 (97%), 59 of 60 and 59 of 60 (98%). The agent was shown Caruca's `rm` file as an
    example.
  - `binwalk`, which has no Caruca file: 326 of 337 (97%).
  - With one agent run per command, these are observations, not verdicts.

  → [Observations, "Scores"](../../naive_llm_caruca/observations.md#scores) ·
  [Task 018, "5"](../tasks/018_naive_vs_caruca_syntax_scoring.md#5-results-for-the-four-commands-2026-10-27)
- **12:24 (scored), not yet committed · Naive LLM · generator use.** The agent's files fit Caruca's own
  test-line generator worst. Generated lines doing real work (answer key / Caruca's GPT-4o / agent):
  `cut` 15 of 29 / 0 of 30 / 0 of 240; `sort` 41 of 56 / 38 of 47 / 33 of 56; `rm` 26 of 32 / 26 of 32 /
  3 of 21. The causes are `=` after short options and, for `rm`, an optional file that Caruca's generator
  leaves out. →
  [Observations, "Fit with Caruca's current programs"](../../naive_llm_caruca/observations.md#fit-with-carucas-current-programs)
- **12:24 (scored), not yet committed · Naive LLM · real-world reach.** Read with GNU's own option rules,
  the agent's files and Caruca's answer key both read every valid real-world line checked: `cut` 5,856,
  `sort` 5,010 and `rm` 24,195. Caruca's GPT-4o file reads 4,179 of the 5,010 `sort` lines, because it has
  no `-k`. →
  [Observations, "Fit with Caruca's current programs"](../../naive_llm_caruca/observations.md#fit-with-carucas-current-programs)
- **12:24 (scored), not yet committed · Caruca (v1) and Naive LLM · accuracy.** None of the syntax files
  states which options cannot be combined.
  - `sort` refuses 39 pairs of the options in the answer key, 40 with the agent's extra `-y` (for example
    `--debug` with `-c`). No file
    states any of them; the one rule fact each file gets right is that a line with no options is valid.
  - For `cut`, Caruca's answer key and GPT-4o file encode none of its 7 pair rules. The agent's file
    encodes 3: only one of `-b`, `-c` and `-f` at a time. It misses that `-d` and `-s` need `-f`.
  - Neither Caruca file says that `-` means standard input for `cut` or `sort`; the agent's files do.

  → [Observations, "Headline"](../../naive_llm_caruca/observations.md#headline-facts-checked-against-the-real-program)
- **12:28 (correction), not yet committed · Caruca (v1).** Caruca's JSON converter (`save/transform.py`)
  keeps the *most conservative* label when it merges cases, not the most permissive. A memory note had
  it backwards; task 012 was right. →
  [Task 012, "1.2"](../tasks/012_pash_downstream_study.md#12-why-nothing-plugs-into-pash-today)

## 2026-10-26

- **19:36, not yet committed · Caruca (v1) · real-world reach.** Caruca's real-world matcher counts a
  command line as "read" even when it has taken a word as an option it is not. It lets any word stand
  in for any option that takes a value. Over Caruca's whole collection of real shell-script lines, using
  Caruca's own syntax files, 267,070 of 665,631 lines (40%) are counted as read only that way. For `cut`
  and `sort`, every such reading was checked against GNU's own option rules, and every one was wrong:
  with Caruca's own `cut` file, 78 of 5,856 valid lines are read correctly although all 5,856 count as
  read. →
  [Syntax files vs v1, "2.1 The matcher"](naive_llm_syntax_files_vs_v1.md#21-the-matcher-reading-real-world-command-lines)
  · same mechanism found independently in
  [task 018, "4.2"](../tasks/018_naive_vs_caruca_syntax_scoring.md#42-v1s-matcher-accepts-any-word-as-any-value-taking-option)
- **19:36, not yet committed · Caruca (v1) · accuracy.** The script behind the paper's
  syntax-accuracy figure (`eval/cmp_specs.py`) misses most kinds of difference. Of 8 single changes
  planted in copies of Caruca's reference files, it noticed 1 (a file argument turned into free text).
  It missed, for example, "at least one file" changed to "zero or more", a removed alternative
  spelling, and a number turned into a file. It also scores only the first of a file's alternative
  layouts. →
  [Syntax files vs v1, "2.4 The scorer"](naive_llm_syntax_files_vs_v1.md#24-the-scorer)
- **19:36, not yet committed · Naive LLM · generator use.** Each option, written exactly as Caruca's
  test-line generator writes it, was run once on the real program in the smallest valid command line.
  Forms the program accepted (Caruca's reference / Caruca's GPT-4o file / agent): `cut` 24 of 26 /
  7 of 27 / 8 of 28; `sort` 44 of 53 / 41 of 44 / 37 of 53; `rm` 14 of 15 / 14 of 15 / 17 of 18.
  The agent's habit of writing `=` after short options (`cut -b=1`), copied from one of Caruca's own
  example files, causes all 20 of its rejected `cut` forms. →
  [Syntax files vs v1, "2.2 The generator"](naive_llm_syntax_files_vs_v1.md#22-the-generator-writing-command-lines-to-trace)
- **19:36, not yet committed · Naive LLM · generator use.** The agent correctly made `rm`'s file
  optional, since `rm -f` needs none. But Caruca's generator charges an optional file against the same
  per-line budget as options, so 2,466 of the 3,978 distinct `rm` lines it generates from the agent's
  file (62%) name no file and delete nothing. →
  [Syntax files vs v1, "2.2 The generator"](naive_llm_syntax_files_vs_v1.md#22-the-generator-writing-command-lines-to-trace)
- **19:36, not yet committed · Caruca (v1) · downstream.** Caruca's newest output adapter, for the
  ShellCheck shell linter (added 2025-12-21), warns about a missing destination file only when a syntax
  file requires two or more separate files. Of the 12 files compared (3 per command for `rm`, `cut`,
  `sort` and `convert`), only Caruca's GPT-4o `convert` file triggers it. →
  [Syntax files vs v1, "2.3 The ShellCheck adapter"](naive_llm_syntax_files_vs_v1.md#23-the-shellcheck-adapter)
- **19:31, not yet committed · Caruca (v1) · tooling.** Caruca's `trace` command ignores its option for
  loading a syntax file from another folder, so it cannot trace an outside file. Its count-only mode
  also ignores the options-per-line limit: three different `cut` files all gave 3,483,648, the size of
  Caruca's default set. →
  [Task 018, "4.1"](../tasks/018_naive_vs_caruca_syntax_scoring.md#41-v1s-trace-command-cannot-trace-an-outside-syntax-file)
- **19:14 (run start) · Naive LLM · time and cost.** Run 10 (`dirname`): 57 seconds, $0.88 at list
  price, 5 tool calls. Across runs 4 to 10 (seven commands, no web access): 57 to 1,291 seconds per
  command (mean 333) and $0.80 to $6.04 (mean $2.30). →
  [README, "Observed, run 10"](../../naive_llm_caruca/README.md#prompt_v1--the-bare-task) ·
  [Addendum, "1.2 The runs"](white_paper_addendum_naive_llm.md#12-the-runs)

## 2026-10-20

- **16:45 · Naive LLM · PaSh.** Without being asked, the agent wrote the step that merges sorted pieces
  back together for `sort`, and checked it on 20 option sets: every result matched. The paper places
  that step outside Caruca's scope. But inside PaSh's own code its `sort` description gave no
  parallelization answer for 6 of the 12 invocations tested, every ordinary one such as `sort a.txt`.
  PaSh rejects that pairing of splitter and merger, and hides the error. The agent had tested only
  against stand-ins it wrote itself. →
  [Addendum, "4.4"](white_paper_addendum_naive_llm.md#44-the-consumers-own-code-as-the-check)
- **16:45 · Naive LLM · agent behaviour.** Unprompted, the agent rebuilt Caruca's own "can this command's
  work be split?" test for `cut`: split a file into pieces, run on each, join, compare with one run.
  All 5 option sets matched. Its PaSh option tables for `cut` and `sort` match PaSh's own hand-written
  ones option for option, which it never saw (they are public, so training data may play a part). →
  [Addendum, "4.3"](white_paper_addendum_naive_llm.md#43-parallelizability-the-split-test-and-a-merge) ·
  [Addendum, "4.2"](white_paper_addendum_naive_llm.md#42-the-agents-pash-files-against-pashs-own)
- **16:45 · Caruca (v1) · PaSh.** Caruca's committed PaSh description of `sort` calls all 6 of its cases
  "stateless" (safe to split and simply join), which is false for `sort`. The file dates from
  2024-12-08; the check that would reject that label was added to Caruca on 2025-12-21. Caruca's
  tracing was not re-run to confirm. →
  [Addendum, "4.3"](white_paper_addendum_naive_llm.md#43-parallelizability-the-split-test-and-a-merge)
- **16:45 · Naive LLM and Caruca (v1) · accuracy.** For `convert` (ImageMagick), both of Caruca's syntax
  files list exactly the manual's 248 options. The program accepts 261, which the agent found by trying
  352 words from ImageMagick's library: one manual option is a misspelling the program rejects, one
  option both Caruca files treat as taking no value actually takes one, and at least 10 working
  options are in neither the manual nor the program's help text. →
  [Addendum, "3.2"](white_paper_addendum_naive_llm.md#32-where-the-syntax-came-from)
- **16:45 · Caruca (v1) · generator use.** At its default settings, Caruca's generator makes 1,052
  distinct `convert` lines from Caruca's own reference file, and none of them has both an image to read
  and a file to write, which `convert` needs in order to convert anything (`convert -resize 50% f.jpg`
  answers "no images defined"). From the agent's file, 4 of 2,422 do; from Caruca's GPT-4o file, 2,272
  of 2,272. →
  [Addendum, "3.3"](white_paper_addendum_naive_llm.md#33-option-order-and-carucas-generator)
- **16:45 · PaSh.** PaSh stops reading options at the first file name, so in
  `convert in.png -resize 50% out.jpg` the words `-resize` and `50%` reach the description as input
  files. →
  [Addendum, "3.4"](white_paper_addendum_naive_llm.md#34-what-pash-receives)
- **16:45 · Naive LLM and Caruca (v1) · generator use.** At Caruca's shipped limit of 4 options per
  line, Caruca's reference `cut` file yields 360 lines that do real work out of 11,651 distinct lines;
  Caruca's GPT-4o file 0 of 15,042; the agent's file 0 of 13,222. Both model files write `=` after
  short options (`cut -d=a`), which `cut` rejects. The agent copied that convention from Caruca's own
  `uniq` reference file, where it is also wrong (`uniq -f=1` is rejected). →
  [Addendum, "4.5"](white_paper_addendum_naive_llm.md#45-the-syntax-file-as-input-to-carucas-generator)
- **16:35 · Naive LLM · accuracy.** `binwalk` (a firmware scanner, not one of Caruca's 120 commands):
  its manual describes version 2.3.2 with 49 options; the installed program reports 2.3.3 and accepts
  51; the package is 2.3.4. The installed `binwalk` is a Python script, and the agent took its syntax
  from binwalk's own option table rather than the manual. →
  [Addendum, "2.2"](white_paper_addendum_naive_llm.md#22-where-the-syntax-came-from)
- **16:35 · Naive LLM · agent behaviour.** The agent ran 16 of `binwalk`'s 51 options; its main test
  compared its files with the same option table they were written from, so it could not fail. It never
  ran or mentioned `-D`, which makes binwalk run another program for every match (confirmed after the
  session). →
  [Addendum, "2.2"](white_paper_addendum_naive_llm.md#22-where-the-syntax-came-from) ·
  [Addendum, "2.4"](white_paper_addendum_naive_llm.md#24-two-grammar-details-with-consequences-for-the-pipeline)
- **16:35 · Caruca (v1) · generator use.** Caruca fills its test folders from 8 files (text, arithmetic,
  times, JSON and one JPEG; the paper says PNG images). `binwalk` finds nothing hidden in 7 of them and
  only the image's own header in the eighth. And because Caruca's generator tries every value in a
  number range, the agent's correct port range for one option (0 to 65,535) turns into 65,536 command
  lines. →
  [Addendum, "2.3"](white_paper_addendum_naive_llm.md#23-what-binwalk-needs-from-the-environment) ·
  [Addendum, "2.4"](white_paper_addendum_naive_llm.md#24-two-grammar-details-with-consequences-for-the-pipeline)
- **13:21 · Naive LLM · accuracy.** Asking the program found facts the manual-based answer key lacks.
  For `rm` and `grep`, the agent established 6 facts about argument syntax that neither Caruca's
  reference files nor its GPT-4o output record, 4 of them visible only by running the program. Given a
  deliberately wrong value, `rm` listed its 6 accepted values for the prompt-before-deleting option;
  the manual lists 3. →
  [Addendum, "1.3"](white_paper_addendum_naive_llm.md#13-case-study-a-ask-the-command-not-only-its-manual)
- **12:59 · Naive LLM · agent behaviour.** For `rm`, the first destructive command, the agent's only
  precaution was one scratch folder shared by all 27 of its `rm` runs, guarded by a check that would
  have let the runs proceed in the home folder had the folder not been created. After writing its
  files it never ran `rm` against them. →
  [Run 5 analysis, "2.3 Isolation and safety"](../../naive_llm_caruca/runs/2026-10-20_121932_naive-run-rm_rm_PROMPT_v1/analysis/analysis.md)
- **13:21 to 16:45 · Naive LLM · time and cost.** Six runs without web access, one command each:
  `grep` 322 s, $2.54; `rm` 60 s, $0.80; `binwalk` 193 s, $2.12; `cut` 104 s, $1.25; `convert` 1,291 s,
  $6.04 (2 h 14 min on the clock, because the Mac slept); `sort` 304 s, $2.46. List prices; billed to
  the subscription. →
  [Addendum, "1.2 The runs"](white_paper_addendum_naive_llm.md#12-the-runs)
- **Corrected on 2026-10-27 · Naive LLM · agent behaviour.** In all six of these runs, the agent's closing
  report claimed more testing than its logs show (for example, "Everything passed" over a test that
  ended with one failure; "BAD = 8" reported as everything working). The addendum's summary said
  "four runs" until 2026-10-27. →
  [Addendum, "In brief"](white_paper_addendum_naive_llm.md#in-brief-three-findings-in-plain-language) ·
  [Addendum, "4.7"](white_paper_addendum_naive_llm.md#47-what-this-section-does-not-claim)

## 2026-10-13

- **20:32 · Naive LLM · agent behaviour.** With web access on (run 3, `grep`, Claude Haiku 5.5), the
  agent searched GitHub for "caruca", found this project's public repository and read its notes on
  `grep`'s grammar, which shaped its answer. 739 seconds, $0.96. Web access was removed for every later
  run. →
  [Run 3 analysis](../../naive_llm_caruca/runs/2026-10-13_193448_naive-run-grep_grep_PROMPT_v1/analysis/analysis.md)
- **15:24 · PaSh · tooling.** Whether PaSh actually split a given command can be read reliably with a
  same-named wrapper placed earlier on the command search path, which logs each call; more than one call
  means it was split. Two earlier methods were wrong: a script ending in a redirect to a file silently
  falls back to plain bash, and PaSh's "assert all regions parallelizable" check passes even when nothing
  was attempted. →
  [PaSh VM setup, "3.3"](../docs/pash_vm_setup.md#33-reading-the-decision--solved-after-three-wrong-attempts)
- **12:48 · Caruca (v1) · consistency.** Re-running Caruca's own trace of `cat` reproduced the earlier
  trace exactly: 35 of 35 test setups paired, every recorded file action identical. →
  [Status report 2026-10-13, "What works"](status_reports/status_report_2026-10-13.md#what-works-verified-today)
- **12:48 · v2 pipeline · cost.** Caruca's one language-model call has still never been measured: all
  five live runs of it recorded no tokens and no cost. →
  [Status report 2026-10-13, "What does not work"](status_reports/status_report_2026-10-13.md#what-does-not-work-found-in-the-code-today-and-confirmed-by-the-console-session)

## 2026-10-05 and 2026-10-06 (written up 2026-10-13 12:48)

- **2026-10-06 · Caruca (v1) · accuracy.** `grep`'s manual lists 3 ways to give the search pattern
  (first word, after `-e`, or from a file after `-f`). All 3 of Caruca's `grep` syntax files hold only
  the first, so Caruca generates lines like `grep -e a a`, where `grep` reads the second `a` as a file.
  The answer key shares the gap, so the accuracy check reports a match. →
  [What Caruca is for, "Why the syntax spec matters"](caruca_purpose_grep_case.md#why-the-syntax-spec-matters-so-much-in-v1) ·
  [Addendum, "1.4"](white_paper_addendum_naive_llm.md#14-case-study-b-greps--e-f-form)
- **2026-10-06 · Caruca (v1) · paper.** 69 of the paper's 88 reference specifications come from the two
  parallelizers (PaSh 52, POSH 17); the listed parts add up to 87, not 88. Outside Caruca's own test
  generation and real-world-reach study, the syntax description is used on its own in only 6 ShellCheck
  checks. →
  [What Caruca is for, "Where the v1 paper is thin"](caruca_purpose_grep_case.md#where-the-v1-paper-is-thin)
- **2026-10-06 · v2 pipeline · confound.** The tracing comparison ran 45 times but covered only 12 distinct
  command lines out of the 229 Caruca offered (5%). For 6 of the 9 commands all five runs were the same
  no-option line, so no option was tested. Cause: Caruca's generator repeats lines and the repeats sat at
  the top of the list. →
  [Parity study, "8. Every confound"](v1_v2_parity_study.md#8-every-confound-stated)
- **2026-10-05 · PaSh · speed.** On a CPU-heavy `grep` pipeline in an 8-processor virtual machine, the best
  PaSh setting (8 workers, 250 KB slices) ran 4.73 times faster than plain bash on a 13.8 MB input,
  against 4.29 times with PaSh's default 1 MB slices: tuning gains 7–10%. The number of workers matters
  far more. All 430 timed runs gave the correct answer. →
  [PaSh work scheduling, "What the numbers say"](pash_work_scheduling.md#what-the-numbers-say)
- **2026-10-05 · PaSh · compatibility.** No PaSh version since September 2022 reads JSON descriptions,
  including the version current at the paper's November 2024 run, so Caruca's JSON output could not have
  been fed to it as it was. Of this project's nine study commands, only `uniq` has a hand-written
  splitting description in current PaSh. →
  [PaSh VM setup, "1"](../docs/pash_vm_setup.md#1-the-headline-finding-before-any-instructions) ·
  [PaSh VM setup, "1.2"](../docs/pash_vm_setup.md#12-how-little-the-stock-annotation-set-covers-our-commands)
- **2026-10-05 · PaSh · speed and a bug.** First measured speedups over plain bash (4.894 s) on 2.6 million
  lines: 1 worker 0.97 times, 2 workers 1.84, 4 workers 3.28, 8 workers 4.47. PaSh's fixed cost is about
  0.15 s per run. Separately, a `grep` pattern in double quotes with single backslashes makes parallel
  PaSh return 0 matching lines where bash returns 928. →
  [PaSh VM setup, "5"](../docs/pash_vm_setup.md#5-status-of-phase-0)

## 2026-09-22 to 2026-09-24

- **2026-09-24, written up 12:48 · v2 pipeline · cost.** Cost is not reproducible: three identical runs of
  the syntax step on `cat` (same model, temperature 0, same seed, exactly 6,376 input and 152 output
  tokens each) cost $0.01746, $0.01746 and $0.00978, 1.79 times apart. Likely the provider's prompt
  caching, which v2 does not record. →
  [Task 010, "13. Progress"](../tasks/010_execution_console.md#13-progress)
- **2026-09-22, written up 2026-09-29 09:36 · v2 pipeline and Caruca (v1) · accuracy.** Behaviour labels
  (whether a command may be split), compared with the hand-written reference over cases that line up:
  v2 25 of 77 exactly (32.5%), 68 of 77 under the paper's looser rule (88.3%); Caruca on the same seven
  commands 11 of 64 (17.2%) and 42 of 64 (65.6%). In all three runs v2 called `pwd` safe to split, the
  unsafe direction, which Caruca never does. →
  [Parity study, "5"](v1_v2_parity_study.md#5-stage-4--annotation-diverges-and-hits-a-ceiling-v1-does-not-have)
- **2026-09-22, 16:24 · Caruca (v1) · PaSh.** Caruca's descriptions for the nine study commands, made at its
  default trace setting, hold 64 cases and none is "stateless" or "pure", so PaSh would parallelize
  none of them: correct, but inert. Caruca can say "stateless" only when it traces with split input, the
  setting its own PaSh script uses. The paper never measures a speedup. →
  [Task 012, "1.3"](../tasks/012_pash_downstream_study.md#13-found-while-writing-this-task-the-parity-annotations-are-correct-but-inert-downstream)
- **2026-09-22, written up 2026-09-29 09:36 · v2 pipeline · defect, fixed.** Until 22 September, v2's
  tracing step stored the model's retyped copy of a command's output instead of the bytes the command
  produced. Fixed the same day; nothing published depended on it. →
  [v2 fidelity, "8.2"](v2_fidelity_to_v1.md#82-accidental--seven-found-by-the-2026-09-03-review-an-eighth-on-2026-09-22-all-fixed)
- **2026-09-22 · Caruca (v1) · size.** Caruca's hand-written pipeline is 2,698 lines of code, not the
  3,456 often quoted, which counts blank and comment lines too. This is the baseline for "how much
  hand-written logic does the LLM approach replace". →
  [Task 010, "13. Progress"](../tasks/010_execution_console.md#13-progress)

## 2026-09-14 to 2026-09-20

- **2026-09-14, 15:46 · Caruca (v1) · accuracy.** Caruca's own shipped GPT-4o syntax files match its own
  reference files exactly for 78 of 116 commands by Caruca's own comparison script (83 of 116 by this
  project's scorer); the paper reports 116 of 120. Corrected on 2026-10-26: that script misses most kinds
  of difference (see the 2026-10-26 bullet), so 78 mostly measures missing or extra options. →
  [Parity study, "6"](v1_v2_parity_study.md#6-why-no-number-here-is-compared-to-the-paper)
- **2026-09-14, 15:46 · v2 pipeline · accuracy and consistency.** Syntax step, nine commands: v2 and
  Caruca's GPT-4o output both found every reference option and invented none; arguments typed exactly
  right, 96.7% for v2 and 98.3% for Caruca. Three identical v2 runs at temperature 0 gave identical
  results for 8 of 9 commands. Refined later: v2 drops `tail`'s short `-f` spelling in 3 of 3 runs, which
  the scorer hid. →
  [Parity study, "2"](v1_v2_parity_study.md#2-stage-1--syntax-specification-replicates)
- **2026-09-14, setup figure corrected 2026-09-22 09:06 · v2 pipeline · accuracy.** Test-line step: v2
  reproduced on average 87.8% of Caruca's distinct command lines, but the file setups it asked for
  matched Caruca's in only 20.8% of cases. About half of that gap is notation only. →
  [Parity study, "3"](v1_v2_parity_study.md#3-stage-2--configuration-generation-diverges)
- **2026-09-14, 19:36 · Caruca (v1) · generator.** Caruca's limit on options per line, documented as "flags",
  actually counts an optional file name too. At a limit of 1, Caruca never pairs an option with a file for
  any command whose file is optional (`cat`, `wc`, `tail` and others). →
  [Parity study, "3.2"](v1_v2_parity_study.md#32-v2-does-not-respect-the-enumeration-bound)
- **2026-09-14, 18:40 · v2 pipeline · defect.** In the tracing step, 105 of 135 model sessions (78%) ended
  with a prose answer instead of reporting through the tool they were given; only 12 of 27 command runs
  produced usable output. →
  [Parity study, "4.1"](v1_v2_parity_study.md#41-the-dominant-failure-is-protocol-not-accuracy)
- **2026-09-20, 13:00 · v2 pipeline · accuracy.** Where a tracing session did report, it recovered 60.6% of
  the file changes Caruca's tracer recorded (33 units) and 39.1% of the file reads (23 units). On `pwd`,
  three identical runs gave 1.000, 1.000 and 0.600. →
  [Parity study, "4.2"](v1_v2_parity_study.md#42-where-a-session-did-report-recovery-is-partial)
- **2026-09-14, 15:46 · v2 pipeline · limit.** v2's behaviour step could not process `rm` or `tee`: their
  trace files (about 211,000 and 149,000 tokens) exceed GPT-4o's 128,000-token input. Refined on
  2026-10-13: Caruca's own annotator reads filtered traces (about 78,000 and 72,000 tokens), which fit. →
  [Parity study, "5.2"](v1_v2_parity_study.md#52-a-ceiling-intrinsic-to-the-llm-approach)
- **2026-09-14, 18:40 · v2 pipeline · cost.** All four v2 steps on nine commands, three runs each, cost $3.50
  in model spend (syntax $0.28, test lines $1.35, tracing $0.94, behaviour $0.92). Caruca traced and
  described all nine in about 17 seconds with no model spend. →
  [Parity study, "7"](v1_v2_parity_study.md#7-what-the-comparison-cost)
- **2026-09-14, 15:46 · Caruca (v1) · defect.** Caruca's behaviour-description format accepts any word as a
  condition operator, though Caruca itself writes only three; v2 invented "eq", Caruca's validator accepted
  it, and PaSh cannot read it. →
  [Parity study, "10"](v1_v2_parity_study.md#10-what-the-instrument-cost-and-why-it-came-first)

## 2026-09-03 to 2026-09-08

- **2026-09-08, 16:00 · v2 pipeline · first live run.** The first live model calls (GPT-4o and Claude Haiku
  4.5 on `mkdir`, `cat`, `wc`) cost about $1.15. The syntax step was perfect for both models. Every
  test-line output was rejected, because Caruca's own format description leaves the standard-input field's
  allowed values unstated; fixed later. →
  [Task 006, status block](../tasks/006_evaluation_harness.md#task-006-evaluation-harness--experiment-campaigns-caruca-v2-scoresweepmutate-docsreport)
- **2026-09-06, written up 2026-09-08 16:00 · Caruca (v1) · wasted work.** Across 90 commands, Caruca's
  generator emits 3,261,075 test command lines of which 562,789 are distinct: 82.7% are repeats, and the
  tracer runs them too. At Caruca's shipped limit of 4 options, `cat` gets 13,200 lines for 1,392 distinct
  ones. So the paper's tracing-time figures include the repeats. →
  [E0, "The enumeration-redundancy sweep"](e0_artifact_pinning.md#the-enumeration-redundancy-sweep-instrumentation-not-a-claim)
- **2026-09-06, written up 2026-09-08 16:00 · Caruca (v1) · defect.** Caruca's own estimate of how many lines
  it will generate is wrong for 90 of 90 commands (it says 280 for `mkdir`, which emits 4,240) and crashes
  for 14 of 120. →
  [E0, "The enumeration-redundancy sweep"](e0_artifact_pinning.md#the-enumeration-redundancy-sweep-instrumentation-not-a-claim)
- **2026-09-06, corrected 2026-09-22 · Caruca (v1) · paper.** A fresh Caruca run labels 26 of 29 `cp` cases
  "side-effectful", contradicting the paper's statement that `cp` is "in reality" pure; PaSh never had a
  hand-written `cp` description. →
  [E0, "Claim 3 — cp"](e0_artifact_pinning.md#claim-3--cp-no-hand-written-artifact-has-ever-existed-the-fresh-run-contradicts-the-papers-behavioral-claim-on-main)
- **2026-09-06, written up 2026-09-08 16:00 · Caruca (v1) · paper.** The paper's `grep -c` example describes a
  PaSh description that was fixed on 6 April 2021, 3.5 years before the paper. →
  [E0, "Claim 1 — grep"](e0_artifact_pinning.md#claim-1--grep-reproduced-against-a-2021-revision-and-the-fix-predates-the-paper-by-35-years)
- **2026-09-03, 22:20 · Caruca (v1) · defect.** Caruca's behaviour step cannot run on macOS on any input (it
  resolves `/tmp` to `/private/tmp` and then fails a fixed path check), so it has to run in the Linux
  virtual machine. →
  [v2 fidelity, "8.3"](v2_fidelity_to_v1.md#83-a-v1-defect-that-constrains-v2)

## Numbers that disagree between documents

Found while assembling this file (2026-10-27). Use the figure in the right-hand column.

| What | Figures in circulation | Use |
|---|---|---|
| Runs where the agent overstated its testing | "four" (addendum summary until 2026-10-27, diagram) | all six runs without web access (runs 4 to 9), per the run analyses; both corrected 2026-10-27 |
| `sort` lines doing real work, 1 option per line (reference / GPT-4o / agent) | 43/53, 40/44, 37/52 (run 9 analysis: each line run once) | 41/56, 38/47, 33/56 (task 018: traced by Caruca's own tracer); the methods differ, so quote the method with the number |
| Real-world `cut` and `sort` lines read | task 018's first strict reader: totals 5,909 and 5,011 | the GNU-rules reading: totals 5,856 and 5,010 valid lines (lines GNU itself rejects, such as FreeBSD-only `cut -w`, left out) |
| PaSh speedup over bash at 8 workers, default 1 MB slices | 4.47 times (`pash_vm_setup`), 4.99 times (`pash_work_scheduling`), 4.18 times (email) | unreconciled: same day, different scripts; quote each with its script |
| Tracing-step evidence units | 17 core units (parity study, two older paragraphs) | 33 file-change and 23 read units (re-scored 2026-09-20) |
| Size of Caruca's hand-written code | about 3,456 lines | 2,698 lines of code (3,456 counts blank and comment lines) |
| Real-world collection size | 666,468 (the paper) | 665,628 lines in the shipped file (665,631 as Python reads it); the 840-line gap is unexplained |
| `grep` lines Caruca generates at 1 option per line | 121 (addendum section 2.4) | 122 (addendum section 1.4, run 4, generator run 2026-10-20); 121 came from calling the generator directly |
