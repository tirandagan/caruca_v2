---
name: project_naive_claude_code_arm
description: Third, simplest arm created 2026-10-13 — a fresh Claude Code CLI session gets only a problem statement, two format docs and four verbatim v1 samples (tee, bc, grep, rm); folder `naive_llm_caruca` (formerly "naive_llm_caruca") at repo root; must run from a copy outside any checkout
metadata:
  type: project
---

**The arm.** On 2026-10-13 Tiran asked for a deliberately naive experiment that is neither v2 nor a
replication of v1's pipeline: hand a fresh Claude Code CLI session only a description of the objective
(produce the two files v1 produces per command, `<cmd>.py` syntax description and `<cmd>.json` PaSh
annotation, for downstream consumers such as PaSh), a plain-language description of each file's format,
and samples of finished output. No method hints, no guardrails, no mention of how v1 works. The research
question is how an unguided session solves it (does it read docs, run the binary, isolate it, trace it?).

**Where.** Repo-root folder `naive_llm_caruca/` (name chosen by Tiran, spaces included):
`PROMPT_v1.md` and `PROMPT_v2.md` (each with a `{{COMMAND}}` placeholder), `formats/`, `samples/`, `output/`, and an operator
`README.md` the session must not see. Design record: `ai_docs/tasks/016_naive_claude_code_arm.md`.

**Decisions (Tiran, 2026-10-13).**
- Samples are **tee, uniq, grep and rm** — so those four **cannot be test commands** for this arm.
  (Originally tee, bc, grep, rm; `bc` dropped the same day because PaSh has no annotation for it.)
- **Review feedback applied 2026-10-13** (from Prof. Michael Greenberg, inline comments on Discord, relayed by Tiran; summarised in the README section "Michael's feedback and what changed"): the behaviour
  annotation is PaSh's current Python form — parser table `<cmd>.json` + `InputOutputInfoGenerator<Cmd>.py`
  + `ParallelizabilityInfoGenerator<Cmd>.py`, as in github.com/binpash/annotations (`pash_annotations`
  0.2.4, MIT, installed in the pash VM; samples copied from there) — not v1's JSON; the prompt names
  `{{PATH}}` and `{{MANPAGE_PATH}}`; uses "argument syntax (options, option argument types, operand
  types)"; closes with "generate a correct spec without my intervention… test the binary against the
  spec". The syntax deliverable stays v1's Python DSL.
- The session runs from a copy placed outside any checkout (e.g. `~/naive-arm` in the Lima VM) because
  Claude Code auto-loads `CLAUDE.md` from the cwd and every parent, and caruca_v2's CLAUDE.md describes
  v1's whole pipeline.
- Headless runs use `claude -p ... --output-format stream-json --verbose`; verified against Claude Code
  2.1.293 on the Mac that stream-json requires `--verbose` in print mode.

**Prompt versions (2026-10-13).** Tiran wants graded variations. v1 = objective + formats + samples
only. v2 = v1 plus one guidance section: derive parameters and behaviour by executing the command
across its variations (not from memory); treat probing as an experiment (repeatability,
reproducibility); establish and report the OS and command version because core utilities differ
across Unix flavours and versions. Later versions get the next number and a line in task 016's
revision log; each run records which version it used.

**Claude Code in the VM (2026-10-13).** Installed in Lima `caruca` with the native installer
(`curl -fsSL https://claude.ai/install.sh | bash`), version 2.1.296, at `~/.local/bin/claude` in the
guest home (on PATH via `.profile`, so use `bash -lc`). Tiran signed in on 2026-10-13 with the claude.ai account (Max
subscription; `claude auth status` confirms), so runs bill the subscription, not an API key. Package copy lives at `~/naive-arm` (guest home), written by
`naive_llm_caruca/sync_to_vm.sh`, README excluded. No CLAUDE.md exists above it. Residual
hazard: the Mac home (both checkouts) is mounted at `/Users/tirandagan` inside the VM.

