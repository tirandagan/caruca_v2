/**
 * The console's server: Next, plus the WebSocket that carries a live terminal.
 *
 * Next's route handlers cannot hold a WebSocket open, and §7 asks for **one long-lived local
 * server** that owns each running process — so that closing or reloading the page does not
 * stop a run. That is what this is. It also settles the question `PRODUCT.md` left open about
 * where a long-lived process should live: here, not in the browser and not in a sidecar.
 *
 * **It listens on 127.0.0.1 only.** Nothing about the console may be reachable from the
 * network: run data embeds v1's man pages and specifications, which must not leave this Mac.
 *
 * The process registry is shared with Next's own module context through a `globalThis` symbol.
 * Next compiles server actions in a separate module graph, so without that the actions and
 * this file would each hold their own registry and a run started by one would be invisible to
 * the other.
 */
import { createServer, type IncomingMessage } from "node:http";
import type { Duplex } from "node:stream";
import next from "next";
import { WebSocketServer, type WebSocket } from "ws";
import { attach, get } from "./src/server/processes.js";

const HOST = "127.0.0.1";
const PORT = Number(process.env.CONSOLE_PORT ?? 4317);
const dev = process.env.NODE_ENV !== "production";

/** Where a page connects to watch a terminal. */
const TERMINAL_PATH = "/ws/terminal";

const app = next({ dev, hostname: HOST, port: PORT });
const handle = app.getRequestHandler();

await app.prepare();

const server = createServer((request, response) => {
  void handle(request, response);
});

/**
 * `noServer` because the upgrade is routed by hand: any path other than the terminal one is
 * refused rather than upgraded, so the only socket this server will open is the one it means
 * to.
 */
const terminals = new WebSocketServer({ noServer: true });

terminals.on("connection", (socket: WebSocket, request: IncomingMessage) => {
  const url = new URL(request.url ?? "/", `http://${HOST}:${PORT}`);
  const runId = url.searchParams.get("runId") ?? "";

  const send = (payload: unknown) => {
    if (socket.readyState === socket.OPEN) socket.send(JSON.stringify(payload));
  };

  const info = get(runId);
  if (!info) {
    send({ type: "error", message: `No live run named ${runId}. It may have already finished.` });
    socket.close();
    return;
  }

  const attachment = attach(
    runId,
    (data) => send({ type: "data", data }),
    (exitCode, state) => {
      // The socket stays open: the page should keep showing what the run printed.
      send({ type: "exit", exitCode, state });
    },
  );

  if (!attachment) {
    send({ type: "error", message: `Could not attach to ${runId}.` });
    socket.close();
    return;
  }

  // Everything the terminal has shown so far, then the live stream. This is what makes a
  // reload harmless: the page rebuilds its terminal from the backlog and carries on.
  send({
    type: "attached",
    backlog: attachment.backlog,
    info: {
      runId: attachment.info.runId,
      side: attachment.info.side,
      argv: attachment.info.argv,
      where: attachment.info.where,
      limaInstance: attachment.info.limaInstance,
      state: attachment.info.state,
      startedAt: attachment.info.startedAt,
      concurrentWith: attachment.info.concurrentWith,
    },
  });

  // A run can finish before anyone attaches — `caruca generate cat --max-count 1` takes a
  // couple of hundred milliseconds. The exit listener has already fired by then and will not
  // fire again, so a late joiner would sit showing "live" forever. Tell it straight away, and
  // leave the socket open so the output stays on screen.
  if (attachment.info.state !== "running") {
    send({
      type: "exit",
      exitCode: attachment.info.exitCode,
      state: attachment.info.state,
    });
  }

  // **Nothing a client sends reaches the process.** There is no path from the page into a
  // terminal's input, which is a requirement rather than an omission (§10). Messages are read
  // only so the socket can be closed cleanly.
  socket.on("message", () => {
    /* ignored on purpose */
  });

  socket.on("close", () => attachment.detach());
  socket.on("error", () => attachment.detach());
});

server.on("upgrade", (request: IncomingMessage, socket: Duplex, head: Buffer) => {
  const url = new URL(request.url ?? "/", `http://${HOST}:${PORT}`);

  if (url.pathname !== TERMINAL_PATH) {
    // Next's own development WebSocket (hot reload) must still work in dev.
    if (dev && url.pathname.startsWith("/_next")) return;
    socket.destroy();
    return;
  }

  terminals.handleUpgrade(request, socket, head, (socket_) => {
    terminals.emit("connection", socket_, request);
  });
});

server.listen(PORT, HOST, () => {
  console.log(`  caruca console  http://${HOST}:${PORT}   (terminals on ${TERMINAL_PATH})`);
});
