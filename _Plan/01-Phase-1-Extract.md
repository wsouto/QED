---
tags: [plan, phase-1, extract, api]
created: 2026-05-20
---

# Phase 1 — Data Extraction

## Overview

Phase 1 extracted all tweets from @raicher (user ID `14380292`) starting from **May 17, 2024 at 9:30 PM UTC** — the exact timestamp of his first Bitcoin analysis post.

## The Script

The extraction script is at `_Scripts/extract_raicher.py` with full inline documentation.

**Key design decisions:**

| Decision | Why |
|---|---|
| `start_time` parameter | Filters at the API level — only returns tweets after the first Bitcoin post. Saves credits vs. filtering locally. |
| `max_results=100` | Maximum batch size per call. Fewer calls = fewer credits. |
| `tweet.fields` | Requests rich metadata (dates, engagement stats, reply context) in one shot instead of a second lookup. |
| `2s delay` | X API Free tier allows ~450 requests per 15 min window. 1 req/2s = 30 req/min = well under the limit. |
| Save raw JSON | Preserves the original API response verbatim. Future reprocessing doesn't need new API calls. |

## Execution Log

```
API calls made:    33
Pages saved:       33
Total tweets:      3,219
Errors:            0
```

**Output:** `_Data/raw/page_001.json` through `_Data/raw/page_033.json`

The last page (page 33) returned only 21 tweets and had no `next_token` — this means we reached the chronological end of the timeline for this user.

## Data Format

Each JSON file mirrors the X API v2 response. Here is the structure of the first page showing the very first Bitcoin analysis post:

```json
{
  "data": [
    {
      "id": "1791582201672606146",
      "text": "Acho que nunca mostrei minha teoria dos ciclos de 7ish anos do $BTCUSD aqui no X. Então aproveito para apresentar pra vocês o gráfico abaixo...",
      "edit_history_tweet_ids": ["1791582201672606146"],
      "created_at": "2024-05-17T21:30:00.000Z",
      "public_metrics": {
        "retweet_count": 33,
        "reply_count": 15,
        "like_count": 340,
        "quote_count": 0,
        "impression_count": 99732
      }
    }
  ],
  "meta": {
    "result_count": 100,
    "newest_id": "2057127644123259025",
    "oldest_id": "2025330320588433487",
    "next_token": "7140dibdnow9c7btwoxi40njrs6b8ppmldglqudxh4bax"
  }
}
```

### Explaining the response fields

| Field | Meaning |
|---|---|
| `data[].id` | Unique tweet ID (snowflake). Embeddable in URLs like `https://x.com/raicher/status/{id}` |
| `data[].text` | Full tweet text. URLs, mentions, and hashtags appear as plain text. t.co links are not expanded. |
| `data[].created_at` | ISO 8601 UTC timestamp of when the tweet was posted |
| `data[].public_metrics` | Engagement counters: retweets, replies, likes, quotes, impressions |
| `data[].referenced_tweets` | (if present) Reply-to, quote, or retweet parent references — enables thread reconstruction |
| `data[].in_reply_to_user_id` | (if present) Who this tweet is replying to |
| `meta.result_count` | How many tweets in this page |
| `meta.newest_id` / `oldest_id` | ID range of tweets in this page (newest first, reverse chronological) |
| `meta.next_token` | Pagination cursor. Present when there are more older tweets to fetch. |

## Raw JSON Sample

Here is the full first page of raw data for reference:

```json
{
  "data": [
    {
      "id": "2057127644123259025",
      "edit_history_tweet_ids": ["2057127644123259025"],
      "text": "Se o Dolly Guaraná falou, quem sou eu pra discutir? https://t.co/230bbsYfA3"
    },
    {
      "id": "2057127456486940946",
      "edit_history_tweet_ids": ["2057127456486940946"],
      "text": "@DollynhoCoin @edhyperbtc @Rapha13462 Vai ficar pronto antes da AGI."
    }
  ],
  "meta": {
    "result_count": 100,
    "newest_id": "2057127644123259025",
    "oldest_id": "2025330320588433487",
    "next_token": "7140dibdnow9c7btwoxi40njrs6b8ppmldglqudxh4bax"
  }
}
```

> [!tip] The full raw files are in `_Data/raw/`. Each is named `page_NNN.json` in extraction order.

## Credits

- **Before Phase 1:** $14.91
- **After Phase 1:** $8.81
- **Consumed:** $6.10 for 33 calls ≈ **$0.185 per call**
- **Reasoning:** My original estimate of ~$0.01/call was optimistic. The actual cost per request is higher on this plan tier.

> [!note] All remaining phases (2, 3, 4) cost $0 — purely local processing.

## Next Step

Proceed to **Phase 2** — filter and classify the 3,219 tweets into Bitcoin analysis vs. personal content.
