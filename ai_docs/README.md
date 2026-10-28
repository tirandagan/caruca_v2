# The documents — what is where, and which one to open

> **Start here (since 27 October 2026): [`naive_llm_caruca/README.md`](../naive_llm_caruca/README.md).**
> The project's current focus is the naive-LLM approach against Caruca. That page is the single
> entry point: the short observations document, the scores, every run and diagram, and which older
> material below is dated. Every finding, dated, newest first: [`naive_llm_caruca/latest_findings.md`](../naive_llm_caruca/latest_findings.md).
> On 27 October the naive-LLM documents moved into `naive_llm_caruca/`, and the September–October
> rebuild material into [`archive_2026-09_rebuild/`](archive_2026-09_rebuild/). The map below was
> written on 22 September for the rebuild; its folder table is updated, the rest is kept for history.

Written 22 September 2026. Everything caruca_v2 has written down lives under this folder, except
the cross-session memory notes (`../memory/`, indexed by `../memory/MEMORY.md`) and the four files
at the repository root.

The folder names come from how the material was produced, which is not how you will look for it.
**This page is the map.** It is organised by the three things the documents are for: building the
system, explaining it, and handing it to someone.

---

## Start here, by what you want

| If you want to… | Open | Why that one |
|---|---|---|
| Know what this project is and why | `../CLAUDE.md`, then [`prep/master_idea.md`](prep/master_idea.md) | Goal, the two advisors, the six comparison dimensions, what is in and out of scope |
| See what we have found | [`analysis/README.md`](analysis/README.md) | The index of results. Ten documents; it says in one line what each one settles |
| Understand how the system works | [`analysis/v2_fidelity_to_v1.md`](archive_2026-09_rebuild/analysis/v2_fidelity_to_v1.md) | Mechanism by mechanism, each paired with the v1 mechanism it reproduces |
| Follow one command through both pipelines | [`docs/v2_chain_vs_v1.md`](archive_2026-09_rebuild/docs/v2_chain_vs_v1.md) | Every file each stage reads and writes, with real contents |
| Actually run something | [`docs/caruca_v2_pipeline_usage_guide.md`](archive_2026-09_rebuild/docs/caruca_v2_pipeline_usage_guide.md) | The v2 commands. For v1, [`docs/caruca_v1 pipeline instructions.md`](docs/caruca_v1%20pipeline%20instructions.md) covers Mac/Lima, WSL and native Linux |
| Hand a fresh Claude Code session the task with no method hints | [`../naive_llm_caruca/README.md`](../naive_llm_caruca/README.md) | The naive Claude Code arm: a problem statement, two format descriptions and four v1 samples, and nothing else. Design record in [`tasks/016_naive_claude_code_arm.md`](tasks/016_naive_claude_code_arm.md) |
| Pick up or start a piece of work | [`tasks/`](tasks/) | Numbered work orders, 001–017. Each carries its own status |
| Hand something to Prof. Greenberg or Prof. Eiers | [`docs/presentations/ASSEMBLY.md`](archive_2026-09_rebuild/docs/presentations/ASSEMBLY.md) | What goes in the package, in reading order, and which PDF is current |
| Check the original paper | [`refs/caruca_white_paper.md`](refs/caruca_white_paper.md) | Full transcription with figures. Prefer it over re-extracting the PDF |

---

## The folders

### Building — documents that drive work

| Folder | What it holds |
|---|---|
| [`tasks/`](tasks/) | **The work orders.** `NNN_snake_case.md`, created from `dev_templates/task_template.md` by the `task-creator` skill. 001–004 are the four pipeline stages, 006 the measurement harness, 008 the parity study, 009–012 specified but not built. **005 is reserved** for instrumenting v1 and stays a gap on purpose |
| [`prep_templates/`](prep_templates/) | The five planning passes that were adapted and run. They are the provenance for the five documents in `prep/` — kept so a reader can see how those were produced |
| [`dev_templates/`](dev_templates/) | `task_template.md` only. Everything else went to the archive |

### Explaining — documents that describe what exists

| Folder | What it holds |
|---|---|
| [`prep/`](prep/) | **The design documents**, from the planning passes: the master idea, per-component inputs and outputs, the telemetry and comparison-record shapes, the system architecture, and the roadmap. These are stable; they describe intent |
| [`docs/`](docs/) | **The operating documents still in use**: how to run v1 on this Mac (Lima VM) and how to run PaSh; plus the 2023 NSF proposal reviews |
| [`analysis/`](analysis/) | **Background that still holds**: the paper-claims check (E0), what Caruca is for (the `grep` case), PaSh's work scheduling. `findings/` is the console's findings folder |
| [`archive_2026-09_rebuild/`](archive_2026-09_rebuild/) | **Dated (moved here 2026-10-27):** the September–October step-by-step rebuild: parity study, v2 fidelity, the rebuild's addendum, experiment designs and plan, evaluation gaps, status reports, v2 operating docs, the September handouts and the architecture diagrams. Kept for history; not the current focus |

The naive-LLM experiment's documents (start page, observations, dated findings, addendum, syntax-files
comparison, diagrams) live with the experiment in [`../naive_llm_caruca/`](../naive_llm_caruca/README.md).

### Handing over — documents for someone else to read

| Folder | What it holds |
|---|---|
| [`archive_2026-09_rebuild/docs/presentations/`](archive_2026-09_rebuild/docs/presentations) | **The September handout package (dated).** Current PDFs at the top level, `build_decks.py` which regenerates the slide deck, and `ASSEMBLY.md` which lists what to include and in what order. Superseded PDFs are in `archive/` and must not be handed out. The live deck itself is in Dropbox, not here — `ASSEMBLY.md` says why |

### Material we did not write

| Folder | What it holds |
|---|---|
| [`refs/`](refs/) | The Caruca paper (PDF plus a full markdown transcription and its 82 figures) and Prof. Eiers' dissertation. Authoritative for design intent and for the numbers this project must reproduce or beat |

### Not part of the project

| Folder | What it holds |
|---|---|
| [`_archive/`](_archive/) | Starter-kit residue from the Next.js template this repository began as, archived 2026-09-22. Kept for the licence's attribution requirement and for provenance. **If anything there contradicts a document outside it, the one outside is right** |

---

## Two conventions worth knowing

**Naming tells you which kind of document you are holding.** A handout carries a date and a version
in its filename (`2026-09-22_status_report_v1.1.pdf`), so a superseded copy is obvious at a glance.
A findings document keeps a stable filename and carries its version *inside*
(`v1_v2_parity_study.md`, "Version 1.1 — corrected 22 September 2026"), so citations to it do not
rot. Task documents are numbered once and never renumbered.

**Corrections are dated and kept, never silently rewritten.** When a figure or a claim turns out to
be wrong, the document gets a version bump, a note at the top, and a corrections table at the
bottom saying what it used to say and why that was wrong. Nine documents carry one from the
22 September 2026 accuracy audit. If you are quoting a number from any document here, check
whether it has a corrections section first.
