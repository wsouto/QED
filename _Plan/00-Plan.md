# @raicher Bitcoin Analysis — Obsidian Vault Extraction Plan

**Initial budget:** $14.91 X API credits
**Final balance:** $0.00
**Goal:** Extract all Bitcoin analysis posts → Obsidian vault at `~/Documents/Obsidian/QED/`

---

## Vault Structure

```
~/Documents/Obsidian/QED/
├── 00-Index.md                          ← vault home
├── _Plan/                               ← project documentation
├── _Scripts/                            ← every script used
├── _Data/                               ← raw data + corpus
├── _Logs/                               ← execution logs
├── Analysis/                            ← 8 analysis notes
└── .obsidian/                           ← vault config
```

---

## Phase 1 — Extract ✅ COMPLETE

**Method:** X API user timeline endpoint (`/2/users/:id/tweets`)
**Result:** 3,219 tweets from Aug 13, 2025 → May 20, 2026
**Cost:** $6.10 (33 calls)
**Limitation:** API caps at ~3,200 most recent tweets

---

## Phase 2 — Filter & Classify ✅ COMPLETE

**Method:** Regex keyword matching on tweet text
**Result:** 1,414 analysis tweets identified from Phase 1 data
**Refined later:** Grew to 2,232 after merging search results

---

## Phase 3 — Generate Vault ✅ COMPLETE

**Method:** Python script generates 8 Obsidian markdown notes
**Notes:** 01-First-Post through 08-Bio

---

## Phase 4 — Fill Missing Data ✅ COMPLETE

**Method:** Full-archive search (`/2/tweets/search/all`) with bearer token
**Result:** 1,668 tweets from 7 partial months (May/Jun/Oct 2024, Feb-Mar-Apr-Jun 2025)
**Cost:** $8.81 (29 calls)
**Limitation:** Hit rate limits + credits depleted. 9 months still missing.

---

## Coverage Summary

| Source | Period | Tweets | Cost |
|---|---|---|---|
| User timeline API | Aug 2025 → May 2026 | 3,219 | $6.10 |
| Full-archive search | 7 partial months | 1,668 | $8.81 |
| Nitter (manual) | Key milestones | 10 | $0 |
| **Still missing** | 9 months | ~200-400 est. | — |
| **Final corpus** | | **4,894 tweets** (2,232 analysis) | **$14.91** |

---

## Cost Summary

| Phase | What | Cost |
|---|---|---|
| 1 | Extract (user timeline API, 33 calls) | $6.10 |
| 4 | Fill missing (full-archive search, 29 calls) | $8.81 |
| 2 | Filter & classify | $0 |
| 3 | Generate vault notes | $0 |
| **Total** | | **$14.91** |
