#!/usr/bin/env python3
# ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove
# caruca_v2 agent skill: Retrieve caruca run.
# Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0
# Noncommercial use only. Commercial use is prohibited.
# ATTRIBUTION-NOTICE:END
"""Ask v1 directly: what does its code say, and what does it actually emit?

A recorded score tells you that v2 diverged. It cannot tell you whether v2 was wrong or
v1's documentation was — and those call for opposite write-ups. This script closes that
gap by reading v1's implementation and re-running its enumeration at bounds you choose.

    v1_probe.py cat --spec                 v1's committed syntax specification
    v1_probe.py cat --generate             v1's enumeration at the recorded bounds
    v1_probe.py cat --generate --max-count 2
    v1_probe.py cat --vs-v2                v1 vs v2's recorded output, as sets
    v1_probe.py --source filtered_args     the code behind the enumeration bound
    v1_probe.py --explain-bounds           what --max-count actually counts

Only read-only v1 subcommands are ever run: `generate`, `generate --number`,
`syntax-spec --fetch`. Never `trace` or `annotate` — those execute commands and write into
v1's own `outputs/`, which is gitignored, so anything overwritten there is gone for good.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

import carucadata as cd

# Read-only v1 subcommands. Anything not on this list is refused rather than passed through:
# v1's `trace` and `annotate` execute real commands and write into a gitignored output tree.
SAFE_SUBCOMMANDS = {"generate", "syntax-spec", "oracle"}

# Passages in v1's source worth quoting by name, because they are where the questions that
# come up in this comparison actually get decided. Each is (file, regex for the region).
SOURCE_MAP = {
    "filtered_args": (
        "caruca/src/caruca/ir/syntax.py",
        r"def __filtered_args",
        "How --max-count picks which optional arguments survive. The selection is over "
        "every argument where is_optional() holds — Arity.OPTIONAL or ZERO_OR_MORE — which "
        "includes positionals, not just flags.",
    ),
    "to_concrete_string": (
        "caruca/src/caruca/ir/syntax.py",
        r"def to_concrete_string",
        "The enumeration itself: filtered arg sets crossed with each argument's syntax_variation.",
    ),
    "arity_range": (
        "caruca/src/caruca/ir/syntax.py",
        r"def _arity_range",
        "How an Arity becomes a repetition count. OPTIONAL is [0, 1]; ZERO_OR_MORE is "
        "0..max_repetition, which is what --max-arity sets.",
    ),
    "is_optional": (
        "caruca/src/caruca/ir/syntax.py",
        r"def is_optional",
        "The predicate --max-count selects on.",
    ),
    "cli_args": (
        "caruca/src/caruca/cli/__init__.py",
        r'"--max-arity"',
        "v1's own CLI flag definitions and their help text — the *documented* meaning of "
        "each bound, which is not always the enforced one.",
    ),
    "pclass": (
        "caruca/src/caruca/tracer/data.py",
        r"match no_effect, splittable:",
        "Where the parallelizability class is decided. Only three of the four enum members "
        "are reachable here — S (stateless), N (non-pure), E (side-effectful) — so v1 never "
        "emits `pure`. `S` needs `splittable`, which only split-input traces produce, so at "
        "the `simple` stdin/content default no command can be classified stateless at any "
        "--max-count. A parallelizability comparison made at the default therefore measures "
        "the trace configuration as much as the annotator.",
    ),
    "pclass_enum": (
        "caruca/src/caruca/annotator/pash.py",
        r"class Parallelizability",
        "The four class names themselves. `P = \"pure\"` is defined but never assigned by "
        "the annotator — see the `pclass` passage for where the assignment happens.",
    ),
}


def v1_bin() -> Path:
    root = cd.v1_root()
    exe = root / "caruca" / ".venv" / "bin" / "caruca"
    if not exe.exists():
        raise SystemExit(
            f"v1's venv is not at {exe}. The editable install is expected there "
            f"(see caruca_v2/CLAUDE.md, 'Running the baseline')."
        )
    return exe


def run_v1(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    if not args or args[0] not in SAFE_SUBCOMMANDS:
        raise SystemExit(
            f"refusing to run `caruca {args[0] if args else ''}`. This script runs only "
            f"read-only subcommands ({', '.join(sorted(SAFE_SUBCOMMANDS))}); `trace` and "
            f"`annotate` execute commands and write into v1's gitignored outputs/."
        )
    cmd = [str(v1_bin()), *args]
    print(f"$ {' '.join(shlex.quote(c) for c in cmd)}", file=sys.stderr)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


# --------------------------------------------------------------------------------------


def recorded_bounds(command: str) -> dict:
    """The bounds v2 was actually run at, so a re-run compares like with like."""
    rec = cd.load_record()
    for r in rec.for_command(command, "generate"):
        b = (r.checks.get("invocation_comparison") or {}).get("bounds")
        if b:
            return b
        if r.inputs.get("max_count") is not None:
            return {k: r.inputs.get(k) for k in
                    ("max_arity", "max_count", "skip", "stdin_variation", "content_variation")}
    return {}


def v2_invocations(command: str) -> list[str] | None:
    """v2's recorded invocation list for this command, if a stage-2 run wrote one."""
    rec = cd.load_record()
    for r in rec.for_command(command, "generate"):
        if not r.ok:
            continue
        for p in r.outputs():
            if p.name.endswith(".invocations.txt"):
                return [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]
    return None


