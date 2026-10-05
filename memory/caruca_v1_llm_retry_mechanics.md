---
name: caruca-v1-llm-retry-mechanics
description: "How v1's llm.py 'iteratively prompts' the model: exact prompt layout, validation, the 3-attempt DSPy backtrack loop, and why the feedback is only injected on DSPy >= 2.4.16 (.venv-llm had 2.4.9, where retries are inert)"
metadata:
  type: reference
---

Answers "how does v1 mechanically do the iterative prompting the white paper's syntax-inference section
describes?" Established 2026-10-05 by reading `caruca/src/caruca/llm.py` and the DSPy source, then running
v1's real, unmodified `doc_to_dsl("mkdir")` against a stand-in model that returns scripted answers (no
network). Every statement below was observed in those runs or read directly from source; the "Not tested"
section lists what was not. Complements [[caruca-v1-pipeline-reference]].

## The call chain (v1 `llm.py`)

1. `caruca syntax-spec CMD` → `cli/syntax_spec.py` → `llm.doc_to_dsl(CMD)` and prints the result. Nothing
   else in v1 calls the LLM.
2. The documentation is **not** read from stdin or from live `man`: `_doc_for` reads the bundled file
   `src/caruca/doc_sources/man/<CMD>.txt`.
3. Four few-shot examples (`touch`, `rm`, `mv`, `ls`): each pairs the bundled man page with the raw text of
   the hand-written `syntax_specs/<c>.py`. `LabeledFewShot(k=4)` attaches them to the predictor.
4. The predictor is `dspy.ChainOfThought(Signature)`. The `Signature` docstring is the instruction text
   (role, rules, the list of allowed arity names and type names).
5. Request settings observed at the OpenAI SDK boundary (DSPy 2.4.9): `model=gpt-4o, temperature=0.0,
   seed=42, max_tokens=4096, top_p=1, n=1`. The whole prompt is sent as **one user message**, no system
   message.

## Prompt layout, first attempt (observed, ~25,500 characters for `mkdir`)

Blocks separated by `---`:
1. the instruction text;
2. a format block: `Man Page:` / `Reasoning: Let's think step by step in order to ...` / `Syntax Spec:`;
3. the four examples, each `Man Page: <text>` then `Syntax Spec: <spec>` (no reasoning shown);
4. the target command's man page, ending with the open line `Reasoning: Let's think step by step in order to`.

The model continues from that open line; DSPy splits the reply at the `Syntax Spec:` label. `extract_code`
then keeps the contents of the first ``` fenced block (or the whole string if there is no fence).

## Validation

`DocumentationParser.forward` writes the extracted code to a temporary `.py` file **in the current working
directory** and imports it (`validate_syntax_spec` → `import_from_path`). Valid means "the import raised no
exception". It does not check that a `<CMD>_syntax_spec` variable exists, and it does not compare the spec
with the documentation. The exception text becomes the feedback message. The module is registered as
`sys.modules[<CMD>]`.

## The retry loop

`dspy.Suggest(result, <message with the error text>, target_module=self.cot)` raises when the import
failed. `assert_transform_module(module, backtrack_handler)` wraps `forward` in DSPy's `backtrack_handler`,
whose default is `max_backtracks=2`: **at most three attempts in total**.

On the third attempt DSPy runs with suggestions bypassed: a failure is logged (`SuggestionFailed: ...`) and
**the invalid spec is returned and printed**. There is no exception and no abort. Observed on both DSPy
versions tested. (The white paper says Caruca "will issue an error message and abort".)

## Feedback injection depends on the DSPy version

`backtrack_handler` decides which predictor to re-run by comparing each traced module with `target_module`:

| DSPy release | Comparison in `dspy/primitives/assertions.py` | Result with v1's `target_module=self.cot` |
|---|---|---|
| 2.4.9 through 2.4.14 | `mod.signature == error_target_module` | never matches; logs "Specified module not found in trace" |
| 2.4.16 through 2.5.43 | `mod == error_target_module` | matches |

(2.4.15 was not inspected. Releases 2.6 and later removed these APIs; v1's `llm.py` does not import there.)

**When it matches (run on DSPy 2.5.17):** the retry prompt gains three fields after the man page:
`Previous Reasoning:`, `Previous Syntax Spec:` (the failed output), and `Instructions:` (the feedback
message containing the Python error). On the third attempt `Instructions:` holds both distinct error
messages. This is the behaviour the white paper describes.

**When it does not match (run on DSPy 2.4.9):** all three attempts send a **byte-identical prompt**: no
previous output, no error message. In addition, DSPy 2.4.9's `dspy.OpenAI` caches requests on disk with
joblib (default `~/cachedir_joblib`, disabled by `DSP_CACHEBOOL=false`, relocated by `DSP_CACHEDIR`). With
identical prompt and settings, DSPy issued three requests but **only one reached the OpenAI SDK**; the other
two were cache replays of the same invalid answer. A second process using the same cache directory made
zero SDK calls.

## State of the local environments (checked 2026-10-05, Mac)

- v1's `pyproject.toml` lists `dspy-ai` with no version pin.
- `caruca/caruca/.venv-llm`: dspy-ai **2.4.9** (the no-match case above), openai 1.109.1.
- `caruca/caruca/.venv`: dspy 3.3.1; `.venv-linux`: dspy 3.4.0. Neither has `dspy.Suggest`.
- `target_module=self.cot` has been in `llm.py` since the commit that introduced the feedback loop
  (`60efe62f9`, 2024-10-26). DSPy 2.4.16 was published 2024-09-13; 2.5.17 on 2024-10-26.

## Differences between the white paper's description and the v1 code

| White paper says | v1 code does |
|---|---|
| three examples (`rm`, `mv`, `touch`) | four (`touch`, `rm`, `mv`, `ls`) |
| after three failed attempts: error message and abort | third attempt's output is returned even if invalid |
| retry includes previous output and error message | true on DSPy >= 2.4.16; not on DSPy <= 2.4.14 |
| `man rm \| caruca > rm.spec` | `caruca syntax-spec rm`, reading the bundled man page file |

## Not tested

- The real OpenAI network path on any DSPy 2.5.x release (the 2.5.17 run used the stand-in model only).
- Which DSPy version the paper's authors had installed when they produced their results.
- Whether any committed v1 spec was ever produced by a retry.

**How to apply:** before running or interpreting any v1 syntax-inference result, check the dspy-ai version
of the virtualenv used. Results produced through `.venv-llm` as it stood on 2026-10-05 come from a v1 whose
retry sends no feedback. Re-check the installed version before repeating that claim; it is a point-in-time
observation.
