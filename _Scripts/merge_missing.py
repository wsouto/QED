#!/usr/bin/env python3
"""
Merge the missing-period search results into the corpus.
"""
import json, os, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_MISSING = os.path.join(SCRIPT_DIR, "..", "_Data", "raw_missing")
CORPUS_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# Get existing tweet IDs
existing_ids = set()
for cat in ["bitcoin_analysis", "other"]:
    for t in corpus["classifications"][cat]:
        existing_ids.add(t["id"])

# Classify patterns (same as Phase 2)
import re
PATTERNS = [re.compile(p, re.IGNORECASE) for p in [
    r"\bbitcoin\b", r"\bbtc\b", r"\bbtcusd\b", r"\$btc", r"\$btcusd", r"\#bitcoin",
    r"\brsi\b", r"\bstochrsi\b", r"\bbdw\b", r"\bema\d+\b", r"\bma\d+\b",
    r"\bqed\b", r"\bagulhad[ao]\b", r"\bflecha\w*\b", r"\bnostreidamos\b",
    r"\biniciante™?\b", r"\bbelow.?below.?below\b",
    r"\bgr[áa]fico\b", r"\ban[áa]lise\b", r"\bestrat[ée]gia\b",
    r"\bsuporte\b", r"\bresist[êe]ncia\b", r"\bbreakout\b",
    r"\btopo\b", r"\bfundo\b", r"\btrade\w*\b", r"\bvela\b", r"\btrend\b",
    r"\bsemanal\b", r"\bmensal\b", r"\bdi[áa]rio\b",
]]

def classify_text(text):
    matched = []
    for p in PATTERNS:
        if p.search(text):
            matched.append(p.pattern)
    return matched

# Load all raw_missing pages
added_analysis = 0
added_other = 0

for month_dir in sorted(glob.glob(os.path.join(RAW_MISSING, "*"))):
    if not os.path.isdir(month_dir):
        continue
    for page_file in sorted(glob.glob(os.path.join(month_dir, "page_*.json"))):
        with open(page_file, "r") as f:
            data = json.load(f)
        for tweet in data.get("data", []):
            tid = tweet["id"]
            if tid in existing_ids:
                continue
            existing_ids.add(tid)
            
            text = tweet.get("text", "")
            matched = classify_text(text)
            entry = {
                "id": tid,
                "text": text,
                "created_at": tweet.get("created_at", ""),
                "public_metrics": tweet.get("public_metrics", {}),
                "referenced_tweets": tweet.get("referenced_tweets", []),
                "in_reply_to_user_id": tweet.get("in_reply_to_user_id", ""),
                "matched_terms": matched[:20],
                "source_file": f"raw_missing/{os.path.basename(month_dir)}/{os.path.basename(page_file)}",
                "_source": "full-archive search"
            }
            
            if matched:
                corpus["classifications"]["bitcoin_analysis"].append(entry)
                added_analysis += 1
            else:
                corpus["classifications"]["other"].append(entry)
                added_other += 1

# Update metadata
corpus["metadata"]["bitcoin_analysis_count"] = len(corpus["classifications"]["bitcoin_analysis"])
corpus["metadata"]["other_count"] = len(corpus["classifications"]["other"])
corpus["metadata"]["total_tweets_loaded"] = corpus["metadata"]["bitcoin_analysis_count"] + corpus["metadata"]["other_count"]

with open(CORPUS_PATH, "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=2, ensure_ascii=False)

size_kb = os.path.getsize(CORPUS_PATH) / 1024
print(f"Added to analysis: {added_analysis}")
print(f"Added to other:    {added_other}")
print(f"Total analysis:    {corpus['metadata']['bitcoin_analysis_count']}")
print(f"Total other:       {corpus['metadata']['other_count']}")
print(f"Total tweets:      {corpus['metadata']['total_tweets_loaded']}")
print(f"Corpus size:       {size_kb:.0f} KB")
