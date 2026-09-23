/**
 * The registry of running processes, and their terminals.
 *
 * **The server owns each process, not the browser** (§7, decision 4). That is what makes a run
 * survive closing or reloading the page: the pseudo-terminal, the recording and the child
 * process all live here, and a page that reconnects is handed the output so far and then the
 * live stream. It also settles the question `PRODUCT.md` left open about where a long-lived
 * process should live.
 *
 * Four safety properties, each structural rather than advisory:
 *
 *   1. **Processes are started from argument lists, never a shell string.** `node-pty`'s
 *      `spawn` takes a file and an argv array, and nothing here builds a command by
 *      concatenation. The single form that needs a shell — v1's `annotate` inside the VM —
 *      arrives as `["sh", "-lc", "<one string>"]` from `v1Invocations.ts`, which is the form
 *      `v1.py` already uses.
 *   2. **Only a fixed set of programs may be started.** v1's two virtualenvs, `caruca-v2`, and
 *      `limactl`. Anything else is refused before a process exists.
 *   3. **There is no path from the page into a terminal.** Nothing in this module writes to a
 *      pty's input, and no message from a client can reach one. The page can watch and stop,
 *      and that is all.
 *   4. **The terminal size is fixed and recorded.** v1's tracer sizes its progress bar to the
 *      terminal, so a recording replayed at a different width would not show what v1 showed.
 */
import { createRequire } from "node:module";
import { execFile } from "node:child_process";
import { mkdirSync } from "node:fs";
import { basename, join } from "node:path";
import { promisify } from "node:util";
import { RecordingWriter } from "../data/asciicast.js";
import { repoPaths, v1Root } from "../data/paths.js";
import { writeV1Manifest, V1_RECORDING_NAME, type V1RunManifest } from "../data/v1Runs.js";

const run = promisify(execFile);

/**
 * `node-pty` is loaded through `createRequire` for the same reason `node:sqlite` is: it is a
 * native module and must not be handed to a bundler. It is also loaded lazily, so a console
 * that will only replay never needs it present.
 */
interface PtyProcess {
  readonly pid: number;
  onData(listener: (data: string) => void): { dispose(): void };
  onExit(listener: (event: { exitCode: number; signal?: number }) => void): { dispose(): void };
  kill(signal?: string): void;
  resize(columns: number, rows: number): void;
}
interface PtyModule {
  spawn(
    file: string,
    args: string[],
    options: {
      name: string;
      cols: number;
      rows: number;
      cwd: string;
      env: NodeJS.ProcessEnv;
    },
  ): PtyProcess;
}

let ptyModule: PtyModule | null = null;
function loadPty(): PtyModule {
  if (ptyModule) return ptyModule;
  try {
    ptyModule = createRequire(import.meta.url)("node-pty") as PtyModule;
    return ptyModule;
  } catch (cause) {
    throw new ProcessStartError(
      `node-pty could not be loaded: ${(cause as Error).message}. ` +
        `Run \`npm install\` in console/, which also makes its spawn-helper executable.`,
    );
  }
}

export class ProcessStartError extends Error {}
export class ProgramNotAllowedError extends ProcessStartError {}

/** The terminal size every run uses. Recorded with the run, because v1's output depends on it. */
export const TERMINAL_COLS = 117;
export const TERMINAL_ROWS = 34;

/** How much output a reattaching page is given. Enough for a long trace's progress bar. */
const REPLAY_BUFFER_BYTES = 4 * 1024 * 1024;

/**
 * The only programs the console may start.
 *
 * Checked on the resolved path of the executable, so this cannot be satisfied by a program
 * that merely has one of these names somewhere else.
 */
function allowedPrograms(): string[] {
  const paths = repoPaths();
  const programs = [join(paths.root, ".venv", "bin", "caruca-v2")];
  try {
    const root = v1Root();
    programs.push(join(root, "caruca", ".venv", "bin", "caruca"));
    programs.push(join(root, "caruca", ".venv-llm", "bin", "caruca"));
  } catch {
    // No v1 checkout on this machine; only v2 can be started.
  }
  return programs;
}

/** `limactl` is allowed by name, because it is found on PATH rather than at a fixed place. */
const ALLOWED_BY_NAME = new Set(["limactl"]);

export function assertProgramAllowed(program: string): void {
  if (ALLOWED_BY_NAME.has(basename(program)) && !program.includes("/")) return;
  if (allowedPrograms().includes(program)) return;
  throw new ProgramNotAllowedError(
    `${program} is not one of the programs the console may start. ` +
      `Allowed: caruca-v2, v1's caruca (.venv and .venv-llm), and limactl.`,
  );
}

