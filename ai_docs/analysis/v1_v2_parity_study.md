<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!-- caruca_v2 analysis document. Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
     Licensed under the PolyForm Noncommercial License 1.0.0
     https://polyformproject.org/licenses/noncommercial/1.0.0
     Noncommercial use only. Commercial use is prohibited. -->
<!-- ATTRIBUTION-NOTICE:END -->

# The v1-vs-v2 Parity Study — Does an LLM Pipeline Reproduce Caruca?

> **Status:** all four stages complete. Written 2026-09-14.
> **v1 reference commit:** `d8032407346aadc135b14c043618c8c1d4f4e0cf`
> **Model:** `openai/gpt-4o`, temperature 0.0, seed 42, k=3 samples per cell.
> **Bound:** `--max-arity 1 --max-count 1` on both sides.
> **Spend:** $3.50 of an approved $60 ceiling.
> **Companion:** [`white_paper_addendum.md`](white_paper_addendum.md) routes these results to
> the paper. Method and provenance: `ai_docs/tasks/008_v1_v2_parity_study.md`.

---

## 0. The question, and the short answer

The question this study exists to answer, in Tiran's words: *are we doing exactly what v1 can
do, and are we replicating the results, or are we getting an improvement?*

**Per stage, on nine commands:**

| Stage | What it does | Verdict |
|---|---|---|
| 1. Syntax specification | documentation → flags and types | **Replicates.** Identical coverage; v1 marginally better typing |
| 2. Configuration generation | spec → invocations + environments | **Diverges.** Near-complete invocation recall, but the *environments* are mostly wrong |
| 3. Execution and tracing | run it, record what happened | **Does not replicate.** 15 of 27 cells produced nothing usable; 78% of sessions never reported |
| 4. Annotation | traces → consumer specification | **Diverges**, and v2 cannot process the two largest inputs at all |

**The headline is not a number, it is a distinction.** v2 reproduces what v1 *writes* far
better than what v1 *means*. It recovers v1's flags exactly and its invocation strings almost
exactly, and then asks for the wrong filesystem (stage 2) and derives a different
specification (stage 4). A pipeline scored only on the artifacts it emits would look close to
parity; scored on what those artifacts commit the system to, it does not.

---

## 1. How to read every number here

**Both sides are measured with the same instrument, at the same bound, today.** No figure in
this document is compared against a published one. That is deliberate, and §6 explains why it
had to be.

**One method per stage, never blended.** The four stages have four incompatible denominators —
arguments, invocations, filesystem interactions, annotation cases. There is no
cross-stage score here and there should not be one.

**Where a v1-versus-v2 *delta* is meaningful, and where it is not.** For stages 2 and 3, v1 *is*
the reference: it scores 1.0 by construction, so a percent change against it is an identity,
not a comparison. Those stages report v2's agreement with v1, never a delta. A real delta
exists in exactly two places: stage 1 (v1 also runs an LLM, so both sides can be scored against
the same third party) and stage 4 against the hand-curated ground truth (again a third party,
where v1 is *not* guaranteed to be right). This rule is enforced in code, not prose:
`harness/report.py` has no path that emits a percent change for a reference method.

---

## 2. Stage 1 — syntax specification: **replicates**

Documentation in, a specification of flags and their types out. The only stage where v1 also
uses a model, so this is the one like-for-like comparison in the study.

| | v2 (k=3) | v1's own LLM output |
|---|---|---|
| F1 | **1.000** | **1.000** |
| Exact-argument rate | 0.967 | **0.983** |
| Flags missing | **0** | **0** |
| Flags invented | **0** | **0** |

Per command, the two systems are identical on seven of nine. They differ on two, and both
differences are *typing*, not coverage:

| command | v2 exact | v1 exact |
|---|---|---|
| `tail` | 0.769 | **0.846** |
| `tac` | 0.933 | **1.000** |

**Verdict: replicates.** Neither system misses or invents a single flag on any of the nine
commands. v1 is slightly ahead on argument typing. That direction is worth stating plainly:
most of this study's surprises have run the other way, and this one does not.

