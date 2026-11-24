---
name: design-system-record
description: DESIGN.md (repo root) and .impeccable/design.json record the Caruca document identity as actually built in the 2026-11-24 report; the caruca-design skill stays the authority, DESIGN.md records the built deviations
metadata:
  type: reference
---
`DESIGN.md` at the repo root and the sidecar `.impeccable/design.json` were written on 2026-11-24 by the
impeccable documenter from the built report (`naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/`).
They record: the palette (ink on white, one blue for heads and the naive LLM's column, teal only on list
markers, one tint for the reference column and changed cells, the four-source family `--src-*`), the type
ramp as built (22/15/11pt headings against the skill's 28/20/15pt, named as deviations), print rules
(Letter, margins, page-break rules, running head/foot stamped with pdf-lib), and the named rules (one colour
per source, board whole, 72ch, flat paper). The `caruca-design` skill remains the binding authority
(PRODUCT.md); DESIGN.md describes what was built. Re-run the documenter after any later fix round so it never
describes a layout that no longer exists.
