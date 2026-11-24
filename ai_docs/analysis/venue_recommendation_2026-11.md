# Where to submit the revised Caruca paper, and when

Written 2026-11-24 for Tiran Dagan, Prof. Michael Greenberg and Prof. William Eiers. Every date and rule
below was read on the venue's own web page on **2026-11-24**; the page is linked in the table. Where a
venue has not posted its call yet, the row says **unverified** and gives last year's dates only as a
guide. "AoE" means "Anywhere on Earth", the time zone most computing conferences use: the deadline is
midnight at the last place on Earth where it is still that day (UTC−12). Three other words used below:
a paper is **desk-rejected** when it is turned away without review, usually for breaking a format rule;
a **major revision** is a decision that lets authors fix listed problems and come back in the same
cycle; a **shepherd** is a committee member who checks that an accepted paper makes the agreed changes.

The paper: *Caruca: Effective and Efficient Specification Mining for Opaque Software Components*
(arXiv:2510.14279, October 2025). The revision adds four things: a comparison with a simple
one-prompt LLM approach (the "naive LLM baseline"), measured cost, a test of whether repeated runs agree,
and a downstream test on PaSh's own benchmark scripts.

---

## 1. Recommendation

**Submit to ISSTA 2027 (the ACM SIGSOFT International Symposium on Software Testing and Analysis):
abstract due Friday 8 January 2027, full paper due Monday 11 January 2027, both AoE.** ISSTA is the
main venue for program analysis and testing tools. Mining what a command reads, writes and whether it
can be split for parallel running, then feeding that to analysis tools like ShellCheck and PaSh, is
squarely its subject. The LLM comparison suits the venue too, since it runs many papers comparing LLM
methods with engineered ones. The deadline leaves about four weeks after a mid-December draft. ISSTA
also has a major-revision round, so a paper close to acceptance gets a second chance in the same cycle
instead of being rejected.

**Alternative: ATC 2027 (the ACM SIGOPS Annual Technical Conference), paper due 19 January 2027 AoE.**
This is the authors' home systems community: POSH (Portable Operating System Shell) appeared at ATC
2020 and Koala at ATC 2025. ATC asks for the same ACM two-column template and the same 12-page limit
the current draft already uses, so it needs the least reformatting. Choose it over ISSTA if the advisors
want a systems audience. USENIX ended ATC after 2025; ACM SIGOPS now runs it under the same short name.

**Fallback: ASE 2027 (the IEEE/ACM International Conference on Automated Software Engineering),
abstract due 4 March 2027, paper due 10 March 2027 AoE.** Use it if the draft or the advisors' review
slips past early January. ASE covers specification mining, program analysis and LLMs for software, and
it also has a major-revision round. Its 10-page IEEE format means converting the paper and cutting it
hard.

The three deadlines are mutually exclusive: every venue here forbids having the same paper under review
at two places at once. ISSTA's first decision (20 April 2027) and ATC's (27 April 2027) both arrive
after ASE's deadline. So if January is used, the next stop after a rejection is ICSE 2028 (1 July 2027),
not ASE.

One fact strengthens the systems case and should be in the paper whichever venue is chosen. SaSh,
"Ahead-of-time Analysis of Shell Program Effects", won a Best Paper Award at SOSP 2026. Most of
Caruca's authors wrote it, and it reads command specifications to reason about commands it cannot see
inside. The Caruca abstract says Caruca is "currently powering the full specifications for a
state-of-the-art static analysis tool"; an award-winning consumer is strong evidence for that claim.
Source: https://sigops.org/s/conferences/sosp/2026/.

---

## 2. Every venue checked

The **fit score** (1 to 5) covers two things: how well the venue's subject and community match the
paper, and whether its deadline falls in the usable window, mid-December 2026 to the end of April 2027.
"Closed" means the deadline has already passed. "Prior posting" means the venue's rule on a version
already public on arXiv. Caruca's has been public since October 2025, with author names and the name
"Caruca".

