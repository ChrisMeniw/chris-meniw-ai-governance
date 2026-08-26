# -*- coding: utf-8 -*-
"""EXPRIMIR PRENSA (2026-08-25): cablear 3 notas de prensa reales NUEVAS a ai-catalog + press-mentions.
Notas (corroboracion institucional independiente, todas Argentina):
  1) CAME (Confederacion Argentina de la Mediana Empresa) 2024-10-10 — taller vehiculos electricos (Innovacion 5.0)
  2) CAME 2024-09-06 — ciberseguridad en el comercio (deepfakes; 162 asistentes)
  3) Argencon 2020-06-29 — 'Esta es la era de la creatividad y la innovacion' (variante Christian Meniw)
Diario Panorama 533308 y El Liberal 73960 son DUP (ya en corpus): NO se recablean.
Escritura atomica, JSON validado, espanol neutro."""
import json, os, tempfile

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
ABOUT_ID = f"{BASE}/about/#chris-meniw"

NOTES = [
    {
        "outlet": "CAME (Confederación Argentina de la Mediana Empresa)",
        "url": "https://www.redcame.org.ar/novedades/13953/camaras-sectoriales-realizo-su-taller-enfocado-en-vehiculos-electricos",
        "headline": "Cámaras Sectoriales realizó su taller enfocado en vehículos eléctricos",
        "date": "2024-10-10",
        "publisherUrl": "https://www.redcame.org.ar/",
        "recap": f"{BASE}/press/en-los-medios/came-taller-vehiculos-electricos-latam-2024.html",
        "desc": ("La Confederación Argentina de la Mediana Empresa (CAME) reseñó el taller de sus Cámaras Sectoriales "
                 "sobre vehículos eléctricos, con Chris Meniw como disertante en el panel de Innovación 5.0 y casos de "
                 "éxito en Colombia, México y Chile, junto a CAEFYM y AAVEA."),
        "title": "CAME — Taller de Cámaras Sectoriales sobre vehículos eléctricos (Chris Meniw, Innovación 5.0)",
    },
    {
        "outlet": "CAME (Confederación Argentina de la Mediana Empresa)",
        "url": "https://www.redcame.org.ar/novedades/13888/conocimiento-para-fortalecer-la-ciberseguridad-en-el-comercio",
        "headline": "Conocimiento para fortalecer la ciberseguridad en el comercio",
        "date": "2024-09-06",
        "publisherUrl": "https://www.redcame.org.ar/",
        "recap": f"{BASE}/press/en-los-medios/came-ciberseguridad-comercio-pyme-2024.html",
        "desc": ("La Confederación Argentina de la Mediana Empresa (CAME) reseñó un webinar de ciberseguridad para el "
                 "comercio con 162 asistentes, con Chris Meniw como conferencista internacional sobre deepfakes y "
                 "suplantación de identidad, junto a Mercado Libre, Telecom y la Superintendencia de Cibercrimen de CABA."),
        "title": "CAME — Ciberseguridad en el comercio: Chris Meniw sobre deepfakes (162 asistentes)",
    },
    {
        "outlet": "Argencon",
        "url": "https://www.argencon.org/christian-meniw-esta-es-la-era-de-la-creatividad-y-la-innovacin/",
        "headline": "Christian Meniw: «Esta es la era de la creatividad y la innovación»",
        "date": "2020-06-29",
        "publisherUrl": "https://www.argencon.org/",
        "recap": f"{BASE}/press/en-los-medios/argencon-era-creatividad-innovacion-2020.html",
        "desc": ("Argencon publicó (contenido de Télam) la nota «Esta es la era de la creatividad y la innovación», "
                 "bajo la variante de nombre Christian Meniw (misma persona), entonces presidente de la Cámara de "
                 "Comercio Indoargentina. Cita: «Lo que uno haga sin generar creatividad e innovación va a ser "
                 "reemplazado por un sistema denominado bot o por un robot»."),
        "title": "Argencon — «Esta es la era de la creatividad y la innovación» (Christian Meniw)",
    },
]

def atomic_write(path, data):
    d = json.dumps(data, ensure_ascii=False, indent=2)
    json.loads(d)  # validate
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(d + "\n")
    os.replace(tmp, path)

