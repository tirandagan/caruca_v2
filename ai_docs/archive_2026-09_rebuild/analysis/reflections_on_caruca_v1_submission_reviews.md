# Reflections on Caruca v1 Submission Reviews

> **Version 1.0, 13 October 2026.** Written for Tiran after he shared
> `ai_docs/docs/Caruca v1 submission reviews.md`. **This document does not respond to those
> reviews.** Greenberg passed them on so Tiran could see the vision behind the Caruca work. Tiran's
> direction (10 October 2026) was to keep things simple and to stay pointed at one goal: a working
> v2 that uses an LLM and whose output real downstream tools can consume, starting with PaSh. The
> work that follows from this document is task 013 (`ai_docs/tasks/013_v2_downstream_readiness.md`).

The v1 code cited here is `binpash/caruca` at commit `d80324073`. The v2 code is this repository at
commit `8598d9d`. Every code citation was re-read on 13 October 2026. Sources are listed at the end.

## 1. What these reviews are

The file is not a review of the Caruca paper. It is the National Science Foundation's panel review
of a **grant proposal** submitted in 2023: *"Collaborative Research: FMitF: Track I: Modeling,
Learning, and Checking Specifications for Black-Box Shell Components"*. Greenberg was the lead
investigator and Vasilakis the co-investigator. The programme was "Formal Methods in the Field".
Four reviewers rated it Good, Fair, Good and Fair.

The proposal came about two years before the paper (October 2025). The paper's acknowledgments name
two different NSF grants (CNS-2247687 and CNS-2312346), not this one. Neither repository records
which venue turned the paper down or what its reviewers said, and those reviews may not be
obtainable.

Why read them, then: the reviewers summarise what the proposal set out to build. Caruca is one
piece of that plan made real. Seeing the whole plan shows which parts of it v1 delivered and what v2
is meant to carry forward.

## 2. The vision, in five points

These are taken from how the reviewers describe the proposal. They are not taken from their
criticism of it.

1. **One model per command, in two halves.** The first half is *how the command is called*: its
   flags, its arguments and what type each one is. The second is *what the command does*: which
   files it reads and writes, what it prints, and its exit code. The proposal keeps the two in
   separate languages. The first reviewer calls this the key insight: it "separates language and
   argument parsing from description and behavior, using two separate languages".
2. **A shared, open library of those models.** The idea is that tools stop hand-writing their own
   private notes about each command. The second reviewer singles out "the design of a library of
   specified shell commands" as what makes adoption likely.
3. **Checked by running, not by proof.** Proving that a model matches a real program is impossible
   in general, so the proposal relies on testing: run the command under controlled conditions and
   compare what happens with what the model says.
4. **Correctness depends on the state of the files.** The fourth reviewer quotes the proposal: "an
   invocation may be valid in one system state (e.g., some particular file exists) but invalid in
   another". A model therefore has to say under which conditions each behaviour holds.
5. **Many consumers.** The models are meant to serve tools that transform scripts (parallelizers),
   tools that check scripts (linters, safety and security monitors), documentation, and teaching.
   The running example was `grep`, including `grep -f`, where the pattern comes from a file.

## 3. How v1 carried the vision out (v1 only)

- **The "how it is called" half** is written by an LLM from the man page. It is the only step v1
  gives to an LLM.
- **The "what it does" half** is never asked of the LLM. v1 runs the command many times and records
  every file it touches.
- **Test runs** are built from the first half, combined with a fixed set of prepared folder setups:
  a file that exists, a missing file, an empty directory, a directory with one entry, and so on. That
  is point 4 of the vision, in practical form.
