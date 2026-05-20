#!/usr/bin/env python3
"""
Phase 1: Extract all @raicher tweets from May 17, 2024 to present.

This script paginates through the X API v2 user timeline endpoint,
fetching 100 tweets at a time and saving each API response as a
raw JSON file. It uses the 'start_time' parameter to begin at the
first Bitcoin analysis post (May 17, 2024 9:30 PM UTC).

Endpoint: GET /2/users/:id/tweets
Docs: https://developer.x.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets

Usage:
    python3 extract_raicher.py

Output:
    ../_Data/raw/page_NNN.json  (one file per API call)
    stdout summary on completion
"""

import subprocess
import json
import sys
import os
import time

# --- Configuration ---

USER_ID = "14380292"          # @raicher's numeric user ID
OUTPUT_DIR = os.path.join(    # where raw JSON pages go
    os.path.dirname(os.path.abspath(__file__)),
    "..", "_Data", "raw"
)

START_TIME = "2024-05-17T21:30:00Z"  # first Bitcoin post timestamp
FIELDS = "tweet.fields=created_at,public_metrics,referenced_tweets,in_reply_to_user_id,attachments"

# Rate limit: X API Free allows ~450 requests per 15-minute window.
# 450 req / 900 sec = 1 req per 2 seconds is safe.
DELAY_BETWEEN_CALLS = 2  # seconds


# --- Helper ---

def call_xapi(url: str) -> dict | None:
    """
    Call the xurl CLI with a given URL and parse the JSON response.
    
    xurl prints JSON to stdout and may append 'Error: ...' to stderr
    on non-zero exit codes. We parse stdout only, stripping any
    trailing non-JSON content.
    
    Returns parsed dict on success, None on failure.
    """
    result = subprocess.run(
        ["xurl", url],
        capture_output=True,
        text=True,
        timeout=30  # 30s per call is generous
    )
    
    output = result.stdout
    
    # xurl sometimes appends a human-readable error line after the JSON.
    # Find the last '}' and truncate there.
    last_brace = output.rfind("}")
    if last_brace >= 0:
        output = output[:last_brace + 1]
    else:
        print(f"  [WARN] No JSON object found in response: {output[:200]}")
        return None
    
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON parse failed: {e}")
        print(f"  Raw snippet: {output[:300]}")
        return None


# --- Main Loop ---

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    page = 1
    next_token = None
    total_tweets = 0
    total_calls = 0
    errors = []
    
    print(f"{'='*60}")
    print(f"  Phase 1: Extract @raicher tweets")
    print(f"  Start time: {START_TIME}")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Delay: {DELAY_BETWEEN_CALLS}s between calls")
    print(f"{'='*60}")
    
    while True:
        # --- Build the API URL ---
        # Base: /2/users/{id}/tweets with max_results=100
        # Pagination: add pagination_token when we have one
        # Time filter: start_time ensures we only get tweets after May 17, 2024
        
        url = (
            f"/2/users/{USER_ID}/tweets"
            f"?max_results=100"
            f"&{FIELDS}"
            f"&start_time={START_TIME}"
        )
        if next_token:
            url += f"&pagination_token={next_token}"
        
        # --- Make the API call ---
        print(f"\n  Request {page}: fetching...", end="")
        sys.stdout.flush()
        
        data = call_xapi(url)
        total_calls += 1
        
        if data is None:
            print(" FAILED (empty response)")
            errors.append(f"Page {page}: empty response")
            break
        
        # --- Check for API-level errors ---
        # The X API returns errors in the 'title' or 'errors' fields.
        # Example: {"title": "CreditsDepleted", "detail": "..."}
        
        if "title" in data:
            title = data.get("title", "Unknown error")
            detail = data.get("detail", "")
            print(f"\n  [API ERROR] {title}: {detail}")
            errors.append(f"Page {page}: {title} — {detail}")
            break
        
        if "errors" in data:
            for err in data["errors"]:
                msg = err.get("message", "Unknown")
                print(f"\n  [API ERROR] {msg}")
                errors.append(f"Page {page}: {msg}")
            break
        
        # --- Extract tweet data ---
        tweets = data.get("data", [])
        meta = data.get("meta", {})
        tweet_count = len(tweets)
        total_tweets += tweet_count
        
        oldest_id = meta.get("oldest_id", "?")
        newest_id = meta.get("newest_id", "?")
        next_token = meta.get("next_token", None)
        
        # --- Save raw page to disk ---
        filename = f"page_{page:03d}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        # --- Print summary for this page ---
        print(f" OK — {tweet_count} tweets, oldest={oldest_id[:8]}...{oldest_id[-4:]}, next={bool(next_token)}")
        
        # --- Check if we've reached the end ---
        if not next_token:
            print(f"\n{'='*60}")
            print(f"  END OF TIMELINE REACHED")
            print(f"{'='*60}")
            break
        
        # --- Rate limiting: pause before next call ---
        time.sleep(DELAY_BETWEEN_CALLS)
        page += 1
    
    # --- Final Summary ---
    print(f"\n{'='*60}")
    print(f"  PHASE 1 COMPLETE")
    print(f"{'='*60}")
    print(f"  API calls made:    {total_calls}")
    print(f"  Pages saved:       {page}")
    print(f"  Total tweets:      {total_tweets}")
    print(f"  Errors:            {len(errors)}")
    if errors:
        for e in errors:
            print(f"    • {e}")
    print(f"  Output directory:  {OUTPUT_DIR}")
    print(f"{'='*60}")
    
    return total_calls, page, total_tweets, errors


if __name__ == "__main__":
    main()