**Golden image (2026-10-13).** Runs use a clone of Lima VM `naive-golden`, not the caruca VM: created
with `limactl create --name=naive-golden template:ubuntu-24.04 --mount-none --cpus 4 --memory 4 --disk 20`;
Claude Code 2.1.296 installed (native installer); package at `~/naive-arm` (guest home
`/home/tirandagan.guest`); no mounts, no `/Users` inside. Stock image already has `strace` and
`unshare`; `kernel.apparmor_restrict_unprivileged_userns=1` left as stock. Reset = `limactl clone
naive-golden <run>` then `limactl delete -f <run>`; `limactl snapshot` is **unimplemented on vz**
(verified) and qemu is not installed. `sync_to_vm.sh [vm]` copies the package with `limactl copy`. Run flow (scripts in the folder,
tested 2026-10-13): `./new_run_vm.sh <name>` → `limactl shell <name>` (welcome lands in `~/naive-arm`)
→ `naive-run [-i] <cmd> [PROMPT_vN.md]` → `./collect_run.sh <name>` (results to the package's
`runs/<date>_<name>/`, clone deleted). `limactl clone` needs the source stopped;
`new_run_vm.sh` stops the golden image itself.
Sign-in to the golden image was pending when this was written; check `claude auth status` there.

**Command rules in `naive-run` (Tiran, 2026-10-13).** No hard blocks: any installed command runs. The
**core nine** of the parity study (`cat grep pwd rm tac tail tee uniq wc`, confirmed from
`ai_docs/archive_2026-09_rebuild/analysis/v1_v2_parity_study.md` and task 012) run without a question; anything else warns
and asks y/N; the four samples (tee uniq grep rm) print a note and run. Tiran first asked to be able
to enter grep (a sample) after the helper refused it, then asked for the confirmation on non-core
commands.

**Tool-call logging (2026-10-13).** No CLI flag logs tool calls for an interactive session. Verified:
Claude Code 2.1.29x writes every session to `~/.claude/projects/<cwd-slug>/<session-id>.jsonl`
(`assistant` records with `tool_use` blocks carrying name + full input; `user` records with
`tool_result`; timestamps). Headless `-p --output-format stream-json --verbose` has the same blocks
plus a final `result` event. `naive-run` copies the newest transcript to `runs/<tag>.transcript.jsonl`;
`collect_run.sh` copies `~/.claude/projects`; `tool_log.py` renders either file. `--debug-file` is an
internal debug log, not a tool log.

**Watch mode (2026-10-13).** Tiran wants to see progress on screen with tool names, inputs and
results (not thinking) and a complete action log; interactive `claude "<prompt>"` only prefills the
input box (his sed session sat until he typed something). So `naive-run` defaults to watch mode:
`claude -p … --output-format stream-json --verbose --permission-mode bypassPermissions | naive-watch.py`,
rendering live and writing `<tag>.jsonl` + `<tag>.actions.log`. In `-p` mode tools needing
permission are denied unless allowed, hence bypass in the throwaway VM (recorded in `<tag>.env`).

**Layout leak found by run 1 (2026-10-13).** Run 1 (sed, v1, interactive, clone `naive-run-grep`,
45 tool calls, ~8 min, all four files produced) read `PROMPT_v2.md` and `runs/sed_PROMPT_v1.env`
from its cwd, searched the filesystem for caruca/pash_annotations, and queried the GitHub API for
"caruca". Fix: prompts in `~/prompts`, logs in `~/runs`; `~/naive-arm` holds only formats/, samples/,
output/. Run 1 was collected and then **deleted by Tiran** on 2026-10-13 evening (leaky layout, old helper);
only the README's Observed summary survives. Tiran's call: all deliverables, scripts and collected
runs stay in the package folder; `runs/` is never copied into a VM because `sync_to_vm.sh` stages
only prompts, formats/, samples/.

