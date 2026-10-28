<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!-- caruca_v2 analysis document. Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
     Licensed under the PolyForm Noncommercial License 1.0.0
     https://polyformproject.org/licenses/noncommercial/1.0.0
     Noncommercial use only. Commercial use is prohibited. -->
<!-- ATTRIBUTION-NOTICE:END -->

# Status Report, 13 October 2026 — Where v2 Stands Against v1, and What Closes It

> **Written for:** Tiran, as the coordinator's report across every Caruca session running on
> 13 October 2026. Not an advisor handout; the 22 September report is the last of those.
> **Question answered:** can Caruca v2 run the same four pipeline steps v1 runs, with identical
> or better results — where does it fall short — is the console that runs both sides finished —
> and what is left to bring the work to a close.
> **Direction received the same day, which shapes the "what closes it" section:** PaSh is a
> consumer of Caruca's output, not the objective. The goal is a strong, repeatable, reproducible
> description of how a command is called and what it does, that PaSh and the paper's other tools
> can read. The immediate job is to make the pipeline run properly end to end and diagnose every
> problem in executing it. And v1's source is never modified: wrapper fixes only, v1 problems are
> recorded as findings, improvements are made in v2 and written up as increments.
> **Evidence:** everything marked *verified today* was run or read on 13 October 2026 by the
> coordinating session; everything else cites the document it comes from.

---

## 1. The short answer

**v2 runs all four steps, but it does not yet reproduce v1 at three of them, and the console
cannot yet start one of v1's four steps.** Measured on nine commands in September, at the same
bound on both sides, with the same scoring instrument:

| step | what it does | does v2 match v1? | the single cause, where it is known |
|---|---|---|---|
| 1 · syntax description | man page → the flags and the types of their values | **Yes.** Every flag v1 finds, v2 finds; v1 is marginally better at typing on two commands | v2's prompt is a paraphrase; copying v1's exact prompt (task 009) is expected to close the typing gap |
| 2 · test invocations and their file setups | description → the command lines to run, and the files each one needs | **Half.** The command lines are nearly right (88% of v1's found); the file setups are mostly wrong (only 21% agree) | v2 was given v1's *documented* rule for the flag limit, not the rule v1's code enforces; and v1's own schema never says what its setup types mean. Both are repairs to what v2 is asked, not tuning |
| 3 · running and tracing | run each command line in a sandbox and record what it touched | **No.** 78% of v2's runs ended without handing back a report; where one came back, it recovered 61% of what v1 recorded | the model answers in prose instead of calling the reporting tool. Fixing it means forcing the tool call, which is a change to the method and needs your decision |
| 4 · consumer description | traces → the specification a tool like PaSh reads | **Different, and capped.** On the strict instrument v2 agrees with the hand-written answer more often than v1 (32% vs 17%); under the paper's own looser rule, 88% vs 66%. But v2 cannot read the two largest trace files at all | the traces for `rm` and `tee` exceed the model's input limit. After v1's own relevance filter they fit |

**Repeatability — the property you named as the goal — is measured, and v2 does not have it
yet.** At temperature 0, with a fixed seed, v2 gave different answers across three identical
runs on at least one command at three of the four steps (`tac` at step 1, `pwd` at step 3,
`tail` at step 4, where it aligned 14, 12 and 2 cases). v1's own LLM step has the same exposure,
but the paper ran it once and never measured it. This is the clearest thing v2's evaluation adds,
and it is also an unsolved property of v2.

**The console runs v1 faithfully, which is now verified, but it is not finished.** Three of
v1's four steps and all four of v2's can be started from it. v1's step 4 cannot, the metering
of v1's one model call described in the design does not exist in the code, and the campaign
screen (its last phase) is unstarted.

---

## 2. Each step in more detail

The figures are from `v1_v2_parity_study.md` (version 1.1) and the diagnosis in task 011,
section 3. Nine commands: `cat pwd rm sha256sum tac tail tee uniq wc`. Model `openai/gpt-4o`,
temperature 0, seed 42, three samples per command. Bound of one optional element per command
line on both sides.

### Step 1 — syntax description: matches

Both systems found every flag on every command; neither invented one. v1 typed values better on
`tail` (11 of 13 right against v2's 10) and `tac` (5 of 5 against 4 of 5 in one of three runs).
Task 009 diagnosed both: v2 drops `tail -f` (the short spelling), which the scorer did not count
as missing because it matches on any shared spelling; and v2 types `tac -s` as `String`, a type
that did not exist in the prompt v1's committed specifications came from. **Nothing has been
changed yet.** Task 009 is written; no code.

### Step 2 — invocations and file setups: the command lines match, the setups do not

v2 produced 414 command lines v1 did not. 403 of them (97%) pair a flag with an optional file
name — `cat -n relpath_1` — which v1 never does at this bound, because v1's code counts the
optional file name as one of the "optional flags" even though its help text says flags only.
v2 followed the instruction it was given. Task 011 files this as a request repair: state the
rule v1 actually enforces, citing the line of v1 code that enforces it.

The file setups disagree with v1's on 79% of matched command lines. About half of that is how
the setup is written down, not which files would exist (v1 stores an empty placeholder where v2
stores nothing; v2 adds a field v1's loader ignores) — a scorer fix. The other half is real:
v2 marks a path as "must already exist" where v1 would create a file, a directory, or a missing
path, because v1's schema names the type and never says what it does. And v1 builds five
variants of every path where v2 is asked for one setup per command line; whether to ask v2 for
all five is a change to the method, for you to decide.

### Step 3 — running and tracing: does not reproduce

135 tracing sessions; 105 ended in prose without calling the reporting tool. The tool is
registered and the prompt asks for it by name. Where a session did report, recovery of v1's
recorded filesystem interactions was 61% on the state-changing tier. v2 traced v1's own command
lines, so a step-2 error is not counted twice. Two further limits on these figures: the campaign
capped each command at five configurations, and (confound 8, 6 October) 45 executions covered
only 12 distinct command lines, with six of nine commands testing no flag at all.

The one fix with a chance of working — requiring the tool call — is a method change (task 011
kind D). It is the single largest blocker to the pipeline running end to end, and it is a
decision, not a bug fix.

### Step 4 — consumer description: diverges, and hits a size ceiling

v2 agrees with the hand-written PaSh answers more often than v1 does on the same seven commands,
on both instruments. But 17 of v2's 25 strict agreements come from `tail` alone; v2's case counts
swing widely; and v2 classes `pwd` as safe to split where the paper itself names it as the
example of a side-effecting command. v2 cannot process `rm` (about 211k tokens) or `tee` (149k)
against a 128k window; after v1's own relevance filter they shrink to about 78k and 72k. Whether
feeding v2 the filtered view counts as matching v1 depends on whether v1's own annotator reads
the filtered or the raw traces — task 011's open check 2, unresolved.

Two facts found by other sessions since, both bearing on this step: v1 merges the answers from
its five setups by keeping the *most* parallel-friendly one, after discarding failed runs
(`annotator/annotator.py:121-124`), and v2's prompt states neither rule; and v1 never emits
`stateless` at the default trace mode, only under split-input tracing (`run.sh`'s mode).

### What has never been run

Every v2 step was measured on **v1's input to that step** (v1's committed specification into
step 2, v1's configurations into step 3, v1's traces into step 4). That is deliberate — it stops
an upstream error being counted twice — but it means **a chain where each v2 step feeds the
next has not been run as a measured campaign for any command.** "v2 can run the same steps"
is true step by step; "v2 can run the pipeline" has not been demonstrated. Task 013's W4(3)
is the first plan to do it.

---

## 3. The console — the wrapper that runs both sides

### What works, verified today

- Server starts with `npm --prefix console run dev` (or `cd console && npm run dev`), serves
  `127.0.0.1:4317` only. 216 console tests pass; the TypeScript check is clean. v2's own suite:
  292 tests pass.
- **v1's trace of `cat`, started from the Live page, runs in the Lima VM and matches the parity
  study's v1 trace exactly**: 35 of 35 configurations paired, every projected filesystem
  interaction identical (precision and recall 1.000 on both tiers, by the same comparison the
  parity study used). This was an unverified acceptance item in task 010; it is verified now.
- **v1's 36 working files are untouched** by a console run (sha256 identical before and after).
- From the page: v1's `generate`, `syntax-spec --fetch`, `trace` (both at the study's bound and
  at v1's defaults); v2's four steps (each behind a confirmation that shows the estimate and
  refuses to start if it has moved); `score --self-test`; `metrics rebuild`. Stop, reattach
  after reload, and two runs at once were verified in September.
- Replay, Inspect, Compare and Findings screens are built (phases 1–3), with eleven findings
  backfilled and a re-check that recomputes each figure with today's scorer.

### What does not work, found in the code today and confirmed by the Console session

1. **v1's step 4 cannot be started.** The Live page has no annotate button for v1. And the
   server's branch for it could not work if one existed: it looks for the trace file inside the
   run folder it has just created, empty, and there is no option to name an earlier trace run.
   So the one v1 step that must run inside the VM (it cannot run on macOS at all) is the one
   the console cannot reach.
2. **The metering of v1's model call does not exist.** Task 010's decision 8 — route v1's
   single LLM call through OpenRouter so both sides take the same route and v1's cost is
   recorded for the first time — is described on screen and in three source comments, but no
   forwarder is in the code, the process environment is passed through unchanged, and nothing
   sets `OPENAI_BASE_URL`. All five live v1 step-1 records have null tokens and null cost. Two
   failed for want of a key, two were stopped while DSPy backed off, one succeeded with a valid
   grammar (so credentials were in that shell), and none was metered.
3. **The console's default for v2's step 3 traces macOS's `cat`, while v1's row beside it
   traces GNU's in the VM.** A side-by-side at the default compares two operating systems'
   `cat`. The September campaigns set the VM explicitly, so the published figures are not
   affected; the default invites the mistake.
4. The Pipeline page still says "Nothing here executes anything — live runs are the next piece
   of work."
5. **Phase 6 (campaigns and tools) is unstarted**: no `sweep`, no `report`, no `report
   --rescore`, no scoring of a real specification, and v1's `oracle` is not wired. Running a
   campaign still means the command line.

All five are recorded in task 010's progress section (13 October entry).

---

## 4. The sessions, and what is sitting uncommitted

Four Caruca sessions were running. All reported; none started new work or committed on account
of the status request.

| session | doing | state |
|---|---|---|
| caruca-v2-28 | Task 013 (ready v2 for downstream tools, PaSh first) and the reflections on the NSF proposal reviews | Both written; no code; four new files |
| Caruca Console | Task 010's author; re-ran the suites, then confirmed the three defects above | Idle; recording the corrected picture in memory |
| pash-downstream-study | Task 012 Phase 0: PaSh VM built, format question settled (modern PaSh reads Python classes, not JSON), overhead measured at 0.17 s | In plan mode on a task it has numbered 014 (VM provisioning + benchmark); waiting on you |
| caruca-v2-03 (this one) | Coordinating | — |

**The working tree has 25+ uncommitted paths from at least three sessions**, on `main`, which
is level with `origin/main`. The last code commit was 5 October. Nobody should commit until you
decide how to bundle them; the memory index (`memory/MEMORY.md`) alone has been edited by three
sessions today.

**Two collisions to settle:**
- **Task numbering.** caruca-v2-28 created `013_v2_downstream_readiness.md` today;
  pash-downstream-study had planned a 013 and has provisionally renumbered to 014.
- **The Caruca-to-PaSh adapter has three claimants**: task 012 Phase 1 specifies it, task 013
  W2 sequences it, and the PaSh session's plan would build it. It needs one owner.

**One thing found in v1's checkout:** `caruca/save/ls.json` shows as modified (329 lines
removed; file time 3 September, the day the Lima VM was set up). No run today touched it. Under
the no-modification rule this should be restored with `git checkout -- save/ls.json` in v1's
tree — your call, since it is v1's tree.

---

## 5. Decisions only you can make

| # | decision | why it is yours | recommendation |
|---|---|---|---|
| 1 | Require the reporting tool call in step 3 (task 011, 3a) | It changes the method, so it runs as a *new arm* beside the unchanged one, both reported | **Yes.** Without it the pipeline does not run end to end; the unchanged arm stays as the honest control |
| 2 | Ask step 2 for all five file-setup variants v1 builds (task 011, 2e) | Same: a method change | Yes, as a new arm; otherwise setup agreement can never be compared |
| 3 | Feed step 4 the relevance-filtered traces (task 011, 4a) | Only if v1's own annotator reads the raw traces is this a method change; open check 2 decides | Resolve the check first (free, read v1's code); then it is likely a fidelity alignment, no decision needed |
| 4 | Make v1's exact prompt the default for step 1 (task 009) | A recorded scope decision, cleared in principle on 22 September | Yes |
| 5 | Who owns the PaSh adapter, and does the PaSh session's 014 fold into 013 | Three documents claim it | One owner: whichever task builds the first downstream run; the others reference it |
| 6 | Spend: task 011 phases 3 and 6 (rerun the nine at three samples, all four steps; step-3 reruns) | About $10 and under $5 at September's rates; $56.50 of the approved $60 ceiling remains | Approve after the free code changes land, not before |
| 7 | Restore `save/ls.json` in v1's checkout | It is v1's tree | Restore it, and record why |
| 8 | How to commit the 25+ uncommitted paths | Three sessions' work interleaved | One commit per session's work, in this order: memory and analysis docs; task 013 and reflections; PaSh VM doc |

---

## 6. What closes it — in order

Everything in A and B is free (no model calls) and is code or documents only. Nothing touches
v1's source.

**A. Make the console able to run every step of both sides (task 010).**
1. A v1 annotate button, and an "input run" picker that names the trace run to annotate —
   shared with v2's step 4, which also takes v1's traces.
2. The metering forwarder for v1's one model call, or — simpler and honest — record the two
   environment-variable *names* and read the tokens and cost from the provider's response via
   a local listener. Until it exists, take the on-screen claim down.
3. Default v2's step 3 to the VM whenever v1's row runs there; fix the stale Pipeline text.
4. Phase 6: `sweep` and `report --rescore` from the page, so a campaign is one click and every
   figure is recomputed from stored results (task 011's guardrail 4).

**B. Apply the free repairs and alignments (tasks 009 and 011, kinds A–C).**
1. Step 1: v1's verbatim prompt, one message, v1's request settings; count a missing spelling
   as missing.
2. Step 2: state the limit rule v1 enforces, citing `ir/syntax.py`; describe what each setup
   type does, derived from v1's `prepare_env` code; score setups after loading both through
   v1's own model; merge alias spellings.
3. Step 4: resolve open check 2; feed the filtered traces if it is an alignment.
4. Add the recorded cached-token count to telemetry, so cost becomes reproducible or its
   variation is explained.

**C. Your decisions 1–4 above**, then run the two new arms.

**D. Paid reruns on the nine (about $10), with predictions written first**, then a
confirmation set of commands outside the nine, chosen before any results are seen.

**E. The first chained run: v2's own step-1 description through all four steps, for one small
command, inside the VM.** This is the moment "v2 can run the pipeline" becomes a demonstrated
claim rather than a step-by-step one.

**F. Only then, downstream consumers**: PaSh first because its VM exists (tasks 012/013), then
ShellCheck, which tests the syntax half PaSh does not. Each is a test that the output is
consumable, not an optimisation target.

The documents that record each step as it lands: tasks 009, 010, 011 and 013; the parity study
for re-published figures; `findings/` for each conclusion.
