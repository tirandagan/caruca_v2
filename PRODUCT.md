# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

**Next.js** — the user's answer for all new UI work in this repo (asked during init, 2026-08-29). No UI
framework existed before this decision; the repo's only Node surface is the branded document pipeline
(`scripts/md-to-pdf/`: tsx + markdown-it + puppeteer + shiki + pdf-lib), which is unrelated to app UI and
stays as it is.

**Open:** the Eval Console's PTY streaming needs a long-lived Node process holding pseudo-terminals and a
websocket to the browser, which Next.js route handlers do not provide on their own. Whether that is a
custom Next server, a sidecar Node service, or a different arrangement is undecided. Do not invent one.

## Users

**Primary — Tiran Dagan, operating the tooling.** A PhD student running specification-mining comparisons
day to day. His job: generate a spec for a shell command by two different methods, diff both against
ground truth, and record what each run cost. He works from a WSL machine that cannot run the trace phase
(see Capabilities and Constraints), so the loop is: generate and analyze locally, ship tracing to a
provisioned host, bring results back. Optimize for his success first — dense telemetry, fast scanning,
repeated comparison runs.

**Secondary — advisors and reviewers.** Prof. Michael Greenberg (PhD advisor; also PI/advisor for Caruca
v1, and a co-author of the original paper) and Prof. William Eiers (PhD advisor; not involved in Caruca).
They judge whether the evidence supports a paper resubmission. They read results; they do not operate the
tooling.

**Secondary — prospective paper co-authors.** Evangelos Lamprou (Brown), Seong-Heon Jung (NYU), Mayank
Keoliya (UPenn), Lukas Lazarek (Brown), Konstantinos Kallas (UCLA), Nikos Vasilakis (Brown). Several
authored v1; framing that reads as "fixing v1's flaws" lands badly with this audience (see Brand
Commitments).

**Machine consumers.** PaSh, POSH, ShellCheck, and Shseer each expect their own annotation shape. Output
correctness is defined against their formats, not against human judgment.

## Product Purpose

caruca_v2 is a **research project, not a product for sale**. It determines, through instrumented
comparison, whether an LLM-based approach can match or exceed Caruca v1's hand-written pipeline at mining
partial specifications for opaque shell commands — rather than assuming it can.

Two objectives:

- **Near-term:** prove an LLM approach can do this at all, and measure its efficacy.
- **Longer-term:** produce evidence and documentation to revise and resubmit the Caruca white paper
  (arXiv:2510.14279), which was not accepted in its original submission.

Success is a defensible three-way comparison — v1 vs. a naive single-prompt LLM baseline vs. ground truth
— across six named evaluation dimensions, in a form usable directly in a paper.

## Positioning

The original Caruca paper is explicit that "the LLM solely generates the syntax specification — it is not
involved in any remaining components." Everything downstream — configuration generation, tracing
orchestration, specification derivation, four output adapters — is hand-written procedural code. That
asymmetry is this project's opening.

Two things caruca_v2 has that v1 does not, and that a neighboring project could not truthfully claim:

1. **It measures what the paper never measured.** v1 reports zero LLM cost, zero token counts, and never
   tests run-to-run reproducibility. caruca_v2 instruments both systems for tokens, dollars, wall-clock,
   model ID, and seed, and reports variance across repeated runs as a first-class result.
2. **It extends past v1's sweet spot on purpose, and labels it.** A `v1-faithful` profile replicates v1's
   fixture model exactly as the control; a `v2-extended` profile adds symlinks, permission states, deeper
   directory trees, correlated file content, pipe/SIGPIPE cases, and environment-variable variation. The
   two are always tagged separately in results, never blended into one average.

## Operating Context

**The v1 baseline lives outside this repo** at `~/stevens/caruca/` (upstream `binpash/caruca`, commit
`d80324073`). It is **private, unlicensed, and fork-restricted at the org level**. Referencing paths and
reproducing behavior is fine; copying its source into a public location is not.

**Four surfaces are in scope** (all four confirmed during init, 2026-08-29):

- **CLI — `caruca-v2`.** The primary instrument. Subcommand-per-stage, mirroring v1's shape:
  `baseline syntax-spec`, `naive-llm`, `sandbox generate|trace`, `augment`, `compare`, `web serve`. Every
  telemetry-producing subcommand takes `--out DIR`, defaulting to `eval/runs/<timestamp>/`. Integration
  with v1 is by **subprocess wrapping**, not library import.
