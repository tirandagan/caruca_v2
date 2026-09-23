"use client";

/**
 * Replays a terminal recording exactly as it was recorded.
 *
 * Why a real terminal emulator and not a list of lines (decision 4): v1's tracer redraws a
 * tqdm progress bar in place with carriage returns, and a line list turns that into thousands
 * of separate lines. Feeding the recorded bytes to xterm reproduces what a person saw,
 * carriage returns, escape sequences and all.
 *
 * **The page cannot type.** No input handler is attached and `disableStdin` is set, so there
 * is no path from the browser into a terminal. That is a requirement, not an omission (§10),
 * and it is why a live run can be watched safely from a page that anyone on this Mac can open.
 *
 * **The width comes from the recording.** v1's progress bar sizes itself to the terminal, so
 * replaying at the viewer's width would show something v1 never drew.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import type { Terminal } from "@xterm/xterm";
import type { AsciicastEvent, AsciicastHeader } from "../data/asciicast.js";
import "@xterm/xterm/css/xterm.css";

const SPEEDS = [0.5, 1, 2, 4, 8] as const;

export interface TerminalPlayerProps {
  header: Pick<AsciicastHeader, "width" | "height" | "title">;
  events: AsciicastEvent[];
  durationSeconds: number;
}

export function TerminalPlayer({ header, events, durationSeconds }: TerminalPlayerProps) {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const termRef = useRef<Terminal | null>(null);
  const timerRef = useRef<number | null>(null);
  const cursorRef = useRef(0);

  const [ready, setReady] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState<number>(1);
  const [at, setAt] = useState(0);

  // xterm touches `window` on import, so it is loaded in an effect rather than at module scope.
  useEffect(() => {
    let disposed = false;
    let term: Terminal | null = null;

    void (async () => {
      const { Terminal: XTerm } = await import("@xterm/xterm");
      if (disposed || !hostRef.current) return;
      term = new XTerm({
        cols: header.width,
        rows: header.height,
        // No path from the page into the terminal. See the note above.
        disableStdin: true,
        cursorBlink: false,
        convertEol: false,
        fontFamily: "'JetBrains Mono', Consolas, monospace",
        fontSize: 12.5,
        lineHeight: 1.35,
        theme: {
          background: "#0B1F33",
          foreground: "#D7E3F0",
          cursor: "#0B1F33",
          selectionBackground: "#2563EB",
        },
        scrollback: 20000,
      });
      term.open(hostRef.current);
      termRef.current = term;
      setReady(true);
    })();

    return () => {
      disposed = true;
      term?.dispose();
      termRef.current = null;
    };
  }, [header.width, header.height]);

  const stopTimer = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const reset = useCallback(() => {
    stopTimer();
    setPlaying(false);
    cursorRef.current = 0;
    setAt(0);
    termRef.current?.reset();
  }, [stopTimer]);

  /** Write every event up to `target` seconds without waiting - used for seeking. */
  const seekTo = useCallback(
    (target: number) => {
      const term = termRef.current;
      if (!term) return;
      term.reset();
      let index = 0;
      while (index < events.length && events[index]!.time <= target) {
        const event = events[index]!;
        if (event.kind === "o") term.write(event.data);
        index += 1;
      }
      cursorRef.current = index;
      setAt(target);
    },
    [events],
  );

  // The playback loop. Each step waits the real gap between two recorded events, divided by
  // the chosen speed, so the timing is the recording's own rather than a fixed tick.
  useEffect(() => {
    if (!playing || !ready) return;

    const step = () => {
      const term = termRef.current;
      if (!term) return;

      const index = cursorRef.current;
      if (index >= events.length) {
        setPlaying(false);
        setAt(durationSeconds);
        return;
      }

      const event = events[index]!;
      if (event.kind === "o") term.write(event.data);
      cursorRef.current = index + 1;
      setAt(event.time);

      const next = events[index + 1];
      if (!next) {
        setPlaying(false);
        setAt(durationSeconds);
        return;
      }
      const waitMs = Math.max(0, ((next.time - event.time) * 1000) / speed);
      timerRef.current = window.setTimeout(step, waitMs);
    };

    // A recording that starts with a long pause should not look frozen.
    const first = events[cursorRef.current];
    const lead = first ? Math.max(0, ((first.time - at) * 1000) / speed) : 0;
    timerRef.current = window.setTimeout(step, Math.min(lead, 400));

    return stopTimer;
    // `at` is deliberately excluded: it changes on every step and would restart the loop.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, ready, speed, events, durationSeconds, stopTimer]);

  const atEnd = cursorRef.current >= events.length && !playing;

  return (
    <div>
      <div ref={hostRef} className="terminal__body" style={{ padding: "10px 12px" }} />
      <div
        className="row"
        style={{
          padding: "8px 12px",
          borderTop: "1px solid var(--border-default)",
          background: "var(--surface-thead)",
        }}
      >
        <button
          className="btn btn--primary"
          type="button"
          disabled={!ready}
          onClick={() => {
            if (atEnd) reset();
            setPlaying((value) => !value);
          }}
        >
          {playing ? "Pause" : atEnd ? "Replay" : "Play"}
        </button>
        <button className="btn" type="button" disabled={!ready} onClick={reset}>
          Restart
        </button>

        <label className="label" htmlFor="speed" style={{ marginLeft: 8 }}>
          Speed
        </label>
        <select
          id="speed"
          className="btn"
          value={speed}
          onChange={(event) => setSpeed(Number(event.target.value))}
        >
          {SPEEDS.map((value) => (
            <option key={value} value={value}>
              {value}x
            </option>
          ))}
        </select>

        <input
          type="range"
          min={0}
          max={Math.max(durationSeconds, 0.001)}
          step={0.01}
          value={at}
          disabled={!ready}
          onChange={(event) => {
            stopTimer();
            setPlaying(false);
            seekTo(Number(event.target.value));
          }}
          style={{ flex: 1, minWidth: 120, accentColor: "var(--blue)" }}
          aria-label="Position in the recording"
        />

        <span className="mono faint" style={{ fontSize: "var(--text-caption)" }}>
          {at.toFixed(1)}s / {durationSeconds.toFixed(1)}s · {header.width}x{header.height}
        </span>
      </div>
    </div>
  );
}
