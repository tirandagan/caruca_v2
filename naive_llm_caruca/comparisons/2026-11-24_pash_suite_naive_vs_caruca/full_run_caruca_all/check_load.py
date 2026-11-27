#!/usr/bin/env python3
"""Runs in the pash VM. For each Caruca set: every swapped-in file is byte-identical to its source, its JSON
parses, both generator modules import in a fresh interpreter and their classes exist. Failures are recorded,
not fixed. Writes load_check.jsonl next to this script's output folder (T024_OUT)."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
OUT = Path(os.environ.get("T024_OUT", Path.home() / "t024/out_caruca_all"))
man = json.loads((OUT / "manifest.json").read_text())
PROBE = r'''
import importlib, json, sys
sys.path.insert(0, sys.argv[1]); C = sys.argv[2]; c = sys.argv[3]
import pash_annotations.annotation_generation.AnnotationGeneration as AG
G = "pash_annotations.annotation_generation.annotation_generators."
r = {"in_name_table": AG.DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(c) == C}
for k in ("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"):
    try:
        getattr(importlib.import_module(G + k + C), k + C); r[k] = "ok"
    except Exception as e:
        r[k] = f"{type(e).__name__}: {e}"[:300]
print(json.dumps(r))
'''
rows = []
for s in ("caruca-pash-all", "caruca-main-all"):
    root = Path(man["sets"][s]["folder"]); pkg = root / "pash_annotations"
    for c, v in man["caruca"][s].items():
        C = "".join(p.capitalize() for p in c.split("_"))
        files = {f"{c}.json": pkg / "parser/command_flag_option_info/data" / f"{c}.json",
                 f"InputOutputInfoGenerator{C}.py": pkg / "annotation_generation/annotation_generators" / f"InputOutputInfoGenerator{C}.py",
                 f"ParallelizabilityInfoGenerator{C}.py": pkg / "annotation_generation/annotation_generators" / f"ParallelizabilityInfoGenerator{C}.py"}
        same = all(hashlib.sha256(p.read_bytes()).hexdigest() == v["files"][n] for n, p in files.items())
        try:
            json.loads(files[f"{c}.json"].read_text()); js = "ok"
        except Exception as e:
            js = f"{type(e).__name__}: {e}"[:200]
        p = subprocess.run([sys.executable, "-I", "-c", PROBE, str(root), C, c], capture_output=True, text=True)
        r = json.loads(p.stdout) if p.stdout.strip() else {"probe_error": p.stderr.strip()[-300:]}
        row = {"set": s, "command": c, "source": v["source"], "bytes_same_as_source": same, "json": js} | r
        row["loads"] = same and js == "ok" and r.get("InputOutputInfoGenerator") == "ok" and \
            r.get("ParallelizabilityInfoGenerator") == "ok" and r.get("in_name_table") is True
        rows.append(row)
with open(OUT / "load_check.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r, sort_keys=True) + "\n")
bad = [r for r in rows if not r["loads"]]
print(f"{len(rows)} files checked, {len(rows) - len(bad)} load, {len(bad)} fail")
for r in bad:
    print(json.dumps(r))