def do_spec(command: str) -> int:
    root = cd.v1_root()
    p = root / "caruca" / "src" / "caruca" / "syntax_specs" / f"{command}.py"
    print(cd.rule(f"v1's committed syntax specification — {command}"))
    print(f"[{p}]")
    print("v1 is private and unlicensed: read this, do not copy it anywhere public.")
    print()
    if p.exists():
        print(p.read_text())
    else:
        print(f"no committed spec at {p}")
        print("Command registration is reflective and name-coupled: syntax_specs/<cmd>.py")
        print("must define <cmd>_syntax_spec. Nothing else registers a command.")
        return 1
    return 0


def do_generate(command: str, max_arity: int | None, max_count: int | None,
                number_only: bool, skip: str | None) -> int:
    b = recorded_bounds(command)
    ma = max_arity if max_arity is not None else b.get("max_arity", 1)
    mc = max_count if max_count is not None else b.get("max_count", 4)
    used_recorded = (max_arity is None and max_count is None and bool(b))

    args = ["generate", command, "--max-arity", str(ma), "--max-count", str(mc)]
    if skip:
        args += ["--skip", skip]
    if number_only:
        args.append("--number")

    print(cd.rule(f"v1 enumeration — {command}  (max-arity {ma}, max-count {mc})"))
    if used_recorded:
        print(f"Using the bounds v2 was recorded at: {json.dumps(b)}")
        print("Change them with --max-count / --max-arity to test what a different bound "
              "would have produced.")
    print()
    r = run_v1(args)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        return r.returncode
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if number_only:
        print(r.stdout.strip())
        return 0
    uniq = sorted(set(lines))
    print(f"{len(lines)} lines, {len(uniq)} distinct")
    print()
    for ln in uniq:
        print(ln)
    return 0


def _flag_count(invocation: str) -> int:
    return sum(1 for tok in invocation.split()[1:] if tok.startswith("-"))


def do_vs_v2(command: str, max_arity: int | None, max_count: int | None) -> int:
    """Set-diff v1's enumeration against v2's recorded output.

    The scorer already reports recall and precision; what this adds is the ability to move
    the bound and see the difference close or persist. If v2's surplus disappears when v1
    is re-run one notch looser, the divergence is about what the bound *means*, not about
    the model inventing invocations.
    """
    v2 = v2_invocations(command)
    if v2 is None:
        print(f"No recorded v2 invocation list for {command!r} "
              f"(needs a stage-2 run that wrote <cmd>.invocations.txt).")
        return 1
    b = recorded_bounds(command)
    ma = max_arity if max_arity is not None else b.get("max_arity", 1)
    mc = max_count if max_count is not None else b.get("max_count", 4)

    r = run_v1(["generate", command, "--max-arity", str(ma), "--max-count", str(mc)])
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode
    v1set = sorted({ln.strip() for ln in r.stdout.splitlines() if ln.strip()})
    v2set = sorted(set(v2))

    missing = [x for x in v1set if x not in set(v2set)]
    spurious = [x for x in v2set if x not in set(v1set)]

    print()
    print(cd.rule(f"{command}: v1 (max-count {mc}, max-arity {ma}) vs v2's recorded output"))
    print(f"v1 distinct      {len(v1set)}")
    print(f"v2 distinct      {len(v2set)}")
    print(f"in both          {len(set(v1set) & set(v2set))}")
    print(f"only in v1       {len(missing)}")
    print(f"only in v2       {len(spurious)}")
    print()
    print("NOTE: this is a raw string comparison. The recorded score uses a semantic")
    print("equivalence (options as a multiset, '=' and short bundles normalized), so its")
    print("matched count can be higher. Use this to move the bound, not to restate the score.")

    if missing:
        print()
        print(f"--- only in v1 ({len(missing)}) ---")
        for x in missing[:60]:
            print(f"  {x}")
        if len(missing) > 60:
            print(f"  … {len(missing) - 60} more")
    if spurious:
        print()
        print(f"--- only in v2 ({len(spurious)}) ---")
        for x in spurious[:60]:
            print(f"  {x}")
        if len(spurious) > 60:
            print(f"  … {len(spurious) - 60} more")

    # The flag-count histogram is the tell for a bound disagreement: if v2's surplus all
    # sits at one flag plus an operand while v1's stops at one element total, the two are
    # counting different things.
    print()
    print("flag counts (operands excluded), which is where a bound disagreement shows:")
    for label, items in (("v1", v1set), ("v2", v2set)):
        hist: dict[int, int] = {}
        for x in items:
            hist[_flag_count(x)] = hist.get(_flag_count(x), 0) + 1
        print(f"  {label}: " + ", ".join(f"{k} flag(s): {v}" for k, v in sorted(hist.items())))
    return 0