export type RunSide = "v1" | "v2";
export type RunState = "running" | "exited" | "stopped" | "failed";

export interface StartSpec {
  readonly runId: string;
  readonly side: RunSide;
  readonly argv: readonly string[];
  readonly cwd: string;
  /** Where the recording and, for v1, the run record are written. */
  readonly runDir: string;
  readonly where: "mac" | "lima";
  readonly limaInstance?: string | null;
  /** A v1 run record to write when the run ends. v2 writes its own manifest. */
  readonly v1Manifest?: Omit<V1RunManifest, "ended_at" | "exit_code" | "concurrent_with"> | null;
  readonly title?: string;
}

export interface LiveRun {
  readonly runId: string;
  readonly side: RunSide;
  readonly argv: readonly string[];
  readonly where: "mac" | "lima";
  readonly limaInstance: string | null;
  readonly runDir: string;
  readonly startedAt: number;
  state: RunState;
  exitCode: number | null;
  /** Runs that were going at the same time. Their wall-clock times are not comparable. */
  concurrentWith: string[];
}

interface Entry {
  readonly info: LiveRun;
  readonly pty: PtyProcess;
  readonly recording: RecordingWriter;
  /** Output so far, for a page that connects late or reconnects. */
  buffer: string;
  readonly listeners: Set<(data: string) => void>;
  readonly exitListeners: Set<(code: number | null, state: RunState) => void>;
  readonly manifest: StartSpec["v1Manifest"];
  stopRequested: boolean;
}

/**
 * One registry per server process, held on `globalThis`.
 *
 * Next reloads modules in development. Without this, a reload would orphan every running
 * process: the child would keep going with nothing watching it and nothing able to stop it.
 */
const REGISTRY_KEY = Symbol.for("caruca.console.processes");
type Registry = Map<string, Entry>;

function registry(): Registry {
  const holder = globalThis as unknown as Record<symbol, Registry | undefined>;
  if (!holder[REGISTRY_KEY]) holder[REGISTRY_KEY] = new Map();
  return holder[REGISTRY_KEY]!;
}

/** Runs that are going right now. */
export function running(): LiveRun[] {
  return [...registry().values()]
    .filter((entry) => entry.info.state === "running")
    .map((entry) => entry.info);
}

export function get(runId: string): LiveRun | null {
  return registry().get(runId)?.info ?? null;
}

export function all(): LiveRun[] {
  return [...registry().values()].map((entry) => entry.info);
}

/**
 * Start a process in a pseudo-terminal.
 *
 * The environment is the one this server was started with, plus the pseudo-terminal's own
 * `TERM`. Nothing else is added: v2 loads `.env` itself, and v1's defaults — including
 * `CARUCA_ISOLATION_METHOD`, which must stay unset — are left exactly as they are, because a
 * v1 run under different settings is not the run the measurements came from.
 */
export function start(spec: StartSpec): LiveRun {
  const [program, ...args] = spec.argv;
  if (!program) throw new ProcessStartError("no program to run");
  assertProgramAllowed(program);

  if (registry().has(spec.runId)) {
    throw new ProcessStartError(`${spec.runId} is already registered.`);
  }

  mkdirSync(spec.runDir, { recursive: true });

  const startedAt = Date.now();
  const concurrentWith = running().map((other) => other.runId);

  const recording = new RecordingWriter(
    join(spec.runDir, V1_RECORDING_NAME),
    {
      width: TERMINAL_COLS,
      height: TERMINAL_ROWS,
      ...(spec.title ? { title: spec.title } : {}),
      command: spec.argv.join(" "),
      caruca: {
        side: spec.side,
        runId: spec.runId,
        host: spec.where,
        ...(spec.limaInstance ? { limaInstance: spec.limaInstance } : {}),
      },
    },
    startedAt,
  );

  const pty = loadPty().spawn(program, args, {
    name: "xterm-256color",
    cols: TERMINAL_COLS,
    rows: TERMINAL_ROWS,
    cwd: spec.cwd,
    env: process.env,
  });

  const info: LiveRun = {
    runId: spec.runId,
    side: spec.side,
    argv: spec.argv,
    where: spec.where,
    limaInstance: spec.limaInstance ?? null,
    runDir: spec.runDir,
    startedAt,
    state: "running",
    exitCode: null,
    concurrentWith,
  };

  const entry: Entry = {
    info,
    pty,
    recording,
    buffer: "",
    listeners: new Set(),
    exitListeners: new Set(),
    manifest: spec.v1Manifest ?? null,
    stopRequested: false,
  };
  registry().set(spec.runId, entry);

  // Anything already running now overlaps with this one too, in both directions.
  for (const other of registry().values()) {
    if (other.info.runId !== spec.runId && other.info.state === "running") {
      other.info.concurrentWith = [...new Set([...other.info.concurrentWith, spec.runId])];
    }
  }

  pty.onData((data) => {
    recording.write(data);
    entry.buffer = (entry.buffer + data).slice(-REPLAY_BUFFER_BYTES);
    for (const listener of entry.listeners) listener(data);
  });

  pty.onExit(({ exitCode }) => {
    info.state = entry.stopRequested ? "stopped" : exitCode === 0 ? "exited" : "failed";
    info.exitCode = exitCode;
    void recording.close();

    if (entry.manifest) {
      try {
        writeV1Manifest(spec.runDir, {
          ...entry.manifest,
          ended_at: new Date().toISOString(),
          exit_code: exitCode,
          concurrent_with: info.concurrentWith,
        } as V1RunManifest);
      } catch {
        // A run record that could not be written must not take the server down; the
        // recording is already on disk and the state below still reports the outcome.
      }
    }

    for (const listener of entry.exitListeners) listener(exitCode, info.state);
  });

  return info;
}

