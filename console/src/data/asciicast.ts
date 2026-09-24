/**
 * Terminal recordings, in the asciicast v2 format.
 *
 * Decision 4 puts a real terminal on each side, and §6.3 requires every byte each terminal
 * shows to be recorded with its timing so a run can be replayed exactly. asciicast v2 is the
 * standard format for that: a JSON header line, then one JSON array per event,
 * `[seconds, "o", data]`. It is line-oriented, so a recording can be appended to while a run
 * is still going and read back by a replayer that started before the run finished.
 *
 * Phase 0(f): these are committed, like the rest of the run data.
 *
 * **The width matters and is recorded.** v1's tracer draws a tqdm progress bar sized to the
 * terminal, so a recording replayed at a different width does not show what v1 showed. The
 * header carries the size the run actually used.
 */
import { appendFileSync, createWriteStream, readFileSync, writeFileSync } from "node:fs";
import type { WriteStream } from "node:fs";

export class RecordingUnreadableError extends Error {}

export interface AsciicastHeader {
  readonly version: 2;
  readonly width: number;
  readonly height: number;
  /** Unix seconds at which recording started. */
  readonly timestamp?: number;
  readonly title?: string;
  readonly env?: Record<string, string>;
  /** Ours: exactly what was run and where, so a recording explains itself. */
  readonly command?: string;
  readonly caruca?: {
    readonly side: "v1" | "v2";
    readonly runId: string;
    readonly host: "mac" | "lima";
    readonly limaInstance?: string;
  };
}

/** `"o"` is output, `"i"` input, `"m"` a marker. The console never records input: it cannot type. */
export type AsciicastEventKind = "o" | "i" | "m";

export interface AsciicastEvent {
  /** Seconds since the recording started. */
  readonly time: number;
  readonly kind: AsciicastEventKind;
  readonly data: string;
}

export interface Recording {
  readonly header: AsciicastHeader;
  readonly events: AsciicastEvent[];
  /** Seconds from the first event to the last. Zero for a recording with no output. */
  readonly durationSeconds: number;
}

export function parseRecording(text: string): Recording {
  const lines = text.split("\n").filter((line) => line.trim().length > 0);
  const first = lines[0];
  if (!first) throw new RecordingUnreadableError("Recording is empty: no header line.");

  let header: AsciicastHeader;
  try {
    header = JSON.parse(first) as AsciicastHeader;
  } catch (cause) {
    throw new RecordingUnreadableError(`Header is not valid JSON: ${(cause as Error).message}`);
  }
  if (header.version !== 2) {
    throw new RecordingUnreadableError(
      `Only asciicast v2 is supported; this recording says version ${String(header.version)}.`,
    );
  }

  const events: AsciicastEvent[] = [];
  for (let index = 1; index < lines.length; index += 1) {
    const line = lines[index]!;
    let parsed: unknown;
    try {
      parsed = JSON.parse(line);
    } catch {
      // A run killed mid-write can leave a partial final line. Everything before it is still
      // a valid recording, and truncating there is better than refusing to replay at all.
      break;
    }
    if (!Array.isArray(parsed) || parsed.length < 3) break;
    const [time, kind, data] = parsed as [unknown, unknown, unknown];
    if (typeof time !== "number" || typeof kind !== "string" || typeof data !== "string") break;
    events.push({ time, kind: kind as AsciicastEventKind, data });
  }

  const last = events.at(-1);
  return { header, events, durationSeconds: last ? last.time : 0 };
}

export function readRecording(path: string): Recording {
  try {
    return parseRecording(readFileSync(path, "utf8"));
  } catch (cause) {
    if (cause instanceof RecordingUnreadableError) throw cause;
    throw new RecordingUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }
}

/** Everything the terminal showed, concatenated. For searching, never for deriving numbers. */
export function outputText(recording: Recording): string {
  return recording.events
    .filter((event) => event.kind === "o")
    .map((event) => event.data)
    .join("");
}

/**
 * Writes a recording as a run proceeds.
 *
 * Appends line by line and flushes as it goes, so a recording is replayable even if the run is
 * killed - which matters, because the runs most worth watching again are the ones that failed.
 */
/**
 * How large a recording may grow before it stops recording.
 *
 * Recordings are committed (Phase 0(f)), and a runaway run can produce an unreasonable amount
 * of output: v1's `generate grep` at its defaults prints about three million lines in six
 * seconds, which produced a 33 MB recording from twelve seconds of running. Past this point
 * the recording stops taking output and says so in the file, while the run itself carries on
 * untouched — a recording is evidence about a run, and it must never be the reason a run is
 * cut short.
 *
 * 16 MB is chosen against what these are for: replaying a run. A trace's progress bar over an
 * hour is well inside it, and anything larger is a wall of enumeration nobody will watch.
 */
export const RECORDING_CAP_BYTES = 16 * 1024 * 1024;

export class RecordingWriter {
  private readonly stream: WriteStream;
  private readonly startedAt: number;
  private closed = false;
  private written = 0;
  private capped = false;

  constructor(
    private readonly path: string,
    header: Omit<AsciicastHeader, "version" | "timestamp">,
    startedAt = Date.now(),
    private readonly cap: number = RECORDING_CAP_BYTES,
  ) {
    this.startedAt = startedAt;
    const full: AsciicastHeader = {
      ...header,
      version: 2,
      timestamp: Math.floor(startedAt / 1000),
    };
    writeFileSync(path, `${JSON.stringify(full)}\n`);
    this.stream = createWriteStream(path, { flags: "a" });
  }

  /** Record bytes the terminal showed, timestamped relative to the start of the recording. */
  write(data: string, at = Date.now()): void {
    if (this.closed) throw new Error(`Recording ${this.path} is already closed.`);
    if (this.capped) return;

    const seconds = (at - this.startedAt) / 1000;
    const line = `${JSON.stringify([seconds, "o", data])}\n`;
    this.written += line.length;

    if (this.written > this.cap) {
      // Say so in the recording itself, so a replay shows the truncation rather than simply
      // ending. The run is not affected.
      this.capped = true;
      this.stream.write(
        `${JSON.stringify([
          seconds,
          "m",
          `recording stopped at ${Math.round(this.cap / (1024 * 1024))} MB; the run continued`,
        ])}\n`,
      );
      return;
    }

    this.stream.write(line);
  }

  /** True once the recording stopped taking output. The run itself was not interrupted. */
  get isCapped(): boolean {
    return this.capped;
  }

  /** A named point in the recording: a stage boundary, a turn, a tool call. */
  marker(label: string, at = Date.now()): void {
    if (this.closed) throw new Error(`Recording ${this.path} is already closed.`);
    this.stream.write(`${JSON.stringify([(at - this.startedAt) / 1000, "m", label])}\n`);
  }

  close(): Promise<void> {
    if (this.closed) return Promise.resolve();
    this.closed = true;
    return new Promise((resolve, reject) => {
      this.stream.end((error?: Error | null) => (error ? reject(error) : resolve()));
    });
  }
}

/** Append a single event to an existing recording, without holding a stream open. */
export function appendEvent(path: string, event: AsciicastEvent): void {
  appendFileSync(path, `${JSON.stringify([event.time, event.kind, event.data])}\n`);
}
