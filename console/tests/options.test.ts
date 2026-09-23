/**
 * The option table against each CLI's own `--help`.
 *
 * The first of §9's three Phase 4 tests: "the option table against each CLI's `--help`, so the
 * console cannot silently drift from the CLIs". It is checked in both directions — a flag the
 * table invents and a flag the CLI adds are both failures — because either one produces a form
 * that quietly does the wrong thing.
 *
 * It runs the real programs. Where a CLI is not installed the test says so and skips, rather
 * than passing on a machine that could not have checked anything.
 */
import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { SUBCOMMANDS, sharedOptions, type Side } from "../src/data/options.js";
import { repoPaths, v1Root } from "../src/data/paths.js";

function v1Bin(): string | null {
  try {
    const bin = join(v1Root(), "caruca", ".venv", "bin", "caruca");
    return existsSync(bin) ? bin : null;
  } catch {
    return null;
  }
}

function v2Bin(): string | null {
  const bin = join(repoPaths().root, ".venv", "bin", "caruca-v2");
  return existsSync(bin) ? bin : null;
}

function binFor(side: Side): string | null {
  return side === "v1" ? v1Bin() : v2Bin();
}

/**
 * Every long flag the CLI *declares* for this subcommand.
 *
 * Only declarations count, and argparse prints those at the start of an indented line in the
 * options section. A flag merely *mentioned* in help prose is not an option: v1's `--skip`
 * says its default is "--version,--help,--interactive", and v2's `--skip` uses `--foo,--bar`
 * as an example. Scanning the whole text for `--word` picks all five up and reports the table
 * as missing flags that do not exist.
 */
function flagsFromHelp(bin: string, subcommand: string, cwd: string): Set<string> {
  const help = execFileSync(bin, [...subcommand.split(" "), "--help"], {
    cwd,
    encoding: "utf8",
    env: { ...process.env, NO_COLOR: "1", COLUMNS: "200" },
  });

  const flags = new Set<string>();
  let inOptions = false;

  for (const line of help.split("\n")) {
    if (/^\s*(options|optional arguments):\s*$/i.test(line)) {
      inOptions = true;
      continue;
    }
    // A new unindented section heading ends the options block.
    if (inOptions && /^\S/.test(line) && line.trim().length > 0) break;
    if (!inOptions) continue;

    // `  --flag`, `  --flag VALUE`, `  -p N, --parallel N`, `  --parallel N, -p N`
    const declaration = /^\s{1,4}(-[a-zA-Z](?: [A-Z_]+)?, )?(--[a-z][a-z0-9-]*)/.exec(line);
    if (declaration?.[2]) flags.add(declaration[2]);
  }

  flags.delete("--help");
  return flags;
}

const v1Available = v1Bin() !== null;
const v2Available = v2Bin() !== null;

describe.skipIf(!v1Available || !v2Available)("the option table matches each CLI", () => {
  for (const entry of SUBCOMMANDS) {
    const bin = binFor(entry.side);
    if (!bin) continue;

    const cwd =
      entry.side === "v1" ? join(v1Root(), "caruca") : repoPaths().root;

    it(`${entry.side} ${entry.name}: every flag in the table exists in --help`, () => {
      const actual = flagsFromHelp(bin, entry.name, cwd);
      const invented = entry.options
        .map((option) => option.flag)
        .filter((flag) => !actual.has(flag));
      expect(invented, `not in ${entry.side} ${entry.name} --help`).toEqual([]);
    });

    it(`${entry.side} ${entry.name}: every flag in --help is in the table`, () => {
      const actual = flagsFromHelp(bin, entry.name, cwd);
      const known = new Set(entry.options.map((option) => option.flag));
      const missing = [...actual].filter((flag) => !known.has(flag));
      expect(missing, `present in ${entry.side} ${entry.name} --help but unknown here`).toEqual(
        [],
      );
    });
  }
});

describe("the table's own shape", () => {
  it("gives every option help text", () => {
    for (const entry of SUBCOMMANDS) {
      for (const option of entry.options) {
        expect(option.help.length, `${entry.side} ${entry.name} ${option.flag}`).toBeGreaterThan(5);
      }
    }
  });

  it("never lists the same flag twice in one subcommand", () => {
    for (const entry of SUBCOMMANDS) {
      const flags = entry.options.map((option) => option.flag);
      expect(new Set(flags).size, `${entry.side} ${entry.name}`).toBe(flags.length);
    }
  });

  it("names the five generation options that are set once for both sides", () => {
    // §6.1: different limits on each side would measure the limits rather than the systems.
    expect(sharedOptions().map((option) => option.flag).sort()).toEqual([
      "--content",
      "--max-arity",
      "--max-count",
      "--skip",
      "--stdin",
    ]);
  });

  it("carries a caveat on every option that does not do what its help says", () => {
    // Three of v1's options are documented in a way that misleads; each is flagged.
    const v1Generate = SUBCOMMANDS.find((e) => e.side === "v1" && e.name === "generate")!;
    expect(v1Generate.options.find((o) => o.flag === "--number")?.caveat).toContain("crashes");
    expect(v1Generate.options.find((o) => o.flag === "--output")?.caveat).toContain("never used");

    const v1Trace = SUBCOMMANDS.find((e) => e.side === "v1" && e.name === "trace")!;
    expect(v1Trace.options.find((o) => o.flag === "--output")?.caveat).toContain("FILE");
  });

  it("requires a model and a temperature on every v2 stage", () => {
    for (const entry of SUBCOMMANDS.filter((e) => e.side === "v2" && e.stage)) {
      const required = entry.options.filter((option) => option.required).map((o) => o.flag);
      expect(required.sort(), entry.name).toEqual(["--model", "--temperature"]);
    }
  });
});
