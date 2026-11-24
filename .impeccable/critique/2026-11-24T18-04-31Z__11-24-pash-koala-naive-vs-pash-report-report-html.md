---
target: report/report.html (PaSh suite comparison report for Michael)
total_score: 17
max_score: 28
na_heuristics: 3,7,9
p0_count: 0
p1_count: 3
timestamp: 2026-11-24T18-04-31Z
slug: 11-24-pash-koala-naive-vs-pash-report-report-html
---
# Critique: report/report.html (draft 0.7, 12 pages), PaSh suite comparison for Michael Greenberg

Method: dual-agent (A: design review · B: detector + visual evidence). Detector ran degraded (regex fallback, 0 findings; undercount). Browser overlay skipped: print PDF.

## Design health score (print; 3 heuristics n/a)
| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of status | 3 | version line present; no date; draft number not in running head |
| 2 | Match with reader's language | 2 | "PaSh grammar"/"main grammar" undefined; "nine commands" vs "seven commands"; "the merge-step case"; "A5" before the reader knows A-sections |
| 3 | User control | n/a | print |
| 4 | Consistency | 2 (fixed → 3) | Table 3 column order (fixed), orange "differs" tint vs grey shading (fixed), figure typeface (fixed), addendum numbering A1 A2 A3 A5 A6 (open) |
| 5 | Error prevention | 2 | Table 3 split-decision counts exclude `cat` without saying so; "52 commands" beside "2 command lines" in one row |
| 6 | Recognition over recall | 3 | glossary after every term's first use |
| 7 | Flexibility | n/a | print |
| 8 | Aesthetic and minimalist | 2 (partly fixed) | same facts drawn 3–4 times; near-empty page 5 (fixed by removing Figure 4); 12 pages for one script |
| 9 | Error recovery | n/a | print |
| 10 | Help and documentation | 3 | A2 glossary, A3 setup for a reader new to PaSh |
| **Total** | | **17/28 at review time (61%, Acceptable)**; about 20/28 after the reviewer's batch | |

## Design-specificity verdict
Specific in structure and copy (the four-column board, the script box beside the summary, content-written captions); generic skin on figures and chrome at review time (matplotlib default face, serif running head), both since fixed. Detector: 0 findings, degraded.

## Already fixed by the finish reviewer's batch (before this synthesis)
Board split across pages 1–2 (now whole on page 1); serif running head/foot and truncated title (brand face embedded, limit raised); figures in DejaVu (re-lettered in Lexend Deca); Table 3 column order; near-empty page 5 and the unreadable Figure 4 (removed); orange "differs" tint (neutral token surface); gap after inline code chips; inline heading style; second blue.

## Priority issues still open
- [P1] Table 3 does not reconcile with Table 2: `cat` differs in Table 2 but is outside Table 3's split-decision denominators (0 of 1, 2 of 4) with no stated rule; and "52 of 52 commands, by hand" sits beside "2 of 2 command lines". Fix: state the counting rule in the caption (lines where PaSh's own files give no split answer are left out, which is `cat`), label units per cell, replace "the merge-step case" with plain words.
- [P1] Undefined and coined terms on first read: "PaSh grammar" vs "main grammar" (never explained; both columns identical on this script), "nine commands" vs "seven commands", "the split that pays", "A5". Fix: one sentence each in the opener and Table 1 header sub-lines; add both grammars to A2; say the two Caruca columns agreed on this script.
- [P1] Repetition: "nothing generated" ×3, "never ran PaSh / never told about the quotes" ×4, the `sed` explanation twice. Fix: each fact once in the body, once at most in the addendum.
- [P2] The same split/whole facts appear in Table 1 row 2, Table 2, Figure 1 and Figure 3. Reviewer A proposes dropping Figure 3; the user asked for visual evidence, so this is the user's call.
- [P2] "Faults in the files, so far" as a heading over an item that says "the file is not wrong" reads as indictment to a v1 co-author. Rename to "Why the cells differ" and move the `sort` item out from under it.
- [P3] No date; README's addendum numbering stale (A1–A4 vs A1 A2 A3 A5 A6); A5 group headings are bold paragraphs while A-sections are h3; "every stage left whole is a bottleneck" stated as a law (add "here").

## Persona red flags
Riley / Michael (number-checker, co-author): will cross-check Tables 2 and 3 and find `cat` counted in one and not the other; will ask why two identical Caruca columns exist; will ask whether regenerating `sed` keeps the naive baseline naive (must be reported as a second version). Jordan (new reader): stalls at nine vs seven commands and at "main grammar". Sam (greyscale print): Table 2's meaning carried by tint alone (fixed with weight 600).

## Questions to consider
Could Table 2 fold into Table 1 as a per-command row so one table plus Figure 2 is the whole body? Should the two Caruca columns merge where they agree? Should the title state the finding? When 86 scripts arrive, what is the one page-one table?
