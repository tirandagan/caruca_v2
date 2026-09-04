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

Add new analysis docs here as they're produced, with a one-line description — don't inline their
content in `CLAUDE.md`.
