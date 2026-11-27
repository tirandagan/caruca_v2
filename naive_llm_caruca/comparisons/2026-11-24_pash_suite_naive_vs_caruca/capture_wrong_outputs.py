"""Re-run a few scripts whose output was wrong under Caruca's expanded files, keeping the printed output,
so the report can show concise diffs against bash (the batch deleted outputs after hashing them).

Run inside the pash VM:  python3 capture_wrong_outputs.py
Uses run_koala_caruca_all.run_one exactly as the batch did (plain mode, no stand-in programs), writes
~/t024/wrong_output_examples/ (copied to full_run_caruca_all/wrong_output_examples/)<script>__<set>.out and .diff, and checks each output's sha256
against the batch record, so the kept output is the same wrong output the batch saw.
"""
import difflib, gzip, hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_koala_caruca_all as rk

CASES = [("unixfun/26", "caruca-pash-all"), ("oneliners/top-n", "caruca-main-all"),
         ("oneliners/spell", "caruca-pash-all"), ("unixfun/23", "caruca-pash-all")]
dest = rk.ROOT / "wrong_output_examples"  # the repo mount is read-only in the VM; copied out afterwards
dest.mkdir(parents=True, exist_ok=True)
rec = [json.loads(l) for l in gzip.open(HERE / "full_run_caruca_all" / "results.jsonl.gz", "rt")]
def recorded(sid, sname):
    g, s = sid.split("/")
    return {r["out_sha256"] for r in rec if r["group"] == g and r["script"] == s and r["set"] == sname}
summary = []
for sid, sname in CASES:
    inv = rk.invocation(sid)
    rdir = Path("/tmp/wrong_examples") / sid.replace("/", "_"); rdir.mkdir(parents=True, exist_ok=True)
    outs = {}
    for who in ("bash", sname):
        res, standin, log, out = rk.run_one(who, inv, rdir, f"{who}_keep", shim=False)
        data = out.read_bytes(); outs[who] = data
        (dest / f"{sid.replace('/', '_')}__{who}.out").write_bytes(data)
    sha = hashlib.sha256(outs[sname]).hexdigest()
    same_as_batch = sha in recorded(sid, sname)
    a = outs["bash"].decode(errors="replace").splitlines(); b = outs[sname].decode(errors="replace").splitlines()
    diff = list(difflib.unified_diff(a, b, "bash", sname, n=1, lineterm=""))
    (dest / f"{sid.replace('/', '_')}__{sname}.diff").write_text("\n".join(diff) + "\n")
    summary.append({"script": sid, "set": sname, "bash_lines": len(a), "set_lines": len(b),
                    "bash_bytes": len(outs["bash"]), "set_bytes": len(outs[sname]),
                    "same_wrong_output_as_batch": same_as_batch, "diff_lines": len(diff)})
    print(json.dumps(summary[-1]))
(dest / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
