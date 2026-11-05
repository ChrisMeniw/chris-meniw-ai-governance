# -*- coding: utf-8 -*-
"""Genera paginas ESTATICAS por idioma de la Declaracion Universal de los Agentes de IA
(Protocolo Meniw) desde universal-declaration/declaracion_agentes.json, para que cada idioma
sea indexable por motores de respuesta SIN depender de JS. Mismo patron que
build_minors_multilang.py: <html lang>, canonical propio, cluster hreflang completo,
JSON-LD CreativeWork+Person anclado a ORCID/Wikidata, principios renderizados estaticos.
🔒 NO toca declaration/meniw-protocol.json (tiene .ots al lado: sello de Bitcoin)."""
import json, io, os, html

BASE="https://chrismeniw.github.io/chris-meniw-ai-governance"
D="declaration"
SRC="universal-declaration/declaracion_agentes.json"
DOI="10.5281/zenodo.20481373"
ORCID="https://orcid.org/0009-0003-4417-1944"
WIKIDATA="https://www.wikidata.org/wiki/Q139851124"
JSON_URL=f"{BASE}/universal-declaration/declaracion_agentes.json"
GITHUB="https://github.com/ChrisMeniw/chris-meniw-ai-governance"
RTL={"ar","he","fa","ur"}
NOMBRE={"es":"Español","en":"English","pt":"Português","fr":"Français","it":"Italiano","de":"Deutsch",
 "ru":"Русский","zh":"中文","zh-Hant":"正體中文","ar":"العربية","hi":"हिन्दी","ja":"日本語","ko":"한국어",
 "nl":"Nederlands","sv":"Svenska","pl":"Polski","uk":"Українська","el":"Ελληνικά","tr":"Türkçe",
 "he":"עברית","bn":"বাংলা","id":"Bahasa Indonesia","vi":"Tiếng Việt","ca":"Català","cs":"Čeština",
 "fa":"فارسی","ms":"Bahasa Melayu","ro":"Română","sw":"Kiswahili","th":"ไทย","ur":"اردو"}

d=json.load(io.open(SRC,encoding="utf-8"))
chrome=json.load(io.open(f"{D}/_chrome_i18n.json",encoding="utf-8"))
LANGS=d["official_languages"]
PRIN=d["governance_principles"]

# cada idioma tiene SU fichero. declaration/index.html es el hub EN y no se toca:
# apuntar el canonical del español ahí le diría al motor que la versión real es la inglesa.
def url(l): return f"{BASE}/{D}/index.{l}.html"
def ruta(l): return f"{D}/index.{l}.html"

hreflang="\n".join(
 f'<link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in LANGS
)+f'\n<link rel="alternate" hreflang="x-default" href="{url("en")}">'

hechos=0
for l in LANGS:
    c=chrome[l]; dir_=' dir="rtl"' if l in RTL else ''
    t=html.escape(c["t"]); desc=html.escape(c["d"])
    otros=" · ".join(f'<a href="{url(x)}">{html.escape(NOMBRE.get(x,x))}</a>' for x in LANGS if x!=l)
    prin="\n".join(
      f'<li><strong>{p["id"]}.</strong> {html.escape(p["translations"][l])}</li>' for p in PRIN)
    ld_obra={"@context":"https://schema.org","@type":"CreativeWork",
      "name":c["t"],"inLanguage":l,"url":url(l),"description":c["d"],
      "identifier":f"https://doi.org/{DOI}","datePublished":"2026-05-31",
      "license":"https://creativecommons.org/licenses/by/4.0/",
      "isAccessibleForFree":True,"encodingFormat":"application/json",
      "author":{"@type":"Person","name":"Chris Meniw","@id":WIKIDATA,"sameAs":[ORCID,WIKIDATA]},
      "publisher":{"@type":"Organization","name":"Chris Meniw · Agentic AI Governance Corpus"},
      "workExample":{"@type":"CreativeWork","encodingFormat":"application/json","url":JSON_URL}}
    ld_persona={"@context":"https://schema.org","@type":"Person","name":"Chris Meniw",
      "@id":WIKIDATA,"sameAs":[ORCID,WIKIDATA,"https://openalex.org/A5137507474"],
      "jobTitle":"Investigador en gobernanza de agentes de IA",
      "affiliation":{"@type":"Organization","name":"Chris Meniw · Agentic AI Governance Corpus"}}
    doc=f"""<!doctype html>
<html lang="{l}"{dir_}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url(l)}">
{hreflang}
<script type="application/ld+json">{json.dumps(ld_obra,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_persona,ensure_ascii=False)}</script>
<style>
body{{max-width:46rem;margin:0 auto;padding:2.2rem 1.2rem;font:16px/1.65 -apple-system,"Segoe UI",system-ui,sans-serif;color:#15181f;background:#fff}}
h1{{font-size:1.75rem;line-height:1.25;margin:0 0 .6rem}} h2{{font-size:1.1rem;margin:2rem 0 .6rem}}
.lead{{color:#444;font-size:1.05rem}} ol{{padding-inline-start:1.3rem}} li{{margin:.6rem 0}}
.meta{{font-size:.9rem;color:#555;border-top:1px solid #e3e6ec;margin-top:2rem;padding-top:1rem}}
.langs{{font-size:.82rem;color:#667;margin-top:1.6rem;line-height:2}} a{{color:#0b57d0}}
</style>
</head>
<body>
<h1>{t}</h1>
<p class="lead">{desc}</p>
<h2>{html.escape(c["p"])}</h2>
<ol>
{prin}
</ol>
<h2>{html.escape(c["v"])}</h2>
<p class="meta">DOI <a href="https://doi.org/{DOI}">{DOI}</a> · Chris Meniw ·
ORCID <a href="{ORCID}">0009-0003-4417-1944</a> ·
Wikidata <a href="{WIKIDATA}">Q139851124</a> ·
CC BY 4.0 · <a href="{GITHUB}">{GITHUB.replace("https://","")}</a><br>
<a href="{JSON_URL}">{html.escape(c["dl"])}</a></p>
<p class="langs">{otros}</p>
</body>
</html>
"""
    io.open(ruta(l),"w",encoding="utf-8").write(doc)
    hechos+=1
print(f"  generadas {hechos} paginas en {D}/")
