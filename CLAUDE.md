# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Session memory

@memory/MEMORY.md

The file above is this project's persistent cross-session memory index (see "Persistent memory" under
Conventions, below, for what it is and how to maintain it). It's `@`-referenced here specifically so it
loads automatically every session, the same way this CLAUDE.md itself does — don't wait for a memory
entry to "look relevant" before reading it, the index is small by design. Each index line links to a
topic file under `memory/`; open a topic file only when the task actually touches what it covers.

## What this project is

`caruca_v2` is a **research project**, not a product. Goal: reproduce the behavior of
**Caruca** — a miner of partial specifications for opaque shell commands — using an **LLM/agentic
approach (Claude Code + Claude Agent SDK)** in place of Caruca's hand-written procedural logic, and then
**evaluate the two systematically against each other**.

Lead: Tiran Dagan (PhD student). Two PhD advisors: Prof. Michael Greenberg (also the PI/advisor for
Caruca itself) and Prof. William Eiers (a PhD advisor to Tiran, but **not** involved in Caruca).

The comparison dimensions that drive every design decision here. This numbering is canonical and matches
`ai_docs/prep/master_idea.md`'s "Evaluation Criteria & Success Definition" section — keep the two in sync,
and refer to them by number ("dimension 6") in analysis docs:

1. **Correctness/fidelity** of the produced specifications/annotations vs. baseline + ground truth
2. **Cost/performance** — wall-clock, tokens, $ (requires adding telemetry to *both* the baseline and the new system)
3. **Coverage** of command behaviors, flags, and configurations
4. **Consistency/reproducibility** across repeated runs (LLM nondeterminism is itself a result)
5. **Percent-change roll-up** — an explicit v1-vs-v2 delta per dimension above, giving one headline number each
6. **Reduction in hand-encoded logic** — how much procedural code is replaced for equal-or-better output
   on dimensions 1-4. Measure against v1's ~3,456 LOC of hand-written pipeline logic, **not** the paper's
   published 6,520 (which also counts ~3,130 LOC of LLM-generated spec data); see
   `memory/caruca_v1_loc_baseline.md`.

caruca_v2 serves two objectives: prove an LLM approach can do this at all and demonstrate efficacy
(near-term), and produce evidence/documentation to revise and resubmit the Caruca white paper — not
accepted in its original submission — incorporating v2's findings (longer-term). Write evaluation output
at paper-worthy rigor, not just internal notes.

**Current state (2026-09-22).** The planning passes are done (`ai_docs/prep/`: `master_idea.md`,
`component_functionality.md`, `data_telemetry_schema.md`, `system_architecture.md`, `roadmap.md`), **and so
is the pipeline.** All four v2 stages are built and run live (`src/caruca_v2/`, CLI `caruca-v2`, tasks
001-004), the measurement harness is built (`src/caruca_v2/harness/`: `score`, `sweep`, `report`, per-stage
scorers, task 006), the C0 pilot and the nine-command parity campaigns have been run against real models,
and the results are written up in `ai_docs/analysis/`. Spend so far is a few dollars. What has *not* run is
the experiment programme's campaigns C1-C6. Start any orientation at `ai_docs/analysis/README.md` and the
task list, not at this paragraph.

Work is staged into **Tier 0** (Baseline Instrumentation + naive-LLM baseline, plain docs + Evaluation
Harness's Q2-style comparison + telemetry + variance — no sandbox needed) and **Tier 1** (Secure Sandbox
both profiles, tool-augmentation, real execution-based per-consumer checks, Web GUI); see `memory/caruca_v2_build_tiering.md`
for why. Tier 0 is the near-term deliverable, and the DSPy migration on v1's `llm.py` is its hard
prerequisite. Do not skip straight to an agentic rebuild without a measurable baseline and a naive-LLM
control to compare against.

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
reproduce or beat. Read it before proposing architecture. A full Markdown transcription — every section,
Tab. 1, the DSL/math notation, and all figures (cropped out of the PDF's vector content, not full-page
screenshots) — lives at `ai_docs/refs/caruca_white_paper.md` with images in `ai_docs/refs/images/`; prefer
reading/grepping that over re-extracting from the PDF. Fall back to
`pdftotext -layout "ai_docs/refs/caruca white paper.pdf" -` only if the Markdown ever needs to be
regenerated or cross-checked (write scratch output outside the repo).

Map of the paper to the code: §3 syntax inference → `llm.py` + `ir/syntax.py`; §4 configuration generator →
`ir/string.py` + `ir/environment.py`; §5 isolated tracing → `tracer/`; §6 specification derivation →
`tracer/data.py` + `annotator/`; §7 adapters/evaluation → the four output formats.