**A reproducibility result fell out of k=3.** `tac` shows a **0.200 spread** in exact-argument
rate across three samples at temperature 0; every other command is stable at 0.000. One
command in nine is enough to justify k>1 for the whole experiment program — with a single
sample there is no way to tell "v2 differs from v1" from "v2 differs from itself". The paper
runs its LLM step once per command and reports no variance measurement at all.

---

## 3. Stage 2 — configuration generation: **diverges**

A specification in; out come the concrete invocations it allows and the environment each one
needs. v1 does this with roughly 715 lines of nested combinatorial Python.

All 27 cells produced configurations **accepted by v1's own `CommandConfig` model**. Validity
is not the issue.

| command | invocation recall | precision | **environments covered** |
|---|---|---|---|
| `cat` | 1.000 | 0.385 | 0.200 |
| `pwd` | 1.000 | 0.714 | 0.200 |
| `rm` | 1.000 | 1.000 | **0.000** |
| `sha256sum` | 1.000 | 0.590 | 0.200 |
| `tac` | 1.000 | 0.614 | 0.500 |
| `tail` | 0.964 | 0.352 | **0.000** |
| `tee` | 0.933 | 1.000 | 0.148 |
| `uniq` | **0.000** | 0.000 | — |
| `wc` | 1.000 | 0.462 | 0.417 |
| **mean** | **0.878** | 0.568 | **0.185** |

Three separate things are happening and they must not be averaged into one verdict.

### 3.1 Invocation recall is near-complete — once the comparison is fair

Six of nine commands are at 1.000. The original instrument scored `grep` at **0.041**; the same
output scores **0.863** once `--color=always` and `--color always` are recognised as one
invocation. That change is justified by injectivity rather than by the score: on v1's own
output, even sorting every token after the binary merges **zero** distinct invocations
(`grep` 73/73, likewise `cat`, `mkdir`, `wc`), so normalization leaves the denominator
untouched. The pre-normalization figure rides along in every record.

### 3.2 v2 does not respect the enumeration bound

**Corrected 2026-09-14, after inspecting the raw outputs side by side.** An earlier version of
this document attributed `uniq`'s zero to a defect in v1's enumerator. That was wrong, and the
correction inverts the finding.

`--max-count 1` bounds how many **optional elements** an invocation may carry — and an optional
positional is one of them. So at this bound v1 emits a flag *or* an operand, never both:

| command | positionals | v1 invocations combining a flag with an operand |
|---|---|---|
| `uniq`, `cat`, `wc` | optional (the DSL default) | **0** |
| `cp`, `mv`, `ln` | mandatory (`AT_LEAST_ONE`/`EXACTLY_ONE`) | 232 / 88 / 96 |

Mandatory positionals must always appear, so they do not consume the budget; optional ones do.
At `--max-count 2`, v1 emits flag-plus-operand forms for `uniq`, `cat` and `wc` too (48, 24, 14).

**v1's implementation is internally consistent, but it does not match its own documentation.**
The CLI describes `--max-count` as *"the maximum number of optional flags to use for a single
invocation"*. The implementation (`ir/syntax.py::__filtered_args`) collects every argument for
which `is_optional()` holds — `Arity.OPTIONAL` or `Arity.ZERO_OR_MORE` — across all argument
groups, which sweeps in **positionals**. So an optional file operand silently consumes one of
the slots the help text reserves for flags.

The practical consequence is larger than it sounds: **at `--max-count 1`, v1 never emits a flag
applied to a file** for any command whose file argument is optional. `cat -n relpath_1` is not in
its enumeration, and neither is any other flag-plus-file pairing for `cat`, `wc`, `tail`, `tac`,
`sha256sum` or `uniq`. At the shipped default of 4, one of the four slots is likewise consumed
by the operand rather than a flag.

**v2 applies the bound without distinguishing optional from mandatory positionals.** Where a
positional is *mandatory* it must always appear and does not consume the budget — and there v2
is exactly right, matching v1's flag-plus-operand count precisely (`rm` 30 = 30, `tee` 18 = 18),
which is why `rm` scores 1.000 recall *and* 1.000 precision. Where the positional is *optional*,
v2 attaches it anyway:

| command | positionals | v1 flag+operand | v2 flag+operand | out of bounds |
|---|---|---|---|---|
| `rm` | mandatory | 30 | 30 | — legal |
| `tee` | mandatory | 18 | 18 | — legal |
| `tail` | optional | 0 | 50 | **50 / 77** |
| `cat` | optional | 0 | 24 | **24 / 39** |
| `sha256sum` | optional | 0 | 24 | **24 / 39** |
| `uniq` | optional | 0 | 24 | **24 / 25** |
| `wc` | optional | 0 | 14 | **14 / 26** |
| `tac` | optional | 0 | 10 | **10 / 22** |
| `pwd` | none | 0 | 0 | — |
| **total** | | | | **146 / 285** |

This single error explains both stage-2 anomalies at once. **Precision** is low (0.352 on
`tail`) because the surplus invocations are bound violations, not creative extras — and it is
1.000 on exactly the two commands where the positional is mandatory. And **`uniq` scores 0.000
recall** because 24 of its 25 invocations violate the bound while the two legal operand-only
forms v1 emits — `uniq relpath_1` and `uniq abspath_1` — were never produced.

`pwd` is the control: it takes no operands, so there is no bound to violate, and it is the one
command with nothing to explain.

**Corrected twice.** The first write-up blamed v1's enumerator; the second counted every
flag-plus-operand invocation as a violation, including the two commands where it is legal. Both
errors were mine, both were caught by reading the raw outputs, and the second is why the figure
is 146 rather than 194.

### 3.3 The real v2 gap is the environment, and the invocation diff cannot see it

**0.185 mean coverage.** The systematic cause: v2 types a plain string operand as an existing
*file*. On `grep a relpath_1` it emits `arg_type: "already"` for the regex `a` — asking the
sandbox to contain a file named `a` — where v1 emits `no_env`.

The invocation string is right. The configuration validates. **Nothing downstream would
object**, and the traces would simply describe the wrong filesystem. This is the single most
important finding in the study, and it was invisible until the comparison task 002 deferred was
actually built: scored on invocation strings alone, that run reads as a near-success.

Under-generation and over-generation are different failures and are reported separately; §3.2
shows the over-generation here is a single systematic error rather than a diffuse one.

---

## 4. Stage 3 — execution and tracing: **does not replicate**

Each configuration gets a fresh workspace built from v1's own fixtures, the command runs, and
what it did is recorded. v2 traced **v1's own configurations**, not its stage-2 output, so an
upstream typing error is not scored twice.

27 cells, **12 produced a usable result and 15 did not**. $0.940.

### 4.1 The dominant failure is protocol, not accuracy

Across **135 tool-loop sessions**:

| | |
|---|---|
| Ended without calling `report_observations` | **105 (78%)** |
| Used exactly 2 turns of the 15 available | 111 |
| Executions performed per session | exactly 1, in all 135 |

The shape is consistent: turn 1 calls `run_command`, turn 2 answers **in prose** rather than
calling the reporting tool, and the loop ends. The tool is registered, the system prompt asks
for it by name, and the model had thirteen unused turns.

Success is strongly command-dependent, which rules out simple randomness:

| command | sessions reporting |
|---|---|
| `pwd` | 13/15 (87%) |
| `rm` | 7/15 (47%) |
| `cat`, `sha256sum` | 4/15 (27%) |
| `tail`, `tee` | 1/15 (7%) |
| `tac`, `uniq`, `wc` | **0/15** |

**This is model behaviour, not an instrument defect** — the prompt asks for the report and the
tool exists, so the request is answerable. It is the same *shape* as the stage-2 failure where
a model stopped at 10 of 122 invocations, which was addressed by asking once whether anything
was missing. Whether to do the equivalent here is a scope decision, not a bug fix, and it is
deliberately not taken: it would be the second time the LLM side is nudged, and every nudge
runs in the direction of flattery.

### 4.2 Where a session did report, recovery is partial

Pooled over the 17 core and 11 inference units that could be compared:

| tier | precision | recall |
|---|---|---|
| core `{ad md de mo wf rd}` | 0.769 | **0.588** |
| inference `{rf}` | **1.000** | 0.545 |

Per command the results are bimodal rather than middling — `cat`, `pwd` and `sha256sum` recover
everything; `rm` and `tail` recover nothing; `tee` recovers a quarter:

