# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`caruca_v2` is a **research project**, not a product. Goal: reproduce the behavior of
**Caruca** — a miner of partial specifications for opaque shell commands — using an **LLM/agentic
approach (Claude Code + Claude Agent SDK)** in place of Caruca's hand-written procedural logic, and then
**evaluate the two systematically against each other**.

Lead: Tiran Dagan (PhD student). Two PhD advisors: Prof. Michael Greenberg (also the PI/advisor for
Caruca itself) and Prof. William Eiers (a PhD advisor to Tiran, but **not** involved in Caruca).

The comparison dimensions that drive every design decision here:

1. **Correctness/fidelity** of the produced specifications/annotations vs. baseline + ground truth
2. **Cost/performance** — wall-clock, tokens, $ (requires adding telemetry to *both* the baseline and the new system)
3. **Coverage** of command behaviors, flags, and configurations
4. **Consistency/reproducibility** across repeated runs (LLM nondeterminism is itself a result)
5. **How much hand-encoded logic** is eliminated for equal-or-better output

**Current state:** git repo initialized and pushed to `github.com/tirandagan/caruca_v2` (private). Only
scaffolding + this file exist so far — no pipeline code yet. The near-term work per the project brief is:
understand the baseline, build a **baseline + evaluation harness first**, then the **naive-LLM baseline**
(see below) — before attempting any agentic pipeline rebuild. Do not skip straight to an agentic rebuild
without a measurable baseline and a naive-LLM control to compare against.

## Two "LLM approaches" in scope — don't conflate them

Per Prof. Eiers' guidance (email thread with Tiran + Prof. Greenberg, Aug 2026), there are two different
systems in scope here, at very different levels of ambition, and the near-term deliverable is the
**simpler one**:

