# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`caruca_v2` is a **research project**, not a product. Goal: reproduce the behavior of
**Caruca** — a miner of partial specifications for opaque shell commands — using an **LLM/agentic
approach (Claude Code + Claude Agent SDK)** in place of Caruca's hand-written procedural logic, and then
**evaluate the two systematically against each other**.

Lead: Tiran Dagan (PhD student). PI/advisor: Prof. Michael Greenberg; also Prof. William Eiers.

The comparison dimensions that drive every design decision here:

1. **Correctness/fidelity** of the produced specifications/annotations vs. baseline + ground truth
2. **Cost/performance** — wall-clock, tokens, $ (requires adding telemetry to *both* the baseline and the new system)
3. **Coverage** of command behaviors, flags, and configurations
4. **Consistency/reproducibility** across repeated runs (LLM nondeterminism is itself a result)
5. **How much hand-encoded logic** is eliminated for equal-or-better output

**Current state: greenfield.** Only scaffolding exists (`ai_docs/`, `.claude/`). No source code, no git
repo yet (`git init` has not been run). The near-term work per the project brief is: understand the
baseline, then build a **baseline + evaluation harness first**, before writing the LLM-driven version.
Do not skip to implementing the new miner without a measurable baseline to compare against.

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

## The baseline lives outside this repo

The implementation is at `~/stevens/caruca/` (git root; remote `binpash/caruca`, commit `d80324073`).
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
- `ai_docs/prep/` — project-planning output; `ai_docs/prep_templates/` and most of `ai_docs/dev_templates/`
  and `.claude/commands/` came from a **Next.js/Drizzle/Trigger.dev web-app starter kit and do not apply
  here**. Same for the `drizzle` / `typescript-react` / `trigger-dev-task-writer` agents in `.claude/agents/`.
  Ignore them unless a task genuinely calls for one; don't let their conventions leak into a Python research
  codebase.
- **Measurement discipline**: any claim comparing the two approaches needs recorded evidence — command,
  model ID, seed/temperature, token counts, wall-clock, hardware, and the exact baseline commit. Prefer
  writing results to files under `ai_docs/` or an `eval/` directory over reporting them only in chat.
