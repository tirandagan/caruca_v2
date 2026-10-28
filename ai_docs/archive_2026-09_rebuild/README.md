# Archive: the step-by-step rebuild (September to early October 2026)

**Dated material, moved here on 27 October 2026.** Before the naive-LLM experiment, this project rebuilt
Caruca's four steps one by one with GPT-4o (the "v2 pipeline": write the syntax description, generate test
command lines, run and trace them, write the behaviour description) and compared each step with Caruca.
These documents record that work. Their findings still stand as recorded, and the main ones are listed,
dated, in [`naive_llm_caruca/latest_findings.md`](../../naive_llm_caruca/latest_findings.md). But this
is no longer the project's focus, and some plans here were overtaken.

**The current work starts at [`naive_llm_caruca/README.md`](../../naive_llm_caruca/README.md).**

| File | Was at | What it is |
|---|---|---|
| [`analysis/v1_v2_parity_study.md`](analysis/v1_v2_parity_study.md) | `ai_docs/analysis/` | v2 pipeline vs Caruca, step by step, nine commands, three runs each |
| [`analysis/v2_fidelity_to_v1.md`](analysis/v2_fidelity_to_v1.md) | `ai_docs/analysis/` | How each part of the rebuild matches Caruca's code |
| [`analysis/white_paper_addendum.md`](analysis/white_paper_addendum.md) | `ai_docs/analysis/` | Proposals for the paper drawn from the rebuild (the naive-LLM addendum replaced it as the focus) |
| [`analysis/experiment_designs.md`](analysis/experiment_designs.md), [`analysis/experiment_implementation_plan.md`](analysis/experiment_implementation_plan.md) | `ai_docs/analysis/` | Planned experiments for the rebuild; most never ran |
| [`analysis/evaluation_gaps.md`](analysis/evaluation_gaps.md) | `ai_docs/analysis/` | Gaps in the paper's evaluation, found by reading Caruca's code |
| [`analysis/scientific_vs_engineering_contributions.md`](analysis/scientific_vs_engineering_contributions.md) | `ai_docs/analysis/` | Early framing of what could be published |
| [`analysis/reflections_on_caruca_v1_submission_reviews.md`](analysis/reflections_on_caruca_v1_submission_reviews.md) | `ai_docs/analysis/` | Reflections on the 2023 NSF grant-proposal reviews (not the paper's reviews) |
| [`analysis/status_reports/`](analysis/status_reports/) | `ai_docs/analysis/status_reports/` | Status reports of 22 September and 13 October |
| [`docs/v2_chain_vs_v1.md`](docs/v2_chain_vs_v1.md), [`docs/caruca_v2_pipeline_usage_guide.md`](docs/caruca_v2_pipeline_usage_guide.md), [`docs/caruca_v2_llm_prompts.md`](docs/caruca_v2_llm_prompts.md), [`docs/console_walkthrough_grep_rm.md`](docs/console_walkthrough_grep_rm.md) | `ai_docs/docs/` | Operating the rebuild: the chain beside Caruca, the CLI guide, the prompts inventory, a console walkthrough |
| [`docs/presentations/`](docs/presentations/) | `ai_docs/docs/presentations/` | The September handout PDFs and how they were assembled |
| [`diagrams/`](diagrams/) | `ai_docs/diagrams/` | The rebuild's system-architecture diagram, page and widescreen, with Graphviz sources |

Links inside these documents were rewritten for the move; links that were already broken before it were
left as they were.