- **Four consumers** were evaluated: PaSh and POSH (both parallelizers), ShellCheck (a linter) and
  Shseer (a checker of each command's before/after file conditions).

Where v1 narrowed the vision:

- **The consumers lean one way.** 69 of the 88 reference models it was compared against come from
  the two parallelizers. This is covered in `caruca_purpose_grep_case`.
- **The downstream results never started from the LLM's own "how it is called" half.** v1's tracing
  reads the human-curated grammar files in `syntax_specs/`, or simplified versions of them in
  `pash_syntax_specs/` when run for PaSh (`caruca/src/caruca/cli/trace.py:11-16`). The LLM's grammar
  was scored separately, by comparing it with those same curated files. So the two halves were each
  shown to work, but never one feeding the other on the way to a consumer.

## 4. What this means for v2: seven recommendations

Kept to what serves the stated goal: a working v2 whose output downstream tools use.

**1. Define "done" as a downstream tool using v2's output correctly.** PaSh comes first, and task 012
already designs that study. Next is ShellCheck, because it reads the "how it is called" half: the
half Greenberg calls v1's objective, and the half PaSh does not exercise. Shseer is third; it reads
the before/after file conditions (point 4 of the vision). POSH is last, since the paper itself could
not run it.

**2. Keep the two halves as two separate outputs**, each tested by the consumer that reads it. v2
already splits them this way: stage 1 writes the grammar, and stages 2 to 4 produce the behaviour.
Keep it so.

**3. Run v2 end to end from its own grammar.** Task 012 already plans this as one of its comparison
groups (its "end-to-end arm"). It is the clearest thing v2 adds, because the paper's downstream
results never started from the LLM's grammar (section 3 above).

**4. Clear PaSh's path in this order.** The cheapest comparison group comes first: v2's annotation
step reading v1's recorded runs, so any failure can only belong to that step. It needs four things,
in this order:

- a way to read PaSh's decision for each command inside a multi-command script (task 012, the last
  open item of phase 0);
- the converter from Caruca's output into the Python form PaSh reads (task 012, phase 1);
- v1 runs recorded in *split mode*, where the input is also fed in pieces, which is the only way any
  command can come out as "safe to split" (task 012, phase 2);
- a shortened copy of the recorded runs for `rm` and `tee`, whose full records are too long for the
  model to read in one go (task 011, workstream 4a).

The full v2 chain comes second. It needs stage 3 to always hand back its observations; 78% of
sessions currently end without doing so (task 011, workstream 3a). It also needs stage 2's request
to stop counting a file name against the flag limit, which accounts for most of its surplus
command lines (task 011, workstreams 2a to 2d).

**5. Decide on purpose how results from different folder setups combine.** For each command line, v1
labels every run separately: safe to split and run in parallel ("stateless"), not splittable but
touching nothing else ("non-pure"), or changing files ("side-effectful"). It then merges the labels
by keeping **the most parallel-friendly one**, after first discarding every run that failed (section
7 has the code). So if one setup says "safe to split" and another says "changes files", the merged
answer is "safe to split". Under v1's default input mode "safe to split" never occurs, so the rule
only chooses between two labels PaSh treats alike. In split mode, which PaSh needs, a single setup
can decide that a command gets parallelized. Whether that actually happens for the nine study
commands has not been tested.

v2's annotation instructions (`prompts/annotate/system.md`) say nothing about merging labels or
about failed runs, so the model decides each time, and possibly differently each time. The
recommendation:

- measure first (task 012 already includes a deliberately too-permissive label, to prove that harm
  would be caught);
- record each setup's label before merging, so a wrong answer can be traced to the merge;
- then choose: copy v1's rule (faithful to v1), or add the safe rule, keep the *least*
  parallel-friendly label, as a separate comparison group. Do not quietly replace one with the
  other.

**6. Write the operating conditions down once, and record them with every run.** v2 already works
under fixed conditions. It does not state them in one place, and the record kept for each run
(its manifest) leaves some out. The conditions are:

- the command is run directly, not through a shell;
- `SHELL` is `/bin/sh`;
- standard input comes from a prepared file;
- each run is stopped after 2 seconds;
- the prepared files are v1's;
- the commands are GNU coreutils 9.4 on Ubuntu 24.04, in both virtual machines.

Two concrete gaps:

- **v2's tracing step runs on the Mac by default.** `--isolation` defaults to `host`
  (`src/caruca_v2/cli.py:231`), and on the Mac that means macOS's own versions of the commands, not
  the GNU versions v1 and PaSh use. The parity study's tracing campaign chose the virtual machine
  explicitly, so its results are unaffected. Any run meant for a downstream tool should do the same.
- **The per-run record omits key facts about the run.** It stores v1's commit
  (`src/caruca_v2/v1.py:1108`) but not v2's own commit, the operating system the commands ran on,
  or the coreutils version. Task 011 will keep changing v2 while task 012 runs, so without these
  later results cannot be compared with earlier ones.

**7. Small timeout fix (low priority).** When a run hits the time limit, v2 keeps no output and no
exit code (`src/caruca_v2/tools.py:461-467`). The comment at `src/caruca_v2/stages/trace.py:154`
says the opposite, and v1 records the exit code 124 that the `timeout` program returns. Three steps:

