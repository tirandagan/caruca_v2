# The documents — what is where, and which one to open

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
| Understand how the system works | [`analysis/v2_fidelity_to_v1.md`](analysis/v2_fidelity_to_v1.md) | Mechanism by mechanism, each paired with the v1 mechanism it reproduces |
| Follow one command through both pipelines | [`docs/v2_chain_vs_v1.md`](docs/v2_chain_vs_v1.md) | Every file each stage reads and writes, with real contents |
| Actually run something | [`docs/caruca_v2_pipeline_usage_guide.md`](docs/caruca_v2_pipeline_usage_guide.md) | The v2 commands. For v1, [`docs/caruca_v1 pipeline instructions.md`](docs/caruca_v1%20pipeline%20instructions.md) covers Mac/Lima, WSL and native Linux |
| Pick up or start a piece of work | [`tasks/`](tasks/) | Numbered work orders, 001–012. Each carries its own status |
| Hand something to Prof. Greenberg or Prof. Eiers | [`docs/presentations/ASSEMBLY.md`](docs/presentations/ASSEMBLY.md) | What goes in the package, in reading order, and which PDF is current |
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
| [`docs/`](docs/) | **The operating documents**: how to run v2, how to run v1 on each machine, what the prompts contain, and the stage-by-stage walkthrough of one command through both pipelines |
| [`analysis/`](analysis/) | **What we found.** Results, arguments and experiment designs produced *by* this project. Has its own index — read that, not the filenames. `status_reports/` holds the dated advisor updates |
| [`diagrams/`](diagrams/) | The architecture diagram, in page and widescreen shapes, with the Graphviz source beside each |

### Handing over — documents for someone else to read

| Folder | What it holds |
|---|---|
| [`docs/presentations/`](docs/presentations/) | **The handout package.** Current PDFs at the top level, `build_decks.py` which regenerates the slide deck, and `ASSEMBLY.md` which lists what to include and in what order. Superseded PDFs are in `archive/` and must not be handed out. The live deck itself is in Dropbox, not here — `ASSEMBLY.md` says why |

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
