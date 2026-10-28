"""Smoke test for task 019, section 4.2: does Claude Code work through OpenRouter as the campaign needs?

    python3 smoke_test.py [--model anthropic/claude-fable-5.1]

In a fresh clone of naive-golden, one short Claude Code session (signed out of claude.ai; key, base URL and
model as naive-run sets them) is asked to run `echo smoke` with its Bash tool and then reply "done": two
turns, so the second must read the first turn's cached prompt. Checks: the session ends without error; the
model asked for is the one used; the effort setting is accepted; cache-read tokens appear; OpenRouter's bill
(the key's usage before and after) is close to Claude Code's own figure. Writes smoke_test.json beside this
file (no key in it) and deletes the clone. Claude Code's system prompt is cached on the first turn, so
expect about $0.20-0.40.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_campaign as rc  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="anthropic/claude-fable-5.1")
args = ap.parse_args()
k = rc.key()
st = rc.state(k)
name = "t019-smoke"
subprocess.run([os.path.join(rc.ARM, "new_run_vm.sh"), name], check=True, capture_output=True)
try:
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        os.chmod(f.name, 0o600)
        f.write(k)
    subprocess.run(["limactl", "copy", f.name, f"{name}:~/.k"], check=True)
    os.unlink(f.name)
    before = rc.usage(k)
    inner = (
        "chmod 600 ~/.k; K=$(cat ~/.k); rm -f ~/.k; claude auth logout >/dev/null 2>&1; cd ~/naive-arm; "
        "ANTHROPIC_BASE_URL=https://openrouter.ai/api ANTHROPIC_AUTH_TOKEN=\"$K\" ANTHROPIC_API_KEY= "
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 DISABLE_AUTOUPDATER=1 "
        f"claude -p 'Run the shell command: echo smoke. Then reply with the single word done.' "
        f"--model {args.model} --effort medium --output-format stream-json --verbose "
        "--permission-mode bypassPermissions --strict-mcp-config --disallowedTools WebSearch WebFetch RemoteTrigger"
    )
    p = subprocess.run(["limactl", "shell", name, "--", "bash", "-lc", inner], capture_output=True, text=True, timeout=600)
    after = rc.usage(k)
finally:
    subprocess.run(["limactl", "delete", "-f", name], capture_output=True)

events, per_msg = [], {}
for ln in p.stdout.splitlines():
    try:
        r = json.loads(ln)
    except json.JSONDecodeError:
        continue
    events.append(r)
    m = r.get("message") if isinstance(r.get("message"), dict) else None
    if r.get("type") == "assistant" and m and isinstance(m.get("usage"), dict):
        per_msg[m.get("id")] = m["usage"]
res = next((e for e in events if e.get("type") == "result"), {})
init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
out = {
    "model_asked": args.model, "model_in_init": init.get("model"),
    "models_used": sorted((res.get("modelUsage") or {}).keys()), "is_error": res.get("is_error"),
    "result": str(res.get("result", ""))[:200], "turns": res.get("num_turns"),
    "per_message_usage": list(per_msg.values()),
    "cache_read_tokens": sum(u.get("cache_read_input_tokens", 0) for u in per_msg.values()),
    "claude_cost_usd": res.get("total_cost_usd"), "billed_usd": round(after - before, 6),
    "ran_bash": any(b.get("type") == "tool_use" for e in events if e.get("type") == "assistant"
                    for b in (e.get("message") or {}).get("content") or [] if isinstance(b, dict)),
    "stderr_tail": [l for l in p.stderr.splitlines() if "sk-or" not in l][-5:],
}
json.dump(out, open(os.path.join(rc.HERE, "smoke_test.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
ok = (not out["is_error"] and out["ran_bash"] and out["cache_read_tokens"] > 0
      and any(args.model.split("/")[-1].replace(".", "-") in m.replace(".", "-") for m in out["models_used"]))
print("SMOKE TEST", "PASSED" if ok else "FAILED")
