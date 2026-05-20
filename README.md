# QED — @raicher Bitcoin Analysis Vault

> *"Acho que nunca mostrei minha teoria dos ciclos de 7ish anos do $BTCUSD aqui no X..."*
> — Allan Raicher (@raicher), May 17, 2024

An **Obsidian vault** documenting Allan Raicher's Bitcoin technical analysis methodology as published on X (Twitter). This vault contains **4,894 tweets** (2,232 Bitcoin analysis posts) extracted via the X API, classified, and structured for study.

## What's Inside

```
QED/
├── 00-Index.md                   ← Map of Content — start here
├── Analysis/                     ← 8 interconnected study notes
│   ├── 01-First-Post.md          ← The genesis thread (May 17, 2024)
│   ├── 02-Methodology.md         ← RSI crossover, 7yr cycles, colored arrows
│   ├── 03-Raicher-Strategy.md    ← Raicher Strategy 2, Below-Below-Below
│   ├── 04-Glossary.md            ← QED, Agulhada, Flechas, key terms
│   ├── 05-Key-Predictions.md     ← Notable calls and QED moments
│   ├── 06-Corpus.md              ← All 2,232 analysis tweets chronologically
│   ├── 07-Evolution.md           ← How the method evolved over time
│   └── 08-Bio.md                 ← Account history and context
├── _Data/
│   ├── corpus.json               ← 4,894 classified tweets (machine-readable)
│   └── raw/                      ← Original API responses (33 + 20 files)
├── _Scripts/                     ← Every extraction & processing script
└── _Plan/                        ← Full project documentation
```

## How to Use

### Read the Analysis

Open the vault in [Obsidian](https://obsidian.md):

1. **File → Open Vault → Open folder as vault** → select `QED/`
2. Start at **00-Index.md** for the Map of Content
3. Use the Graph View (Ctrl+G) to see how notes connect

### Study the Method

The methodology is distilled across three core notes:

- **02-Methodology.md** — The core system: RSI crossover signals, 7-year cycle theory, colored arrow phases, and key RSI levels
- **03-Raicher-Strategy.md** — Specific strategies: Raicher Strategy 2 indicator, Below-Below-Below multi-timeframe approach, BBW volatility analysis
- **04-Glossary.md** — Every unique term explained: QED, Agulhada, Flechas, Nostreidamos, Linha Solar, and more

### Explore the Corpus

For researchers and developers:

- **`_Data/corpus.json`** — All 4,894 tweets classified as `bitcoin_analysis` or `other`, each with:
  - Full text, timestamp, and engagement metrics (likes, retweets, replies, impressions)
  - Classification tags showing exactly which keywords matched
  - Source attribution (API page or search result)
- **`_Data/DATA-MANIFEST.md`** — Complete coverage map with documented gaps
- **`_Scripts/`** — All Python scripts used for extraction, filtering, and vault generation

## Coverage

| Source | Period | Tweets |
|---|---|---|
| X API user timeline | Aug 2025 → May 2026 | 3,219 |
| X API full-archive search | May/Jun/Oct 2024, Feb-Mar-Apr-Jun 2025 | 1,668 |
| Nitter (manual) | Key milestones from missing months | 10 |
| **Gaps** | Jul-Sep/Nov-Dec 2024, Jan/May/Jul-Aug 2025 | ~200-400 est. |

**Coverage notes:** The X API user timeline endpoint caps at the most recent ~3,200 tweets. The remaining months were filled via full-archive search. 9 lower-activity months remain unfilled due to API rate limits and credit depletion. See `_Data/DATA-MANIFEST.md` for details.

## Methodology

### Extraction Pipeline

```
X API → raw JSON pages → keyword classification → corpus.json → Obsidian notes
```

1. **Phase 1** — `/2/users/:id/tweets` endpoint, 100 tweets/call, paginated to end
2. **Phase 2** — Regex keyword matching (6 categories, ~40 patterns)
3. **Phase 3** — Automated note generation with Obsidian-native formatting
4. **Phase 4** — Full-archive search (`/2/tweets/search/all`) for missing period

### Keywords Used for Classification

| Category | Example patterns |
|---|---|
| Core method | bitcoin, btc, btcusd, rsi, agulhada, qed |
| Brand | nostreidamos, iniciante, bitcoinheiros, raicher strategy |
| Analysis language | gráfico, suporte, resistência, breakout, tendência |
| Indicators | stochrsi, bbw, ma7, ema231, média do rsi |
| Trading terms | trade, bear/bull market, topo, fundo, stop loss |
| Timeframes | semanal, mensal, diário, 4h |

## Contributing

This vault is meant to be a living document. Contributions welcome:

- **Missing tweets** — If you have access to the gap periods, open an issue or PR with tweet data
- **Corrections** — False classifications, wrong dates, missing context
- **Analysis** — New insights, patterns, or methodology documentation
- **Charts** — Visual recreations of his analysis with TradingView links

### To contribute

1. Fork the repo
2. Make changes in Obsidian or directly to markdown files
3. Submit a PR

If you're adding tweets, include the source (tweet ID, date, text, and engagement metrics if available).

## How It Was Built

All extraction was done via the [X API v2](https://developer.x.com/en/docs/twitter-api) using the [xurl](https://github.com/xdevplatform/xurl) CLI. The full-archive search used a bearer token from the X Developer Portal. Every script, API response, and processing decision is preserved in `_Plan/` and `_Scripts/`.

**Total API cost:** $14.91 (33 user timeline calls + 29 full-archive search calls)

## License

The documentation, scripts, and structure in this repository are shared for educational purposes. Tweet content is the property of their original author (@raicher). No affiliation with or endorsement by @raicher is implied.
