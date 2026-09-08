# Experiment Implementation Plan — Running the Science on the Implemented v2

**Written 2026-09-06.** This document is the third in a sequence. The first,
[`scientific_vs_engineering_contributions.md`](scientific_vs_engineering_contributions.md), argued
*which* v2 directions count as scientific contributions (nine candidates, labeled S1–S9). The
second, [`experiment_designs.md`](experiment_designs.md), turned the strongest of those into
protocol-level designs (seven experiments, labeled E0–E6). **Both were written before v2 existed as
code.** This document re-grounds every experiment in the system that now exists — the four-stage
LLM pipeline implemented 2026-09-03 — and answers three questions for each:

1. What does the implemented v2 already provide for this experiment?
2. What still has to be built, at the level of named files?
3. What exactly do we run, what does it cost, and what observation comes out the other end?

It also delivers a **second cycle** of experiment ideas — ones that only became possible once v2
was implemented — after putting each through the same scientific filters the first document
established (chiefly: *could the result have come out the other way, and would that result also
have been worth publishing?*). Ideas that fail the filter are named and demoted explicitly rather
than silently dropped.

Companion documents: [`v2_fidelity_to_v1.md`](v2_fidelity_to_v1.md) is the mechanism-by-mechanism
account of what v2 is; [`evaluation_gaps.md`](evaluation_gaps.md) catalogues the coverage gaps
several experiments convert into results. The build work this plan requires is captured as
**task 006** (`ai_docs/tasks/006_evaluation_harness.md`); the run campaigns it proposes are the
approval artifact in Part 6.

Everything below was verified against the actual code and repositories on 2026-09-06:
v2 at the current working tree (last commit `8a18aef`), v1 at
`~/dev/stevens/caruca` commit `d8032407346aadc135b14c043618c8c1d4f4e0cf`.

---

## Part 1 — The headline findings

### 1a. The verdict the second cycle was asked to deliver: there is enough

The existing program — the nine candidate contributions and seven experiment designs — survives
contact with the implemented system, and in several places got *easier* than the designs assumed
(details per-experiment in Part 4). The second cycle (Part 5) produced one genuinely new
experiment, one reframed study, and two extensions of existing designs; the remaining candidates
were correctly demoted to instrumentation by adversarial review. So the honest summary is:
**the science program is sufficient; the second cycle thickens it rather than replacing it.**
What stands between the current state and publishable observations is not a shortage of ideas —
it is that *nothing has been run yet*, plus one missing piece of measurement infrastructure.

### 1b. Nothing has been run — and one approval unblocks everything

As of today, `eval/` is empty: **zero live model calls have ever been made** through the v2
pipeline. All four stages are implemented, reviewed, and tested (149 tests, all green, with the
LLM and v1 both mocked), but every result-producing phase in tasks 001–004 is blocked on the same
single gate: an approved run matrix with a cost estimate. That approval artifact is **Part 6 of
this document**. Its bottom line, computed from measured prompt sizes rather than guesses: the
entire language-model side of the program — every campaign in this plan — costs on the order of
**a few hundred dollars**. Money is not the scarce resource here; person-time and Lima
(Linux VM) compute hours are.

### 1c. The missing infrastructure is itself a finding — and becomes task 006

Reviewing the experiments against the implemented code surfaced a precise gap. v2 measures
stage 2 and stage 4 against v1 automatically (invocation set-diffs in
`src/caruca_v2/stages/generate.py:107`, annotation diffs in `src/caruca_v2/stages/annotate.py:85,120`),
but:

- **Stage 1 — the headline stage — has no correctness comparison at all.** `caruca-v2 naive-llm`
  checks only that the generated specification *imports and validates* under v1's own interpreter;
  it never diffs the result against v1's committed specification or the hand-annotated ground
  truth. Without that scorer there is no accuracy number, and without an accuracy number there is
  no experiment.
- **There is no way to run a sweep.** Every run is one CLI invocation with one model and one
  temperature. Repeated-sampling variance, model comparisons, arm-by-arm campaigns — all of the
  designs below need a runner that drives the stages' typed `run()` entry points in a loop,
  handles rate limits *outside* the measured call (v2 deliberately never retries inside a
  measurement), and writes the standard run directories.
- **The mutated-documentation experiments need a mutation harness** that rewrites a man page and
  the corresponding ground truth *with the same transformation*, so the scorer can still judge
  the output.

These are not experiments; they are the instrument the experiments are performed with. Per
Tiran's direction they are recorded here as a first-class finding and specified as a single
coherent build in **`ai_docs/tasks/006_evaluation_harness.md`** (Part 3 summarizes the
components). Task numbering note: 005 remains reserved for the v1-instrumentation work that
`001_naive_llm_baseline_cli.md` already assigns to it.

### 1d. Groundwork already done for the blocking reproducibility check

The reproducibility check (E0 — "pin the artifacts") turned out to be cheaper than its design
assumed, because three of its open questions were resolved while preparing this plan
(read-only, 2026-09-06):

- The worry that the paper's numbers came from a diverged branch is **retired**: the
  `caruca-experiments` branch is v1's `main` plus two commits (a CLI crash fix and
  documentation), with no differences in any annotation or evaluation artifact, and the `paper`
  branch is fully contained in `main`.
