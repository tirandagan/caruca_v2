<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!-- caruca_v2 analysis document. Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
     Licensed under the PolyForm Noncommercial License 1.0.0
     https://polyformproject.org/licenses/noncommercial/1.0.0
     Noncommercial use only. Commercial use is prohibited. -->
<!-- ATTRIBUTION-NOTICE:END -->

# Addendum to *Caruca* — Proposed Additions for the Resubmission

**To:** the Caruca co-authors
**From:** Tiran Dagan (Stevens), with Prof. Greenberg and Prof. Eiers
**Re:** arXiv:2510.14279, *Caruca: Effective and Efficient Specification Mining for Opaque
Software Components*
**Date:** 2026-09-14 · **Status:** draft for discussion, not a submission

---

## What this is, and what it is not

This addendum proposes material for the revised paper, drawn from a line of work that rebuilds
Caruca's pipeline with a language model in place of its hand-written logic and measures the two
against each other. Sections follow the paper's own structure so each proposal lands where it
belongs.

**It is not a critique of the system.** Every finding below was produced *by* Caruca — using its
specifications as ground truth, its enumerator as a reference, its models as validators and its
annotator as a comparison. A pipeline that can be reproduced closely enough to disagree with in
this much detail is a pipeline that was built well. Several findings are simply what happens
when a careful instrument is pointed at a system for the first time.

**Two proposals need the authors' input before they can be written up**, both marked 👤 below.

Supporting detail: [`v1_v2_parity_study.md`](v1_v2_parity_study.md) (technical comparative
report), [`e0_artifact_pinning.md`](e0_artifact_pinning.md) (artifact provenance).

---

## Summary of proposed additions

| # | Proposal | Paper section | Needs authors? |
|---|---|---|---|
| 1 | The LLM step's cost, tokens and reproducibility — currently unmeasured | §7 (new subsection) | no |
| 2 | Q2 as a *distribution*, not a single run | §7.2 | no |
| 3 | The shipped artifacts do not reproduce the 116/120 figure | §7.2 | 👤 **yes** |
| 4 | Specification validity versus specification *meaning* | §4 / §7 | no |
| 5 | An enumeration-redundancy and bound-sensitivity note | §4.2 | no |
| 6 | A soundness note on `Predicate.operator` and `CommandConfig.stdin` | §6.4 | no |
| 7 | What resists replacement by a model, and why | §8 or a new §9 | no |
| 8 | Two specification defects worth correcting | artifact appendix | 👤 **yes** |

---

## 1. The LLM step has never been costed — and it is now measurable (new §7 subsection)

The paper reports four evaluation questions; none of them measures the LLM step itself. Q4
measures the *tracing* cost — wall-clock per command under flag-count bounds — while the syntax
inference of §3 is reported only as an accuracy figure. That leaves the paper's central
efficiency claim resting on the part of the pipeline the paper does not price.

Measured on nine commands at a one-flag bound, `gpt-4o`, temperature 0:

| pipeline stage | LLM cost | the hand-written equivalent |
|---|---|---|
| syntax specification (§3) | $0.284 / 27 runs | — (this *is* the LLM step) |
| configuration generation (§4) | $1.354 / 27 runs | deterministic, sub-second |
| execution and tracing (§5) | ~$0.035 per 5 configurations | 17 seconds, **all nine commands** |
| specification derivation (§6) | $0.920 / 27 runs | under a second each |

**The comparison a reviewer will want is not "LLM versus free" but "LLM versus seconds".** v1's
entire side of this study — tracing and annotating all nine commands — took **17 seconds of wall
clock and no API spend**. That framing is more favourable to the paper than silence on the
question, and it forecloses the obvious reviewer objection that the costs were not reported.

**Recommendation:** add a short subsection to §7 reporting the syntax-inference step's token
count, dollar cost and wall clock per command, alongside Q4's tracing cost. The numbers are
small and the transparency is disproportionately valuable.

---

## 2. Q2 should be a distribution, not a single run (§7.2)

§7.2 reports 116/120 from one generation per command. An LLM step run once has no error bar,
and reviewers increasingly ask for one.

Running the same command three times at temperature 0 produces **identical results on eight of
nine commands** — and a **0.200 spread in exact-argument rate on the ninth** (`tac`). Temperature
0 is not determinism, and one command in nine is enough to make the point.

**Recommendation:** re-run §7.2 with k≥3 per command and report median with range. If the
spread is as small as it appears, this *strengthens* the result: it converts an unqualified
number into a measured one at negligible cost (the whole nine-command, k=3 sweep cost $0.28).

