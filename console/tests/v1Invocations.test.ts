/**
 * v1's argument lists against the forms §3 records.
 *
 * The second and third of §9's Phase 4 tests. Decision 7 says a v1 run started from the
 * console must be the same kind of run the measurements came from, and that only means
 * anything if it is checked — so each form below is compared against the table in §3, and the
 * output guard is tested against the paths it exists to refuse.
 */
import { describe, expect, it } from "vitest";
import { join } from "node:path";
import {
  LIMA_V1_CARUCA,
  UnsafeV1OutputError,
  VENV_DEFAULT,
  VENV_LLM,
  displayInvocation,
  refuseUnsafeOutput,
  v1Annotate,
  v1Cwd,
  v1Generate,
  v1SyntaxSpec,
  v1Trace,
} from "../src/data/v1Invocations.js";
import { v1ProtectedOutputs, v1Root, repoPaths } from "../src/data/paths.js";

const RUN_DIR = join(repoPaths().v1Runs, "2026-09-22T120000Z_cat_test1234");

describe("the forms §3 records", () => {
  it("generate runs on the Mac from v1's own venv, in v1's package directory", () => {
    // §3: `$CARUCA_V1_ROOT/caruca/.venv/bin/caruca generate CMD …`, from `$CARUCA_V1_ROOT/caruca`
    const invocation = v1Generate("cat", { maxCount: 1 });
    expect(invocation.where).toBe("mac");
    expect(invocation.venv).toBe(VENV_DEFAULT);
    expect(invocation.cwd).toBe(v1Cwd());
    expect(invocation.argv[0]).toMatch(/\/caruca\/\.venv\/bin\/caruca$/);
    expect(invocation.argv.slice(1)).toEqual(["generate", "cat", "--max-count", "1"]);
  });

  it("generate is never given --output, because v1 accepts it and never uses it", () => {
    const invocation = v1Generate("cat", { maxCount: 1 });
    expect(invocation.argv).not.toContain("--output");
    expect(invocation.outputPath).toBeNull();
  });

  it("trace runs inside the Lima VM, with an explicit output file", () => {
    // §3 writes this as `limactl shell caruca -- ~/caruca-venv/bin/caruca trace CMD …`, but
    // that form does not run: `limactl` quotes each argument, so the guest's bash gets a
    // literal `~` and reports "No such file or directory". Expanding it here would give the
    // Mac's home, and v1's virtualenv is under the guest's. The absolute guest path is used
    // instead, and the invocation is otherwise identical.
    const out = join(RUN_DIR, "cat.json");
    const invocation = v1Trace("cat", out, { maxCount: 1 });
    expect(invocation.where).toBe("lima");
    expect(invocation.limaInstance).toBe("caruca");
    expect(invocation.argv.slice(0, 4)).toEqual(["limactl", "shell", "caruca", "--"]);
    expect(invocation.argv[4]).toMatch(/^\/.*\/caruca-venv\/bin\/caruca$/);
    expect(invocation.argv[4]).not.toContain("~");
    expect(invocation.argv.slice(5, 7)).toEqual(["trace", "cat"]);
    expect(invocation.argv).toContain("--output");
    expect(invocation.outputPath).toBe(out);
  });

  it("resolves v1's path from the guest, not from the Mac's home", () => {
    // The two differ: the guest's home is not /Users/<name>.
    const invocation = v1Trace("cat", join(RUN_DIR, "cat.json"));
    expect(invocation.argv[4]).not.toContain(process.env.HOME ?? "/Users");
  });

  it("trace passes no isolation variable, so v1 uses its own default", () => {
    // The parity study ran under v1's default (`CARUCA_ISOLATION_METHOD` unset, meaning `try`).
    // Setting it would be running a different v1.
    const invocation = v1Trace("cat", join(RUN_DIR, "cat.json"));
    expect(invocation.argv.join(" ")).not.toContain("CARUCA_ISOLATION_METHOD");
  });

  it("trace --length-only asks for a count and writes nothing", () => {
    const invocation = v1Trace("mkdir", join(RUN_DIR, "x.json"), {}, { lengthOnly: true });
    expect(invocation.argv).toContain("--length-only");
    expect(invocation.argv).not.toContain("--output");
    expect(invocation.outputPath).toBeNull();
  });

  it("annotate runs in the VM through sh -lc, the form v1.py already uses", () => {
    // §3: `limactl shell caruca -- sh -lc "~/caruca-venv/bin/caruca annotate FORMAT CMD --input FILE"`
    const input = join(RUN_DIR, "cat.json");
    const invocation = v1Annotate("pash", "cat", input);
    expect(invocation.usesShell).toBe(true);
    expect(invocation.argv.slice(0, 6)).toEqual([
      "limactl",
      "shell",
      "caruca",
      "--",
      "sh",
      "-lc",
    ]);
    expect(invocation.argv[6]).toContain(`${LIMA_V1_CARUCA} annotate pash cat --input `);
    expect(invocation.argv[6]).toContain(input);
    // Exactly seven elements: the shell string is one argument, not several.
    expect(invocation.argv).toHaveLength(7);
  });

  it("syntax-spec uses .venv-llm, because the plain venv cannot import it", () => {
    const invocation = v1SyntaxSpec("cat");
    expect(invocation.venv).toBe(VENV_LLM);
    expect(invocation.argv[0]).toContain("/.venv-llm/bin/caruca");
  });

  it("syntax-spec --fetch reads the committed spec and calls no model", () => {
    const invocation = v1SyntaxSpec("cat", { fetch: true });
    expect(invocation.argv).toContain("--fetch");
    expect(invocation.venv).toBe(VENV_DEFAULT);
  });

  it("every form runs from v1's package directory", () => {
    const forms = [
      v1Generate("cat"),
      v1Trace("cat", join(RUN_DIR, "cat.json")),
      v1Annotate("pash", "cat", join(RUN_DIR, "cat.json")),
      v1SyntaxSpec("cat"),
    ];
    for (const form of forms) expect(form.cwd).toBe(v1Cwd());
  });

  it("no form is a shell string except the one that has to be", () => {
    expect(v1Generate("cat").usesShell).toBe(false);
    expect(v1Trace("cat", join(RUN_DIR, "c.json")).usesShell).toBe(false);
    expect(v1SyntaxSpec("cat").usesShell).toBe(false);
    expect(v1Annotate("pash", "cat", join(RUN_DIR, "c.json")).usesShell).toBe(true);
  });

  it("produces a command line that can be pasted into a terminal", () => {
    const line = displayInvocation(v1Trace("cat", join(RUN_DIR, "cat.json"), { maxCount: 1 }));
    expect(line.startsWith("limactl shell caruca -- ")).toBe(true);
    expect(line).toContain("--max-count 1");
  });
});

