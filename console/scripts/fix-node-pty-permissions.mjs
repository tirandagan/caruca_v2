/**
 * Makes node-pty's `spawn-helper` executable.
 *
 * Phase 0(e) of task 010. node-pty ships a prebuilt `darwin-arm64` binary, so nothing is
 * compiled here — but npm blocks package install scripts by default, and one of the scripts it
 * blocks is the one that chmods `spawn-helper`. Left at 0644, every single pty spawn fails with
 * `Error: posix_spawnp failed.`, which names neither the file nor the permission bit. This runs
 * from our own package, where our own scripts are allowed, so the trap cannot reappear.
 *
 * No-op until node-pty is installed (Phase 5 brings it in), and never fatal: a console that
 * cannot spawn terminals must still start, because replay does not need them.
 */
import { chmodSync, existsSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const HELPER_RELATIVE = [
  ["build", "Release", "spawn-helper"],
  ["prebuilds", `${process.platform}-${process.arch}`, "spawn-helper"],
];

function nodePtyRoot() {
  try {
    const require = createRequire(import.meta.url);
    return dirname(require.resolve("node-pty/package.json"));
  } catch {
    return null;
  }
}

const root = nodePtyRoot();
if (!root) {
  console.log("node-pty not installed yet - nothing to fix.");
  process.exit(0);
}

let fixed = 0;
for (const parts of HELPER_RELATIVE) {
  const helper = join(root, ...parts);
  if (!existsSync(helper)) continue;
  const mode = statSync(helper).mode & 0o777;
  if (mode & 0o111) continue;
  chmodSync(helper, 0o755);
  console.log(`made executable (was ${mode.toString(8)}): ${helper}`);
  fixed += 1;
}

if (fixed === 0) console.log("node-pty spawn-helper already executable.");