**Per-run packaging (Tiran, 2026-10-13 evening).** Every `naive-run` invocation gets its own
`~/runs/<date>_<time>_<vm>_<cmd>_<version>/` with prompt.md, output/, stream.jsonl, stream.actions.log,
transcript_<session>.jsonl, run.env (incl. `run_number_in_this_clone`); output/ is emptied after each
run; `collect_run.sh <vm> [--keep]` copies each run folder into the package's `runs/` unchanged and
saves only sessions no run folder captured (`_other-sessions/`). The golden image's own session
history (an "update claude" session and the sign-in) was inherited by every clone and re-saved on
every collection, so on 2026-10-13 the image's `~/.claude/projects` was emptied and `new_run_vm.sh`
now empties it in each clone at creation; `_other-sessions` appears only for a bare `claude` run
in the clone. Tested 2026-10-13 with a stand-in `claude` (two runs in one
clone → two folders). Tiran also wants no accumulation of several runs in one folder.

**Run 2 (2026-10-13 19:05).** grep, v1, watch mode, clean layout, clone `naive-run-grep`: 327 s, 33
tool calls, tried `pip install pash-annotations` (no pip in the stock image; PyPI reachable), ran grep
with patterns in 12 calls, all four files produced; collected to the package's `runs/`; not scored.
grep is a sample command, so this run is a copying test as much as a solving test.

**Run 3 (2026-10-13 19:34).** grep, v1, watch mode, model **`claude-haiku-5-5`** (the golden image's
default; the README did not record the model before this), collected to
`runs/2026-10-13_193448_naive-run-grep_grep_PROMPT_v1/`; **analysed 2026-10-13** in its
`analysis/analysis.md` (+ two Excalidraw diagrams); not scored. Facts established from the log (all
read directly from `stream.jsonl` / `stream.actions.log`):
- 739 s, 73 turns, 72 tool calls (43 Bash, 9 Write, 15 Edit, 4 Read, 1 TaskStop), $0.96 list;
  output 123,918 tokens of which 82,852 thinking; cache reads 11.2M.
- **Claude Code 2.1.296's Bash tool defines a shell function `grep` that execs its bundled ugrep**
  (`grep --version` → "ugrep 7.8.4"); the session noticed at call 6 and used `/usr/bin/grep` by path.
  Any run whose test command is `grep` has this confound; `run.env`'s `binary=` path is the fix.
- **Leak: the public caruca_v2 repo is one GitHub search away.** The session searched
  `api.github.com/search/repositories?q=caruca`, found `tirandagan/caruca_v2`, listed its tree and
  read three `memory/*grep*` notes via raw.githubusercontent.com (calls 14–17); the four-syntax
  structure of its `grep.py` follows those notes. Decide: block network in clones, or record it per run.
- Manual page read only for its first 1500 bytes (version header); option list taken from `--help`.
  85 probe invocations in `/tmp/grep_probe` before the first write (call 28, 19:41:53); no isolation.
- Wrote 3 check scripts (syntax: 129 grep runs; PaSh: real parser/classes from the downloaded
  0.2.4 wheel, 42 invocations; behaviour: split-and-concatenate on a 400-line corpus). One finding
  (PaSh's parser leaves `--opt=value` tokens among operands) fed back into both generators.
- Output: `grep.py` **imports under v1's real `caruca.ir.syntax`** (4 syntaxes; `min=0`, `arity=`
  on Glob/Path accepted); parser table = sample + 30 entries (`-0..-9`, 20 `--color=WHEN`) − 2;
  classes rewritten. No file states the grep version. Report error: claims the sample lacked `-y`/`-u`
  (it has both).
Run 2 (19:05) is still unanalysed.

**Status.** Package built 2026-10-13; runs 1 to 3 done the same day (see above). **Task 017** (created
2026-10-13) is the comprehensive write-up of how the arm was built, for the advisors; deliverable
`ai_docs/docs/naive_claude_code_arm_how_it_was_built.md`, not started. Related: [[caruca_v2_baseline_scope]] (the naive
single-prompt control, task 001) and task 007 (agentic SDK arm) are the other two LLM arms.