| command | paired configs | v1 distinct interactions | core recall |
|---|---|---|---|
| `cat` | 4 | 2 | 1.000 |
| `pwd` | 4 | 2 | 1.000 |
| `sha256sum` | 1 | 2 | 1.000 |
| `tee` | 1 | 5 | 0.250 |
| `rm` | 3 | 2 | **0.000** |
| `tail` | 1 | 2 | **0.000** |

**Read these denominators before reading the rates.** v1's projected traces hold 2 distinct
interactions for most of these commands, so a command scores 1.000 or 0.000 with very little in
between. Seventeen core units total is thin evidence, and the honest summary is that stage 3
produced too few usable observations to characterise accuracy at all — which is itself the
result.

### 4.3 Why projection is not optional

v1's raw traces are mostly dynamic-loader noise: `ls` records 17,512 `(action, path)` pairs that
reduce to **20** distinct relevant ones; `dirname` records 640 that reduce to **1**. Scored raw,
`dirname` recall is capped near 12% however perfectly a model observes, because
`/usr/lib/.../libc.so.6` is not visible through `list_dir`/`read_file`/`stat_path`. Both sides
are projected through **v1's own relevance filter**, and the projection *is* the ceiling — which
is what makes "fraction of the recoverability ceiling achieved" computable rather than
rhetorical.

**Two tiers, never summed.** `core` covers state changes, every one recoverable from a pre/post
listing or the command's own streams; a miss there is a model failure. `inference` covers reads,
which leave nothing a prober can see directly. Adding them would make the score a function of
how many files the command happens to read.

## 5. Stage 4 — annotation: **diverges**, and hits a ceiling v1 does not have

Traces in, a consumer specification out. 21 of 27 cells produced an annotation; **all six
failures are `rm` and `tee`** (§5.2).

Both sides scored by the same instrument against the same third party, the hand-curated
ground truth:

| | aligned cases | parallelizability class agreeing |
|---|---|---|
| **v2** | 33 | **10 (30%)** |
| **v1** | 64 | 11 (17%) |

v2 agrees with the humans at nearly twice v1's rate, over half as many aligned cases. Its case
counts swing widely — 2 for `cat` where v1 derives 14, but 14 for `sha256sum` where v1 derives 8.

**Both rates are low, and neither is an accuracy figure.** Of v1's 62 class disagreements with
the ground truth, **58 are v1 being *more conservative* than the humans** (`pure → non-pure` ×33,
`stateless → non-pure` ×16) against 4 in the other direction. E0 predicted exactly this for
`grep` at this bound; nine commands confirm it with 58/62 directional consistency. At
`--max-count 1` v1 sees only single-flag invocations, has less evidence, and falls back
conservatively. Neither figure is comparable to the paper's Q1, which was execution-based.

### 5.1 The two artifacts are written at different granularities

v1's annotator emits one conjunction per observed flag combination — 14 cases for `cat`, each
like `(exists "-n") and (len_args_eq 0)`. The hand-curated file writes 3 general atoms —
`exists "-n"`, `len_args_eq 0`, `"default"`. Matching by predicate key aligns **zero** of them.

Relating them requires a stated rule, so the scorer applies **subsumption**: the rule PaSh
itself uses to select a case — a general case governs every invocation satisfying it, most
specific first, `"default"` last. The alignment mode is recorded in every result, and the
predicate field is excluded from scoring when subsumption did the aligning.

### 5.2 A ceiling intrinsic to the LLM approach

**v2 cannot annotate `rm` or `tee` at all.** Their traces are ~211,000 and ~149,000 tokens
against gpt-4o's 128,000-token window. v1's annotator is deterministic code with no such limit:
it annotated all nine in under a second each.

This is the first constraint this study has found that is **intrinsic to the approach rather
than to the instrument**. It is not a prompt problem and not a tuning problem. It scales the
wrong way: the more thoroughly a command is traced, the less able the LLM annotator is to read
the result.

---

## 6. Why no number here is compared to the paper

The obvious baseline for stage 1 is the paper's **116/120**. It cannot be used, because v1's
own shipped artifacts do not reproduce it.

