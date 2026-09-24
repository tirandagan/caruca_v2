"use client";

/**
 * A live terminal, watched over a WebSocket.
 *
 * The server owns the process; this only displays it. Two consequences worth stating, because
 * both are requirements rather than side effects:
 *
 *   - **Reloading the page does not stop the run.** On connect the server sends everything the
 *     terminal has shown so far, then the live stream, so the display rebuilds and carries on.
 *     Closing the tab detaches a listener and nothing else.
 *   - **There is no path from here into the process.** `disableStdin` is set, no key handler is
 *     attached, and the server ignores anything a client sends. The page can watch and stop.
 *
 * The terminal is created at the size the server recorded, not the viewer's, because v1's
 * tracer sizes its progress bar to the terminal.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import type { Terminal } from "@xterm/xterm";
import { Badge } from "./ui.js";
import "@xterm/xterm/css/xterm.css";

export type LiveState = "connecting" | "running" | "exited" | "stopped" | "failed" | "gone";

export interface LiveTerminalProps {
  readonly runId: string;
  readonly side: "v1" | "v2";
  readonly cols: number;
  readonly rows: number;
  /** Called when the run ends, so the page can refresh what it shows beside the terminal. */
  readonly onFinished?: (state: string, exitCode: number | null) => void;
}

interface ServerMessage {
  type: "attached" | "data" | "exit" | "error";
  data?: string;
  backlog?: string;
  message?: string;
  exitCode?: number | null;
  state?: string;
  info?: { where: "mac" | "lima"; argv: string[]; concurrentWith: string[] };
}

export function LiveTerminal({ runId, side, cols, rows, onFinished }: LiveTerminalProps) {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const termRef = useRef<Terminal | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  const [state, setState] = useState<LiveState>("connecting");
  const [exitCode, setExitCode] = useState<number | null>(null);
  const [where, setWhere] = useState<"mac" | "lima" | null>(null);
  const [concurrent, setConcurrent] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const write = useCallback((text: string) => {
    termRef.current?.write(text);
  }, []);

  useEffect(() => {
    let disposed = false;
    let term: Terminal | null = null;

    void (async () => {
      const { Terminal: XTerm } = await import("@xterm/xterm");
      if (disposed || !hostRef.current) return;

      term = new XTerm({
        cols,
        rows,
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
        scrollback: 50000,
      });
      term.open(hostRef.current);
      termRef.current = term;

      const socket = new WebSocket(
        `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/terminal?runId=${encodeURIComponent(runId)}`,
      );
      socketRef.current = socket;

      socket.onmessage = (event) => {
        const message = JSON.parse(event.data as string) as ServerMessage;
        switch (message.type) {
          case "attached":
            // Everything shown so far, then the live stream. This is the reload path.
            if (message.backlog) write(message.backlog);
            setState("running");
            setWhere(message.info?.where ?? null);
            setConcurrent(message.info?.concurrentWith ?? []);
            break;
          case "data":
            if (message.data) write(message.data);
            break;
          case "exit":
            // The terminal keeps whatever it showed. A finished run is still worth reading,
            // and this is the only place the output of a run that took 200ms is visible.
            setState((message.state as LiveState) ?? "exited");
            setExitCode(message.exitCode ?? null);
            onFinished?.(message.state ?? "exited", message.exitCode ?? null);
            break;
          case "error":
            setError(message.message ?? "the server refused the connection");
            setState("gone");
            break;
        }
      };

      socket.onerror = () => setError("the connection to the server failed");
      socket.onclose = () =>
        setState((current) => (current === "running" || current === "connecting" ? "gone" : current));
    })();

    return () => {
      disposed = true;
      socketRef.current?.close();
      term?.dispose();
      termRef.current = null;
    };
  }, [runId, cols, rows, write, onFinished]);

  return (
    <div className="terminal">
      <div className="terminal__head">
        <span className="label">{side === "v1" ? "v1 · caruca" : "v2 · caruca-v2"}</span>
        <span className="terminal__where">
          {where === "lima" ? "lima vm · caruca" : where === "mac" ? "this mac" : "…"}
        </span>
        {state === "running" ? (
          <Badge tone="ok" dot>
            live
          </Badge>
        ) : state === "connecting" ? (
          <Badge tone="muted">connecting</Badge>
        ) : state === "stopped" ? (
          <Badge tone="warn">stopped</Badge>
        ) : state === "failed" ? (
          <Badge tone="bad">failed{exitCode === null ? "" : ` (${exitCode})`}</Badge>
        ) : state === "gone" ? (
          <Badge tone="muted">not attached</Badge>
        ) : (
          <Badge tone="ok">finished</Badge>
        )}
      </div>

      <div ref={hostRef} className="terminal__body" style={{ padding: "10px 12px" }} />

      {error ? (
        <div style={{ padding: "8px 12px", borderTop: "1px solid var(--border-default)" }}>
          <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
            {error}
          </span>
        </div>
      ) : null}

      {concurrent.length > 0 ? (
        <div
          style={{
            padding: "8px 12px",
            borderTop: "1px solid var(--border-default)",
            background: "var(--warning-bg)",
          }}
        >
          <span style={{ fontSize: "var(--text-caption)", color: "var(--warning-text)" }}>
            Ran alongside {concurrent.length} other run
            {concurrent.length === 1 ? "" : "s"}. The two share this Mac&apos;s processors, so
            wall-clock time from this run is not comparable with a run made on its own.
          </span>
        </div>
      ) : null}
    </div>
  );
}
