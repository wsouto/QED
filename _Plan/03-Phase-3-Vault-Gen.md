---
tags: [plan, phase-3, generate, vault]
created: 2026-05-20
---

# Phase 3 — Generate Obsidian Vault Notes

## Overview

Phase 3 reads the classified `corpus.json` and writes all `Analysis/*.md` notes with Obsidian-native formatting.

## The Scripts

### `_Scripts/generate_vault.py`

The main generator. For each of the 8 analysis notes, it:

1. Filters the corpus for relevant tweets
2. Formats them as Obsidian callouts `> [!quote]` with engagement stats
3. Writes YAML frontmatter (`tags:`, `aliases:`, `created:`, `tweet_id:`)
4. Saves to `Analysis/` directory

### `_Scripts/patch_missing_tweets.py`

Discovered that the X API only returns ~3,200 most recent tweets from the user timeline endpoint. Our extraction (Phase 1) captured **Aug 2025 → May 2026**, missing **May 2024 → Aug 2025**.

This script injects 10 known missing tweets gathered via Nitter, including:
- The first Bitcoin analysis post (May 17, 2024)
- The RSI crossover strategy launch (June 5, 2024)
- The 31st crossover milestone (September 23, 2024)
- The FAQ post (December 15, 2024)

## Notes Generated

| Note | Size | Content |
|---|---|---|
| `01-First-Post.md` | 2 KB | The May 17, 2024 thread — full thread, metadata, context |
| `02-Methodology.md` | 3 KB | RSI crossover, 7-year cycles, colored arrows, RSI levels |
| `03-Raicher-Strategy.md` | 2 KB | Raicher Strategy 2, Below-Below-Below, BBW, Linha Solar |
| `04-Glossary.md` | 3 KB | 12 entries: QED, Agulhada, Flechas, Nostreidamos, etc. |
| `05-Key-Predictions.md` | 9 KB | Top QED posts, notable price predictions |
| `06-Corpus.md` | 508 KB | All 1,414 analysis tweets chronologically |
| `07-Evolution.md` | 2 KB | Timeline from May 2024 → present, milestone table |
| `08-Bio.md` | 2 KB | Account history, first tweet from 2008, fun facts |

## API Limitation Note

The user timeline endpoint (`/2/users/:id/tweets`) returned a maximum of ~3,200 tweets — consistent with the legacy v1.1 API limit. We captured:

- **API range:** Aug 13, 2025 → May 20, 2026 (3,219 tweets)
- **Missing:** May 17, 2024 → Aug 13, 2025 (~15 months)

The 10 most critical missing tweets were manually injected from Nitter data. For a complete archive of this period, future work could use:
1. Nitter scraping for specific date ranges
2. X API search endpoint with higher plan tiers
3. Manual collection of notable posts

## Known Issues

- Tweet IDs for Nitter-sourced posts are approximate (marked with `_source: nitter`)
- Engagement metrics for some patched tweets are rounded/estimated
- The `06-Corpus.md` is 508 KB — Obsidian handles this fine, but search may be slower
