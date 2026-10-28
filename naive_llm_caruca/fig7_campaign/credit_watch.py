"""Warn before the money runs out (task 019; Tiran, 2026-10-28: "warn me if we are depleting available credits").

    python3 credit_watch.py [--below 40] [--every 600]

Every 10 minutes, reads what is left: the key's monthly limit remaining (GET /api/v1/key) and the account's
unused credit (GET /api/v1/credits), and takes the smaller. Appends one line to credit_watch.log each time.
Exits with a WARNING line once that falls below --below dollars, or quietly once no batch driver
(run_campaign.py) is running. The key is read from the repo's .env and never printed.
"""
import argparse, datetime, json, subprocess, sys, time, urllib.request, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_campaign as rc  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--below", type=float, default=40.0)
ap.add_argument("--every", type=int, default=600)
args = ap.parse_args()
k = rc.key()
LOG = os.path.join(rc.HERE, "credit_watch.log")


def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {k}"})
    return json.load(urllib.request.urlopen(req, timeout=30))["data"]


while True:
    try:
        key, cred = get("https://openrouter.ai/api/v1/key"), get("https://openrouter.ai/api/v1/credits")
        key_left = key.get("limit_remaining")
        acct_left = cred["total_credits"] - cred["total_usage"]
        left = min(x for x in (key_left, acct_left) if x is not None)
        line = (f"{datetime.datetime.now():%Y-%m-%d %H:%M}  left ${left:.2f}  (key: ${key_left:.2f} of its "
                f"${key.get('limit')} monthly limit; account: ${acct_left:.2f} of ${cred['total_credits']})")
    except Exception as e:  # a failed reading is logged, not fatal
        left, line = None, f"{datetime.datetime.now():%Y-%m-%d %H:%M}  reading failed: {type(e).__name__}"
    open(LOG, "a").write(line + "\n")
    if left is not None and left < args.below:
        print("WARNING: " + line, flush=True)
        sys.exit(0)
    driver = subprocess.run(["pgrep", "-f", "[r]un_campaign.py"], capture_output=True, text=True)
    if driver.returncode != 0:
        print("no batch running; " + line, flush=True)
        sys.exit(0)
    time.sleep(args.every)