**Baseline numbers to measure against** (§7; 6,520 LOC Python, GPT-4o default, Xeon E5-2667 v2 / Python 3.11):

| Question | Result |
|---|---|
| Q1 spec quality per consumer | PaSh 52/52, POSH 16/17, ShellCheck 6/6, Shseer 18/18; 59/60 commands overall. **Four numbers, three methods — never describe Q1 as "execution-based".** PaSh's 52/52 is a per-command *hand comparison* against PaSh's own hand-written annotations, restricted to invocations in PaSh's benchmark suite, counting parallelizable-pure and non-parallelizable-pure as one answer; POSH was diff-only ("we were unable to run it"); only ShellCheck (full 2.2K-test suite) and Shseer were genuinely re-run. A separate, **unnumbered** check swapped Caruca's annotations into PaSh and confirmed the suite's output by hash. Verified 2026-09-22 against §7.1 and Tab. 1; `ai_docs/tasks/012_pash_downstream_study.md` builds both halves |
| Q2 LLM syntax-spec accuracy | 116/120 exact vs. ground truth (1 type misclassification, 3 missing/spurious options). **Not reproducible from the shipped artifacts:** v1's own committed LLM specs score **78/116** by v1's own `cmp_specs.py` and 83/116 by an independent scorer (`memory/caruca_v1_stage1_baseline.md`). Use 78/116 as the stage-1 baseline; cite 116/120 only as the published figure |
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
- `~/stevens/caruca/eval/user-scripts/invocations.txt` — the real-world invocation corpus behind the §7.3
  coverage numbers: 665,628 lines, against the paper's 666,468 (the 840-line gap is unexplained).
  `eval/user-scripts/completeness_accumulate.sh` rebuilds it from `ShellExtractResults/` with the Go parser
  in `parser/`, runs `caruca oracle --full-match-only` over it into `oracle_results.txt`, then removes one
  normalization strategy at a time to get the per-level counts in `command_counts/`. Not
  `eval/command-invocations.txt`: that is a separate 659-line file of benchmark-script fragments
  (e.g. `[ ! -d ${IN}/bio ]`).
- `~/stevens/caruca/outputs/llm-dsl-generation/*.py` — the LLM's previously generated specs (a free comparison set)
- `~/stevens/caruca/caruca/save/*.json` — committed reference PaSh annotations

## Environment constraints — resolve by machine, there are two

**Check which machine you are on before applying anything in this section** (`memory/dev_machine_paths.md`).
The WSL PC uses `~/stevens/...`; this Mac uses `~/dev/stevens/...`. Paths elsewhere in this file are written
in the WSL form.

**The WSL PC** cannot run the trace phase: `strace`, `mergerfs`/overlayfs, `docker` and GNU `parallel` are
missing and system Python is 3.11 (the package needs ≥3.12 — `tracer/tracer.py` uses a PEP 701 nested
f-string). There, `generate`, `annotate` and `oracle` run fine.

**The Mac** can run everything, but only inside the Lima VM named `caruca` (Ubuntu 24.04; set up 2026-09-03,
`memory/mac_lima_tracing_env.md`, full operating instructions in `ai_docs/docs/caruca_v1 pipeline instructions.md`).
Two Mac-specific facts that contradict the WSL paragraph above: **`caruca annotate` cannot run on macOS at
all, on any input** (`tracer/data.py::__readwrite` resolves `/tmp` to `/private/tmp`, then calls
`relative_to("/tmp/sandbox_outer/sandbox_inner")` — `memory/caruca_v1_macos_annotate_limitation.md`), so
v2's `annotate` takes `--v1-runner lima`; and tracing needs no remote host.

**One trace-mode fact that is load-bearing for any parallelizability comparison, on either machine.** v1's
annotator assigns only `stateless`, `non-pure` or `side-effectful` — it never emits `pure`
(`tracer/data.py:215-225`) — and reaches `stateless` only from split-input traces. Those exist only under
`caruca trace --stdin split --content split`, which is what v1's own PaSh pipeline (`caruca/run.sh`) uses.
**At the `simple` default no command can be classified `stateless`, at any `--max-count`.** Comparisons made
at the default measure the trace configuration as much as the annotator.

