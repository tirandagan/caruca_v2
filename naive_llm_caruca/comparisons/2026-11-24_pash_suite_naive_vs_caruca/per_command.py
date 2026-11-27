#!/usr/bin/env python3
"""Compare the naive LLM's annotation files against PaSh's own files, command by command.

Reads the records in full_run/ (Python 3 stdlib only; runs with `python3 -I per_command.py`)
and writes per_command.md and per_command.json in the same folder.
"""
import glob
import gzip
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDS = HERE / "full_run"
OUT_MD = HERE / "per_command.md"
OUT_JSON = HERE / "per_command.json"

REF = "pash-own"
TARGET = "naive"
ANSWER_METHOD = "as PaSh passes them"

# General-knowledge correctness judgements for commands where only the naive LLM has a file.
# Keyed by command name; applies to what the naive LLM's file answered for the command in general.
NAIVE_ONLY_JUDGEMENTS = {
    "mkdir": {
        "judgement": "right",
        "unsure": False,
        "explanation": (
            "`mkdir` creates directories (filesystem side effects, not a data stream), "
            "so refusing to split is right."
        ),
    },
    "join": {
        "judgement": "mixed (no-split right; raises wrong)",
        "unsure": False,
        "explanation": (
            "The 1 'no split' answer is right for `join` in general under PaSh's stream-splitting model "
            "(joining two sorted inputs on a key requires key-partitioned co-shuffling, which PaSh does "
            "not implement). The 2 exceptions (`join requires exactly two operands`) are bugs in the "
            "naive file's argument parser."
        ),
    },
    "fmt": {
        "judgement": "wrong",
        "unsure": False,
        "explanation": (
            "`fmt` reflows paragraphs across line boundaries (and across multiple input files when "
            "there is no blank line between them), so splitting arbitrarily or per file does not preserve "
            "exact output in general. In addition, the naive file misparsed `-w1` as a filename operand "
            "(`stdin: False`), which triggered a PaSh compiler stop (`AssertionError` in `pipe_append`) "
            "in both parts that use it."
        ),
    },
    "rev": {
        "judgement": "right",
        "unsure": False,
        "explanation": (
            "`rev` reverses characters within each line independently, so splitting by line chunks "
            "and concatenating outputs preserves exact output."
        ),
    },
    "mogrify": {
        "judgement": "not sure",
        "unsure": True,
        "explanation": (
            "Not sure: `mogrify` transforms each input image file independently, so per-file parallelism "
            "(`INDIV_FILES`) is semantically valid when output paths do not collide; however, `mogrify` "
            "writes files directly rather than streaming stdin to stdout, so PaSh cannot split it as a "
            "streaming stage (and rejected the part because of `OTHER_OUTPUT`)."
        ),
    },
    "convert": {
        "judgement": "right",
        "unsure": False,
        "explanation": (
            "`convert -resize 70% - -` transforms a binary image stream on stdin/stdout; "
            "it cannot be split on line boundaries, so 'no split' is right."
        ),
    },
    "iconv": {
        "judgement": "not sure",
        "unsure": True,
        "explanation": (
            "Not sure: `iconv` returned `INDIV_FILES -> CONCATENATE`; per-file transcoding is valid for "
            "independent files in stateless encodings (such as UTF-8/ASCII here), but can fail in general "
            "for stateful encodings (e.g. ISO-2022) or BOM handling across concatenated outputs."
        ),
    },
    "ls": {
        "judgement": "right",
        "unsure": False,
        "explanation": (
            "`ls` lists directory entries with no input stream to split and global sorting of entries, "
            "so 'no split' is right."
        ),
    },
    "mktemp": {
        "judgement": "right",
        "unsure": False,
        "explanation": (
            "`mktemp` creates a unique temporary file or directory (filesystem side effect, no input "
            "stream), so 'no split' is right."
        ),
    },
}


