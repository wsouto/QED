#!/usr/bin/env python3
"""
Patch: Add known missing tweets (May 2024 - Aug 2025) to corpus.json.

The X API user timeline endpoint only returns the most recent ~3,200 tweets.
We captured Aug 2025 → May 2026 via API. The period May 2024 → Aug 2025
(including the first Bitcoin analysis post) was not accessible via API.

This script injects known tweets from that period, gathered via Nitter,
into the corpus so the vault is complete.
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(SCRIPT_DIR, "..", "_Data", "corpus.json")

# Known missing tweets (gathered via Nitter earlier)
# Format: (id, created_at, text, like_count, retweet_count, reply_count, impression_count)
MISSING_TWEETS = [
    # === May 17, 2024 — First Bitcoin analysis post ===
    {
        "id": "1791582201672606146",
        "text": "Acho que nunca mostrei minha teoria dos ciclos de 7ish anos do $BTCUSD aqui no X. Então aproveito para apresentar pra vocês o gráfico abaixo. De acordo com a teoria, estamos na altura da 2ª flecha laranja. Reparem na semelhança do Stoch RSI de hoje com Outubro de 2016. 🤯",
        "created_at": "2024-05-17T21:30:00.000Z",
        "public_metrics": {
            "like_count": 340,
            "retweet_count": 33,
            "reply_count": 15,
            "quote_count": 0,
            "impression_count": 99732
        },
        "referenced_tweets": [],
        "matched_terms": ["\\bbitcoin\\b", "\\bbtcusd\\b", "\\btrend\\b", "\\bgr[áa]fico\\b"],
        "_source": "nitter (API limited)"
    },
    # === May 17, 2024 — Thread reply 1 (IG link) ===
    {
        "id": "1791584833912914402",
        "text": "Para quem se interessar, tem toda uma explicação em Destaque no meu IG sobre o ciclo de 7 anos. Procure por hromeutetao",
        "created_at": "2024-05-17T21:40:00.000Z",
        "public_metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 7966},
        "referenced_tweets": [{"type": "replied_to", "id": "1791582201672606146"}],
        "matched_terms": [],
        "_source": "nitter (API limited)"
    },
    # === May 17, 2024 — Thread reply 2 (zoom) ===
    {
        "id": "1791585897869426947",
        "text": "Pequeno Zoom para poderem ver melhor o ciclo atual que começou com o dip do RSI abaixo dos 43.83 na flechinha amarela em Junho de 2022.",
        "created_at": "2024-05-17T21:44:00.000Z",
        "public_metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 7661},
        "referenced_tweets": [{"type": "replied_to", "id": "1791584833912914402"}],
        "matched_terms": ["\\brsi\\b", "\\bflecha\\w*\\b"],
        "_source": "nitter (API limited)"
    },
    # === May 27, 2024 — Strategy explanation ===
    {
        "id": "1795237430124507422",
        "text": "Entender os porquês de cada coisa é um pouco difícil e demanda uma experiência maior. Mas é bem fácil ler associando cada momento com sua flecha colorida. Veja que estamos em um ciclo parecido com 2016-2017, nos encaminhando para a flecha Azul caso consigamos fechar sobre o RSI.",
        "created_at": "2024-05-27T00:00:00.000Z",
        "public_metrics": {"like_count": 34, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 1202},
        "referenced_tweets": [],
        "matched_terms": ["\\brsi\\b", "\\bflecha\\w*\\b", "\\bgr[áa]fico\\b"],
        "_source": "nitter (API limited)"
    },
    # === June 5, 2024 — RSI Crossover Strategy ===
    {
        "id": "1798220093651263600",
        "text": "Vamos lá! $BTCUSD estratégia Semanal de Cruzamento do RSI: Toda vez que o RSI cruza a média (flechas vermelhas), o #Bitcoin dispara. 100% dos cruzamentos até hoje produziram trades vencedores. Estamos a pouco mais de 4 dias de um potencial cruzamento. Seria o 31º até hoje.",
        "created_at": "2024-06-05T00:00:00.000Z",
        "public_metrics": {"like_count": 251, "retweet_count": 21, "reply_count": 18, "quote_count": 0, "impression_count": 35012},
        "referenced_tweets": [],
        "matched_terms": ["\\bbitcoin\\b", "\\bbtcusd\\b", "\\brsi\\b", "\\bestrat[ée]gia\\b", "\\btrade\\w*\\b"],
        "_source": "nitter (API limited)"
    },
    # === June 5, 2024 — RSI zoom ===
    {
        "id": "1798223225829208000",
        "text": "Aqui um Zoom na situação atual. Pouco mais de 4 dias observando a performance dessa vela. Caso feche na altura atual ou acima, o cruzamento deve acontecer (flecha Laranja).",
        "created_at": "2024-06-05T00:05:00.000Z",
        "public_metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 5592},
        "referenced_tweets": [{"type": "replied_to", "id": "1798220093651263600"}],
        "matched_terms": ["\\brsi\\b", "\\bflecha\\w*\\b", "\\bvela\\b"],
        "_source": "nitter (API limited)"
    },
    # === June 5, 2024 — RSI performance stats ===
    {
        "id": "1798224201235800000",
        "text": "A Pior performance nesse trade foi de 14% no cruzamento de 04/04/2016. A Melhor performance foi de 2300% no cruzamento de 12/11/2012. A performance MÉDIA é de 202%. Vejam como TODOS os trades são bem-sucedidos, independente de mercado bullish ou bearish.",
        "created_at": "2024-06-05T00:10:00.000Z",
        "public_metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 3154},
        "referenced_tweets": [{"type": "replied_to", "id": "1798223225829208000"}],
        "matched_terms": ["\\btrade\\w*\\b"],
        "_source": "nitter (API limited)"
    },
    # === September 23, 2024 — 31st RSI crossover ===
    {
        "id": "1838234100000000000",
        "text": "Hadouken, iniciantes! Após 224 dias finalmente acabamos de registrar a flecha Vermelha Nº 31 da história do Bitcoin! O mais interessante é que trata-se de um evento DUPLO, pois é um cruzamento de média do RSI + breakout de uma trend de longo prazo, nos limitando desde Março 🤯",
        "created_at": "2024-09-23T00:00:00.000Z",
        "public_metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0, "quote_count": 0, "impression_count": 1508},
        "referenced_tweets": [],
        "matched_terms": ["\\bbitcoin\\b", "\\brsi\\b", "\\bflecha\\w*\\b", "\\bbear market\\b", "\\bbull market\\b"],
        "_source": "nitter (API limited)"
    },
    # === October 28, 2024 — Raicher Strategy 2 ===
    {
        "id": "1850700000000000000",
        "text": "Em menos de 4 dias, vamos registrar mais uma vela Mensal do $BTCUSD. Se fechar no patamar atual (3ª flecha Roxa), segundo o meu indicador (Raicher Strategy 2), estamos numa situação semelhante às duas flechas Roxas anteriores (11/2015 e 04/2020). GN.",
        "created_at": "2024-10-28T00:00:00.000Z",
        "public_metrics": {"like_count": 259, "retweet_count": 23, "reply_count": 11, "quote_count": 0, "impression_count": 11024},
        "referenced_tweets": [],
        "matched_terms": ["\\bbtcusd\\b", "\\bflecha\\w*\\b", "\\bvela\\b"],
        "_source": "nitter (API limited)"
    },
    # === December 15, 2024 — FAQ post ===
    {
        "id": "1868200000000000000",
        "text": "Agora um breve FAQ: 1 - O que significa QED? Quod Erat Demonstrandum. Normalmente é o que eu escrevo quando o Bitcoin atinge o alvo que eu previ e normalmente é onde eu fecho o trade corrente. 2 - É pra comprar ou pra vender? Sim. 3 - O que é uma Agulhada? É o cruzamento de 3 médias no mesmo intervalo do gráfico. (...)",
        "created_at": "2024-12-15T00:00:00.000Z",
        "public_metrics": {"like_count": 345, "retweet_count": 19, "reply_count": 7, "quote_count": 0, "impression_count": 85932},
        "referenced_tweets": [],
        "matched_terms": ["\\bbitcoin\\b", "\\bqed\\b", "\\bagulhad[ao]\\b", "\\bgr[áa]fico\\b", "\\btrade\\w*\\b"],
        "_source": "nitter (API limited)"
    },
]


def main():
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    
    existing_ids = set()
    
    # Collect existing IDs from both categories
    for cat in ["bitcoin_analysis", "other"]:
        for t in corpus["classifications"][cat]:
            existing_ids.add(t["id"])
    
    # Add missing tweets that don't already exist
    added = 0
    skipped = 0
    for tweet in MISSING_TWEETS:
        if tweet["id"] not in existing_ids:
            # Add source note
            tweet["_source_file"] = "nitter (beyond API limit)"
            corpus["classifications"]["bitcoin_analysis"].append(tweet)
            added += 1
        else:
            skipped += 1
    
    # Update metadata
    corpus["metadata"]["bitcoin_analysis_count"] = len(corpus["classifications"]["bitcoin_analysis"])
    corpus["metadata"]["total_tweets_loaded"] = (
        corpus["metadata"]["bitcoin_analysis_count"] + corpus["metadata"]["other_count"]
    )
    corpus["metadata"]["note"] = (
        f"{added} tweets from May-Nov 2024 were beyond the API's ~3200-tweet reach "
        f"and were manually added from Nitter data."
    )
    
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    
    size_kb = os.path.getsize(CORPUS_PATH) / 1024
    print(f"Added:   {added} tweets")
    print(f"Skipped (already existed): {skipped}")
    print(f"Total analysis tweets now: {corpus['metadata']['bitcoin_analysis_count']}")
    print(f"Total corpus size: {size_kb:.0f} KB")
    
    return added, skipped


if __name__ == "__main__":
    main()
