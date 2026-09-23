# Analysis Index

Findings and evaluations produced *by this project* (as opposed to `ai_docs/refs/`, which holds
source material we didn't write — the paper, upstream docs, transcripts). Kept out of `CLAUDE.md`
itself so routine sessions don't load analysis content they don't need; link in from here instead.

| Document | What it is |
|---|---|
| [`v2_fidelity_to_v1.md`](v2_fidelity_to_v1.md) | Mechanism-by-mechanism account of how caruca_v2 works, each feature paired with the v1 mechanism it reproduces and marked IDENTICAL / DELIBERATE / DEFECT. Includes the consolidated deviation ledger and the commands to re-verify every claim. |
| [`evaluation_gaps.md`](evaluation_gaps.md) | 14 opportunities to broaden v1's / the paper's test & evaluation coverage (filesystem fixtures, content types, evaluation methodology), split into gaps the authors don't discuss vs. gaps they already flag themselves. |
| [`scientific_vs_engineering_contributions.md`](scientific_vs_engineering_contributions.md) | Which v2 directions are publishable science vs. product/engineering work, and why. Nine ranked candidate contributions (S1–S9), a table of necessary-but-uncountable work with salvage framings, and two proposed paper structures for the resubmission. Grounded in Shaw's ICSE result/validation acceptance data and the SIGPLAN empirical-evaluation checklist. |
| [`experiment_designs.md`](experiment_designs.md) | Protocol-level designs (E0-E6) for the candidates worth running, each with the infrastructure that already exists, what still needs building, an effort estimate, and the null result that would falsify it. E0 is a blocking reproducibility check on the paper's `grep`/`ps`/`cp` claims. |
| [`experiment_implementation_plan.md`](experiment_implementation_plan.md) | The E0-E6/S-candidate designs re-grounded in the implemented v2 (2026-09-06): per-experiment implementation + run plans, the evaluation-harness gap as a first-class finding (-> task 006), an adversarially-reviewed second cycle (observation-limited tracing promoted, per-stage fidelity study reframed, two new arms, demotions recorded), and the run matrix + cost estimate whose approval unblocks the result phases of tasks 001-004. |
| [`e0_artifact_pinning.md`](e0_artifact_pinning.md) | E0 results (2026-09-06): the paper's grep claim reproduces only against a pre-2021 PaSh revision (fixed 3.5 years before Caruca); the ps annotation is still wrong upstream today but ps is outside v1's shipped population; cp never had a hand-written annotation and 26 of 29 fresh cases contradict the paper's "pure" claim on main (the other 3 do not — see that document's 22 September corrections). Plus the population pin (120 vs 108) and the enumeration-redundancy sweep (82.7% duplicate invocations; --number wrong for 90/90 commands). |
| [`v1_v2_parity_study.md`](v1_v2_parity_study.md) | The v1-vs-v2 parity study (task 008, 2026-09-14): per-stage verdicts of replicates / diverges / improves on nine commands, with both sides measured by the same instrument at the same bound. Stage 1 replicates (identical flag recall); stage 2 diverges (0.878 invocation recall but 0.208 environment agreement, over the 24 cells where it is defined); stage 4 diverges and cannot process the two largest traces at all. Includes every confound, the places a disagreement pointed at v1 rather than v2, and why no figure is compared against a published one. |
| [`white_paper_addendum.md`](white_paper_addendum.md) | Proposed additions for the resubmission, written for the co-authors and following the paper's own section order. Eight proposals, two needing the authors' input: the shipped artifacts score 78/116 by Caruca's own cmp_specs against the published 116/120, and one specification defect that stands (grep --include is typed String where its siblings are Glob; a second, uniq's two-operand form, was listed in draft and has since been withdrawn inside that document). |
| [`status_reports/status_report_2026-09-22.md`](status_reports/status_report_2026-09-22.md) | Advisor status report for the 22 September 2026 meeting with Profs. Eiers and Greenberg: where the project stands, the parity-study findings in plain language, problems and solutions (Lima VM, schema repairs, self-corrections), what the work adds to the paper, proposed in-scope changes vs. follow-up study ideas, open questions, and what is left. PDF at `../docs/presentations/2026-09-22_status_report_v1.1.pdf` (the v1.0 PDF is in that folder's `archive/`). |

See also [`../docs/v2_chain_vs_v1.md`](../docs/v2_chain_vs_v1.md): one command followed
through both pipelines stage by stage — what each step reads, what it writes, where the file
lives and what is inside it. The concrete counterpart to the parity study's scores.

**Corrections of 22 September 2026.** Six documents carry a dated corrections note from an audit run
that day: `v1_v2_parity_study` (stage-4 figures recomputed; four statements corrected),
`white_paper_addendum` (section 5 re-framed), `v2_fidelity_to_v1` (how the paper measured PaSh;
the split-mode note), `e0_artifact_pinning` (two reasoning defects, verdicts unchanged),
`status_report_2026-09-22` (version 1.1), and `experiment_implementation_plan`. The recurring error:
the paper's PaSh quality figure was described as an execution test when it is a hand comparison, and
v1's cautious parallelizability classes were blamed on the flag bound rather than the trace mode.

Add new analysis docs here as they're produced, with a one-line description — don't inline their
content in `CLAUDE.md`.

## findings/

Since 22 September 2026, each conclusion this project reaches also lives as its own file in
[`findings/`](findings/) — one claim per file, with the numbers behind it, what each is counted
over, the campaign or runs it came from, and any correction it has been through.

The point is that they can be re-checked. The execution console recomputes each number with
today's scorer and reports whether it still holds, which the prose documents above cannot do.
Eleven were backfilled from `v1_v2_parity_study.md`, `e0_artifact_pinning.md` and
`memory/caruca_v1_stage1_baseline.md`; the documents remain the place the reasoning is written
out at length.