**No web lookups + fixed model (Tiran, 2026-10-20).** Prompted by run 3 (grep), which used `curl` from
Bash (not the WebSearch tool) to search the GitHub API for "caruca", found this public repo and read
three memory notes. Tiran's call: the agent may not search or browse, but **programs that need the
network keep it** (pip/apt), so **the VM is not firewalled** (he rejected a firewall). Enforced by:
both prompts edited in place with a "What you may not use" section (wording avoids the withheld word
"documentation"); `vm/naive-run` passes `--disallowedTools WebSearch WebFetch RemoteTrigger
--strict-mcp-config` in both modes; a post-run audit writes every http(s) URL in Bash commands to
`bash_urls.txt` (the shell is covered only by the prompt). Model: Fable 5.1 medium, else Opus 5.5 high,
chosen by a trial call before the run; no `--fallback-model` (effort is per session, so a mid-run switch
would run Opus at medium). Observed 2026-10-20:
- a trial `claude -p` with the full default system prompt cost **$3.02 list** on the Mac (151K cached
  tokens from plugins and skills), even with `--tools ""`; with `--system-prompt` replaced it cost **$0.02**.
- a refused model gives exit 1, `is_error: true`, `terminal_reason: api_error`.
- in a fresh clone of `naive-golden` (Claude Code 2.1.296), the account **can** use `claude-fable-5-1`;
  with the flags, the init event had no WebSearch, WebFetch or RemoteTrigger and `mcp_servers: []`.
  Run 3's init had listed WebSearch, WebFetch and a supabase plugin MCP server.
- run 3 ran on `claude-haiku-5-5` (the account default; no model was set).

