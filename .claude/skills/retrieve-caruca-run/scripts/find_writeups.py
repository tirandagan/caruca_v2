#!/usr/bin/env python3
# ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove
# caruca_v2 agent skill: Retrieve caruca run.
# Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0
# Noncommercial use only. Commercial use is prohibited.
# ATTRIBUTION-NOTICE:END
"""Find what has already been written about a command or a topic — and what was retracted.

This project's analysis documents correct each other. The parity study's §3.2 blames v2 for
the stage-2 bound divergence; task 011 later shows the cause was the prompt's wording and
says so explicitly. Both files are on disk, neither is deleted, and a search that returns
them as equal peers will get the attribution backwards.

So this does two things a plain grep does not: it reports the enclosing heading for every
hit, so you can see what section a claim sits in, and it flags documents that carry
correction language, so you know to read the later one before citing the earlier one.

    find_writeups.py cat                 everything mentioning cat
    find_writeups.py --topic max_count   a topic across all documents
    find_writeups.py cat --topic prompt
    find_writeups.py --corrections       every retraction in the document set

Verify against the artifacts before repeating any of it: `caruca_run.py` is the record,
these are interpretations of it, and some are superseded.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import carucadata as cd

# Phrases that mean "an earlier claim in this project was withdrawn or amended". Finding one
# is not a defect in the document — this project corrects itself in writing on purpose — but
# it does mean the surrounding claim has a history worth reading before it is cited.
CORRECTION_MARKERS = (
    "corrected", "correction", "superseded", "supersedes", "misattribut",
    "that was wrong", "an earlier version", "retract", "inverts the finding",
    "was mine", "errors were mine", "overstates",
)

SEARCH_DIRS = (
    ("ai_docs/analysis", "analysis — findings produced by this project"),
    ("ai_docs/tasks", "tasks — the working plans, often holding the current view"),
    ("memory", "memory — cross-session notes"),
    ("ai_docs/prep", "prep — project planning"),
)

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")


def headings_index(lines: list[str]) -> list[tuple[int, str]]:
    """(line_number, heading trail) for every line, so a hit can name its section.

    Fenced code blocks are skipped, because these documents quote shell and Python freely
    and a `# comment` inside a fence is not a section. One such line in
    `v2_fidelity_to_v1.md` was otherwise being read as the document's top-level heading.
    """
    stack: list[tuple[int, str]] = []
    out: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append((i, " › ".join(t for _, t in stack)))
            continue
        m = None if in_fence else HEADING.match(line)
        if m:
            level = len(m.group(1))
            stack = [s for s in stack if s[0] < level]
            stack.append((level, m.group(2).strip()))
        out.append((i, " › ".join(t for _, t in stack)))
    return out


def _norm(s: str) -> str:
    """Fold case and treat `-` and `_` alike.

    These documents write the same knob as `max_count`, `max-count` and `--max-count`
    depending on whether they are quoting the Python, the ledger key or the CLI. Someone
    searching for one means all three.
    """
    return s.lower().replace("-", "_")


def scan(root: Path, term: str, context: int, whole_word: bool = False) -> list[dict]:
    """Every line matching `term`, with the heading it sits under.

    `whole_word` matters more than it looks: a command name like `cat` or `wc` is a
    substring of `specification`, `indicate` and `switch`, so a plain substring search for
    a three-letter command returns mostly noise. Topics (`max_count`) stay substring, since
    they are written several ways.
    """
    hits: list[dict] = []
    needle = _norm(term)
    pat = re.compile(rf"(?<![a-z0-9_]){re.escape(needle)}(?![a-z0-9_])") if whole_word else None
    for rel, _ in SEARCH_DIRS:
        d = root / rel
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            try:
                text = p.read_text()
            except (OSError, UnicodeDecodeError):
                continue
            lines = text.splitlines()
            idx = headings_index(lines)
            corr_lines = [j + 1 for j, ln in enumerate(lines)
                          if any(m in ln.lower() for m in CORRECTION_MARKERS)]
            for i, line in enumerate(lines):
                hay = _norm(line)
                if not (pat.search(hay) if pat else needle in hay):
                    continue
                hits.append({
                    "path": p,
                    "rel": p.relative_to(root),
                    "line": i + 1,
                    "heading": idx[i][1],
                    "text": line.strip(),
                    "context": lines[max(0, i - context): i + context + 1] if context else [],
                    "corrections": corr_lines,
                })
    return hits


def do_corrections(root: Path) -> int:
    print(cd.rule("documents carrying correction or retraction language"))
    print("A marker here means a claim in this file was amended. Read the amendment before")
    print("citing the original — this project corrects itself in writing rather than by")
    print("deleting, so both versions are on disk.")
    print()
    found = False
    for rel, _ in SEARCH_DIRS:
        d = root / rel
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            try:
                lines = p.read_text().splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            idx = headings_index(lines)
            marks = [(i + 1, idx[i][1], ln.strip()) for i, ln in enumerate(lines)
                     if any(m in ln.lower() for m in CORRECTION_MARKERS)]
            if not marks:
                continue
            found = True
            print(f"\n{p.relative_to(root)}")
            for ln, head, txt in marks[:12]:
                print(f"  :{ln}  [{head or '—'}]")
                print(f"      {cd.truncate(txt, 150)}")
            if len(marks) > 12:
                print(f"  … {len(marks) - 12} more")
    if not found:
        print("none found")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("command", nargs="?", help="a unix command, e.g. cat")
    ap.add_argument("-t", "--topic", action="append", default=None,
                    help="a term to search for, e.g. max_count. Repeatable.")
    ap.add_argument("-C", "--context", type=int, default=0, help="lines of context per hit")
    ap.add_argument("--corrections", action="store_true",
                    help="list every retraction in the document set and stop")
    ap.add_argument("--limit", type=int, default=8, help="max hits shown per file")
    args = ap.parse_args(argv)

    try:
        root = cd.repo_root()
    except cd.RepoNotFound as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.corrections:
        return do_corrections(root)

    terms = list(args.topic or [])
    if args.command:
        terms.insert(0, args.command)
    if not terms:
        ap.print_help()
        return 0

    # A file must contain every term, so `cat --topic max_count` narrows rather than unions.
    # What gets *shown* is the topic hits, not the command hits: in a document about `cat`
    # the command name appears on every other line, while the topic is the thing asked about.
    topics = list(args.topic or [])
    per_term = [scan(root, t, args.context, whole_word=(t == args.command and not topics))
                for t in terms]
    if args.command and topics:
        per_term[0] = scan(root, args.command, args.context, whole_word=True)

    files_per_term = [{h["path"] for h in hs} for hs in per_term]
    common = set.intersection(*files_per_term) if files_per_term else set()
    # Show the narrowest term's hits: the last topic if there is one, else the command's.
    show = per_term[-1] if topics else per_term[0]
    hits = [h for h in show if h["path"] in common]

    if not hits:
        print(f"nothing written about {' + '.join(terms)} in "
              f"{', '.join(d for d, _ in SEARCH_DIRS)}.")
        print("The artifacts are still there: caruca_run.py "
              f"{args.command or '<command>'}")
        return 0

    print(cd.rule(f"written up: {' + '.join(terms)}"))
    by_file: dict[Path, list[dict]] = {}
    for h in hits:
        by_file.setdefault(h["path"], []).append(h)

    for p, hs in sorted(by_file.items(), key=lambda kv: str(kv[0])):
        corr = hs[0]["corrections"]
        flag = ""
        if corr:
            # Point at the amendment nearest the first hit rather than just saying one
            # exists. A warning that fires on every file teaches the reader to skip it;
            # a line number is something to go and read.
            near = min(corr, key=lambda c: abs(c - hs[0]["line"]))
            flag = f"   ⚠ {len(corr)} correction note(s); nearest to this hit at :{near}"
        print(f"\n{hs[0]['rel']}{flag}")
        for h in hs[: args.limit]:
            print(f"  :{h['line']}  [{h['heading'] or '—'}]")
            print(f"      {cd.truncate(h['text'], 160)}")
            for c in h["context"]:
                print(f"      | {cd.truncate(c.strip(), 150)}")
        if len(hs) > args.limit:
            print(f"  … {len(hs) - args.limit} more hits in this file")

    print()
    print(cd.rule())
    print("These are interpretations. Check them against the record before repeating them:")
    print(f"  caruca_run.py {args.command or '<command>'} -v numbers")
    print("A ⚠ file has been amended somewhere; `--corrections` lists every amendment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