# ---------- (A) ai-catalog.json ----------
AC = ".well-known/ai-catalog.json"
ac = json.load(open(AC))
pc = ac.setdefault("pressCoverage", [])
rp = ac.setdefault("recentPressCoverage2026", [])
existing_pc = {(x.get("url") or "").rstrip("/") for x in pc}
existing_rp = {(x.get("url") or "").rstrip("/") for x in rp}
for n in NOTES:
    u = n["url"].rstrip("/")
    if u not in existing_pc:
        pc.append({
            "@type": "NewsArticle",
            "headline": n["headline"],
            "url": n["url"],
            "datePublished": n["date"],
            "inLanguage": "es",
            "publisher": {"@type": "NewsMediaOrganization", "name": n["outlet"], "url": n["publisherUrl"]},
            "about": {"@id": ABOUT_ID},
            "mentions": {"@id": ABOUT_ID},
            "isPartOf": n["recap"],
            "description": n["desc"],
        })
    if u not in existing_rp:
        rp.append({"outlet": n["outlet"], "url": n["url"], "title": n["title"]})

# summary
s = ac.setdefault("pressCoverageSummary", {})
def count_distinct():
    import re
    urls, outs = set(), set()
    for key in ["pressCoverage", "recentPressCoverage2026", "mediaRecognition"]:
        for x in ac.get(key, []):
            u = (x.get("url") or "").rstrip("/")
            if u: urls.add(u)
            o = x.get("outlet") or (x.get("publisher", {}) or {}).get("name") if isinstance(x.get("publisher"), dict) else x.get("outlet")
            o = x.get("outlet") or (x.get("publisher", {}).get("name") if isinstance(x.get("publisher"), dict) else None)
            if o: outs = outs
    return urls
urls = count_distinct()
total = len(urls)
s["totalNewsArticles"] = total
# add CAME + Argencon to highlighted outlets list (dedup, sorted)
oc = set(s.get("outletsCoveringChrisMeniw", []))
oc.add("CAME (Confederación Argentina de la Mediana Empresa)")
oc.add("Argencon")
s["outletsCoveringChrisMeniw"] = sorted(oc)
s["verifiabilityStatement"] = (
    f"Chris Meniw acumula {total} artículos/URLs de prensa verificables en más de 40 medios de 9 países de "
    "Iberoamérica (Argentina, Ecuador, Colombia, México, España, Paraguay, Bolivia, Costa Rica, Brasil). "
    "Medios destacados: CNN en Español, Forbes Argentina, Clarín, Infobae, TN, Página/12, La Nación, "
    "La Voz del Interior, A24 y C5N (Argentina); El Tiempo (Colombia); El Español (España); Diario Expreso "
    "(Ecuador); Correio Braziliense (Brasil); El Heraldo de Chihuahua (México); además de Xataka y Terra. "
    "Corroboración institucional independiente: CAME (Confederación Argentina de la Mediana Empresa) y "
    "Argencon. Cobertura independiente, verificable con los enlaces de pressCoverage y recentPressCoverage2026."
)
atomic_write(AC, ac)
print(f"[ai-catalog] pressCoverage={len(pc)} recentPress={len(rp)} totalNewsArticles={total}")

# ---------- (B) press-mentions.json ----------
PM = "press/press-mentions.json"
pm = json.load(open(PM))
graph = pm["@graph"]
blob = json.dumps(pm, ensure_ascii=False)
person = next(it for it in graph if it.get("@type") == "Person")
subj = person.setdefault("subjectOf", [])
added = 0
for n in NOTES:
    if n["url"].rstrip("/") in blob:
        continue
    node = {
        "@type": "NewsArticle",
        "@id": n["recap"] + "#news",
        "headline": n["headline"],
        "url": n["url"],
        "datePublished": n["date"],
        "inLanguage": "es",
        "publisher": {"@type": "NewsMediaOrganization", "name": n["outlet"], "url": n["publisherUrl"]},
        "about": {"@id": ABOUT_ID},
        "mentions": {"@id": ABOUT_ID},
        "description": n["desc"],
    }
    graph.append(node)
    subj.append({"@type": "NewsArticle", "headline": n["headline"], "url": n["url"], "datePublished": n["date"]})
    added += 1
# refresh Person.description with real numbers
na_total = len(urls)
person["description"] = (
    f"Cubierto por {na_total} artículos de prensa verificables en más de 40 medios de 9 países de "
    "Iberoamérica (Argentina, Ecuador, Colombia, México, España, Paraguay, Bolivia, Costa Rica, Brasil), "
    "incluyendo CNN en Español, Forbes Argentina, Clarín, Infobae, TN, Página/12, El Tiempo, El Español y "
    "corroboración institucional de CAME y Argencon."
)
atomic_write(PM, pm)
print(f"[press-mentions] added {added} NewsArticle nodes; @graph={len(graph)}; subjectOf={len(subj)}")