---

## 3. 👤 The shipped artifacts do not reproduce 116/120 (§7.2)

**This one needs the authors before anything is written.**

Scoring the committed LLM output (`outputs/llm-dsl-generation/*.py`, 117 specifications) against
the committed ground truth (`caruca/src/caruca/syntax_specs/*.py`), at `d8032407`:

| instrument | result |
|---|---|
| Caruca's own `eval/cmp_specs.py` — the §7.2 tool — `diff_count == 0` | **78 / 116** |
| an independently written structural scorer | **83 / 116** |
| the paper, §7.2 | **116 / 120** |

The instrument checks out: ground truth scored against *itself* is **117/117**, and two
independently built scorers land within five of each other. The signature is typing rather than
coverage — 105/116 commands have no missing or spurious options, but only 86/116 have no type
misclassification, against the paper's reported 3 and 1.

**The most likely explanation is simply that the committed set is not the run the paper
reported.** Drift explains less than expected: the LLM output and the ground truth were
committed a day apart, with only two subsequent specification commits. This is a
reproducibility gap in the artifact set, of the same kind E0 found for the `ps` and `cp`
claims — not evidence the measurement was wrong.

**Question for the authors:** which run produced the §7.2 figure, and can that artifact be
committed? A reader who re-runs `cmp_specs.py` on the shipped files today gets 78/116, and the
paper promises an MIT release. Either committing the reported run or noting that the shipped
specifications are a later regeneration would close this cleanly.

---

## 4. A specification can be valid and still mean the wrong thing (§4, §7)

The most useful thing this study found is a distinction the paper's evaluation does not
currently draw.

A model asked to reproduce §4's configuration generation produced invocation strings matching
Caruca's enumeration at **0.878 mean recall** — and environments matching at **0.185**. Every one
of its configurations passed `CommandConfig` validation. On `grep a relpath_1` it typed the
regex `a` as an *existing file*, asking the sandbox to contain a file named `a`, where Caruca
types it `no_env`.

Identical invocation string. Valid configuration. Different world. Nothing downstream objects;
the traces simply describe a filesystem that was never intended.

**Why this matters to the paper regardless of the LLM work:** §4.3's execution environments are
where a mined specification acquires its meaning, and the evaluation currently has no measure
for them. Q1 checks the derived specification against consumers; Q2 checks the *syntax*
specification against ground truth. Nothing checks that the environment a configuration
requests is the environment the command's arguments actually imply.

**Recommendation:** add an environment-level check to §7 — for a sample of commands, whether
each argument's `arg_type` matches its role. It is cheap, it is orthogonal to the existing
questions, and it closes a gap a reviewer could otherwise open.

---

## 5. Enumeration redundancy and bound sensitivity (§4.2)

Two measurements that bear on §4.2's combinatorics, both from Caruca's own enumerator:

**Redundancy.** Over 90 commands that enumerate fully, Caruca emits 3,261,075 invocations of
which 562,789 are distinct — **82.7% duplicates** (median 75.7%, max 92.9% on `who`). The tracer
inherits the duplicated stream. `--number` disagrees with actual emission for **90 of 90**.

**Bound sensitivity in the derived specification.** At a one-flag bound, Caruca's derived PaSh
annotations disagree with the hand-curated ones on parallelizability class in 62 of 83 cases —
and **58 of those 62 are Caruca being *more conservative* than the human annotators**
(`pure → non-pure` ×33, `stateless → non-pure` ×16) against 4 in the other direction. With less
evidence the system falls back conservatively, which is the right direction to fail in, but it
means a derived class is a function of the bound as much as of the command.

**Recommendation:** report the distinct-invocation count alongside the emitted count in §4.2,
and state in §6 that derived classes tighten with bound width. Both make the system look more
carefully characterised, not less capable — conservatism under thin evidence is a feature worth
claiming.

---

## 6. Two places where the schema does not enforce what the code requires (§6.4)

`Predicate.operator` is typed `str`. Caruca's annotator emits exactly three operators — `and`,
`exists`, `len_args_eq` — but any string validates. A model handed the schema produced
`{"operator": "eq", "operands": ["flag", "-b"]}`, which passed `PaSh` validation cleanly and is
meaningless to PaSh itself.