- **Eval Console (web).** Backend spawns v1's CLI and `caruca-v2`'s subcommands each inside a PTY,
  streams both over websocket to two synchronized terminal panes (left = v1, right = v2), plus a metrics
  panel reading the telemetry JSON the CLIs already write. Purely a presentation layer over existing CLI
  surfaces — it computes nothing new. Design captured, build deferred behind the five priority components.
- **Results / project site.** For advisors and co-authors to read the three-way comparison,
  percent-change roll-ups, and the running "what changed between v1 and v2, and why" record.
- **Document & deck pipeline.** `scripts/md-to-pdf/` renders branded PDFs; `ai_docs/docs/presentations/`
  builds the advisor status deck. Supporting documents ship to advisors as PDFs alongside presentations,
  with an assembly list; documents are cited without file extensions.

**Work is staged into two tiers.** Tier 0: Baseline Instrumentation, Naive-LLM Baseline (plain docs only),
and the Evaluation Harness's syntax-spec comparison + telemetry + variance — no sandbox needed. Tier 1:
Secure Sandbox (both profiles), tool augmentation, real execution-based per-consumer evaluation, and the
Eval Console. Tier 0 is the near-term deliverable.

**Conventions that govern where work lands:** numbered task documents in `ai_docs/tasks/`; source material
in `ai_docs/refs/`; this project's own findings in `ai_docs/analysis/`; planning output in `ai_docs/prep/`;
cross-session memory in the in-repo `memory/` folder (indexed by `memory/MEMORY.md`), never Claude Code's
global memory store.

## Capabilities and Constraints

**Built today:** nothing of the pipeline. The planning passes are complete (master idea, component
functionality, telemetry schema, system architecture, roadmap) and the branded document/deck pipeline
works. Implementation starts at the roadmap's Phase 1.

**Two distinct "LLM approaches" are in scope and must never be conflated:**

1. **Naive-LLM baseline — the current deliverable.** One straightforward, few-shot-primed prompt: command
   binary + its documentation in, a specification in v1's own Python-DSL shape out. No agentic tool use,
   no validation or retry loop. Per Prof. Eiers, it is deliberately *not* engineered to be good — its
   purpose is to be a weak control that shows how much v1's engineered pipeline gains over an
   off-the-shelf prompt. Making it better defeats it.
2. **Agentic Claude Code / Agent-SDK full-pipeline rebuild — explicitly out of scope for now.** A later,
   separate experiment.

**Six evaluation dimensions.** This numbering is canonical; refer to dimensions by number in analysis
work, but never in prose for a human reader without saying what the number means.

1. Correctness/fidelity of produced specifications vs. baseline and ground truth
2. Cost/performance — wall-clock, tokens, dollars, for both systems
3. Coverage of command behaviors, flags, and configurations
4. Consistency/reproducibility across repeated runs
5. Percent-change roll-up — one headline delta per dimension above
6. Reduction in hand-encoded logic

**Hard environment constraints.** The dev machine is WSL and **cannot run the trace phase**: `strace`,
`mergerfs`/overlayfs, `docker`, and GNU `parallel` are absent, and system Python is 3.11 while v1 needs
≥3.12. `generate`, `annotate`, and `oracle` run fine locally. Tracing runs on a provisioned host; the
`Traces` JSON file is the seam that carries results back. Any sandbox backend must preserve
strace/ptrace-level syscall visibility.

**Known blocker.** v1's `caruca syntax-spec CMD` — its only LLM step — dies at import against DSPy 3.3.1
(the code targets DSPy ~2.4). Migrating it is a prerequisite for any live comparison, not an afterthought.
It also hardcodes `gpt-4o`; the model must be made configurable before any cost comparison runs.

**Terminology is exact and versioned, and blending conditions is a correctness error:** "v1" vs. "v2";
"naive-LLM baseline"; "v1-faithful" vs. "v2-extended" profiles; "plain docs" vs. "augmented docs";
"ground truth". Each is always labeled separately in results.

**Measurement discipline.** Any claim comparing the two approaches requires recorded evidence: command,
model ID, seed and temperature, token counts, wall-clock, hardware, and the exact baseline commit. Results
are written to files, not reported only in conversation.

**Undecided, on purpose — do not invent answers:** the sandbox isolation backend (Docker/overlayfs
extension vs. Firecracker vs. gVisor); the extended `Traces` schema versioning strategy; whether v1's
annotator gets extended to read v2-extended trace shapes; Eval Console build timing; and any concrete
target numbers for the six dimensions ("deliberately qualitative at this stage").

## Brand Commitments