1. **Naive-LLM baseline — build this first.** A deliberately minimal, non-agentic system: one
   straightforward prompt telling an LLM what to produce, given a command's **binary + its documentation**
   as input, asked to directly emit a **specification in a downstream-consumable format** (comparable to
   Caruca's PaSh/POSH/SaSh/ShellCheck outputs). Include a handful of concrete worked examples in the
   prompt (few-shot) — similar in spirit to Caruca's own `llm.py` few-shot priming on `touch`/`rm`/`mv`/`ls`.
   Eiers was explicit: **do not** engineer this to be good — *"we don't want to have Claude try to min-max
   the perfect specification synthesizer... it would be another experiment."* Its whole purpose is to be a
   weak, naive control, so the evaluation can show *how much better* Caruca's engineered pipeline is over
   an off-the-shelf LLM prompt.
2. **Agentic Claude Code / Agent-SDK full-pipeline rebuild** (Tiran's original proposal — a **later,
   separate experiment**, not the current deliverable). This would replace every Caruca stage — config
   generation, tracing orchestration, spec derivation, adapters — with agentic LLM reasoning rather than a
   single prompt. Per Eiers' email, this is explicitly **out of scope for now**.

So the comparison to run first is **three-way**: Caruca (baseline) vs. the naive-LLM baseline vs. ground
truth (`~/stevens/caruca/benchmarks/annotations/`) — not yet Caruca vs. a full agentic rebuild. Telemetry
(tokens, cost, wall-clock, model ID) needs to be captured for Caruca's existing LLM step and for the
naive-LLM baseline alike, per the cost/performance dimension above.

## The paper is part of the codebase

`ai_docs/refs/caruca white paper.pdf` — *Caruca: Effective and Efficient Specification Mining for Opaque
Software Components* (Lamprou, Jung, Keoliya, Lazarek, Kallas, **Greenberg**, Vasilakis; arXiv:2510.14279,
Oct 2025). It is the authoritative statement of design intent and of the numbers this project must
reproduce or beat. Read it before proposing architecture. Extract text with
`pdftotext -layout "ai_docs/refs/caruca white paper.pdf" -` (write scratch output outside the repo).

Map of the paper to the code: §3 syntax inference → `llm.py` + `ir/syntax.py`; §4 configuration generator →
`ir/string.py` + `ir/environment.py`; §5 isolated tracing → `tracer/`; §6 specification derivation →
`tracer/data.py` + `annotator/`; §7 adapters/evaluation → the four output formats.

**Baseline numbers to measure against** (§7; 6,520 LOC Python, GPT-4o default, Xeon E5-2667 v2 / Python 3.11):

| Question | Result |
|---|---|
| Q1 spec quality per consumer | PaSh 52/52, POSH 16/17, ShellCheck 6/6, Shseer 18/18; 59/60 commands overall |
| Q2 LLM syntax-spec accuracy | 116/120 exact vs. ground truth (1 type misclassification, 3 missing/spurious options) |
| Q3 real-world coverage | 651,733/666,468 invocations (97.78%) with normalization; 66,882 (10%) exact match |
| Q4 cost | ≤2-flag limit: 103/120 commands < 1 hr, all but `convert` < 1 day. ≤4 flags: 80 < 1 hr, 24 > 1 day |

The Q2 ground truth cost **two graduate students 80 person-hours** of man-page annotation — that artifact is
the single most expensive input to the evaluation and should be reused, not recreated.

Known baseline limits (fair game as targets for the LLM approach): `git` is unsupported because
`.git`-style filesystem preconditions are outside the environment model; aggregators are not synthesized;
string normalization does not hold for content-sensitive commands (`xargs`, `nohup`); flag-combination
explosion dominates cost for wide-interface commands with simple semantics (`convert`).

## The baseline ("v1") lives outside this repo

Tiran refers to the original hand-written implementation as **v1** (this repo, `caruca_v2`, is **v2**) —
use that shorthand; "baseline" and "v1" mean the same thing throughout this file.

v1's implementation is at `~/stevens/caruca/` (git root; remote `binpash/caruca`, commit `d80324073`).
Read these before touching anything — they were verified by execution, not inferred:

- `~/stevens/caruca/caruca/CLAUDE.md` — baseline architecture (three-level IR, tracer, annotator, CLI)
- `~/stevens/caruca/caruca/CODE_INSIGHTS.md` — verified defects, latent bugs, env gotchas, with repro commands
- siblings of the package: `eval/`, `benchmarks/`, `outputs/`

Upstream `binpash/caruca` is **private, unlicensed, and fork-restricted at the org level** (the paper
announces a future MIT release; it hasn't happened). Don't copy its source into a public location or a
personal fork. Referencing paths and reproducing behavior is fine.

### Baseline pipeline — and where the LLM boundary currently sits

```
man page ──LLM(gpt-4o via DSPy)──► syntax spec (Python DSL)   ← the ONLY LLM step today
             │
             ├─ hardcoded ─► configuration generation (Syntax IR → String IR → Environment IR)
             ├─ hardcoded ─► execution + strace in an overlayfs sandbox  → Traces JSON
             └─ hardcoded ─► specification derivation → annotation (PaSh | POSH | SaSh | ShellCheck)
```

The paper is explicit that "the LLM solely generates the syntax specification — it is not involved in any
remaining components." That asymmetry is the research opening: everything downstream is explicit code in
`~/stevens/caruca/caruca/src/caruca/{ir,tracer,annotator}/`. This project asks how much of it an agentic
LLM pipeline can synthesize or replace.

Two structural facts that shape the comparison:

- The **trace ↔ annotate boundary is a JSON file** (`Traces` pydantic model). Tracing needs the sandbox
  toolchain; annotation does not. Keep that seam — it lets tracing run on a capable host while
  annotation/evaluation runs anywhere, and it gives a natural point to A/B the two annotators on
  *identical* trace input.
- Command registration is **reflective and name-coupled**: `syntax_specs/<cmd>.py` must define
  `<cmd>_syntax_spec`. Nothing else registers a command.

## Running the baseline

There is a working editable install at `~/stevens/caruca/caruca/.venv` (Python **3.12.9**):

```sh
CARUCA=~/stevens/caruca/caruca
source $CARUCA/.venv/bin/activate     # or call $CARUCA/.venv/bin/caruca directly

caruca generate CMD --number          # count invocations — ALWAYS do this before tracing; counts explode
caruca generate CMD                   # print invocation strings, no execution
caruca trace CMD --length-only        # count of executions a trace would perform
caruca trace CMD                      # execute+strace everything → outputs/CMD.json
caruca annotate pash CMD              # outputs/CMD.json → PaSh annotation (also: posh|sash|shellcheck)
caruca syntax-spec --fetch CMD        # show the committed syntax spec
caruca syntax-spec CMD                # LLM-generate one from the man page  ← currently BROKEN, see below
echo 'rm -rf /tmp/x' | caruca oracle  # coverage probe: can the spec parse this real invocation?

cd $CARUCA && ./run.sh                       # regenerate save/*.json for every PaSh command
cd $CARUCA && python -m pytest tests/unit    # fast, no sandbox; ~11 of 18 currently fail (stale API)
cd $CARUCA && python -m pytest tests/unit/test_syntax_ir.py::TestConcretization::test_single_flag -vv
```

Evaluation assets to reuse rather than rebuild:

- `~/stevens/caruca/benchmarks/annotations/pash/*.json`, `annotations/posh.txt` — ground-truth annotations
- `~/stevens/caruca/benchmarks/MILESTONES` — checklist of which PaSh commands are done
- `~/stevens/caruca/eval/cmp_specs.py` — argument-by-argument diff of two syntax specs (the §7.2 method)
- `~/stevens/caruca/eval/llm_correctness.sh` — batch-runs `cmp_specs.py` over all commands (needs GNU `parallel`)
- `~/stevens/caruca/eval/command-invocations.txt` — real-world invocation corpus behind the §7.3 numbers
- `~/stevens/caruca/outputs/llm-dsl-generation/*.py` — the LLM's previously generated specs (a free comparison set)
- `~/stevens/caruca/caruca/save/*.json` — committed reference PaSh annotations

## Environment constraints on this machine

This WSL box **cannot run the trace phase**: `strace`, `mergerfs`/overlayfs, `docker`, and GNU `parallel`
are all missing, and system Python is 3.11 (the package needs ≥3.12 — `tracer/tracer.py` uses a PEP 701
nested f-string). `generate`, `annotate`, and `oracle` work fine here.

Plan accordingly: do generation, annotation, spec-diffing, and analysis locally; run tracing on a
provisioned host (see `~/stevens/caruca/caruca/cloudlab-setup.sh`) and ship the `Traces` JSON back.
Isolation backend is selectable via `CARUCA_ISOLATION_METHOD` = `try` (default, vendored overlayfs script) |
`docker` | `none`. Timing comparisons against §7.4 are only meaningful on comparable hardware — record the
machine.

`caruca syntax-spec CMD` (the LLM path) **dies at import** against installed DSPy 3.3.1 — the code targets
DSPy ~2.4 (`dspy.OpenAI`, `dspy.Suggest`, `dspy.predict.Retry`, `assert_transform_module` all removed).
If the evaluation needs a live baseline LLM step, migrating `llm.py` is a prerequisite, not an afterthought.
It also hardcodes `gpt-4o` at `llm.py:110` — make the model configurable before running any cost comparison,
and record model IDs alongside every measurement. Note the paper's numbers are GPT-4o numbers; a fair
correctness comparison has to separate "better model" from "better method."

## Conventions in this repo

- **Task documents**: numbered markdown in `ai_docs/tasks/` (`NNN_snake_case.md`), created by the
  `task-creator` skill from `ai_docs/dev_templates/task_template.md`. Use them for multi-session work.
- `ai_docs/refs/` — reference material (the paper, upstream docs, transcripts) pinned for future sessions.
- `ai_docs/prep/` — project-planning output; `ai_docs/prep_templates/` came from a **Next.js/Drizzle/
  Trigger.dev web-app starter kit** and is being adapted one file at a time for this research project.
  `01_generate_master_idea.md` has been adapted (strips ShipKit/SaaS framing, reframes around this
  project's actual goal/stakeholders/components/evaluation criteria) — safe to run. `02` through `10` are
  still the original ShipKit content (app naming, UI theme, logo, Trigger.dev workflows, Drizzle schemas,
  etc.) and do **not** apply here as-is; most depend on knowing v2's system design, which isn't settled yet,
  so don't adapt them speculatively. `.claude/commands/0N_*.md` are thin `@`-reference wrappers around
  their `ai_docs/prep_templates/` counterparts — editing the template is enough, no need to update both.
  Most of `ai_docs/dev_templates/` (Drizzle migrations, Next.js refactors, Trigger.dev, Stripe/auth setup)
  is also starter-kit-specific and doesn't apply; `task_template.md` is closer to reusable but still has
  stack-specific sections to strip once real implementation starts. Same starter-kit origin for the
  `drizzle` / `typescript-react` / `trigger-dev-task-writer` agents in `.claude/agents/` — ignore them
  unless a task genuinely calls for one.
- **Measurement discipline**: any claim comparing the two approaches needs recorded evidence — command,
  model ID, seed/temperature, token counts, wall-clock, hardware, and the exact baseline commit. Prefer
  writing results to files under `ai_docs/` or an `eval/` directory over reporting them only in chat.