export interface Attachment {
  /** Everything the terminal has shown so far. */
  readonly backlog: string;
  readonly info: LiveRun;
  readonly detach: () => void;
}

/**
 * Watch a run: the output so far, then everything that follows.
 *
 * This is what makes a reload harmless. The page throws its terminal away and is handed the
 * backlog when it comes back, so the run continues undisturbed and the display catches up.
 */
export function attach(
  runId: string,
  onData: (data: string) => void,
  onExit?: (code: number | null, state: RunState) => void,
): Attachment | null {
  const entry = registry().get(runId);
  if (!entry) return null;

  entry.listeners.add(onData);
  if (onExit) entry.exitListeners.add(onExit);

  return {
    backlog: entry.buffer,
    info: entry.info,
    detach: () => {
      entry.listeners.delete(onData);
      if (onExit) entry.exitListeners.delete(onExit);
    },
  };
}

export interface StopResult {
  readonly runId: string;
  readonly stopped: boolean;
  /** For a Lima run, what was still running in the VM afterwards. Empty is the good answer. */
  readonly survivingInVm: string[];
  readonly detail: string;
}

/**
 * Stop a run on the Mac and, for a Lima run, inside the VM as well.
 *
 * Killing `limactl` on the host does not necessarily stop what it started inside the guest, so
 * a Lima run is followed by a kill inside the VM and then a check. §10 requires that stopping
 * a Lima trace leaves no v1 process running in the VM, so the check reports what survived
 * rather than assuming.
 */
export async function stop(runId: string): Promise<StopResult> {
  const entry = registry().get(runId);
  if (!entry) return { runId, stopped: false, survivingInVm: [], detail: "no such run" };

  if (entry.info.state !== "running") {
    return { runId, stopped: false, survivingInVm: [], detail: `already ${entry.info.state}` };
  }

  entry.stopRequested = true;
  entry.pty.kill("SIGTERM");

  if (entry.info.where !== "lima" || !entry.info.limaInstance) {
    return { runId, stopped: true, survivingInVm: [], detail: "stopped on this Mac" };
  }

  const instance = entry.info.limaInstance;
  // Scoped to v1's own entry point inside the VM, so nothing else in the guest is touched.
  const pattern = "caruca-venv/bin/caruca";

  try {
    await run("limactl", ["shell", instance, "--", "pkill", "-TERM", "-f", pattern], {
      timeout: 20_000,
    });
  } catch {
    // pkill exits non-zero when it matched nothing, which is the outcome we want.
  }

  let surviving: string[] = [];
  try {
    const { stdout } = await run(
      "limactl",
      ["shell", instance, "--", "pgrep", "-af", pattern],
      { timeout: 20_000 },
    );
    surviving = stdout.split("\n").map((line) => line.trim()).filter(Boolean);
  } catch {
    // pgrep exits 1 when nothing matches: nothing survived.
    surviving = [];
  }

  return {
    runId,
    stopped: true,
    survivingInVm: surviving,
    detail:
      surviving.length === 0
        ? `stopped on this Mac and in the VM "${instance}"`
        : `stopped here, but ${surviving.length} process(es) are still running in "${instance}"`,
  };
}

/** Forget a finished run. Its recording and record stay on disk. */
export function forget(runId: string): void {
  const entry = registry().get(runId);
  if (entry && entry.info.state === "running") return;
  registry().delete(runId);
}