def read_jsonl(path: Path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def rate(a: int, b: int) -> dict:
    return {"a": a, "b": b, "text": f"{a} of {b}"}


def base_id(script_id: str) -> str:
    return script_id.split("#")[0]


def geom_mean(xs):
    if not xs:
        return None
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def load_and_fix_results(records_dir: Path):
    """Apply the same two fix-ups as prep_full_records.py and full_run/numbers.md."""
    res = read_jsonl(records_dir / "results.jsonl.gz")
    log = Counter()
    log["result_rows_read"] = len(res)

    # Fix-up 1: compare every non-bash row against the same repeat's bash row.
    bash = {(r["id"], r["phase"], r["mode"], r["repeat"]): r for r in res if r["set"] == "bash"}
    for r in res:
        if r["set"] == "bash":
            continue
        b = bash[(r["id"], r["phase"], r["mode"], r["repeat"])]
        was = (r["same_as_bash"], r["output_files_same_as_bash"])
        r["same_as_bash"] = r["out_sha256"] == b["out_sha256"]
        bash_later = r["order"] is not None and r["order"].index("bash") > r["order"].index(r["set"])
        if r.get("output_files_sha") and b.get("output_files_sha"):
            r["output_files_same_as_bash"] = r["output_files_sha"] == b["output_files_sha"]
        elif r["output_files"] == 0 and b["output_files"] == 0:
            r["output_files_same_as_bash"] = True
        elif bash_later:
            r["output_files_same_as_bash"] = None
        log["fixup1_rows_compared_again"] += 1
        log["fixup1_same_as_bash_changed"] += int(was[0] != r["same_as_bash"])
        log["fixup1_output_files_changed"] += int(was[1] != r["output_files_same_as_bash"])

    # Fix-up 2: drop the 7 web-search plain rows without `node`, replace superseded rows with redo-*.
    broken = [
        r for r in res
        if r["mode"] == "plain"
        and r["id"] == "web-search/engine"
        and "node" in (r.get("stderr") or "")
        and "No such file" in (r.get("stderr") or "")
    ]
    broken_ids = {id(r) for r in broken}
    res = [r for r in res if id(r) not in broken_ids]

    redone = {(r["id"], r["mode"], r["repeat"]) for r in res if r["phase"].startswith("redo")}
    superseded = [
        r for r in res
        if not r["phase"].startswith("redo") and (r["id"], r["mode"], r["repeat"]) in redone
    ]
    sup_ids = {id(r) for r in superseded}
    res = [r for r in res if id(r) not in sup_ids]

    sed2_bash = [r for r in res if r["phase"] == "sed2" and r["set"] == "bash"]
    sed2_ids = {id(r) for r in sed2_bash}
    res = [r for r in res if id(r) not in sed2_ids]

    log["fixup2_web_search_without_node_dropped"] = len(broken)
    log["fixup2_superseded_by_redo_dropped"] = len(superseded)
    log["sed2_bash_rows_dropped"] = len(sed2_bash)

    # Fold phases into "main" and check uniqueness.
    for r in res:
        r["phase_recorded"] = r["phase"]
        r["phase"] = "main"
    dup_check = Counter((r["id"], r["set"], r["mode"], r["repeat"]) for r in res)
    dups = [k for k, v in dup_check.items() if v > 1]
    if dups:
        raise RuntimeError(f"Duplicate result rows after fix-ups: {dups[:5]}")
    log["result_rows_kept"] = len(res)
    return res, dict(log)


def attribute_compiler_stops(rp, rn, ans_by_key):
    """Identify differential compiler stops (`pash crash`) and attribute culprit commands.

    For each distinct part where one set has outcome == 'pash crash' and the other does not,
    inspect the part's commands and their `as PaSh passes them` IO answers from answers/*.jsonl.gz.
    In this suite, every differential compiler stop is an `AssertionError` in PaSh's `pipe_append`
    (`assert not other_in is None`), caused by a non-first pipeline stage whose annotation reported
    `io.stdin is False` under the crashing set and not under the other set.
    """
    naive_only_parts = []
    pash_only_parts = []
    both_crash_parts = []

    naive_only_culprit = defaultdict(set)  # cmd -> set of part keys (id, text_sha)
    pash_only_culprit = defaultdict(set)
    naive_only_coocc = defaultdict(set)
    pash_only_coocc = defaultdict(set)
    unattributed = []

    for rk in sorted(rp):
        op = rp[rk]["outcome"]
        on = rn[rk]["outcome"]
        p_crash = op == "pash crash"
        n_crash = on == "pash crash"
        if not (p_crash or n_crash):
            continue
        if p_crash and n_crash:
            both_crash_parts.append({
                "script": rk[0],
                "text_sha": rk[1],
                "reason_pash_own": rp[rk]["reason"],
                "reason_naive": rn[rk]["reason"],
                "commands": [c["command"] for c in rp[rk]["commands"]],
            })
            continue

        crashing_set = TARGET if n_crash else REF
        other_set = REF if n_crash else TARGET
        crashing_reg = rn[rk] if n_crash else rp[rk]
        other_reg = rp[rk] if n_crash else rn[rk]

        # Record co-occurrence for every command in the part.
        part_cmds = {c["command"] for c in crashing_reg["commands"]}
        for cmd in part_cmds:
            if n_crash:
                naive_only_coocc[cmd].add(rk)
            else:
                pash_only_coocc[cmd].add(rk)

        # Programmatically find culprit command(s) for AssertionError / pipe_append:
        # a non-first command (position > 1) whose IO answer reports stdin == False in crashing_set
        # and does not report stdin == False in other_set.
        culprits = []
        if "AssertionError" in (crashing_reg.get("reason") or ""):
            for c in crashing_reg["commands"]:
                pos = c["position"]
                if pos <= 1:
                    continue
                a_crash = ans_by_key.get((rk[0], crashing_set, pos))
                a_other = ans_by_key.get((rk[0], other_set, pos))
                crash_no_stdin = (
                    a_crash is not None
                    and a_crash.get("io") is not None
                    and a_crash["io"].get("stdin") is False
                )
                other_no_stdin = (
                    a_other is not None
                    and a_other.get("io") is not None
                    and a_other["io"].get("stdin") is False
                )
                if crash_no_stdin and not other_no_stdin:
                    culprits.append(c["command"])

        entry = {
            "script": rk[0],
            "text_sha": rk[1],
            "crashing_set": crashing_set,
            "crashing_outcome": crashing_reg["outcome"],
            "crashing_reason": crashing_reg["reason"],
            "other_outcome": other_reg["outcome"],
            "other_reason": other_reg["reason"],
            "culprit_commands": culprits,
            "all_commands_in_part": [c["command"] for c in crashing_reg["commands"]],
        }
        if not culprits:
            unattributed.append(entry)
        for cmd in culprits:
            if n_crash:
                naive_only_culprit[cmd].add(rk)
            else:
                pash_only_culprit[cmd].add(rk)

        if n_crash:
            naive_only_parts.append(entry)
        else:
            pash_only_parts.append(entry)

    return {
        "naive_only_parts": naive_only_parts,
        "pash_only_parts": pash_only_parts,
        "both_crash_parts": both_crash_parts,
        "naive_only_culprit": naive_only_culprit,
        "pash_only_culprit": pash_only_culprit,
        "naive_only_coocc": naive_only_coocc,
        "pash_only_coocc": pash_only_coocc,
        "unattributed": unattributed,
    }


def main():
    occ_all = read_jsonl(RECORDS / "occurrences.jsonl.gz")
    reg_all = read_jsonl(RECORDS / "regions.jsonl.gz")
    cmds_rec = read_jsonl(RECORDS / "commands.jsonl.gz")
    manifest = json.loads((RECORDS / "manifest.json").read_text(encoding="utf-8"))
    results, fixup_log = load_and_fix_results(RECORDS)

    ans_all = []
    for path_str in sorted(glob.glob(str(RECORDS / "answers" / "*.jsonl.gz"))):
        ans_all.extend(read_jsonl(Path(path_str)))

    pash_stock = set(manifest["pash"]["stock_commands"])
    naive_manifest_cmds = (
        set(manifest["naive"]["commands"].keys())
        if isinstance(manifest["naive"]["commands"], dict)
        else set(manifest["naive"]["commands"])
    )

    # Filter occurrences: phase == "main", mode == "instrumented", inside parts (outside_pash == False).
    po = {}
    na = {}
    outside_naive = defaultdict(list)
    for o in occ_all:
        if o["phase"] != "main" or o["mode"] != "instrumented":
            continue
        if o["outside_pash"]:
            if o["set"] == TARGET:
                outside_naive[o["command"]].append(o)
            continue
        key = (base_id(o["id"]), o["region_text_sha"], o["position"])
        if o["set"] == REF:
            assert key not in po, f"Duplicate occurrence key in {REF}: {key}"
            po[key] = o
        elif o["set"] == TARGET:
            assert key not in na, f"Duplicate occurrence key in {TARGET}: {key}"
            na[key] = o

    assert set(po) == set(na), "Occurrence keys differ between pash-own and naive"
    total_uses = len(po)

    # Filter regions: phase == "main", mode == "instrumented".
    rp = {}
    rn = {}
    for r in reg_all:
        if r["phase"] != "main" or r["mode"] != "instrumented":
            continue
        rk = (base_id(r["id"]), r["text_sha"])
        if r["set"] == REF:
            assert rk not in rp, f"Duplicate region key in {REF}: {rk}"
            rp[rk] = r
        elif r["set"] == TARGET:
            assert rk not in rn, f"Duplicate region key in {TARGET}: {rk}"
            rn[rk] = r

    assert set(rp) == set(rn), "Region keys differ between pash-own and naive"
    total_parts = len(rp)

    # Index `as PaSh passes them` answer rows by (script_id, set, position) via occurrence answer_ref.
    ans_by_ref = {}
    # Each answer file lists rows in order per (id, set, method); match using occurrences' answer_ref
    # or sequential position within each script's `as PaSh passes them` rows.
    ans_pash_method = defaultdict(list)
    for a in ans_all:
        if a.get("method") == ANSWER_METHOD and a["set"] in (REF, TARGET):
            ans_pash_method[(base_id(a["id"]), a["set"])].append(a)

    # Map (script_id, set, position) -> answer row for regions that have 1 region (like unixfun 12/16/34/36),
    # and match by (script, command, invocation) cleanly for all occurrences.
    occ_to_ans = {}
    for s_name, occ_map in ((REF, po), (TARGET, na)):
        by_script_occ = defaultdict(list)
        for k, o in sorted(occ_map.items()):
            by_script_occ[k[0]].append((k, o))
        for sid, items in by_script_occ.items():
            arows = ans_pash_method.get((sid, s_name), [])
            # Build lookup by (command, invocation) and also by 1-based position if lengths match.
            if len(arows) == len(items):
                for (k, o), a in zip(items, arows):
                    if a["command"] == o["command"]:
                        occ_to_ans[(sid, s_name, o["position"])] = a
            # Also match by exact invocation when a script has multiple regions
            by_inv = defaultdict(list)
            for a in arows:
                by_inv[(a["command"], a.get("example_invocation") or a.get("invocation"))].append(a)
            for k, o in items:
                if (sid, s_name, o["position"]) not in occ_to_ans:
                    cands = by_inv.get((o["command"], o["invocation"]), [])
                    if cands:
                        occ_to_ans[(sid, s_name, o["position"])] = cands[0]

    stops = attribute_compiler_stops(rp, rn, occ_to_ans)

    # Group occurrences and distinct parts by command.
    by_cmd = defaultdict(list)
    parts_by_cmd = defaultdict(set)
    for k, o in po.items():
        cmd = o["command"]
        assert na[k]["command"] == cmd
        by_cmd[cmd].append(k)
        parts_by_cmd[cmd].add((k[0], k[1]))

    # Self-checks on manifest vs occurrence `source` consistency.
    source_manifest_mismatches = []
    for cmd, ks in by_cmd.items():
        src_n = {na[k]["source"] for k in ks}
        src_p = {po[k]["source"] for k in ks}
        has_n_occ = src_n == {"ours"}
        has_p_occ = src_p == {"pash-own"}
        if has_n_occ != (cmd in naive_manifest_cmds):
            source_manifest_mismatches.append(("naive", cmd, sorted(src_n), cmd in naive_manifest_cmds))
        if has_p_occ != (cmd in pash_stock):
            source_manifest_mismatches.append(("pash-own", cmd, sorted(src_p), cmd in pash_stock))
    assert not source_manifest_mismatches, f"Source/manifest mismatch: {source_manifest_mismatches}"

    # ---- Section 1: per-command table (one row per command used inside a part, sorted by uses desc)
    section1 = []
    for cmd, ks in sorted(by_cmd.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        n_uses = len(ks)
        n_parts = len(parts_by_cmd[cmd])
        has_naive = cmd in naive_manifest_cmds
        has_pash = cmd in pash_stock

        split_pash = sum(po[k]["split"] is True for k in ks)
        split_naive = sum(na[k]["split"] is True for k in ks)
        gained_uses = sum((na[k]["split"] is True) and not (po[k]["split"] is True) for k in ks)
        lost_uses = sum((po[k]["split"] is True) and not (na[k]["split"] is True) for k in ks)

        naive_no_split = sum(na[k]["file_answer"] == "says no split" for k in ks)
        naive_no_split_direct = sum(na[k]["direct_file_answer"] == "says no split" for k in ks)
        naive_raised = sum(na[k]["file_answer"] == "raised" or na[k]["exception"] is not None for k in ks)
        pash_no_split = sum(po[k]["file_answer"] == "says no split" for k in ks)
        pash_raised = sum(po[k]["file_answer"] == "raised" or po[k]["exception"] is not None for k in ks)

        stop_naive_only = len(stops["naive_only_culprit"].get(cmd, set()))
        stop_pash_only = len(stops["pash_only_culprit"].get(cmd, set()))
        stop_naive_only_coocc = len(stops["naive_only_coocc"].get(cmd, set()))
        stop_pash_only_coocc = len(stops["pash_only_coocc"].get(cmd, set()))

        if has_naive and not has_pash:
            verdict = "naive only"
        elif split_naive > split_pash:
            verdict = "naive splits more"
        elif split_naive < split_pash:
            verdict = "naive splits less"
        elif split_naive == 0 and split_pash == 0:
            verdict = "neither splits"
        else:
            verdict = "same"

        if has_naive and has_pash:
            group = "both"
        elif has_naive and not has_pash:
            group = "naive_only"
        elif not has_naive and has_pash:
            group = "pash_only"
        else:
            group = "neither"

        section1.append({
            "command": cmd,
            "group": group,
            "naive_has_file": has_naive,
            "pash_own_has_file": has_pash,
            "uses_in_parts": rate(n_uses, total_uses),
            "parts_with_command": rate(n_parts, total_parts),
            "split_pash_own": rate(split_pash, n_uses),
            "split_naive": rate(split_naive, n_uses),
            "gained_uses": gained_uses,
            "lost_uses": lost_uses,
            "naive_said_no_split": rate(naive_no_split, n_uses),
            "naive_said_no_split_direct": rate(naive_no_split_direct, n_uses),
            "naive_raised": rate(naive_raised, n_uses),
            "pash_own_said_no_split": rate(pash_no_split, n_uses),
            "pash_own_raised": rate(pash_raised, n_uses),
            "compiler_stop_naive_only": rate(stop_naive_only, n_parts),
            "compiler_stop_pash_own_only": rate(stop_pash_only, n_parts),
            "compiler_stop_naive_only_cooccurring_parts": rate(stop_naive_only_coocc, n_parts),
            "compiler_stop_pash_own_only_cooccurring_parts": rate(stop_pash_only_coocc, n_parts),
            "verdict": verdict,
        })

    # ---- Section 2: totals for the three groups (+ neither for reconciliation)
    total_cmds = len(section1)
    group_specs = [
        ("both", "Both have files"),
        ("naive_only", "Only the naive LLM has a file"),
        ("pash_only", "Only PaSh's own has a file"),
        ("neither", "Neither has a file (reconciliation)"),
    ]
    section2 = []
    for gkey, glabel in group_specs:
        rows = [r for r in section1 if r["group"] == gkey]
        g_cmds = [r["command"] for r in rows]
        g_uses = sum(r["uses_in_parts"]["a"] for r in rows)
        g_sp_pash = sum(r["split_pash_own"]["a"] for r in rows)
        g_sp_naive = sum(r["split_naive"]["a"] for r in rows)
        g_stop_n = sum(r["compiler_stop_naive_only"]["a"] for r in rows)
        g_stop_p = sum(r["compiler_stop_pash_own_only"]["a"] for r in rows)
        g_raise_n = sum(r["naive_raised"]["a"] for r in rows)
        g_raise_p = sum(r["pash_own_raised"]["a"] for r in rows)
        g_raise_n_cmds = sorted(r["command"] for r in rows if r["naive_raised"]["a"] > 0)
        g_raise_p_cmds = sorted(r["command"] for r in rows if r["pash_own_raised"]["a"] > 0)
        section2.append({
            "group": gkey,
            "label": glabel,
            "commands": rate(len(rows), total_cmds),
            "command_names": sorted(g_cmds),
            "uses": rate(g_uses, total_uses),
            "split_pash_own": rate(g_sp_pash, g_uses),
            "split_naive": rate(g_sp_naive, g_uses),
            "compiler_stops_naive_only": rate(g_stop_n, total_parts),
            "compiler_stops_pash_own_only": rate(g_stop_p, total_parts),
            "files_raising_uses_naive": rate(g_raise_n, g_uses),
            "files_raising_uses_pash_own": rate(g_raise_p, g_uses),
            "files_raising_commands_naive": g_raise_n_cmds,
            "files_raising_commands_pash_own": g_raise_p_cmds,
        })

    # Manifest-level file coverage summary (all 82 naive files vs 30 PaSh's own files).
    cmds_po_suite = {c["command"]: c["source"] for c in cmds_rec if c["set"] == REF}
    cmds_na_suite = {c["command"]: c["source"] for c in cmds_rec if c["set"] == TARGET}
    naive_only_suite_cmds = sorted(c for c, s in cmds_na_suite.items() if s == "ours" and cmds_po_suite.get(c) == "none")
    naive_only_in_parts = sorted(r["command"] for r in section1 if r["group"] == "naive_only")
    naive_only_outside_only = sorted(set(naive_only_suite_cmds) - set(naive_only_in_parts))

    manifest_coverage = {
        "naive_total_files": len(naive_manifest_cmds),
        "pash_own_total_files": len(pash_stock),
        "both_files": len(naive_manifest_cmds & pash_stock),
        "both_not_in_parts": sorted((naive_manifest_cmds & pash_stock) - set(by_cmd)),
        "naive_only_total_files": len(naive_manifest_cmds - pash_stock),
        "naive_only_in_parts": naive_only_in_parts,
        "naive_only_outside_parts_only": naive_only_outside_only,
        "naive_only_unused_in_suite_count": len((naive_manifest_cmds - pash_stock) - set(naive_only_suite_cmds)),
        "pash_own_only_total_files": len(pash_stock - naive_manifest_cmds),
        "pash_own_only_in_parts": sorted(r["command"] for r in section1 if r["group"] == "pash_only"),
        "pash_own_only_not_in_parts": sorted((pash_stock - naive_manifest_cmds) - set(by_cmd)),
    }

    # ---- Section 3: What the naive LLM adds
    section3_in_parts = []
    for cmd in sorted(naive_only_in_parts, key=lambda c: (-len(by_cmd[c]), c)):
        ks = by_cmd[cmd]
        fa_counts = Counter(na[k]["file_answer"] for k in ks)
        recipes = Counter(
            ", ".join(na[k]["recipes"]) if na[k]["recipes"] else "none"
            for k in ks
        )
        excs = sorted({na[k]["exception"] for k in ks if na[k]["exception"]})
        part_transitions = Counter(
            (rp[(k[0], k[1])]["outcome"], rn[(k[0], k[1])]["outcome"])
            for k in sorted({(k[0], k[1]) for k in ks})
        )
        scripts = sorted({k[0] for k in ks})
        sample_invs = sorted({na[k]["invocation"] for k in ks})[:3]
        j = NAIVE_ONLY_JUDGEMENTS[cmd]
        section3_in_parts.append({
            "command": cmd,
            "uses_in_parts": len(ks),
            "parts": len(parts_by_cmd[cmd]),
            "scripts": scripts,
            "file_answers": dict(fa_counts),
            "split_in_pash": rate(sum(na[k]["split"] is True for k in ks), len(ks)),
            "recipes": dict(recipes),
            "exceptions": excs,
            "part_outcome_transitions": {f"{a} -> {b}": cnt for (a, b), cnt in part_transitions.items()},
            "sample_invocations": sample_invs,
            "judgement": j["judgement"],
            "unsure": j["unsure"],
            "explanation": j["explanation"],
        })

    section3_outside_only = []
    for cmd in naive_only_outside_only:
        rows = [a for a in ans_all if a["set"] == TARGET and a["command"] == cmd]
        allow_lines = sum(r.get("lines", 1) for r in rows if r["allows_split"] is True)
        no_split_lines = sum(r.get("lines", 1) for r in rows if r["allows_split"] is False and not r["exception"])
        raised_lines = sum(r.get("lines", 1) for r in rows if r["exception"])
        total_lines = allow_lines + no_split_lines + raised_lines
        scripts = sorted({base_id(r["id"]) for r in rows})
        sample_invs = sorted({(r.get("example_invocation") or r.get("invocation") or "") for r in rows})[:2]
        j = NAIVE_ONLY_JUDGEMENTS[cmd]
        section3_outside_only.append({
            "command": cmd,
            "answer_rows": len(rows),
            "answer_lines": total_lines,
            "allows_split_lines": allow_lines,
            "no_split_lines": no_split_lines,
            "raised_lines": raised_lines,
            "scripts_count": len(scripts),
            "sample_scripts": scripts[:5],
            "sample_invocations": sample_invs,
            "judgement": j["judgement"],
            "unsure": j["unsure"],
            "explanation": j["explanation"],
        })

    # ---- Section 4: wall-clock evidence (scripts where exactly one command's split differs)
    times_by_set = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for r in results:
        if r["mode"] != "plain":
            continue
        s = r["set"]
        if s not in (REF, TARGET, "bash", "pash-own-copy"):
            continue
        sid = base_id(r["id"])
        times_by_set[s][sid][r["repeat"]] += r["seconds"]

    med_time = {
        s: {sid: statistics.median(rep_map.values()) for sid, rep_map in s_map.items()}
        for s, s_map in times_by_set.items()
    }

    by_script_uses = defaultdict(list)
    for k in sorted(po):
        by_script_uses[k[0]].append(k)

    all_scripts = sorted(med_time[REF].keys())
    single_cmd_scripts = []
    multi_cmd_scripts = []
    zero_diff_scripts = []

    for sid in all_scripts:
        diff_cmds = defaultdict(lambda: {"gained_in_naive": 0, "lost_in_naive": 0})
        for k in by_script_uses.get(sid, []):
            sp_p = po[k]["split"] is True
            sp_n = na[k]["split"] is True
            if sp_p != sp_n:
                c = po[k]["command"]
                if sp_n:
                    diff_cmds[c]["gained_in_naive"] += 1
                else:
                    diff_cmds[c]["lost_in_naive"] += 1
        tp = med_time[REF][sid]
        tn = med_time[TARGET][sid]
        ratio = tn / tp
        if not diff_cmds:
            zero_diff_scripts.append(sid)
        elif len(diff_cmds) == 1:
            cmd = next(iter(diff_cmds))
            single_cmd_scripts.append({
                "script": sid,
                "command": cmd,
                "gained_in_naive": diff_cmds[cmd]["gained_in_naive"],
                "lost_in_naive": diff_cmds[cmd]["lost_in_naive"],
                "pash_own_seconds": round(tp, 4),
                "naive_seconds": round(tn, 4),
                "ratio_naive_over_pash_own": round(ratio, 4),
            })
        else:
            multi_cmd_scripts.append({
                "script": sid,
                "commands": {c: dict(v) for c, v in sorted(diff_cmds.items())},
                "pash_own_seconds": round(tp, 4),
                "naive_seconds": round(tn, 4),
                "ratio_naive_over_pash_own": round(ratio, 4),
            })

    # Noise band from pash-own-copy vs pash-own across all 86 scripts
    copy_ratios = [med_time["pash-own-copy"][sid] / med_time[REF][sid] for sid in all_scripts]
    noise_band = {
        "min": round(min(copy_ratios), 4),
        "median": round(statistics.median(copy_ratios), 4),
        "max": round(max(copy_ratios), 4),
    }

    single_by_cmd = defaultdict(list)
    for row in single_cmd_scripts:
        single_by_cmd[row["command"]].append(row)
    single_cmd_summary = {}
    for cmd, rows in sorted(single_by_cmd.items()):
        rs = [r["ratio_naive_over_pash_own"] for r in rows]
        single_cmd_summary[cmd] = {
            "scripts": rate(len(rows), len(all_scripts)),
            "geom_mean_ratio": round(geom_mean(rs), 4),
            "median_ratio": round(statistics.median(rs), 4),
            "min_ratio": round(min(rs), 4),
            "max_ratio": round(max(rs), 4),
            "slower_than_noise_band_max": rate(sum(r > noise_band["max"] for r in rs), len(rs)),
            "faster_than_noise_band_min": rate(sum(r < noise_band["min"] for r in rs), len(rs)),
        }

    # Self-checks against full_run/numbers.md totals
    self_checks = {
        "scripts": len(all_scripts),
        "distinct_parts": total_parts,
        "uses_in_parts": total_uses,
        "commands_in_parts": total_cmds,
        "pash_own_parallel_parts": sum(r["outcome"] == "parallelized" for r in rp.values()),
        "naive_parallel_parts": sum(r["outcome"] == "parallelized" for r in rn.values()),
        "pash_own_split_uses": sum(o["split"] is True for o in po.values()),
        "naive_split_uses": sum(o["split"] is True for o in na.values()),
        "pash_own_compiler_stops": sum(r["outcome"] == "pash crash" for r in rp.values()),
        "naive_compiler_stops": sum(r["outcome"] == "pash crash" for r in rn.values()),
        "differential_compiler_stops_unattributed": len(stops["unattributed"]),
        "source_manifest_mismatches": len(source_manifest_mismatches),
    }
    assert self_checks["scripts"] == 86
    assert self_checks["distinct_parts"] == 177
    assert self_checks["uses_in_parts"] == 609
    assert self_checks["pash_own_parallel_parts"] == 41
    assert self_checks["naive_parallel_parts"] == 43
    assert self_checks["pash_own_split_uses"] == 126
    assert self_checks["naive_split_uses"] == 192
    assert self_checks["pash_own_compiler_stops"] == 4
    assert self_checks["naive_compiler_stops"] == 4
    assert self_checks["differential_compiler_stops_unattributed"] == 0

    payload = {
        "generated_by": "per_command.py",
        "records_dir": "full_run",
        "fixups": fixup_log,
        "self_checks": self_checks,
        "manifest_coverage": manifest_coverage,
        "compiler_stops_detail": {
            "naive_only": stops["naive_only_parts"],
            "pash_own_only": stops["pash_only_parts"],
            "both": stops["both_crash_parts"],
        },
        "section1_commands": section1,
        "section2_groups": section2,
        "section3_naive_only": {
            "in_parts": section3_in_parts,
            "outside_parts_only": section3_outside_only,
            "unused_in_suite_count": manifest_coverage["naive_only_unused_in_suite_count"],
        },
        "section4_wall_clock": {
            "total_scripts": len(all_scripts),
            "scripts_with_zero_split_diffs": len(zero_diff_scripts),
            "scripts_with_one_differing_command": len(single_cmd_scripts),
            "scripts_with_multiple_differing_commands": len(multi_cmd_scripts),
            "noise_band_pash_own_copy_vs_pash_own": noise_band,
            "single_command_summary": single_cmd_summary,
            "single_command_scripts": single_cmd_scripts,
            "multi_command_scripts": multi_cmd_scripts,
        },
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {OUT_MD.name} and {OUT_JSON.name} ({total_cmds} commands, {total_uses} uses, {total_parts} parts).")


def render_markdown(d: dict) -> str:
    sc = d["self_checks"]
    mc = d["manifest_coverage"]
    lines = []
    lines.append("# Naive LLM vs PaSh's Own Annotation Files, Command by Command")
    lines.append("")
    lines.append(
        f"Built by `per_command.py` from `full_run/` ({sc['scripts']} scripts, "
        f"{sc['distinct_parts']} distinct parts, {sc['uses_in_parts']} command uses inside parts across "
        f"{sc['commands_in_parts']} distinct commands). Per-command and per-part counts use "
        "`phase == \"main\"` and `mode == \"instrumented\"`. Wall-clock numbers in Section 4 apply the "
        "same two fix-ups as `prep_full_records.py` and `full_run/numbers.md` (same-repeat bash "
        "comparison; 7 `web-search/engine` timed rows missing `node` dropped; 7 superseded rows replaced "
        "by redone repeats)."
    )
    lines.append("")
    lines.append(
        "\"File said 'no split'\" and \"raised an error\" use `file_answer` (the file's answer to the "
        "words as PaSh passes them, matching what PaSh actually acted on). \"Parts where the naive file "
        "made PaSh's compiler stop and PaSh's own did not (and the reverse)\" counts distinct parts with "
        "`outcome == \"pash crash\"` under one set and not the other, attributed programmatically to the "
        "culprit command using `full_run/answers/*.jsonl.gz` (see footnote below Section 1)."
    )
    lines.append("")

    # ---- Section 1
    lines.append("## 1. Per-Command Comparison (Commands Used Inside Parts)")
    lines.append("")
    lines.append(
        "| Command | Naive LLM has a file | PaSh's own has a file | Uses in parts | "
        "Uses split with PaSh's own | Uses split with naive LLM | Naive file said \"no split\" | "
        "Naive file raised an error | PaSh's own file said \"no split\" | "
        "Parts: compiler stop (naive only / PaSh's own only) | Verdict |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in d["section1_commands"]:
        yn_n = "yes" if r["naive_has_file"] else "no"
        yn_p = "yes" if r["pash_own_has_file"] else "no"
        stop_cell = (
            f"naive: {r['compiler_stop_naive_only']['text']}; "
            f"PaSh's own: {r['compiler_stop_pash_own_only']['text']}"
        )
        lines.append(
            f"| `{r['command']}` | {yn_n} | {yn_p} | {r['uses_in_parts']['text']} | "
            f"{r['split_pash_own']['text']} | {r['split_naive']['text']} | "
            f"{r['naive_said_no_split']['text']} | {r['naive_raised']['text']} | "
            f"{r['pash_own_said_no_split']['text']} | {stop_cell} | `{r['verdict']}` |"
        )
    lines.append("")
    lines.append(
        "**Notes on Section 1:**"
    )
    lines.append(
        "- **Compiler-stop attribution:** Across the 177 distinct parts, PaSh's compiler stopped "
        "(`outcome == \"pash crash\"`) in 4 parts under PaSh's own files and 4 parts under the naive LLM's "
        "files. Two stops are shared under both sets (`covid/5` `AssertionError`; `oneliners/bi-grams` "
        "`NameError: name 'Arg' is not defined`). Two stops occur **only under the naive LLM**: "
        "`unixfun/34` and `unixfun/36`, both `AssertionError` in `pipe_append` because naive's `fmt` "
        "file misparsed `-w1` as a filename operand (`stdin: False` in a non-first pipeline stage; PaSh's "
        "own has no `fmt` file, so those parts stopped with `missing annotation`). Two stops occur "
        "**only under PaSh's own**: `unixfun/12` and `unixfun/16`, both `AssertionError` in `pipe_append` "
        "because PaSh's own `tail` file misparsed `-n 1` as a filename operand `1` (`stdin: False`; "
        "naive's `tail` file parsed `-n 1` with `stdin: True`, so both parts ran in parallel). "
        "Attributing each differential stop to the unique non-first command reporting `stdin: False` "
        "in `full_run/answers/*.jsonl.gz` assigns `2 of 2` parts to `fmt` (naive only) and `2 of 3` "
        "parts to `tail` (PaSh's own only). Co-occurring command counts for those parts are also "
        "recorded in `per_command.json`."
    )
    lines.append(
        "- **Why `tr`, `sort`, `cut`, `grep` split more under naive:** In `unixfun/12` and `unixfun/16`, "
        "avoiding PaSh's own `tail` crash accounts for all of naive's gains on `cut` (+3 uses) and `grep` "
        "(+1 use), 3 of 7 gained uses on `sort`, and 2 of 11 gained uses on `tr`. The remaining gains "
        "come directly from the commands' own files: `cat` (+43 single-file splits), `tr` (+9 `tr -d '\\n'` "
        "uses where PaSh's own allows only an unimplemented split), `awk` (+7 uses where PaSh's own gives "
        "`no answer`), and `sort` (+4 `sort -u` uses in `covid/1`–`4` where PaSh's own says `no split`)."
    )
    lines.append(
        "- **`file_answer` vs `direct_file_answer`:** For naive, `sed` says `no split` in 36 of 37 uses "
        "as PaSh passes the arguments (quotes kept on the script argument) vs 24 of 37 directly with "
        "quotes removed; `head` says `no split` in 7 of 10 uses as PaSh passes them vs 1 of 10 directly "
        "(the other 6 return an unimplemented split directly). PaSh's own files never raised an error "
        "(`0 of 609`)."
    )
    lines.append("")

    # ---- Section 2
    lines.append("## 2. Totals by File-Ownership Group")
    lines.append("")
    lines.append(
        "Totals over the 44 commands used inside parts (the 3 ownership groups with at least one file, "
        "plus the \"Neither has a file\" group so all counts reconcile to 44 commands and 609 uses). "
        "Only **1 of 44** commands in parts (`bigrams_aux`, 1 use in `oneliners/bi-grams`) has a file "
        "only in PaSh's own package — near none, because PaSh's other 9 PaSh-only files in `manifest.json` "
        "are internal benchmark helpers and test stubs (`alt_bigram_aux_reduce`, `alt_bigrams_aux`, "
        "`bigram_aux_map`, `bigram_aux_reduce`, `custom_sort`, `custom_tr`, `set_diff`, `test_one`, "
        "`test_two`) that do not appear in the suite's parts."
    )
    lines.append("")
    lines.append(
        "| Group | Commands (in parts) | Uses in parts | Uses split (PaSh's own) | "
        "Uses split (naive LLM) | Compiler stops (naive only / PaSh's own only) | "
        "Files raising (naive / PaSh's own) |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for g in d["section2_groups"]:
        stop_str = (
            f"naive: {g['compiler_stops_naive_only']['text']}; "
            f"PaSh's own: {g['compiler_stops_pash_own_only']['text']}"
        )
        raise_str = (
            f"naive: {g['files_raising_uses_naive']['text']}"
            + (f" ({', '.join(f'`{c}`' for c in g['files_raising_commands_naive'])})" if g['files_raising_commands_naive'] else "")
            + f"; PaSh's own: {g['files_raising_uses_pash_own']['text']}"
        )
        lines.append(
            f"| {g['label']} | {g['commands']['text']} | {g['uses']['text']} | "
            f"{g['split_pash_own']['text']} | {g['split_naive']['text']} | {stop_str} | {raise_str} |"
        )
    lines.append("")
    lines.append(
        f"**Full package inventory (`manifest.json`):** The naive LLM wrote files for "
        f"{mc['naive_total_files']} commands and PaSh's own package has {mc['pash_own_total_files']}: "
        f"{mc['both_files']} overlap (18 in parts; `tee` only outside parts; `mv` unused), "
        f"{mc['naive_only_total_files']} are naive-only (5 in parts; 4 outside parts only: "
        f"`convert`, `iconv`, `ls`, `mktemp`; {mc['naive_only_unused_in_suite_count']} unused in the 86 scripts), "
        f"and {mc['pash_own_only_total_files']} are PaSh-only (1 in parts: `bigrams_aux`; 9 unused)."
    )
    lines.append("")

    # ---- Section 3
    lines.append("## 3. What the Naive LLM Adds (Commands Where Only the Naive LLM Has a File)")
    lines.append("")
    lines.append(
        "Without a file, PaSh splits none of these commands, so any split here would be a pure gain. "
        "In practice, **0 of 39** uses of the 5 naive-only commands inside parts were split by PaSh: "
        "`mkdir` (31 uses) was rightly marked non-splittable; `join` (3 uses) rightly refused 1 use "
        "and raised an argument-parser exception on 2; `rev` (2 uses) was rightly marked splittable "
        "but its part hit an unrelated `NotImplementedError` on a redirection; `mogrify` (1 use) was "
        "marked `INDIV_FILES` splittable but rejected by PaSh as non-streaming output (`OTHER_OUTPUT`); "
        "and `fmt` (2 uses) was wrongly parsed and marked splittable, turning 2 `missing annotation` "
        "parts into PaSh compiler stops (`pash crash`)."
    )
    lines.append("")
    lines.append("### 3.1 Commands Used Inside Parts (5 commands, 39 uses)")
    lines.append("")
    lines.append(
        "| Command | Uses in parts | Naive file said | Split in PaSh | What happened to parts | "
        "Answer right in general? | Notes |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for item in d["section3_naive_only"]["in_parts"]:
        fa_str = ", ".join(f"{k}: {v} of {item['uses_in_parts']}" for k, v in sorted(item["file_answers"].items()))
        trans_str = ", ".join(f"{k} ({v})" for k, v in sorted(item["part_outcome_transitions"].items()))
        lines.append(
            f"| `{item['command']}` | {item['uses_in_parts']} of {sc['uses_in_parts']} | {fa_str} | "
            f"{item['split_in_pash']['text']} | {trans_str} | **{item['judgement']}** | {item['explanation']} |"
        )
    lines.append("")
    lines.append(
        "### 3.2 Commands Exercised Only Outside Parts (4 commands in `commands.jsonl.gz` / `answers/`)"
    )
    lines.append("")
    lines.append(
        "Four additional naive-only commands ran in the suite only outside PaSh parts (so PaSh never "
        "compiled them, though `full_run/answers/*.jsonl.gz` recorded the naive files' direct answers). "
        f"The other {mc['naive_only_unused_in_suite_count']} naive-only files were not called by any script."
    )
    lines.append("")
    lines.append(
        "| Command | Scripts | Naive file direct answer | Answer right in general? | Notes |"
    )
    lines.append("|---|---|---|---|---|")
    for item in d["section3_naive_only"]["outside_parts_only"]:
        parts_ans = []
        if item["allows_split_lines"]:
            parts_ans.append(f"allows a split: {item['allows_split_lines']} of {item['answer_lines']}")
        if item["no_split_lines"]:
            parts_ans.append(f"no split: {item['no_split_lines']} of {item['answer_lines']}")
        if item["raised_lines"]:
            parts_ans.append(f"raised: {item['raised_lines']} of {item['answer_lines']}")
        lines.append(
            f"| `{item['command']}` | {item['scripts_count']} of {sc['scripts']} | {', '.join(parts_ans)} | "
            f"**{item['judgement']}** | {item['explanation']} |"
        )
    lines.append("")

    # ---- Section 4
    w = d["section4_wall_clock"]
    nb = w["noise_band_pash_own_copy_vs_pash_own"]
    lines.append("## 4. Wall-Clock Time")
    lines.append("")
    lines.append(
        "Per-command wall-clock time cannot be separated because all of a source's annotation files were "
        "swapped in at once (Tiran's decision, 2026-11-24), so any script-level timing difference belongs "
        "to the source as a whole. The only per-command time evidence in this run comes from scripts where "
        "exactly one command's split differed between the naive LLM's files and PaSh's own."
    )
    lines.append("")
    lines.append(
        f"Across all {w['total_scripts']} scripts, {w['scripts_with_zero_split_diffs']} of {w['total_scripts']} "
        f"have identical splits under both sets, {w['scripts_with_multiple_differing_commands']} of "
        f"{w['total_scripts']} differ on 2 to 5 commands, and **{w['scripts_with_one_differing_command']} of "
        f"{w['total_scripts']}** differ on exactly one command — in **all 25**, that command is `cat` "
        "(1 single-file `cat` use split under naive and left unsplit under PaSh's own). No other command "
        "has a single-command-differing script."
    )
    lines.append("")
    cat_sum = w["single_command_summary"]["cat"]
    lines.append(
        f"Across those 25 `cat`-only scripts, the naive ÷ PaSh's own time ratio has geometric mean "
        f"**{cat_sum['geom_mean_ratio']:.2f}** (median **{cat_sum['median_ratio']:.2f}**, range "
        f"{cat_sum['min_ratio']:.2f}–{cat_sum['max_ratio']:.2f}; above 1 means naive is slower). "
        f"For reference, the identical second copy of PaSh's own files ranged from {nb['min']:.2f} to "
        f"{nb['max']:.2f} (median {nb['median']:.2f}); {cat_sum['slower_than_noise_band_max']['text']} "
        f"`cat`-only scripts are slower than that upper noise bound and "
        f"{cat_sum['faster_than_noise_band_min']['text']} are faster than the lower bound."
    )
    lines.append("")
    lines.append(
        "| Script | Sole differing command (naive vs PaSh's own) | PaSh's own median (s) | "
        "Naive LLM median (s) | Time ratio (naive ÷ PaSh's own) |"
    )
    lines.append("|---|---|---|---|---|")
    for row in w["single_command_scripts"]:
        delta = f"`{row['command']}` (+{row['gained_in_naive']} / -{row['lost_in_naive']})"
        lines.append(
            f"| `{row['script']}` | {delta} | {row['pash_own_seconds']:.2f} | "
            f"{row['naive_seconds']:.2f} | {row['ratio_naive_over_pash_own']:.2f} |"
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