- The paper's three named divergence claims (`grep`/`ps`/`cp`) **cannot refer to v1's local
  annotation copies**: the local `grep` annotation has handled `-c` since 2024-07-01 (before the
  paper), and no local `ps` annotation exists. They must refer to the upstream hand-written
  annotation set.
- That upstream, `github.com/binpash/annotations`, is **public with full history** (updated
  2026-01-26), so the archaeology can be done from this machine: did the corrections land
  *before* the paper (paper cited an older revision) or *after* it (Caruca's findings were
  adopted upstream — the stronger story)?

E0's remaining work and two additions it picked up from review are in Part 4.

---

## Part 2 — What the implemented v2 already provides, experiment by experiment

The 2026-09-03 build (tasks 001–004; mechanism-level account in
[`v2_fidelity_to_v1.md`](v2_fidelity_to_v1.md)) put the following capabilities in place. Each row
names the experiments that consume it — this is the map from "code that exists" to "science it
enables."

| Capability (with path) | What it is | Which experiments lean on it |
|---|---|---|
| Four typed stage entry points — `run()` in `src/caruca_v2/stages/{syntax_spec,generate,trace,annotate}.py` | Each pipeline stage is a plain function taking a client and returning a result object; the CLI is a thin wrapper. A harness can drive stages in loops without shelling out. | Every campaign in Part 6 |
| `--docs PATH` override on `naive-llm` (`src/caruca_v2/cli.py:113`) | Feed the model *any* documentation file instead of v1's committed man page | The memorization experiment (E2) — this flag is the injection point for renamed, permuted, ablated, and synthetic man pages |
| A/B-on-identical-inputs **by default** | Each stage defaults its input to the v1-produced artifact (v1's committed spec, v1's configs, v1's traces), so "LLM stage vs. hand-written stage on the same input" is the zero-flag behavior | The per-stage fidelity study (second cycle, Part 5) — its "isolation cells" are literally the default chaining |
| Built-in stage-2 and stage-4 comparisons (`generate.py:107`, `annotate.py:85,120`) | Invocation set-diff with the correct denominator (v1's actual emitted lines, not its misleading `--number` hint); structural + textual annotation diffs against fresh v1 output and against ground truth, each tagged with the comparison method | Per-stage fidelity study; the spec-holding study (E1) reuses the diff discipline |
| Telemetry that cannot fabricate (`src/caruca_v2/telemetry.py`) | Tokens/cost read from the API usage block or the run errors; full prompt + response in `manifest.json`; prompt identified by hash; `seed_honored` recorded honestly; SQLite cache rebuildable from JSON sidecars | Every cost/variance claim in every experiment |
| One access layer for all models (OpenRouter, `src/caruca_v2/llm.py`) | Same plumbing for every model family; GPT-4o pinned to OpenAI routing with fallbacks off, for comparability with the paper | Cross-model disagreement (S5b); model arm of configuration selection |
| No-retry discipline (`llm.py:7-9`) | A malformed response is a *measurement*, never retried | First-pass validity measurement; keeps the naive baseline honest per Prof. Eiers' guardrail |
| Frozen prompts with hashes (`prompts/README.md`) | Prompt wording is an experimental parameter; editing one is a new condition by construction | Prompt-form arm of configuration selection; prevents silent tuning during the per-stage study |
| Hard tool allowlist + isolation in stage 3 (`src/caruca_v2/tools.py`, `--isolation lima`) | The tracing LLM can only run the command under test and inspect the jailed workspace; destructive commands require the Lima VM | Observation-limited tracing (second cycle) — the restricted tool surface *is* the experimental condition |
| Working Lima VM for v1's full pipeline (`memory/mac_lima_tracing_env.md`) | v1 tracing verified end-to-end on this Mac (`ls`: 682 configs, 594 clean executions, 17,512 strace events) | Everything on the v1-as-instrument track: E0, E1, E3's sensitivity sweep, strace ground truth for stage-3 scoring |

Two constraints that shape run planning, also established by the build:

- **v1's `annotate` cannot run on macOS at all** (a hardcoded `/tmp` path assumption). The v1
  side of every annotation comparison runs inside the Lima VM (`--v1-runner lima`).
- **v1's `outputs/` holds traces for exactly one command (`ls`).** Any stage-4 or stage-3
  comparison beyond `ls` first needs v1 traces generated in Lima. The plan below folds that
  generation into the E0/E1 Lima sessions so the VM work is done once.

---

## Part 3 — The instrument to build first (task 006, summarized)

Full specification in `ai_docs/tasks/006_evaluation_harness.md`. Placement decision made there:
the harness lives **inside the package** (`src/caruca_v2/harness/`, surfaced as new CLI
subcommands) rather than as loose `eval/` scripts — v1's own loose evaluation scripts rotted
against its package API (11 of 18 v1 unit tests fail today for stale-API reasons), and
in-package code stays under the same test-and-lint regime as the pipeline. Components, in
build order:

1. **`src/caruca_v2/harness/score.py` (`caruca-v2 score`) — the stage-1 scorer.** Takes a generated specification,
   has *v1 itself* interpret it (the same subprocess pattern as `src/caruca_v2/v1.py` — v2 never
   re-implements v1 formats), normalizes it to an argument inventory (flags, aliases, arity,
   value types), and diffs that against a chosen reference. Two references, both supported:
   v1's 121 committed specifications and the 108 hand-annotated ground-truth JSON files
   (which population the paper's "120 commands" denominators refer to is pinned in E0).
   Two instruments, both reported and tagged: this structural diff (primary), and v1's own
   `eval/cmp_specs.py` (the paper's instrument — kept for comparability, with its known
   denominator bug documented in `memory/caruca_v1_eval_tooling_notes.md`; fix upstream as
   binpash/caruca#54, still open).
   **Design requirement from day one:** the reference source is parameterized by an optional
   *transform* — the renamed-documentation arms of the memorization experiment must score
   against ground truth renamed by the same map, and retrofitting that later means a rebuild.
2. **`src/caruca_v2/harness/sweep.py` (`caruca-v2 sweep`) — the campaign runner.** Drives the four `run()` functions over
   (commands × arms × models × k samples) from a declarative campaign file; enforces the
   configuration freeze (refuses to run a campaign tagged post-freeze with unfrozen
   parameters); handles rate limits and transient API failures *around* the measured call
   (backoff and re-queue — never inside a measurement, preserving the no-retry discipline);
   resumable, since sidecar run directories are durable.
3. **`src/caruca_v2/harness/mutate_docs.py` (`caruca-v2 mutate-docs`) — the documentation mutation harness.** Three transforms:
   consistent renaming of command + flag surface forms (seeded, with the rename maps committed
   as JSON — they are original work and contain no v1 text); semantic permutation (swap flag
   description bodies among same-shape flags); section ablation (SYNOPSIS-only / drop
   DESCRIPTION / drop EXAMPLES). Mutated pages are generated at runtime into gitignored
   `eval/docs_variants/` — derived man-page text never gets committed, same licensing posture
   as the rest of v2.
4. **`src/caruca_v2/harness/report.py` (`caruca-v2 report`) — aggregation.** Campaign roll-ups from the sidecars/`metrics.db`:
   accuracy with confidence intervals over samples, per-arm deltas, disagreement sets across
   samples, percent-change records in the shape `ai_docs/prep/data_telemetry_schema.md` defines
   (with its load-bearing `method` tag, so numbers from different comparison methods are never
   blended).
5. **`src/caruca_v2/harness/diff_annotations.py` — semantic annotation diff** (for the spec-holding
   study, E1): compares *parallelizability meaning* case-by-case, not JSON text.
6. **`src/caruca_v2/harness/assumption_sweep.py` — the sensitivity sweep** shared by the
   validity-domain experiment (E3) and, later, the fixture-axis study (E4): re-run v1 in Lima
   with one assumed-irrelevant dimension varied, and record whether the derived class changes.

Deliberately *not* in task 006: the witness generator (E1 phase 2) and the synthetic-tool
ground-truth generator (E5) — each is its own later task.

---

## Part 4 — The seven designed experiments, reviewed against the implemented system

Each entry: the question in plain language, what changed now that v2 exists, what to build, what
to run, what it costs, and what the resulting observation does for the paper. Effort estimates
are single-person calendar time and come from the original designs unless the review changed them.

### E0 — Pin the artifacts, and reproduce the paper's three divergence claims

**The question.** The paper reports, almost in passing, that three hand-written specifications
disagree with observed behavior: `grep` (marked always parallelizable-as-stateless, but `-c`
breaks that), `ps` (marked stateless, actually side-effectful), `cp` (marked side-effectful,
actually pure). Those three sentences are the seed of the whole resubmission argument, so before
anything is built on them we pin exactly which artifact revisions they refer to and confirm they
reproduce.

**What changed.** Three of E0's four open questions were already resolved while preparing this
plan (Part 1d): the branch question is retired, the local-copy question is answered (the claims
refer to the upstream annotation set), and the upstream repository is public and fully
clonable. E0 is now mostly *archaeology plus three reproduction runs*, not detective work.

**Picked up in review — two additions.**
- **The denominator pin:** v1 carries 120 man pages, 121 committed specifications, and 108
  hand-annotated ground-truth files. Which population is the paper's "120 commands"? Every
  accuracy figure this program publishes divides by that answer, so E0 settles it first.
- **The enumeration-redundancy count:** building v2 revealed that v1's invocation generator
  emits duplicates (`mkdir` at its defaults: 4,240 lines emitted, 1,094 unique) and that its
  `--number` count disagrees with what it actually emits (280 vs. 4,240). A small script sweeps
  all 120 commands and records hint / emitted / unique counts. This is instrumentation, not a
  result — but it corrects the cost accounting for any execution-count claims, feeds the
  adaptive-querying baseline later, and E0's Lima session is the natural place to run it.

**Run protocol.** (1) Clone `github.com/binpash/annotations`; walk the history of the grep, ps,
and cp annotations; date each correction relative to the paper (Oct 2025). (2) Settle the
108/120/121 denominator from the file sets plus the paper's own wording. (3) Run the redundancy
sweep (`generate --number` for all 120, full emission where counts are sane). (4) In Lima:
trace grep, ps, cp with v1 (`generate CMD --number` first — counts explode), derive annotations,
and diff against the pinned upstream revisions. While the VM is warm, batch-generate v1 traces
(`outputs/*.json`) for the small-trace commands the per-stage study needs later.

**Costs.** No model calls. One to two days; a few Lima CPU-hours.

**Results (run 2026-09-06, same day as this plan):** see [`e0_artifact_pinning.md`](e0_artifact_pinning.md) —
all three claims reached definite states, the population and redundancy questions are settled,
and two provenance questions (the paper's ps and cp runs) go to Prof. Greenberg.

**For the paper.** A provenance appendix an artifact-evaluation committee can follow, and — if
the upstream corrections postdate the paper — an *adoption* claim: the tool's findings were
already taken up by the annotation maintainers. Blocking for E1.

### E1 — How far do the hand-written specifications actually hold?

**The question.** Not "does Caruca match the annotations" (the paper answered that) but "how far
do the annotations themselves hold, and what happens downstream where they don't?" Run v1 as a
*differential oracle* over the complete shipped annotation sets of PaSh, POSH, ShellCheck, and
Shseer — not just each system's own benchmark subset — classify every disagreement, and for the
soundness-critical ones build a **witness**: a runnable script where the hand-written annotation
and the observed behavior lead a consumer to different outputs.

**What changed.** Nothing structural — E1 never needed v2's LLM stages; v1 is the instrument.
What v2 adds is discipline (the method-tagged comparison records) and the Lima environment that
makes v1 fully runnable on this machine. The upstream annotation sets being public removes the
last acquisition question.

**To build.** `src/caruca_v2/harness/diff_annotations.py` (semantic, case-by-case comparison of
parallelizability classes); the divergence taxonomy (over-general flag handling / missing
flag-conditional behavior / imprecise class / stale vs. installed version / **Caruca is wrong** —
that bucket must exist and be reported with equal prominence); the witness generator as phase 2
(concurrent split-invocation execution — the same machinery evaluation-gap 2 describes, which is
why that gap stops being "one more test mode").

**Run protocol.** After E0 pins revisions: batch v1 runs in Lima over every annotated command in
all four sets; diff per invocation case; classify; construct witnesses for divergences where
observed behavior is the more accurate account; verify witnesses by output-hash comparison (the
paper's own method).

**Costs.** No model calls. Lima CPU-days (bounded by `generate --number` checks per command);
two to three weeks person-time after E0.

**For the paper.** The motivating finding of the resubmission ("Paper A"). Null result — near-zero
divergence — is also publishable: it validates the crowd-sourcing premise those systems propose.
Diplomatic handling per the original design: the systems' authors are prospective co-authors, and
manual annotation being unable to avoid these errors *at scale* is the paper's own motivating
argument, now evidenced.

### E2 — Does the model read the documentation, or remember it?

**The question.** Coreutils man pages are in every frontier model's training data. Measured
accuracy on them may be recall, not reading. Four arms: (A) unmodified pages — reproduces the
paper's number; (B) renamed — `cat` becomes `zorp`, `-n` becomes `--enumerate`, semantics intact;
recall of names now actively hurts; (C) permuted — real names, swapped meanings; snapping back to
the real `cat` is the memorization signal; (D) synthetic tools from the ground-truth generator
(E5) — uncontaminated ceiling. Review added arm (E), the section ablation — see Part 5.

**What changed — this experiment got substantially cheaper.** The injection point exists
(`naive-llm --docs`); the model/temperature surface exists (required flags, OpenRouter); the
telemetry exists. What was "build a pipeline and a harness" is now "build the mutation harness
and the scorer." Arm A is not even a separate run: it *is* the baseline campaign (Part 6, C2).

**To build.** `mutate_docs.py` and the transform-aware scorer (Part 3, items 1 and 3). One design
decision to record: the four few-shot exemplars (`touch`/`rm`/`mv`/`ls` with their real
specifications) stay *unmodified* in arms B and C — they teach the specification language, which
is not the capability under test. That choice is stated in the write-up; an
exemplars-also-renamed sub-arm is cheap insurance if a reviewer asks.

**Run protocol.** Arms B, C, E over the full command population at k=5 samples each, frozen
configuration, scored under the matching transform; confidence intervals over samples (the
paper's 116/120 and 99.7% are single-run numbers — repeated sampling is itself an upgrade).

**Costs.** ~1,800 calls ≈ **$55** at GPT-4o prices (Part 6 math). One to two weeks including the
mutation harness.

**For the paper.** The standalone fast paper ("Paper B"), and the direct answer to the
"tested on training data" objection the SIGPLAN checklist tells reviewers to raise. Falsification
— accuracy holds under renaming and permutation — would be the *best possible* outcome for the
program: it would mean the method generalizes to undocumented in-house tooling.

### E3 — What does a mined specification actually guarantee?

**The question.** v1's coverage figure (97.78%) blends tiers of increasingly strong assumptions —
exact match, then path-, integer-, and string-content-agnosticism, then arity extrapolation —
implemented as filters but never given meaning. The experiment: state each extrapolation tier as
an explicit assumption about commands, derive each specification's *validity domain* from the
tiers used to build it (the formal half — paper work, no code), then **test each assumption
empirically**: for commands where string-agnosticism fired, does argument content ever change the
derived class? Same for arity and path naming.

**What changed.** Nothing is lost and one worry is retired: v2 does not implement v1's `oracle`
command, but E3 never needed it from v2 — the strategy instrumentation, the `--exclude` filters,
and the tier scripts all live in v1 and run under Lima. The sensitivity sweep
(`assumption_sweep.py`) is shared with the later fixture-axis study — build once.

**Run protocol.** From v1's oracle logs, list (command, strategy-fired) pairs; for each, re-run
v1 with the assumed-irrelevant dimension varied (content across the five fixture blobs, arity
counts grown, path names permuted); record the fraction of commands where the derived
specification changes. Output: the coverage figure *typed by assumption tier with measured
violation rates*, and a soundness-versus-coverage curve ("use only specifications at tier k or
stronger" priced in missed optimizations).

**Costs.** No model calls. Lima CPU-days; three to four weeks including the formal write-up.

**For the paper.** The technical core of the resubmission — the analytic model a programming-
languages reviewer looks for first, answering "what does it mean for your specification to be
correct, given that the hand-written ground truth is itself approximate?"

### E4 — Which fixture dimensions actually change the answer?

Unchanged from its design (ablate each unvaried fixture axis — symlinks, permissions, empty
content, integer magnitude, environment variables, nesting, correlated inputs, content types —
and measure which change derived specifications, for what fraction of commands). It shares E3's
sweep harness and runs after it. **One clarification recorded here so it isn't tripped over
later:** Tiran's 2026-09-03 "no extra files, no richer fixtures" directive governs the
*fidelity replication* — v2's stages must reproduce v1's environments exactly. E4 is a
deliberately *extended* experimental arm on the v1-side instrument, run and reported as such
(the `v2_extended` profile the telemetry schema already anticipates). Three to four weeks,
no model calls.

### E5 — A ground-truth generator, not a ground-truth set

Unchanged in design (synthetic CLI tools with man pages generated *from* the implementation;
ground truth correct by construction, contamination impossible), raised in priority by review:
it now unblocks *two* things — the memorization experiment's arm D and the decontaminated arm of
the observation-limited tracing study (Part 5), which needs binaries the model cannot already
know. Realism check against v1's real-world corpus stands. Two to three weeks, standalone,
community artifact.

### E6 — Downstream utility, and downstream harm

Unchanged (run PaSh/Shseer over the 177-script corpus with mined specifications; report *N* newly
analyzable scripts with measured speedups, and — the number that matters — *E*, the cases where a
mined specification changes a script's output). Still last: it wants E1's witness machinery and
E3's typed specifications settled first. Two to three weeks, mostly harness and runtime.

### S5 — Treat sampling disagreement as signal, not noise

The one first-document candidate that is *pure v2* and was not yet a numbered experiment design.
Sample the stage-1 specification k times; the intersection is a candidate under-approximation,
the union an over-approximation, and the **disagreement set is a free error-localizer**. Two
claims, tested in order: (1) disagreement predicts *where* the specification is wrong (against
ground truth) better than uniform suspicion; (2) spending execution budget on the disagreement
set beats spending it uniformly at equal cost.

**Implementation on v2.** Claim 1 falls out of the baseline campaign at no extra cost: C2
(Part 6) already collects k=10 samples per command; the scorer plus `report.py` compute
per-argument disagreement and correlate it with ground-truth error locations. Claim 2 needs the
execution path (v1's tracer in Lima, or stage 3) to spend targeted budget — sequenced after the
Lima warm-up, and *not promised from campaign data alone*. Review added a cross-model variant
(S5b, Part 5).

**For the paper.** The mechanism section of the resubmission: nondeterminism converted from a
threat-to-validity paragraph into the engine that directs execution budget.

---

## Part 5 — The second cycle: experiments the implemented v2 newly enables

Tiran's instruction was explicit: if the reviewed program is thin on scientific interest, generate
more. The candidates below exist *because* v2 was built — none could have been proposed from the
planning documents alone. Each was drafted, then put through an adversarial review against the
first document's own filters (the three reviewer questions; "could it have come out the other
way?"; Shaw's result-type acceptance data; the SIGPLAN empirical-evaluation checklist), with the
reviewer instructed to attack rather than admire. Verdicts first, details after:

| Candidate | Verdict |
|---|---|
| Observation-limited tracing (N3) | **Promoted — the strongest new experiment** |
| Per-stage fidelity study (N2) | **Promoted after reframing** (pre-registered, per-stage, never blended) |
| Documentation-section ablation | **New** — added as arm E of the memorization experiment |
| Cross-model disagreement (S5b) | **New** — added as an arm of the disagreement study |
| Prompt-form sensitivity (N4) | **Merged** into configuration selection — mandatory confound control, not standalone science |
| First-pass validity (N1) | **Demoted** to a reported measurement inside the baseline campaign |
| Enumeration redundancy (N5) | **Demoted** to instrumentation inside E0 |

### Promoted: observation-limited tracing — what can probing recover that interposition sees?

**The question.** v1 watches a command through `strace` — kernel-level interposition that sees
every file interaction. v2's stage 3 gives a model no such vantage: it may run the command
(argv[0] fixed to the command under test) and inspect the jailed workspace through `list_dir` /
`read_file` / `stat_path`, under a turn budget. That is a *different observation model* —
black-box probing with chosen inputs versus white-box interposition — and the question "how much
of the strace-derived specification is recoverable by probing, as a function of query budget?"
is a real information-access question, connected to the query-complexity framing the first
document gave the adaptive-mining idea (S4).

**What the review demanded, adopted in full.** The experiment is only science with an **analytic
recoverability ceiling** stated first: classify the seven interaction codes v1 records
(read/write/append/move/delete/make-dir/remove-dir) by what black-box probing can recover *in
principle* — state-diffing the workspace before and after recovers writes, creates, deletes, and
directory operations; *reads* are recoverable only indirectly, through content-marking
experiments (give files distinct contents, see which content shapes the output). The reported
result is then **fraction of ceiling achieved versus query budget** — a curve over turn caps
(3 / 7 / 15 / 30; the current default of 15 is arbitrary and must not be the only point), scored
against strace ground truth generated in Lima. Two further requirements: a **pre-registered
partial-credit scoring protocol** (task 003 explicitly deferred defining one; it must be fixed
*before* any run, or the scoring can be accused of being fitted to the results), and a
**decontaminated arm** on the synthetic binaries from the ground-truth generator — on `ls`, the
model may report what it *knows* rather than what it *probed*, and only unknown tools separate
those. One qualitative observation is worth recording alongside the numbers: whether the model
spontaneously invents content-marking experiments to expose reads.

**Cost.** Model-side ≈ $100–200 (tool loops are token-heavy: roughly 15 turns × ~2k tokens ≈
30k tokens per configuration, 5 configurations per command by default). Lima hours for strace
ground truth. The analytic ceiling is a few days of thinking and a table.

**Why it survives the filter.** Both outcomes are informative: near-ceiling recovery at small
budgets says specification mining does not need kernel access (deployability on platforms without
ptrace); a large stubborn gap says interposition is load-bearing and quantifies why. It doubles
as the stage-3 cell of the per-stage study below.

### Promoted, reframed: the per-stage fidelity study — which computations resist replacement?

**The question.** The paper's pipeline draws the LLM boundary at syntax inference and states the
rest is explicit code. v2 now has an LLM implementation of *all four* stages, each comparable
against its hand-written counterpart **on identical inputs by default**. The scientific version
of the "how much hand-written logic can be replaced" dimension is not a line count — it is:
*per stage, at fixed effort, how faithful is the LLM replacement, and does fidelity track the
kind of computation* (linguistic extraction vs. combinatorial enumeration vs. interactive
observation vs. deterministic aggregation)?

**What the review demanded, adopted in full.** Three disciplines. (1) **Pre-registration**: an
ex-ante prediction per stage, written down before any run (draft predictions below — to be
confirmed or amended by the team, then frozen). (2) **Per-stage metrics reported separately,
never blended into one "replaceability" chart** — blending strength tiers is exactly the sin the
validity-domain experiment indicts in the paper's 97.78%, and this study must not repeat it.
Metrics: stage 1 — argument-inventory F1 against ground truth; stage 2 — invocation-set recall/
precision against v1's enumeration (already implemented, `generate.py:107`); stage 3 — fraction
of the recoverability ceiling (the metric above); stage 4 — structural identity against v1's
annotator on identical traces (already implemented, `annotate.py:120`). (3) **Fixed-effort
protocol**: the no-retry, no-tuning guardrail extends to stages 2–4 for the duration of the
study, pre-empting "did you just try harder on the stage that looked bad?"

**Isolation vs. propagation — two different questions, kept apart.** *Isolation cells* run each
LLM stage on v1-produced inputs (the default chaining) and answer "can the stage be replaced?"
*Propagation runs* chain LLM stages end-to-end and answer "do errors compound or wash out?"
Isolation cells for stages 2–4 do **not** wait for the stage-1 campaign — they wait only on Lima-
generated v1 traces beyond `ls` (folded into E0/E1 Lima sessions) and the pre-registered stage-3
protocol. Propagation runs come after the baseline campaign.

**Draft ex-ante predictions (to confirm before freezing):** stage 1 high (the paper's own
result); stage 2 low on exact set-fidelity, degrading with invocation count (combinatorial
enumeration is a known model weakness — and the run design must bound it: enumeration output for
a command like `mkdir` runs to thousands of lines, so stage-2 cells run on the small-enumeration
command subset identified by E0's counting sweep); stage 3 mid, bounded by the analytic ceiling,
with reads under-reported; stage 4 mid-to-high on structure, brittle on exact case splits.

**Why it survives the filter.** Any per-stage outcome pattern was genuinely open before running,
and the result transfers: it tells anyone building "LLM replaces component X" systems which
component *kinds* to attempt. It is also the honest, measured answer to the reduction-in-
hand-encoded-logic evaluation dimension — replacing the line-count framing the first document
already ruled out as a contribution.

**Addendum (2026-09-08, directed by Tiran):** this study gains a second axis — *approach*.
Task 007 (`ai_docs/tasks/007_agentic_sdk_arm.md`) adds a per-stage toggle between the frozen
one-shot prompt and a Claude Agent SDK agentic arm (same information, added iteration), with a
plumbing-control arm in between, so the comparison becomes (stage × model × approach). The
one-shot control itself stays untouched, preserving the original design.

### New arm: documentation-section ablation (arm E of the memorization experiment)

Near-free once `--docs` and the mutation harness exist: feed SYNOPSIS-only, no-DESCRIPTION, and
no-EXAMPLES variants and measure where specification-relevant information actually lives in
documentation. Falsifiable both ways (SYNOPSIS suffices → interface extraction needs almost no
prose; long-tail prose is load-bearing → machine-readable docs need more than usage strings), and
it composes with the renamed arm — SYNOPSIS-only × renamed isolates pure structure-reading.

### New arm: cross-model versus within-model disagreement (S5b)

The single-plumbing OpenRouter layer makes this a flag change: same prompt, same harness, five
model families. Hypothesis: cross-family disagreement localizes ground-truth error better than
within-model resampling *at matched sample count*, because failure modes decorrelate across
families. Either outcome changes practice (multi-vendor ensembles versus cheap resampling), and
the result generalizes to any propose-and-verify pipeline.

### Merged and demoted — recorded so they are not re-proposed

- **Prompt-form sensitivity** (does the few-shot rendering and instruction paraphrase change
  accuracy?) is mandatory *methodology*, not a finding: it is the named mitigation for the two
  stage-1 confounds in the deviation ledger (`v2_fidelity_to_v1.md` §8.1 items 1 and 5) and runs
  as an arm of configuration selection, before any headline v1-vs-v2 stage-1 number. One figure
  in the methods section.
- **First-pass validity** (what fraction of never-retried responses are valid v1-DSL — i.e. what
  does v1's retry scaffolding actually buy?) is a *reported measurement* inside the baseline
  campaign, free. Its v1-comparison half additionally waits on task 005 (v1's LLM step is dead
  code against installed DSPy until repaired). Standalone it is a one-model, one-DSL
  observation — the "report" category Shaw's data shows accepted at 0%.
- **Enumeration redundancy** (v1's duplicate emissions) is instrumentation inside E0: a
  cost-accounting correction and, later, the baseline-inefficiency figure for adaptive querying.

### The sufficiency answer, stated plainly

The second cycle was asked for in case the reviewed program was thin. It is not thin. The
program that carries the resubmission is the one already designed — the spec-holding study (E1)
as motivation, validity domains (E3) as the technical core, disagreement-as-signal (S5) as
mechanism, downstream utility (E6) as validation, with the memorization study (E2) as the fast
standalone paper. The second cycle adds one genuinely new experiment (observation-limited
tracing), one reframed study (per-stage fidelity), and two cheap arms — a thickening of the
program, honestly reported as such.

---

## Part 6 — The combined program, and the run matrix to approve

### Two parallel tracks

**Track A — the model track** (spends tokens; blocked today on this Part's approval):

```
task 006 harness (scorer first, transform-aware from day one)
  → C0 pilot calibration (first live calls ever; replaces estimates with measurements)
  → C1 configuration selection on the 10 held-out commands   [prompt-form arm lives here]
  → FREEZE model/temperature/prompt                          [the project's chosen-once rule]
  → C2 baseline campaign (120 commands × 10 samples)         [arm A + validity + disagreement]
  → C3 mutation arms B/C/E   → C4 cross-model arm
  → C6 propagation runs (after C2; stage-3 cells after Lima ground truth)
```

The order is load-bearing in one place: **configuration selection precedes the 120-command
campaign**, never the reverse — running the big campaign first either silently *becomes*
selection or burns budget on a configuration that gets abandoned. The held-out subset
(`mkdir cp ln cat head sort uniq grep wc chmod`, task 001's Decision 3) exists precisely so
selection never touches the population being measured.

**Track B — the instrument track** (no tokens; only Lima hours and person-time; can start now):

```
E0 (archaeology + denominator pin + redundancy sweep + grep/ps/cp reproduction)
  → E1 (full-population spec-holding study; witness generator as phase 2)
  → E3(b) sensitivity sweep  → E4 later (shares the sweep harness)
E5 ground-truth generator: anytime, unblocks E2 arm D + the decontaminated tracing arm
during every Lima session: batch-generate v1 traces for the per-stage cells
```

### The run matrix (the approval artifact)

Cost basis, so the numbers can be checked rather than trusted: the 120 man pages average
~6.2 KB (~1,700 tokens); the stage-1 few-shot block (four exemplar man pages + specifications)
is ~22 KB (~6,000 tokens); so a stage-1 call is ~8–9k tokens in, ≤4,096 out (typical 200–800).
At GPT-4o's OpenRouter list price as of writing ($2.50/M input, $10/M output — **re-verify at
approval time**; the call counts below are price-independent) that is ≈ **$0.03 per stage-1
call**. Tool-loop (stage-3) calls are an order of magnitude heavier per command. C0 exists to
replace all of these estimates with measured numbers after twelve calls.

| # | Campaign | Runs | Model calls | Est. cost (GPT-4o basis) | Yields | Waits on |
|---|---|---|---|---|---|---|
| C0 | Pilot calibration | 3 per stage × 4 stages | 12 | < $1 | Measured per-stage token profile; live-plumbing shakeout | task 006 sweep runner |
| C1 | Configuration selection | 10 held-out cmds × 4 models × 2 temps × 2 prompt forms × k=3 | 480 | ≈ $15 | Frozen configuration; prompt-form confound measured | C0; scorer |
| C2 | Baseline campaign | 120 cmds × k=10, frozen config | 1,200 | ≈ $40 | Headline naive-baseline accuracy + CIs; first-pass validity; consistency/variance (evaluation dimension 4); within-model disagreement sets | C1 freeze |
| C3 | Documentation mutation (arms B, C, E) | 120 cmds × 3 arms × k=5 | 1,800 | ≈ $55 | The read-vs-remember curves; section ablation | C2 (uses its arm-A numbers); mutation harness |
| C4 | Cross-model disagreement | 120 cmds × 4 more families × k=5 | 2,400 | $30–150 (family-dependent) | Cross- vs within-model localization | C2 |
| C5 | Per-stage isolation cells | stage 2: ~30 small-enumeration cmds × k=3; stage 3: ~20 cmds × turn budgets {3,7,15,30}; stage 4: ~20 small-trace cmds × k=3 | ~700 (many multi-turn) | $150–350 (token-heavy loops; C0 recalibrates) | Per-stage fidelity; the budget-recovery curve | Lima traces; pre-registered stage-3 protocol; E0 counting sweep (picks the subsets) |
| C6 | Propagation runs | ~30 cmds full chain × k=3 | ~360 (multi-stage) | $100–200 | Error compounding vs. washing out | C2, C5 |
| — | Track B (E0, E1, E3, E5) | Lima + local | 0 | $0 | Motivating finding; technical core; ground truth | — |

**Program total, model side: ≈ $400–800.** Wall-clock: C2 and C3 are a few thousand short calls —
an afternoon each with modest parallelism in the sweep runner (rate-limit handling outside the
measured call). The scarce resources are person-time (harness ≈ 1–2 weeks; then the campaigns
interleave with Track B's multi-week studies) and Lima CPU-days.

**APPROVED by Tiran 2026-09-08 (all campaigns C0-C6 as tabled).** Approving this table unblocks the result phases of all four existing tasks at once
(001 Phase 7, 002 Phase 4, 003 Phase 5, 004 Phase 4 all name this approval as their gate).
Each campaign can also be approved or trimmed line-by-line; the dependency column says what a
trim takes with it.

---

## Part 7 — What each observation does for the white paper

The resubmission structures proposed in the first document ("Paper A" — the revised Caruca paper
built around *what a mined specification guarantees*; "Paper B" — the standalone
*read-vs-remember* study) map onto the campaigns like this:

| Observation (from) | Where it lands |
|---|---|
| Divergence rate + taxonomy + witnesses for hand-written specifications (E1) | Paper A's motivating section — replaces assertion with measurement; the `grep`/`ps`/`cp` paragraph grows into a study |
| Provenance + adoption evidence (E0) | Paper A artifact appendix; possibly a sentence in the introduction if upstream corrections postdate the paper |
| Typed coverage + assumption violation rates + soundness-vs-coverage curve (E3) | Paper A's technical core; retires the blended 97.78% presentation |
| Disagreement-directed budget results (S5, C2 + Lima phase) | Paper A's mechanism section; converts the nondeterminism caveat into the method |
| Downstream N and divergence count E (E6) | Paper A's validation; replaces the proxy metric the SIGPLAN checklist objects to |
| Accuracy-vs-contamination curves (E2 arms A–D, C2/C3) | Paper B, standalone; also one paragraph in Paper A answering the training-data objection |
| Section-ablation result (arm E, C3) | Paper B secondary finding (where interface information lives in documentation) |
| Per-stage fidelity + propagation (C5/C6) | The measured successor to the "reduction in hand-encoded logic" evaluation dimension, reported per-stage; frames v2 as *extending* v1's boundary-drawing with evidence about where the boundary belongs |
| Recoverability-ceiling curve (observation-limited tracing, C5) | Either a section of Paper A (observation models for mining) or the seed of a third, methods-focused paper |
| Cross-model localization (S5b, C4) | Generalization section of whichever paper carries S5 |
| First-pass validity; enumeration redundancy; cost telemetry | Methods and threats-to-validity material only — reported, never claimed as contributions |

## Part 8 — What this plan deliberately does not claim

Unchanged from the first document's discipline, restated because it now binds run reporting:
lines-of-code reduction, wall-clock speedups, and token bills appear in the papers only where
load-bearing (the query-complexity curve; the one automation-cost-versus-80-person-hours
comparison the original paper gestures at but never makes). The per-stage study is the *replacement*
for the line-count framing, not a vehicle for it. And every number this program publishes carries
its comparison-method tag (`q2_syntax_diff` / `annotation_diff` / `q1_execution`) — the three are
never blended.

---

## Provenance of claims in this document

- v2 implementation facts: verified against the working tree at commit `8a18aef` on 2026-09-06
  (paths cited inline; e.g. `cli.py:113` for `--docs`, `generate.py:107` and
  `annotate.py:85,120` for the built-in comparisons, `prompts/README.md` for the frozen-prompt
  rule, `trace.py:40` for the 15-turn default).
- v1 facts: `~/dev/stevens/caruca` at `d8032407346aadc135b14c043618c8c1d4f4e0cf`; branch
  comparisons run 2026-09-06 (`git log main..origin/caruca-experiments`, artifact-path diffs);
  local `grep` annotation history via `git log -- benchmarks/annotations/pash/grep.json`
  (unchanged since 2024-07-01).
- Upstream: `gh repo view binpash/annotations` on 2026-09-06 (public, updated 2026-01-26).
- Size/cost basis: `wc -c` over v1's 120 man pages (740,301 bytes total) and the four exemplar
  man pages + specifications (22,361 bytes), 2026-09-06; token conversion at ~3.7 bytes/token;
  GPT-4o OpenRouter list prices as of the knowledge cutoff, flagged for re-verification.
- The adversarial review of the second-cycle candidates was performed 2026-09-06 with full
  context of both parent documents and both implementation surveys; its verdicts are
  incorporated above in full (promotions, reframings, demotions, and the three execution-order
  corrections: selection-before-campaign, transform-aware scorer from day one, isolation cells
  decoupled from the baseline campaign).
