<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!--
 caruca_v2 execution console.
 Adaptations and additions copyright (c) 2026 Tiran Dagan.
 Licensed under the PolyForm Noncommercial License 1.0.0
 https://polyformproject.org/licenses/noncommercial/1.0.0
 Noncommercial use only. Commercial use is prohibited.
-->
<!-- ATTRIBUTION-NOTICE:END -->

# The execution console

A local web page that runs v1 and v2 side by side, each in a real terminal, and explains every
number it shows. Specified in `ai_docs/tasks/010_execution_console.md`.

**It runs on this Mac only and is never deployed.** v1 traces inside the Lima VM, v2 needs the
local v1 checkout and the API key, and run data embeds v1's man pages and specifications, which
must not reach a public location. The server listens on 127.0.0.1 only.

## State of the build

| phase | what it is | status |
|---|---|---|
| 0 | Seven questions answered before any code | **done** — see §9 of the task |
| 1 | The data layer: readers, event adapters, recordings, findings | **done** — `src/data/` |
| 2 | Replay and Inspect screens, and the visual design | **done** |
| 3 | Compare and Findings, and the backfill | **done** |
| 4 | The Pipeline builder and pre-flight, still without execution | **done** |
| 5 | Live runs: pseudo-terminals, recording, stop, reattach | **done** — 216 tests |
| 6 | Campaigns and tools | not started |

## Installing and running it

**You need:** this repo, Node 22.5 or newer (`node -v`), and the project's Python virtual
environment at `.venv/` — the console runs `caruca-v2` from there and never from your `PATH`.

```sh
cd console
npm install          # ~30 seconds; also fixes a file permission npm leaves broken (see below)
npm run dev          # then open http://127.0.0.1:4317
```

That is the whole thing. It binds to `127.0.0.1` only, so nothing on your network can reach it,
and the page makes no outside requests — the fonts and the logo are served from `public/`.

**To stop it:** Ctrl-C in that terminal. Nothing is left running.

Leave it running while you work; every page reads the run directories fresh on each request, so
a run that finishes while the page is open shows up when you reload.

| command | what it does |
|---|---|
| `npm run dev` | the console, on 127.0.0.1:4317 |
| `npm test` | the test suite, against the committed run directories |
| `npm run typecheck` | types only, no build |
| `npm run build` | a production build; you don't need it, since this is never deployed |
| `node scripts/record-sample.mjs` | re-record the terminal replay fixture from a free v1 command |

### If something goes wrong

- **Every page returns 500 with "Module not found".** Delete `.next/` and start again.
  `npm run build` and `npm run dev` share that folder, so running the build while the dev
  server is up leaves it in a state the dev server cannot use.
- **Port 4317 is in use.** An earlier console is still running:
  `pkill -f "next dev -H 127.0.0.1 -p 4317"`.
- **Compare says campaigns are missing.** `eval/campaigns/` is the one part of the run data
  that is still gitignored, so a fresh checkout has none. Everything else works without it.
- **`posix_spawnp failed` when a terminal starts.** `npm install` should have prevented this.
  It means npm blocked the step that makes `node-pty`'s helper executable; run
  `npm approve-scripts node-pty` then `node scripts/fix-node-pty-permissions.mjs`.

## The screens

| route | what it is |
|---|---|
| `/` | Runs. The way in, and where the three different run counts are stated side by side |
| `/runs/<run_id>` | Run. The terminal beside the events |
| `/runs/<run_id>/inspect` | Inspect. Prompts as sent, raw response, per-turn figures, sessions |
| `/compare` | Compare. One row per command, one column per stage, every figure with its denominator |
| `/compare/<stage>/<command>` | The items behind one number, from the generated drill-down |
| `/findings` | Findings. Each claim, its numbers, and a button that re-derives them |
| `/pipeline` | Pipeline. What a run would consist of, and what it would cost. Executes nothing |
| `/live` | Live. Start runs and watch them, v1 left and v2 right, in real terminals |

A recorded run replays in a real terminal emulator, at 0.5x to 8x, seekable. A run without a
recording — which is all 135 of them today — says so and shows its reconstructed command line,
rather than an empty black rectangle that reads as a run which produced no output.

**The page cannot type into a terminal.** No input handler is attached and `disableStdin` is
set, so there is no path from the browser into a process. That is a requirement, not an
oversight.

### Deleting runs

The Runs page lets you select runs and delete them — the directory, its files, and its rows in
`eval/metrics.db`. Three things are worth knowing before you use it:

- **It shows you what depends on them first.** A run can be cited by a scored campaign cell and
  by a written-up finding. Deleting it does not change those documents; it makes their numbers
  impossible to check again, and nothing complains until someone tries. The review step names
  every such dependency. You are warned, then allowed through.
- **It does not remove the evidence from git.** `eval/runs/` is committed, so deleted files
  remain in the repository's history. Recover with `git checkout -- eval/runs` followed by
  `caruca-v2 metrics rebuild`. Equally: this is not a way to make something go away.
- **Every deletion is logged** to `eval/deleted_runs.jsonl`, with what went, when, why, and what
  depended on it at the time — because in a research record an unexplained gap is worse than a
  documented removal.

The safe thing to bulk-delete is the empty directories: runs that died before recording
anything. They are listed separately and nothing can depend on them.

## The data layer

```
src/data/
  paths.ts         where everything lives; refuses to point v1 at its own outputs/
  schema.ts        the shapes on disk, mirrored from src/caruca_v2/telemetry.py
  runs.ts          v2 run directories; separates "died before recording" from "malformed"
  v1Runs.ts        v1 run records, which this console writes and v1 does not
  commandLine.ts   rebuilding a v2 run's command line from its manifest
  metricsDb.ts     eval/metrics.db, read-only, via Node's built-in sqlite
  campaigns.ts     ledgers and summaries (the one part of eval/ not committed)
  consistency.ts   spread per metric, not just the headline
  asciicast.ts     terminal recordings: read, and write as a run proceeds
  events.ts        one event format for replay and live
  findings.ts      one Markdown file per finding, with the re-check
  promptDrift.ts   has a run's prompt been edited since the run happened?
  compare.ts       the matrix: each stage's headline figure, its denominator, its verdict
  parityCampaigns.ts  which campaigns make up a comparison, and coping when they are absent
  parityDiff.ts    the per-command drill-down, read from what scripts/parity_diff.py wrote
  harness.ts       calling caruca-v2: report, rescore, score --self-test
  deleteRuns.ts    the only destructive operation, with its impact report and its log
  recheck.ts       re-deriving a recorded number with today's scorer
  options.ts       one option table, mirroring both CLIs; tested against their --help
  v1Invocations.ts v1's argument lists, in the forms the parity study used
  preflight.ts     counts, environment checks, cost estimates from measured runs
  pipelinePlan.ts  what a run would consist of, built without running anything

src/server/
  processes.ts     the registry: every running process, its terminal and its recording
  startRun.ts      building a run, and the confirmation a paid one needs first
server.ts          Next plus the WebSocket that carries a live terminal
```

### Running things

`/live` starts runs and shows them, v1 on the left and v2 on the right, each in a real
terminal. What to know:

- **The server owns every process, not the page.** Closing or reloading the tab leaves a run
  going; coming back reattaches and replays what you missed. That is why the console has a
  custom server rather than plain `next dev`: Next's route handlers cannot hold a WebSocket
  open.
- **Nothing that costs money starts without being asked for by name.** Every v2 stage calls a
  model, and so does a live v1 stage 1. The confirmation carries the estimate and what it is
  based on, and the run is refused if that figure has moved since it was shown.
- **The page cannot type into a terminal.** No input path exists, in either direction.
- **Stop reaches inside the VM.** For a Lima run the console kills the process in the guest as
  well, then checks and reports anything that survived rather than assuming.
- **Only four programs can be started**, checked on the resolved path: `caruca-v2`, v1's
  `caruca` from either virtualenv, and `limactl`.

