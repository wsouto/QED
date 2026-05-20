---
tags: [data, manifest, stats]
created: 2026-05-20
---

# Data Manifest

## Raw Data Summary

| Metric | Value |
|---|---|
| **Source account** | @raicher (ID: `14380292`) |
| **Date range covered** | May 17, 2024 → May 20, 2026 |
| **Total tweets in corpus** | 4,894 |
| **Bitcoin analysis tweets** | 2,232 |
| **Other tweets** | 2,662 |
| **Corpus file** | `corpus.json` (3.7 MB) |

## Coverage by Period

| Period | Source | Tweets | Notes |
|---|---|---|---|
| May 2024 | Full-archive search | 54 | Mostly Bitcoin analysis posts |
| Jun 2024 | Full-archive search | 26 | Light activity |
| Jul 2024 | ❌ Missing | — | Rate limited + credits depleted |
| Aug 2024 | ❌ Missing | — | Rate limited + credits depleted |
| Sep 2024 | ❌ Missing | — | Rate limited + credits depleted |
| Oct 2024 | Full-archive search | 16 | Light activity |
| Nov 2024 | ❌ Missing | — | Rate limited + credits depleted |
| Dec 2024 | ❌ Missing | — | Rate limited + credits depleted |
| Jan 2025 | ❌ Missing | — | Rate limited + credits depleted |
| Feb 2025 | Full-archive search | 563 | Heavy activity |
| Mar 2025 | Full-archive search | 355 | |
| Apr 2025 | Full-archive search | 354 | |
| May 2025 | ❌ Missing | — | Rate limited + credits depleted |
| Jun 2025 | Full-archive search | 300 | Partial (credits died mid-month) |
| Jul 2025 | ❌ Missing | — | Credits depleted |
| Aug 2025 (1st-13th) | ❌ Missing | — | Before API cutoff |
| Aug 13, 2025 → May 20, 2026 | User timeline API | 3,219 | Complete |

## Extraction Methods Used

| Method | Endpoint | Auth | Cost | Quality |
|---|---|---|---|---|
| User timeline | `/2/users/:id/tweets` | OAuth 2.0 | $6.10 | Complete for recent tweets only (~3,200 cap) |
| Full-archive search | `/2/tweets/search/all` | Bearer token | $8.81 | Complete for available months but hit rate limits + credit wall |
| Nitter manual | Browser scrape | None | $0 | Key milestones only |

## Data Sources

```
_Data/
├── raw/                          ← user timeline API (33 files, 3,219 tweets)
│   ├── page_001.json  ~  page_033.json
├── raw_missing/                  ← full-archive search (20 files, 1,668 tweets)
│   ├── 2024-05/
│   ├── 2024-06/
│   ├── 2024-10/
│   ├── 2025-02/  (6 pages)
│   ├── 2025-03/  (4 pages)
│   ├── 2025-04/  (4 pages)
│   └── 2025-06/  (3 pages)
├── corpus.json                   ← consolidated, classified (4,894 tweets)
└── DATA-MANIFEST.md              ← this file
```

## Missing Periods

9 months with no data due to rate limits and credit depletion during full-archive search:

- July 2024 — September 2024
- November 2024 — December 2024
- January 2025
- May 2025
- July 2025
- August 1-13, 2025

Raicher was less active during this period (just starting his Bitcoin analysis). Estimated ~200-400 tweets missing total. Key milestones (first post, RSI strategy, FAQ) were manually injected via Nitter.

## Cost Summary

| Item | Amount |
|---|---|
| Initial balance | $14.91 |
| User timeline API (33 calls) | -$6.10 |
| Full-archive search (29 calls) | -$8.81 |
| **Remaining** | **$0.00** |
