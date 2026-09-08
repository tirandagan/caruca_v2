# Handout package: what to convert and include

What to hand to Prof. Michael Greenberg and Prof. William Eiers alongside the slides. Every document
listed here is cited by name in a footnote on at least one slide, so a reader who follows a footnote
should find the matching PDF in the package.

Generated 29 August 2026, from the deck now kept in Dropbox as `2026-08-31 Review.pptx` (see The deck, below).

## File naming

Every generated PDF in this folder is prefixed with the ISO date it was created:
`YYYY-MM-DD_<name>.pdf`. The folder therefore sorts chronologically, and any handout can be traced
to the day it was produced without opening it. The numbered reading order below is the package
order and is deliberately *not* the same as the folder's sort order.

Dates come from when the document was first produced, not from the filesystem — every file on this
Mac reports a creation date of 2026-09-01, which is only when the repository was cloned here (see
[`dev_machine_paths`](../../../memory/dev_machine_paths.md) for the two-machine setup). Use the
first git commit that added the file, or today's date for something new.

Tooling and this index are deliberately unstamped: `build_decks.py` keeps its name so the
documented command below stays valid, and `ASSEMBLY.md` stays findable.

## The deck

26 slides, one deck for both advisors.

**The live deck is in Dropbox, not in this repository:**
`/03 Academic/Stevens/05 Research/Caruca/2026-08-31 Review.pptx`, with a PDF export
`2026-08-31 Review.pdf` beside it and the logo and fonts in the same folder. It was renamed from
`caruca_v2_status.pptx` to the review date when it moved there.

`build_decks.py` in this folder regenerates a deck from scratch as `caruca_v2_status.pptx`, but that
is **not** a substitute for the Dropbox copy. As the note at the end of this file warns, hand edits
made in PowerPoint are overwritten by the build script, and keeping a renamed copy is exactly how
you protect them — which is what the Dropbox filename is. Treat Dropbox as authoritative and the
script as the way to regenerate structure, not as a source of the current slides.

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

## Addendum — added after the August deck

These two documents postdate the deck and are **not cited on any slide**, so they sit
outside the "every document here is footnoted somewhere in the deck" rule that governs the numbered
list above. Include them when the conversation is about research framing rather than build status.
If they later earn slides, move them into the numbered list and record the slide numbers.

### 8. scientific_vs_engineering_contributions
- **Source:** `ai_docs/analysis/scientific_vs_engineering_contributions.md`
- **Needs converting.**
- **Covers:** which v2 directions count as publishable science versus product and engineering work.
  Nine ranked candidate contributions, a table of necessary-but-uncountable work paired with a
  salvage framing for each, and two proposed paper structures for the resubmission. Grounded in
  Shaw's ICSE acceptance data by result and validation type, and the SIGPLAN empirical-evaluation
  checklist.
- **Read it with:** `evaluation_gaps` — Part 4 says which of those fourteen gaps can be converted
  into results and which cannot.

### 9. experiment_designs
- **Source:** `ai_docs/analysis/experiment_designs.md`
- **Needs converting.**
- **Covers:** protocol-level designs for the experiments worth running, each with the infrastructure
  that already exists in v1, what still needs building, an effort estimate, and the null result that
  would falsify it. Opens with a blocking reproducibility check on the paper's own `grep`, `ps`, and
  `cp` claims.
- **Read it with:** `scientific_vs_engineering_contributions`, which it implements.

## Summary of what to do

- **Already PDFs, just copy:** `master_idea.pdf`, `caruca white paper.pdf`
- **Convert these five:** `system_architecture`, `roadmap`, `evaluation_gaps`, `component_functionality`,
  `data_telemetry_schema`
- **Addendum, also needs converting:** `scientific_vs_engineering_contributions`, `experiment_designs`

## Suggested order in the package

1. `2026-08-31 Review` — the deck (from Dropbox)
2. `master_idea` — the goal and the measures, which frames everything else
3. `system_architecture` — how the pieces fit
4. `roadmap` — what gets built and in what order
5. `evaluation_gaps` — the fourteen testing opportunities
6. `component_functionality` — component-level detail
7. `data_telemetry_schema` — recording and storage detail
8. `caruca_white_paper` — the original paper, last, as reference

Addendum, after the numbered package (not cited in the deck):

9. `scientific_vs_engineering_contributions` — what would make v2 publishable
10. `experiment_designs` — the experiments that follow from it

## Also in this folder

- `build_decks.py` — regenerates the deck from a single content definition. Run it with the project's
  virtual environment: `../../../.venv/bin/python build_decks.py`
- Diagrams live in `ai_docs/diagrams/`: `002_architecture_widescreen` is the version used in the slides,
  `001_caruca_v2_system_architecture` is the page-shaped version used in the printed document.

## If you edit the slides by hand

Editing the `.pptx` directly is fine, but re-running `build_decks.py` overwrites it. Either make your
changes in the script, or keep a renamed copy of anything you hand-edit.
