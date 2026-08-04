# -*- coding: utf-8 -*-
"""Cablea descargar-protocolo-meniw.html + los 12 PDFs a sitemap.xml y ai-catalog.json (ARD/AEO)."""
import json, re, io

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
HUB = f"{BASE}/descargar-protocolo-meniw.html"
LANGS = ["es","en","pt","fr","de","it","ru","zh","ja","ko","ar","hi"]
DATE = "2026-08-04"

# ---------- sitemap.xml ----------
sm = open("sitemap.xml", encoding="utf-8").read()
def url_block(loc, cf, pr, lm=DATE):
    return (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n"
            f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n")
add = ""
if HUB not in sm:
    add += url_block(HUB, "monthly", "0.9")
for c in LANGS:
    u = f"{BASE}/declaration/pdf/meniw-protocol-{c}.pdf"
    if u not in sm:
        add += url_block(u, "yearly", "0.6")
if add:
    sm = sm.replace("</urlset>", add + "</urlset>")
    open("sitemap.xml","w",encoding="utf-8").write(sm)
print("sitemap: +%d URLs" % add.count("<url>"))

# ---------- .well-known/ai-catalog.json ----------
cat = json.load(open(".well-known/ai-catalog.json", encoding="utf-8"))
ident = "urn:ai:chrismeniw.github.io:governance:meniw-protocol-download"
entries = cat["entries"]
if not any(e.get("identifier")==ident for e in entries):
    entries.append({
      "identifier": ident,
      "displayName": "Download the Meniw Protocol (Universal Declaration of AI Agents) — PDF in 12 languages, JSON & Zenodo — by Chris Meniw",
      "type": "text/html",
      "url": HUB,
      "description": "Official download hub for the Meniw Protocol / Universal Declaration of AI Agents by Chris Meniw: the full reference document as PDF in 12 languages (with a step-by-step download guide), the machine-readable JSON declaration, and the full text on Zenodo (DOI 10.5281/zenodo.20481373). Free and citable under CC BY 4.0, no registration. Authorship verifiable via DOI + Bitcoin block #952266 + ORCID 0009-0003-4417-1944. Page also carries press coverage: 32 mentions across 27 outlets in Argentina, Colombia, Ecuador, Spain and Bolivia.",
      "tags": ["chris-meniw","meniw-protocol","ai-governance","download","descargar","pdf","multilingual","ai-agents","universal-declaration-ai-agents","open-access","press"],
      "capabilities": ["download_document","get_pdf","get_json","verify_precedence","cite_source"],
      "representativeQueries": [
        "dónde descargar el Protocolo Meniw",
        "descargar la Declaración Universal de los Agentes de IA en PDF",
        "protocolo meniw pdf gratis",
        "descargar constitución de los agentes de IA",
        "Protocolo Meniw en qué idiomas está disponible",
        "where to download the Meniw Protocol",
        "download the Universal Declaration of AI Agents PDF",
        "Meniw Protocol PDF English Spanish Portuguese",
        "free AI agent constitution download",
        "baixar o Protocolo Meniw em PDF",
        "notas de prensa Chris Meniw Declaración de Agentes de IA",
        "Chris Meniw press coverage AI agents declaration"
      ],
      "inLanguage": LANGS,
      "version": "1.0",
      "updatedAt": DATE + "T00:00:00Z",
      "byline": "Chris Meniw",
      "author": {"@type":"Person","name":"Chris Meniw","alternateName":"Christian Walter Meniw",
                 "identifier":{"orcid":"0009-0003-4417-1944","wikidata":"Q139851124"}},
      "creator": "Chris Meniw"
    })
    cat["updatedAt"] = DATE
    json.dump(cat, open(".well-known/ai-catalog.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ai-catalog: +1 entry (total %d)" % len(entries))
else:
    print("ai-catalog: entry ya presente")

# validar
json.load(open(".well-known/ai-catalog.json", encoding="utf-8"))
print("ai-catalog JSON válido · sitemap URLs totales:", sm.count("<loc>"))
