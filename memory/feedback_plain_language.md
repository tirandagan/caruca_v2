---
name: feedback-plain-language
description: "Explain things in plain language, assume Tiran hasn't read the docs, never use coded shorthand like section numbers or dimension numbers without explaining them"
metadata:
  type: feedback
---

When giving Tiran information, follow these rules:

1. **Assume he has not read the documents** — including ones written moments ago in the same session, and
   including files already in the repo. Do not treat a document's contents as shared context just because
   it exists or because it was just created.
2. **Use very simple language.** Explain everything in basic terms. Spell out what a thing *is* before
   discussing it.
3. **No coded shorthand.** Never refer to something only by a number, label, or section reference and
   assume it lands. This means: no bare "dimension 6," "Q2," "§7.2," "Tier 0," "gap #14," "Phase 3,"
   "the v2-extended profile." If one of those terms is genuinely useful, define it in the same sentence
   the first time it appears, every time.
4. **Be concrete about problems.** When describing a problem or situation, make it unmistakable what is
   actually wrong and why it matters, in ordinary words.
5. **Offer documents for further reading** — point to the relevant file paths at the end, as optional
   depth, rather than assuming he'll go read them to understand the answer.

**Why:** Tiran asked for this explicitly on 2026-08-29, right after two exchanges where the shorthand
failed. He had to ask "what is dimension 6?" and then "I don't understand your statement about 3,456
versus 3,130" — both times because a numbered item from a project document and a set of raw measurements
were referenced as if already understood. He leads the project but does not hold every document's contents
in working memory, especially documents Claude authored minutes earlier. Coded references force him to go
look things up just to follow a sentence.

**How to apply:** applies to all conversational replies, summaries, and status updates. It does *not* mean
dumbing down the technical substance or hiding detail — the analysis stays rigorous, the *explanation* gets
plainer. Written artifacts (planning docs, analysis docs) may still use precise numbered/sectioned
conventions internally, since that is what makes them citable for the paper; but when talking *about* those
artifacts in conversation, translate. Related: [[feedback-v1-v2-framing]] covers a different kind of
framing rule (tone toward v1), not this one.
