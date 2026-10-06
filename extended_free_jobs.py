#!/usr/bin/env python3
"""
extended_free_jobs.py — بدائل Apify المجانية (بديل غير معتمد على حد الاستهلاك)
Sources: Arbeitnow, RemoteOK, Himalayas, WeWorkRemotely (RSS), Remotive API, Jobicy API.
All free, no API keys. Merges into jobs_queue.json with dedupe.
"""
import json, os, re, sys, time, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(BASE, "jobs_queue.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 chameleon-ops"}

def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def fetch_json(url):
    return json.loads(get(url))

def now():
    return datetime.now(timezone.utc).isoformat()[:10]

new_jobs = []

def add(title, company, location, url, description="", source=""):
    if not title or not company or not url:
        return
    new_jobs.append({
        "title": title.strip()[:120], "company": company.strip()[:80],
        "location": location.strip()[:80], "url": url.strip(),
        "description": (description or "")[:4000], "source": source, "pulled": now(),
    })

# 1) Arbeitnow — free, no key
try:
    d = fetch_json("https://www.arbeitnow.com/api/job-board-api")
    for j in d.get("data", [])[:40]:
        loc = j.get("location") or "Remote"
        if j.get("remote"):
            loc = "Remote"
        add(j.get("title") or j.get("job_title", ""), j.get("company") or j.get("company_name", ""),
            loc, j.get("url") or j.get("job_url", ""), j.get("description", ""), "arbeitnow")
except Exception as e:
    print("arbeitnow fail:", str(e)[:80])

# 2) RemoteOK — free API
try:
    d = fetch_json("https://remoteok.com/api")
    for j in d[1:41]:
        if not isinstance(j, dict):
            continue
        add(j.get("position", ""), j.get("company", ""), j.get("location") or "Remote",
            j.get("url", ""), j.get("description", ""), "remoteok")
except Exception as e:
    print("remoteok fail:", str(e)[:80])

# 3) Himalayas — public jobs API
try:
    d = fetch_json("https://himalayas.app/jobs/api?limit=40")
    for j in d.get("jobs", []):
        locs = j.get("locationRestrictions") or []
        add(j.get("title", ""), (j.get("company") or {}).get("name", j.get("companyName", "")),
            "Remote" if not locs else ", ".join(locs)[:80], j.get("applicationLink") or j.get("url", ""),
            j.get("description", ""), "himalayas")
except Exception as e:
    print("himalayas fail:", str(e)[:80])

# 4) WeWorkRemotely RSS feeds
for cat in ("all",):
    try:
        root = ET.fromstring(get(f"https://weworkremotely.com/remote-jobs.rss"))
        for item in root.iter("item"):
            title = (item.findtext("title") or "").split(" at ")
            t = title[0] if title else ""
            c = title[1] if len(title) > 1 else ""
            add(t, c, "Remote", item.findtext("link") or "",
                re.sub(r"<[^>]+>", " ", item.findtext("description") or "")[:2000], "weworkremotely")
    except Exception as e:
        print(f"wwr {cat} fail:", str(e)[:60])

# merge + dedupe (by url, then company+title)
q = json.load(open(QUEUE, encoding="utf-8")) if os.path.exists(QUEUE) else []
seen = {j.get("url") for j in q} | {(j.get("company"), j.get("title")) for j in q}
added = 0
for j in new_jobs:
    if j["url"] in seen or (j["company"], j["title"]) in seen:
        continue
    q.append(j); seen.add(j["url"]); seen.add((j["company"], j["title"])); added += 1

json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"EXTENDED: fetched {len(new_jobs)}, added {added}, queue total {len(q)}")
