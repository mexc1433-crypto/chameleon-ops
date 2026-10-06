#!/usr/bin/env python3
"""
filter_jobs.py - Chameleon queue filter (director's approved rules #2026-10-06)
Rules:
  1. Base salary only -> skip explicit commission-only / no-base-salary jobs.
  2. No German-required jobs (German removed from CV entirely).
  3. Must match Hassan's real profile: outbound sales / marketing / content / BD / SaaS.
  4. Priority: closest to real profile (sales + tech/automation, 150+ freelance projects) first.
Input: jobs_queue.json -> Output: filtered_queue.json + printed top list
"""
import json, re, sys

COMMISSION_ONLY = re.compile(
    r"commission[\s\-]?only|100% commission|pure commission|no base salary|"
    r"بدون راتب|عمولة فقط|لا يوجد راتب|راتب من العمولات", re.I)
GERMAN_REQ = re.compile(
    r"(fluent|native|professional|c1|c2|required|proficient|speaker|speaking)[^\n]{0,40}german|"
    r"german[^\n]{0,25}(fluent|native|c1|c2|required|speaker|speaking)|deutsch", re.I)
PROFILE = re.compile(
    r"\b(sales|outbound|bdr|sdr|sales development|business development|bd\b|account executive|"
    r"marketing|growth|content|copywrit|brand|social media|community|crm|lead generation|"
    r"partnership|saas|b2b|media buying|performance marketing|account manager)\w*", re.I)

# priority weights: sales+tech profile of Hassan (sales/outbound + coding/automation, 150+ projects)
W = {
    "outbound sales": 4, "sdr": 4, "bdr": 4, "sales development": 4,
    "business development": 3, "saas": 3, "account executive": 3, "inside sales": 3,
    "sales": 2, "lead generation": 2, "crm": 2, "b2b": 2, "account manager": 2,
    "marketing": 2, "growth": 2, "content": 1, "social media": 1, "community": 1,
    "automation": 2, "python": 2, "technical": 1, "api": 1, "no-code": 1, "low-code": 1,
}

def text_of(j):
    return " ".join([str(j.get("title") or ""), str(j.get("description") or "")]).lower()

def base_salary_signal(j):
    t = text_of(j)
    return bool(re.search(r"base salary|salary[: ]|EGP|\d{3,4}\s*(egp|aed|sar|usd|us\$|\$)|"
                          r"monthly salary|الراتب|راتب شهري", t))

def priority(j):
    t = text_of(j)
    return sum(w for k, w in W.items() if k in t) + (2 if j.get("remote") else 0)

def main():
    q = json.load(open("jobs_queue.json", encoding="utf-8"))
    kept, skipped = [], {"commission_only": [], "german": [], "no_match": [], "no_url": []}
    for j in q:
        if not j.get("url"):
            skipped["no_url"].append(j.get("title")); continue
        t = text_of(j)
        if COMMISSION_ONLY.search(t):
            skipped["commission_only"].append(f"{j.get('title')} @ {j.get('company')}"); continue
        if GERMAN_REQ.search(t):
            skipped["german"].append(f"{j.get('title')} @ {j.get('company')}"); continue
        if not PROFILE.search(t):
            skipped["no_match"].append(f"{j.get('title')} @ {j.get('company')}"); continue
        j["priority"] = priority(j)
        j["salary_mentioned"] = base_salary_signal(j)
        kept.append(j)
    kept.sort(key=lambda x: (-x.get("priority", 0), -x.get("match_score", 0)))
    json.dump(kept, open("filtered_queue.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"FILTER: kept {len(kept)} / {len(q)}")
    print(f"  skipped commission-only: {len(skipped['commission_only'])}")
    print(f"  skipped german-required: {len(skipped['german'])}")
    print(f"  skipped no-profile-match: {len(skipped['no_match'])}")
    print(f"  skipped no-url: {len(skipped['no_url'])}")
    for s in skipped["commission_only"][:5]: print("   [COMM]", s)
    for s in skipped["german"][:5]: print("   [DE ]", s)
    print("TOP PRIORITY:")
    for j in kept[:10]:
        print(f"  [P{j['priority']}|S{j.get('match_score','?')}] {j['title']} @ {j['company']} | {j.get('location')} | {j['url'][:70]}")

if __name__ == "__main__":
    main()
