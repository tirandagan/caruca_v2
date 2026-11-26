---
target: PaSh suite report (report.html, Draft 1.0)
total_score: 22
max_score: 36
na_heuristics: 3
p0_count: 2
p1_count: 3
timestamp: 2026-11-26T09-13-23Z
slug: 11-24-pash-koala-naive-vs-pash-report-report-html
---
Method: dual-agent (A: design review sub-agent · B: detector sub-agent). Target: report.html → report.pdf, Draft 1.0, 23 pages. Mode: Read.

## Design Health Score

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 3 | Running head/foot and page n of N; no section numbers or contents line, forward refs to A4/A7 from page 1 |
| 2 | Match system / real world | 2 | Study-private words (parts, source, grammar, uses, split/whole) from page 1; Python exception names, a PaSh source line and 15 script codes on page 4 |
| 3 | User control and freedom | n/a | static PDF |
| 4 | Consistency and standards | 2 | Three names for the second sed file; time stated in two opposite directions in one cell; the tint means "reference" in Table 1 and "differs" in Table 2 |
| 5 | Error prevention | 2 | "+2, −0" cells defined only on page 2; "a / b" code cells in A4; "0.42× bash's speed" asks the reader to invert |
| 6 | Recognition rather than recall | 2 | Glossary (A2) and the setup picture (Figure 3) arrive on pages 7–8, after every result that needs them |
| 7 | Flexibility and efficiency | 3 | Table 1 + lead paragraphs are a one-page read; Figure 2's side annotations are self-reading |
| 8 | Aesthetic and minimalist design | 2 | Visually clean; textually not: 16 sentences over 30 words in six pages, paragraphs with 12–20 numbers, 14 appendix pages of raw tables |
| 9 | Error recovery (caveats) | 3 | Faults, sleeps and the independent recount stated plainly; not framed as threats to validity |
| 10 | Help and documentation | 3 | A2/A3/A8 complete but placed last |
| **Total** | | **22/36** | **Needs work** (heuristic 3 n/a) |

## Design Specificity Verdict
Authored, not templated: the spell.sh listing beside the summary, one colour per source carried through every table cap, bar, box and dot, the tinted reference column. The information architecture is the weak part: a six-page body that assumes the vocabulary, then 17 appendix pages of which 14 are raw tables.
Deterministic scan: 1 advisory finding (h1 renders pure black instead of the ink token); zero layout, contrast or type findings at full fidelity. Detector's shipped parser modules were missing (degraded run reported); the reviewer reinstalled them in a scratch copy and reran. White-space scan: page 5 is 32% blank below its last line, page 23 is 76% blank; all other pages 0–11%. Code-span density: 40 per 1,000 words in the body, 105 per 1,000 in the addendum.
Browser overlay skipped: print-only target rendered by puppeteer.

## Overall Impression
The layout is paper-grade; the prose and the appendix are not yet. Page 1 works. Pages 2 and 4 slip into lab-notebook register (number strings, exception names, script codes). The appendix carries ten pages of tables a reader will never scan. The single biggest opportunity: put the method and the six defining words before Table 1, and cut the body's number strings to one sentence per finding with the numbers living in tables and figure annotations.

## What's Working
- Table 1 is a real comparison board: one figure per cell with its basis beneath, every rate "a of b", and it sits on page 1 beside the script it refers to.
- Figure 2's noise band from an identical second copy of PaSh's own files calibrates every timing claim honestly.
- Limits and faults are disclosed without hedging; the independent recount paragraph is publishable as is.

## Priority Issues
1. [P0] Method after results. Figure 3 and the six words a reader needs (annotation file, source, part, split/whole, Caruca's two grammars, naive LLM) arrive on pages 7–8. Fix: a 100-word "How it was run" with a half-width Figure 3 before Table 1; the long form stays in A3. Command: /impeccable clarify.
2. [P0] Page 4 is a debugging note. One 95-word sentence with NameError, AssertionError, a PaSh source line and 15 script codes; the two Time paragraphs list 12 and 14 numbers each. Fix: three sentences each ("PaSh's compiler stopped in 4 parts under its own files and 14 under Caruca's PaSh grammar, all 10 extra from Caruca's sort file; a PaSh bug we reported; PaSh ran those parts as plain bash, so output stayed right"); details move to A4. Command: /impeccable distill.
3. [P1] Time stated in two directions. "0.42× bash's speed" (higher = better) above "1.15 times PaSh's own time" (higher = worse). Fix: one convention, time ÷ bash time, lower is better, with slower/faster spelled out. Command: /impeccable clarify.
4. [P1] Appendix balance: A5 (5 pp), A6 (5 pp) and A7 (4 pp) are repository material in a PDF. Tension: Tiran asked on 26 Nov that every metric in his spec appear in the PDF. Fix options: keep A5 but as one page (per-script time chart + crash list), replace A6 by its 8-command summary (already Table 2), reduce A7 to one table of group counts with a pointer. Command: /impeccable distill.
5. [P1] Number strings as prose: page 2's opener (12 numbers), page 1 "What we saw" (9), page 4 Time (12 and 14, mapped positionally to sources). Fix: one sentence per finding; the counts go into a Table 1 row ("command uses split") and Figure 2's side column. Command: /impeccable clarify.
6. [P2] Table 2 and Figure 1 show the same data twice; Table 2's reference column is a different unit ("0 of 82" vs "+43"). Fix: keep Figure 1 with PaSh's own count as a grey label per row; move Table 2 to A4. Command: /impeccable distill.
7. [P2] The second sed file appears in every exhibit under three names before it is explained. Fix: one sentence in "What we ran" and one name ("after one fix to its sed file") everywhere. Command: /impeccable clarify.
8. [P2] Page composition: page 5 a third empty (Table 3 cannot split), page 23 nine lines, A7 orphan rows, A4a/A4b near-duplicates, A4's "other, not classified: 31" is the largest unexplained number. Command: /impeccable layout.

## Persona Red Flags
- Michael (advisor, PaSh co-author, wants observations in plain words): hits "parts", "source", "two grammars" on page 1 undefined; page 4 reads as a bug log; will ask what the 31 unclassified parts are.
- A paper reviewer: no research question, method after results, caveats not titled threats to validity, four nouns for one concept (source / annotation set / files / copy).
- Tiran (owner, wants every metric visible): would object to dropping A5–A7 outright; needs the condensed forms to still carry crashes, per-script rates and times.

## Minor Observations
- h1 pure black vs ink token (detector). Blue is both heading colour and naive LLM colour; on page 5 a blue heading sits under blue dots. Light-orange dots are low contrast in Figure 2. A5 footnote markers use a synthesised oblique. Title names the setup, not the finding. "What this does not show" mixes a commit hash with conclusions.

## Questions to Consider
- Should timing stay in the body when PaSh is slower than bash in 74–83 of 86 scripts at this input size?
- Should the headline "gained" count exclude cat, which the report itself calls correct but useless?
- Is "agreement with PaSh's own files" the right yardstick when the report shows those files wrong for col and merge-dependent for sort?
