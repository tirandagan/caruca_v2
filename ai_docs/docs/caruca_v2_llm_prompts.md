# caruca_v2 — Inventory of LLM Prompts

Every piece of text this repository sends to a language model, listed against the pipeline
step it belongs to, with the text itself reproduced verbatim.

Pinned to commit `0c86a8e` ("Enhance LLM and generate stages with exhaustive continuation
support", 2026-09-08). Prompt wording is a frozen experimental parameter — an edit changes
the `prompt_hash` recorded in telemetry and therefore invalidates comparability with runs
already on record — so this inventory is only valid for that commit. Re-generate it after
any prompt change.

## How prompts are assembled

Every instruction lives in `prompts/` as Markdown and is loaded verbatim at runtime;
nothing is built from string literals in Python. One directory per pipeline stage, each
holding `system.md` (the system message) and `user.md` (the single user message).
`src/caruca_v2/prompting.py` loads the two files, replaces `{{placeholders}}` by plain
ordered string substitution — no expressions, no conditionals, no escaping — and hashes the
result (SHA-256 over system, a NUL byte, then user) into the `prompt_hash` that goes into
every telemetry record. An unfilled placeholder raises rather than sending a prompt with a
literal `{{man_page}}` in it.

The values injected through those placeholders — man pages, committed syntax specs, trace
fixtures — come from the caruca v1 checkout at runtime and are deliberately never written
into a file in this repository, because v1 is private and unlicensed.

---

## 1. Prompt files, by pipeline step

The v1 column names the hand-written component each stage stands in for, so the table
doubles as the correspondence between the two systems.

| # | Pipeline step | v1 equivalent (paper §) | Stage dir | File | Location | Role | Placeholders | Verbatim text |
|---|---|---|---|---|---|---|---|---|
| 1 | Syntax inference — documentation in, syntax specification out | `llm.py` + `ir/syntax.py` (§3) — the one place v1 itself uses an LLM | `syntax_spec` | `system.md` | `prompts/syntax_spec/system.md` | Defines the DSL contract: use only constructors the examples show, cover the whole documented interface, `arity` semantics, the closed list of value types, output as one fenced Python file binding `<command>_syntax_spec` | *(none)* | [§4.1](#41-stage-1--syntax_specsystemmd) |
| 1 | Syntax inference | same | `syntax_spec` | `user.md` | `prompts/syntax_spec/user.md` | Carries the four few-shot exemplars, the target command's man page, and the symbol name to define | `{{few_shot_examples}}`, `{{command}}`, `{{man_page}}`, `{{spec_symbol}}` | [§4.2](#42-stage-1--syntax_specusermd) |
| 2 | Configuration generation — syntax specification in, concrete invocations + environments out | `ir/string.py` + `ir/environment.py` (§4) | `generate` | `system.md` | `prompts/generate/system.md` | Explains the DSL input, the probe-value table, the `Selection`/`List` inline-choices exception, the JSON Lines output contract (`invocation` + `config`), and the no-abbreviation / continue-on-request rule | `{{config_schema}}` | [§4.3](#43-stage-2--generatesystemmd) |
| 2 | Configuration generation | same | `generate` | `user.md` | `prompts/generate/user.md` | Supplies the command, its specification, the probe values, and the bounds (arity cap, flag-combination cap, skipped flags, stdin and content variation) | `{{command}}`, `{{syntax_spec}}`, `{{probe_values}}`, `{{max_arity}}`, `{{max_count}}`, `{{skip_flags}}`, `{{stdin_variation}}`, `{{stdin_values}}`, `{{content_variation}}`, `{{content_values}}` | [§4.4](#44-stage-2--generateusermd) |
| 3 | Isolated tracing — one invocation run and observed | `tracer/` (§5) — `strace` in an overlayfs sandbox | `trace` | `system.md` | `prompts/trace/system.md` | The agent contract: only `{{command}}` may be run, observation tools do not execute anything, everything stays inside the working directory, and the report goes through `report_observations` using v1's seven action codes | `{{command}}` | [§4.5](#45-stage-3--tracesystemmd) |
| 3 | Isolated tracing | same | `trace` | `user.md` | `prompts/trace/user.md` | The single invocation to run, the pre-run directory listing, and the name of the stdin fixture already wired up | `{{invocation}}`, `{{listing}}`, `{{stdin_name}}` | [§4.6](#46-stage-3--traceusermd) |
| 4 | Specification derivation + annotation — traces in, one consumer's annotation out | `tracer/data.py::to_annotation` + the whole `annotator/` package (§6) | `annotate` | `system.md` | `prompts/annotate/system.md` | Describes the traces input and action codes, asks for inputs/outputs, parallelizability, divisibility, pre/post-conditions, and imposes the assert-only-what-the-traces-support rule; the output format is injected per consumer | `{{format_instructions}}` | [§4.7](#47-stage-4--annotatesystemmd) |
| 4 | Specification derivation + annotation | same | `annotate` | `user.md` | `prompts/annotate/user.md` | The command, the target consumer (PaSh / POSH / SaSh / ShellCheck), and the traces JSON | `{{command}}`, `{{format}}`, `{{traces}}` | [§4.8](#48-stage-4--annotateusermd) |

`prompts/README.md` sits alongside these but contains no prompt text — it is the policy
note on layout, placeholder semantics, what may be committed, and why editing a frozen
prompt is a new experimental condition.

### File digests

The SHA-256 of each template file, for identifying the version this inventory describes.
These are **not** the runtime `prompt_hash`, which is computed over the *assembled* system
and user messages after substitution.

| File | SHA-256 |
|---|---|
| `prompts/syntax_spec/system.md` | `418b933fe4eeee5537a8f27fefc00419eb19794be41e13b0a18a7638344335d8` |
| `prompts/syntax_spec/user.md` | `aff8a71569080a4dcc603396dc68980ffcc09b4104a5c01fdd050f20b0683bd7` |
| `prompts/generate/system.md` | `3757e26bd83a34eab513c31ed43ee97c3d0d52a364fad29fd0616f139f3cd7a6` |
| `prompts/generate/user.md` | `55392bdeedfdd6e398fb22174ec72e60821cd38d1c8dddf4c54a9aa08ed6b4da` |
| `prompts/trace/system.md` | `1a74343d5fa53bc8411daa8b1dee98b2ebe07c2422fc499634e4086d419b0717` |
| `prompts/trace/user.md` | `f36f874148f4a9840475e4d0ccd607a33752df438d252d9a2384fd7fcfd4108e` |
| `prompts/annotate/system.md` | `a70b1af996e25d9f2c7317b21d138f6e2c626cb44faecdf65dd239ef7728dd7c` |
| `prompts/annotate/user.md` | `952c8fde4a050a045314ceff08d061ba781727253f6832a479ebca525237fc42` |

---

## 2. Model-facing text that lives in Python

The `prompts/` rule covers the two message templates per stage. Four other kinds of text
still reach the model and are not in `prompts/`: mid-conversation continuation
instructions, the per-consumer output-format block substituted into
`{{format_instructions}}`, the few-shot exemplar framing substituted into
`{{few_shot_examples}}`, and the stage-3 tool schemas with their descriptions. They are
listed here because a reader auditing "everything the model was told" needs them, and
because they are *not* covered by `prompt_hash` — the hash is taken before any of them are
appended.

| File | Location | Applies to | Text sent to the model |
|---|---|---|---|
| `llm.py` | `src/caruca_v2/llm.py:165` — `CONTINUE_INSTRUCTION` | Any stage whose response hits the token cap (`finish_reason == "length"`): stages 2 and 4 use it via `complete_series`, and stage 3 via the tool loop | `Continue from exactly where you stopped. Same format, no repetition, no commentary.` |
| `llm.py` | `src/caruca_v2/llm.py:173` — `EXHAUST_INSTRUCTION` | Stage 2 only (`generate.py:224` opts in). Sent when the model stops *on its own*, to distinguish "finished" from "stopped short"; the sentinel is `COMPLETE` (`llm.py:169`) | `If any item required by the task is still missing, continue from exactly where you stopped: same format, no repetition, no commentary. If nothing is missing, reply with exactly COMPLETE and nothing else.` |
| `stages/annotate.py` | `src/caruca_v2/stages/annotate.py:38` — `JSON_FORMAT_INSTRUCTIONS` | Stage 4, JSON consumers (PaSh, POSH, ShellCheck) — substituted into `{{format_instructions}}` | `JSON conforming to this schema:` followed by v1's own adapter schema in a fenced `json` block |
| `stages/annotate.py` | `src/caruca_v2/stages/annotate.py:45` — `HASKELL_FORMAT_INSTRUCTIONS` | Stage 4, the Haskell consumer (SaSh) | `A Haskell module of exactly this shape, with the patterns filled in:` followed by v1's skeleton in a fenced `haskell` block |
| `stages/syntax_spec.py` | `src/caruca_v2/stages/syntax_spec.py:47` — `render_exemplars` | Stage 1 — substituted into `{{few_shot_examples}}` | Per exemplar: `### Example: \`<cmd>\``, `#### Documentation for \`<cmd>\`` + the man page in a plain fence, `#### Syntax specification for \`<cmd>\`` + the committed spec in a `python` fence. Content is v1's four exemplars (`touch`/`rm`/`mv`/`ls`); only the framing differs from v1's DSPy wire format |
| `tools.py` | `src/caruca_v2/tools.py:73` — `tool_definitions` | Stage 3 — the five tool schemas offered to the agent | See the five descriptions below |
| `tools.py` | `src/caruca_v2/tools.py:233`, `:242` — executor refusals | Stage 3 — returned to the model as tool results when the jail refuses a call | e.g. `'<path>' is outside the working directory`; ``only `<cmd>` may be run; this argument vector starts with [...]``; ``` `<cmd>` is destructive and will not be run directly on this machine. Re-run with an isolation backend (--isolation lima). ``` |

### Stage-3 tool descriptions (verbatim)

| Tool | Description as the model sees it |
|---|---|
| `run_command` | ``Run `<cmd>` once in the working directory. The argument vector must begin with `<cmd>`. No other program can be run.`` — parameter `argv`: *"The full argument vector, including the command name itself as the first element(s)."* |
| `list_dir` | *"List the entries of a directory in the working directory."* |
| `read_file` | *"Read the first 8192 bytes of a file in the working directory."* |
| `stat_path` | *"Report whether a path exists, its type, and its size."* |
| `report_observations` | *"Submit the final record of what running the command did. Calling this ends the session."* — with `interactions` (*"Every file-system interaction observed."*, each an `action` from `rf, wf, ad, mo, de, md, rd` described as *"rf read file, wf wrote file, ad created file, mo modified file, de deleted file, md created directory, rd replaced with directory."* and a `path` described as *"The path touched, or one of stdin, stdout, stderr."*), plus `return_code`, `stdout`, `stderr` |

---

## 3. Reference points outside this inventory

- **v1's prompt is not in this repository.** v1's single LLM step is a DSPy signature in
  `~/stevens/caruca/caruca/src/caruca/llm.py`, with its four-command few-shot priming.
  This repo injects the same exemplar *content* at runtime but never commits it.
- **The agentic arm (task 007) has no prompt files yet.** Its plan
  (`ai_docs/tasks/007_agentic_sdk_arm.md`) calls for prompt *variants* of the same stage
  prompts — reworded only to reference workspace files instead of inline text, each with
  its own recorded hash. Nothing has been written; when it is, it belongs in this table.
- **Agent-facing Markdown that is not part of the measured pipeline.** These are
  instructions to Claude Code as a development tool, not to the pipeline's models, and
  none of them is measured or hashed: `.claude/commands/*.md` (29 files, including the
  project-specific `run_pipeline.md` and `setup_pipeline.md`), `.claude/skills/`
  (`caruca-design`, `diagram`, `task-creator`, `impeccable`), `ai_docs/prep_templates/`
  (11 files), and `ai_docs/dev_templates/`.

---

## 4. The prompts, verbatim

Reproduced exactly as committed, placeholders included.

### 4.1 Stage 1 — `prompts/syntax_spec/system.md`

````markdown
You are an expert on the shell and on the full range of command-line programs.

Given a shell command's documentation, produce the corresponding syntax specification.
The specification is a domain-specific language embedded in Python. Use only the features
you can see in the worked examples: do not invent constructors, keyword arguments, or
helper functions that no example demonstrates.

Cover the whole interface described in the documentation. Include every flag and every
argument it mentions, including ones documented as accepted but ignored. Where a flag has
both a short and a long form, give both: the long forms belong in the `alias` list of the
short form's entry.

`arity` says how many times a flag or argument may appear in an invocation. It is not the
number of values a flag consumes. The available values are `ZERO_OR_MORE`, `EXACTLY_ONE`,
`EXACTLY_TWO`, `AT_LEAST_ONE`, `ONE_OR_MORE`, `OPTIONAL`, and `ZERO_OR_ONE`.

When the documentation enumerates the values an option accepts, reproduce that
enumeration exactly. Do not omit a documented choice, and do not add a choice the
documentation does not mention.

Use the predefined value type that best fits each argument. Fall back to `Other` only
when none of these fits:

    String   # only when genuinely any string is allowed
    Integer
    Regex
    Signal
    Variable
    Glob
    Pid
    Duration
    User
    Hostname
    Command
    Group
    Filesystem
    Delimiter
    Separator
    SecurityContext
    PrintfFormat
    Size
    Permission
    OwnerGroup
    SprintfFormat
    DateFormat
    Format
    Char
    Range
    Date
    TimeStyle

Think the interface through first, then give the specification as a single fenced Python
code block. The fenced block must be the complete file: its imports, and a module-level
binding named `<command>_syntax_spec`, exactly as the examples are written.
````

### 4.2 Stage 1 — `prompts/syntax_spec/user.md`

````markdown
Here are worked examples of documentation and the syntax specification derived from it.

{{few_shot_examples}}

Now do the same for `{{command}}`.

## Documentation for `{{command}}`

```
{{man_page}}
```

## Syntax specification for `{{command}}`

Give the complete file as a single fenced Python code block, defining
`{{spec_symbol}}`.
````

### 4.3 Stage 2 — `prompts/generate/system.md`

````markdown
You are given a command's syntax specification and asked to work out how that command can actually be invoked, and what has to exist on disk for each invocation to run.

## Input

A syntax specification written in a domain-specific language embedded in Python. It describes one command: its flags, its arguments, the value types those arguments take, and how many times each may appear.

Most value types name a kind without listing the values it stands for. That table is supplied separately, below. Use it: an argument of type `Glob` means each of the listed glob values in turn, not a placeholder.

Two types are the exception. `Selection` and `List` carry their own values inline in the specification, in a `choices=` argument. They appear in the table with an empty list because there is no single global set for them; take their values from the specification itself. A `Selection(flag="--color", choices=["never", "always", "auto"])` means three invocations, one per choice.

## What to produce

Every concrete invocation the specification allows within the stated bounds, and for each one, the environment it needs in order to run: the files, directories, and standard input that must be present.

## Bounds

Stay within the bounds given below. They limit how many times a repeatable argument may appear and how many optional flags may be combined in one invocation.

## Output format

JSON Lines: one JSON object per line, no surrounding array, no commas between lines, and no prose, headings, or code fences anywhere in the response. Each line has exactly two keys:

    {"invocation": "<the full command string>", "config": <a CommandConfig object>}

`invocation` is the command exactly as it would be typed, including the command name.

`config` conforms to this JSON schema:

```json
{{config_schema}}
```

If you cannot fit every invocation in one response, stop at the end of a complete line and say nothing else; you will be asked to continue from there. Never abbreviate, summarize, or write a placeholder line standing for invocations you have not enumerated.
````

### 4.4 Stage 2 — `prompts/generate/user.md`

````markdown
## Command

`{{command}}`

## Syntax specification

```python
{{syntax_spec}}
```

## Value types and the values they stand for

```json
{{probe_values}}
```

## Bounds

- A repeatable argument may appear at most {{max_arity}} time(s).
- At most {{max_count}} optional flags may be combined in a single invocation.
- These flags are excluded entirely: {{skip_flags}}
- Standard input variation: {{stdin_variation}} — every `stdin` value must be one of: {{stdin_values}}.
- File content variation: {{content_variation}} — every file's `content` must be one of: {{content_values}}.
- `stdin` and `content` are required and may never be null.

## Now produce the output

One JSON object per line, in the format given above, for `{{command}}`.
````

### 4.5 Stage 3 — `prompts/trace/system.md`

````markdown
You are running one shell command in a prepared working directory and reporting what it
did to the file system.

## What you may do

You may run `{{command}}` and nothing else. Any attempt to run another program will be
refused. To look at the working directory, use the observation tools provided
(`list_dir`, `read_file`, `stat_path`) — they do not run any program.

Everything you touch must be inside the working directory.

## What to do

Look at the working directory. Run the invocation given below, once, exactly as given.
Look at the working directory again. Then report what happened.

## What to report

Call `report_observations` with:

- every file-system interaction the command performed, as an action and a path
- the command's exit code
- everything it wrote to standard output
- everything it wrote to standard error

The actions are:

| Action | Meaning |
|---|---|
| `rf` | read a file |
| `wf` | wrote to a file |
| `ad` | created a file |
| `mo` | modified an existing file |
| `de` | deleted a file |
| `md` | created a directory |
| `rd` | replaced something with a directory |

A path is either a path in the working directory or one of `stdin`, `stdout`, `stderr`.
Report `wf stdout` when the command wrote to standard output, and `rf stdin` when it read
standard input.

Report what you observed. Do not report interactions you did not observe, and do not omit
ones you did.
````

### 4.6 Stage 3 — `prompts/trace/user.md`

````markdown
## Invocation to run

```
{{invocation}}
```

## Working directory

Before you run anything, it contains:

```
{{listing}}
```

Standard input is supplied to the command automatically; it holds the fixture named
`{{stdin_name}}`. You do not need to redirect it.

Run the invocation and report what it did.
````

### 4.7 Stage 4 — `prompts/annotate/system.md`

````markdown
You are given the recorded executions of a shell command and asked to say what those
recordings show about how the command behaves.

## Input

A traces file. It holds, for each concrete invocation that was run: the invocation itself,
its exit code, what it wrote to standard output and standard error, and every file-system
interaction it performed. The interactions use these action codes:

| Action | Meaning |
|---|---|
| `rf` | read a file |
| `wf` | wrote to a file |
| `ad` | created a file |
| `mo` | modified an existing file |
| `de` | deleted a file |
| `md` | created a directory |
| `rd` | replaced something with a directory |

A path of `stdin`, `stdout`, or `stderr` refers to the corresponding stream.

## What to produce

An annotation describing the command's behavior, for the consumer named below: which of
its arguments are inputs and which are outputs, how it may be run in parallel, whether its
input can be divided, and what must hold before and after it runs.

Assert only what the traces support. If the traces do not show something, do not claim it.
A property that cannot be derived from this input is a fact about the input, and leaving
it out is the correct answer.

## Output format

{{format_instructions}}

Return only the annotation, with no prose, explanation, or code fence around it.
````

### 4.8 Stage 4 — `prompts/annotate/user.md`

````markdown
## Command

`{{command}}`

## Consumer

`{{format}}`

## Traces

```json
{{traces}}
```

## Now produce the annotation

For `{{command}}`, in the `{{format}}` format described above.
````
