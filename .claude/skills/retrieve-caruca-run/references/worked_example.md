<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!--
 caruca_v2 agent skill: Retrieve caruca run.
 Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
 Licensed under the PolyForm Noncommercial License 1.0.0
 https://polyformproject.org/licenses/noncommercial/1.0.0
 Noncommercial use only. Commercial use is prohibited.
-->
<!-- ATTRIBUTION-NOTICE:END -->

# A divergence explained end to end

A real question, answered with these scripts. The point is not the conclusion — it is
already written up — but the shape of the reasoning, which generalises to any stage and
any command.

> **The question.** On the comparison for `cat`, v1 emits only single-argument invocations
> while v2 adds a second argument (`abspath_1`, `relpath_1`). Does that go against the
> requirements set up in the original article and codebase?

Note what is being asked. Not "what is the score" but "who is wrong" — and the answer
turns out to be different for the paper than for the code. A reply that only reported
0.556 would have answered nothing.

## 1. What does the record say?

```sh
python3 $S/caruca_run.py cat -s 2 -v numbers
```

Invocation F1 **0.556** over v1's 15 distinct invocations at `--max-arity 1 --max-count 1`.
Recall **1.000**, precision **0.385**, 15 matched, 0 missing, 24 spurious, identical across
all three samples.

Read that shape before going further. Recall 1.0 with low precision means v2 produced
everything v1 did *and more* — so this is not a model that failed to enumerate. Something
made it enumerate more. Zero spread across samples means it is deterministic, so it is not
sampling noise either. Both facts point away from "the model got it wrong".

## 2. What are the items?

```sh
python3 $S/caruca_run.py cat -s 2 -v items
```

All 24 surplus invocations have the same shape: a flag that v1 also emitted, plus a file
operand. `cat -A abspath_1`, `cat -n relpath_1`. Not one is a flag v1 does not know, or a
malformed line. A surplus with a single uniform shape is a rule disagreement, not a
mistake — mistakes are not that tidy.

## 3. What was the model actually told?

```sh
python3 $S/caruca_run.py cat -s 2 -v prompt
```

> At most 1 optional **flags** may be combined in a single invocation.

By that instruction `cat -A abspath_1` is correct: it has one flag. The operand is not a
flag. So before blaming the model, the question becomes whether the instruction matches
what v1 enforces.

## 4. What does v1 actually enforce?

```sh
python3 $S/v1_probe.py --source filtered_args
```

`ir/syntax.py::__filtered_args` selects over every argument where `is_optional()` holds —
`Arity.OPTIONAL` or `Arity.ZERO_OR_MORE` — across all argument positions. That includes
positionals.

```sh
python3 $S/v1_probe.py cat --spec
```

`cat`'s operand is `Path(arity=Arity.ZERO_OR_MORE)`, so it *is* optional, so it consumes
one of the budget slots the prompt reserves for flags.

The prompt's wording is v1's own CLI help text — *"the maximum number of optional flags to
use for a single invocation"* — which does not describe what v1's code does. v2 was handed
v1's documentation, and v1's documentation is wrong about v1.

## 5. Test it by moving the bound

```sh
python3 $S/v1_probe.py cat --vs-v2 --max-count 2
```

```
only in v1       66
only in v2        0
```

At `--max-count 2`, every one of v2's 39 invocations is something v1 itself emits. The
surplus is not invention; it is v1's own output one notch looser. The flag histogram the
script prints says the same thing from the other side: both sides cap at one flag, but v2
has 36 one-flag invocations to v1's 12, because v2 attaches operands.

**This step is what makes the answer a conclusion rather than a story.** A hypothesis you
can make vanish by changing one parameter is established. Always look for the parameter.

## 6. What does the paper say?

`ai_docs/refs/caruca_white_paper.md` §4.1 counts *"flags and options"* per invocation —
64.7% of real invocations use none, 29.0% one, 5.9% two — and §4.2 states the two axes
separately: Caruca explores "(1) combinations of flags and options **and** (2) several
possible values for each positional and option argument."

The budget belongs to axis 1. Positional values are axis 2. So the paper agrees with the
prompt, and v1's implementation is the outlier — which also means the paper's own ">99%
coverage at ≤2 flags" is overstated for any command with an optional operand, since one
slot silently goes to the operand.

## 7. Has this been written up?

```sh
python3 $S/find_writeups.py cat --topic operand
```

Three documents, and they do not agree:

- `ai_docs/analysis/v1_v2_parity_study.md` §3.2, titled *"v2 does not respect the
  enumeration bound"* — attributes the cause to v2.
- `ai_docs/tasks/011_v2_improvement_program.md` — states that §3.2 **misattributes** it:
  403 of 414 surplus invocations are the prompt's wording. **This is the current view.**
- `ai_docs/analysis/white_paper_addendum.md` — raises it with the paper's authors as an
  open question.

Had the search come first, the parity study's confident section title would likely have
been repeated. Deriving the answer first is what surfaces the disagreement.

## The answer

**Against v1's code, yes; against v1's documentation and the paper, no.** That split is
the finding. v2 obeyed the instruction it was given; the instruction was v1's help text;
v1's help text does not describe v1's behaviour; and the paper sides with the help text.

## The shape, generalised

1. **Score** — and read its *shape*, not just its value. Recall vs. precision, and spread
   across samples, already narrow the cause before you look at anything else.
2. **Items** — a uniform surplus is a rule disagreement; a scattered one is a model error.
3. **Prompt as sent** — what was the model actually asked for?
4. **v1's source** — what does the code enforce, as against what it documents?
5. **Move a parameter** — make the divergence appear or vanish on demand.
6. **The paper** — when v1 and its documentation disagree, the paper breaks the tie.
7. **The write-ups** — last, so you notice when they conflict with what you just derived.

Steps 3-6 are the ones a score alone cannot give you, and they are where the reportable
finding almost always is.