describe("the guard on v1's output paths", () => {
  it("refuses v1's own outputs directory, which git cannot restore", () => {
    expect(() => refuseUnsafeOutput(join(v1ProtectedOutputs(), "cat.json"))).toThrow(
      UnsafeV1OutputError,
    );
    expect(() => refuseUnsafeOutput(v1ProtectedOutputs())).toThrow(UnsafeV1OutputError);
  });

  it("refuses anywhere else in v1's checkout", () => {
    expect(() => refuseUnsafeOutput(join(v1Root(), "caruca", "save", "ls.json"))).toThrow(
      UnsafeV1OutputError,
    );
  });

  it("refuses a path that escapes into the checkout with ..", () => {
    const sneaky = join(repoPaths().v1Runs, "..", "..", "..", "caruca", "caruca", "outputs", "x");
    expect(() => refuseUnsafeOutput(sneaky)).toThrow(UnsafeV1OutputError);
  });

  it("distinguishes a prefix match from a real containment", () => {
    // `outputs-backup` starts with the same characters as `outputs` but is not inside it. It
    // is still refused — because it is inside v1's checkout — and the message must say so,
    // otherwise a `startsWith` bug would look like a passing test.
    const sibling = `${v1ProtectedOutputs()}-backup/cat.json`;
    expect(() => refuseUnsafeOutput(sibling)).toThrow(/inside v1's checkout/);
    expect(() => refuseUnsafeOutput(join(v1ProtectedOutputs(), "cat.json"))).toThrow(
      /own outputs directory/,
    );
  });

  it("allows a path that is outside the checkout entirely", () => {
    expect(refuseUnsafeOutput("/tmp/somewhere/cat.json")).toBe("/tmp/somewhere/cat.json");
  });

  it("allows a path inside the run's own folder", () => {
    const allowed = join(RUN_DIR, "cat.json");
    expect(refuseUnsafeOutput(allowed)).toBe(allowed);
  });

  it("refuses at construction, so an unsafe form cannot be built at all", () => {
    expect(() => v1Trace("cat", join(v1ProtectedOutputs(), "cat.json"))).toThrow(
      UnsafeV1OutputError,
    );
    expect(() => v1Annotate("pash", "cat", join(v1ProtectedOutputs(), "cat.json"))).toThrow(
      UnsafeV1OutputError,
    );
  });
});
