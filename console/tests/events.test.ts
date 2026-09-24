/**
 * The event stream, and the asciicast recordings it sits beside.
 *
 * The distinction these tests protect: the recording is what a person saw, the events are what
 * the run recorded, and a number never comes from the former.
 */
import { describe, expect, it } from "vitest";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { eventsForRun } from "../src/data/events.js";
import { findRun, listRuns, loadRun } from "../src/data/runs.js";
import {
  RecordingWriter,
  parseRecording,
  readRecording,
  outputText,
  RecordingUnreadableError,
} from "../src/data/asciicast.js";

const TRACE_RUN = "2026-09-14T163935Z_cat_a3ea2a72";

describe("events for an existing run", () => {
  const events = eventsForRun(loadRun(findRun(TRACE_RUN)));

  it("starts with the run and ends with the run", () => {
    expect(events[0]!.kind).toBe("run_start");
    expect(events.at(-1)!.kind).toBe("run_end");
  });

  it("marks every timing as derived, because none was recorded (Phase 0(a))", () => {
    expect(events.every((event) => event.timingDerived)).toBe(true);
  });

  it("marks the command line as reconstructed (Phase 0(b))", () => {
    const start = events.find((event) => event.kind === "run_start")!;
    expect(start.argvReconstructed).toBe(true);
    expect(start.where).toBe("lima");
  });

  it("lays turns out in order by accumulating their durations", () => {
    const turns = events.filter((event) => event.kind === "model_turn");
    expect(turns).toHaveLength(10);
    const times = turns.map((turn) => turn.at);
    expect([...times].sort((a, b) => a - b)).toEqual(times);
    // The last turn's position is the sum of all ten durations.
    const summed = turns.reduce((total, turn) => total + turn.seconds, 0);
    expect(times.at(-1)).toBeCloseTo(summed, 6);
  });

  it("reports five stage-3 sessions, one of which never reported", () => {
    // §10: "one ended without calling the reporting tool, and four reported two interactions each".
    const sessions = events.filter((event) => event.kind === "trace_session");
    expect(sessions).toHaveLength(5);
    expect(sessions.filter((session) => !session.reported)).toHaveLength(1);
    expect(sessions.filter((session) => session.interactions === 2)).toHaveLength(4);
  });

  it("names the artifact and what reads it next", () => {
    const artifacts = events.filter((event) => event.kind === "artifact_written");
    expect(artifacts).toHaveLength(1);
    expect(artifacts[0]!.path).toContain("cat.traces.json");
    expect(artifacts[0]!.consumedBy).toBe("annotate");
  });

  it("totals the turn costs back to the run's cost", () => {
    const turns = events.filter((event) => event.kind === "model_turn");
    const end = events.find((event) => event.kind === "run_end")!;
    const summed = turns.reduce((total, turn) => total + turn.costUsd, 0);
    expect(summed).toBeCloseTo(end.costUsd, 10);
  });

  it("builds events for every run on disk without throwing", () => {
    // Guards the adapter against the shape variation across 135 manifests: four stages, five
    // runs with no prompt_variant, failed runs, and runs with no validation report.
    for (const summary of listRuns().runs) {
      expect(eventsForRun(loadRun(summary.dir)).length).toBeGreaterThan(0);
    }
  });
});

describe("terminal recordings", () => {
  it("round-trips what was written, with timings", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-cast-"));
    const path = join(dir, "terminal.cast");
    const started = Date.now();
    const writer = new RecordingWriter(
      path,
      { width: 117, height: 30, command: "caruca trace cat", caruca: { side: "v1", runId: "r1", host: "lima", limaInstance: "caruca" } },
      started,
    );
    writer.write("hello\r\n", started + 250);
    writer.marker("stage:trace", started + 400);
    writer.write("\r100%|####|", started + 1000);
    return writer.close().then(() => {
      const recording = readRecording(path);
      expect(recording.header.width).toBe(117);
      expect(recording.header.caruca?.host).toBe("lima");
      expect(recording.events).toHaveLength(3);
      expect(recording.events[0]!.time).toBeCloseTo(0.25, 6);
      expect(recording.events[1]!.kind).toBe("m");
      expect(recording.durationSeconds).toBeCloseTo(1.0, 6);
      // The progress-bar redraw survives byte for byte, carriage return included.
      expect(outputText(recording)).toBe("hello\r\n\r100%|####|");
    });
  });

  it("replays everything before a truncated final line rather than refusing", () => {
    const recording = parseRecording(
      `{"version":2,"width":80,"height":24}\n[0.1,"o","a"]\n[0.2,"o","b`,
    );
    expect(recording.events).toHaveLength(1);
    expect(outputText(recording)).toBe("a");
  });

  it("refuses a version it cannot replay faithfully", () => {
    expect(() => parseRecording(`{"version":1,"width":80,"height":24}\n`)).toThrow(
      RecordingUnreadableError,
    );
  });

  it("refuses an empty file", () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-cast-"));
    const path = join(dir, "empty.cast");
    writeFileSync(path, "");
    expect(() => readRecording(path)).toThrow(RecordingUnreadableError);
  });
});

