#!/usr/bin/env python3
"""
Phase 2: Filter and classify @raicher tweets.

Reads all raw JSON pages from Phase 1, classifies each tweet
as 'bitcoin_analysis' or 'other', and produces a consolidated
corpus.json with all metadata preserved.

Classification method: keyword matching on tweet text.
Tweets that match any Bitcoin analysis keyword are tagged
as bitcoin_analysis. The rest are tagged as other.

Usage:
    python3 filter_tweets.py

Output:
    ../_Data/corpus.json  (consolidated, classified corpus)
    stdout summary
"""

import json
import os
import re
import glob
from collections import Counter

# --- Paths ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "_Data", "raw")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")
RAICHER_USER_ID = "14380292"

# --- Keyword Definitions ---
# Each tweet is checked against these keyword patterns.
# Grouped by category for documentation purposes.
# All matching is case-insensitive.

ANALYSIS_KEYWORDS = {
    # Core method: Bitcoin and trading fundamentals
    "bitcoin_method": [
        r"\bbitcoin\b", r"\bbtc\b", r"\bbtcusd\b", r"\$btc",
        r"\$btcusd", r"\#bitcoin",
    ],
    # RSI and indicators
    "indicators": [
        r"\brsi\b", r"\bstochrsi\b", r"\bbdw\b",  # BBW = Bollinger Band Width
        r"\bema\d+\b", r"\bma\d+\b",               # MA7, MA21, MA77, EMA231
        r"\bmédia do rsi\b", r"\bmédia móvel\b",
        r"\bmoving average\b",
    ],
    # His signature terms
    "signature_terms": [
        r"\bqed\b", r"\bagulhad[ao]\b", r"\bagulhadas\b",
        r"\bflecha\w*\b",                            # flecha, flechinha
        r"\bnostreidamos\b",
        r"\biniciante™?\b",
        r"\babaixo-abaixo-abaixo\b",
        r"\bbelow.?below.?below\b",
        r"\braicher strategy\b",
    ],
    # Chart and analysis language
    "analysis_language": [
        r"\bgr[áa]fico\b", r"\bchart\b",
        r"\ban[áa]lise\b", r"\ban[áa]lise técnica\b",
        r"\bestrat[ée]gia\b", r"\bstrategy\b",
        r"\bsuporte\b", r"\bresist[êe]ncia\b",
        r"\bbreakout\b",
        r"\btopo\b", r"\bfundo\b",
        r"\bbear market\b", r"\bbull market\b",
        r"\btrade\w*\b",                             # trade, trader, trading
        r"\btend[êe]ncia\b", r"\btrend\b",
        r"\bvela\b",                                # candle
        r"\bcruzamento\b",                          # crossover
        r"\bconflu[êe]ncia\b",
        r"\bliquidez\b",
        r"\bvolatilidade\b",
    ],
    # Price action
    "price_action": [
        r"\bath\b", r"\ball[ -]?time[ -]?high\b",
        r"\bresist[êe]ncia\b",
        r"\bstop loss\b", r"\bstop\b",
        r"\bentrada\b", r"\bsa[íi]da\b",
        r"\bprevis[ãa]o\b", r"\bprediction\b",
    ],
    # Time references in analysis context (like "weekly", "monthly", "daily")
    "timeframes": [
        r"\bsemanal\b", r"\bmensal\b", r"\bdi[áa]rio\b",
        r"\bgr[áa]fico de \d+ [dD]ias\b", r"\b\d+h\b",  # 4h, 1h, etc.
    ],
}

# --- Helper Functions ---

def compile_patterns():
    """Compile all keyword patterns into a single regex for efficiency."""
    all_patterns = []
    for category, patterns in ANALYSIS_KEYWORDS.items():
        for p in patterns:
            all_patterns.append(re.compile(p, re.IGNORECASE))
    return all_patterns

PATTERNS = compile_patterns()


def classify_tweet(tweet: dict) -> tuple[str, list[str]]:
    """
    Classify a single tweet as 'bitcoin_analysis' or 'other'.
    
    Returns (category, matched_terms) tuple.
    A tweet is 'bitcoin_analysis' if any keyword pattern matches its text.
    """
    text = tweet.get("text", "")
    matched = []
    
    for pattern in PATTERNS:
        if pattern.search(text):
            matched.append(pattern.pattern)
    
    if matched:
        return ("bitcoin_analysis", matched)
    else:
        return ("other", [])


