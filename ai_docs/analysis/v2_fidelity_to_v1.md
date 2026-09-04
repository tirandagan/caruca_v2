# How caruca_v2 Works, and Exactly Where It Matches caruca v1

> **What this document is.** A line-by-line account of every mechanism in caruca_v2,
> paired with the v1 mechanism it reproduces. It exists to answer one question for a
> reviewer: *when v2 and v1 disagree, is that the LLM disagreeing, or is it the harness
> disagreeing?* Every row below is an answer to that question.
>
> **Status:** written 2026-09-03, covering the code delivered by tasks 001-004.
> **v1 reference commit:** `d8032407346aadc135b14c043618c8c1d4f4e0cf` (`binpash/caruca`).
> **v2 code reviewed:** `src/caruca_v2/` at 4,251 lines, 120 tests passing.

---

## 0. How to read this document

The honest framing matters more than a clean headline, so it goes first.

A document asserting *zero* deviation from v1 would not survive review, and it would not
be true. Some deviation is forced (v1's LLM step runs through DSPy 2.4, which no longer
exists; reproducing its exact wire format would mean depending on a dead library). Some is
deliberate (v2 measures token cost; v1 measures nothing). And the review that preceded
this document found four places where v2 diverges by *accident* — those are defects, and
they are listed as defects.

So every mechanism below carries one of three verdicts:

| Verdict | Meaning |
|---|---|
| **IDENTICAL** | v2 produces the same behavior as v1, and in most cases does so by *calling v1's own code* rather than reimplementing it. |
| **DELIBERATE** | v2 differs on purpose. The reason and the cost to comparability are stated. |
| **DEFECT** | v2 differs by accident. This is a bug, listed in §7, not a design choice. |

The strongest claim this project can make is not "we reimplemented v1 faithfully." It is
**"we did not reimplement v1 at all where it mattered."** Wherever fidelity is
load-bearing — environment construction, format validation, output-envelope assembly —
v2 shells out to v1's own interpreter and calls v1's own functions. Two copies of a
semantic can drift; one copy cannot.

---

## 1. Provenance: how the v1 facts in this document were obtained

Nothing here is inferred from the paper or from v1's own documentation. Every v1 fact was
obtained by reading v1's source at the pinned commit, or by executing v1 and observing the
result. Where a claim came from execution, the command is given so it can be re-run.

Two facts discovered this way contradict what the project's own planning documents said,
which is the point of doing it by execution:

- Task 002 stated that v1's `--max-arity` defaults to 2. **It defaults to 1**
  (`cli/__init__.py:29`). The paper's "two-flag limit" is the `--max-count` knob
  (default 4, `cli/__init__.py:54`), which is a different thing.
- Task 002 stated that `caruca generate CMD --number` gives the denominator for a
  coverage comparison. **It does not.** v1 computes `--number` from a different formula
  than its enumerator follows. For `mkdir` at arity 1 it reports **280** against **4,240**
  actual emitted lines (and 1,094 *unique* ones — v1 emits duplicates).

```sh
CARUCA=~/dev/stevens/caruca/caruca
cd $CARUCA && ./.venv/bin/caruca generate mkdir --max-arity 1 --number   # 280
cd $CARUCA && ./.venv/bin/caruca generate mkdir --max-arity 1 | wc -l    # 4240
cd $CARUCA && ./.venv/bin/caruca generate mkdir --max-arity 1 | sort -u | wc -l  # 1094
```

---

## 2. The three invariants that make fidelity checkable

These hold across every stage and are enforced structurally, not by convention.

### 2.1 v1 is a subprocess, never an import — IDENTICAL by construction

`import caruca` appears nowhere in v2's source or tests. Every interaction with v1 goes
through one boundary module, `src/caruca_v2/v1.py`, which runs v1's own interpreter
(`$CARUCA_V1_ROOT/caruca/.venv/bin/python`, Python 3.12.13) as a child process and
exchanges JSON with it.

Why this matters for fidelity: v2 runs on Python 3.12.9 with pydantic 2.13.5 and
`openai` 3.8.0. v1 runs on its own pinned environment. Importing v1 into v2's process
would silently resolve v1's dependencies against v2's versions, and a pydantic behavior
change would show up as an apparent v1/v2 disagreement. The subprocess boundary makes
that class of false result impossible.

```sh
# The check, mechanised:
grep -rn "^import caruca\b\|^from caruca\b" src tests --include='*.py' | grep -v caruca_v2
# (the only matches are inside triple-quoted subprocess script *strings* in v1.py,
#  and inside the fake-v1 package source that tests/conftest.py writes to disk)
```

### 2.2 No v1 text is committed to this repository — DELIBERATE (licensing)