Plan accordingly: do generation, spec-diffing and analysis locally; run tracing (and, on the Mac,
annotation) in Lima or on a provisioned host (see `cloudlab-setup.sh` in v1's tree) and ship the `Traces`
JSON back.
Isolation backend is selectable via `CARUCA_ISOLATION_METHOD` = `try` (default, vendored overlayfs script) |
`docker` | `none`. Timing comparisons against §7.4 are only meaningful on comparable hardware — record the
machine.

v2 will likely need stronger isolation than these for destructive commands (e.g. `rm`) and undocumented
binaries — candidate approaches (Firecracker, gVisor, bubblewrap) are scoped in
`ai_docs/prep/master_idea.md` under MVP Components; any candidate must preserve strace/ptrace visibility.

`caruca syntax-spec CMD` (the LLM path) **dies at import** against installed DSPy 3.3.1 — the code targets
DSPy ~2.4 (`dspy.OpenAI`, `dspy.Suggest`, `dspy.predict.Retry`, `assert_transform_module` all removed).
If the evaluation needs a live baseline LLM step, migrating `llm.py` is a prerequisite, not an afterthought.
It also hardcodes `gpt-4o` at `llm.py:110` — make the model configurable before running any cost comparison,
and record model IDs alongside every measurement. Note the paper's numbers are GPT-4o numbers; a fair
correctness comparison has to separate "better model" from "better method."

## Conventions in this repo

- **Task documents**: numbered markdown in `ai_docs/tasks/` (`NNN_snake_case.md`), created by the
  `task-creator` skill from `ai_docs/dev_templates/task_template.md`. Use them for multi-session work.
- **`ai_docs/README.md` is the map of every document in the project** — which folder answers which
  question, what each one is for, and the naming and corrections conventions. Written 2026-09-22 when the
  document set was reorganised. Read it before hunting through folders.
- `ai_docs/refs/` — reference material (the paper, upstream docs, transcripts) pinned for future sessions.
- `ai_docs/analysis/` — findings/evaluations produced *by this project* (as opposed to `refs/`, which is
  source material we didn't write). Start at `ai_docs/analysis/README.md` for the index — don't inline
  analysis content here in `CLAUDE.md`; link out to it instead so routine sessions don't load findings
  they don't need. Ten documents live there now, including the parity study, the co-author addendum and the
  experiment programme — the index describes each one, so read it rather than guessing from filenames.
- `ai_docs/prep/` — project-planning output; `ai_docs/prep_templates/` came from a **Next.js/Drizzle/
  Trigger.dev web-app starter kit** and is being adapted one file at a time for this research project.
  **Adapted, safe to run**: `01_generate_master_idea.md` (→ `ai_docs/prep/master_idea.md`, **done**),
  `05_generate_app_pages_and_functionality.md` (→ `component_functionality.md`, **done**),
  `08_generate_initial_data_models.md` (→ `data_telemetry_schema.md`, **done**),
  `09_generate_system_design.md` (→ `system_architecture.md` + `ai_docs/diagrams/`, **done**),
  `10_generate_build_order_worker.md` (→ `roadmap.md`, phases = MVP components done end-to-end, **done**).
  All five adapted passes are complete. **The starter-kit material that never applied was archived on
  2026-09-22** to `ai_docs/_archive/shipkit/` (see its README): prep passes `02`, `03`, `04`, `06`, `07`
  and the theme HTML, 17 of the 18 `ai_docs/dev_templates/`, the 22 slash commands that wrapped them, and
  all three `.claude/agents/`. **Do not go looking in the archive for guidance** — it is kept for the
  licence's attribution requirement and for provenance, nothing else. What remains is live:
  `ai_docs/prep_templates/` holds the five adapted passes, `ai_docs/dev_templates/` holds
  `task_template.md` (which the `task-creator` skill builds task documents from, and which still has
  stack-specific sections to strip), and `.claude/commands/` holds seven commands — the five prep
  wrappers plus `run_pipeline` and `setup_pipeline`. The `0N_*.md` wrappers are thin `@`-references to
  their `ai_docs/prep_templates/` counterparts; editing the template is enough.
- **v1-vs-v2 framing**: in narrative writing for stakeholders (planning docs, paper drafts, advisor
  summaries), frame v2 as extending v1's capabilities, not fixing v1's flaws — several co-authors/reviewers
  are v1's own authors. Technical facts (like the DSPy breakage above) still get stated plainly; this is
  about narrative tone, not suppressing facts.
- **Model/configuration selection is core v2 scope, not scope creep**: v1's behavior is fixed by
  hand-written code, so it has no configuration surface outside its one LLM call. Any v2 component that's
  NLP-based instead of hardcoded inherently needs a model, decoding parameters (e.g. temperature), and an
  output-format constraint chosen — these directly drive accuracy, consistency, and cost, so selecting and
  documenting them deliberately is part of the method, not an optional add-on. Keep it distinct from
  iterative tuning of a component's output to win a comparison, which stays out of scope per
  `memory/caruca_v2_baseline_scope.md` — "chosen once, up front, and frozen" is in scope; "iteratively
  refined" is not.
- **Template/skill attribution is mandatory and self-enforcing**: every file in `ai_docs/prep_templates/`,
  `ai_docs/dev_templates/`, `.claude/commands/`, and the `diagram` / `caruca-design` / `task-creator`
  skills carries an `ATTRIBUTION-NOTICE` block instructing the agent to print a credit block *before any
  other output*. Licensing is **PolyForm Noncommercial 1.0.0** (source-available, not OSI, not Creative
  Commons) — see `LICENSE-TEMPLATES.md` for scope and full text. That is the **repository-wide** license:
  it covers the research code (`src/`, `tests/`, `prompts/`, `scripts/`, `eval/`, `ai_docs/`) as well as the
  templates and skills. The filename is historical; only `ai_docs/refs/` and `.claude/skills/impeccable/`
  are excluded, as third-party work. Two rules when touching these files:
  - **Never strip the notice**, and keep it immediately after the YAML frontmatter (or at the very top when
    there is none). In `.claude/commands/*.md` the frontmatter `description:` must stay, or the slash
    command advertises the HTML comment as its description.
  - **Two credit variants, do not mix them up.** Files Tiran authored (prep `01`, `05`, `08`, `09`, `10`;
    the three skills; their command wrappers) say "Created by Tiran Dagan". Everything else began as
    **ShipKit** starter-kit material and uses the derived-work variant crediting ShipKit upstream, with
    copyright claimed only over Tiran's adaptations. New templates written from scratch get the original
    variant. The tell for existing files is mtime: `2026-08-25 22:09` is the ShipKit drop, `08-29` is
    Tiran's work.
- **Measurement discipline**: any claim comparing the two approaches needs recorded evidence — command,
  model ID, seed/temperature, token counts, wall-clock, hardware, and the exact baseline commit. Prefer
  writing results to files under `ai_docs/` or an `eval/` directory over reporting them only in chat.
- **Persistent memory lives in-repo, not in Claude Code's global store**: `memory/` at the repo root holds
  the cross-session notes that Claude Code's auto-memory feature would otherwise keep under
  `~/.claude/projects/<hashed-path>/memory/` outside the repo. Tiran wants everything about this project
  inside the project folder, so that store is not used here — `memory/` is the sole location. Start at
  `memory/MEMORY.md` for the index; each entry links to a topic file with the same frontmatter shape
  (`name`, `description`, `metadata.type` of `user`/`feedback`/`project`/`reference`) the harness's own
  auto-memory docs describe. When you'd otherwise write to the global auto-memory path, write here instead
  and update `memory/MEMORY.md`'s index — same read/write discipline (check before recommending from a
  memory that names a specific file/fact, update or remove stale entries, don't duplicate).
  - `memory/MEMORY.md` is `@`-referenced at the top of this file, so it loads on every session
    automatically — no need to go read it manually. Individual topic files under `memory/` are *not*
    auto-loaded; open one only when its `MEMORY.md` line looks relevant to the current task, same as the
    `ai_docs/analysis/` docs above.
  - **Update it proactively, without being asked.** Write a new or updated topic file whenever you learn
    something in one of these categories, in the same turn you learn it — don't wait for the user to say
    "remember this" — and add/update its one-line entry in `memory/MEMORY.md`:
    - **user**: something about Tiran's role, preferences, or knowledge that should shape how you explain
      or scope future work.
    - **feedback**: a correction ("no, don't do X") or a confirmed approach ("yes, that was right") —
      capture the *why*, not just the rule, so future sessions can judge edge cases.
    - **project**: a decision, deadline, stakeholder ask, or piece of context about the ongoing work that
      isn't derivable from the code or git history (e.g. who Greenberg/Eiers are and how they relate to
      Caruca vs. this project, or scope calls like the naive-LLM-baseline-first decision).
    - **reference**: a pointer to where something authoritative lives outside this repo (a path, a doc, an
      external system) that a future session would otherwise have to rediscover.
  - Skip anything derivable by reading the code, `git log`, or files already in the repo — memory is for
    facts that would otherwise be lost between sessions, not a second copy of the codebase.
  - If the user explicitly asks you to remember or forget something, do it immediately in that same turn.
