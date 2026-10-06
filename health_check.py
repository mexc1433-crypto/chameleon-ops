#!/usr/bin/env python3
"""Chameleon supervisor health check - prints JSON status of observable components."""
import json, os, sys, urllib.request
def get(url, tok=None):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"} if tok else {"User-Agent": "chameleon-check"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode()), None
    except Exception as e:
        return None, str(e)
status = {}
# 1. repo + latest action run
d, err = get("https://api.github.com/repos/mexc1433-crypto/chameleon-ops/actions/runs?per_page=1", os.environ.get("GITHUB_TOKEN_3",""))
if err: status["github_actions"] = {"ok": False, "error": err}
else:
    r = d["workflow_runs"][0]
    status["github_actions"] = {"ok": r["conclusion"] != "failure", "last_run": r["conclusion"], "created_at": r["created_at"]}
# 2. bots
for name, tok in [("apps_bot", os.environ.get("TELEGRAM_BOT_TOKEN","")), ("replies_bot", os.environ.get("TELEGRAM_BOT_TOKEN_2",""))]:
    d, err = get(f"https://api.telegram.org/bot{tok}/getMe")
    status[name] = {"ok": bool(d and d.get("ok")), "username": (d or {}).get("result",{}).get("username","")}
# 3. queue
try:
    q = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs_queue.json")))
    status["local_queue"] = {"ok": len(q) > 0, "size": len(q)}
except Exception as e:
    status["local_queue"] = {"ok": False, "error": str(e)}
print(json.dumps(status, ensure_ascii=False, indent=1))
sys.exit(0 if all(v.get("ok") for v in status.values()) else 1)