Free things to try, which call no model: v1's `generate` (prints invocations, executes
nothing), `syntax-spec --fetch` (reads v1's committed specification), v1's `trace` (executes
under strace in the VM), and `caruca-v2 score --self-test`.

### The pipeline screen

`/pipeline` builds a run and shows what it would do. It executes nothing — live runs are the
next piece of work — but everything it shows is real:

- **Counts come from running v1's `generate` and counting the lines**, never from
  `--number`, which disagrees with actual emission on every command checked and crashes on
  fourteen. `generate` prints invocations and executes nothing, so counting `rm` is safe.
- **Cost estimates come from measured runs of the same stage and model**, with the observed
  range stated. Where nothing comparable has been measured it says so rather than guessing.
- **Every command line is shown in full and matches where the step would run.** A stage that
  must use the Lima VM shows the flags that put it there.
- **v1's `generate` is drawn as not part of v1's chain**, because v1's `trace` works out its
  own invocations. It is stage 3's preview and count.

Three tests keep this honest, and they run the real programs:

| test | what it prevents |
|---|---|
| `options.test.ts` | the option table drifting from either CLI, in either direction |
| `v1Invocations.test.ts` | v1 being run in a form the parity study did not use |
| `v1Invocations.test.ts` | v1 ever being pointed at its own `outputs/`, which git cannot restore |

### Re-checking a finding

Each finding on `/findings` has a button that re-derives its numbers. A campaign-level check
runs `caruca-v2 report --rescore`, which recomputes every score from the run artifacts with
today's scorer — tens of seconds, and read-only, so re-checking cannot alter the evidence it
is checking.

Two things the result always states:

- **The precision it compared at.** A number in a document is rounded: the study says 0.606, the
  scorer says 0.6062992125984252. Comparing those exactly would mark every written-down number
  as changed, so comparison happens at the precision the number was written to. A rate stored
  as `1.0` loses its decimals in YAML, so rates are compared to three places rather than as
  whole numbers — otherwise a recomputed 0.999 would pass as a match.
- **Whether it was re-derived or only re-read.** Some figures cannot be rebuilt from a campaign
  (see below). Where the console can only re-read what was recorded, it says so, because
  "matches" under the weaker check is a weaker claim.

Regenerate the backfilled findings with `node scripts/backfill-findings.mjs`. It refuses to
overwrite a file that already exists, so edits survive.

Three rules run through all of it:

1. **Numbers come from files, never from terminal text.** The recording is what a person saw;
   the events are what the run recorded. Parsing a progress bar for a token count is how a
   reported figure stops matching its evidence.
2. **Absent is not zero.** A v1 run has no token count for its LLM step until task 005 adds
   one, and rendering that as `0` would claim v1's LLM step is free.
3. **Every rate carries its denominator.** `evidenceSchema` will not accept a number without
   one. The parity study's 0.185-instead-of-0.208 error survived review because the
   denominator was not stated.

## Things the code knows that the task document does not say

Found while building Phase 1, and worth knowing before reading the code:

- **28 of the 163 run directories are empty.** The directory is created when a run starts and
  the manifest written only when it ends, so anything that dies in between leaves a shell. 135
  directories hold a manifest. §3 of the task says all 163 do.
- **The metrics database knows 25 runs whose directories are gone**, all from 2026-09-08. Their
  turn-level numbers survive; their prompts and outputs do not. So the Runs screen has three
  possible denominators — directories, manifests, database rows — and they are all different.
- **No per-turn clock time was ever recorded.** Every sidecar carries the run's *start* time,
  so replay timing is rebuilt by accumulating each turn's duration. Derived timings are marked
  `timingDerived` so no screen presents them as measured.
- **`harness/` is not at the repo root**; it is `src/caruca_v2/harness/`. The task document's
  paths (`harness/methods.py`) do not exist as written.
- **A prompt file cannot be compared to a recorded prompt, and `prompt_hash` cannot detect
  prompt drift.** The files are templates; the manifests record rendered text; the hash covers
  the rendering. `src/data/promptDrift.ts` explains what does work. One run on disk has
  genuinely drifted: `2026-09-08T201630Z_grep_48518d16`.
- **`better-sqlite3` does not build against Node 26.** Node's built-in `node:sqlite` is used
  instead, so the console carries no compiled dependency at all except `node-pty`.
- **`report --json` labels every stage's metrics with stage-1 names.** It emits its two metric
  slots as `f1` and `exact_argument_rate` whatever the campaign, filling them from that stage's
  own metric list — so stage 2's invocation recall arrives under the key
  `exact_argument_rate`. `recheck.ts` resolves the slot through each method's declared metric
  list rather than reading the key at face value.
- **`report p1_annotate` produces no metric values at all.** The stage-4 method names
  `rates.*` metrics that the ledger does not carry; only the `agreement.*` counts survive
  flattening. Stage 4's figures are computed by the console from the ledger instead, and
  labelled as re-read rather than re-derived.
- **v1 cannot be started in the VM with `~/caruca-venv/bin/caruca` as an argument.** `limactl`
  quotes each argument, so the guest's bash gets a literal `~`. `v1.py` only uses that form
  inside `sh -lc`. The console resolves the absolute guest path from the VM instead.
- **A process killed with SIGTERM can still report exit code 0**, so how a run ended is
  recorded separately from its exit code. Without that, a stopped run's record is
  indistinguishable from one that finished, and its partial outputs look complete.
- **Stage 3's pooled figures cannot be rebuilt from a campaign.** The ledger records each
  cell's rate but not its unit counts, and a pooled rate cannot be rebuilt from rates. The
  study's 0.606 (pooled over 33 units) and the report's 0.623 (mean over 12 cells) are both
  correct and mean different things.
