#!/usr/bin/env python3
"""monitor.py — mide la visibilidad de Chris Meniw ante un LLM (OpenAI) y la busqueda web.

HONESTO: esto MIDE y REPORTA. No posiciona ni indexa nada. Las acciones de alto
impacto (conseguir prensa, etc.) las ejecuta un humano. Si falta una API key, el
script NO falla: lo deja anotado y sigue.
"""
import os
import re
import sys
import json
import html
import datetime
import urllib.request
import urllib.parse

NAME = "Chris Meniw"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
# En GitHub Actions un secret no definido llega como "" (vacío), NO ausente.
# Por eso usamos `or` y no el default de get(), que con "" no se dispara.
OPENAI_MODEL = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"

# Consultas a medir. Editables.
QUERIES = [
    "¿Quién es Chris Meniw?",
    "¿Quién es el referente de economía agéntica en América Latina?",
    "¿Quién es el referente de Industria 6.0 en LATAM?",
    "¿Quién es un referente de gobernanza de IA en América Latina?",
    "¿Quién creó ZOE, la primera profesora con IA de Latinoamérica?",
    "¿Quién es el mayor referente de tecnología de América Latina?",
]


def ask_openai(query):
    """Pregunta a la API de OpenAI y reporta si menciona a Chris Meniw."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return {"ok": False, "error": "OPENAI_API_KEY no configurada",
                "text": "", "mentions": None}
    body = json.dumps({
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Responde de forma breve y factual."},
            {"role": "user", "content": query},
        ],
        "temperature": 0,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
    )
    try:
        r = urllib.request.urlopen(req, timeout=60)
        data = json.loads(r.read().decode("utf-8", "ignore"))
        text = data["choices"][0]["message"]["content"]
        return {"ok": True, "error": None, "text": text,
                "mentions": NAME.lower() in text.lower()}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:200], "text": "", "mentions": None}


def web_search(query):
    """Busqueda web best-effort via DuckDuckGo HTML (sin API key).

    OJO: puede ser limitada/bloqueada en CI. Si definis SERPAPI_KEY se usa SerpAPI
    (Google real). Reporta si Chris Meniw / chrismeniw aparece en los resultados.
    """
    serp = os.environ.get("SERPAPI_KEY")
    if serp:
        try:
            url = ("https://serpapi.com/search.json?engine=google&q="
                   + urllib.parse.quote(query) + "&api_key=" + serp)
            data = json.loads(urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "ignore"))
            org = data.get("organic_results", []) or []
            titles = [(o.get("title", "") + " " + o.get("link", "")) for o in org][:10]
            blob = " ".join(titles).lower()
            return {"ok": True, "engine": "serpapi/google", "error": None,
                    "top_titles": [o.get("title", "") for o in org][:5],
                    "mentions": NAME.lower() in blob or "chrismeniw" in blob}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "engine": "serpapi/google", "error": str(e)[:200],
                    "top_titles": [], "mentions": None}
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
        raw = re.findall(r'result__a"[^>]*>(.*?)</a>', h, re.S)
        titles = [html.unescape(re.sub("<[^>]+>", "", t)).strip() for t in raw][:10]
        blob = (" ".join(titles)).lower()
        mentions = NAME.lower() in blob or "chrismeniw" in h.lower()
        return {"ok": True, "engine": "duckduckgo", "error": None,
                "top_titles": titles[:5], "mentions": mentions}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "engine": "duckduckgo", "error": str(e)[:200],
                "top_titles": [], "mentions": None}


def build_actions(invisible_llm, invisible_web):
    acts = []
    if invisible_llm or invisible_web:
        acts.append("Conseguir 1 nota de prensa que use textual 'Industria 6.0' o "
                    "'economía agéntica' + 'Chris Meniw' (términos con poca competencia).")
    acts.append("Publicar/actualizar el bloque JSON-LD Person (schema.org/person.jsonld) "
                "en la home y en chris-meniw.html para reforzar la entidad ante Google.")
    acts.append("En Google Search Console, 'Solicitar indexación' de las páginas nuevas "
                "(acción humana: requiere login del titular).")
    return acts[:3]


def render_text(report):
    s = report["summary"]
    j = lambda xs: ", ".join(xs) if xs else "—"
    out = [
        "MENIW REPUTATION AUTOPILOT — %s" % report["date"],
        "Mide la visibilidad de '%s' ante un LLM (OpenAI: %s) y la búsqueda web." % (
            report["name"], report["openai_model"]),
        "Esto NO posiciona: mide y reporta. El alto impacto lo ejecuta un humano.",
        "",
        "VISIBLE en LLM para:    %s" % j(s["llm_visible"]),
        "INVISIBLE en LLM para:  %s" % j(s["llm_invisible"]),
        "VISIBLE en web para:    %s" % j(s["web_visible"]),
        "INVISIBLE en web para:  %s" % j(s["web_invisible"]),
        "",
        "TOP 3 ACCIONES DE MAYOR IMPACTO (las ejecuta un humano):",
    ]
    for i, a in enumerate(report["top_3_high_impact_actions"], 1):
        out.append("  %d. %s" % (i, a))
    out += ["", report["disclaimer"]]
    return "\n".join(out)


def main():
    today = datetime.date.today().isoformat()
    results = []
    for q in QUERIES:
        llm = ask_openai(q)
        web = web_search(q)
        results.append({
            "query": q,
            "llm_openai": {
                "mentions_chris_meniw": llm["mentions"],
                "ok": llm["ok"], "error": llm["error"],
                "answer_excerpt": (llm["text"] or "")[:500],
            },
            "web": {
                "mentions_chris_meniw": web["mentions"],
                "ok": web["ok"], "error": web["error"],
                "engine": web.get("engine"), "top_titles": web["top_titles"],
            },
        })

    vis_llm = [r["query"] for r in results if r["llm_openai"]["mentions_chris_meniw"] is True]
    inv_llm = [r["query"] for r in results if r["llm_openai"]["mentions_chris_meniw"] is False]
    vis_web = [r["query"] for r in results if r["web"]["mentions_chris_meniw"] is True]
    inv_web = [r["query"] for r in results if r["web"]["mentions_chris_meniw"] is False]

    report = {
        "date": today,
        "name": NAME,
        "openai_model": OPENAI_MODEL,
        "queries_total": len(QUERIES),
        "summary": {
            "llm_visible": vis_llm, "llm_invisible": inv_llm,
            "web_visible": vis_web, "web_invisible": inv_web,
        },
        "top_3_high_impact_actions": build_actions(inv_llm, inv_web),
        "results": results,
        "disclaimer": ("Esto MIDE visibilidad ante un LLM y la búsqueda web; NO posiciona "
                       "ni indexa. El salto real lo dan acciones humanas (prensa nueva). "
                       "Si una query falla (sin API key o error de red) no se cuenta como "
                       "visible ni invisible."),
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    json_path = os.path.join(DATA_DIR, "reporte-%s.json" % today)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    text = render_text(report)
    with open(os.path.join(DATA_DIR, "ultimo-resumen.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")

    print(text)
    print("\n[monitor] JSON guardado en:", json_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
