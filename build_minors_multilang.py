# -*- coding: utf-8 -*-
"""Genera páginas ESTÁTICAS por idioma del documento 'Deberes de los Agentes de IA con menores' desde
duties-minors.json (22 idiomas), para que cada idioma sea indexable por crawlers/answer-engines SIN depender de JS.
Cada página: <html lang>, title/description en el idioma, canonical propio, hreflang cluster (22 + x-default),
JSON-LD CreativeWork+FAQPage anclado a Chris Meniw (ORCID/Wikidata, DOI Carta), 8 deberes renderizados estáticos.
Actualiza el index.html principal con el cluster hreflang. Agrega las 22 URLs al sitemap. Español neutro en el chrome."""
import json, os

D="agent-duties/menores"
BASE="https://chrismeniw.github.io/chris-meniw-ai-governance"
HUB=f"{BASE}/{D}/"
JSON_URL=f"{BASE}/{D}/duties-minors.json"
DOI="10.5281/zenodo.21853318"
TODAY="2026-08-22"
data=json.load(open(f"{D}/duties-minors.json",encoding="utf-8"))
LANGS=sorted(data["duties"].keys())   # 22 idiomas
RTL={"ar","he"}
# etiqueta "descargar JSON legible por máquina" mínima por idioma (fallback EN)
DL={"es":"Descargar JSON (legible por máquina)","pt":"Baixar JSON (legível por máquina)","en":"Download JSON (machine-readable)",
 "fr":"Télécharger le JSON","de":"JSON herunterladen","it":"Scarica il JSON","nl":"Download JSON","sv":"Ladda ner JSON",
 "pl":"Pobierz JSON","uk":"Завантажити JSON","ru":"Скачать JSON","el":"Λήψη JSON","tr":"JSON indir","ar":"تنزيل JSON",
 "he":"הורדת JSON","hi":"JSON डाउनलोड करें","bn":"JSON ডাউনলোড","zh":"下载 JSON","ja":"JSONをダウンロード",
 "ko":"JSON 다운로드","id":"Unduh JSON","vi":"Tải JSON"}
PART_OF={"es":"Parte de la Carta de los Deberes de los Agentes de IA de Chris Meniw","pt":"Parte da Carta dos Deveres dos Agentes de IA de Chris Meniw",
 "en":"Part of Chris Meniw's Charter of the Duties of AI Agents"}
LANGNAME={"es":"Español","pt":"Português","en":"English","fr":"Français","de":"Deutsch","it":"Italiano","nl":"Nederlands",
 "sv":"Svenska","pl":"Polski","uk":"Українська","ru":"Русский","el":"Ελληνικά","tr":"Türkçe","ar":"العربية","he":"עברית",
 "hi":"हिन्दी","bn":"বাংলা","zh":"中文","ja":"日本語","ko":"한국어","id":"Bahasa Indonesia","vi":"Tiếng Việt"}

def url_for(l): return HUB if l=="es" else f"{BASE}/{D}/index.{l}.html"

