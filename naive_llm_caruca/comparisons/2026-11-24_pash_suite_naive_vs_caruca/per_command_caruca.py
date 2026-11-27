#!/usr/bin/env python3
"""Copy of per_command.py for the Caruca expanded rerun (2026-11-26): Caruca's files against PaSh's own,
command by command. The counting code is per_command.py's with the set names changed ("target" -> the target
set, a Caruca set); its hand-written notes (which described the target LLM's run) are replaced by a renderer
that prints only counts, plus a wrong-output table. The target LLM's general-knowledge judgements are not
carried over: Caruca-only commands are "not judged".

    python3 -I per_command_caruca.py caruca-main-all     # or caruca-pash-all

Reads full_run_caruca_all/; writes full_run_caruca_all/per_command_<set>.md and .json.
"""
import glob
import gzip
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
RECORDS = HERE / "full_run_caruca_all"
TARGET = sys.argv[1] if len(sys.argv) > 1 else "caruca-main-all"
OUT_MD = RECORDS / f"per_command_{TARGET}.md"
OUT_JSON = RECORDS / f"per_command_{TARGET}.json"

REF = "pash-own"
ANSWER_METHOD = "as PaSh passes them"

NOT_JUDGED = {"judgement": "not judged", "unsure": True,
              "explanation": "Not judged in this rerun (qualitative judgements are done separately)."}


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
    target_only_parts = []
    pash_only_parts = []
    both_crash_parts = []

    target_only_culprit = defaultdict(set)  # cmd -> set of part keys (id, text_sha)
    pash_only_culprit = defaultdict(set)
    target_only_coocc = defaultdict(set)
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
                "reason_target": rn[rk]["reason"],
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
                target_only_coocc[cmd].add(rk)
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
                target_only_culprit[cmd].add(rk)
            else:
                pash_only_culprit[cmd].add(rk)

        if n_crash:
            target_only_parts.append(entry)
        else:
            pash_only_parts.append(entry)

    return {
        "target_only_parts": target_only_parts,
        "pash_only_parts": pash_only_parts,
        "both_crash_parts": both_crash_parts,
        "target_only_culprit": target_only_culprit,
        "pash_only_culprit": pash_only_culprit,
        "target_only_coocc": target_only_coocc,
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
    target_manifest_cmds = (
        set(manifest["caruca"][TARGET].keys())
    )

    # Filter occurrences: phase == "main", mode == "instrumented", inside parts (outside_pash == False).
    po = {}
    na = {}
    outside_target = defaultdict(list)
    for o in occ_all:
        if o["phase"] != "main" or o["mode"] != "instrumented":
            continue
        if o["outside_pash"]:
            if o["set"] == TARGET:
                outside_target[o["command"]].append(o)
            continue
        key = (base_id(o["id"]), o["region_text_sha"], o["position"])
        if o["set"] == REF:
            assert key not in po, f"Duplicate occurrence key in {REF}: {key}"
            po[key] = o
        elif o["set"] == TARGET:
            assert key not in na, f"Duplicate occurrence key in {TARGET}: {key}"
            na[key] = o

    assert set(po) == set(na), "Occurrence keys differ between pash-own and target"
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

    assert set(rp) == set(rn), "Region keys differ between pash-own and target"
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
        if has_n_occ != (cmd in target_manifest_cmds):
            source_manifest_mismatches.append((TARGET, cmd, sorted(src_n), cmd in target_manifest_cmds))
        if has_p_occ != (cmd in pash_stock):
            source_manifest_mismatches.append(("pash-own", cmd, sorted(src_p), cmd in pash_stock))
    assert not source_manifest_mismatches, f"Source/manifest mismatch: {source_manifest_mismatches}"

    # ---- Section 1: per-command table (one row per command used inside a part, sorted by uses desc)
    section1 = []
    for cmd, ks in sorted(by_cmd.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        n_uses = len(ks)
        n_parts = len(parts_by_cmd[cmd])
        has_target = cmd in target_manifest_cmds
        has_pash = cmd in pash_stock

        split_pash = sum(po[k]["split"] is True for k in ks)
        split_target = sum(na[k]["split"] is True for k in ks)
        gained_uses = sum((na[k]["split"] is True) and not (po[k]["split"] is True) for k in ks)
        lost_uses = sum((po[k]["split"] is True) and not (na[k]["split"] is True) for k in ks)

        target_no_split = sum(na[k]["file_answer"] == "says no split" for k in ks)
        target_no_split_direct = sum(na[k]["direct_file_answer"] == "says no split" for k in ks)
        target_raised = sum(na[k]["file_answer"] == "raised" or na[k]["exception"] is not None for k in ks)
        pash_no_split = sum(po[k]["file_answer"] == "says no split" for k in ks)
        pash_raised = sum(po[k]["file_answer"] == "raised" or po[k]["exception"] is not None for k in ks)

        stop_target_only = len(stops["target_only_culprit"].get(cmd, set()))
        stop_pash_only = len(stops["pash_only_culprit"].get(cmd, set()))
        stop_target_only_coocc = len(stops["target_only_coocc"].get(cmd, set()))
        stop_pash_only_coocc = len(stops["pash_only_coocc"].get(cmd, set()))

        if has_target and not has_pash:
            verdict = "Caruca only"
        elif split_target > split_pash:
            verdict = "Caruca splits more"
        elif split_target < split_pash:
            verdict = "Caruca splits less"
        elif split_target == 0 and split_pash == 0:
            verdict = "neither splits"
        else:
            verdict = "same"

        if has_target and has_pash:
            group = "both"
        elif has_target and not has_pash:
            group = "target_only"
        elif not has_target and has_pash:
            group = "pash_only"
        else:
            group = "neither"

        section1.append({
            "command": cmd,
            "group": group,
            "target_has_file": has_target,
            "pash_own_has_file": has_pash,
            "uses_in_parts": rate(n_uses, total_uses),
            "parts_with_command": rate(n_parts, total_parts),
            "split_pash_own": rate(split_pash, n_uses),
            "split_target": rate(split_target, n_uses),
            "gained_uses": gained_uses,
            "lost_uses": lost_uses,
            "target_said_no_split": rate(target_no_split, n_uses),
            "target_said_no_split_direct": rate(target_no_split_direct, n_uses),
            "target_raised": rate(target_raised, n_uses),
            "pash_own_said_no_split": rate(pash_no_split, n_uses),
            "pash_own_raised": rate(pash_raised, n_uses),
            "compiler_stop_target_only": rate(stop_target_only, n_parts),
            "compiler_stop_pash_own_only": rate(stop_pash_only, n_parts),
            "compiler_stop_target_only_cooccurring_parts": rate(stop_target_only_coocc, n_parts),
            "compiler_stop_pash_own_only_cooccurring_parts": rate(stop_pash_only_coocc, n_parts),
            "verdict": verdict,
        })

    # ---- Section 2: totals for the three groups (+ neither for reconciliation)
    total_cmds = len(section1)
    group_specs = [
        ("both", "Both have files"),
        ("target_only", "Only Caruca has a file"),
        ("pash_only", "Only PaSh's own has a file"),
        ("neither", "Neither has a file (reconciliation)"),
    ]
    section2 = []
    for gkey, glabel in group_specs:
        rows = [r for r in section1 if r["group"] == gkey]
        g_cmds = [r["command"] for r in rows]
        g_uses = sum(r["uses_in_parts"]["a"] for r in rows)
        g_sp_pash = sum(r["split_pash_own"]["a"] for r in rows)
        g_sp_target = sum(r["split_target"]["a"] for r in rows)
        g_stop_n = sum(r["compiler_stop_target_only"]["a"] for r in rows)
        g_stop_p = sum(r["compiler_stop_pash_own_only"]["a"] for r in rows)
        g_raise_n = sum(r["target_raised"]["a"] for r in rows)
        g_raise_p = sum(r["pash_own_raised"]["a"] for r in rows)
        g_raise_n_cmds = sorted(r["command"] for r in rows if r["target_raised"]["a"] > 0)
        g_raise_p_cmds = sorted(r["command"] for r in rows if r["pash_own_raised"]["a"] > 0)
        section2.append({
            "group": gkey,
            "label": glabel,
            "commands": rate(len(rows), total_cmds),
            "command_names": sorted(g_cmds),
            "uses": rate(g_uses, total_uses),
            "split_pash_own": rate(g_sp_pash, g_uses),
            "split_target": rate(g_sp_target, g_uses),
            "compiler_stops_target_only": rate(g_stop_n, total_parts),
            "compiler_stops_pash_own_only": rate(g_stop_p, total_parts),
            "files_raising_uses_target": rate(g_raise_n, g_uses),
            "files_raising_uses_pash_own": rate(g_raise_p, g_uses),
            "files_raising_commands_target": g_raise_n_cmds,
            "files_raising_commands_pash_own": g_raise_p_cmds,
        })

    # Manifest-level file coverage summary (all 82 target files vs 30 PaSh's own files).
    cmds_po_suite = {c["command"]: c["source"] for c in cmds_rec if c["set"] == REF}
    cmds_na_suite = {c["command"]: c["source"] for c in cmds_rec if c["set"] == TARGET}
    target_only_suite_cmds = sorted(c for c, s in cmds_na_suite.items() if s == "ours" and cmds_po_suite.get(c) == "none")
    target_only_in_parts = sorted(r["command"] for r in section1 if r["group"] == "target_only")
    target_only_outside_only = sorted(set(target_only_suite_cmds) - set(target_only_in_parts))

    manifest_coverage = {
        "target_total_files": len(target_manifest_cmds),
        "pash_own_total_files": len(pash_stock),
        "both_files": len(target_manifest_cmds & pash_stock),
        "both_not_in_parts": sorted((target_manifest_cmds & pash_stock) - set(by_cmd)),
        "target_only_total_files": len(target_manifest_cmds - pash_stock),
        "target_only_in_parts": target_only_in_parts,
        "target_only_outside_parts_only": target_only_outside_only,
        "target_only_unused_in_suite_count": len((target_manifest_cmds - pash_stock) - set(target_only_suite_cmds)),
        "pash_own_only_total_files": len(pash_stock - target_manifest_cmds),
        "pash_own_only_in_parts": sorted(r["command"] for r in section1 if r["group"] == "pash_only"),
        "pash_own_only_not_in_parts": sorted((pash_stock - target_manifest_cmds) - set(by_cmd)),
    }

    # ---- Section 3: What the target LLM adds
    section3_in_parts = []
    for cmd in sorted(target_only_in_parts, key=lambda c: (-len(by_cmd[c]), c)):
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
        j = NOT_JUDGED
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
    for cmd in target_only_outside_only:
        rows = [a for a in ans_all if a["set"] == TARGET and a["command"] == cmd]
        allow_lines = sum(r.get("lines", 1) for r in rows if r["allows_split"] is True)
        no_split_lines = sum(r.get("lines", 1) for r in rows if r["allows_split"] is False and not r["exception"])
        raised_lines = sum(r.get("lines", 1) for r in rows if r["exception"])
        total_lines = allow_lines + no_split_lines + raised_lines
        scripts = sorted({base_id(r["id"]) for r in rows})
        sample_invs = sorted({(r.get("example_invocation") or r.get("invocation") or "") for r in rows})[:2]
        j = NOT_JUDGED
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
        diff_cmds = defaultdict(lambda: {"gained_in_target": 0, "lost_in_target": 0})
        for k in by_script_uses.get(sid, []):
            sp_p = po[k]["split"] is True
            sp_n = na[k]["split"] is True
            if sp_p != sp_n:
                c = po[k]["command"]
                if sp_n:
                    diff_cmds[c]["gained_in_target"] += 1
                else:
                    diff_cmds[c]["lost_in_target"] += 1
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
                "gained_in_target": diff_cmds[cmd]["gained_in_target"],
                "lost_in_target": diff_cmds[cmd]["lost_in_target"],
                "pash_own_seconds": round(tp, 4),
                "target_seconds": round(tn, 4),
                "ratio_target_over_pash_own": round(ratio, 4),
            })
        else:
            multi_cmd_scripts.append({
                "script": sid,
                "commands": {c: dict(v) for c, v in sorted(diff_cmds.items())},
                "pash_own_seconds": round(tp, 4),
                "target_seconds": round(tn, 4),
                "ratio_target_over_pash_own": round(ratio, 4),
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
        rs = [r["ratio_target_over_pash_own"] for r in rows]
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
        "target_parallel_parts": sum(r["outcome"] == "parallelized" for r in rn.values()),
        "pash_own_split_uses": sum(o["split"] is True for o in po.values()),
        "target_split_uses": sum(o["split"] is True for o in na.values()),
        "pash_own_compiler_stops": sum(r["outcome"] == "pash crash" for r in rp.values()),
        "target_compiler_stops": sum(r["outcome"] == "pash crash" for r in rn.values()),
        "differential_compiler_stops_unattributed": len(stops["unattributed"]),
        "source_manifest_mismatches": len(source_manifest_mismatches),
    }
    assert self_checks["scripts"] == 86
    assert self_checks["distinct_parts"] == 177
    assert self_checks["uses_in_parts"] == 609
    assert self_checks["pash_own_parallel_parts"] == 41
    assert self_checks["pash_own_split_uses"] == 126
    assert self_checks["pash_own_compiler_stops"] == 4
    assert self_checks["differential_compiler_stops_unattributed"] == 0

    payload = {
        "generated_by": "per_command_caruca.py", "target": TARGET, "wrong_outputs": wrong_outputs(results),
        "records_dir": "full_run_caruca_all",
        "fixups": fixup_log,
        "self_checks": self_checks,
        "manifest_coverage": manifest_coverage,
        "compiler_stops_detail": {
            "target_only": stops["target_only_parts"],
            "pash_own_only": stops["pash_only_parts"],
            "both": stops["both_crash_parts"],
        },
        "section1_commands": section1,
        "section2_groups": section2,
        "section3_target_only": {
            "in_parts": section3_in_parts,
            "outside_parts_only": section3_outside_only,
            "unused_in_suite_count": manifest_coverage["target_only_unused_in_suite_count"],
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


def wrong_outputs(results):
    """caruca-all: scripts whose output under TARGET differs from bash's in the same repeat, with the commands
    split under TARGET and not under PaSh's own (pass with the stand-in programs)."""
    inst = {(base_id(r["id"]), r["set"]): r for r in results if r["mode"] == "instrumented"}
    out = []
    for sid in sorted({base_id(r["id"]) for r in results}):
        rows = [r for r in results if base_id(r["id"]) == sid and r["set"] == TARGET]
        bad = [r for r in rows if not r["same_as_bash"]]
        if not bad:
            continue
        a, o = inst.get((sid, TARGET)), inst.get((sid, REF))
        out.append({"script": sid, "runs_differing": rate(len(bad), len(rows)),
                    "split_here_not_with_pash_own": sorted(set((a or {}).get("split_commands") or [])
                                                           - set((o or {}).get("split_commands") or []))})
    return out


def render_markdown(d: dict) -> str:
    sc, mc, T = d["self_checks"], d["manifest_coverage"], d["target"]
    name = {"caruca-pash-all": "Caruca's files, PaSh grammar (all converted)",
            "caruca-main-all": "Caruca, full grammar where traced"}.get(T, T)
    L = [f"# {name} vs PaSh's own files, command by command", "",
         f"Built by `per_command_caruca.py {T}` from `full_run_caruca_all/` ({sc['scripts']} scripts, "
         f"{sc['distinct_parts']} distinct parts, {sc['uses_in_parts']} command uses inside parts, "
         f"{sc['commands_in_parts']} distinct commands). Counts only. Splits and parts are from the pass with the "
         "stand-in programs; times are medians of the three timed repeats. 'Said no split' and 'raised' are the "
         "files' answers to the words as PaSh passes them. A compiler stop is a part whose outcome is 'pash crash' "
         "under one set and not the other.", ""]
    L += ["## 1. Per command (commands used inside parts)", "",
          "| Command | Caruca has a file | PaSh's own has a file | Uses in parts | Split with PaSh's own | "
          "Split with Caruca | Caruca said no split | Caruca raised | PaSh's own said no split | "
          "Compiler stops (Caruca only / PaSh's own only) | Verdict |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in d["section1_commands"]:
        L.append(f"| `{r['command']}` | {'yes' if r['target_has_file'] else 'no'} | "
                 f"{'yes' if r['pash_own_has_file'] else 'no'} | {r['uses_in_parts']['text']} | "
                 f"{r['split_pash_own']['text']} | {r['split_target']['text']} | {r['target_said_no_split']['text']} | "
                 f"{r['target_raised']['text']} | {r['pash_own_said_no_split']['text']} | "
                 f"{r['compiler_stop_target_only']['text']} / {r['compiler_stop_pash_own_only']['text']} | `{r['verdict']}` |")
    stops = d["compiler_stops_detail"]
    L += ["", "Compiler stops under Caruca only: " + (", ".join(
        f"`{p['script']}` ({(p['crashing_reason'] or '')[:80]}; culprit: {', '.join(p['culprit_commands']) or 'not attributed'})"
        for p in stops["target_only"]) or "none") + ".", "",
          "Compiler stops under PaSh's own only: " + (", ".join(
        f"`{p['script']}` (culprit: {', '.join(p['culprit_commands']) or 'not attributed'})"
        for p in stops["pash_own_only"]) or "none") + ".", ""]
    L += ["## 2. Totals by who has a file", "",
          "| Group | Commands (in parts) | Uses in parts | Split (PaSh's own) | Split (Caruca) | "
          "Compiler stops (Caruca only / PaSh's own only) | Uses whose file raised (Caruca / PaSh's own) |",
          "|---|---|---|---|---|---|---|"]
    for g in d["section2_groups"]:
        L.append(f"| {g['label']} | {g['commands']['text']} | {g['uses']['text']} | {g['split_pash_own']['text']} | "
                 f"{g['split_target']['text']} | {g['compiler_stops_target_only']['text']} / "
                 f"{g['compiler_stops_pash_own_only']['text']} | {g['files_raising_uses_target']['text']} / "
                 f"{g['files_raising_uses_pash_own']['text']} |")
    L += ["", f"Files (`manifest.json`): Caruca {mc['target_total_files']} commands, PaSh's own "
          f"{mc['pash_own_total_files']}; both {mc['both_files']}; Caruca only {mc['target_only_total_files']} "
          f"(in parts: {', '.join(f'`{c}`' for c in mc['target_only_in_parts']) or 'none'}; outside parts only: "
          f"{', '.join(f'`{c}`' for c in mc['target_only_outside_parts_only']) or 'none'}; not called by any script: "
          f"{mc['target_only_unused_in_suite_count']}); PaSh's own only {mc['pash_own_only_total_files']}.", ""]
    L += ["## 3. Wrong output", "",
          "Scripts whose printed output under this set differs from plain bash's (same repeat), and the commands "
          "PaSh split with this set but not with its own files there.", "",
          "| Script | Runs differing from bash | Split with Caruca, not with PaSh's own |", "|---|---|---|"]
    for w_ in d["wrong_outputs"]:
        L.append(f"| `{w_['script']}` | {w_['runs_differing']['text']} | "
                 f"{', '.join(f'`{c}`' for c in w_['split_here_not_with_pash_own']) or '-'} |")
    if not d["wrong_outputs"]:
        L.append("| none | | |")
    w = d["section4_wall_clock"]; nb = w["noise_band_pash_own_copy_vs_pash_own"]
    L += ["", "## 4. Time where exactly one command's split differs", "",
          f"All of a source's files are swapped in at once, so a time difference belongs to the source. Of "
          f"{w['total_scripts']} scripts, {w['scripts_with_zero_split_diffs']} split the same under both sets, "
          f"{w['scripts_with_one_differing_command']} differ on one command and "
          f"{w['scripts_with_multiple_differing_commands']} on more than one. Noise (second copy of PaSh's own ÷ "
          f"PaSh's own): {nb['min']:.2f} to {nb['max']:.2f}, median {nb['median']:.2f}.", "",
          "| Command | Scripts | Time ratio Caruca ÷ PaSh's own, geometric mean (min-max) | Above the noise band | Below it |",
          "|---|---|---|---|---|"]
    for c, s in w["single_command_summary"].items():
        L.append(f"| `{c}` | {s['scripts']['text']} | {s['geom_mean_ratio']:.2f} ({s['min_ratio']:.2f}-{s['max_ratio']:.2f}) | "
                 f"{s['slower_than_noise_band_max']['text']} | {s['faster_than_noise_band_min']['text']} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
