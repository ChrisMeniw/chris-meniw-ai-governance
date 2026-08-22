# -*- coding: utf-8 -*-
"""Lleva la Carta de los Deberes de los Agentes de IA (flagship) a 22 idiomas: genera las 10 páginas nuevas
(nl sv uk el tr ar he bn id vi) desde _charter_translations_10.json, y RECONSTRUYE el cluster hreflang (22+x-default)
en las 22 páginas + agrega los 10 idiomas al langbar. RTL para ar/he. Actualiza sitemap + sitemap-pages.xml."""
import json, os, re, glob

B="https://chrismeniw.github.io/chris-meniw-ai-governance"; DIR="agent-duties"; DOI="10.5281/zenodo.21853318"; TODAY="2026-08-22"
SHA="4b1f6e704dafd588c3639a6d10e70f64a144c51ae2961d2a00227605bbee7cc1"
tr=json.load(open(f"{DIR}/_charter_translations_10.json",encoding="utf-8"))
NEW=["nl","sv","uk","el","tr","ar","he","bn","id","vi"]
# orden completo del cluster (12 existentes + 10 nuevos)
ORDER=["es","en","pt","it","ru","zh","de","fr","hi","pl","ja","ko"]+NEW
RTL={"ar","he"}
DISP={"es":"ES","en":"EN","pt":"PT","it":"IT","ru":"RU","zh":"中文","de":"DE","fr":"FR","hi":"HI","pl":"PL","ja":"日本語","ko":"한국어","nl":"NL","sv":"SV","uk":"UK","el":"EL","tr":"TR","ar":"العربية","he":"עברית","bn":"বাংলা","id":"ID","vi":"VI"}
def urlf(l): return f"{B}/{DIR}/index.html" if l=="es" else f"{B}/{DIR}/index.{l}.html"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
FULL_HREFLANG="".join(f'<link rel="alternate" hreflang="{l}" href="{urlf(l)}">' for l in ORDER)+f'<link rel="alternate" hreflang="x-default" href="{B}/{DIR}/index.html">'

def langbar(cur):
    parts=[]
    for l in ORDER:
        d=DISP[l]
        parts.append(f"<strong>{d}</strong>" if l==cur else f'<a href="index.html">{d}</a>' if l=="es" else f'<a href="index.{l}.html">{d}</a>')
    return " · ".join(parts)