- match v1's behaviour;
- check that the command inside the virtual machine is actually stopped, not just the program on
  the Mac that launched it;
- put a cap on how much output a run may produce.

## 5. For the paper, briefly

The vision's story is one model of each command, used by many tools. The simplest strong evidence
v2 can add is the same LLM-produced model, carried end to end, used correctly by more than one
downstream tool. Alongside that come two things the paper does not report: what the LLM steps cost,
and how much their answers vary between identical runs.

## 6. Deliberately not doing

- Formal semantics or proofs.
- A new specification language.
- Synthesis methods beyond running the command and watching it.
- Adoption studies or partner communities.
- Plans for broadening participation.
- Commands whose arguments are themselves programs (`sed`, `awk`, `find`). For the record, v1 tests
  `sed` only with one-character scripts (section 7).

These are the reviewers' themes for a grant. None of them is needed for a working v2 that
downstream tools can use.

## 7. v1 facts established while writing this

**Checked by reading the source, 13 October 2026:**

- **Each folder setup gets its own label, and the merged label is the most parallel-friendly one.**
  - The comparison ranks "stateless" highest (`caruca/src/caruca/annotator/pash.py:7-29`).
  - Each per-run record is "one run of a command with a given file system environment"
    (`annotator/annotator.py:18-21`).
  - The merged label is `max(...)` over the successful runs (`annotator/annotator.py:121-124`).
  - The same rule applies again when cases with identical conditions are merged
    (`annotator/__init__.py:33`).
- **Failed runs never contribute.**
  - Runs with a nonzero exit code are skipped before labels are derived (`tracer/data.py:149-150,
    254`).
  - Runs that wrote anything to standard error are skipped when labels are merged
    (`annotator/annotator.py:38-40`).
- **sed's test script is split into single characters.**
  - The intended script is written `choices=("s/a/b/g")` (`syntax_specs/sed.py:8,23`;
    `pash_syntax_specs/sed.py:10`). Parentheses around a single string do not make a list in
    Python, so this is just the string.
  - The argument type is `Other`, which is `String` (`ir/syntax.py:421`).
  - `String` builds test values by looping over that string (`ir/syntax.py:287`), so the values
    are `s`, `/`, `a`, `b`, `g`.
  - The same pattern appears at `ir/syntax.py:386`, where `Hostname` gets the single string
    `"localhost"`.
  - What sed does with each one-character script was not run.
- **Downstream results came from curated grammars** (section 3).

**Reported while researching this document, not yet checked** (task 013 checks each one; none of
them should be quoted as fact):

- `NonEmptyDirectory`'s after-run check compares a path object with a string, which would always be
  false (`ir/environment.py:252`).
- The handler for a run that times out can never be reached (`tracer/tracer.py:157`).
- The paper mentions a faster kernel filter for `strace` (seccomp-BPF), but the command line does
  not pass `--seccomp-bpf` (`tracer/tracer.py:86`).
- The `docker` isolation mode looks non-functional.
- The paper's internal counts do not agree:
  - Shseer is "12" in two places and 18 in the results table;
  - 52 + 17 + 6 + 12 = 87, not the stated 88;
  - the flag-normalised count (64,542) is smaller than the exact-match count (66,882), although
    normalising can only add matches.
- The script that builds the real-world reach tiers looks for `ShortFlatSplat`, apparently a typo
  for `ShortFlagSplat` (`eval/user-scripts/completeness_accumulate.sh:9`).

## Sources

| Claim | Where it was checked |
|---|---|
| What the proposal set out to do; the five points | `Caruca v1 submission reviews`: the first reviewer's solicitation paragraph, the second's broader-impacts strengths, the third's summary and field-area notes, the fourth's summary of the three thrusts and its quotes from pages 5 and 18 |
| The paper's funding | The paper, Acknowledgments |
| 69 of 88; Greenberg's view of v1's objective | `caruca_purpose_grep_case` |
| PaSh study design, comparison groups, phases | `012_pash_downstream_study` |
| Stage 2 and 3 problems, workstreams | `011_v2_improvement_program`; `v1_v2_parity_study` |
| GNU coreutils 9.4 on Ubuntu 24.04 | `012_pash_downstream_study`, phase 0 record |
| v1 and v2 code | The file and line references above |
| Cost and run-to-run variation not in the paper | `memory/caruca_paper_unmeasured_contributions.md` |
