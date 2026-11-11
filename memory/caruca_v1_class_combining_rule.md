---
name: caruca-v1-class-combining-rule
description: "v1 merges per-environment PaSh classes by keeping the MOST parallelizable (stateless wins), drops failed runs first; v2's annotate prompt states neither rule; sed's test script is iterated character by character; the paper's downstream results came from curated grammars, not LLM output"
metadata:
  type: project
---

Read in v1's source at `binpash/caruca` `d80324073` and in v2 at `8598d9d`, first on 2026-10-10 and
again on 2026-10-13. Paths are under `caruca/src/caruca/` unless they say otherwise.

**1. Merging labels across filesystem environments keeps the most parallelizable class.**
- `Parallelizability.__ge__` ranks S (stateless) > P > N > E (`annotator/pash.py:7-29`).
- A `RunSpecification` is "one run of a command with a given file system environment"
  (`annotator/annotator.py:18-21`).
- `Specification.to_pash` sets `pclass = max(...)` over the successful runs
  (`annotator/annotator.py:121-124`).
- Merging cases with the same predicate also takes `max` (`annotator/__init__.py:33`).
- **Consequence:** if one environment shows S and another shows E, the result is S.
- Under the `simple` stdin default S never occurs, so the rule only chooses between N and E. PaSh
  treats both as not parallelizable, so nothing changes downstream.
- In split mode, which task 012 needs, one environment can decide "stateless". **Not tested:** whether
  this actually happens for the nine parity commands.

**2. Failed runs never contribute.**
- Traces with a nonzero exit code are skipped (`tracer/data.py:149-150, 254`).
- At merge time, runs that wrote to stderr are also skipped (`annotator/annotator.py:38-40`).
- So a timed-out run (exit 124 from `timeout 2`) also vanishes.

**3. v2's annotate prompt states neither rule.**
- `prompts/annotate/system.md` (36 lines) has no wording about combining environments or about failed
  runs, so the model decides each time.
- Task 013 records this as decision D1: measure first, then teach v1's rule as kind B, and add the
  safe least-parallelizable rule only as a separate arm.

**4. sed's test script is split into single characters.**
- `choices=("s/a/b/g")` is a plain string, not a 1-tuple (`syntax_specs/sed.py:8,23`,
  `pash_syntax_specs/sed.py:10`).
- `Other = String` (`ir/syntax.py:421`), and `String` maps over `self.choices` (`ir/syntax.py:287`),
  so the test values are `s`, `/`, `a`, `b`, `g`.
- The same pattern appears at `ir/syntax.py:386` (`Hostname = MetaString(("localhost"))`).
- **Not tested:** which of those one-character sed scripts succeed.

**5. The paper's downstream (Q1) results never started from the LLM's grammar.**
- `trace` loads the curated `syntax_specs/`, or `pash_syntax_specs/` / `posh_syntax_specs/` with
  `--pash` / `--posh` (`cli/trace.py:11-16`; `syntax_specs/__init__.py:10-16`).
- `syntax_specs/*.py` is the human-curated ground truth ([[caruca-v1-eval-tooling-notes]]).
- The LLM's grammar was scored separately against those same files (Q2).
- Running end to end from the LLM's grammar is therefore new in v2 (task 012's V2-e2e arm).

**Why:** facts 1 to 3 decide whether PaSh parallelizes a command in task 012's split-mode arms. They
were not in any document before 2026-10-10.

**How to apply:** when a V1 or V2 PaSh annotation says "stateless", check which environment produced
it before attributing harm. Keep per-environment labels (task 013, workstream W3a).

Related: [[project-pash-downstream-study]], [[caruca-v1-pipeline-reference]],
[[project-proposal-reviews-vision]].

**Observed consequence (2026-11-11, task 021, Lima `caruca`, coreutils 9.4).** v1's split-mode trace of `sort`
on its main grammar (`--max-count 2`, branch `pash-python-annotations` commit `4bf74dd9a`) labels 34 cases
`stateless`, including `sort -n -u`, `-n -s`, `-g -u`, `-h -s`, `-k … -u` (the rest pair `-m`). Ran
`printf '2\n1\n' | sort -n -u` → `1 2`, halves joined → `2 1`: **v1's `stateless` for `sort -n -u` is wrong.**
Not established: why. Candidates are the rule above (one passing environment wins) and v1's text inputs
making every numeric key equal.
