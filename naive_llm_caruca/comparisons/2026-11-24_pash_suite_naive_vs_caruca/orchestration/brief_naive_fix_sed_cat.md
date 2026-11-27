# Brief: the naive LLM's `sed` fault, the `cat` question, and a vetted list of judgment errors

You are a worker. An orchestrating Claude session gave you this brief. Work only on it. Tiran asked for
this on 2026-11-24 after seeing the pilot (`report/report.html` and `README.md` in the parent folder).

## Rules that bind this work (read them first)

- `memory/feedback_instrument_defect_vs_tuning.md` and `memory/caruca_v2_baseline_scope.md`: the naive
  LLM is a deliberately weak control. **Never hand-edit a file the agent wrote, and never tune the prompt
  to win.** What is allowed is repairing the *instrument*: if the agent was not told a fact that makes a
  right answer impossible (here: how PaSh hands operands to the files), add that fact to the format
  description, record it as a repair, and re-run the agent the same way as before.
- `memory/feedback_readme_is_prompt_variant_log.md`: any change to what the agent is told goes into
  `naive_llm_caruca/README.md`'s log in the same turn (what changed, why, expected, observed).
- `memory/reference_naive_run_playbook.md`, `memory/project_requesty_llm_billing.md`: how a run is made
  (clone of the golden VM, Fable 5.1 medium, now billed through requesty.ai; the `naive-runs` worker's
  changes from today are in `naive_llm_caruca/vm/naive-run` and `fig7_campaign/run_campaign.py`).
- The Lima VM `pash` is running a timed batch: **no timing runs there**. Read-only use and cheap direct
  calls of annotation files are fine. The naive LLM runs in its own VM clone.

## 1. The `sed` fault: establish it, repair the instrument, regenerate

The checker showed (`orchestration/review_checker.md`, check 5, and its instrumented records in the
pash VM at `~/t024-check/sed_debug.txt`) that PaSh hands the naive `sed` file the sed script **with its
double quotes on** (`"s/[^[:print:]]//g"`), that the file's checker reads the opening `"` as an unknown
sed command and allows no split, and that asked directly without quotes the same file allows a split.
PaSh's own `sed` file handles the quotes.

1. Reproduce this yourself from the naive `sed` file (first Fig. 7 run of `sed`; find its folder via the
   `"repeat": 1` row in `fig7_campaign/ledger.jsonl`) and PaSh's own `sed` file. Show the exact code path.
2. Decide whether the agent could have known: read everything the agent was given about the PaSh file
   format and operands (`naive_llm_caruca/formats/`, `samples/`, the prompt). If nothing says that
   operands arrive as PaSh passes them (quotes kept), that is an instrument defect. Repair it with the
   smallest plain-language addition to the format description, and nothing else.
3. Re-run the naive LLM on `sed` exactly as the campaign does, with the repaired format description.
   Ledger row with `"repeat"` = next number and `"note": "after format repair 2026-11-24: operands arrive as PaSh passes them (quotes kept)"`,
   `"billing": "requesty"`. Budget: $5. Check the new files import, then ask the new `sed` file directly
   with the quoted operand exactly as PaSh passes it, and with the unquoted one; record both answers.
   Do not run PaSh on it (the VM is busy); the orchestrator will rerun the benchmark.
4. README log entry, as the rule requires.

## 2. The `cat` question: who is right?

Under the naive LLM's files and under Caruca's, PaSh splits a plain `cat FILE`; under PaSh's own files
it runs it whole. Tiran asks: is the naive LLM wrong, or is PaSh's own file wrong? Vet it:

- Read all three `cat` files (PaSh's own in the installed package, the naive LLM's first run, Caruca's
  from task 021's `sides.jsonl` rows) and say what each claims and why.
- Is splitting `cat` of one file *correct* (same output)? Is it *useful* (faster)? Separate the two. For
  usefulness use existing evidence only: task 022's observation on `cat` (its `observations.md`), the
  pilot's `naive-cat-pash-own` control (one untimed run), and reasoning about what PaSh does with a
  split `cat` (it reads the file in pieces and then joins them: say what that costs). No timing in the
  pash VM now; if a timed test is needed, write down exactly what to run later.
- Verdict, with evidence: judgment error (file is wrong about the command), design choice (file is
  right but chooses not to split), or instrument gap (the agent was not told what PaSh does with a
  split). Say it for the naive LLM and for Caruca separately.

## 3. Every difference in the pilot, classified

For each cell of Table 2 in `report/report.html` where a source differs from PaSh's own (`cat` ×3,
`sed` naive, `col` naive, `sort` Caruca ×2), write one row: the file's claim; the fact (what the command
really does, with how you checked); whose error, if anyone's (naive LLM / Caruca / PaSh's own / none);
the class (file does not parse its input correctly / wrong judgment about the command / design
limitation of the method / instrument gap); whether the output was still right; and what, if anything,
is being fixed. Then one paragraph each: are the naive LLM's and Caruca's errors the same kind, or
different kinds? Is any of PaSh's own files wrong on this script?

Write it as `orchestration/judgment_errors.md`, plain language (`memory/feedback_plain_language.md`),
every claim with its evidence. The orchestrator will put it in the report.

## When done

Reply with: the new `sed` run folder and both direct-call answers; the `cat` verdicts (naive, Caruca);
the path of `judgment_errors.md`; anything not established.
