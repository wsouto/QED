#!/usr/bin/env python3
"""
Phase 5: Fill missing tweets via full-archive search.

Queries /2/tweets/search/all month by month from May 2024 to Jul 2025,
saves raw results, and merges into the existing corpus.

Usage:
    BEARER_TOKEN="your_token" python3 fill_missing_tweets.py
"""

import subprocess
import json
import os
import time
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "_Data", "raw_missing")
CORPUS_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")
BEARER = os.environ.get("BEARER_TOKEN", "")

if not BEARER:
    print("ERROR: Set BEARER_TOKEN env var")
    sys.exit(1)

# Month ranges to fill (May 2024 → Jul 2025)
MONTHS = []
for year in [2024, 2025]:
    for month in range(1, 13):
        if year == 2024 and month < 5:
            continue
        if year == 2025 and month > 7:
            continue
        start = f"{year}-{month:02d}-01T00:00:00Z"
        if month == 12:
            end = f"{year+1}-01-01T00:00:00Z"
        else:
            end = f"{year}-{month+1:02d}-01T00:00:00Z"
        MONTHS.append((f"{year}-{month:02d}", start, end))

print(f"Will query {len(MONTHS)} months: {MONTHS[0][0]} → {MONTHS[-1][0]}")
print(f"Using bearer token: {BEARER[:20]}...{BEARER[-10:]}")
print()

def call_search(query, start, end, next_token=None):
    """Call full-archive search with the bearer token."""
    url = (f"/2/tweets/search/all"
           f"?query={query}"
           f"&max_results=100"
           f"&start_time={start}"
           f"&end_time={end}"
           f"&tweet.fields=created_at,public_metrics,author_id,referenced_tweets")
    if next_token:
        url += f"&next_token={next_token}"
    
    result = subprocess.run(
        ["xurl", "-H", f"Authorization: Bearer {BEARER}", url],
        capture_output=True, text=True, timeout=60
    )
    output = result.stdout
    idx = output.rfind("}")
    if idx >= 0:
        output = output[:idx+1]
    return json.loads(output)

os.makedirs(OUTPUT_DIR, exist_ok=True)
total_tweets = 0
total_calls = 0

for month_label, start, end in MONTHS:
    month_dir = os.path.join(OUTPUT_DIR, month_label)
    os.makedirs(month_dir, exist_ok=True)
    
    month_count = 0
    page = 0
    next_token = None
    
    print(f"📅 {month_label}: ", end="", flush=True)
    
    while True:
        data = call_search("from:raicher", start, end, next_token)
        total_calls += 1
        
        if "errors" in data or "title" in data:
            err = data.get("title", data.get("detail", "unknown"))
            print(f"ERROR: {err}")
            break
        
        tweets = data.get("data", [])
        meta = data.get("meta", {})
        
        if not tweets:
            break
        
        # Save page
        filename = f"page_{page:02d}.json"
        with open(os.path.join(month_dir, filename), "w") as f:
            json.dump(data, f, indent=2)
        
        month_count += len(tweets)
        total_tweets += len(tweets)
        next_token = meta.get("next_token")
        page += 1
        
        print(".", end="", flush=True)
        
        if not next_token:
            break
        time.sleep(1)
    
    print(f" {month_count} tweets ({page} pages)")

print(f"\n=== Complete ===")
print(f"  Months queried: {len(MONTHS)}")
print(f"  API calls: {total_calls}")
print(f"  Tweets found: {total_tweets}")
print(f"  Output: {OUTPUT_DIR}")
