#!/usr/bin/env python
"""Write a readable side-by-side of what v1 and v2 each produced, per command.

The parity study reports aggregates. The underlying outputs are all on disk, but they are
spread across 163 run directories, 27 KB manifests, and four different locations on the v1
side. This renders one Markdown file per command showing, per stage, **what v1 emitted, what
v2 emitted, and the specific lines that differ** — the evidence behind every number in
`ai_docs/analysis/v1_v2_parity_study.md`.

Output goes to `eval/parity_diffs/`, which is gitignored on purpose: these files quote v1's
specifications, invocations and annotations verbatim, and v1 is private and unlicensed. They
are for reading locally, not for committing or sharing.

    python scripts/parity_diff.py            # every command in the study
    python scripts/parity_diff.py wc grep    # just these
    python scripts/parity_diff.py --stdout wc
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from caruca_v2 import v1  # noqa: E402
from caruca_v2.harness import annotation as ann  # noqa: E402
from caruca_v2.harness import score as score_module  # noqa: E402
from caruca_v2.harness import trace_recovery as tr  # noqa: E402

COMMANDS = ["cat", "pwd", "rm", "sha256sum", "tac", "tail", "tee", "uniq", "wc"]
CAMPAIGNS = {
    "syntax_spec": "p1_syntax_spec",
    "generate": "p1_generate",
    "trace": "p1_trace",
    "annotate": "p1_annotate",
}
OUT = REPO / "eval" / "parity_diffs"
LIMIT = 40  # lines shown per side before truncating; the full files are always on disk


def cells(stage: str, command: str) -> list[dict]:
    """Every ledger row for one command in one stage campaign."""
    path = REPO / "eval" / "campaigns" / CAMPAIGNS[stage] / "ledger.jsonl"
    if not path.is_file():
        return []
    return [
        row
        for row in (json.loads(line) for line in path.read_text().splitlines() if line.strip())
        if row.get("command") == command
    ]


def fence(lines, lang: str = "text", limit: int = LIMIT) -> str:
    shown = list(lines)[:limit]
    body = "\n".join(str(x) for x in shown)
    more = f"\n… {len(list(lines)) - limit} more" if len(list(lines)) > limit else ""
    return f"```{lang}\n{body}{more}\n```"


def side_by_side(title_a: str, a: list[str], title_b: str, b: list[str]) -> str:
    """A unified diff of two line lists, labelled."""
    diff = list(difflib.unified_diff(a, b, fromfile=title_a, tofile=title_b, lineterm="", n=1))
    if not diff:
        return "_identical_\n"
    return fence(diff, "diff", limit=80)


def stage1(command: str) -> str:
    """v1's own LLM specification versus v2's, both against v1's committed ground truth."""
    out = ["## Stage 1 — syntax specification\n"]
    rows = cells("syntax_spec", command)
    if not rows:
        return "".join(out) + "_no cells_\n\n"

    run = Path(rows[0]["run_dir"])
    v2_spec = run / f"{v1.slug(command)}.py"
    v1_spec = v1.generated_spec_path(command)
    truth = v1.syntax_spec_path(command)

    out.append(f"* ground truth: `{truth}`\n")
    out.append(f"* v1's own LLM output: `{v1_spec}`\n")
    out.append(f"* v2's output: `{v2_spec}`\n\n")

    for label, path in (("v1 LLM output", v1_spec), ("v2 output", v2_spec)):
        if not path.is_file():
            out.append(f"### {label}\n_missing_\n\n")
            continue
        record = score_module.score_spec(command, path, reference=score_module.REFERENCE_V1_SPECS)
        counts, agree = record.get("counts", {}), record.get("agreement", {})
        out.append(
            f"### {label} — scored against ground truth\n\n"
            f"* matched {counts.get('matched')} of {counts.get('reference_flags')} "
            f"reference flags; missing {counts.get('missing')}, spurious {counts.get('spurious')}\n"
            f"* fully agreeing arguments: {agree.get('fully_agreeing')} of {counts.get('matched')} "
            f"(F1 {record.get('f1'):.3f}, exact {record.get('exact_argument_rate'):.3f})\n"
        )
        for key, name in (("missing_surfaces", "missing"), ("spurious_surfaces", "spurious")):
            surfaces = record.get(key) or []
            if surfaces:
                out.append(f"* {name}: {', '.join('/'.join(s) for s in surfaces)}\n")
        out.append("\n")

    if v1_spec.is_file() and v2_spec.is_file():
        out.append("### v1's LLM output vs v2's, line by line\n\n")
        out.append(
            side_by_side(
                "v1", v1_spec.read_text().splitlines(), "v2", v2_spec.read_text().splitlines()
            )
        )
        out.append("\n")
    return "".join(out)


