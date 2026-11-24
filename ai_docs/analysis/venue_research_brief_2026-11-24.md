# Brief: where to submit the revised Caruca paper, and when

You are a research worker. An orchestrating Claude session gave you this brief on behalf of Tiran Dagan
(PhD student; advisors Prof. Michael Greenberg and Prof. William Eiers). Work only on it. You may use
web search and web fetch; cite every date and rule with its URL and the date you read it.

## The paper

*Caruca: Effective and Efficient Specification Mining for Opaque Software Components* (Lamprou, Jung,
Keoliya, Lazarek, Kallas, Greenberg, Vasilakis; arXiv:2510.14279, October 2025). Read
`ai_docs/refs/caruca_white_paper.md` (abstract, intro, evaluation) and `memory/project_dual_objectives.md`,
`memory/caruca_v2_project_overview.md`, `memory/project_pash_suite_comparison.md` for what the revision adds:
an LLM-based comparison (a naive LLM baseline against Caruca's hand-written pipeline), measured cost,
reproducibility and a downstream evaluation on PaSh's benchmark suite. The topic is program analysis of
shell commands: mining partial specifications (what a command reads, writes, whether it can be
parallelized) from documentation and execution traces, consumed by analysis and testing tools (PaSh,
POSH, ShellCheck, Shseer). Tiran frames it as **analysis work: static analysis, software testing**, with a
systems flavour (the authors' home venues are OSDI, ATC, EuroSys; PaSh is OSDI'22, Koala is ATC'25).
The original submission was rejected; the venue is not on file.

**Timing constraint:** the revised paper will not be ready before the middle of December 2026. So only
deadlines from mid-December 2026 onward count, and a deadline that leaves a few weeks after that is
better than one in the third week of December.

## Produce

`ai_docs/analysis/venue_recommendation_2026-11.md`, plain language, short, for Tiran and the two
advisors. Sections:

1. **Recommendation first**: the best-fit venue and deadline, in three sentences, then one alternative,
   then a fallback. Say why each fits the paper's content (analysis of software, specification mining,
   testing tools, systems evaluation) and the authors' community.
2. **The table**: every candidate you checked, one row each: venue (full name, year, series), abstract
   and paper deadlines (with time zone), notification date, conference dates and place, page limit and
   format, double-blind or not, arXiv/prior-posting policy (the paper is already on arXiv), rebuttal or
   revision rounds, acceptance rate if published, fit score with one line of reasoning, and the URL you
   read. Candidates to check at minimum: USENIX ATC 2027 (Tiran wrote "ASC"; treat it as ATC unless
   something else matches), SOSP 2027, ISSTA 2027 (Tiran wrote "ista"), OSDI 2027, EuroSys 2028, ICSE
   2028, FSE 2027, ASE 2027, OOPSLA 2027 (both rounds), PLDI 2027, ECOOP 2027, ISSRE 2027, ICSME 2027,
   SANER 2028, CAV 2027, TACAS 2028, the ACM/IEEE testing-and-analysis workshops that match, and any
   venue you find with a January–April 2027 deadline that fits better. Mark any date you could not
   verify as "unverified" rather than guessing.
3. **A timeline** from today (2026-11-24) to the recommended deadline: what has to be done when
   (experiments finished, draft, internal review, submission), with the advisors' review time built in.
4. **Risks**: double-blind conflicts with the arXiv version, page limits versus the paper's current
   length (count it), venues that forbid parallel submission, and anything else that could bite.

Rules: plain language (`memory/feedback_plain_language.md`), no bare acronyms without the full name on
first use, every date with its source. Do not commit. Reply with the path and the one-line recommendation.