Scoring v1's committed LLM output (`outputs/llm-dsl-generation/*.py`, 117 specs) against v1's
committed ground truth (`syntax_specs/*.py`):

| Instrument | Result |
|---|---|
| v1's own `eval/cmp_specs.py` — the paper's Q2 tool | **78 / 116** |
| This project's independent structural scorer | **83 / 116** |
| The paper §7.2 | **116 / 120** |

**The instrument is sound.** v1's ground truth scored against *itself* is **117/117**, and two
independently built scorers land within five of each other. The signature is typing rather than
coverage: 105/116 commands have no missing or spurious options, but only 86/116 have no type
misclassification.

**This is not a claim that the paper is wrong.** The most likely explanation is that the
committed set is *a* run rather than the run the paper reported — the shipped artifacts simply
do not let the published figure be re-derived. Drift explains less than expected: the LLM set
and the ground truth were committed a day apart, with only two subsequent spec commits. It
belongs in the same class as E0's `ps` and `cp` findings, and is a question for the v1 authors.

The consequence is methodological: **v1 is measured here, today, on the same artifacts and with
the same instrument as v2.** That is the only footing on which the two can be honestly compared.

---

## 7. What the comparison cost

| stage | cells | v2 spend | v1 side |
|---|---|---|---|
| 1 syntax specification | 27 | $0.284 | free — already committed |
| 2 configuration generation | 27 | $1.354 | free — deterministic, host-side |
| 3 execution and tracing | 27 | $0.940 | 17 seconds, all nine commands |
| 4 annotation | 27 | $0.920 | under a second each |
| **total** | | **$3.50** | **~17 seconds of compute** |

Two observations the paper could not make, because it measured neither.

**v1's side is effectively free.** Tracing and annotating all nine commands took 17 seconds of
wall clock and no API spend. The LLM pipeline's cost is not compared against zero — it is
compared against *seconds*.

**Both completed campaigns came in far under estimate.** Stage 2 was priced at $3.77 from C0's
measured token profile and cost $1.35. Stage 3 was priced at $13.50–47.25 with no measured
basis and cost **$0.940** — an order-of-magnitude overestimate, now corrected by measurement.
Part of that is because 78% of its sessions ended after two turns.

---

## 8. Every confound, stated

A result that does not name what could undermine it is not a result.

1. **The exhaust nudge (stage 2).** A model that stops early is asked once whether anything is
   missing. This lifted `grep` from 10 invocations to 75. Every stage-2 number here is produced
   under that policy and is not comparable to a single-shot number. It runs in the direction of
   flattery.
2. **Prompt wording (all stages).** v1's prompts cannot be copied — licensing — so v2's are
   paraphrases. This is the largest uncontrolled difference in the stage-1 comparison.
3. **`rm` is a contamination control.** It is one of v1's four few-shot exemplars, so its own
   specification appears in the stage-1 prompt. It scores 1.000/1.000 — which is the expected
   upper bound, and confirms the instrument rather than measuring the model. It is excluded
   from any claim about generalisation.
4. **The bound is tighter than the paper's, and that was a cost decision rather than a
   principled one.** `--max-count 1` throughout. The paper's §4.1 invocation study (665,000 real
   invocations from 49,000 GitHub scripts) reports 64.7% with no flags, 29.0% with one and 5.9%
   with two — so a one-flag bound reaches roughly 93.7% of real usage where the paper's ≤2
   reaches 99.6% and its ≤4 default reaches 99.998%. The narrower bound also makes v1
   systematically conservative at stage 4 (§5). A re-run at the paper's ≤2 is the obvious next
   step, and §7.4's timings suggest it is affordable.
5. **One model, one temperature.** `gpt-4o` at 0.0. Nothing here separates "better method" from
   "better model".
6. **Nine commands, three of them in the reserved held-out set.** `cat`, `uniq` and `wc` are in
   task 001's C1 set. This study tunes nothing, so it cannot leak configuration choices, but
   the overlap is stated.
7. **Stage 3 rests on 17 core units.** Most commands have 2 distinct interactions to
   recover, so per-command rates are effectively binary.

---

## 9. Where v2 looks better because v1 has a defect