### Full-paper venues with a deadline in the window

| Venue | Abstract / paper deadline | Notification | Conference | Length and format | Double-blind | Prior posting (arXiv) | Rebuttal / revision | Acceptance rate | Fit | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| **ISSTA 2027**: 36th ACM SIGSOFT Int. Symposium on Software Testing and Analysis, published in the Proceedings of the ACM on Software Engineering | Abstract Fri 8 Jan 2027, paper Mon 11 Jan 2027, AoE | First decision Tue 20 Apr 2027 (includes early reject); final Thu 17 Jun 2027 | 7–10 Sep 2027, Singapore | 18 pages, single-column ACM `acmsmall`. Appendix counts; references and the data-availability section do not. Over-length is desk-rejected | Yes | The call never mentions arXiv. It says only "should not have been published previously", and under ACM policy a preprint is not a publication | Author response 22–25 Mar; major revision due 20 May (4 weeks) | 2026: 210 of 888, 23.6% (a university news release, not an official page: https://en-cist.buct.edu.cn/2026/0831/c10280a222487/pagem.htm) | **5**: its exact subject; major-revision round; deadline in window | https://conf.researchr.org/track/issta-2027/issta-2027-research-papers |
| **ATC 2027**: ACM SIGOPS Annual Technical Conference (run by USENIX until 2025) | No abstract deadline; paper Tue 19 Jan 2027 AoE, "no extensions" | 27 Apr 2027 | 28 Jun–1 Jul 2027, Rennes, France | 12 pages, references not counted. ACM `acmart` two-column `sigplan` template, the same as the current draft | Yes | Allowed, but "your submission must use an anonymized name" for a system already known, so Caruca must be renamed in the submitted copy | Author response 3–5 Apr (facts only, no new experiments). Conditional accept with a shepherd, no revision round. **The first review round reads only the first two pages** | No official figure found | **5**: home community; same template; topics include "bug-finding, tracing, analyzing" | https://atc.sigops.org/2027/call-for-papers/ |
| **ECOOP 2027, round 2**: 41st European Conf. on Object-Oriented Programming (Dagstuhl LIPIcs) | Paper Thu 11 Feb 2027 AoE | 8 Apr 2027 | 28 Jun–2 Jul 2027, Turin, Italy | No limit at submission; final version at most 25 LIPIcs pages without references | Yes | Explicitly allowed, under any title; no renaming needed | Author response 22–26 Mar; "asked for revisions" goes to a later round | 2026: 30 of 98, about 31% (https://drops.dagstuhl.de/storage/00lipics/lipics-vol372-ecoop2026/LIPIcs.ECOOP.2026.0/LIPIcs.ECOOP.2026.0.pdf) | **2**: a programming-languages venue; the paper is not about language design | https://2027.ecoop.org/track/ecoop-2027-technical-papers |
| **ICSME 2027**: 43rd IEEE Int. Conf. on Software Maintenance and Evolution | Abstract 19 Feb, paper 26 Feb 2027, AoE | Early decisions 26 Apr; final 25 May 2027 | 7–11 Sep 2027, Toronto | 10 pages plus 2 pages of references only, IEEE two-column | Yes | Allowed, but "the title of the submission must be different from the authors' preprints on arXiv" | Author response 27–30 Apr; no revision round | 2025: 45 of 188 received (24%; the chairs quote 31%, counting only the 146 reviewed) (https://ieeexplore.ieee.org/document/11185932) | **3**: code analysis and LLM topics fit, but maintenance and evolution is not the paper's subject | https://conf.researchr.org/track/icsme-2027/icsme-2027-papers |
| **ASE 2027**: 42nd IEEE/ACM Int. Conf. on Automated Software Engineering | Abstract Thu 4 Mar, paper Wed 10 Mar 2027, AoE | Early reject 19 May; first decision 10 Jun; final 27 Jul 2027 | 24–28 Oct 2027, El Paso, Texas | 10 pages, appendices included, plus 2 pages for references and data availability. IEEE `IEEEtran` conference format | Yes | Allowed; "should avoid specifying that the manuscript was submitted to ASE 2027" | Author response 19–24 May; major revision due 8 Jul | 2025: 247 of 1,136 reviewed, 21.7% (chairs' message, read from a copy of the IEEE front matter: https://tsingpig.github.io/files/ASE%202025%20papers/ASE%202025/pdfs/ASE2025-5DQL9ko9OwpjaORDC0qal7/573300z057/573300z057.pdf) | **4**: strong subject fit; the deadline gives the most time; the format needs the biggest cut | https://conf.researchr.org/track/ase-2027/ase-2027-research-track |
| **OOPSLA 2027, round 2**: ACM SIGPLAN Object-Oriented Programming, Systems, Languages and Applications, published in the Proceedings of the ACM on Programming Languages | Paper Wed 7 Apr 2027 AoE (round 1, 14 Oct 2026, is closed) | First 2 Jul; final 13 Aug 2027 | 10–15 Oct 2027, Prague | 23 pages, single-column `acmsmall`; references and appendices not counted | Yes | Allowed; "should not broadly advertise your work" | Author response 15–19 Jun; revision due 30 Jul | Not on the call page. A snippet of the 2026 editorial gives 75 articles from 227 submissions (unverified; the ACM Digital Library page was blocked) | **2**: the call warns that LLM papers "without a substantial PL angle … may be … desk-rejected" | https://2027.splashcon.org/track/splashoopsla2027 |
| **ISSRE 2027**: 38th IEEE Int. Symposium on Software Reliability Engineering | Abstract 9 Apr, paper 16 Apr 2027, AoE | Early decision 15 Jun; final 9 Jul 2027 | 19–22 Oct 2027, Macau | **12 pages including references**, IEEE Computer Society format | Yes | Allowed; "must not state or imply that the work is under submission to ISSRE 2027" | Factual rebuttal 7–11 Jun; major revision 16 Jun–2 Jul | 2025: 47 of 170, 27.6% (https://ieeexplore.ieee.org/document/11229737) | **3**: static and dynamic analysis are in scope; the length limit is the tightest here | https://conf.researchr.org/track/issre-2027/issre-2027-papers |
| **CAV 2027**: 39th Int. Conf. on Computer Aided Verification (Springer Lecture Notes in Computer Science, LNCS) | Paper Wed 20 Jan 2027, 23:59 AoE; no abstract deadline | Early reject 4 Mar; final 23 Apr 2027 | 21–23 Jul 2027, Amsterdam | 18 pages in LNCS format; references and appendices not counted | Yes, for regular papers | Allowed, but asks authors not to post within a week before or a month after the deadline | Rebuttal 5–8 Apr | 2026: 81 of 319, about 25% (a bookseller's copy of Springer's description) | **1**: a formal verification venue; the paper does not verify anything | https://conferences.i-cav.org/2027/cfp/ |
| **SOSP 2027**: ACM Symposium on Operating Systems Principles | **Unverified.** The 2027 call is not posted (its page returns "not found"). In 2026: abstract 26 Mar, paper 1 Apr, AoE | 2026: 3 Jul | 2027 place not settled on any official page | 2026: 12 pages, references not counted, ACM `sigplan` two-column | 2026: yes | 2026: allowed, but a known system name must be anonymized | 2026: author response, shepherding, no revision round | 2026: 62 of 390, 16% (search snippet of the ACM Digital Library page; unverified) | **4 if it opens**: SaSh's 2026 award shows the community values this line of work; very selective | https://sigops.org/s/conferences/sosp/2026/cfp.html |

### Venues outside the window, for later rounds

| Venue | Abstract / paper deadline | Notification | Conference | Length and format | Double-blind | Prior posting (arXiv) | Rebuttal / revision | Acceptance rate | Fit | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| **ICSE 2028**: 50th IEEE/ACM Int. Conf. on Software Engineering | Abstract 24 Jun, paper 1 Jul 2027, 23:59:59 AoE. One cycle only: the spring cycle was dropped from 2027 on | 21 Oct 2027; final decision after revision 19 Dec 2027 | Main conference 3–5 May 2028, Waikoloa, Hawaii | 10 pages plus 2 of references, ACM `sigconf` | Yes | Allowed; must not say it was submitted to ICSE 2028 | Author response 24–26 Sep; revision due 18 Nov | 2026: 321 of 1,469, 21.9% (https://icse2026.hotcrp.com/) | **4**: the best next stop after an April rejection | https://conf.researchr.org/track/icse-2028/icse-2028-papers |
| **EuroSys 2028**: European Conf. on Computer Systems | **Unverified**, not posted. The 2027 pattern gives a spring cycle around 7 May (abstract) and 14 May 2027 (paper), and a fall cycle around 24 Sep 2027 | Not posted | Not posted (2027 is 19–22 Apr 2027, Rabat) | 2027: 12 pages plus references, ACM two-column | 2027: yes | 2027: allowed, but the submitted copy needs "a substantially different title and … a different system/tool name" | 2027: author response; revise-and-resubmit into the next cycle | No official figure found | **3**: systems fit; just after the window | https://2027.eurosys.org/cfp.html |
| **OSDI 2027**: 21st USENIX Symposium on Operating Systems Design and Implementation | Abstract 1 Dec, paper 8 Dec 2026, 5:59 pm EST: **before the paper can be ready** | 16 Mar 2027 | 7–9 Jul 2027, Baltimore | 12 pages plus references, USENIX format | Yes | Allowed, but the system needs an anonymized name | No author response; conditional accept only | 2026: 134 of 669, 20.0% (https://www.usenix.org/sites/default/files/osdi26-message.pdf) | **0**: too early | https://www.usenix.org/conference/osdi27/call-for-papers |
| **FSE 2027**: ACM Int. Conf. on the Foundations of Software Engineering | Paper 2 Oct 2026, extended to 3 Oct: **closed**. FSE 2028 is not posted (unverified; about October 2027 by the pattern) | — | 12–16 Jul 2027, Shenzhen | 18 pages plus 4 of references, `acmsmall` | Yes | Allowed if the preprint does not name the venue | Author response; major revision | No official figure found | **0** for 2027 | https://conf.researchr.org/track/fse-2027/fse-2027-papers |
| **PLDI 2027**: ACM SIGPLAN Conf. on Programming Language Design and Implementation | 12 Nov 2026: **closed**. PLDI 2028 is not posted (unverified; about mid-November 2027) | — | 5–11 Jun 2027, Atlanta | 20 pages, `acmsmall`; a required "AI Use" section counts toward the limit | Yes | Allowed; do not advertise widely | Two review rounds | Not found | **0** | https://pldi27.sigplan.org/track/pldi-2027-papers |
| **TACAS 2027 / 2028**: Tools and Algorithms for the Construction and Analysis of Systems (part of ETAPS, the European Joint Conferences on Theory and Practice of Software) | 2027: 15 Oct 2026, **closed**. 2028: only a placeholder page (ETAPS 2028 runs 2–7 Apr 2028, Karlsruhe); dates unverified | — | 10–15 Apr 2027, Copenhagen | 18 pages in LNCS format, references not counted | Yes, for regular papers | Allowed, but asks authors not to post in the two weeks either side of the deadline | Rebuttal | 2026: the two sources disagree (72 of 177, or 56 of 190) | **1** | https://www.etaps.org/2027/cfp ; https://etaps.org/2028 |
| **SANER 2027 / 2028**: IEEE Int. Conf. on Software Analysis, Evolution and Reengineering | 2027: 25 Sep 2026, **closed**. 2028: not posted (its page returns "not found"; about late September 2027 by the pattern, unverified) | — | 9–12 Mar 2027, Richmond, Virginia | 10 pages plus 2 of references, IEEE | Yes | The arXiv copy must not be updated from one month before the deadline | No rebuttal | 2026: 47 of 265 received (https://ieeexplore.ieee.org/document/11576533) | **1** | https://conf.researchr.org/track/saner-2027/saner-2027-papers |
| **ASPLOS 2028**: ACM Architectural Support for Programming Languages and Operating Systems | **Unverified**, not posted; a tracker projects about 15 Apr 2027 | — | — | 2027: 11 pages, references not counted | 2027: yes | 2027: allowed; no advertising from two weeks before the deadline | 2027: author response and major revision | Not found | **2**: wants work spanning hardware, languages and operating systems | https://www.asplos-conference.org/?p=8512 |
| **Middleware 2027**: ACM/IFIP Int. Middleware Conference | Winter cycle: paper 4 Dec 2026. Summer cycle: paper 4 Jun 2027. Both outside the window | Winter 29 Mar; summer 13 Sep 2027 | 13–17 Dec 2027, Kyoto | 12 pages, ACM `sigconf` | Yes | Allowed, but the name must differ from the online version | Minor or major revision possible | Not found | **1** | https://middleware-conf.github.io/2027/call-for-papers/ |
| **ICST 2027**: IEEE Int. Conf. on Software Testing, Verification and Validation | 2 Nov 2026, **closed**. ICST 2028 is not posted (unverified) | — | 17–21 May 2027, San Sebastián | 10 pages plus 2 of references, IEEE | Yes | Allowed if it does not name the venue | Major revision | — | **0** | https://conf.researchr.org/track/icst-2027/icst-2027-research-papers |
| **MSR 2027**: Int. Conf. on Mining Software Repositories | 23 Oct 2026, **closed** | — | 26–27 Apr 2027, Dublin | 10 pages plus 2, IEEE | Yes | Allowed; a different preprint title is suggested | Author response | — | **0** | https://conf.researchr.org/track/msr-2027/msr-2027-technical-papers |
| **SAS 2027**: Static Analysis Symposium | **Unverified**, not posted; 2026's was 7 May 2026, so about May 2027 | — | With SPLASH 2027, Prague | 2026: no page limit, LNCS | 2026: yes | Not stated | 2026: rebuttal | Not found | **2** | https://2027.splashcon.org/home/sas-2027 |

### Workshops and short-paper tracks

None of these is a place for the full paper. Most are **archival**: they publish in the ACM or IEEE
digital library, which counts as prior publication and would block a later conference version of the
same work.

| Venue | Deadline | Length | Archival? | Note | Source |
|---|---|---|---|---|---|
| HotOS XXI 2027: ACM SIGOPS Workshop on Hot Topics in Operating Systems, 24–26 May 2027, Burghausen, Germany | Mon 1 Feb 2027 (no time zone given) | 5 pages plus references | Yes (ACM) | Position papers only; needs a renamed system; fit 2 | https://www.sigops.org/s/conferences/hotos/2027/cfp.html |
| ICST 2027 workshops: AIST (AI in Software Testing), A-MOST (Advances in Model-Based Testing) | 4 Feb 2027 | 8 pages, IEEE | Yes (IEEE) | Fit 1 | https://conf.researchr.org/home/icst-2027/aist-2027 |
| FSE 2027 Ideas, Visions and Reflections track | 12 Feb 2027 AoE | 4 pages plus 1 | Yes (ACM) | Fit 1 | https://conf.researchr.org/track/fse-2027/fse-2027-ideas-visions-and-reflections |
| SOAP 2027: ACM SIGPLAN Workshop on the State Of the Art in Program Analysis, at PLDI 2027 | **Unverified**, not posted; 2026's was 10 Mar 2026 | 4–6 pages | Yes (ACM) | Fit 2 | https://pldi26.sigplan.org/home/SOAP-2026 |
| FTfJP 2027: Formal Techniques for Judicious Programming, at ECOOP 2027 | **Unverified**, not posted; 2026's was 25 Feb 2026 | 2026: 12 pages | 2026: ACM, but authors could opt out | The only workshop found with a non-archival option; fit 1 | https://2026.ecoop.org/home/FTfJP-2026 |
| LLM4Code 2027, ICSE 2027 workshops, AST 2027 | 13 Nov / 30 Oct 2026: **closed** | — | — | — | https://llm4code.github.io/ |
| PLOS 2027: Workshop on Programming Languages and Operating Systems | **Unverified**, not posted; 2026's was 5 Jun 2026 | 6 pages | Yes (ACM) | Outside the window | https://plos-workshop.org/2026/ |

Notes:
- The brief's "ASC" was treated as ATC, as the brief said to do. No other venue named ASC was searched
  for.
- Journals: the ACM Transactions on Software Engineering and Methodology (TOSEM) and the ACM
  Transactions on Programming Languages and Systems (TOPLAS) accept papers at any time. Their
  author-guideline pages blocked automated reading, so their rules are not confirmed.

---

## 3. Timeline: today to ISSTA (Monday 11 January 2027)

The timeline gives the advisors three weeks to review, and that window includes the holidays. The
fallbacks are built in.

| When | What | Who |
|---|---|---|
| **This week (by Fri 27 Nov)** | Ask Michael which venue rejected the original submission, and whether its reviews can be found. If it was ISSTA or ATC, that venue asks for the earlier reviews and a summary of changes. Ask both advisors to block review time for 15 Dec–4 Jan. Confirm the author list, and check who on it is already submitting to ATC, which allows each author at most 2 papers. | Tiran → advisors |
| **By Fri 4 Dec** | Finish the experiments: the PaSh benchmark batch started today, the independent check of it, the counts and the charts. Settle the numbers for the naive LLM comparison. After this date, re-run only failed runs; start nothing new. | Tiran |
| **Mon 7 – Mon 14 Dec** | Write the new sections: the comparison with the naive LLM baseline, cost, agreement across repeated runs, and the PaSh benchmark results. Move the paper to ISSTA's single-column template and cut it to 18 pages. Anonymize it: rename the system, remove author names and acknowledgements, refer to the group's own earlier papers in the third person, and give an anonymous artifact link. Add the required data-availability section. | Tiran |
| **Tue 15 Dec** | Send the full draft to both advisors and the co-authors. | Tiran |
| **15 Dec – Mon 4 Jan** | Advisors review. A useful early check: Michael reads the introduction and evaluation by 22 Dec, so structural problems surface before the holidays. | Advisors |
| **Mon 4 – Thu 7 Jan** | Apply the comments. On **Wed 6 Jan**, decide where to submit: ISSTA on 11 Jan; ATC on 19 Jan, which gives one more week and lets the paper stay in its current two-column template; or move to ASE on 10 Mar if the draft is not ready. | All |
| **Fri 8 Jan (AoE)** | Register the abstract on ISSTA's submission site; this is mandatory: title, abstract, authors and conflicts of interest. | Tiran |
| **Fri 8 – Mon 11 Jan** | Final read; check the page limit (ISSTA desk-rejects papers over 18 pages); check the PDF. | Tiran |
| **Mon 11 Jan (AoE)** | **Submit.** | Tiran |
| 22–25 Mar 2027 | Author response. | All |
| 20 Apr 2027 | First decision: accept, major revision or reject. | — |
| 20 May 2027 | Major revision due, if asked for. | All |
| 17 Jun 2027 | Final decision. Conference is 7–10 Sep 2027 in Singapore. | — |
| If rejected in April | Next stop: ICSE 2028 (1 July 2027, ACM two-column template), or EuroSys 2028's spring cycle (about mid-May 2027, unverified; it needs a new title and system name). | All |

---

## 4. Risks

**The double-blind rules and the version already on arXiv.** Every venue allows a version that is
already public. Several add a condition:
- ATC, SOSP, OSDI, HotOS, EuroSys and Middleware require a different system name in the submitted copy,
  so "Caruca" cannot appear in it.
- EuroSys and ICSME also require a different title.
- ISSTA's call says nothing about preprints. ACM's policy does not count a preprint as prior
  publication, but renaming the system for ISSTA too costs little and avoids an argument.
- **Do not update the arXiv version while the paper is under review.** CAV, the TACAS conference and
  SANER explicitly ask authors not to post near their deadlines.
- Under ISSTA's rules, the title and author list cannot change between submission and the final
  version.

**Page limits against the paper's current length (counted 2026-11-24 from the arXiv PDF).**
- The PDF has 14 pages in the ACM two-column layout. The body (title through conclusion) runs to partway
  down page 13, about 12.5 pages and about 10,700 words including figure text. The 39 references take
  about 1.5 pages.
- The revision adds four parts. My estimate, not measured, is 1.5 to 2.5 more pages.
- What each venue needs (estimates, not measured):
  - **ATC:** 12 pages, references not counted, so about 2 to 3 pages must come out of today's text.
  - **ISSTA:** 18 single-column pages; today's body is roughly 19 to 22 such pages, so a similar cut.
  - **ASE and ICSME:** 10 IEEE pages, about a third smaller than today's body once the new material is
    in.
  - **ISSRE:** 12 pages including references, about the same as ASE.

**One venue at a time.** Every venue here forbids having the paper under review anywhere else. Both
January options decide in late April, after ASE (10 Mar), OOPSLA round 2 (7 Apr) and ISSRE (16 Apr)
have closed. So choosing January means the next option after a rejection is ICSE 2028 in July, or
EuroSys 2028's spring cycle if it opens. OOPSLA also refuses a paper rejected in its own first round,
though papers rejected by OOPSLA 2026 are welcome.

**The calendar.**
- The advisors' review window falls over Christmas and New Year.
- ISSTA's abstract deadline is a Friday and its paper deadline the next Monday, so nothing can slip into
  that weekend.
- If 6 January shows the draft is not ready, switch to ASE: that is safer than submitting a rushed
  paper.

**ATC's two-page first round.** In ATC's first round, reviewers judge the paper on its first two pages
alone. The introduction must make the case on its own: what Caruca does, what is new in the revision,
and the headline numbers.

**ATC's two-papers-per-author cap.** Each author may be on at most two ATC 2027 submissions. Senior
co-authors who are active in systems may already be at that limit. Check before choosing ATC.

**Rules on writing with AI tools.**
- ATC forbids papers "produced entirely or substantively by generative AI".
- ISSTA and ASE follow the ACM and IEEE authorship policies, which require disclosing some uses.
- PLDI requires an "AI Use" section that counts toward its page limit.
- The text must be the authors' own, and any AI use the policies require must be disclosed.

**Scope warnings.** OOPSLA and SANER warn that papers mainly applying LLMs may be desk-rejected as out
of scope. This is part of why both score low.

**What reviewers will push on.**
- The PaSh benchmark runs use small inputs on an ARM virtual machine, not the original suite's inputs,
  which are no longer available.
- Timing taken on the Mac needs the sleep check the project already does.
- The paper should say both of these plainly, especially at ATC, whose reviewers care about
  measurement.

**The original rejection is not on file.** If the original venue is one of these candidates, the venue
must be told and the earlier reviews addressed. Finding the reviews is worth a short email: they are
the best guide to what has to change.

---

How this was checked: four research agents read the official call pages on 2026-11-24. I then re-read
the official pages myself for ATC 2027, ISSTA 2027, ASE 2027, ICSE 2028, OOPSLA 2027, ECOOP 2027,
ICSME 2027, ISSRE 2027, CAV 2027, OSDI 2027, EuroSys 2027 and SOSP 2026, and confirmed that SOSP 2027's
call page returns "not found". Each quoted rule and date above matched what those pages say on that
date.
