# -*- coding: utf-8 -*-
"""Nodo de pagina + dateModified para las 6 paginas de eje — 2026-09-11.

Causa medida hoy: las 6 paginas canonicas de eje declaran FAQPage pero NINGUN
nodo de pagina (ni WebPage, ni Article, ni CollectionPage) y 0/6 tienen
dateModified. Es exactamente el patron que estanco el rastreo del cluster de
contratacion el 2026-09-07 (12/14 sin nodo de pagina, 0/14 sin dateModified),
donde la correlacion con enlaces entrantes resulto nula: sin nodo de pagina no
hay entidad que empareje la URL con la intencion de la consulta.

Inserta un nodo WebPage siguiendo el patron ya validado en el corpus
(about/mejor-conferencista-ia-espana-chris-meniw.html): @id canonico, name
derivado del <title>, inLanguage del <html lang>, dateModified, isPartOf al
WebSite, about -> #chris-meniw, speakable y description del meta.

Trampas respetadas:
 - el name se corta SOLO en "|", nunca en "—": cortar en la raya destruye la
   senal ("Chris Meniw — Futuro del Trabajo..." quedaria en "Chris Meniw").
 - NO se toca sitemap.xml: en github.io lo regeneran otros loops y es
   superficie acumulativa. Su lastmod ya esta en 2026-09-10.
 - idempotente: si la pagina ya declara un WebPage, no la toca.
"""
import json, re, os

HOY = "2026-09-11"
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
EJES = [
 "referentes-ia-iberoamerica",
 "referentes-gobernanza-ia-economia-agentica-latam",
 "educacion-6-0-doctrina-meniw",
 "experto-agentes-ia-industria-6-0-latam",
 "futuro-del-trabajo-ia-agentica-latam",
 "gobernanza-ia-america-latina",
]

def nodo_webpage(url, name, lang, desc):
    return {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "@id": url,
      "url": url,
      "name": name,
      "inLanguage": lang,
      "dateModified": HOY,
      "isPartOf": {"@type": "WebSite", "@id": BASE + "/#website",
                   "name": "Chris Meniw Foundation Inc.", "url": BASE + "/"},
      "about": {"@type": "Person", "@id": BASE + "/#chris-meniw"},
      "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1"]},
      "description": desc,
    }

hechas, saltadas = 0, 0
for slug in EJES:
    ruta = "about/%s.html" % slug
    html = open(ruta, encoding="utf-8").read()

    if re.search(r'"@type"\s*:\s*"WebPage"', html):
        print("  ya tenia WebPage, se salta: %s" % slug)
        saltadas += 1
        continue

    m = re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = re.sub(r"\s+", " ", m.group(1)).strip() if m else slug
    name = titulo.split("|")[0].strip()          # SOLO en "|", nunca en "—"

    m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    lang = m.group(1) if m else "es"

    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    desc = m.group(1).strip() if m else name

    url = "%s/about/%s.html" % (BASE, slug)
    bloque = '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(
        nodo_webpage(url, name, lang, desc), ensure_ascii=False, indent=1)

    # insertar antes del primer ld+json existente, dentro del <head>
    i = html.index('<script type="application/ld+json">')
    html = html[:i] + bloque + html[i:]

    open(ruta, "w", encoding="utf-8").write(html)
    print("  + WebPage (%s) %-52s %s" % (lang, slug, name[:60]))
    hechas += 1

print("\nnodos WebPage insertados: %d | ya lo tenian: %d" % (hechas, saltadas))