v1 is private, unlicensed, and fork-restricted at the org level. Man pages, syntax specs,
data fixtures, and the DSL's value tables are read from `CARUCA_V1_ROOT` **at runtime** and
injected into prompts through `{{placeholder}}` substitution. The committed prompt files in
`prompts/` contain only text written for this project.

Consequence for reproducibility: a committed prompt file is not the full prompt. The full
assembled prompt is recorded in each run's `manifest.json` (`prompt_system`, `prompt_user`)
and identified by `prompt_hash` (SHA-256), which is what the write-up cites. Run directories
are gitignored for the same reason.

### 2.3 v1 judges v2's output, not the other way round — IDENTICAL by construction

Every stage's output is validated by v1's own code:

| Stage output | Validated by | Mechanism |
|---|---|---|
| `<cmd>.py` syntax spec | v1 importing it | `v1.validate_syntax_spec` runs v1's venv Python, imports the module, checks the binding |
| `<cmd>.configs.json` | v1's `CommandConfig` pydantic model | `v1.validate_configs` calls `CommandConfig.model_validate` per entry |
| `<cmd>.traces.json` | v1's `Traces` model | `v1.assemble_traces` *builds* the file through v1's models; `v1.validate_traces` re-reads it |
| `<cmd>.<fmt>.annotation` | v1's `PaSh` / `Posh` / `SaSh` models | `v1.validate_annotation` |

There is no v2-side reimplementation of any of these formats to drift against.

---

## 3. Stage 1 — syntax specification (`caruca-v2 naive-llm`)

**What it replaces:** v1's `llm.py` (163 lines), the only place v1 uses an LLM.

**v2 module:** `src/caruca_v2/stages/syntax_spec.py` (250 lines).

### 3.1 Input

| Aspect | v1 | v2 | Verdict |
|---|---|---|---|
| Documentation source | `doc_sources/man/<cmd>.txt`, read via `importlib.resources` (`llm.py:157-158`) | Same file, read from `CARUCA_V1_ROOT` (`v1.man_page`) | **IDENTICAL** |
| Corpus | 120 man pages | The same 120 files; no copies, no edits | **IDENTICAL** |
| Override | none | `--docs PATH` | **DELIBERATE** — additive. Default path is v1's, so the default condition is v1's. Recorded as `inputs.docs_source` in every manifest. |

### 3.2 Few-shot exemplars

| Aspect | v1 | v2 | Verdict |
|---|---|---|---|
| Which commands | `["touch", "rm", "mv", "ls"]` (`llm.py:116`) | The same four, in the same order (`v1.EXEMPLAR_COMMANDS`) | **IDENTICAL** |
| What each pairs | man page + the raw text of `syntax_specs/<cmd>.py` (`llm.py:118-123`) | The same two files, read at runtime | **IDENTICAL** |
| How they are serialised into the prompt | DSPy `LabeledFewShot(k=4)` wire format (`llm.py:129-131`) | Markdown sections rendered by `syntax_spec.render_exemplars` | **DELIBERATE** — see §6.1 |

### 3.3 Instruction text

v1's instructions live in a DSPy `Signature` docstring (`llm.py:30-66`). v2's live in
`prompts/syntax_spec/system.md`. The text is **paraphrased, not copied** (§2.2 — v1 is
unlicensed), but covers the same ground point for point:

| v1 instruction | v2 counterpart | Verdict |
|---|---|---|
| "expert on the shell and all kinds of commands" | "expert on the shell and on the full range of command-line programs" | **DELIBERATE** (wording) |
| "Only use features that you see in the examples" | "Use only the features you can see in the worked examples" | **DELIBERATE** (wording) |
| "Include all the flags and arguments... even ignored ones" | "Include every flag and every argument it mentions, including ones documented as accepted but ignored" | **DELIBERATE** (wording) |
| "Include both short and long versions of flags/options" | "Where a flag has both a short and a long form, give both" | **DELIBERATE** (wording) |
| "Arity... Don't use it as the number of arguments a flag takes" | "It is not the number of values a flag consumes" | **DELIBERATE** (wording) |
| The seven arity names | The same seven, verbatim | **IDENTICAL** — these are identifiers, not prose. All seven verified to exist in `ir/environment.py:24-32` |
| The 30-name value-type list | The same list, same order | **IDENTICAL** — identifiers |

The wording differences are unavoidable (licensing) and are the single largest known
threat to a clean stage-1 comparison. §6.1 says what to do about it.

### 3.4 Decoding configuration

