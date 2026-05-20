---
tags: [script, search, python, bearer]
created: 2026-05-20
source: _Scripts/fill_missing_tweets.py
---

# Missing Data Script — `fill_missing_tweets.py`

## Purpose

Queries the X API full-archive search endpoint (`/2/tweets/search/all`) to fill tweets from the missing period (May 2024 → Jul 2025) that the user timeline endpoint couldn't reach.

## Requirements

- **Bearer token** from the X Developer Portal (OAuth 2.0 Application-Only auth)
- Passed via `BEARER_TOKEN` environment variable

## How it works

1. Iterates month by month from May 2024 to July 2025
2. For each month, queries `from:raicher` with `start_time`/`end_time`
3. Paginates through all results (100 per call)
4. Saves raw JSON to `_Data/raw_missing/{YYYY-MM}/`

## Merge companion

After running, use `merge_missing.py` to incorporate results into `corpus.json`.