**The `caruca-design` skill at `.claude/skills/caruca-design/` is the binding design authority** — the
user stated it "contains every aspect of our design guides." It holds the tokens, type, fonts, logo, UI
kit, and an `eval-console` kit. Read it before designing; do not re-derive or contradict it. Its visual
identity was extracted from this repo's own PDF pipeline (`scripts/md-to-pdf/styles.ts`, `cover.ts`,
fonts, logo), so it and the shipped documents are already one system.

**Name:** Caruca (the system); "Caruca v2" or `caruca_v2` (this project); `caruca-v2` (the CLI binary).

**Voice:** first-person researcher — "I want to determine…". Precise, and honestly hedged where a thing is
undecided. Claims are always qualified by methodology. Numbers carry their basis ("52/52", "+/-N% on
exact-match"). No emoji, no exclamation marks, no marketing superlatives; enthusiasm is expressed through
precision. Sentence case everywhere.

**Framing constraint (matters to real people):** in narrative writing for stakeholders — planning docs,
paper drafts, advisor summaries — frame v2 as **extending v1's capabilities, not fixing v1's flaws**.
Several reviewers and prospective co-authors wrote v1. Technical facts are still stated plainly; this
governs tone, not disclosure.

**Explanation constraint:** assume the reader has not read the underlying documents. Never use bare
internal shorthand ("dimension 6", "§7.2") without saying what it means. Link documents as optional
further reading rather than assuming they were read.

## Evidence on Hand

Real, verified, reusable. Do not fabricate substitutes for anything absent here.

- **The paper.** `ai_docs/refs/caruca white paper.pdf`, fully transcribed to
  `ai_docs/refs/caruca_white_paper.md` with figures in `ai_docs/refs/images/`. Authoritative for design
  intent and for the numbers this project must reproduce or beat.
- **Published baseline results** (GPT-4o, Xeon E5-2667 v2, Python 3.11): spec quality — PaSh 52/52, POSH
  16/17, ShellCheck 6/6, Shseer 18/18, 59/60 commands overall. LLM syntax-spec accuracy — 116/120 exact
  vs. ground truth. Real-world coverage — 651,733/666,468 invocations (97.78%) with normalization; 66,882
  (10%) exact match. Cost — with a ≤2-flag limit, 103/120 commands under an hour.
- **Ground truth, the most expensive input to the whole evaluation.** Two graduate students spent
  **80 person-hours** hand-annotating man pages. Concretely: 121 curated syntax specs, 54 committed
  reference PaSh annotations, and 13 benchmark ground-truth annotations under
  `~/stevens/caruca/benchmarks/annotations/`. Reuse it; never recreate it.
- **Existing evaluation tooling to reuse:** `eval/cmp_specs.py` (argument-by-argument spec diff — note its
  known denominator bug), `eval/llm_correctness.sh`, `eval/syntax-spec-correctness.sh` (an independent
  ASP/clingo cross-check for `rm`, `mv`, `cp`, `cat`, `mkdir`), and
  `eval/command-invocations.txt` (the real-world invocation corpus).
- **A free comparison set:** `~/stevens/caruca/outputs/llm-dsl-generation/*.py`, specs the v1 LLM step
  produced previously.
- **v1's true LOC split**, measured rather than taken from the paper: ~3,456 lines of hand-written
  pipeline logic and ~3,130 lines of generated spec data. The published 6,520 figure is roughly the sum.
  Dimension 6 ("reduction in hand-encoded logic") must be stated against ~3,456, with the split disclosed;
  measuring against 6,520 overstates the reduction by about 2×.
- **Absent — never invent:** cost, token, or wall-clock numbers for v1 (none exist anywhere yet; this is
  precisely what Phase 1 creates), reproducibility/variance figures for either system, pricing, licensing,
  deployment claims, user counts, or testimonials.

## Product Principles

1. **A measurement that isn't recorded didn't happen.** Every run emits its telemetry — tokens, cost,
   wall-clock, model ID, seed — alongside its output, automatically. Nothing is reconstructed after the
   fact.
2. **Never blend two conditions into one number.** v1 vs. naive-LLM, plain docs vs. augmented docs,
   v1-faithful vs. v2-extended: always labeled separately. An average across conditions destroys the exact
   thing this project exists to measure.
3. **Keep the weak baseline weak.** The naive-LLM control earns its meaning by staying naive. Improving it
   is a different experiment, and running it silently invalidates the comparison.
4. **A gap found is a result, not a defect to hide.** Where v1's unmodified annotator mishandles an
   extended trace shape, that is a reportable coverage finding. Surface it; don't design around it.
5. **Extend, don't indict.** v2's contribution is measured reach beyond v1's sweet spot. State facts
   plainly, and frame them as extension — the people reviewing this built v1.