| Parameter | v1 (`llm.py:109-114`) | v2 | Verdict |
|---|---|---|---|
| `max_tokens` | 4096 | 4096 (`llm.DEFAULT_MAX_TOKENS`) | **IDENTICAL** |
| `seed` | 42 | 42 (`llm.DEFAULT_SEED`) | **IDENTICAL** |
| Model | hardcoded `gpt-4o` | `--model`, required; `openai/gpt-4o` routed to OpenAI with fallbacks disabled | **DELIBERATE** — v1's model is a hardcoded constant with no configuration surface. Making it explicit is core v2 scope. Provider pinning exists so that `openai/gpt-4o` *is* the paper's model, not a re-host. |
| Temperature | never set → provider default | `--temperature`, required, recorded | **DELIBERATE** — v1 does not record what it used; v2 refuses to run without stating it. |
| Access layer | DSPy 2.4 `dspy.OpenAI` | `openai` SDK against OpenRouter | **DELIBERATE** — v1's path is dead code against DSPy 3.3.1. See §6.2. |

`max_tokens = 4096` **truncates option-heavy commands**, exactly as it did for v1. v2 does
not raise the limit to "fix" this: truncation is flagged (`output_truncated`,
`finish_reason: "length"`) and the run fails honestly.

### 3.5 Output extraction

v1's `extract_code` (`llm.py:20-27`):

```python
pattern = r"```.*?\n([\s\S]*?)```"
match = re.search(pattern, string)
return string if not match else match.group(1)
```

v2's `syntax_spec.FENCE_PATTERN` uses **the same regular expression**, and — importantly —
reproduces the fallback: when there is no fence, v1 treats the whole response as the spec,
and so does v2. **IDENTICAL.**

Task 001's draft said an unfenced response should fail immediately. That would have been a
divergence from v1, so v2 instead records `inputs.output_fenced: false` and lets validation
decide the outcome — an unfenced-but-valid response succeeds for v2 exactly as it would
have for v1.

### 3.6 Validation

| Aspect | v1 (`llm.py:135-150`) | v2 (`v1.validate_syntax_spec`) | Verdict |
|---|---|---|---|
| Method | import the generated file via `importlib.util` | The same, in v1's own interpreter | **IDENTICAL** |
| Working directory | the file's directory (`tempfile.NamedTemporaryFile(dir='.')`) | the file's directory (`cwd=spec_path.parent`) | **IDENTICAL** |
| Checks the `<cmd>_syntax_spec` binding | **No** — v1's check stops at import | **Yes** | **DELIBERATE** — additive and strictly stronger. v1's own command registration is reflective and requires the binding (`syntax_specs/__init__.py:15`), so a module that imports without it is unusable to v1 anyway. Reported separately from the import result. |
| On failure | `dspy.Suggest` triggers a **retry** with the error message (`llm.py:88-95`) | **No retry, ever** | **DELIBERATE** — this is the Eiers guardrail, §6.3. |

### 3.7 What v2 adds that v1 has nothing comparable to

Telemetry. v1 records no tokens, no cost, no wall-clock, no model ID. v2 records all of
them per call, plus `prompt_hash`, `seed`, and the full decoding configuration. This is
additive; it changes nothing about what is sent to the model.

---

## 4. Stage 2 — configuration generation (`caruca-v2 generate`)

**What it replaces:** `ir/string.py` (186) + `ir/environment.py` (420) + `ir/contents.py`
(74) + `ir/mixin.py` (35) = **715 lines** of nested combinatorial Python.

**v2 module:** `src/caruca_v2/stages/generate.py` (379 lines).

### 4.1 Input and bounds

| Aspect | v1 | v2 | Verdict |
|---|---|---|---|
| Spec source | `syntax_specs/<cmd>.py`, imported reflectively | The same file's **text**, read at runtime | **IDENTICAL** input; v2 reads it as text because the LLM reads text |
| `--max-arity` | default **1** (`cli/__init__.py:29`) | default 1 (`generate.V1_DEFAULT_MAX_ARITY`) | **IDENTICAL** |
| `--max-count` | default **4** (`cli/__init__.py:54`) | default 4 | **IDENTICAL** |
| `--stdin` | default `simple` (`cli/__init__.py:40`) | default `simple` | **IDENTICAL** |
| `--content` | default `simple` (`cli/__init__.py:47`) | default `simple` | **IDENTICAL** |
| `--skip` | no default → nothing skipped; `--skip` bare means `--version,--help,--interactive` | default: nothing skipped | **IDENTICAL** in effect |
| `--elaborate-relations` | flag, default off | not exposed; the probe table is extracted with it off | **IDENTICAL** at the default; the non-default path is not reachable in v2 |

Every one of these is recorded in `manifest.inputs`, because a v1/v2 comparison is only
meaningful when both sides used the same bounds.

