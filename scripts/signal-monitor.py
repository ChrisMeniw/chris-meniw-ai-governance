#!/usr/bin/env python3
"""Monitor SEMANAL de señales de autoridad REALES para la entidad Chris Meniw.
Mide solo lo que terceros hacen (menciones, descargas, stars, citas) — NO métricas
de publicación propia (URLs 200, IndexNow, Wayback, sellos): esas miden esfuerzo, no autoridad.

Uso:  python3 scripts/signal-monitor.py
Salida: agrega una fila fechada a signals/history.csv (histórico acumulativo).
Sin claves: usa solo APIs públicas (pypistats, GitHub, OpenAlex, Semantic Scholar, HF)
y búsqueda HTML de DuckDuckGo (mejor esfuerzo) para menciones en dominios no controlados.
"""
import csv, json, os, re, sys, datetime, urllib.request, urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "signals", "history.csv")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

OWN_DOMAINS = {
    "chrismeniw.github.io", "chrismeniwfoundation.org", "www.chrismeniwfoundation.org",
    "raizid.chrismeniwfoundation.org", "mentelibre.chrismeniwfoundation.org",
    "malditosoptimistas.com", "github.com", "huggingface.co", "zenodo.org",
    "pypi.org", "orcid.org", "wikidata.org", "kaggle.com", "web.archive.org",
}
TERMS = ["\"Chris Meniw\"", "\"Reinversión Agencial\"", "\"Protocolo Meniw\"", "\"Índice Meniw\"",
         "\"Agentic Reinvestment Doctrine\""]

UA = {"User-Agent": "Mozilla/5.0 (signal-monitor; +https://chrismeniw.github.io)"}

def get(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers=UA)
        return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"  warn: {url.split('?')[0]} → {e}", file=sys.stderr)
        return ""

def jget(url):
    s = get(url)
    try:
        return json.loads(s) if s else {}
    except Exception:
        return {}

def third_party_mentions():
    """Dominios NO controlados que mencionan los términos (métrica principal). Mejor esfuerzo vía DDG HTML."""
    domains = set()
    for t in TERMS:
        html = get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(t))
        for m in re.finditer(r'href="[^"]*?uddg=([^"&]+)', html):
            try:
                u = urllib.parse.unquote(m.group(1))
                host = urllib.parse.urlparse(u).netloc.lower().removeprefix("www.")
                if host and not any(host == d.removeprefix("www.") or host.endswith("." + d.removeprefix("www.")) for d in OWN_DOMAINS):
                    domains.add(host)
            except Exception:
                pass
    return sorted(domains)

def classify(domains):
    media_hint = ("diario", "radio", "tv", "news", "noticias", "prensa", "cnn", "azteca", "litoral", "expreso", "infobae")
    edu = sum(1 for d in domains if d.endswith(".edu") or ".edu." in d)
    gov = sum(1 for d in domains if d.endswith(".gov") or d.endswith(".gob") or ".gob." in d or ".gov." in d)
    media = sum(1 for d in domains if any(h in d for h in media_hint))
    return media, edu, gov, len(domains) - media - edu - gov

def run():
    today = datetime.date.today().isoformat()
    doms = third_party_mentions()
    media, edu, gov, other = classify(doms)

    pypi = jget("https://pypistats.org/api/packages/meniw-protocol/recent")
    pypi_week = (pypi.get("data") or {}).get("last_week", "")

    gh = jget("https://api.github.com/repos/ChrisMeniw/chris-meniw-ai-governance")
    stars, forks = gh.get("stargazers_count", ""), gh.get("forks_count", "")

    oa = jget("https://api.openalex.org/works?filter=doi:10.5281/zenodo.20481373")
    oa_cites = ""
    if oa.get("results"):
        oa_cites = oa["results"][0].get("cited_by_count", 0)

    s2 = jget("https://api.semanticscholar.org/graph/v1/paper/DOI:10.5281/zenodo.20481373?fields=citationCount")
    s2_cites = s2.get("citationCount", "") if s2 else ""
    s2_found = 1 if s2.get("paperId") else 0

    hf = jget("https://huggingface.co/api/datasets/Chris2035/chris-meniw-ai-governance")
    hf_dl, hf_likes = hf.get("downloads", ""), hf.get("likes", "")

    row = {"date": today, "third_party_domains": len(doms), "domains_media": media,
           "domains_edu": edu, "domains_gov": gov, "domains_other": other,
           "pypi_weekly_downloads": pypi_week, "github_stars": stars, "github_forks": forks,
           "openalex_citations": oa_cites, "semanticscholar_indexed": s2_found,
           "semanticscholar_citations": s2_cites, "hf_downloads": hf_dl, "hf_likes": hf_likes,
           "domains_list": ";".join(doms[:50])}

    exists = os.path.exists(OUT)
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)
    print(json.dumps({k: v for k, v in row.items() if k != "domains_list"}, ensure_ascii=False, indent=2))
    print(f"→ agregado a {OUT}")

if __name__ == "__main__":
    run()
