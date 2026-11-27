# Assessment A: design-director critique, PaSh-suite report (Draft 2.2, 16 pp.)

## Verdict on design specificity
The report clearly follows the ACM conference look: booktabs rules, Libertinus, numbered sections, one colour per source carried as a rule over each column, and a tinted PaSh's own reference column. That holds across Tables 1 and 3 to 6 and Figures 2 to 4. Page 1 still makes the reader do the comparing. The finding line names neither PaSh's own files nor bash as baselines, and "about 5 % slower" matches no number in Table 1, which shows 1.15 against 1.09 and 1.10. The table gives every cell the same weight, so a 77 of 86 failure looks like a 41 of 86 reference value. Cross-referencing is set up underneath (116 link annotations) but invisible: links inherit the text colour, have no underline, have no way back, and the PDF has no bookmark outline (pypdf finds 0 entries).

## Heuristics (adapted to a static Read surface, 0 to 4)
| # | Heuristic, as it applies to a printed and PDF paper | Score | Why |
|---|---|---|---|
| 1 | Visibility of status: where am I, what is this page for | 2 | Every page repeats the same running head; no section name; no PDF outline |
| 2 | Match with the reader's language | 2 | Mostly plain prose, but "Caruca's full grammar" is a hybrid (22 full plus small for the rest); "use", "part" and "line" are three counting units |
| 3 | Control and freedom: jump and come back | 1 | Links go one way only; footnotes and appendix parts have no link back |
| 4 | Consistency and standards | 2 | Source column order changes (T1: own, naive, small, full; T2: naive, full, small; T3: Caruca, own, naive; A.5: naive, full, small, own); one footnote series 1 to 19 mixes body notes and table notes |
| 5 | Preventing misreading | 2 | Rows where higher is better sit next to rows where lower is better, with no arrows; "5 % slower" has no stated comparator; the start-up-removed time row on page 1 covers only 10 one-pass scripts |
| 6 | Recognition rather than recall | 3 | The source colours work; terms are defined on page 1 and in A.1, but A.1 sits on page 8 |
| 7 | Skimming versus deep reading | 3 | Finding line, then Table 1, then section notes, then the appendix is a good layering |
| 8 | Minimal design | 2 | Table 2 repeats about 60 % of Table 1; tiny grey sub-lines and run-in notes add noise |
| 9 | Recovery from errors (here: threats and errata) | 3 | Section 7 and the independent check are honest and easy to find |
| 10 | Help and documentation | 3 | A.1 Words used and A.9 Records are thorough |
| | Total | 23/40 | Solid content, weak navigation |

## Cognitive load
- Page 1 uses six different denominators: 86 scripts, 177 parts, 609 uses, 484 uses, 178 lines and 113 lines. The 178 and 113 appear in Table 2 and Table 7. The reader has to keep asking "of what?".
- Seven conditions to track: bash, PaSh's own, the naive LLM, the naive LLM's second sed file, Caruca small, Caruca full, and PaSh's own second copy. The two "second" conditions appear on pages 1, 3 and 7 and pull attention away from the main three-way comparison.
- Sentences of 30 words or more that a professor would have to read twice:
  - p1 "Caruca's files come from two lists … called Caruca's full grammar below" (about 40 words; it also redefines "full").
  - p6 "With its own files PaSh took 2.3 times …" (8 numbers in 2 sentences).
  - p6 "With PaSh's start-up removed …" (11 numbers in 1 paragraph).
  - p10 "How we know what PaSh did" (about 45 words in its third sentence).
- Places where the reader has to hunt:
  - Koala's stored-answer check (46, 46, 37, 36) is buried in the Table 1 caption.
  - What "without cat" means is never said on page 1.
  - Why 1.00 appears in the first time row needs the reader to infer that the row is divided by PaSh's own time.