def do_source(key: str | None) -> int:
    root = cd.v1_root()
    if not key:
        print(cd.rule("passages of v1 this skill knows how to find"))
        for k, (f, _, why) in SOURCE_MAP.items():
            print(f"\n{k}\n  {f}\n  {why}")
        print("\nAnything else: grep v1's tree directly at " + str(root))
        return 0
    if key not in SOURCE_MAP:
        print(f"unknown passage {key!r}. Known: {', '.join(SOURCE_MAP)}", file=sys.stderr)
        return 2
    rel, pattern, why = SOURCE_MAP[key]
    p = root / rel
    if not p.exists():
        print(f"not found: {p}", file=sys.stderr)
        return 1
    text = p.read_text()
    m = re.search(pattern, text)
    print(cd.rule(f"v1 · {rel} · {key}"))
    print(why)
    print(f"[{p}]  v1 is private and unlicensed: read it, do not copy it anywhere public.")
    print()
    if not m:
        print(f"(pattern {pattern!r} did not match; the file may have moved on)")
        return 1
    lines = text.splitlines()
    start_line = text[: m.start()].count("\n")
    lo = max(0, start_line - 3)
    hi = min(len(lines), start_line + 45)
    for i in range(lo, hi):
        print(f"{i + 1:5}  {lines[i]}")
    return 0


EXPLAIN_BOUNDS = """\
What `--max-count` counts in v1, and why it matters for stage 2
───────────────────────────────────────────────────────────────

v1's CLI help says:
    --max-count   "The maximum number of optional flags to use for a single invocation"

v1's code (ir/syntax.py::__filtered_args) selects over every argument where
`is_optional()` holds — `Arity.OPTIONAL` or `Arity.ZERO_OR_MORE` — across all argument
positions. That set includes **positional operands**, not just flags.

Consequence: for any command whose file operand is optional (the DSL default), an operand
consumes one of the slots the help text reserves for flags. At `--max-count 1`, v1 emits a
flag *or* an operand, never both — `cat -n relpath_1` is simply not in its enumeration.
Where the operand is *mandatory* (`rm`, `tee`), it must always appear and does not consume
the budget, so flag-plus-operand forms do appear.

v2's prompt (prompts/generate/user.md) repeats v1's *help text*:
    "At most {max_count} optional flags may be combined in a single invocation."

So on a command with an optional operand, v2 and v1 are obeying different rules, and v2's
"spurious" invocations are the prompt's wording rather than a model error.

The paper sides with the prompt. §4.1 counts "flags and options" per invocation and §4.2
lists positional values as a *separate* axis from flag combinations — so a positional is
not supposed to consume the flag budget.

Before calling stage-2 surplus a model failure, check three things:
  1. Is this command's operand optional or mandatory?   v1_probe.py CMD --spec
  2. Does v1 emit the surplus one notch looser?         v1_probe.py CMD --vs-v2 --max-count 2
  3. What did the prompt actually say?                  caruca_run.py CMD -s 2 -v prompt

Documented in: ai_docs/analysis/v1_v2_parity_study.md §3.2 (which attributes the cause to
v2), ai_docs/tasks/011_v2_improvement_program.md (which corrects that attribution — the
current view), and ai_docs/analysis/white_paper_addendum.md (which raises it with the
paper's authors). Cite 011.
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("command", nargs="?", help="a unix command, e.g. cat")
    ap.add_argument("--spec", action="store_true", help="v1's committed syntax specification")
    ap.add_argument("--generate", action="store_true", help="re-run v1's enumeration")
    ap.add_argument("--number", action="store_true", help="with --generate, count only")
    ap.add_argument("--vs-v2", action="store_true", help="set-diff v1 against v2's recorded output")
    ap.add_argument("--max-arity", type=int, default=None)
    ap.add_argument("--max-count", type=int, default=None)
    ap.add_argument("--skip", default=None)
    ap.add_argument("--source", nargs="?", const="", metavar="PASSAGE",
                    help="quote a passage of v1's source; omit the value to list them")
    ap.add_argument("--explain-bounds", action="store_true",
                    help="what --max-count actually counts, and why stage 2 diverges")
    args = ap.parse_args(argv)

    if args.explain_bounds:
        print(EXPLAIN_BOUNDS)
        return 0
    if args.source is not None:
        return do_source(args.source or None)

    if not args.command:
        ap.print_help()
        return 0

    try:
        cd.v1_root()
    except cd.RepoNotFound as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    rc = 0
    if args.spec:
        rc |= do_spec(args.command)
    if args.generate or args.number:
        rc |= do_generate(args.command, args.max_arity, args.max_count, args.number, args.skip)
    if args.vs_v2:
        rc |= do_vs_v2(args.command, args.max_arity, args.max_count)
    if not (args.spec or args.generate or args.number or args.vs_v2):
        rc |= do_spec(args.command)
        print()
        rc |= do_generate(args.command, args.max_arity, args.max_count, False, args.skip)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
