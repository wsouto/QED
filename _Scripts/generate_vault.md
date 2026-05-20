---
tags: [script, vault, generator, python]
created: 2026-05-20
source: _Scripts/generate_vault.py
---

# Vault Generator — `generate_vault.py`

## Purpose

Reads the classified corpus and generates all 8 Obsidian markdown notes with frontmatter, wikilinks, callouts, and tags.

## How it works

1. Loads `_Data/corpus.json`
2. Generates each note using a dedicated function:
   - `gen_first_post()` — finds tweet ID `1791582201672606146` and its thread
   - `gen_methodology()` — extracts RSI, cycle theory, arrow system info
   - `gen_raicher_strategy()` — RS2, Below-Below-Below, BBW, Linha Solar
   - `gen_glossary()` — 12 predefined entries with definitions and examples
   - `gen_key_predictions()` — filters QED tweets, ranks by engagement
   - `gen_corpus()` — all 1,414 analysis tweets in chronological order
   - `gen_evolution()` — monthly grouping, milestone table, method progression
   - `gen_bio()` — static content about the account

3. Each note uses:
   - **YAML frontmatter** — `tags:`, `aliases:`, `created:`, `tweet_id:`
   - **Wikilinks** — `[[02-Methodology]]` cross-references
   - **Obsidian callouts** — `> [!quote] [date](link)` for tweet text
   - **Engagement emojis** — ❤️🔁💬👁️ with counts

## Related

- [[_Scripts/patch_missing_tweets]] — injects tweets beyond API limit
- [[_Plan/03-Phase-3-Vault-Gen]] — full phase documentation
