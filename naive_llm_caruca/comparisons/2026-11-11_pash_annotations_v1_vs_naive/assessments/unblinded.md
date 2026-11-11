# Assessments with the letters revealed

Made by `score_pash.py unblind` from the assessments' front matter and the keys. Ratings are the assessor's, unchanged.

| Command | Side | Letter | Inputs/outputs right | Answers given | Splitting safe | Splitting allowed | Parser table | Confidence |
|---|---|---|---|---|---|---|---|---|
| cat | v1-pash | A | medium | low | safe | medium | wrong | high |
| cat | naive:2026-10-28_100411 | B | high | high | unsafe | high | good | medium |
| cat | pash-own | R | high | high | none_offered | none | good | high |
| cp | naive:2026-10-28_114133 | A | medium | high | none_offered | none | gaps | high |
| cp | naive:2026-10-28_150709 | B | high | high | none_offered | none | gaps | high |
| cp | naive:2026-10-28_153913 | C | high | high | none_offered | none | gaps | high |
| cp | v1-pash | D | low | low | none_offered | none | wrong | high |
| cut | naive:2026-10-27_230555 | A | medium | high | safe | high | good | high |
| cut | v1-pash | B | high | low | safe | low | gaps | high |
| cut | naive:2026-10-28_145447 | C | medium | high | safe | high | good | high |
| cut | naive:2026-10-28_152550 | D | medium | high | safe | high | good | high |
| cut | v1-main | E | high | low | safe | low | good | high |
| cut | naive:2026-10-20_135253 | F | medium | high | safe | high | good | high |
| cut | pash-own | R | medium | high | unsafe | high | good | high |
| grep | naive:2026-10-28_135447 | A | medium | high | unsafe | high | gaps | medium |
| grep | naive:2026-10-20_112956 | B | medium | high | unsafe | high | gaps | medium |
| grep | naive:2026-10-13_193448 | C | high | medium | safe | high | good | medium |
| grep | v1-pash | D | low | low | safe | low | wrong | high |
| grep | pash-own | R | medium | high | unsafe | high | gaps | high |
| rm | naive:2026-10-20_121932 | A | high | high | none_offered | none | gaps | high |
| rm | v1-main | B | high | medium | none_offered | none | gaps | high |
| rm | naive:2026-10-28_105951 | C | medium | high | none_offered | none | gaps | high |
| rm | v1-pash | D | medium | low | none_offered | none | wrong | high |
| rm | pash-own | R | medium | high | none_offered | none | gaps | high |
| sort | naive:2026-10-28_151151 | A | high | high | broken | low | gaps | high |
| sort | v1-pash | B | low | low | unsafe | low | wrong | high |
| sort | naive:2026-10-28_154444 | C | high | high | broken | low | gaps | high |
| sort | naive:2026-10-20_160340 | D | high | high | broken | low | wrong | high |
| sort | v1-main | E | medium | low | unsafe | low | wrong | high |
| sort | naive:2026-10-28_140825 | F | high | high | safe | high | good | medium |
| sort | pash-own | R | high | high | unsafe | medium | gaps | medium |
| split | naive:2026-10-28_134035 | A | high | high | none_offered | none | good | high |
| split | v1-pash | B | low | low | none_offered | none | wrong | high |
| wc | naive:2026-10-28_091448 | A | high | high | broken | none | good | high |
| wc | v1-pash | B | high | low | none_offered | none | gaps | high |
| wc | pash-own | R | medium | high | none_offered | none | gaps | high |

## Stability: the same side assessed twice under different letters

| Command | Side | Fields the same (of 6) | Fields that changed |
|---|---|---|---|
| cut | naive:2026-10-20_135253 | 6 | — |
| cut | naive:2026-10-27_230555 | 5 | confidence: high → medium |
| cut | naive:2026-10-28_145447 | 6 | — |
| cut | naive:2026-10-28_152550 | 6 | — |
| cut | pash-own | 6 | — |
| cut | v1-main | 6 | — |
| cut | v1-pash | 6 | — |
| rm | naive:2026-10-20_121932 | 6 | — |
| rm | naive:2026-10-28_105951 | 6 | — |
| rm | pash-own | 6 | — |
| rm | v1-main | 5 | io_complete: medium → low |
| rm | v1-pash | 6 | — |
| sort | naive:2026-10-20_160340 | 6 | — |
| sort | naive:2026-10-28_140825 | 6 | — |
| sort | naive:2026-10-28_151151 | 6 | — |
| sort | naive:2026-10-28_154444 | 6 | — |
| sort | pash-own | 6 | — |
| sort | v1-main | 5 | parser_table: wrong → gaps |
| sort | v1-pash | 6 | — |

Overall: 111/114 (97%) of rating fields unchanged.