def stage2(command: str) -> str:
    """v1's enumeration versus v2's, plus the environments each requested."""
    out = ["## Stage 2 — configuration generation\n\n"]
    rows = cells("generate", command)
    if not rows:
        return "".join(out) + "_no cells_\n\n"

    run = Path(rows[0]["run_dir"])
    manifest = json.loads((run / "manifest.json").read_text())
    comparison = (manifest.get("checks") or {}).get("invocation_comparison") or {}
    counts = comparison.get("counts", {})

    reference = v1.reference_invocations(command, max_arity=1, max_count=1)
    v2_lines = (run / f"{v1.slug(command)}.invocations.txt").read_text().splitlines()

    out.append(
        f"* v1 emitted **{counts.get('v1_lines')}** lines "
        f"(**{counts.get('v1_unique')}** distinct invocations)\n"
        f"* v2 emitted **{counts.get('produced_lines')}** lines "
        f"(**{counts.get('produced_unique')}** distinct)\n"
        f"* matched **{counts.get('matched')}**, missing **{counts.get('missing')}**, "
        f"spurious **{counts.get('spurious')}** "
        f"(recall {comparison.get('recall')}, precision {comparison.get('precision')})\n"
        f"* equivalence: {comparison.get('equivalence')}\n\n"
    )

    out.append("### What v1 emitted\n\n")
    v1_lines = sorted(set(reference.invocations)) if reference.available else ["unavailable"]
    out.append(fence(v1_lines))
    out.append("\n\n### What v2 emitted\n\n")
    out.append(fence(sorted(set(v2_lines))))
    out.append("\n\n")

    for key, heading in (
        ("missing_sample", "In v1 but not v2 (missing)"),
        ("spurious_sample", "In v2 but not v1 (spurious)"),
    ):
        sample = comparison.get(key) or []
        out.append(f"### {heading} — {len(sample)} shown\n\n")
        out.append(fence(sample) if sample else "_none_\n")
        out.append("\n\n")

    form = comparison.get("form_notes") or {}
    if form:
        out.append(
            f"### Form differences among matches\n\n"
            f"Of {form.get('matched')} matched invocations, {form.get('form_identical')} were "
            f"spelled identically. {form.get('differs_equals_style', 0)} differed in `=` style "
            f"and {form.get('differs_token_order_only', 0)} in token order only — "
            f"reported, never scored.\n\n"
        )

    config = (manifest.get("checks") or {}).get("config_comparison") or {}
    if config.get("available"):
        out.append(
            f"### Environments requested\n\n"
            f"* v2 configurations covered by one v1 would build: "
            f"**{config.get('env_covered_rate')}**\n"
            f"* agreement by field: `{json.dumps(config.get('rates'))}`\n\n"
        )
        for mismatch in (config.get("mismatch_sample") or [])[:6]:
            out.append(
                f"* `{mismatch['invocation']}`\n"
                f"  * v2 asks for: `{mismatch['produced']['demands']}`\n"
                f"  * v1 would build: `{mismatch['closest_v1']['demands']}`\n"
                f"  * differing: {', '.join(mismatch['differing_fields'])}\n"
            )
        out.append("\n")
    return "".join(out)


def stage3(command: str) -> str:
    """v1's strace record versus what v2's model reported observing."""
    out = ["## Stage 3 — execution and tracing\n\n"]
    rows = cells("trace", command)
    if not rows:
        return "".join(out) + "_no cells_\n\n"

    ok = [r for r in rows if r.get("status") == "ok"]
    out.append(f"* {len(ok)} of {len(rows)} cells produced a usable observation\n")

    manifest = json.loads((Path(rows[0]["run_dir"]) / "manifest.json").read_text())
    sessions = (manifest.get("checks") or {}).get("sessions") or []
    reported = sum(1 for s in sessions if s.get("status") == "ok")
    out.append(
        f"* in the first cell, {reported} of {len(sessions)} sessions called "
        f"`report_observations`; the rest ended in prose after "
        f"{sessions[0].get('turns') if sessions else '?'} turns\n\n"
    )

    if not ok:
        out.append("_no v2 traces to compare_\n\n")
        return "".join(out)

    produced_path = Path(ok[0]["run_dir"]) / f"{v1.slug(command)}.traces.json"
    reference_path = v1.v1_root() / "caruca" / "outputs" / f"{command}.parity.json"
    if not (produced_path.is_file() and reference_path.is_file()):
        out.append("_one side is missing_\n\n")
        return "".join(out)

    record = tr.compare_traces(
        json.loads(produced_path.read_text()),
        json.loads(reference_path.read_text()),
        command=command,
    )
    projection, core, inference = record["projection"], record["core"], record["inference"]
    out.append(
        f"* v1 recorded {projection['reference_raw_pairs']} raw `(action, path)` pairs, "
        f"reduced to **{projection['reference_distinct_projected']} distinct** by v1's own "
        f"relevance filter ({projection['system_paths_excluded']} system paths dropped)\n"
        f"* core recall {core['micro']['recall']}, inference recall "
        f"{inference['micro']['recall']}\n\n"
        f"* v1 traces: `{reference_path}`\n* v2 traces: `{produced_path}`\n\n"
    )
    for key, heading in (
        ("missing_sample", "v1 saw, v2 did not"),
        ("spurious_sample", "v2 reported, v1 did not"),
    ):
        sample = record.get(key) or []
        out.append(f"### {heading}\n\n")
        out.append(fence([" ".join(x) for x in sample]) if sample else "_none_\n")
        out.append("\n\n")
    return "".join(out)


