#!/usr/bin/env python3
"""
linkedin_guest.py — بديل Apify المجاني لسحب وظائف لينكد إن MENA
يستخدم بحث لينكد إن الضيف العام (بدون دخول، بدون Apify، بدون تكلفة)
Usage: python3 linkedin_guest.py "Marketing Manager" mena 25
Modes: mena (9 دول) | country "<اسم>" | remote
"""
import html as H
import json, os, re, sys, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(BASE, "jobs_queue.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}

MENA = ["Egypt", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman", "Bahrain", "Jordan", "Lebanon"]

def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def fetch_listings(title, loc, rows):
    out, start = [], 0
    pages = (rows + 9) // 10
    for _ in range(pages):
        url = ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
               + urllib.parse.urlencode({"keywords": title, "location": loc, "start": start}))
        try:
            h = get(url)
        except Exception as e:
            print(f"  list fail {loc}@{start}: {str(e)[:60]}", flush=True)
            break
        t = re.findall(r'base-search-card__title[^>]*>\s*(.*?)\s*<', h)
        c = re.findall(r'base-search-card__subtitle[^>]*>\s*<[^>]*>\s*(.*?)\s*<', h)
        l = re.findall(r'job-search-card__location[^>]*>\s*(.*?)\s*<', h)
        d = re.findall(r'job-search-card__listdate[^>]*>\s*(.*?)\s*<', h) or re.findall(r'job-search-card__listdate--new[^>]*>.*?\s*(.*?)\s*<', h)
        links = [x for x in dict.fromkeys(re.findall(r'href="(https://\w+\.linkedin\.com/jobs/view/[^"]+?)"', H.unescape(h)))]
        if not t:
            break
        for i in range(min(len(t), len(c))):
            out.append({"title": H.unescape(t[i]), "company": H.unescape(c[i]),
                        "location": l[i] if i < len(l) else loc,
                        "posted": d[i] if i < len(d) else "",
                        "url": links[i].split("?")[0] if i < len(links) else ""})
        start += 10
        time.sleep(2.5)
        if len(out) >= rows:
            break
    return out[:rows]

def fetch_description(url, cap=3000):
    try:
        h = get(url)
        m = re.search(r'description__text[^>]*>(.*?)</section>', h, re.S)
        if not m:
            m = re.search(r'<div[^>]*class="show-more-less-html__markup[^"]*"[^>]*>(.*?)</div>', h, re.S)
        if m:
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            txt = re.sub(r"\s+", " ", H.unescape(txt)).strip()
            return txt[:cap]
    except Exception as e:
        print("  desc fail:", str(e)[:60], flush=True)
    return ""

def main():
    title = sys.argv[1] if len(sys.argv) > 1 else "Marketing Manager"
    mode = sys.argv[2] if len(sys.argv) > 2 else "mena"
    rows = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    locs = MENA if mode == "mena" else (["Remote"] if mode == "remote" else [mode])

    q = json.load(open(QUEUE, encoding="utf-8")) if os.path.exists(QUEUE) else []
    seen = {j.get("url") for j in q}
    added = 0
    for loc in locs:
        jobs = fetch_listings(title, loc, rows)
        print(f"LINKEDIN_GUEST {loc}: {len(jobs)} listings", flush=True)
        # وصف الوظيفة لأول 5 فقط لكل دولة (توفيرًا للطلبات)
        for j in jobs[:5]:
            if j["url"]:
                j["description"] = fetch_description(j["url"])
                time.sleep(1.5)
        for j in jobs:
            if not j["url"] or j["url"] in seen:
                continue
            j["source"] = "linkedin_guest"
            q.append(j); seen.add(j["url"]); added += 1
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"LINKEDIN_GUEST DONE: added {added}, queue total {len(q)}")

if __name__ == "__main__":
    main()
