#!/usr/bin/env python3
"""
Phase 3: Generate Obsidian vault notes from classified corpus.

Reads _Data/corpus.json and writes all Analysis/*.md notes
with frontmatter, wikilinks, Obsidian callouts, and tags.

Usage:
    python3 generate_vault.py

Output:
    ../Analysis/01-First-Post.md through ../Analysis/08-Bio.md
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime

# --- Paths ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")
ANALYSIS_DIR = os.path.join(SCRIPT_DIR, "..", "Analysis")

# --- Load Corpus ---

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

analysis_tweets = corpus["classifications"]["bitcoin_analysis"]
other_tweets = corpus["classifications"]["other"]
all_tweets_sorted = sorted(
    analysis_tweets + other_tweets,
    key=lambda t: t.get("created_at", ""),
    reverse=True  # newest first (matching API order)
)

# Index by ID for quick lookup
tweets_by_id = {}
for t in all_tweets_sorted:
    tweets_by_id[t["id"]] = t

# Chronological order (oldest first) for timeline views
analysis_chrono = sorted(analysis_tweets, key=lambda t: t.get("created_at", ""))


# --- Helpers ---

def fmt_metrics(m):
    """Format metrics for display."""
    if not m:
        return ""
    parts = []
    if m.get("like_count"): parts.append(f"❤️ {m['like_count']}")
    if m.get("retweet_count"): parts.append(f"🔁 {m['retweet_count']}")
    if m.get("reply_count"): parts.append(f"💬 {m['reply_count']}")
    if m.get("impression_count"): parts.append(f"👁️ {m['impression_count']:,}")
    return "  ·  ".join(parts)


def fmt_date(iso_str):
    """Format ISO date for display."""
    if not iso_str:
        return "unknown"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y at %I:%M %p UTC")
    except:
        return iso_str[:10]


def fmt_date_short(iso_str):
    """Format ISO date as YYYY-MM-DD."""
    if not iso_str:
        return "unknown"
    return iso_str[:10]


def tweet_link(tweet_id):
    return f"https://x.com/raicher/status/{tweet_id}"


def tweet_callout(t):
    """Render a tweet as an Obsidian callout."""
    text = t.get("text", "")
    date_str = fmt_date(t.get("created_at", ""))
    url = tweet_link(t["id"])
    metrics = fmt_metrics(t.get("public_metrics", {}))
    
    lines = [f"> [!quote] [{date_str}]({url})"]
    # Add the text, preserving line breaks
    for para in text.split("\n"):
        if para.strip():
            lines.append(f"> *{para}*")
        else:
            lines.append(f">")
    if metrics:
        lines.append(f">")
        lines.append(f"> {metrics}")
    lines.append("")
    return "\n".join(lines)


def extract_hashtags(text):
    """Extract hashtags from text."""
    return re.findall(r'#(\w+)', text)


def extract_cashtags(text):
    """Extract cashtags like $BTCUSD."""
    return re.findall(r'\$(\w+)', text)


# ============================================================
# NOTE 1: First Post — May 17, 2024 thread
# ============================================================

def gen_first_post():
    first_id = "1791582201672606146"
    first = tweets_by_id.get(first_id)
    if not first:
        return "# First Post\n\nTweet not found in corpus."
    
    # Find thread replies by the same user within the same day
    thread_time = first.get("created_at", "")
    thread_date = thread_time[:10] if thread_time else ""
    
    thread_tweets = [t for t in analysis_chrono
                     if t.get("created_at", "").startswith(thread_date)
                     and t.get("in_reply_to_user_id") == "14380292"
                     and t["id"] != first_id
                     or t["id"] == first_id]
    # Also check referenced_tweets for thread structure
    thread_replies = []
    for t in analysis_chrono:
        refs = t.get("referenced_tweets", [])
        for ref in refs:
            if ref.get("id") == first_id or ref.get("id") in [rt["id"] for rt in thread_replies]:
                if t not in thread_replies and t["id"] != first_id:
                    thread_replies.append(t)
    
    # Order chronologically
    thread_all = sorted([first] + thread_replies, key=lambda x: x.get("created_at", ""))
    
    metrics = first.get("public_metrics", {})
    
    content = []
    content.append("---")
    content.append("tags: [analysis, first-post, bitcoin, rsi, cycles]")
    content.append("aliases: [first-bitcoin-post, may-17-2024, genesis]")
    content.append("created: 2026-05-20")
    content.append("tweet_id: \"1791582201672606146\"")
    content.append("---")
    content.append("")
    content.append("# First Bitcoin Analysis Post")
    content.append("")
    content.append(f"**Date:** {fmt_date(first.get('created_at', ''))}")
    content.append(f"**Link:** [{tweet_link(first_id)}]({tweet_link(first_id)})")
    content.append(f"**Views:** {metrics.get('impression_count', 'N/A'):,}")
    content.append(f"**Likes:** {metrics.get('like_count', 0):,}")
    content.append("")
    content.append("## Context")
    content.append("")
    content.append("This was the first time @raicher shared his Bitcoin cycle theory on X. Before this, his timeline was mostly astrophotography, casual replies, and personal updates. This post marks the beginning of his public Bitcoin analysis — and the start of the **\"iniciante™\"** brand.")
    content.append("")
    content.append("He introduces a **7-ish year cycle theory** using colored arrows to mark Bitcoin's macro phases, with the RSI and StochRSI as confirmation tools. The chart shows the 2nd orange arrow — positioning the current market similarly to October 2016 (pre-bull-run).")
    content.append("")
    content.append("## The Thread")
    content.append("")
    for t in thread_all:
        content.append(tweet_callout(t))
    
    content.append("## Aftermath")
    content.append("")
    content.append("The post went viral (99.7K views), and replies were a mix of engagement and skepticism. Raicher continued refining the method over the following weeks — leading to the June 5 RSI crossover strategy, the Raicher Strategy 2 indicator, and eventually the consistent daily/weekly analysis cadence that defines his current presence.")
    content.append("")
    content.append("See [[02-Methodology]] for how the method evolved, and [[07-Evolution]] for the full timeline.")
    content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 2: Methodology
# ============================================================

def gen_methodology():
    content = []
    content.append("---")
    content.append("tags: [analysis, methodology, rsi, cycles, trading]")
    content.append("aliases: [method, theory, cycle-theory]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Methodology")
    content.append("")
    content.append("## Core Principle")
    content.append("")
    content.append("@raicher's analysis is built on **technical analysis** of Bitcoin's price chart using **RSI (Relative Strength Index)**, **moving averages**, and **cycle theory**. The core insight: Bitcoin moves in identifiable macro cycles that repeat with predictable patterns.")
    content.append("")
    content.append("## The 7-Year Cycle Theory")
    content.append("")
    content.append("Introduced in the [[01-First-Post]] thread. Bitcoin's price action follows approximately 7-year cycles, divided into distinct phases marked by colored arrows:")
    content.append("")
    content.append("| Arrow | Phase | Description |")
    content.append("|---|---|---|")
    content.append("| 🟡 Yellow | Start | RSI dips below 43.83 — cycle bottom forms |")
    content.append("| 🟠 Orange | 1st impulse | First bullish move after the bottom |")
    content.append("| 🔵 Blue | 2nd impulse | Main parabolic leg begins |")
    content.append("| 🔴 Red | Top | Cycle top — RSI above 71.52 |")
    content.append("| 🟢 Green | Bear market start | Bull market ends, accumulation begins |")
    content.append("")
    content.append("The RSI levels are critical:")
    content.append("- **RSI 71.52** → Top confirmation")
    content.append("- **RSI 43.82** → Bottom confirmation (buy zone)")
    content.append("")
    content.append("## RSI Crossover Strategy")
    content.append("")
    content.append("The most frequently cited entry signal (see [[04-Glossary#QED]] for his confirmation marker).")
    content.append("")
    content.append("**Rule:** When the **weekly RSI crosses above its moving average**, it produces a buy signal. Historically:")
    content.append("- **100% win rate** — every crossover produced a profitable trade")
    content.append("- Average return: ~202%")
    content.append("- Best: 2,300% (Nov 2012)")
    content.append("- Worst: 14% (Apr 2016)")
    content.append("- 31st crossover occurred in September 2024")
    content.append("")
    content.append("## Key Indicators Used")
    content.append("")
    content.append("| Indicator | Purpose |")
    content.append("|---|---|")
    content.append("| **RSI** | Momentum oscillator — primary signal generator |")
    content.append("| **StochRSI** | RSI of RSI — finer timing for entries/exits |")
    content.append("| **MA7, MA21, MA77** | Short/medium/long moving averages |")
    content.append("| **EMA231** | Very long-term trend filter (~1 year) |")
    content.append("| **BBW** (Bollinger Band Width) | Volatility contraction → expansion signals |")
    content.append("| **Below-Below-Below** | Multi-timeframe RSI confirmation (see [[03-Raicher-Strategy]]) |")
    content.append("")
    content.append("## Colored Arrow System")
    content.append("")
    content.append("His charts use a consistent color-coding system that makes the analysis scannable at a glance. Each arrow represents a structural inflection point. The system evolved from the 7-year cycle theory and became more granular over time.")
    content.append("")
    content.append("## Key RSI Levels")
    content.append("")
    content.append("- **Below 30**: Oversold — accumulation zone")
    content.append("- **30-50**: Bearish momentum")
    content.append("- **50**: Midline — bullish/bearish divide")
    content.append("- **50-70**: Bullish momentum")
    content.append("- **Above 70**: Overbought — can stay overbought in trends")
    content.append("- **71.52**: His specific top confirmation level")
    content.append("- **43.83**: His specific bottom confirmation level")
    content.append("")
    content.append("## Timeframe Hierarchy")
    content.append("")
    content.append("He analyzes multiple timeframes and uses confluences across them:")
    content.append("1. **Monthly** — macro cycle phase, RSI on monthly")
    content.append("2. **Weekly** — primary trend, RSI crossover signals")
    content.append("3. **Daily** — short-term analysis, entries/exits")
    content.append("4. **4H / 1H** — intraday timing (less common)")
    content.append("")
    content.append("## Signature Terms")
    content.append("")
    content.append("See [[04-Glossary]] for the full glossary.")
    content.append("")
    content.append("- **QED** — *Quod Erat Demonstratum* — his \"told you so\" when price hits a predicted target")
    content.append("- **Agulhada** — Triple moving average cross that defines hidden trend lines")
    content.append("- **Nostreidamos** — His analysis brand/telegram channel")
    content.append("- **Flechas** — Colored arrows for cycle phases")
    content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 7: Evolution Timeline
# ============================================================

def gen_evolution():
    content = []
    content.append("---")
    content.append("tags: [analysis, evolution, timeline]")
    content.append("aliases: [timeline, history]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Evolution of the Method")
    content.append("")
    content.append("A chronological timeline of how @raicher's Bitcoin analysis developed on X.")
    content.append("")
    
    # Group tweets by month
    monthly_groups = defaultdict(list)
    for t in analysis_chrono:
        month_key = t.get("created_at", "")[:7]  # YYYY-MM
        monthly_groups[month_key].append(t)
    
    # Generate timeline entries for key milestones
    milestones = []
    
    for t in analysis_chrono:
        text = t.get("text", "").lower()
        date = t.get("created_at", "")[:10]
        tweet_id = t["id"]
        
        # Check for introduction/tutorial-style posts
        if "nunca mostrei" in text or "primeira vez" in text:
            milestones.append((date, f"Introduced a new concept: \"{t['text'][:80]}...\"", tweet_id))
        elif "vamos lá" in text:
            milestones.append((date, f"Major strategy post: RSI crossover breakdown", tweet_id))
        elif "raicher strategy" in text.lower():
            milestones.append((date, f"Mentioned the Raicher Strategy indicator", tweet_id))
        elif "faq" in text or "o que significa" in text:
            milestones.append((date, f"FAQ / explainer post", tweet_id))
        elif "qed" in text.lower() and t.get("public_metrics", {}).get("like_count", 0) > 100:
            milestones.append((date, f"QED — price target hit", tweet_id))
    
    # Key milestones (manually curated from known data)
    known_milestones = [
        ("2024-05-17", "First Bitcoin analysis post — 7-year cycle theory", "1791582201672606146"),
        ("2024-05-27", "Monthly strategy: colored arrow system explained", ""),
        ("2024-06-05", "RSI Weekly crossover strategy — 100% historical win rate", ""),
        ("2024-09-23", "31st RSI crossover confirmed — \"Hadouken, iniciantes!\"", ""),
        ("2024-10-28", "Raicher Strategy 2 indicator mentioned", ""),
        ("2024-12-15", "FAQ post: QED, Agulhada, and method terminology explained", ""),
        ("2025-02-04", "Below-Below-Below multi-timeframe strategy", ""),
    ]
    
    content.append("## Key Milestones")
    content.append("")
    content.append("| Date | Event |")
    content.append("|---|---|")
    for date, event, tid in known_milestones:
        date_display = fmt_date_short(date)
        content.append(f"| {date_display} | {event} |")
    content.append("")
    
    content.append("## Monthly Activity")
    content.append("")
    content.append("Bitcoin analysis tweets per month since May 2024:")
    content.append("")
    content.append("| Month | Tweets |")
    content.append("|---|---|")
    for month in sorted(monthly_groups.keys()):
        count = len(monthly_groups[month])
        content.append(f"| {month} | {count} |")
    content.append("")
    
    content.append("## Method Progression")
    content.append("")
    content.append("1. **May 2024** — Introduced 7-year cycle theory with colored arrows")
    content.append("2. **June 2024** — Perfected the weekly RSI crossover strategy")
    content.append("3. **September 2024** — Live tracking of the 31st RSI crossover")
    content.append("4. **October 2024** — Developed Raicher Strategy 2 indicator")
    content.append("5. **December 2024** — Formalized the method with FAQ and glossary")
    content.append("6. **2025** — Consistent daily/weekly analysis cadence established")
    content.append("7. **2026** — Multi-timeframe approach (Below-Below-Below), BBW indicators")
    content.append("")
    content.append("See [[01-First-Post]] for the origin, and [[02-Methodology]] for the current method.")
    content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 4: Glossary
# ============================================================

def gen_glossary():
    content = []
    content.append("---")
    content.append("tags: [analysis, glossary, reference]")
    content.append("aliases: [glossary, terms, dictionary]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Glossary")
    content.append("")
    content.append("Terms and concepts used in @raicher's Bitcoin analysis.")
    content.append("")
    
    glossary_entries = [
        {
            "term": "QED",
            "aliases": ["Quod Erat Demonstratum"],
            "definition": "Latin for \"which was to be demonstrated.\" Raicher's signature when price hits a predicted target. Used as a closing marker on successful trades and predictions.",
            "example": "\"QED, fechamos com uma vela HORROROSA...\"",
        },
        {
            "term": "Agulhada",
            "aliases": ["Agulhadas", "Needle"],
            "definition": "The crossing of 3 moving averages at the same chart point. An agulhada doesn't have a direction — it's just a point. Connecting agulhadas reveals hidden trend lines that aren't visible otherwise.",
            "example": "\"a agulhada clássica\"",
        },
        {
            "term": "Flechas (Arrows)",
            "aliases": ["Flechinha", "Colored arrows"],
            "definition": "Colored markers on charts indicating cycle phases: Yellow (start), Orange (1st impulse), Blue (2nd impulse), Red (top), Green (bear market). Each corresponds to specific RSI levels.",
            "example": "\"estamos na altura da 2ª flecha laranja\"",
        },
        {
            "term": "Nostreidamos",
            "definition": "Portuguese portmanteau roughly meaning \"we will prove it.\" His analysis brand. Also the name of his Telegram channel where high-res charts are shared.",
            "example": "\"Raicher's Gulch — Versão em alta resolução exclusiva pro Telegram\"",
        },
        {
            "term": "Iniciante™",
            "aliases": ["iniciante"],
            "definition": "Portuguese for \"beginner.\" His self-deprecating brand. Used as a sign-off on analysis posts (\"GN, iniciantes™\"). Contrasts with the advanced nature of the analysis.",
            "example": "\"GN, iniciantes™\"",
        },
        {
            "term": "Below-Below-Below",
            "aliases": ["BBB", "abaixo-abaixo-abaixo"],
            "definition": "A multi-timeframe RSI strategy where RSI is below key levels across 3 timeframes simultaneously, creating a high-probability reversal setup.",
            "example": "\"Lembra da estratégia BELOW-BELOW-BELOW, iniciante?\"",
        },
        {
            "term": "Raicher Strategy 2",
            "aliases": ["RS2"],
            "definition": "A custom indicator developed by Raicher for monthly chart analysis. First mentioned in October 2024. Identifies purple arrow signals on the monthly timeframe.",
            "example": "\"segundo o meu indicador (Raicher Strategy 2)\"",
        },
        {
            "term": "BBW",
            "aliases": ["Bollinger Band Width"],
            "definition": "Bollinger Bands Width indicator. Used to measure volatility contraction and expansion. Low BBW = compression phase → expected expansion.",
            "example": "\"Lembram quando fiz essa previsão baseada no BBW em Julho?\"",
        },
        {
            "term": "Linha Solar",
            "aliases": ["Solar Line"],
            "definition": "A trend line derived from connecting specific candle wicks (\"agulhadas\"). Projects future price levels. Mentioned in Dec 2024 projecting BTC to 130K.",
            "example": "\"Caso o Bitcoin ganhe de volta a Linha Solar ☀️\"",
        },
        {
            "term": "Linha Azul",
            "aliases": ["Blue Line"],
            "definition": "The dominant trend line on the daily chart. Born from agulhadas on Oct 15, 2023 and Aug 2, 2024. Represents the primary daily trend.",
            "example": "\"Tivemos 22 dias de férias acima da linha Azul\"",
        },
        {
            "term": "EMA231",
            "definition": "Exponential Moving Average of 231 periods. Used as a long-term trend filter on the daily chart. Acts as support/resistance.",
            "example": "\"343 fechou MAIS UMA VEZ acima da EMA231\"",
        },
        {
            "term": "RSI 43.83 / 71.52",
            "definition": "Specific RSI levels used as cycle inflection points. 43.83 = bottom confirmation (buy). 71.52 = top confirmation (sell). These are unique to his analysis, not standard RSI levels.",
            "example": "\"RSI 71.52: Confirmação de topo / RSI 43.82: Confirmação de fundo\"",
        },
    ]
    
    for entry in glossary_entries:
        content.append(f"### {entry['term']}")
        content.append("")
        if entry.get("aliases") and len(entry["aliases"]) > 0:
            aliases_str = ", ".join(entry["aliases"])
            content.append(f"**Also known as:** {aliases_str}")
            content.append("")
        content.append(entry["definition"])
        content.append("")
        if entry.get("example"):
            content.append(f"> *\"{entry['example']}\"*")
            content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 8: Bio / Account History
# ============================================================

def gen_bio():
    content = []
    content.append("---")
    content.append("tags: [analysis, bio, account]")
    content.append("aliases: [about, history]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# About @raicher")
    content.append("")
    content.append("## Account")
    content.append("")
    content.append("| Field | Value |")
    content.append("|---|---|")
    content.append("| Username | `@raicher` |")
    content.append("| Display Name | Raicher |")
    content.append("| Bio | `iniciante™ @bitcoinheiros • WWJGD?` |")
    content.append("| Joined | April 14, 2008 |")
    content.append("| User ID | `14380292` |")
    content.append("| Total Tweets | ~17,029 |")
    content.append("| Following | 1,078 |")
    content.append("| Followers | 16,070 |")
    content.append("")
    content.append("## First Tweet Ever")
    content.append("")
    content.append("**April 14, 2008** — the day he joined:")
    content.append("")
    content.append("> *\"Resolvendo problemas das minhas funcionárias, ou melhor, das minhas patroas hahahahaha!\"*")
    content.append(">")
    content.append("> *\"Solving problems for my employees, or rather, for my bosses hahahahaha!\"*")
    content.append("")
    content.append("The account was mostly inactive or used for casual posts (astrophotography, aurora borealis, general replies) for ~16 years.")
    content.append("")
    content.append("## Transition to Bitcoin Analysis")
    content.append("")
    content.append("In **May 2024**, @raicher began posting Bitcoin technical analysis. The trigger appears to have been the Bitcoin halving cycle (April 2024) and the developing bull market. He introduced his 7-year cycle theory on [[01-First-Post]] and has been posting consistently ever since.")
    content.append("")
    content.append("## Related Accounts")
    content.append("")
    content.append("| Account | Relation |")
    content.append("|---|---|")
    content.append("| `@bitcoinheiros` | Bitcoin education channel he promotes |")
    content.append("| `nostreidamos` (Telegram) | High-res chart sharing |")
    content.append("")
    content.append("## Interesting Facts")
    content.append("")
    content.append("- His real name is Allan (revealed by people in replies)")
    content.append("- Lives in California (posts aurora photos from his backyard)")
    content.append("- Has an Instagram where he posted the original 7-year cycle explanation (username: `hromeutetao`)")
    content.append("- Self-identifies as \"iniciante\" (beginner) despite sophisticated analysis")
    content.append("- Uses \"GN\" (Good Night) as a consistent sign-off")
    content.append("- Responds to trolls with humor and confidence")
    content.append("")
    content.append("See the [[06-Corpus]] for the full chronological archive of his analysis posts.")
    content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 3: Raicher Strategy
# ============================================================

def gen_raicher_strategy():
    content = []
    content.append("---")
    content.append("tags: [analysis, strategy, below-below, raicher-strategy]")
    content.append("aliases: [strategy, raicher-strategy-2, below-below-below]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Raicher Strategy & Indicators")
    content.append("")
    content.append("## Raicher Strategy 2")
    content.append("")
    content.append("A custom indicator developed for monthly chart analysis. First publicly mentioned on October 28, 2024:")
    content.append("")
    content.append("> *\"Em menos de 4 dias, vamos registrar mais uma vela Mensal do $BTCUSD. Se fechar no patamar atual (3ª flecha Roxa), segundo o meu indicador (Raicher Strategy 2), estamos numa situação semelhante às duas flechas Roxas anteriores (11/2015 e 04/2020).\"*")
    content.append("")
    content.append("The RS2 indicator identifies purple arrow signals on the monthly timeframe — analogous to the orange/blue/red arrow system but at a higher macro level. Purple arrows appeared only 3 times in Bitcoin history:")
    content.append("1. November 2015")
    content.append("2. April 2020")
    content.append("3. October 2024 (current)")
    content.append("")
    content.append("## Below-Below-Below Strategy")
    content.append("")
    content.append("A multi-timeframe confluence strategy. The name means RSI is below key levels across three timeframes simultaneously. This creates a high-probability reversal setup because all timeframes agree on the direction.")
    content.append("")
    content.append("The strategy was developed for the 2-day chart and has produced 5 historical green arrow signals.")
    content.append("")
    content.append("> *\"Aqui estão as 5 flechinhas Verdes da história do gráfico de 2 Dias Below-Below-Below para seu deleite visual.\"*")
    content.append("")
    content.append("## BBW (Bollinger Band Width) Strategy")
    content.append("")
    content.append("Uses Bollinger Bands Width to identify volatility contraction phases. When BBW compresses to extreme lows, it historically precedes major Bitcoin price expansions.")
    content.append("")
    content.append("Raicher made a notable BBW-based prediction in July 2024 that he referenced months later when it played out:")
    content.append("")
    content.append("> *\"Lembram quando fiz essa previsão baseada no BBW em Julho? Vejam como seguimos exatamente dentro da área verde da previsão até agora.\"*")
    content.append("")
    content.append("## Linha Solar (Solar Line)")
    content.append("")
    content.append("A trend line derived from two agulhadas — the Trump election candle wick and the December 4, 2024 agulhada. In December 2024, Raicher projected this line would intersect 130K on December 30.")
    content.append("")
    content.append("## Linha Azul (Blue Line)")
    content.append("")
    content.append("The dominant daily trend line, born from agulhadas on October 15, 2023 and August 2, 2024. Used as the primary support/resistance on the daily chart. Breaking below this line was a significant bearish signal (discussed in December 2024).")
    content.append("")
    content.append("See [[02-Methodology]] for how these strategies fit into the overall system.")
    content.append("")
    
    return "\n".join(content)


# ============================================================
# NOTE 5: Key Predictions
# ============================================================

def gen_key_predictions():
    content = []
    content.append("---")
    content.append("tags: [analysis, predictions, qed]")
    content.append("aliases: [predictions, calls, qed-moments]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Key Predictions & QED Moments")
    content.append("")
    content.append("Notable calls where @raicher made a prediction and later marked it with QED (\"Quod Erat Demonstratum\").")
    content.append("")
    
    # Find QED tweets with high engagement
    qed_tweets = [t for t in analysis_chrono if "qed" in t.get("text", "").lower()]
    key_tweets = sorted(qed_tweets, key=lambda t: t.get("public_metrics", {}).get("like_count", 0), reverse=True)[:15]
    
    if key_tweets:
        content.append("## Top QED Posts by Engagement")
        content.append("")
        for t in key_tweets:
            content.append(tweet_callout(t))
    
    content.append("## Notable Predictions")
    content.append("")
    content.append("While many predictions are embedded in ongoing analysis threads, key forward-looking statements from the corpus include:")
    content.append("")
    
    # Find price target tweets
    target_tweets = [t for t in analysis_chrono if any(x in t.get("text", "").lower() for x in ["k usd", "k$", "usd", "previsão", "alvo", "target", "projetando", "100k", "130k", "242k"])]
    for t in target_tweets[:10]:
        text = t.get("text", "")
        likes = t.get("public_metrics", {}).get("like_count", 0)
        if likes > 50:
            content.append(tweet_callout(t))
    
    return "\n".join(content)


# ============================================================
# NOTE 6: Full Corpus
# ============================================================

def gen_corpus():
    content = []
    content.append("---")
    content.append("tags: [analysis, corpus, archive]")
    content.append("aliases: [all-tweets, complete-archive]")
    content.append("created: 2026-05-20")
    content.append("---")
    content.append("")
    content.append("# Full Corpus — Bitcoin Analysis Tweets")
    content.append("")
    content.append(f"All {len(analysis_chrono)} Bitcoin analysis tweets from @raicher, in chronological order (oldest first).")
    content.append("")
    content.append(f"**Date range:** {fmt_date_short(analysis_chrono[0].get('created_at',''))} → {fmt_date_short(analysis_chrono[-1].get('created_at',''))}")
    content.append("")
    
    for t in analysis_chrono:
        content.append("---")
        content.append("")
        content.append(tweet_callout(t))
    
    return "\n".join(content)


# ============================================================
# Main Generation
# ============================================================

def main():
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    
    generators = [
        ("01-First-Post.md", gen_first_post),
        ("02-Methodology.md", gen_methodology),
        ("03-Raicher-Strategy.md", gen_raicher_strategy),
        ("04-Glossary.md", gen_glossary),
        ("05-Key-Predictions.md", gen_key_predictions),
        ("06-Corpus.md", gen_corpus),
        ("07-Evolution.md", gen_evolution),
        ("08-Bio.md", gen_bio),
    ]
    
    print("=" * 60)
    print("  Phase 3: Generate Obsidian Vault Notes")
    print("=" * 60)
    
    for filename, gen_fn in generators:
        print(f"  Generating {filename}...", end=" ")
        content = gen_fn()
        filepath = os.path.join(ANALYSIS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"({size_kb:.0f} KB)")
    
    # Count total lines across all files
    total_lines = 0
    for filename, _ in generators:
        filepath = os.path.join(ANALYSIS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            total_lines += len(f.readlines())
    
    print(f"\n{'='*60}")
    print(f"  PHASE 3 COMPLETE")
    print(f"{'='*60}")
    print(f"  Notes generated: {len(generators)}")
    print(f"  Output: {ANALYSIS_DIR}")
    print(f"  Total lines: {total_lines}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