def stage4(command: str) -> str:
    """Three annotations of the same command: v1's, v2's, and the hand-curated one."""
    out = ["## Stage 4 — annotation\n\n"]
    rows = cells("annotate", command)
    if not rows:
        return "".join(out) + "_no cells_\n\n"

    ok = [r for r in rows if r.get("status") == "ok"]
    if not ok:
        reason = rows[0].get("error") or "unknown"
        out.append(f"v2 produced no annotation. Reason:\n\n{fence([str(reason)[:400]])}\n\n")
        return "".join(out)

    v2_path = Path(ok[0]["run_dir"]) / f"{v1.slug(command)}.pash.annotation"
    v1_path = v1.v1_root() / "caruca" / "outputs" / f"{command}.parity.pash.json"
    truth_text = v1.ground_truth_annotation(command, "pash")

    out.append(f"* v1: `{v1_path}`\n* v2: `{v2_path}`\n* hand-curated ground truth\n\n")

    for label, text in (
        ("v1's annotator", v1_path.read_text() if v1_path.is_file() else None),
        ("v2", v2_path.read_text() if v2_path.is_file() else None),
        ("hand-curated ground truth", truth_text),
    ):
        out.append(f"### {label}\n\n")
        if text is None:
            out.append("_missing_\n\n")
            continue
        payload = json.loads(text)
        cases = payload.get("cases", []) if isinstance(payload, dict) else payload
        out.append(f"{len(cases)} case(s)\n\n")
        out.append(fence(json.dumps(cases, indent=1).splitlines(), "json", limit=45))
        out.append("\n\n")

    if v2_path.is_file() and truth_text:
        record = ann.compare_annotation(
            "pash",
            v2_path.read_text(),
            truth_text,
            label="gt",
            reference_kind=ann.REFERENCE_GROUND_TRUTH,
        )
        agreement = record.get("agreement") or {}
        out.append(
            f"### v2 against the ground truth\n\n"
            f"* alignment: `{record.get('alignment')}` "
            f"(the two are written at different granularities)\n"
            f"* aligned {agreement.get('comparable')} case(s); "
            f"class agreeing {agreement.get('pclass')}, "
            f"fully agreeing {agreement.get('fully_agreeing')}\n\n"
        )
        for item in (record.get("disagreement_sample") or [])[:8]:
            out.append(
                f"* `{item['case']}` — **{item['field']}**: "
                f"v2 `{item['produced']}` vs truth `{item['reference']}`\n"
            )
        out.append("\n")
    return "".join(out)


def render(command: str) -> str:
    parts = [
        f"# Parity diff — `{command}`\n\n",
        "What v1 produced, what v2 produced, and where they differ. Generated by "
        "`scripts/parity_diff.py`; the aggregates are in "
        "`ai_docs/analysis/v1_v2_parity_study.md`.\n\n",
        f"v1 commit `{v1.v1_commit()}` · model `openai/gpt-4o` · temperature 0.0 · "
        "bound `--max-arity 1 --max-count 1`\n\n",
        "> Quotes v1 source verbatim. v1 is private and unlicensed — read locally, do not "
        "commit or share.\n\n---\n\n",
    ]
    for fn in (stage1, stage2, stage3, stage4):
        try:
            parts.append(fn(command))
        except Exception as exc:  # noqa: BLE001 - one broken stage must not lose the rest
            parts.append(f"_{fn.__name__} failed: {type(exc).__name__}: {exc}_\n\n")
        parts.append("---\n\n")
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("commands", nargs="*", default=None, help="default: all nine")
    parser.add_argument("--stdout", action="store_true", help="print instead of writing files")
    args = parser.parse_args()

    targets = args.commands or COMMANDS
    if not args.stdout:
        OUT.mkdir(parents=True, exist_ok=True)
    for command in targets:
        text = render(command)
        if args.stdout:
            print(text)
        else:
            path = OUT / f"{v1.slug(command)}.md"
            path.write_text(text)
            print(f"  {path}  ({len(text):,} bytes)")
    if not args.stdout:
        print(f"\n{len(targets)} file(s) in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