Five times in this study a scored disagreement has pointed at v1 rather than v2. Recording them
so that "v2 improved on v1" is never claimed where "v1 had a bug" is the truth.

**One entry was withdrawn.** `uniq`'s enumeration was listed here until the raw outputs were
read side by side; v1 was respecting the `--max-count` bound correctly and v2 was not (§3.2).
It is the one place in this study where a v1 defect was claimed and turned out to be a v2 error,
and it is left visible rather than quietly deleted.

1. **`--include` typed `String`** where its siblings `--exclude`/`--exclude-dir` are `Glob`, in
   `grep`'s committed specification.
2. **`dash_as_stdin=True`** set on `grep`'s positional, but v1's enumerator never emits the
   bare-dash form.
3. **`cmp_specs.py`'s denominator** counts dataclass fields rather than arguments
   (binpash/caruca#54, open).
4. **`generate --full` renames every configuration it emits** — `to_exec_env("split", "varied")`
   against `(prefix, stdin_variation, content_variation)` puts `"split"` into `prefix`. All 175
   configurations of `cat` come out named `splitcat`.
5. **v1's own outputs are not stable against themselves** in two places: `Predicate` list fields
   are built from Python sets (order varies per process), and configuration `identifier`s are
   `random.choices(...)`. A naive comparison reports v1 disagreeing with v1 on every
   configuration.

---

## 10. What the instrument cost, and why it came first

Six defects in the *measurement* were found before any conclusion was drawn, four of them
before any money was spent. Three share one root cause worth naming:

> **v1's pydantic schema understates what v1 expects, because the real constraint lives in v1's
> code rather than in its type system.**

- `stdin` and `File.content` are `Content` behind a `PlainValidator`, which contributes nothing
  to `model_json_schema()`. They reached the model as **empty schemas**, so `null` read as legal.
- `node_type` and `arg_type` are discriminator tags with defaults, so pydantic omits them from
  `required` — but a discriminated union reads the tag *before* defaults apply.
- `Predicate.operator` is typed `str` with no enum, while v1's annotator emits exactly three
  operators. **The prompt never named `exists` or `len_args_eq`.** v2 invented
  `{"operator": "eq", ...}`, which v1's validator accepted and PaSh cannot interpret.

In each case the model was asked an unanswerable question, and in each case validation gave
false assurance. Three more were in the comparison rather than the request: the literal
invocation diff charged one convention difference to recall *and* precision; the ground-truth
annotation comparison diffed two different schemas so that a perfect answer scored zero; and
case alignment failed entirely between two artifacts written at different granularities.

**None of these are model failures, and all of them would have been reported as such.** That is
the argument for building the instrument before running the program.

---

## 11. The answer, stated plainly

**Are we doing exactly what v1 does?** At stage 1, yes — identical flag coverage, marginally
worse typing. At stage 2, v2 finds nearly all of v1's invocations and then asks for the wrong
world. At stage 3 it mostly does not finish: 78% of sessions execute the command once and then
answer in prose instead of reporting, so 15 of 27 cells yield nothing. At stage 4 it produces a
different specification and cannot process the largest inputs at all.

**Are we replicating, or improving?** Neither, yet — and the honest summary is that the study
mostly measured the instrument. Six defects in v1, three schema-understatement defects, and
three comparison defects were found and fixed before any stage produced a trustworthy number.
The numbers that survive say: **v2 reproduces v1's surface faithfully and its intent poorly.**

**What would change the answer.** The environment typing at stage 2 is one specific, diagnosable
error, not a diffuse weakness — the model does not know that a regex pattern is not a filename.
That is the first thing to test on a wider command set. Whether fixing it is instrument repair
or tuning is a judgement call that should be made explicitly, before it is made accidentally.

---

## Provenance

Every number traces to a ledger under `eval/campaigns/p1_*/`, a run directory with its
`prompt_hash` and full prompt text, v1 commit `d8032407346aadc135b14c043618c8c1d4f4e0cf`, and
model `openai/gpt-4o`. Method, defect history and the raw per-command tables are in
`ai_docs/tasks/008_v1_v2_parity_study.md`. The scorers are in `src/caruca_v2/harness/`, each
self-tested by scoring v1's own artifacts against themselves and requiring a perfect result.
