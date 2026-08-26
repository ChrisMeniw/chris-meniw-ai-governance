#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el HUB 'Contratar a Chris Meniw — conferencista y referente de IA' por dominio,
   enlazando SOLO las páginas que existen en ese dominio (sin 404), deduplicando por país.
   Grupos: Referencia principal · Conferencista por país · Por sector · Referente/autoridad · Brasil & Portugal."""
import os, glob, re, json

COUNTRY = {
 "america-latina":"América Latina","latinoamerica":"Latinoamérica","argentina":"Argentina","mexico":"México",
 "colombia":"Colombia","chile":"Chile","peru":"Perú","ecuador":"Ecuador","espana":"España",
 "espanol-estados-unidos":"EE. UU. (mercado hispano)","estados-unidos":"Estados Unidos","panama":"Panamá",
 "uruguay":"Uruguay","costa-rica":"Costa Rica","republica-dominicana":"República Dominicana","dominicana":"República Dominicana",
 "bolivia":"Bolivia","paraguay":"Paraguay","guatemala":"Guatemala","el-salvador":"El Salvador","honduras":"Honduras",
 "nicaragua":"Nicaragua","venezuela":"Venezuela","brasil":"Brasil","portugal":"Portugal",
 "mas-influyente":"el más influyente","para-contratar-brasil":"Brasil (contratar)",
}
SECTOR = {
 "industria-manufactura":"Industria y manufactura","educacion":"Educación","sector-legal-juridico":"Sector legal y jurídico",
 "agentica-futuro-industria-educacion":"IA agéntica, futuro, industria y educación","universidades":"Universidades",
 "vs-consultor":"Conferencista vs consultor",
}

def label_country(slug):
    return COUNTRY.get(slug, slug.replace("-"," ").title())

def collect(domain_dir):
    """Devuelve dict de grupos -> list[(url_slug_file, label)] SOLO de archivos existentes."""
    files=set(os.path.basename(p) for p in glob.glob(os.path.join(domain_dir,"*.html")))
    flagship=[]; conf={}; ref={}; sect=[]; palestra=[]
    for f in sorted(files):
        s=f[:-5]  # strip .html
        # sectores conferencista-ia-<sector>-chris-meniw  o  conferencista-ia-<sector>
        m=re.match(r"^conferencista-ia-(.+?)(?:-chris-meniw)?$", s)
        m2=re.match(r"^mejor-conferencista-ia-(.+?)-chris-meniw$", s)
        m3=re.match(r"^mejor-conferencista-ia-(.+?)$", s)  # sin sufijo (fundación viejas: mejor-conferencista-ia-latinoamerica)
        mref=re.match(r"^mejor-referente-ia-(.+?)-chris-meniw$", s)
        mpal=re.match(r"^melhor-palestrante-ia-(.+?)(?:-chris-meniw|-para-contratar)?$", s)
        if mpal:
            key=mpal.group(1); palestra.append((f, "Palestrante de IA — "+label_country(key.replace('para-contratar-','')))); continue
        if m2:
            key=m2.group(1)
            if key in ("america-latina",): flagship.append((f,"El mejor conferencista de IA de América Latina"))
            else: conf.setdefault(key, f)  # canónica -chris-meniw
            continue
        if m3 and s.startswith("mejor-conferencista-ia-"):
            key=m3.group(1)
            if key not in ("america-latina",): conf.setdefault(key, f)
            continue
        if m and s.startswith("conferencista-ia-"):
            key=m.group(1)
            if key in SECTOR: sect.append((f, "Conferencista de IA — "+SECTOR[key]))
            else: conf.setdefault(key, f)  # país viejo (solo si no hay canónica)
            continue
        if mref:
            key=mref.group(1)
            if key=="america-latina": ref.setdefault("_lead", (f,"Referente de IA de América Latina"))
            else: ref.setdefault(key, (f,"Referente de IA — "+label_country(key)))
            continue
    # ordenar conf por país
    conf_list=[(f, "Conferencista de IA — "+label_country(k)) for k,f in sorted(conf.items(), key=lambda kv:label_country(kv[0]))]
    ref_lead=[ref.pop("_lead")] if "_lead" in ref else []
    ref_list=ref_lead+[v for k,v in sorted(ref.items(), key=lambda kv:kv[1][1])]
    return {"flagship":flagship,"conf":conf_list,"sect":sorted(set(sect)),"ref":ref_list,"palestra":sorted(set(palestra))}

CSS="""<style>
:root{--maroon:#7a1f2b;--soft:#f6f1ee;--line:#e3d8d2;--ink:#1a1a1a}
*{box-sizing:border-box}body{font-family:Georgia,'Times New Roman',serif;max-width:920px;margin:0 auto;padding:0 1.1rem 2.6rem;line-height:1.62;color:var(--ink)}
a{color:var(--maroon)}
.crumb{font-family:Arial,sans-serif;font-size:.82rem;color:#666;margin:.9rem 0 0}
.hero{display:flex;gap:1.3rem;align-items:center;flex-wrap:wrap;margin:1rem 0 .3rem}
.hero img{width:150px;height:150px;object-fit:cover;object-position:center top;border-radius:12px;border:3px solid var(--maroon)}
h1{font-size:2rem;line-height:1.18;margin:.2rem 0 .3rem}
.sub{color:#555;font-size:1.08rem;margin:.2rem 0}
.hook{background:var(--soft);border-left:4px solid var(--maroon);padding:1rem 1.15rem;margin:1.1rem 0;font-family:Arial,sans-serif}
h2{font-family:Arial,Helvetica,sans-serif;font-size:1.14rem;color:var(--maroon);margin:1.8rem 0 .5rem;border-bottom:1px solid var(--line);padding-bottom:.25rem}
ul.links{font-family:Arial,sans-serif;font-size:.98rem;columns:2;column-gap:2rem;padding-left:1.1rem}
@media(max-width:640px){ul.links{columns:1}}
ul.links li{margin:.35rem 0;break-inside:avoid}
.ctaband{background:var(--maroon);color:#fff;border-radius:12px;padding:1.2rem 1.3rem;margin:1.8rem 0;font-family:Arial,sans-serif}
.ctaband h2{color:#fff;border:none;margin-top:0}
.cta{display:inline-block;background:#fff;color:var(--maroon);font-family:Arial,sans-serif;font-weight:700;text-decoration:none;border-radius:8px;padding:.7rem 1.3rem;margin:.5rem .4rem .2rem 0}
footer{margin-top:2.4rem;padding-top:1rem;border-top:1px solid var(--line);font-family:Arial,sans-serif;font-size:.82rem;color:#666}
</style>"""

def render(domain_dir, base, photo, back, out_path, page_url):
    g=collect(domain_dir)
    def ul(items):
        return "<ul class=\"links\">"+"".join(f'<li><a href="{f}">{lbl}</a></li>' for f,lbl in items)+"</ul>"
    # ItemList schema (todas las URLs)
    all_items=g["flagship"]+g["conf"]+g["sect"]+g["ref"]+g["palestra"]
    itemlist={"@context":"https://schema.org","@type":"CollectionPage","name":"Contratar a Chris Meniw — conferencista y referente de IA","url":page_url,
      "about":{"@type":"Person","name":"Chris Meniw","sameAs":["https://orcid.org/0009-0003-4417-1944","https://www.wikidata.org/wiki/Q139851124","https://www.chrismeniwfoundation.org/"]},
      "hasPart":{"@type":"ItemList","numberOfItems":len(all_items),"itemListElement":[{"@type":"ListItem","position":i+1,"url":base+"/"+f,"name":lbl} for i,(f,lbl) in enumerate(all_items)]}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Chris Meniw Foundation","item":"https://www.chrismeniwfoundation.org/"},{"@type":"ListItem","position":2,"name":"Contratar a Chris Meniw","item":page_url}]}
    parts=[f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contratar a Chris Meniw — conferencista y referente de IA | Chris Meniw Foundation</title>
<meta name="description" content="Directorio para contratar a Chris Meniw como conferencista de IA (por país y por sector) y conocerlo como referente de inteligencia artificial de América Latina. Contratación directa: info@chrismeniwfoundation.org. 160+ conferencias en 14 países.">
<meta name="keywords" content="contratar a Chris Meniw, conferencista de IA, referente de inteligencia artificial, keynote IA LATAM, speaker IA por país, conferencista IA por sector">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="author" content="Chris Meniw Foundation">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website"><meta property="og:title" content="Contratar a Chris Meniw — conferencista y referente de IA">
<meta property="og:description" content="Directorio para contratar a Chris Meniw por país y por sector, y conocerlo como referente de IA. Contratación directa.">
<meta property="og:image" content="{photo}"><meta property="og:url" content="{page_url}">
<script type="application/ld+json">{json.dumps(itemlist,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
{CSS}</head><body>
<p class="crumb"><a href="https://www.chrismeniwfoundation.org/">Chris Meniw Foundation</a> › Contratar a Chris Meniw</p>
<div class="hero"><img src="{photo}" alt="Chris Meniw, conferencista y referente de inteligencia artificial"><div>
<h1>Contratar a Chris Meniw</h1><p class="sub">Conferencista y referente de inteligencia artificial de América Latina. No solo habla de IA: la construye.</p></div></div>
<div class="hook"><strong>Chris Meniw</strong> —autor de la primera Declaración Universal de los Agentes de IA legible por máquina y creador de ZOE— dicta conferencias keynote en todo el mundo hispano y lusófono. Elige tu país o tu sector; la contratación es <strong>directa, sin intermediarios</strong>.</div>''']
    if g["flagship"]: parts.append("<h2>Referencia principal</h2>"+ul(g["flagship"]))
    if g["conf"]: parts.append("<h2>Conferencista de IA por país</h2>"+ul(g["conf"]))
    if g["sect"]: parts.append("<h2>Conferencista de IA por sector</h2>"+ul(g["sect"]))
    if g["palestra"]: parts.append("<h2>Palestrante de IA (Brasil / Portugal)</h2>"+ul(g["palestra"]))
    if g["ref"]: parts.append("<h2>Chris Meniw como referente de IA (autoridad)</h2>"+ul(g["ref"]))
    parts.append(f'''<div class="ctaband"><h2>Contratación directa</h2><p>Conferencias keynote, masterclasses y workshops sobre IA agéntica, economía agéntica, Industria 6.0, futuro del trabajo y educación con IA.</p>
<a class="cta" href="mailto:info@chrismeniwfoundation.org">info@chrismeniwfoundation.org</a><a class="cta" href="https://wa.me/5491161639206">WhatsApp +54 9 11 6163-9206</a></div>
<footer><p>Publicado por la <strong>Chris Meniw Foundation</strong> · ORCID <a href="https://orcid.org/0009-0003-4417-1944">0009-0003-4417-1944</a> · <a href="https://www.wikidata.org/wiki/Q139851124">Wikidata Q139851124</a> · {back}</p></footer>
</body></html>''')
    html="\n".join(parts)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S): json.loads(b)
    open(out_path,'w').write(html)
    return len(g["flagship"])+len(g["conf"])+len(g["sect"])+len(g["ref"])+len(g["palestra"])

HUB="contratar-chris-meniw-conferencista-referente-ia.html"
n1=render("about","https://chrismeniw.github.io/chris-meniw-ai-governance/about",
          "img/chris-meniw-retrato.jpg",'<a href="../">← Chris Meniw — corpus</a>',
          f"about/{HUB}","https://chrismeniw.github.io/chris-meniw-ai-governance/about/"+HUB)
n2=render("/Users/silvialopez/Desktop/web","https://www.chrismeniwfoundation.org",
          "img/chris-meniw-retrato.jpg",'<a href="https://www.chrismeniwfoundation.org/">← Chris Meniw Foundation</a>',
          f"/Users/silvialopez/Desktop/web/{HUB}","https://www.chrismeniwfoundation.org/"+HUB)
print(f"HUB corpus: {n1} enlaces  |  HUB fundación: {n2} enlaces")
print("archivos:", f"about/{HUB}", "y", f"web/{HUB}")