describe("a recording of a real program", () => {
  // Produced by `node scripts/record-sample.mjs`, which runs v1's `generate cat --max-count 1`
  // through a pseudo-terminal. That command executes nothing and calls no model, so the
  // fixture is free to regenerate - and it is real terminal output rather than invented text.
  const path = new URL("./fixtures/v1-generate-cat.cast", import.meta.url).pathname;

  it("reads back what v1 printed, with the line endings a terminal produces", () => {
    const recording = readRecording(path);
    expect(recording.header.width).toBe(117);
    expect(recording.header.caruca?.side).toBe("v1");

    const text = outputText(recording);
    expect(text).toContain("cat -b");
    // A pty gives the program a terminal, so it emits CRLF. A pipe would not, and the
    // difference is exactly why replay uses a terminal emulator rather than a line list.
    expect(text).toContain("\r\n");
  });

  it("carries a duration and at least one event", () => {
    const recording = readRecording(path);
    expect(recording.events.length).toBeGreaterThan(0);
    expect(recording.durationSeconds).toBeGreaterThan(0);
  });
});

describe("tool calls", () => {
  it("names the tool, rather than reporting every call as unnamed", () => {
    // The audit records the tool under `tool`; reading `name` produced a rail of "(unnamed)".
    const events = eventsForRun(loadRun(findRun(TRACE_RUN)));
    const calls = events.filter((event) => event.kind === "tool_call");
    expect(calls.length).toBeGreaterThan(0);
    expect(calls.some((call) => call.name.includes("not recorded"))).toBe(false);
    expect(new Set(calls.map((call) => call.name))).toEqual(
      new Set(["run_command", "report_observations"]),
    );
  });

  it("calls report_observations exactly as often as a session reported", () => {
    // A cross-check between two independently recorded parts of the manifest: five sessions,
    // four of which reported, and four calls to the reporting tool. If these ever disagree,
    // one of the two is being read wrongly.
    const events = eventsForRun(loadRun(findRun(TRACE_RUN)));
    const reportCalls = events.filter(
      (event) => event.kind === "tool_call" && event.name === "report_observations",
    );
    const reportedSessions = events.filter(
      (event) => event.kind === "trace_session" && event.reported,
    );
    expect(reportCalls).toHaveLength(reportedSessions.length);
    expect(reportCalls).toHaveLength(4);
  });

  it("keeps each call's arguments, which is what makes the audit readable", () => {
    const events = eventsForRun(loadRun(findRun(TRACE_RUN)));
    const first = events.find((event) => event.kind === "tool_call");
    expect(first?.arguments).toEqual({ argv: ["cat"] });
  });

  it("records that every call was allowed for this run", () => {
    const events = eventsForRun(loadRun(findRun(TRACE_RUN)));
    const refused = events.filter((event) => event.kind === "tool_call" && !event.allowed);
    expect(refused).toHaveLength(0);
  });
});

describe("a recording that would grow without limit", () => {
  it("stops recording at the cap, marks the file, and lets the run continue", async () => {
    // v1's `generate grep` at its defaults prints about three million lines in six seconds.
    // A recording is evidence about a run; it must never be the reason a run is cut short.
    const dir = mkdtempSync(join(tmpdir(), "caruca-cap-"));
    const path = join(dir, "big.cast");
    const started = Date.now();
    const writer = new RecordingWriter(path, { width: 80, height: 24 }, started, 2048);

    for (let i = 0; i < 200; i += 1) writer.write("x".repeat(100), started + i);
    expect(writer.isCapped).toBe(true);
    writer.write("more output after the cap", started + 500);
    await writer.close();

    const recording = readRecording(path);
    const markers = recording.events.filter((event) => event.kind === "m");
    expect(markers).toHaveLength(1);
    expect(markers[0]!.data).toContain("the run continued");
    // Nothing recorded after the cap.
    expect(outputText(recording)).not.toContain("more output after the cap");
  });

  it("records everything when the cap is not reached", async () => {
    const dir = mkdtempSync(join(tmpdir(), "caruca-cap-"));
    const path = join(dir, "small.cast");
    const writer = new RecordingWriter(path, { width: 80, height: 24 });
    writer.write("hello");
    expect(writer.isCapped).toBe(false);
    await writer.close();
    expect(outputText(readRecording(path))).toBe("hello");
  });
});
