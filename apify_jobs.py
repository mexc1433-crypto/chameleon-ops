#!/usr/bin/env python3
"""
Chameleon Job Discovery (fixed) - Apify LinkedIn Jobs -> scored queue (jobs_queue.json)
Usage: python3 apify_jobs.py "Job Title" "mena|remote|<country>" [rows]
Fixes: per-location run tracking (original had undefined run_id), merges into queue with dedupe.
Env: APIFY_API_TOKEN or APIFY_API_KEY
"""
import json, os, sys, time, urllib.request

TOKEN = os.environ.get("APIFY_API_TOKEN") or os.environ.get("APIFY_API_KEY", "")
ACTOR = "curious_coder~linkedin-jobs-scraper"
MATCH = ["marketing", "digital", "community", "content", "brand", "performance",
         "social media", "growth", "crm", "b2b", "media", "partnership", "communications",
         "sales", "outbound", "business development", "saas", "lead generation"]

MENA = ["Egypt", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman", "Bahrain", "Jordan", "Lebanon"]
title = sys.argv[1] if len(sys.argv) > 1 else "Marketing Manager"
mode = sys.argv[2] if len(sys.argv) > 2 else "mena"
if mode == "mena":
    LOCS = MENA
elif mode == "remote":
    LOCS = ["Remote", "Worldwide"]
else:
    LOCS = [mode]
rows = int(sys.argv[3]) if len(sys.argv) > 3 else 20
rows = max(3, rows // len(LOCS))


def api(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 headers={"Authorization": "Bearer " + TOKEN,
                                          "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())


run_ids = []
for loc in LOCS:
    try:
        r = api(f"https://api.apify.com/v2/acts/{ACTOR}/runs", {"title": title, "location": loc, "rows": rows})
        rid = r["data"]["id"]
        run_ids.append((loc, rid))
        print("RUN", loc, rid, flush=True)
    except Exception as e:
        print("RUN_FAIL", loc, str(e)[:100], flush=True)

if not run_ids:
    print("NO_RUNS")
    sys.exit(1)

statuses = {rid: "RUNNING" for _, rid in run_ids}
deadline = time.time() + 900
while time.time() < deadline:
    time.sleep(15)
    done = True
    for _, rid in run_ids:
        if statuses[rid] in ("SUCCEEDED", "FAILED", "ABORTED"):
            continue
        try:
            st = api(f"https://api.apify.com/v2/actor-runs/{rid}")["data"]["status"]
        except Exception:
            st = "UNKNOWN"
        statuses[rid] = st
        if st not in ("SUCCEEDED", "FAILED", "ABORTED"):
            done = False
    print("status:", {r: statuses[r] for _, r in run_ids}, flush=True)
    if done:
        break

out = []
for loc, rid in run_ids:
    if statuses[rid] != "SUCCEEDED":
        continue
    try:
        items = api(f"https://api.apify.com/v2/actor-runs/{rid}/dataset/items?clean=true&format=json")
    except Exception:
        continue
    if isinstance(items, dict):
        items = items.get("data", {}).get("items", items.get("items", []))
    for j in items:
        url = j.get("jobUrl") or j.get("url") or ""
        desc = (j.get("description") or "")[:3000]
        text = (str(j.get("title", "")) + " " + desc).lower()
        score = 0
        hits = [m for m in MATCH if m in text]
        score += min(2 * len(hits), 8)
        posted = str(j.get("postedDate") or j.get("postedAt") or "")
        if posted:
            try:
                ts = time.mktime(time.strptime(posted[:19], "%Y-%m-%dT%H:%M:%S"))
                days = (time.time() - ts) / 86400
                score += 3 if days < 1 else (2 if days < 3 else (1 if days < 7 else 0))
            except Exception:
                pass
        out.append({"title": j.get("title"), "company": j.get("companyName") or j.get("company"),
                    "location": j.get("location"), "url": url, "posted": posted,
                    "match_score": score, "source": "apify/linkedin",
                    "easy_apply": "?", "remote": "remote" in text or "عن بعد" in text,
                    "description": desc})

try:
    cur = json.load(open("jobs_queue.json"))
except Exception:
    cur = []
seen = {j.get("url") for j in cur}
merged = cur + [j for j in out if j.get("url") and j["url"] not in seen]
merged.sort(key=lambda x: -x.get("match_score", 0))
json.dump(merged, open("jobs_queue.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"QUEUED +{len(merged)-len(cur)} (total {len(merged)}) -> jobs_queue.json")
for j in sorted(out, key=lambda x: -x.get("match_score", 0))[:8]:
    print(f"  [{j['match_score']}] {j['title']} @ {j['company']} ({j['posted'][:10]})")
