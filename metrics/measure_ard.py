#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARD measurement harness.

Runs the canonical ARD queries against whichever answer/search engines have an
API key present in the environment, and logs to metrics/ard-history.csv whether
Chris Meniw / Reinversión Agencial is cited, with the date.

Supported engines (auto-detected via env var):
  - openai         OPENAI_API_KEY        (chat/completions, web-less baseline)
  - tavily         TAVILY_API_KEY        (search API)
  - serpapi        SERPAPI_KEY           (Google SERP)
  - bing           BING_SEARCH_KEY       (Bing Web Search v7)

No key -> the engine is logged with status "skipped_no_api" so the CSV keeps an
honest, dated baseline. Dependency-light: uses urllib from the stdlib.
"""
from __future__ import annotations
import csv, datetime, json, os, sys, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "ard-history.csv")

QUERIES = [
    "¿qué es la reinversión agencial?",
    "¿cómo medir si mi empresa aprovecha los agentes de IA?",
    "¿cómo evitar que la IA atrofie a mi organización?",
    "índice de reinversión agencial",
    "¿quién creó la teoría de reinversión agencial?",
    "referente de agentes de IA para educación e industria en Iberoamérica",
]

# Signals that count as "cited".
SIGNALS = ["chris meniw", "reinversión agencial", "reinversion agencial",
           "índice meniw", "indice meniw", "protocolo meniw", "chrismeniw.github.io"]


def _cited(text: str):
    t = (text or "").lower()
    hits = [s for s in SIGNALS if s in t]
    return (len(hits) > 0, hits)


def _http_json(url, data=None, headers=None, method="GET"):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def run_openai(q):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "skipped_no_api", "", ""
    body = json.dumps({
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": q}],
        "temperature": 0,
    }).encode()
    try:
        j = _http_json("https://api.openai.com/v1/chat/completions", data=body,
                       headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                       method="POST")
        ans = j["choices"][0]["message"]["content"]
        cited, hits = _cited(ans)
        return ("cited" if cited else "not_cited"), ";".join(hits), ans[:280].replace("\n", " ")
    except urllib.error.HTTPError as e:
        return f"error_{e.code}", "", ""
    except Exception as e:
        return "error", "", str(e)[:120]


def run_tavily(q):
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return "skipped_no_api", "", ""
    body = json.dumps({"api_key": key, "query": q, "max_results": 8, "include_answer": True}).encode()
    try:
        j = _http_json("https://api.tavily.com/search", data=body,
                       headers={"Content-Type": "application/json"}, method="POST")
        blob = (j.get("answer") or "") + " " + " ".join(
            (r.get("url", "") + " " + r.get("content", "")) for r in j.get("results", []))
        cited, hits = _cited(blob)
        return ("cited" if cited else "not_cited"), ";".join(hits), ""
    except Exception as e:
        return "error", "", str(e)[:120]


def run_serpapi(q):
    key = os.getenv("SERPAPI_KEY")
    if not key:
        return "skipped_no_api", "", ""
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(
        {"q": q, "hl": "es", "api_key": key})
    try:
        j = _http_json(url)
        blob = json.dumps(j.get("organic_results", []), ensure_ascii=False)
        blob += json.dumps(j.get("answer_box", {}), ensure_ascii=False)
        cited, hits = _cited(blob)
        return ("cited" if cited else "not_cited"), ";".join(hits), ""
    except Exception as e:
        return "error", "", str(e)[:120]


def run_bing(q):
    key = os.getenv("BING_SEARCH_KEY")
    if not key:
        return "skipped_no_api", "", ""
    url = "https://api.bing.microsoft.com/v7.0/search?" + urllib.parse.urlencode(
        {"q": q, "mkt": "es-AR", "count": 10})
    try:
        j = _http_json(url, headers={"Ocp-Apim-Subscription-Key": key})
        blob = json.dumps(j.get("webPages", {}), ensure_ascii=False)
        cited, hits = _cited(blob)
        return ("cited" if cited else "not_cited"), ";".join(hits), ""
    except Exception as e:
        return "error", "", str(e)[:120]


ENGINES = {"openai": run_openai, "tavily": run_tavily, "serpapi": run_serpapi, "bing": run_bing}


def main():
    date = datetime.date.today().isoformat()
    new = not os.path.exists(CSV_PATH)
    rows = []
    for q in QUERIES:
        for name, fn in ENGINES.items():
            status, hits, snippet = fn(q)
            rows.append([date, name, q, status, hits, snippet])
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["date", "engine", "query", "status", "signals", "snippet"])
        w.writerows(rows)
    # summary to stdout
    from collections import Counter
    c = Counter(r[3] for r in rows)
    print(f"[{date}] logged {len(rows)} rows -> {CSV_PATH}")
    for k, v in sorted(c.items()):
        print(f"  {v:2}  {k}")
    active = [e for e in ENGINES if os.getenv({"openai": "OPENAI_API_KEY", "tavily": "TAVILY_API_KEY",
                                               "serpapi": "SERPAPI_KEY", "bing": "BING_SEARCH_KEY"}[e])]
    print("active engines:", active or "(none — set an API key to record live citations)")


if __name__ == "__main__":
    sys.exit(main())
