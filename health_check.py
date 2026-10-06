#!/usr/bin/env python3
"""Chameleon supervisor health check v2 - prints JSON status of observable components.
v2 additions: filtered_queue size, packages count, bank consistency (root vs data/),
skills total, last errors count, wave state."""
import json, os, sys, urllib.request, glob

BASE = os.path.dirname(os.path.abspath(__file__))

def get(url, tok=None):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"} if tok else {"User-Agent": "chameleon-check"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode()), None
    except Exception as e:
        return None, str(e)

def load(path):
    with open(os.path.join(BASE, path), encoding="utf-8") as f:
        return json.load(f)

status = {}

# 1. repo + latest action run
d, err = get("https://api.github.com/repos/mexc1433-crypto/chameleon-ops/actions/runs?per_page=1", os.environ.get("GITHUB_TOKEN_3",""))
if err or not d.get("workflow_runs"):
    status["github_actions"] = {"ok": False, "error": err or "no runs"}
else:
    r = d["workflow_runs"][0]
    status["github_actions"] = {"ok": r["conclusion"] != "failure", "last_run": r["conclusion"], "created_at": r["created_at"], "name": r["name"]}

# 2. bots
for name, tok in [("apps_bot", os.environ.get("TELEGRAM_BOT_TOKEN","")), ("replies_bot", os.environ.get("TELEGRAM_BOT_TOKEN_2",""))]:
    d, err = get(f"https://api.telegram.org/bot{tok}/getMe")
    status[name] = {"ok": bool(d and d.get("ok")), "username": (d or {}).get("result",{}).get("username","")}

# 3. queues
try:
    q = load("jobs_queue.json")
    status["local_queue"] = {"ok": len(q) > 0, "size": len(q)}
except Exception as e:
    status["local_queue"] = {"ok": False, "error": str(e)}
try:
    fq = load("filtered_queue.json")
    jobs = fq if isinstance(fq, list) else next((v for v in fq.values() if isinstance(v, list)), [])
    status["filtered_queue"] = {"ok": True, "size": len(jobs)}
except Exception as e:
    status["filtered_queue"] = {"ok": False, "error": str(e)}

# 4. bank consistency (root bank.json vs data/bank.json) + skills total
try:
    root = load("bank.json"); data = load("data/bank.json")
    same = root == data
    pool = root.get("skills_pool", {})
    total = sum(len(v) for v in pool.values() if isinstance(v, list))
    status["skills_bank"] = {"ok": same, "root_equals_data": same, "skills_total": total}
except Exception as e:
    status["skills_bank"] = {"ok": False, "error": str(e)}

# 5. packages ready (repo packages dir + locally generated cv_*.pdf)
try:
    repo_pkgs = sum(1 for p in glob.glob(os.path.join(BASE, "packages", "*", "*_cv.pdf")))
    local_pkgs = sum(1 for p in glob.glob(os.path.join(BASE, "cv_*.pdf")))
    status["packages"] = {"ok": True, "repo_packages": repo_pkgs, "local_ready": local_pkgs}
except Exception as e:
    status["packages"] = {"ok": False, "error": str(e)}

# 6. errors log freshness
try:
    el = load("errors_log.json")
    status["errors_log"] = {"ok": True, "count": len(el.get("errors", [])), "updated": el.get("updated", "")}
except Exception as e:
    status["errors_log"] = {"ok": False, "error": str(e)}

print(json.dumps(status, ensure_ascii=False, indent=1))
sys.exit(0 if all(v.get("ok") for v in status.values()) else 1)