### 4.2 The probe-value table — the subtlest fidelity problem in the project

A syntax spec **names** value types (`Glob`, `Signal`, `Permission`). It does not contain
the values those types expand into. Those live in v1's DSL runtime
(`ir/syntax.py:378-421`), as `MetaString` instances. An LLM reading only the spec file
cannot produce `*.txt` for a `Glob` argument, so *every* typed argument would mismatch and
the set-diff would be measuring a missing input rather than the model.

v2 therefore extracts the table from v1 at runtime and injects it into the prompt
(`v1.probe_values`): it instantiates every `ValueArgument` subclass in `caruca.ir.syntax`
and records what `.syntax()` yields. 39 types.

This is input material — the DSL's semantics — not a hint about method. The decision, and
its rationale, were recorded in task 002 before implementation.

**It reproduces v1's bugs deliberately.** `Hostname` is declared
`MetaString(("localhost"))` — a string, not a tuple, because the trailing comma is missing
— so it expands to the nine *characters* `l, o, c, a, l, h, o, s, t`. v2's table contains
those nine characters, because that is what v1 actually generates and therefore what the
comparison target is. Correcting it would create a divergence, not remove one.

```sh
# Re-derive the table:
.venv/bin/python -c "from caruca_v2 import v1; print(v1.probe_values()['Hostname'])"
# ['l', 'o', 'c', 'a', 'l', 'h', 'o', 's', 't']
```

| Type | v1 expansion | In v2's prompt | Verdict |
|---|---|---|---|
| `Glob` | `*.txt *.py *.c *.h` | same | **IDENTICAL** |
| `Path` | `relpath_N`, `abspath_N` (counter-based, `ir/syntax.py:227-249`) | same, counter reset per extraction | **IDENTICAL** |
| `Signal` | `"" HUP INT KILL STOP CONT 0` | same | **IDENTICAL** |
| `Hostname` | nine characters (v1 bug) | nine characters | **IDENTICAL** (bug reproduced on purpose) |
| all 39 | extracted, not transcribed | | **IDENTICAL** |

### 4.3 Output format

| Aspect | v1 | v2 | Verdict |
|---|---|---|---|
| Invocation strings | `caruca generate CMD` prints one per line | `<cmd>.invocations.txt`, one per line | **IDENTICAL** |
| Environment configs | `CommandConfig` objects (`ir/environment.py:380`) | `<cmd>.configs.json`, a list of the same serialised shape, validated by v1's model | **IDENTICAL** shape |
| Wire format from the model | n/a | JSON Lines: `{"invocation": ..., "config": ...}` per line | **DELIBERATE** — see §6.4 |

### 4.4 The comparison

`compare_invocations` set-diffs v2's invocation strings against v1's own
`caruca generate CMD` output, run live at comparison time rather than read from a stale
file. Reported: `matched`, `missing`, `spurious`, `recall`, `precision`, bounded samples,
plus **both** `v1_count` (raw lines) and `v1_unique_count` (deduplicated), because v1
emits duplicates. `v1_length_hint` (the `--number` value) is recorded but never used as a
denominator — see §1.

---

## 5. Stage 3 — execution and tracing (`caruca-v2 trace`)

**What it replaces:** `tracer/tracer.py` (217) + `tracer/strace_parser.py` (458) = **675
lines**.

**v2 modules:** `stages/trace.py` (472), `workspace.py` (106), `tools.py` (402).

This is the stage where fidelity is hardest and most load-bearing, because the LLM sees a
filesystem where v1 saw syscalls.

### 5.1 Workspace construction — IDENTICAL by construction

v2 does **not** reimplement v1's environment setup. `v1.materialize_config` runs a script
inside v1's interpreter that calls v1's own `prepare_env` on each body node — the same
calls `CommandConfig.env()` makes (`ir/environment.py:414-420`):

```python
for sequence in config.body:
    sequence.prepare(sandbox)          # v1's own code, v1's own interpreter
Path(stdin_path).write_bytes(config.stdin.value)   # v1's own Content enum
```

