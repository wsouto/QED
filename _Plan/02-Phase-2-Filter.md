---
tags: [plan, phase-2, filter, classification]
created: 2026-05-20
---

# Phase 2 — Filter & Classify

## Overview

Phase 2 reads the 33 raw JSON pages from Phase 1 and classifies each tweet as `bitcoin_analysis` or `other` using keyword matching.

## The Script

`_Scripts/filter_tweets.py` — fully documented at [[_Scripts/filter_tweets]]

**Key design decisions:**

| Decision | Why |
|---|---|
| Regex keyword matching | Fast, transparent, auditable. No ML model needed — we know exactly why each tweet was classified. |
| Case-insensitive | Catches `QED`, `qed`, `Rsi`, `rsi` uniformly |
| Grouped keyword categories | Makes it easy to tune — add/remove a whole category without touching individual patterns |
| Each tweet lists matched terms | Traceability. Open `corpus.json` and see *exactly* which keywords matched. |

## Classification Results

| Category | Count |
|---|---|
| **Bitcoin analysis** | **1,404** |
| Other | 1,815 |
| **Total** | **3,219** |

43.6% of his tweets since May 17, 2024 are Bitcoin analysis content.

## Top Keywords

| Pattern | Tweets matching |
|---|---|
| `rsi` | 655 |
| `resistência` | 594 |
| `ma\d+` (MA7, MA21, etc.) | 542 |
| `suporte` | 368 |
| `diário` | 241 |
| `stochrsi` | 231 |
| `média do rsi` | 203 |
| `\d+h` (4h, 1h, etc.) | 162 |
| `ema\d+` (EMA231, etc.) | 154 |
| `trade*` | 144 |
| `qed` | 142 |
| `agulhada` | 137 |
| `vela` (candle) | 123 |
| `bitcoin` | 97 |
| `trend` | 87 |
| `semanal` | 81 |
| `gráfico` | 74 |
| `cruzamento` (crossover) | 70 |
| `fundo` | 63 |
| `topo` | 57 |

## Output: `corpus.json`

The consolidated corpus (2.4 MB) is at `_Data/corpus.json`. Structure:

```json
{
  "metadata": {
    "source_account": "raicher",
    "total_tweets_loaded": 3219,
    "bitcoin_analysis_count": 1404,
    "other_count": 1815,
    "classification_method": "keyword matching (regex)",
    "keyword_categories": ["bitcoin_method", "indicators", "signature_terms", ...]
  },
  "classifications": {
    "bitcoin_analysis": [
      {
        "id": "1791582201672606146",
        "text": "Acho que nunca mostrei minha teoria...",
        "created_at": "2024-05-17T21:30:00.000Z",
        "public_metrics": { "like_count": 340, ... },
        "referenced_tweets": [],
        "matched_terms": ["\\\\bbitcoin\\\\b", "\\\\bbtcusd\\\\b", "\\\\btrend\\\\b", ...],
        "source_file": "page_033.json"
      },
      ...
    ],
    "other": [ ... ]
  }
}
```

> [!tip] Each tweet in `bitcoin_analysis` includes `matched_terms` — the exact regex patterns that triggered classification. Use this to refine the keyword list if needed.

## Classification Quality

**Potential false positives:** Tweets that mention "resistência" or "suporte" in a non-trading context (e.g., "resistência emocional"). These are rare — his account is focused enough that false positives are minimal.

**Potential false negatives:** Tweets with Bitcoin analysis images but no text keywords. The X API doesn't analyze image content, so analysis-only charts without descriptive text are missed. However, his style is very text-heavy, so this risk is low.

## Next Step

Proceed to **Phase 3** — generate the Obsidian vault notes from the classified corpus.