**Sign-in lost in clones (observed 2026-10-20).** The check clone `naive-run-check` worked at 11:20
(signed in, inherited from `naive-golden`). The next clone, made at 11:23, reported `loggedIn: false`, and its
run failed at once with "OAuth session expired and could not be refreshed" (0 turns; clone deleted).
*Not established:* the cause. The likely one is that the check clone's token refresh rotated the
refresh token every clone inherits from the golden image. Candidate fix: `claude setup-token`
(long-lived token; it exists in 2.1.293's help). Not tested in the VM. Since then `naive-run` stops (exit 4)
if `claude auth status` is not logged in, or if the trial call's error mentions sign-in, instead of
mislabelling it as a Fable refusal and falling back to Opus.

**Run 4 (2026-10-20, collected).** Tiran signed in to `naive-golden` again with `/login` at about 11:28
(not `setup-token`), and the next clone worked. Run 4 = grep, PROMPT_v1, watch mode, Fable 5.1 medium,
no web tools: 322 s, 10 Bash calls, $2.54 list, **0 URLs**, 72 direct binary runs before writing,
parser table has the sample's exact option set, classes tested only against stand-ins it wrote itself
(no PyPI attempt). Folder `naive_llm_caruca/runs/2026-10-20_112956_naive-run-grep-noweb_grep_PROMPT_v1/`;
README "Observed, run 4". Not scored. **Analysed 2026-10-20** (`analysis/analysis.md` in the run folder,
four diagrams incl. run 3 vs run 4 and v1's paper design vs the agent). Facts established there: call 2's
unqualified `grep --version` hit ugrep (same as run 3; recovered by call 4); the harness's only run ended
`TOTAL FAILURES: 1` yet the report says "Everything passed"; `grep.json` keeps the sample's `--color WHEN`
while `grep.py` says `=WHEN` (probe supports `=WHEN`); 3 of 4 files name GNU grep 3.11; the harness runs
the binary 154 times (counted by replaying it on the Mac with a counting stand-in binary); `grep.py`
imports under v1's real DSL (2 syntaxes, 46/48 option nodes). Diagram helper used for the four diagrams
(fills Excalidraw boilerplate only) lived in the session scratchpad, not the repo.
Whether a later clone will lose the sign-in again is not yet known.

**Run 5 (2026-10-20, collected): rm, the first destructive command.** PROMPT_v1, watch mode, Fable 5.1
medium, no web; sign-in in the clone worked again with no re-login (so the 11:23 sign-in loss has not
recurred across two later clones). 60 s, 5 Bash calls, $0.80 list, 0 URLs. Isolation was only
`cd $(mktemp -d)` with files it created, 27 `rm` runs with stdin from `/dev/null`; no namespace or
sandbox; nothing outside the scratch dir deleted except `output/__pycache__`. **No test of its own
files after writing** (only JSON load + py_compile). Parser table identical to the `rm` sample; syntax
file = sample + 6 `--interactive` values, zero-or-more operands, coreutils 9.4 header. Folder
`naive_llm_caruca/runs/2026-10-20_121932_naive-run-rm_rm_PROMPT_v1/`; README "Observed, run 5". Not
scored. **Analysed + PDF 2026-10-20.** Verified there: `samples/rm/rm.py` == v1 `syntax_specs/rm.py` (the
curated reference) byte for byte, and v1's `outputs/llm-dsl-generation/rm.py` matches it apart from
formatting (tuple vs list, trailing newline); v1's committed `caruca/save/rm.json` (2024-12-08) has 2
cases, both side-effectful, path as input and output. The paper's rm figure: 8,749,056 invocation
configurations (section 2.2). **Caveat found after the analysis:** `rm` is one of v1's own few-shot examples
(`llm.py:116`), so v1's model had rm's reference answer in its prompt, just as the agent had it in
`samples/`. Applied 2026-10-20: the run-5 analysis gained a plain-language "What this run
teaches" section (Tiran asked for the insights, not verbose or technical), the v1 claims and diagram now
carry the caveat, and the PDF was regenerated (17 pages). Runs 1 and 2 have no run folder any more (run 1
deleted by Tiran; run 2's folder is absent from `runs/`), so only runs 3-5 can be re-read from logs.

**Real-world weight of the binary-only syntax facts (measured 2026-10-20 on v1's corpus
`eval/user-scripts/invocations.txt`, 665,628 lines).** `rm`: 24,260 top-level lines; **0** use `--interactive`
in any form, and the only lines with no file operand are 2 × `rm --help`, so run 5's two binary-backed
corrections touch 0 of 24,260 real lines. The corpus file has **no top-level `grep` lines** (the paper's
section 7.3 names grep among covered commands; not explained). Among 1,833 `grep` commands embedded in other
lines (pipelines, `$(...)`), **63 (3.4%) use `-e`/`-f`** (strict count: `-e`/`-f`/`--regexp`/`--file`, or a
flag group ending in e/f), 51 of them with a file operand; 0 use `-y`, `-u`, any `--color`, or negative context.
So of the manual-vs-binary differences, only grep's `-e`/`-f` form shows up in real use. Embedded commands
are a biased sample; not a coverage rate.

**Run 6 (2026-10-20, collected, analysed + PDF): binwalk, first command outside the core utilities.**
Ubuntu package `binwalk 2.3.4+dfsg1-5` (Tiran added it to `naive-golden` with apt); the binary reports
v2.3.3, its manual says 2.3.2 (49 options vs `--help`'s 51; lacks `-0`, `-1`). Not a sample, not in v1's
120 commands: no v1 manual copy, reference grammar or committed annotation, so it cannot be scored. PROMPT_v1,
watch mode, Fable 5.1 medium, no web; 193 s, 18 Bash calls, $2.12 list, 0 URLs. **`/usr/bin/binwalk` is a
4-line Python script; the session read binwalk's installed source and in call 9 ran its module registry to
print the internal option table; syntax file + table follow that table 1:1.** 30 binary runs before writing
(one `mktemp` folder, guard joined by `;` so it fails open), 4 after; 16 of 51 options ever run (not `-D`,
`-r`, `-M`, `-0`, `-1`); main test compares the files with the same table (circular). Missed: `-D
type:ext:cmd` runs a command per match (verified in the clone afterwards); `-e`'s extraction folders cannot
be declared in PaSh's input/output class, so they are only in comments. The `-E -J` probe wrote
`~/.cache/matplotlib` outside the scratch folder. Folder
`naive_llm_caruca/runs/2026-10-20_133813_naive-run-binwalk_binwalk_PROMPT_v1/`; README "Observed, run 6".
Open questions it raised: whether installed source code is allowed (PROMPT_v1 bans only *online*
repositories), and choosing test commands by packaging (script vs compiled). See [[caruca-v1-value-generation]].
**2026-10-20: written up as section 2 of `naive_llm_caruca/white_paper_addendum_naive_llm.md` (version 0.2), PDF
regenerated; analysis index entry updated.** Run numbering agreed with the parallel session: binwalk = 6,
cut = 7 (13:52), convert = 8 (13:58), sort = 9 (16:03), by start time.

**Runs 7 (cut, 13:52) and 9 (sort, 16:03), 2026-10-20: collected, analysed + PDF** (folders
`naive_llm_caruca/runs/2026-10-20_135253_…cut…` and `…160340_…sort…`; README "Observed, run 7/9"; task 016
ledger). First non-sample core utilities. Launched with `script -qec "naive-run <cmd>" /dev/null` fed "y"
(non-core confirmation). Same setup as runs 4-6 (image already had binwalk). Run 7: 104 s, 17 calls (9
Bash, 8 Read), $1.25, 21 probes then a 45-run split-and-join test (v1's stateless idea, unprompted);
three syntaxes, one per selector; table = PaSh's own `cut` table minus `-M` (never seen). Run 9: 304 s, 23
calls, $2.46, 88 probes then ~960 test runs (spelling script ended `BAD = 8`, unreported); table = PaSh's
own `sort` table incl. access kinds, plus `-y`, `--check`. Both hit Claude Code's tool-output limit on a
batch read (34.5 / 31.2 KB → 2 KB preview) and fell back to the Read tool. Both tested classes only
against stand-ins. **Measured in PaSh's real code:** run 7's classes = PaSh's answers except `-z`; run 9's
parallelizability class returns nothing for ordinary sorts (round robin + custom merge fails PaSh's
assertion, swallowed) — rule absent from `formats/pash_annotation.md` (renamed `formats/annotation.md` 2026-10-27); candidate repair, not applied,
Tiran to decide. **Measured through v1's generator** (every distinct line run on coreutils 9.4): run 7's
grammar and v1's model output give 0 lines doing real work at max-count 4, v1's reference 360 (cause:
`=` on short options, copied from the uniq sample = v1's reference). v1's committed `save/sort.json` calls
all 6 cases `stateless` (false in general; cause not established). Details:
[[reference-pash-annotations-runtime]], [[caruca-v1-value-generation]]. Convert (run 8) was run and written up by
another session; see the run 8 paragraph below.

**Run 8 (convert, 13:58, 2026-10-20): collected, analysed + PDF** (folder
`naive_llm_caruca/runs/2026-10-20_135842_naive-run-convert_convert_PROMPT_v1/`; README "Observed, run 8";
task 016 ledger). ImageMagick 6.9.12-98 (`imagemagick 8:6.9.12.98+dfsg1-5.2build2`, already in the golden
image; recorded by hand in the run folder's `package_version.txt`). Not a sample, not a v1 few-shot example.
PROMPT_v1, Fable 5.1 medium, no web. 1,291 s session time but 2 h 14 min wall clock (Mac slept, see
[[reference-naive-run-playbook]]); 33 calls (31 Bash, ToolSearch + TaskStop to stop a hung background
call); **$6.04**; 0 URLs. Read all 4 samples + whole manual; diffed manual (248 names) vs `-help` (250);
tried 352 words from `libMagickWand` strings as names → 261 accepted (10 in neither manual nor `-help`;
manual's `-connected-component` rejected; `-view` takes a value, v1 has it as a flag — both checked in the
clone). ~3,700 binary runs before writing in plain `/tmp/cvt` (hang on `-distribute-cache`; `pkill -f`
matched its own command line, exit 144), ~3,100 after in its own harness; generator script wrote syntax
(426 nodes, 522 spellings, ZERO_OR_MORE inputs + EXACTLY_ONE output) and table (219 flags, 207 options).
Report's "All 522 spellings passed" false (509 run, 1 flagged). **Measured:** v1's reference and v1's model
output for convert both = the manual's 248 names exactly, no `+` forms; in PaSh's real code (copy in pash VM)
classes load, but option words after the first file are typed as input files; **through v1's generator at
max-count 1 only 4 of the agent's 2,422 distinct lines have input+output** (option lines get one file →
"no images defined"); reference 0, v1 model output 2,272/2,272. v1's committed `save/convert.json` empty
since 2024-12-04 (2024-11-28: "Found no successful runs. Defaulting to side-effectful");
`benchmarks/MILESTONES` lists convert unchecked; v1's `pash_syntax_specs/convert.py` = input, `-resize`,
output (3 positions: the syntax format can hold options between files, the samples never show it).
Stock clone image also has `nerdctl` 2.3.5 + rootless containerd (unused by every run so far).
**Run 8 in the addendum (2026-10-20):** written up as section 3, "A wide interface: `convert`", of
`naive_llm_caruca/white_paper_addendum_naive_llm.md` (version 0.3, PDF 17 pages); analysis index updated.
Suggestions there: widen the binary check to `-help`/library/listing commands; use positions for options
between files; test options singly before combining (the paper's own 7.4 remark as a schedule); record which
option orders a consumer annotation holds for. PaSh's own `img_convert.sh` benchmark uses options-first order
(`convert -resize 70% "$i" "$out"`), which the agent's annotation handles; PaSh 0.2.4 ships no `convert`
annotation; v1's hand-written one is `eval/pash-annotations/convert.json` (pure, args[1] → args[2]).
**2026-10-20: runs 7 and 9 written up as section 4 of `naive_llm_caruca/white_paper_addendum_naive_llm.md`
(version 0.4; convert is section 3, from the parallel session; PDF 23 pages, title "Naive LLM").** Facts
re-verified at source for it: v1's split test needs each half's output to keep its input's line order
(`tracer/data.py` 112–146), added 2025-12-21 (`c97306bb4`), after the committed `save/{cut,sort}.json`
(2024-12-07/08); the paper (section 6.3) defines stateless as split-run-concatenate equality and (6.1) puts
aggregator synthesis out of scope, while v1's code never emits `pure` (only S/N/E in `to_annotation`).
Two sessions editing the addendum at once produced two "section 3"s; merged by agreement.

**Run 10 and task 018 (2026-10-26).** Run 10 = `dirname` (57 s, $0.88, 5 tool calls), the first new run of
task 018 (`ai_docs/tasks/018_naive_vs_caruca_syntax_scoring.md`): four scores per syntax file (answer key,
real binary, real-world reach, generator use) for v1's reference, v1's shipped GPT-4o output and the agent;
tools in `naive_llm_caruca/scoring/`, results in `naive_llm_caruca/scoring/results/`. Pilot 3 of 5 scored
(cut, sort, dirname); dd and ls blocked on a golden-image sign-in; main phase (55 new runs) awaits Tiran.

**Syntax-file comparison, 2026-10-26.** The agent's `rm`/`cut`/`sort`/`convert` syntax files (runs
5/7/9/8) were compared with v1's reference and v1's model output, each difference checked on coreutils
9.4 / ImageMagick 6.9.12-98, and all three fed to v1's matcher, generator, ShellCheck adapter and
scorer: `naive_llm_caruca/syntax_files_vs_v1.md` (v0.1), scripts and results in
`naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/`. Not yet folded into the addendum
(another session had uncommitted addendum edits that day). See [[caruca-v1-matcher-behaviour]].

**Task 018 narrowed and scored (2026-10-27).** Tiran: score only `cut`, `sort`, `rm`, `binwalk`. Headline =
program-checked accuracy (facts right / all facts, 8 fact types in `naive_llm_caruca/scoring/facts.py`,
asked for via session caruca-v2-dd). Results: `cut` agent 68/76 (89%) vs reference 61/72 (85%) vs v1 GPT-4o
63/76 (83%); `sort` 181/230 (79%) vs 172/220 (78%) vs 157/204 (77%); `rm` 58/60 vs 59/60 vs 59/60;
`binwalk` agent 326/337 (97%). Generated lines doing real work: agent worst (`cut` 0/240 vs 15/29; `rm` 3/21
vs 26/32; `sort` 33/56 vs 41/56). One agent run each, so no verdicts. Write-up:
`naive_llm_caruca/observations.md`. Three checker repairs before keeping numbers are in task 018 §4.5.