| Aspect | v1 (`ir/environment.py:414-420`) | v2 (`workspace.materialize`) | Verdict |
|---|---|---|---|
| Directory nesting | `TemporaryDirectory(prefix="toplevel_")` containing `TemporaryDirectory(prefix="sandbox_")` | `mkdtemp(prefix="caruca_v2_toplevel_")` containing `sandbox_inner/` | **IDENTICAL** in structure; names differ, and nothing reads the names |
| Parent directory | `/tmp` | the platform temp dir | **DEFECT** in the Lima case only — see §7.3 |
| File contents | `File.prepare_env` writes `content.value` | the same call | **IDENTICAL** |
| Directories | `Directory` / `NonEmptyDirectory` (the latter creates a `file` inside) | the same calls | **IDENTICAL** |
| Preconditions | `AlreadyExistantPath` / `NonexistentPath` raise if violated | the same calls; a raise is reported as `workspace_failed` | **IDENTICAL** |
| stdin payload | `config.stdin.value`, from `data/*.txt` via the `Content` enum | the same enum, the same fixture files | **IDENTICAL** |
| Fixture enrichment | — | **none added** | **IDENTICAL** — explicit Tiran directive 2026-09-03: no extra files, no richer fixtures |

Verified against the real checkout: a real `cat` config produced the real 849-byte
`HUMAN_TEXT` fixture (`human_1.txt` + `human_2.txt` concatenated, as v1's enum defines).

### 5.2 Execution environment

| Aspect | v1 (`tracer/tracer.py`) | v2 (`tools._run`) | Verdict |
|---|---|---|---|
| `PATH` | `/usr/bin:/bin:/usr/local/sbin:/usr/local/bin` (`:55`) | same constant, `v1.EXECUTION_ENV` | **IDENTICAL** value |
| `SHELL` | `/bin/sh` (`:56`) | same constant | **IDENTICAL** value |
| Everything else in the environment | **not inherited** — v1 passes only its own dict | **inherited** (`{**os.environ, ...}`) | **DEFECT** — §7.2 |
| Timeout | `timeout 2` (`:46`) | `subprocess` timeout of 2s | **IDENTICAL** duration; different mechanism (v1 wraps with the `timeout` binary because strace sits in between) |
| Working directory | `cwd=sandbox` (`:106`) | `cwd=workspace.sandbox` | **IDENTICAL** |
| stdin | `input=config.stdin.value` (`:105`) | the bytes v1 wrote for this config | **IDENTICAL** |
| Isolation | `CARUCA_ISOLATION_METHOD` = `try` (overlayfs) \| `docker` \| `none` | `--isolation host \| lima` | **DELIBERATE** — different mechanism, same intent. v1's `try` script needs Linux overlayfs. |

### 5.3 Observation — the irreducible difference

v1 observes with `strace -yfo --trace=%file,%desc,getcwd` plus the `try` summary, and
parses syscalls (`strace_parser.py`, 458 lines). v2's model observes with three
Python-side tools (`list_dir`, `read_file`, `stat_path`) and reports what it saw.

**This is the experiment, not a fidelity failure.** The gap between syscall-derived and
LLM-observed interactions is the quantity stage 3 exists to measure. What matters for
fidelity is that everything *around* the observation is identical, which §5.1, §5.2 and
§5.4 establish.

Observation deliberately does not spawn a binary, so "you may only use `cat`" survives the
model looking around. Enforced in code, and tested: `test_observation_tools_do_not_spawn_a_binary`.

### 5.4 Trace encoding and the sandbox namespace

| Aspect | v1 | v2 | Verdict |
|---|---|---|---|
| Action codes | `FSInteraction`: `rf wf ad mo de md rd` (`tracer/data.py:14-22`) | the same seven; anything else is dropped and counted, never coerced | **IDENTICAL** |
| Stream names | `stdin` / `stdout` / `stderr` passed through (`tracer.py:70-71`) | same | **IDENTICAL** |
| Absolute-path rewriting | `placeholder_sandbox / relpath(path, sandbox)` where `placeholder_sandbox = /tmp/sandbox_outer/sandbox_inner` (`tracer.py:59, 73-77`) | the same constant (`v1.PLACEHOLDER_SANDBOX`), the same rewrite (`Workspace.rewrite`) | **IDENTICAL** |
| Relative paths | passed through unchanged (`tracer.py:79`) | same | **IDENTICAL** |
| Paths outside the sandbox | v1 resolves them into the namespace regardless | v2 leaves them alone | **DELIBERATE** — v1's behavior here is the source of the macOS crash in §7.6; v2 not forcing them avoids fabricating a path |

The `/tmp/sandbox_outer/sandbox_inner` constant is **not cosmetic**: v1's annotator
hardcodes it (`tracer/data.py:266`). A traces file that skips the rewrite is unreadable by
v1's own tooling, which would make the stage-3 → stage-4 seam useless.

### 5.5 Traces envelope — IDENTICAL by construction

`v1.assemble_traces` builds the output file **through v1's own pydantic models** in v1's
interpreter:

```python
CommandInvocationTraces(command=CommandConfig.model_validate(...), return_code=..., traces=...)
CommandInvocationTraceSet(command=..., true_str=..., configs=[...])
Traces(sets).model_dump_json()
```

so a file that comes out is valid because v1 constructed it, not because v2 imitated the
format. Grouping mirrors v1's own: v1 groups by `CommandInvocation` (`tracer.py:200-210`),
v2 groups by the serialised `config.string`, which *is* `asdict(CommandInvocation)`
(`ir/string.py:169, 177`).

One approximation: v1's set-level `true_str` is `str(command)` on the `CommandInvocation`;
v2 uses the first grouped config's `true_string`. For the configs in a group these agree
whenever the body renders identically, which is the normal case. **DELIBERATE**, recorded
here because it is the one place stage 3 approximates rather than calls.

### 5.6 Safety — v2-only, and it constrains nothing v1 did

v1 ran inside an overlayfs sandbox, so it needed no allowlist. v2 runs model-chosen
argument vectors on a developer machine, so `tools.py` enforces: the binary allowlist
(`argv` must begin with the command under test), a path jail, and a refusal to run
destructive commands without an isolation backend. Every decision is recorded in
`checks.tool_audit`.

These are additive restrictions on *what the model may attempt*. They do not change how an
allowed invocation executes — §5.2 governs that.

---

## 6. Stage 4 — annotation (`caruca-v2 annotate`)

**What it replaces:** `tracer/data.py::to_annotation` + the whole `annotator/` package
(139 + 217 + 48 + 12 + 20 + 150 = **586 lines**; task 004's "~850" estimate also counted
the derivation half of `tracer/data.py`).

**v2 module:** `stages/annotate.py` (366 lines).

| Aspect | v1 (`cli/annotate.py`) | v2 | Verdict |
|---|---|---|---|
| CLI shape | `caruca annotate FORMAT CMD --input PATH` | `caruca-v2 annotate FORMAT CMD --traces PATH` | **IDENTICAL** in shape; the flag is renamed for clarity |
| Formats | `pash \| posh \| sash \| shellcheck` | the same four | **IDENTICAL** |
| Default input | `outputs/<cmd>.json` (`annotate.py:6`) | v1's `caruca/outputs/<cmd>.json` | **IDENTICAL** — which makes the A/B-on-identical-traces experiment the *default* behavior |
| Output for pash/posh/sash | `model_dump_json(indent=2, by_alias=True)` (`annotate.py:16`) | the model's own JSON, compared **structurally** | **DELIBERATE** — see below |
| Output for shellcheck | `annotations.code`, rendered Haskell (`annotate.py:12`) | the model's Haskell, compared textually | **IDENTICAL** in kind |
| Format definition given to the model | n/a (v1 is procedural) | v1's own pydantic JSON schema; for shellcheck, v1's own `render_shellcheck_module(cmd, [], None)` skeleton | **IDENTICAL** source — extracted at runtime, never transcribed |

Because v1 renders with `indent=2, by_alias=True` and a model will not reproduce byte-exact
formatting, the three JSON formats are compared **structurally** (`json.loads(a) == json.loads(b)`),
with the text diff also reported. Key order and indentation are not differences a downstream
consumer would notice; substantive differences are. Both numbers are recorded so the write-up
can keep presentation and substance apart — which task 004 explicitly requires.

The ShellCheck check is weaker (it verifies the output is a Caruca module) and the manifest
says so rather than presenting it as equivalent.

**Ground-truth diffs are labelled `annotation_diff` in the record itself**, never
`q1_execution`. The paper's Q1 numbers come from re-running PaSh/ShellCheck/Shseer's own
test suites; a diff against `benchmarks/annotations/` is a different methodology and the
two must never be blended (`memory/caruca_v1_eval_tooling_notes.md`).

---

## 7. Cross-cutting mechanisms

### 7.1 Command naming — IDENTICAL (with one trivial edge)

v1: `cmd_name.replace(" ", "_")` (`syntax_specs/__init__.py:11`), and the module must
define `<cmd>_syntax_spec`. v2: `v1.slug()` = `"_".join(command.split())`, and the same
binding name is required.

These agree on all normal input. They differ only if a command name contains consecutive
spaces (`git  commit` → v1 `git__commit`, v2 `git_commit`), which no corpus entry does.

### 7.2 CLI surface

| v1 | v2 | Verdict |
|---|---|---|
| `caruca syntax-spec CMD` | `caruca-v2 naive-llm CMD` | **DELIBERATE** name — v2's is explicitly the naive control, not a drop-in |
| `caruca generate CMD` | `caruca-v2 generate CMD` | **IDENTICAL** |
| `caruca trace CMD` | `caruca-v2 trace CMD` | **IDENTICAL** |
| `caruca annotate FORMAT CMD` | `caruca-v2 annotate FORMAT CMD` | **IDENTICAL** |
| `caruca oracle` | not implemented | gap, not deviation |
| argparse, subparsers | argparse, subparsers | **IDENTICAL** — chosen for v1 parity over ergonomics |

Every subcommand is a thin wrapper over one typed function in `stages/`, so the harness can
call the function directly. `--model` and `--temperature` are **required** until the
configuration-selection phase freezes them, so no run can be recorded without stating the
configuration that produced it.

### 7.3 Retry behavior — the guardrail

v1's LLM step retries on validation failure (`dspy.Suggest`, `llm.py:88-95`). v2 **never**
retries, anywhere, in any stage. The only continuation v2 sends fires when
`finish_reason == "length"` — i.e. the token cap, not the model, ended the response — and
`checks.parse.hit_turn_cap_while_truncated` distinguishes the two.

This is the largest deliberate divergence in the project and it is not an oversight: it is
Prof. Eiers' guardrail. A control that quietly re-asks until it succeeds is no longer a
control.

---

## 8. Consolidated deviation ledger

### 8.1 Deliberate, with reasons

| # | Deviation | Why it is unavoidable or right | Effect on comparability |
|---|---|---|---|
| 1 | **Few-shot rendering.** v1 serialises exemplars through DSPy's `LabeledFewShot`; v2 renders the same four pairs as Markdown. | Reproducing DSPy 2.4's wire format would mean depending on a library that no longer exists. The exemplar *content* is byte-identical. | Stage-1 only. The largest single confound in stage 1. **Mitigation:** the configuration-selection phase should include a prompt-phrasing arm, so the size of this effect is measured rather than assumed. |
| 2 | **Access layer.** DSPy → OpenRouter + `openai` SDK. | v1's path dies at import against DSPy 3.3.1. v1 itself used a gateway library; the "naive" rule governs the prompting method, not the plumbing. | Cost figures are OpenRouter-billed and may differ marginally from provider list prices. Stated with every cost number. |
| 3 | **No retry.** | The Eiers guardrail (§7.3). | Intentional: v2's stage 1 should look *worse* than v1's on first-pass validation. That is the finding. |
| 4 | **JSON Lines output in stage 2.** | A continuation can append lines; a truncated last line can be dropped and counted. A truncated JSON *array* would have to be repaired, and a repaired line is partly our output. | None — the assembled `configs.json` is the v1 shape and v1 validates it. |
| 5 | **Instruction wording paraphrased.** | v1 is unlicensed; its docstring cannot be committed here. | Same confound as #1, same mitigation. |
| 6 | **Model, temperature, and output format are explicit and recorded.** | v1 has no configuration surface at all; selecting one is core v2 scope. | Additive. Frozen once, up front. |
| 7 | **Telemetry, manifests, `metrics.db`.** | v1 measures nothing. | Additive; never written into a v1-format file. |
| 8 | **Stage-3 tool surface and safety refusals.** | v1 had an overlayfs sandbox; v2 runs on a developer Mac. | Restricts what the model may *attempt*; does not change how an allowed invocation runs. |
| 9 | **Set-level `true_str` approximation** (§5.5). | Reconstructing a `CommandInvocation` from its serialised form would mean reimplementing it. | Nil in the normal case; noted so a reviewer can check it. |
| 10 | **Structural rather than byte comparison for JSON annotations.** | v1 renders `indent=2, by_alias=True`; a model will not match formatting. | Both structural and textual results recorded. |

### 8.2 Accidental — these are defects, found in the 2026-09-03 review

These are **not** design choices. Each is a place where v2 currently diverges from v1 by
mistake, and each is fixable.

| # | Defect | Fidelity impact |
|---|---|---|
| 1 | **Stage 3 inherits the full process environment.** `tools._run` passes `{**os.environ, **v1.EXECUTION_ENV}`; v1 passes *only* `{PATH, SHELL}`. Inherited `LANG`/`LC_ALL`/`HOME`/`COLUMNS` change what `ls`, `sort`, `wc`, and `date` actually do. | **High.** Every stage-3 fidelity comparison would be run against a different environment than v1's. Fix: pass `v1.EXECUTION_ENV` alone. |
| 2 | **Stage 2 does not pass `--max-count` or `--skip` to the v1 reference run.** The prompt states one bound; `caruca generate` is invoked with v1's defaults. Proven: `--max-count 1` yields 44 invocations, the default 4 yields 4,240. | **High.** Any run with a non-default bound produces a meaningless set-diff. |
| 3 | **`--isolation lima` cannot work.** Workspaces are created under the platform temp dir (`/var/folders/...` on macOS); the Lima VM mounts only `$HOME`, so the workspace does not exist in the guest and `cwd` points at nothing. | **High.** Destructive commands *require* lima, so `rm`-class tracing is currently impossible. |
| 4 | **The path jail admits relative traversal.** `tools._check_argv` validates only arguments beginning with `/`. `cat ../../../etc/hosts` executed successfully. | **Safety, not fidelity** — but it is the stated boundary for the one place model-chosen commands reach a shell. |
| 5 | **Per-configuration cost is not recorded.** `checks.sessions` has turn counts but no tokens/cost/wall-clock, and telemetry records carry no config index. | **Medium.** Task 003's "cost/latency per config recorded" criterion is not actually met. |
| 6 | **Run-id entropy is 16 bits.** `secrets.token_hex(2)`; ~7% collision at 100 same-second runs, 71% at 400. A collision raises an uncaught `FileExistsError`. | **Medium**, and it will bite the full-corpus harness before it bites the CLI. |
| 7 | **`ui.detail` mangles bracket-containing invocations.** `find . -name '[a-z]*'` displays as `find . -name '*'`; `cat a[/]b` raises `MarkupError`. | **Low** (presentation), but it silently misreports what was run. |

### 8.3 A v1 defect that constrains v2

**v1's `annotate` cannot run on macOS at all.** `tracer/data.py::__readwrite` resolves each
traced path and calls `relative_to("/tmp/sandbox_outer/sandbox_inner")`; macOS resolves
`/tmp` to `/private/tmp`, so the path leaves the prefix and `relative_to` raises. Verified
against v1's own committed `outputs/ls.json`. Not data-dependent — it fails on every input.

Consequence: the v1 side of every annotation diff must run in the Lima VM
(`--v1-runner lima`). Recorded in `memory/caruca_v1_macos_annotate_limitation.md`.

---

## 9. How to re-verify every claim here

```sh
CARUCA=~/dev/stevens/caruca                 # v1 (Mac path; ~/stevens/caruca on the WSL PC)
V2=~/dev/stevens/caruca_v2                  # this repo

# v1 commit this document describes
git -C $CARUCA rev-parse HEAD               # d8032407346aadc135b14c043618c8c1d4f4e0cf

# §2.1 — no v1 imports in v2
grep -rn "^import caruca\b\|^from caruca\b" $V2/src $V2/tests --include='*.py' | grep -v caruca_v2

# §3.4 — v1's decoding constants
sed -n '108,116p' $CARUCA/caruca/src/caruca/llm.py

# §3.5 — the fence regex is the same on both sides
sed -n '20,27p' $CARUCA/caruca/src/caruca/llm.py
grep -n "FENCE_PATTERN" $V2/src/caruca_v2/stages/syntax_spec.py

# §4.1 — v1's real CLI defaults
sed -n '26,58p' $CARUCA/caruca/src/caruca/cli/__init__.py

# §4.2 — the probe table, extracted live from v1
$V2/.venv/bin/python -c "from caruca_v2 import v1; import json; print(json.dumps(v1.probe_values(), indent=1))"

# §5.2 — v1's execution environment
sed -n '44,60p' $CARUCA/caruca/src/caruca/tracer/tracer.py

# §5.4 — the hardcoded sandbox namespace, on both sides of the seam
grep -n "sandbox_outer" $CARUCA/caruca/src/caruca/tracer/tracer.py \
                        $CARUCA/caruca/src/caruca/tracer/data.py
grep -n "PLACEHOLDER_SANDBOX" $V2/src/caruca_v2/v1.py

# §8.3 — v1's annotate failing on macOS
cd $CARUCA/caruca && ./.venv/bin/caruca annotate pash ls --input outputs/ls.json

# The whole v2 suite (no API money, no v1 checkout required)
cd $V2 && .venv/bin/pytest -q && .venv/bin/ruff check src tests
```

---

## 10. What a reviewer should take from this

1. Where fidelity is load-bearing, v2 does not reimplement v1 — it **calls** v1. Workspace
   construction, format validation, and Traces assembly all run inside v1's own interpreter
   against v1's own models. There is no second copy to drift.
2. Every deliberate deviation is enumerated in §8.1 with its reason and its cost. The two
   that most threaten stage 1 (few-shot rendering, paraphrased instructions) share one
   mitigation: measure them as an arm of the configuration selection rather than assuming
   they are negligible.
3. Seven accidental deviations exist today (§8.2). Three of them would corrupt a stage-2 or
   stage-3 comparison if a run were done now. **No comparison numbers should be generated
   until items 1-3 of §8.2 are fixed.**
4. Every claim above is re-derivable with §9's commands against a pinned v1 commit.
