/**
 * Records one real terminal session, for the tests that exercise replay.
 *
 * Runs a genuinely free v1 command - `caruca generate cat --max-count 1` executes nothing and
 * calls no model - through a pseudo-terminal and writes an asciicast beside the tests. The
 * point is that the replay path is tested against terminal output a real program actually
 * produced, including whatever escape sequences and line endings it really emits, rather than
 * against a string someone typed into a fixture.
 *
 * Re-record with: node scripts/record-sample.mjs
 */
import { spawn } from "node-pty";
import { existsSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, "..", "tests", "fixtures", "v1-generate-cat.cast");

const v1Root = process.env.CARUCA_V1_ROOT ?? join(process.env.HOME, "dev", "stevens", "caruca");
const cwd = join(v1Root, "caruca");
const bin = join(cwd, ".venv", "bin", "caruca");

if (!existsSync(bin)) {
  console.error(`v1 is not installed at ${bin}. Set CARUCA_V1_ROOT.`);
  process.exit(1);
}

const COLS = 117;
const ROWS = 30;
const argv = ["generate", "cat", "--max-count", "1"];

const started = Date.now();
const lines = [
  JSON.stringify({
    version: 2,
    width: COLS,
    height: ROWS,
    timestamp: Math.floor(started / 1000),
    command: `${bin} ${argv.join(" ")}`,
    caruca: { side: "v1", runId: "sample", host: "mac" },
  }),
];

const term = spawn(bin, argv, {
  name: "xterm-256color",
  cols: COLS,
  rows: ROWS,
  cwd,
  env: process.env,
});

term.onData((data) => {
  lines.push(JSON.stringify([(Date.now() - started) / 1000, "o", data]));
});

term.onExit(({ exitCode }) => {
  writeFileSync(OUT, `${lines.join("\n")}\n`);
  console.log(`exit ${exitCode} · ${lines.length - 1} events · ${OUT}`);
});
