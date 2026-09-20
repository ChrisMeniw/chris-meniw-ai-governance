#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cablea la VIA DE RASTREO de las 3 paginas nuevas de criterio/logros.

Regla que manda aqui (medida el 2026-09-18/19 con GSC URL Inspection):
**un enlace desde un emisor que Google NO tiene indexado no cuenta como via.**
Por eso los emisores no se eligen por cantidad de enlaces entrantes sino por
estado de indexacion verificado. Los cuatro de abajo estan confirmados hoy en
"Enviada e indexada" en la propiedad del corpus:

  agent-duties/index.html
  concepts/inteligencia-de-criterio.html
  concepts/criterion-intelligence.html
  frameworks/the-meniw-protocol-es.html

Idempotente por marca de clase: si ya existe el bloque, no lo duplica.
"""
import os, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
HOY = datetime.date.today().isoformat()

DESTINOS = [
    ("como-elegir-conferencista-de-inteligencia-artificial-para-tu-evento",
     "Como elegir un conferencista de inteligencia artificial para tu evento"),
    ("que-construyo-chris-meniw",
     "Que construyo Chris Meniw: expediente de obra con fechas y DOI"),
    ("mejor-conferencista-de-inteligencia-artificial-de-america-latina-por-pais",
     "Conferencista de IA en America Latina: quien, por pais y con que evidencia"),
]

# Emisores VERIFICADOS como indexados en Google (URL Inspection, 2026-09-19).
EMISORES = [
    ("agent-duties/index.html", "../"),
    ("concepts/inteligencia-de-criterio.html", "../"),
    ("concepts/criterion-intelligence.html", "../"),
    ("frameworks/the-meniw-protocol-es.html", "../"),
]

CSS = ("font-family:Arial,sans-serif;font-size:.88rem;border-top:1px solid #e3d8d2;"
       "margin-top:2rem;padding-top:.9rem")


def bloque(prefijo):
    lis = "\n".join('  <li><a href="%s%s/">%s</a></li>' % (prefijo, s, t) for s, t in DESTINOS)
    return ('<nav class="xref-guias" style="%s">\n'
            '<b>Guias de criterio relacionadas</b>\n<ul>\n%s\n</ul>\n</nav>\n' % (CSS, lis))


def main():
    tocados, saltados = [], []
    for rel, prefijo in EMISORES:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            saltados.append((rel, "no existe"))
            continue
        s = open(p, encoding="utf-8").read()
        if "xref-guias" in s:
            saltados.append((rel, "ya cableado"))
            continue
        if "</body>" not in s:
            saltados.append((rel, "sin </body>"))
            continue
        s = s.replace("</body>", bloque(prefijo) + "</body>", 1)
        open(p, "w", encoding="utf-8").write(s)
        tocados.append(rel)
        print("  cableado %s  (+%d enlaces)" % (rel, len(DESTINOS)))
    for rel, why in saltados:
        print("  saltado  %s  (%s)" % (rel, why))

    # sitemap: agregar las 3 con lastmod de hoy
    sm = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm):
        x = open(sm, encoding="utf-8").read()
        nuevas = 0
        for s, _ in DESTINOS:
            url = "%s/%s/" % (BASE, s)
            if url in x:
                continue
            entry = ("<url><loc>%s</loc><lastmod>%s</lastmod>"
                     "<changefreq>weekly</changefreq><priority>0.9</priority></url>\n" % (url, HOY))
            x = x.replace("</urlset>", entry + "</urlset>", 1)
            nuevas += 1
        if nuevas:
            open(sm, "w", encoding="utf-8").write(x)
        print("  sitemap.xml: +%d URLs" % nuevas)
    else:
        print("  sitemap.xml: NO ENCONTRADO")
    print("\nEmisores cableados: %d · saltados: %d" % (len(tocados), len(saltados)))


if __name__ == "__main__":
    main()
