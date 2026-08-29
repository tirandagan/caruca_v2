# Handout package: what to convert and include

What to hand to Michael Greenberg and William Eiers alongside the slides. Every document listed here is
cited by name in a footnote on at least one slide, so a reader who follows a footnote should find the
matching PDF in the package.

Generated 29 August 2026, from the decks in this folder.

## The two decks

| File | For | Slides |
|---|---|---|
| `caruca_v2_status_greenberg.pptx` | Prof. Michael Greenberg | 23 |
| `caruca_v2_status_eiers.pptx` | Prof. William Eiers | 24 |

Both decks share the same core. William's adds two plain-language background slides near the front, plus
one on why the comparison is worth running. Michael's adds two slides of technical detail: what gets
reused from Caruca unchanged, and one thing to fix in the comparison script. Everything else, including
all findings and all four closing questions, is identical in both.

Every slide carries speaker notes. Export those too if you want a reading copy for yourself.

## Documents to convert to PDF

Convert each Markdown file to PDF and include it. Slide numbers below are where each document is cited,
so you can check nothing is missing.

### 1. master_idea
- **Source:** `ai_docs/prep/master_idea.md`
- **A PDF already exists:** `ai_docs/prep/master_idea.pdf` — no conversion needed unless the source has
  changed since it was made.
- **Covers:** the goal, who the stakeholders are, the six measures of success, and the components to build.
- **Cited on:** Greenberg 2, 3, 5, 10, 12 · Eiers 2, 4, 5, 7, 12, 14, 15

### 2. system_architecture
- **Source:** `ai_docs/prep/system_architecture.md`
- **Needs converting.**
- **Covers:** how the existing and new pieces fit together, with the full architecture diagram and the
  open decisions.
- **Note:** this document embeds the tall, page-shaped version of the diagram, which is the right one for
  print. The wide version in the slides is the same diagram laid out for a screen.
- **Cited on:** Greenberg 4, 13 · Eiers 6

### 3. roadmap
- **Source:** `ai_docs/prep/roadmap.md`
- **Needs converting.**
- **Covers:** the six phases of work, what each one makes possible, what counts as finished for each, and
  what needs recording for the paper. The most cited document in both decks.
- **Cited on:** Greenberg 2, 3, 6, 7, 10, 11, 14, 15, 21, 22 · Eiers 2, 5, 8, 9, 12, 13, 15, 16, 22, 23

### 4. evaluation_gaps
- **Source:** `ai_docs/analysis/evaluation_gaps.md`
- **Needs converting.**
- **Covers:** all fourteen opportunities to broaden testing, split into ones the original authors did not
  raise and ones they acknowledge themselves, each with its source.
- **Cited on:** Greenberg 8, 9, 15, 19, 20 · Eiers 10, 11, 16, 20, 21

### 5. component_functionality
- **Source:** `ai_docs/prep/component_functionality.md`
- **Needs converting.**
- **Covers:** what each component takes in and produces, and the commands a researcher would actually type.
- **Cited on:** Greenberg 5, 9, 13, 21 · Eiers 7, 11, 22

### 6. data_telemetry_schema
- **Source:** `ai_docs/prep/data_telemetry_schema.md`
- **Needs converting.**
- **Covers:** exactly what gets recorded for every run, how comparison results are structured, and how
  results are stored.
- **Cited on:** Greenberg 12 · Eiers 14

### 7. caruca_white_paper
- **Source:** `ai_docs/refs/caruca_white_paper.md` (a Markdown transcription)
- **A PDF already exists:** `ai_docs/refs/caruca white paper.pdf` — the original. **Include the original,
  not a conversion of the transcription.** Note the filename contains spaces.
- **Covers:** the published paper, for reference.
- **Cited on:** Greenberg 6, 7, 19 · Eiers 3, 8, 9, 20

## Summary of what to do

- **Already PDFs, just copy:** `master_idea.pdf`, `caruca white paper.pdf`
- **Convert these five:** `system_architecture`, `roadmap`, `evaluation_gaps`, `component_functionality`,
  `data_telemetry_schema`

## Suggested order in the package

1. The deck for that advisor
2. master_idea — the goal and the measures, which frames everything else
3. system_architecture — how the pieces fit
4. roadmap — what gets built and in what order
5. evaluation_gaps — the fourteen testing opportunities
6. component_functionality — component-level detail
7. data_telemetry_schema — recording and storage detail
8. caruca_white_paper — the original paper, last, as reference

## Also in this folder

- `build_decks.py` — regenerates both decks from a single content definition, so the two versions cannot
  drift apart. Run it with the project's virtual environment:
  `../../../.venv/bin/python build_decks.py`
- Diagrams live in `ai_docs/diagrams/`: `002_architecture_widescreen` is the version used in the slides,
  `001_caruca_v2_system_architecture` is the page-shaped version used in the printed document.

## If you edit the slides by hand

Editing the `.pptx` files directly is fine, but re-running `build_decks.py` overwrites them. Either make
your changes in the script, or keep a renamed copy of anything you hand-edit.