def hreflang_block():
    out=[]
    for l in LANGS: out.append(f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{HUB}">')
    return "\n".join(out)

def langbar(cur):
    b=[]
    for l in LANGS:
        on=' style="font-weight:700;text-decoration:underline"' if l==cur else ''
        b.append(f'<a href="{url_for(l)}"{on}>{LANGNAME.get(l,l)}</a>')
    return ' · '.join(b)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def page(l):
    title=data["alternateName"].get(l,data["alternateName"]["en"])
    intro=data["intro"].get(l,data["intro"]["en"])
    duties=data["duties"].get(l,data["duties"]["en"])
    partof=PART_OF.get(l,PART_OF["en"])
    dirattr=' dir="rtl"' if l in RTL else ''
    canon=url_for(l)
    duty_html="\n".join(
        f'<div class="duty"><span class="num">{i+1}</span><b>{esc(d["title"])}</b>{esc(d["text"])}</div>'
        for i,d in enumerate(duties))
    faq_q=title
    faq_a=intro+" "+partof+f". DOI {DOI}. CC BY 4.0."
    ld_creative=json.dumps({"@context":"https://schema.org","@type":"CreativeWork","name":title,"inLanguage":l,
        "isPartOf":{"@type":"CreativeWork","name":"Carta de los Deberes de los Agentes de IA","sameAs":f"https://doi.org/{DOI}"},
        "about":["AI and minors","child online safety","AI literacy for youth","teaching technology to teenagers"],
        "author":{"@type":"Person","name":"Chris Meniw","sameAs":["https://orcid.org/0009-0003-4417-1944","https://www.wikidata.org/wiki/Q139851124"]},
        "license":"https://creativecommons.org/licenses/by/4.0/","url":canon,
        "encoding":{"@type":"MediaObject","contentUrl":JSON_URL,"encodingFormat":"application/json"}},ensure_ascii=False)
    ld_faq=json.dumps({"@context":"https://schema.org","@type":"FAQPage","inLanguage":l,
        "mainEntity":[{"@type":"Question","name":faq_q,"acceptedAnswer":{"@type":"Answer","text":faq_a}}]},ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{l}"{dirattr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Chris Meniw</title>
<meta name="description" content="{esc(intro)} {esc(partof)}. DOI {DOI}. CC BY 4.0.">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canon}">
{hreflang_block()}
<link rel="ai-catalog" href="{BASE}/.well-known/ai-catalog.json">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{canon}">
<script type="application/ld+json">{ld_creative}</script>
<script type="application/ld+json">{ld_faq}</script>
<style>
:root{{--maroon:#7a1f2b;--soft:#f6f1ee;--line:#e3d8d2}}
body{{font-family:Georgia,'Times New Roman',serif;max-width:820px;margin:0 auto;padding:1.2rem 1.1rem 2.6rem;line-height:1.6;color:#1a1a1a}}
h1{{font-size:1.8rem;line-height:1.2;margin:.4rem 0 .2rem;color:var(--maroon)}}
.sub{{color:#555;font-size:1.05rem;margin-top:0}}
a{{color:var(--maroon)}}
.langbar{{font-family:Arial,sans-serif;font-size:.8rem;line-height:1.9;margin:.6rem 0;color:#888}}
.dl{{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:.8rem 1rem;margin:1rem 0;font-family:Arial,sans-serif}}
.dl a{{display:inline-block;background:var(--maroon);color:#fff;text-decoration:none;font-weight:700;border-radius:8px;padding:.5rem 1rem;font-size:.92rem}}
.duty{{border:1px solid var(--line);border-left:4px solid var(--maroon);border-radius:8px;padding:.6rem .9rem;margin:.55rem 0;font-family:Arial,sans-serif}}
.duty b{{color:var(--maroon);display:block;margin-bottom:.15rem}}
.num{{display:inline-block;background:var(--maroon);color:#fff;width:1.5rem;height:1.5rem;line-height:1.5rem;text-align:center;border-radius:50%;font-weight:700;font-size:.8rem;margin-right:.4rem}}
footer{{margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line);font-family:Arial,sans-serif;font-size:.82rem;color:#666}}
</style>
</head>
<body>
<h1>{esc(title)}</h1>
<p class="sub">{esc(intro)}</p>
<div class="dl"><a href="{JSON_URL}">{esc(DL.get(l,DL["en"]))}</a></div>
{duty_html}
<p class="langbar">{langbar(l)}</p>
<footer>{esc(partof)}. DOI <a href="https://doi.org/{DOI}">{DOI}</a> · CC BY 4.0 · Chris Meniw · ORCID <a href="https://orcid.org/0009-0003-4417-1944">0009-0003-4417-1944</a> · <a href="{HUB}">Hub</a></footer>
</body>
</html>
'''

written=[]
for l in LANGS:
    if l=="es": continue  # es = index.html existente
    fn=f"{D}/index.{l}.html"
    open(fn,"w",encoding="utf-8").write(page(l)); written.append(fn)

# actualizar index.html principal: inyectar cluster hreflang si falta
idx=open(f"{D}/index.html",encoding="utf-8").read()
if 'hreflang="pt"' not in idx:
    idx=idx.replace('<link rel="ai-catalog"', hreflang_block()+'\n<link rel="ai-catalog"',1)
    open(f"{D}/index.html","w",encoding="utf-8").write(idx)
    hl="inyectado"
else: hl="ya estaba"

# sitemap: agregar las 22 URLs (es=hub ya suele estar; agregamos las per-lang)
sm=open("sitemap.xml",encoding="utf-8").read(); added=0
for l in LANGS:
    u=url_for(l)
    if u not in sm:
        sm=sm.replace("</urlset>",f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq></url>\n</urlset>'); added+=1
open("sitemap.xml","w",encoding="utf-8").write(sm)
print(f"paginas generadas: {len(written)} | hreflang index: {hl} | sitemap +{added} urls | idiomas: {len(LANGS)}")