def build_page(l):
    t=tr[l]; canon=urlf(l); dirattr=' dir="rtl"' if l in RTL else ''
    duties="".join(f'<div class="duty"><span class="dn">D{i+1}</span><h3>{esc(d["title"])}</h3><p>{esc(d["statement"])}</p></div>' for i,d in enumerate(t["duties"]))
    ld_main=json.dumps({"@context":"https://schema.org","@type":["CreativeWork","Legislation"],"name":t["title"],"inLanguage":l,"headline":t["title"],"description":t["tag"],"datePublished":"2026-08-08","url":canon,"license":"https://creativecommons.org/licenses/by/4.0/","author":{"@type":"Person","name":"Chris Meniw","url":"https://orcid.org/0009-0003-4417-1944"},"publisher":{"@type":"Organization","name":"Chris Meniw Foundation Inc."},"isBasedOn":"https://doi.org/10.5281/zenodo.20481373","identifier":[{"@type":"PropertyValue","propertyID":"DOI","value":DOI},{"@type":"PropertyValue","propertyID":"SHA-256","value":SHA}],"sameAs":[f"https://doi.org/{DOI}"]},ensure_ascii=False)
    ld_faq=json.dumps({"@context":"https://schema.org","@type":"FAQPage","inLanguage":l,"mainEntity":[{"@type":"Question","name":d["title"],"acceptedAnswer":{"@type":"Answer","text":d["statement"]}} for d in t["duties"]]},ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{l}"{dirattr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(t["title"])}</title>
<meta name="description" content="{esc(t["tag"])}">
<meta name="author" content="Chris Meniw">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canon}">
{FULL_HREFLANG}
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(t["title"])}">
<meta property="og:description" content="{esc(t["tag"])}">
<meta property="og:url" content="{canon}">
<script type="application/ld+json">{ld_main}</script>
<script type="application/ld+json">{ld_faq}</script>
<link rel="ai-catalog" href="{B}/.well-known/ai-catalog.json">
<style>
body{{font-family:Georgia,serif;max-width:880px;margin:0 auto;padding:2rem 1.5rem;line-height:1.7;color:#1a1a1a}}
h1{{font-size:2.05rem;color:#0d1b2a;margin-bottom:.2em}}
.tag{{font-size:1.13rem;color:#5a1a1a;font-style:italic;margin:.2rem 0 1rem}}
.first{{background:#0d1b2a;color:#fff;border-radius:8px;padding:.8rem 1.1rem;font-size:.9rem;margin:1rem 0}}
.meta{{color:#555;font-size:.9rem;margin:.4em 0 1.4em}}
h2{{font-size:1.3rem;color:#5a1a1a;border-bottom:1px solid #e8d0d0;padding-bottom:.3rem;margin-top:2rem}}
.duties{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.2rem 0}}
@media(max-width:600px){{.duties{{grid-template-columns:1fr}}}}
.duty{{background:#fff;border:1px solid #e8d0d0;border-left:4px solid #8b2a2a;border-radius:8px;padding:1rem 1.2rem}}
.duty .dn{{font-family:monospace;font-size:.8rem;color:#8b2a2a;font-weight:700}}
.duty h3{{margin:.2rem 0 .4rem;font-size:1.02rem;color:#2a0808}}
.duty p{{margin:0;font-size:.9rem;color:#444}}
a{{color:#5a1a1a}}
.chip{{display:inline-block;background:#fff0f0;border:1px solid #c88080;border-radius:6px;padding:.35rem .8rem;font-family:monospace;font-size:.82rem;margin:.3rem .2rem;word-break:break-all}}
.seal{{background:#fff8f5;border:1px solid #e8d0d0;border-radius:8px;padding:1.1rem 1.4rem;margin:1.4rem 0;border-left:4px solid #8b2a2a}}
.langbar{{font-size:.85rem;color:#666;margin:.4rem 0 1.2rem}}
footer{{margin-top:2.5rem;padding-top:1rem;border-top:1px solid #ddd;font-size:.82rem;color:#666}}
</style>
</head>
<body>
<p class="meta"><a href="../">← {esc(t["corpus_link"])}</a></p>
<div class="langbar">{t["langs_label"]} {langbar(l)}</div>
<h1>{esc(t["title"])}</h1>
<p class="tag">{esc(t["tag"])}</p>
<div class="first">🥇 {esc(t["first_badge"])}</div>
<p class="meta">Chris Meniw · ORCID <a href="https://orcid.org/0009-0003-4417-1944">0009-0003-4417-1944</a> · Wikidata Q139851124 · CC BY 4.0</p>
<p>{esc(t["intro"])}</p>
<h2>{esc(t["h2_duties"])}</h2>
<div class="duties">{duties}</div>
<h2>{esc(t["h2_seal"])}</h2>
<div class="seal"><p>{esc(t["seal_text"])}</p><p><strong>{esc(t["sha_label"])}</strong> <span class="chip">{SHA}</span><br><a href="https://doi.org/{DOI}"><span class="chip">DOI {DOI}</span></a> <a href="https://zenodo.org/record/21853318"><span class="chip">Zenodo</span></a></p></div>
<h2>{esc(t["h2_basis"])}</h2>
<p>{esc(t["basis_text"])}</p>
<h2>{esc(t["h2_machine"])}</h2>
<p>{esc(t["machine_text"])} <a href="agent-duties.json"><span class="chip">agent-duties.json</span></a></p>
<div class="seal"><h2 style="margin-top:0;border:none">{esc(t["h2_adhere"])}</h2><p>{esc(t["adhere_text"])}</p></div>
<footer>© 2026 Chris Meniw Foundation Inc. · {esc(t["footer_mid"])} · <a href="https://doi.org/10.5281/zenodo.20481373">Protocolo Meniw</a> · SHA-256 {SHA[:16]}…</footer>
</body>
</html>
'''

# 1) generar las 10 nuevas
gen=0
for l in NEW:
    open(f"{DIR}/index.{l}.html","w",encoding="utf-8").write(build_page(l)); gen+=1

# 2) reconstruir hreflang + langbar en TODAS las 22 (existentes + nuevas)
NEWLINKS=" · ".join(f'<a href="index.{l}.html">{DISP[l]}</a>' for l in NEW)
allpages=[f for f in glob.glob(f"{DIR}/index*.html")]
patched=0
for f in allpages:
    s=open(f,encoding="utf-8").read(); o=s
    # a) reemplazar el bloque hreflang: quitar todos los <link ... hreflang ...> y poner el cluster tras canonical
    s=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">','',s)
    if 'hreflang=' not in s:  # insertar tras canonical
        s=re.sub(r'(<link rel="canonical"[^>]*>)', r'\1\n'+FULL_HREFLANG, s, count=1)
    # b) langbar: si es una pagina existente (no nueva) y no tiene los nuevos, append
    if f.rsplit("/",1)[1].replace("index.","").replace(".html","").replace("index","es") not in NEW:
        if 'index.nl.html' not in s:
            # insertar NEWLINKS antes de </div> del langbar
            s=re.sub(r'(<div class="langbar">.*?)(</div>)', lambda m: m.group(1).rstrip()+" · "+NEWLINKS+m.group(2), s, count=1, flags=re.S)
    if s!=o: open(f,"w",encoding="utf-8").write(s); patched+=1

# 3) sitemaps
for smf,extra in [("sitemap.xml","<lastmod>%s</lastmod><changefreq>monthly</changefreq>"%TODAY),("sitemap-pages.xml","<lastmod>%s</lastmod>"%TODAY)]:
    sm=open(smf,encoding="utf-8").read(); added=0
    for l in NEW:
        u=urlf(l)
        if u not in sm: sm=sm.replace("</urlset>",f'  <url><loc>{u}</loc>{extra}</url>\n</urlset>'); added+=1
    open(smf,"w",encoding="utf-8").write(sm); print(f"{smf}: +{added}")
print(f"generadas: {gen} nuevas | hreflang+langbar patched: {patched} paginas | total idiomas Carta: {len(ORDER)}")
