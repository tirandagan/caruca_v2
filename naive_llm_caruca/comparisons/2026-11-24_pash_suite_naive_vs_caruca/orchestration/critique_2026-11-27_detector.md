# Assessment B2: detector evidence for report.html / report.pdf (2026-11-27)

## 1. Detector (impeccable detect.mjs)
- Repo run: DEGRADED (htmlparser2/css-select/css-tree/domutils missing), returned [].
- Rerun with the scripts copied to scratchpad/imp + `npm install` of the 4 modules: full parser.
- report.html alone: 1 finding. `design-system-color` (advisory), h1 text rgb(0,0,0). FALSE POSITIVE:
  report.html has no <link>/<style>. build.ts injects report.css and the token CSS at build time, so the detector sees the browser's default colours.
- report.css alone: 17 x `design-system-font` (warning), lines 377-496: Libertinus Serif/Sans + Inconsolata are not in DESIGN.md.
  REAL as drift from DESIGN.md. The fonts are a deliberate override (css comment line 374: "academic typography (Tiran, 2026-11-26) ... ACM acmart").
  DESIGN.md still lists Lexend Deca/JetBrains Mono only, and the THESIS comment in report.html (line 11) also still says Lexend Deca.
- HTML with report.css inlined (temp copy, deleted):
  - tight-leading x92: values like "0.01x" come from pt/px unit misparsing, so they are FALSE POSITIVES as reported. The declared body line-height of 1.22 (css 377/380) is under the rule's 1.3, but it matches acmart's 10/12 pt on purpose.
  - justified-text x33: FALSE POSITIVE. `p` sets `hyphens:auto; -webkit-hyphens:auto` (css 379).
  - oversized-h1 x1 ("2768px"): FALSE POSITIVE from unit misparsing. Declared size is 17.3pt.
  - design-system-font x3: the same real drift as above.
- No contrast, layout or slop-pattern findings in any run.
- Hover/focus/responsive rules: none fired, and none apply to a print PDF.

## 2. Browser overlay
Skipped: print-only target rendered via puppeteer.

## 3. Page fill (/tmp/p, 765x990 px at 90 dpi)
Body = between the head rule (y=71) and the foot rule (y=926). Blank = share of the body below the last ink (pixels < 200 grey).

| pg | blank | pg | blank | pg | blank | pg | blank |
|---|---|---|---|---|---|---|---|
| 1 | 3.1% | 5 | 9.3% | 9 | 5.8% | 13 | 22.8% |
| 2 | 4.6% | 6 | 9.0% | 10 | **31.3%** | 14 | **49.0%** |
| 3 | 1.7% | 7 | 18.4% | 11 | 16.6% | 15 | 17.7% |
| 4 | 10.3% | 8 | 2.7% | 12 | 22.1% | 16 | 2.7% |

Over 30%: page 10 (31.3%) and page 14 (49.0%). Between 15% and 30%: pages 7, 11, 12, 13 and 15.

## 4. Links (pypdf, report.pdf, 16 pages, 612x792 pt)
- /Link annotations per page: p1 19, p2 37, p3 8, p4 4, p5 12, p6 7, p7 4, p8 1, p9 4, p10 1, p11 2, p12 0, p13 2, p14 0, p15 1, p16 14. Total 116, all internal GoTo. No external URIs.
- Named destinations: 46. Breakdown: fn1-fn19 (pages 1-2); sec-2/4/5/7; fig-1..4 and fig-a8; tab-1..7; tab-a1/a4/a5/a6/a8/a9; a-3/5/6/7/9.
- Links to a missing destination: NONE. Destinations nothing links to: NONE.
- Page 1 (19 links):
  - Table 1 body: 7 links, the footnote markers fn2-fn8, one per row label.
  - Table 1 notes block: 10 cross-reference links (sec-2, a-7, fig-3, fig-a8, tab-a4, tab-5, sec-5 x2, tab-6, tab-a6).
  - Prose: fn1 and a-5 (the second is in the "What was run" box).
- Page 2 (37 links):
  - Table 2 body: 11 links, fn9-fn19, one per row label.
  - Table 2 notes: 14 cross-reference links.
  - Prose: 12 links. sec-4 at a line break is 2 rectangles.

## 5. Counts in report.html (5 sections: 2 body, 3 addendum)

|  | Body | Addendum | Total |
|---|---|---|---|
| tables | 8 (Tables 1-7 + the "What was run" box) | 6 (A.1/A.4/A.5/A.6/A.8/A.9 tables) | 14 |
| figures (each one `<img>`, no inline svg) | 4 | 1 | 5 |
| h1 | 1 | 0 | 1 |
| h2 | 7 | 1 ("Addendum") | 8 |
| h3 | 2 | 9 (A.1-A.9) | 11 |
| h4-h6 | 0 | 0 | 0 |
| inline `<code>` (not inside pre) | 128 | 290 | 418 |
| `<pre>` | 0 | 3 | 3 |

- Footnotes: 19 markers (`sup.fnref`, ids fn1-fn19) and 19 matching numbered `<sup>` inside 2 note blocks (`p.footnote`, with 8 numbers, and `p.footnote.tnotes`, with 11).
  Total `<sup>` = 72. The other 34 are in the addendum and are letter markers (e/r/n) in `p.files` (31) and `p.entry` (3), not footnotes.