def load_raw_pages(raw_dir: str) -> list[dict]:
    """Load all raw JSON pages and return a flat list of tweets."""
    all_tweets = []
    page_files = sorted(glob.glob(os.path.join(raw_dir, "page_*.json")))
    
    for filepath in page_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        tweets = data.get("data", [])
        for tweet in tweets:
            # Add page source for traceability
            tweet["_source_file"] = os.path.basename(filepath)
            all_tweets.append(tweet)
    
    return all_tweets


def format_tweet_preview(tweet: dict, max_len: int = 100) -> str:
    """Truncate tweet text for display."""
    text = tweet.get("text", "")
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


# --- Main ---

def main():
    print("=" * 60)
    print("  Phase 2: Filter & Classify @raicher tweets")
    print("=" * 60)
    
    # Load raw data
    print(f"\n  Loading raw data from: {RAW_DIR}")
    all_tweets = load_raw_pages(RAW_DIR)
    print(f"  Loaded {len(all_tweets)} tweets from {len(glob.glob(os.path.join(RAW_DIR, 'page_*.json')))} files")
    
    # Classify each tweet
    print(f"\n  Classifying tweets...")
    classifications = Counter()
    term_counter = Counter()
    
    analysis_tweets = []
    other_tweets = []
    
    for tweet in all_tweets:
        category, matched_terms = classify_tweet(tweet)
        classifications[category] += 1
        
        tweet["_category"] = category
        tweet["_matched_terms"] = matched_terms[:20]  # cap at 20 matches
        
        for term in matched_terms:
            term_counter[term] += 1
        
        if category == "bitcoin_analysis":
            analysis_tweets.append(tweet)
        else:
            other_tweets.append(tweet)
    
    # Print classification summary
    print(f"\n  Results:")
    print(f"    Bitcoin analysis:  {classifications['bitcoin_analysis']}")
    print(f"    Other:             {classifications['other']}")
    print(f"    Total:             {sum(classifications.values())}")
    
    # Print top matching terms
    print(f"\n  Top matching keywords:")
    for term, count in term_counter.most_common(20):
        # Clean up the regex pattern for display
        display = term.replace(r"\b", "").replace(r"\W*", "")
        print(f"    {display:30s}  {count:4d} tweets")
    
    # Build the consolidated corpus
    print(f"\n  Building corpus.json...")
    
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
                {
                    "id": t["id"],
                    "text": t.get("text", ""),
                    "created_at": t.get("created_at", ""),
                    "public_metrics": t.get("public_metrics", {}),
                    "referenced_tweets": t.get("referenced_tweets", []),
                    "in_reply_to_user_id": t.get("in_reply_to_user_id"),
                    "matched_terms": t.get("_matched_terms", []),
                    "source_file": t.get("_source_file", ""),
                }
                for t in analysis_tweets
            ],
            "other": [
                {
                    "id": t["id"],
                    "text": t.get("text", ""),
                    "created_at": t.get("created_at", ""),
                    "public_metrics": t.get("public_metrics", {}),
                    "referenced_tweets": t.get("referenced_tweets", []),
                    "in_reply_to_user_id": t.get("in_reply_to_user_id"),
                    "source_file": t.get("_source_file", ""),
                }
                for t in other_tweets
            ],
        }
    }
    
    # Write corpus
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    
    file_size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"  Written: {OUTPUT_PATH} ({file_size_kb:.1f} KB)")
    
    # Show a few examples
    print(f"\n  Sample of classified tweets:")
    print(f"\n  --- Bitcoin Analysis (first 5) ---")
    for t in analysis_tweets[:5]:
        print(f"    [{t.get('created_at','')[:10]}] {format_tweet_preview(t, 90)}")
    
    print(f"\n  --- Other (first 5) ---")
    for t in other_tweets[:5]:
        print(f"    [{t.get('created_at','')[:10]}] {format_tweet_preview(t, 90)}")
    
    print(f"\n{'='*60}")
    print(f"  PHASE 2 COMPLETE")
    print(f"{'='*60}")
    print(f"  Bitcoin analysis tweets: {classifications['bitcoin_analysis']}")
    print(f"  Other tweets:            {classifications['other']}")
    print(f"  Total:                   {sum(classifications.values())}")
    print(f"  Corpus file:             {OUTPUT_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
