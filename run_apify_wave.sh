#!/bin/bash
cd "$(dirname "$0")"
export APIFY_API_TOKEN="$APIFY_API_KEY"
echo "=== WAVE START $(date -u) ===" >> apify_wave.log
python3 apify_jobs.py "Sales Development Representative" mena 40 >> apify_wave.log 2>&1
python3 apify_jobs.py "Marketing Manager" mena 40 >> apify_wave.log 2>&1
python3 apify_jobs.py "Business Development" remote 30 >> apify_wave.log 2>&1
echo "=== WAVE DONE $(date -u) ===" >> apify_wave.log
