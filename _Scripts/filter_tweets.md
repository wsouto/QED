---
tags: [script, filter, python, classification]
created: 2026-05-20
source: _Scripts/filter_tweets.py
---

# Filter Script — `filter_tweets.py`

## Purpose

Reads all 33 raw JSON pages from Phase 1, classifies each tweet as `bitcoin_analysis` or `other`, and produces a consolidated `corpus.json`.

## How it works

1. Loads all `page_*.json` files from `_Data/raw/`
2. For each tweet, compiles a list of regex patterns grouped by category
3. If **any** pattern matches the tweet text, it's tagged `bitcoin_analysis`
4. Saves the consolidated `corpus.json` with classification metadata

## Keyword System

| Category | Purpose | Example matches |
|---|---|---|
| `bitcoin_method` | Core Bitcoin references | bitcoin, btc, btcusd, $BTC |
| `indicators` | Technical indicators | rsi, stochrsi, bbw, ma7, ema231 |
| `signature_terms` | His unique vocabulary | qed, agulhada, flecha, nostreidamos, below-below-below |
| `analysis_language` | Chart/trading language | gráfico, suporte, resistência, breakout, tendência |
| `price_action` | Trade-specific terms | stop loss, entrada, saída, previsão, ATH |
| `timeframes` | Timeframe references | semanal, mensal, diário, 4h |

## Source Code

```python
#!/usr/bin/env python3
"""
Phase 2: Filter and classify @raicher tweets.

Reads all raw JSON pages from Phase 1, classifies each tweet
as 'bitcoin_analysis' or 'other', and produces a consolidated
corpus.json with all metadata preserved.
"""

import json
import os
import re
import glob
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "_Data", "raw")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")
RAICHER_USER_ID = "14380292"

ANALYSIS_KEYWORDS = {
    "bitcoin_method": [
        r"\bbitcoin\b", r"\bbtc\b", r"\bbtcusd\b", r"\$btc",
        r"\$btcusd", r"\#bitcoin",
    ],
    "indicators": [
        r"\brsi\b", r"\bstochrsi\b", r"\bbdw\b",
        r"\bema\d+\b", r"\bma\d+\b",
        r"\bmédia do rsi\b", r"\bmédia móvel\b",
        r"\bmoving average\b",
    ],
    "signature_terms": [
        r"\bqed\b", r"\bagulhad[ao]\b", r"\bagulhadas\b",
        r"\bflecha\w*\b",
        r"\bnostreidamos\b",
        r"\biniciante™?\b",
        r"\babaixo-abaixo-abaixo\b",
        r"\bbelow.?below.?below\b",
        r"\braicher strategy\b",
    ],
    "analysis_language": [
        r"\bgr[áa]fico\b", r"\bchart\b",
        r"\ban[áa]lise\b",
        r"\bestrat[ée]gia\b", r"\bstrategy\b",
        r"\bsuporte\b", r"\bresist[êe]ncia\b",
        r"\bbreakout\b",
        r"\btopo\b", r"\bfundo\b",
        r"\bbear market\b", r"\bbull market\b",
        r"\btrade\w*\b",
        r"\btend[êe]ncia\b", r"\btrend\b",
        r"\bvela\b",
        r"\bcruzamento\b",
        r"\bconflu[êe]ncia\b",
        r"\bliquidez\b",
        r"\bvolatilidade\b",
    ],
    "price_action": [
        r"\bath\b", r"\ball[ -]?time[ -]?high\b",
        r"\bresist[êe]ncia\b",
        r"\bstop loss\b", r"\bstop\b",
        r"\bentrada\b", r"\bsa[íi]da\b",
        r"\bprevis[ãa]o\b", r"\bprediction\b",
    ],
    "timeframes": [
        r"\bsemanal\b", r"\bmensal\b", r"\bdi[áa]rio\b",
        r"\bgr[áa]fico de \d+ [dD]ias\b", r"\b\d+h\b",
    ],
}

PATTERNS = []
for patterns in ANALYSIS_KEYWORDS.values():
    for p in patterns:
        PATTERNS.append(re.compile(p, re.IGNORECASE))


def classify_tweet(tweet):
    text = tweet.get("text", "")
    matched = []
    for pattern in PATTERNS:
        if pattern.search(text):
            matched.append(pattern.pattern)
    return ("bitcoin_analysis", matched) if matched else ("other", [])


def load_raw_pages(raw_dir):
    all_tweets = []
    for filepath in sorted(glob.glob(os.path.join(raw_dir, "page_*.json"))):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for tweet in data.get("data", []):
            tweet["_source_file"] = os.path.basename(filepath)
            all_tweets.append(tweet)
    return all_tweets


def main():
    all_tweets = load_raw_pages(RAW_DIR)
    classifications = Counter()
    term_counter = Counter()
    analysis_tweets = []
    other_tweets = []

    for tweet in all_tweets:
        category, matched_terms = classify_tweet(tweet)
        classifications[category] += 1
        tweet["_category"] = category
        tweet["_matched_terms"] = matched_terms[:20]
        for term in matched_terms:
            term_counter[term] += 1
        if category == "bitcoin_analysis":
            analysis_tweets.append(tweet)
        else:
            other_tweets.append(tweet)

    corpus = {
        "metadata": {
            "source_account": "raicher",
            "source_user_id": RAICHER_USER_ID,
            "total_tweets_loaded": len(all_tweets),
            "bitcoin_analysis_count": classifications["bitcoin_analysis"],
            "other_count": classifications["other"],
            "classification_date": "2026-05-20",
            "classification_method": "keyword matching (regex)",
            "keyword_categories": list(ANALYSIS_KEYWORDS.keys()),
        },
        "classifications": {
            "bitcoin_analysis": [
                {"id": t["id"], "text": t.get("text", ""),
                 "created_at": t.get("created_at", ""),
                 "public_metrics": t.get("public_metrics", {}),
                 "referenced_tweets": t.get("referenced_tweets", []),
                 "in_reply_to_user_id": t.get("in_reply_to_user_id"),
                 "matched_terms": t.get("_matched_terms", []),
                 "source_file": t.get("_source_file", "")}
                for t in analysis_tweets
            ],
            "other": [
                {"id": t["id"], "text": t.get("text", ""),
                 "created_at": t.get("created_at", ""),
                 "public_metrics": t.get("public_metrics", {}),
                 "referenced_tweets": t.get("referenced_tweets", []),
                 "in_reply_to_user_id": t.get("in_reply_to_user_id"),
                 "source_file": t.get("_source_file", "")}
                for t in other_tweets
            ],
        }
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"Bitcoin analysis: {classifications['bitcoin_analysis']}")
    print(f"Other:            {classifications['other']}")
    print(f"Corpus:           {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
```