## Priority issues
1. **[P0] p1, finding line.** "Ran about 5 % slower" has no comparator; Table 1 shows 1.15 against PaSh's own files. The line also never says how PaSh's own files and bash did, which is exactly the owner's question. Fix: "PaSh printed bash's output in 86 of 86 scripts with the naive LLM's files and in 77 and 76 of 86 with Caruca's. It split 43 of 177 parts (PaSh's own files 41, Caruca 29 and 40) and took 1.15 times PaSh's own time (Caruca 1.09 and 1.10)."
2. **[P0] p1, Table 1 has no verdict cue.** Every cell is the same weight. Fix: shade or bold the cells that are worse than PaSh's own files, with a small ▼ in the source colour (77 of 86, 29 of 177, 11 of 177, 1.15). Leave ties plain. Add an arrow to each row label ("↑ better" or "↓ better"). Add a closing "Reading" row with one short line per column, for example "always right; splits slightly more; 15 % slower" and "wrong in 9 scripts; splits least". Do not crown a "winner", because PaSh's own files are the reference rather than a competitor.
3. **[P1] p1, the "Time ÷ bash, start-up removed" row (0.63, 0.88, 0.85, 0.73) is the 10-script one-pass subset.** The all-script row in Table 6 (0.97, 1.26, 1.05, 1.09) is the fair headline, and in it the naive LLM is clearly worst. A PaSh co-author will notice the choice of subset. Fix: show the all-script row, or put both rows on page 1 and label the subset "10 one-pass scripts".
4. **[P1] Source column order changes from table to table** (T1, T2, T3 and A.5 differ). Readers learn position as well as colour. Fix: one order everywhere: PaSh's own, naive LLM, Caruca small, Caruca full, then the cause or notes column.
5. **[P1] Table 2 (p2) largely duplicates Table 1.** Two summary tables invite the reader to check whether they agree. Fix: merge Table 2's five new rows into Table 1 as a lower block headed "Behind the result", with a thin rule above it. Section 1 then opens on Figure 2 and the "How it fared" prose.
6. **[P1] The table notes are a run-in block of 7 pt text numbered 1 to 19 across body and tables** (note 1 is a body note that sits under Table 1). Fix: ACM-style lettered table notes (a, b, c …) that restart for each table, one note per line with a hanging indent. Body notes stay numbered at the foot of the page. Every table note is a link and has a ↩ back to its row.
7. **[P2] Naming: "Caruca's full grammar" is really full grammar for 22 commands plus the small grammar for the rest.** Readers will assume "full" means all commands. Fix: "Caruca, full where traced" in headers, or a dagger on the header pointing to note a.
8. **[P2] Legibility and white space.** Figure 1 (p1) labels print at about 5 pt and Figure A.8 (p15) at about 6 pt with four-colour "1 1 1 1 of 1" strings; both are unreadable on paper. Pages 10, 13 and 14 leave a third to a half of the page empty. On p13 the A.7 heading sits at the bottom of the page, cut off from its panels. Fix: enlarge Figure 1 to full column width or drop it, since the "How it was run" text already says the same. Split A.8 across two pages at legible size. Keep A.7 with its content.

## Cross-referencing improvements, ranked by value
1. **PDF outline (bookmarks).** There are none now. Fix: `page.pdf({ outline: true, tagged: true })` in build.ts, or add the outline with pdf-lib from the h2 and h3 headings plus table and figure captions.
2. **Visible link cue.** `a.xr` uses `color: inherit`, so links cannot be seen. Fix: a dark ink-blue for a.xr and for footnote marks (as in acmart's screen mode), no underline, still readable in black-and-white print.
3. **Page numbers in references** ("Table A.6, p. 13"). This is the most useful aid on paper. Fix: render in two passes in build.ts, read each anchor's page, then insert "p. N".
4. **Back-links.** Fix: a ↩ at the end of each table note that returns to its row. Each appendix part opens with a one-line "Supports: Table 1, 'Parts split'; section 3".
5. **Lettered table notes that restart for each table** (see issue 6). Fix: the build script numbers them from the DOM.
6. **One contents line on page 1** under the finding line, with linked section numbers ("1 Result · 2 Wrong output · 3 By command · 4 Why · 5 Time · 6 Paper · 7 Limits · A"). Fix: a single 8 pt sans line.
7. **Running head shows the current section** instead of repeating the title. The duplicated "CARUCA V2" in the footer can go. Fix: set the running head per section with CSS string-set or the build script.
8. **PDF metadata title matches the visible title.** It currently reads "PaSh's benchmark suite, with three sources of annotation files". Fix: set `<title>` in report.html.
- Clutter, skip: a margin index (no margin in a single-column ACM layout); "see also" lines at the end of every section (they repeat the notes); figure and table numbers in running heads; a question-to-location index table.

## Strengths
- The source colour runs as a rule over every column and as the dot colour in every figure. Once learned on page 1, it reads without a legend.
- Figure 2 (every metric against PaSh's own files, with a noise band) is the fastest summary in the document. Table 3's "why the split is wrong" column, together with A.7's side-by-side outputs, answers the follow-up question right where it comes up.
- The threats section and the independent-check paragraph are candid and well placed for a skeptical reader.

## Minor observations
- Page-1 rows that add nothing: "Time ÷ PaSh's own" for PaSh's own (1.00), and "Parts split … the reference".
- The "without cat" sub-lines repeat the main value in 3 of 4 columns. Fold them into a note.
- "A Addendum" reads oddly; ACM uses "A Appendix". A.1 Words used belongs earlier, or should be linked from page 1's first definition.
- Captions still carry per-session numbers: Table 6 ("1.69 and 1.62 …"), note 7, and A.4 ("from the second session"). That breaks the one-set-of-results rule outside the body text. Move them to A.3.
- Figure 2's top row places a 2.7× point outside the axis and labels it with text. Clip it and draw an arrow, or start the axis at 3.5.
- On p4, Table 4's "8 raised" cell is the only text in a numeric column. Use a note mark.

## Provocative questions
1. If PaSh's own files are the yardstick, why is "naive LLM vs Caruca" the title instead of "how close each source gets to PaSh's hand-written files"? Would the verdict read faster as distance from the reference?
2. Does the naive LLM's 86 of 86 owe more to its files saying "no split" where they had no good answer than to understanding the commands? Should page 1 show splits refused next to splits made?
3. Would Greenberg rather see one page-1 figure (Figure 2, enlarged) than Table 1, with the table moved to section 1?
