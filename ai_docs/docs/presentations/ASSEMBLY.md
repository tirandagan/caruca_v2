# Handout package: what to convert and include

What to hand to Prof. Michael Greenberg and Prof. William Eiers alongside the slides. Every document
listed here is cited by name in a footnote on at least one slide, so a reader who follows a footnote
should find the matching PDF in the package.

Generated 29 August 2026, from `caruca_v2_status.pptx` in this folder.

## The deck

`caruca_v2_status.pptx` — 26 slides, one deck for both advisors.

**Slides 3 and 4 are background** on what Caruca is and why the comparison is worth running. Skip them
when presenting live to Michael, who co-authored Caruca and does not need them. Walk through them with
William, who has no involvement with Caruca. They stay in the file either way, so the deck still makes
sense when read later without you. The speaker notes on both slides say this.

Every slide carries speaker notes written as what you would actually say. Export those if you want a
reading copy for yourself.

## Documents to convert to PDF

Convert each Markdown file to PDF and include it. Slide numbers below are where each document is cited,
so you can check nothing is missing.

### 1. master_idea
- **Source:** `ai_docs/prep/master_idea.md`
- **A PDF already exists:** `ai_docs/prep/master_idea.pdf` — no conversion needed unless the source has
  changed since it was made.
- **Covers:** the goal, who the stakeholders are, the six measures of success, and the components to build.
- **Cited on slides:** 2, 4, 5, 7, 12, 14, 17

### 2. system_architecture
- **Source:** `ai_docs/prep/system_architecture.md`
- **Needs converting.**
- **Covers:** how the existing and new pieces fit together, with the full architecture diagram and the
  open decisions.
- **Note:** this document embeds the tall, page-shaped version of the diagram, which is the right one for
  print. The wide version in the slides is the same diagram laid out for a screen.
- **Cited on slides:** 6, 15

### 3. roadmap
- **Source:** `ai_docs/prep/roadmap.md`
- **Needs converting.**
- **Covers:** the six phases of work, what each one makes possible, what counts as finished for each, and
  what needs recording for the paper. The most cited document in the deck.
- **Cited on slides:** 2, 5, 8, 9, 12, 13, 16, 17, 18, 24, 25

### 4. evaluation_gaps
- **Source:** `ai_docs/analysis/evaluation_gaps.md`
- **Needs converting.**
- **Covers:** all fourteen opportunities to broaden testing, split into ones the original authors did not
  raise and ones they acknowledge themselves, each with its source.
- **Cited on slides:** 10, 11, 18, 22, 23

### 5. component_functionality
- **Source:** `ai_docs/prep/component_functionality.md`
- **Needs converting.**
- **Covers:** what each component takes in and produces, and the commands a researcher would actually type.
- **Cited on slides:** 7, 11, 15, 24

### 6. data_telemetry_schema
- **Source:** `ai_docs/prep/data_telemetry_schema.md`
- **Needs converting.**
- **Covers:** exactly what gets recorded for every run, how comparison results are structured, and how
  results are stored.
- **Cited on slides:** 14

### 7. caruca_white_paper
- **Source:** `ai_docs/refs/caruca_white_paper.md` (a Markdown transcription)
- **A PDF already exists:** `ai_docs/refs/caruca white paper.pdf` — the original. **Include the original,
  not a conversion of the transcription.** Note the filename contains spaces.
- **Covers:** the published paper, for reference.
- **Cited on slides:** 3, 8, 9, 22

## Summary of what to do

- **Already PDFs, just copy:** `master_idea.pdf`, `caruca white paper.pdf`
- **Convert these five:** `system_architecture`, `roadmap`, `evaluation_gaps`, `component_functionality`,
  `data_telemetry_schema`

## Suggested order in the package

1. `caruca_v2_status` — the deck
2. `master_idea` — the goal and the measures, which frames everything else
3. `system_architecture` — how the pieces fit
4. `roadmap` — what gets built and in what order
5. `evaluation_gaps` — the fourteen testing opportunities
6. `component_functionality` — component-level detail
7. `data_telemetry_schema` — recording and storage detail
8. `caruca_white_paper` — the original paper, last, as reference

## Also in this folder

- `build_decks.py` — regenerates the deck from a single content definition. Run it with the project's
  virtual environment: `../../../.venv/bin/python build_decks.py`
- Diagrams live in `ai_docs/diagrams/`: `002_architecture_widescreen` is the version used in the slides,
  `001_caruca_v2_system_architecture` is the page-shaped version used in the printed document.

## If you edit the slides by hand

Editing the `.pptx` directly is fine, but re-running `build_decks.py` overwrites it. Either make your
changes in the script, or keep a renamed copy of anything you hand-edit.