Similarly, `CommandConfig.stdin` is `Content` behind a pydantic `PlainValidator`, which
contributes nothing to `model_json_schema()`. Anything reading the schema sees an unconstrained
field; `null` appears legal and is not.

**This is not only an LLM problem.** Any third party generating annotations for a new
consumer — which §6.4's adapter design invites — faces the same false assurance: validation
passes, the consumer cannot use the output.

**Recommendation:** constrain `operator` to a `Literal` or enum, and give `SerializableContent`
a `__get_pydantic_json_schema__`. Two small changes that make the adapter contract
self-describing, worth a sentence in §6.4.

---

## 7. What resists replacement by a model (new §9, or §8)

The paper's §3 notes that "the LLM solely generates the syntax specification — it is not
involved in any remaining components." Attempting the remaining components gives that sentence
empirical content, which is publishable in its own right.

| Caruca stage | replaceable? | evidence |
|---|---|---|
| §3 syntax inference | **yes** | identical flag coverage, marginally worse typing |
| §4 configuration generation | **partly** | invocations yes (0.878); environments no (0.185) |
| §5 isolated tracing | **unresolved** | pilot perfect on a 2-interaction trace; wider run pending |
| §6 specification derivation | **no, at scale** | see below |

**§6 has a ceiling the hand-written implementation does not.** Caruca's traces for `rm` are
~211,000 tokens and for `tee` ~149,000, against `gpt-4o`'s 128,000-token window. The LLM
annotator cannot read them at all, while Caruca's annotator processes them in under a second.
The constraint scales the wrong way: **the more thoroughly a command is traced, the less able a
model is to derive a specification from the result.**

This is the strongest argument in the paper's favour that this work produced, and it is an
argument the paper cannot currently make because nobody had tried. A reviewer asking "why not
just use an LLM?" — and one will — can be answered with a measurement instead of an assertion.

**Recommendation:** a short section stating which stages a model can stand in for and which it
cannot, with the context-window result as the concrete limit. Framed as *what the architecture
buys*, not as a defence.

---

## 8. 👤 Two specification defects worth correcting (artifact appendix)

Found by disagreement, verified against Caruca's own behaviour. Both are small.

**`uniq` never generates its two-operand form.** `syntax_specs/uniq.py` declares
`[Path(), Path()]`, both taking the DSL's default `Arity.OPTIONAL`. The enumerator never emits
both operands when both are optional — verified identical at `--max-arity` 1 and 2 (the same 43
lines, at most one operand). `uniq INPUT OUTPUT` is therefore never traced. `cp`, `mv` and `ln`
are unaffected because each declares one mandatory positional. Likely fix: give `uniq`'s
positionals explicit arities.

**`grep --include` is typed `String` where its siblings are `Glob`.** `--exclude` and
`--exclude-dir` are `Glob` in the same specification; `--include` takes a glob in reality.

Two further items, already reported upstream or previously noted: `cmp_specs.py`'s
`correct_percentage` divides element counts by field counts (binpash/caruca#54, open), and
`generate --full` passes `"split"` into `to_exec_env`'s `prefix` parameter, renaming every
configuration it emits — all 175 of `cat`'s come out as `splitcat`.

**Question for the authors:** are these worth an artifact-appendix note, or better handled as
upstream fixes before the release?

---

## 9. What this addendum deliberately does not claim

- **No accuracy figure for the LLM pipeline.** Nine commands, one model, one temperature, one
  bound. Everything here is a direction, not a rate.
- **No cost saving.** The LLM pipeline is more expensive than the hand-written one at every
  stage measured. The interesting cost question is v1 versus the **80 person-hours** of manual
  annotation, and that comparison is not yet made.
- **No claim the §7.2 measurement was wrong.** §3 reports what the shipped artifacts do, and
  asks a question.
- **No stage-3 conclusion.** One pilot cell, on the easiest available trace.
- **Nothing about tuning.** The LLM side was never iterated to improve a score; defects in the
  *request* were fixed, and differences were reported.

---

## Provenance

Every figure traces to a campaign ledger under `eval/campaigns/p1_*/`, a run directory carrying
its full prompt and `prompt_hash`, Caruca commit `d8032407346aadc135b14c043618c8c1d4f4e0cf`, and
model `openai/gpt-4o` at temperature 0.0, seed 42. Comparison code is in
`src/caruca_v2/harness/`; each scorer is self-tested by scoring Caruca's own artifacts against
themselves and requiring a perfect result. Full method and defect history:
`ai_docs/tasks/008_v1_v2_parity_study.md`.
