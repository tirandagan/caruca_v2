---
name: feedback-instrument-defect-vs-tuning
description: "Fixing a prompt/schema that makes a valid answer impossible is an instrument repair, not the excluded 'tuning to win'; Tiran's line, set 2026-09-14"
metadata:
  type: feedback
---

When a caruca_v2 replication stage (tasks 002-004) fails v1 validation, **check whether the
request we sent could have been answered at all before concluding anything about the model.**
Tiran drew this line explicitly on 2026-09-14 while debugging `generate` on `grep`.

**The distinction that governs:**
- **Instrument defect — fix it, no debate.** No setting of the prompt could produce a valid
  answer, so there is nothing being tuned *toward*. Three real examples, all in the JSON
  Schema handed to the model understating v1's actual constraints: `PlainValidator` fields
  rendering as empty schemas, discriminator tags omitted from `required`, and a prompt
  sentence that contradicted the spec it shipped with.
- **Measurement defect — fix it, and say so.** The set-diff charged one convention difference
  (`--color=always` vs `--color always`) to recall *and* precision simultaneously. Fixed by
  normalizing to an argument vector, with the literal figures still reported alongside.
- **Tuning — excluded**, per [[caruca-v2-baseline-scope]]. Iteratively reshaping a prompt to
  raise a score against v1. Also excluded: telling the model how many items to expect (that
  leaks v1's answer) and widening a normalizer until differences disappear.
- **Deliberate scope change — allowed, but it is Tiran's call and must be recorded as such.**
  Reversing `generate`'s "a model that stops on its own has finished" continuation rule was
  approved on 2026-09-14. It is *not* filed as a bug fix, because the old behavior was a
  documented design decision. Every run now records `continuation_policy` / `turns_used` /
  `model_declared_complete`, and any result from that stage must state that a nudged model is
  partly measuring the nudge.

**Why:** the naive control (task 001) exists to be weak and must never be engineered. The
replication arms are different — they are meant to test whether an LLM *can* do v1's work, and
a question the model cannot answer tests nothing. Conflating the two either flatters the model
or slanders it.

**How to apply:** before spending on a re-run, reproduce the rejection offline against the
artifact already on disk (patch the suspect field into the existing output and re-validate
through v1). That is free, and on 2026-09-14 it proved there was no further defect waiting
before a paid run. Full write-up: `ai_docs/tasks/002_llm_config_generation.md` §6.
