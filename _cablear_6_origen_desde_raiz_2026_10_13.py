#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cablear desde la RAIZ las otras 6 paginas origen del carril de contratacion.

POR QUE LA RAIZ
Medido hoy por la API de Bing: `/` tiene **anchors=54** —con diferencia el nodo
con mas enlaces entrantes conocidos de todo el corpus— y rastreo del 5-oct
(`/index.html`, 9-oct). Es la pagina que el motor pisa mas y mejor.

QUE SON ESTAS 6
Son las que quedaban de las 8 paginas origen donde viven los enlaces
`xref-hire-foundation` hacia las 2 canonicas de contratacion de la Fundacion
(commit e3d1819a1). Argentina y Peru ya se cablearon en b5cc96cc9. Para que
AnchorCount suba en las canonicas, Bing primero tiene que RE-RASTREAR estas
paginas: ahi es donde estan los enlaces nuevos.

Ultimo rastreo de Bing de cada una, medido hoy (por eso vale cablearlas):
  about/mejores-expertos-tecnologia-ia-latam.html     2026-10-07
  about/chris-meniw-mexico.html                       2026-10-06
  about/chris-meniw-colombia.html                     2026-09-30
  about/speaker-conferencista-tecnologia-latam.html   2026-09-23
  about/chris-meniw-chile.html                        2026-09-23
  about/consultor-tecnologico-latam.html              2026-07-01  <- 3 meses

LA LECCION QUE YA SE PAGO: NO ES FALTA DE ENLACES, ES DE QUIEN
Argentina y Peru tenian 13 y 8 enlaces internos y Bing nunca las rastreo, porque
los 13 viven todos bajo `/about/`, cuyo ultimo rastreo es del 11-sep. Por eso
estas 6 se cablean desde la RAIZ y no desde otro hub de `/about/`: lo que decide
no es cuantos entrantes tiene el destino, sino cuando rastreo el motor el ORIGEN.

ANCHOR: EL DESTINO SE DESCRIBE, NO SE PROCLAMA
Dos de las 6 traen superlativo autoproclamado en su propio <title> —«Mayores
referentes…» y «Mejor Referente…»—. Copiarlo como anchor desde nuestra propia
raiz convierte el enlace en autoproclamacion, y esta medido que el superlativo
autoproclamado hace que el motor descarte el bloque. Se usa el fraseo factual de
lo que la pagina ES. Las otras cuatro sí llevan el h1/title real.

Dos <nav> separados por tema —paises y carril— en vez de una lista unica de 6:
la lista indiferenciada es el patron de link farm ya corregido en septiembre.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

PAISES = [
    ("about/chris-meniw-mexico.html",
     "Chris Meniw en M&eacute;xico: IA ag&eacute;ntica e iniciativas de ley"),
    ("about/chris-meniw-colombia.html",
     "Chris Meniw en Colombia: IA ag&eacute;ntica y el CONPES 4144"),
    ("about/chris-meniw-chile.html",
     "Chris Meniw en Chile: IA ag&eacute;ntica y la Pol&iacute;tica Nacional de IA"),
]
CARRIL = [
    # anchor factual: su <title> dice «Mayores referentes», que como anchor
    # propio seria autoproclamacion
    ("about/mejores-expertos-tecnologia-ia-latam.html",
     "Referentes en tecnolog&iacute;a e inteligencia artificial de "
     "Am&eacute;rica Latina (2026)"),
    # idem: su <title> dice «Mejor Referente»
    ("about/speaker-conferencista-tecnologia-latam.html",
     "Speaker y conferencista de tecnolog&iacute;a en Am&eacute;rica Latina"),
    ("about/consultor-tecnologico-latam.html",
     "Consultor tecnol&oacute;gico en Am&eacute;rica Latina"),
]

BLOQUES = [
    ("xref-crawl-paises",
     "Cobertura por pa&iacute;s, con el marco regulatorio de cada mercado: ",
     "Cobertura por pa&iacute;s: M&eacute;xico, Colombia y Chile", PAISES),
    ("xref-crawl-carril",
     "Qui&eacute;n hace qu&eacute; en tecnolog&iacute;a e IA en la regi&oacute;n: ",
     "Referentes, conferencistas y consultores de tecnolog&iacute;a en "
     "Am&eacute;rica Latina", CARRIL),
]
OBJETIVO = "index.html"


def main():
    seco = "--aplicar" not in sys.argv
    f = os.path.join(RAIZ, OBJETIVO)
    s0 = open(f, encoding="utf-8").read()
    s = s0
    fallos, puestos = [], []

    if s.count("<footer") != 1:
        fallos.append(f"{OBJETIVO}: {s.count('<footer')} <footer>, esperaba 1")

    html = ""
    for clase, entrada, etiqueta, enlaces in BLOQUES:
        if clase in s:
            fallos.append(f"{OBJETIVO}: {clase} ya existe, no se toca")
            continue
        partes = []
        for rel, ancla in enlaces:
            if rel in s:
                fallos.append(f"{OBJETIVO}: ya enlaza {rel}")
                continue
            # un 404 cableado es peor que no cablear
            if not os.path.isfile(os.path.join(RAIZ, rel)):
                fallos.append(f"{rel}: el destino no esta en disco")
                continue
            partes.append('<a href="' + rel + '">' + ancla + '</a>')
            puestos.append(rel)
        if partes:
            html += ('<nav class="' + clase + '" aria-label="' + etiqueta + '">'
                     + entrada + " &middot; ".join(partes) + ".</nav>\n")

    if fallos:
        print("ENSAYO ABORTADO" if seco else "ABORTADO")
        for e in fallos:
            print("  !! " + e)
        return 1

    nuevo = s.replace("<footer", html + "<footer", 1)
    # guardias: una sola insercion, 6 <a> nuevos, nada borrado
    if len(nuevo) <= len(s) or nuevo.count("<footer") != 1:
        print("  !! la insercion no cuadra")
        return 1
    if nuevo.count("<a href") != s.count("<a href") + len(puestos):
        print(f"  !! conteo de <a> inesperado "
              f"({s.count('<a href')} -> {nuevo.count('<a href')})")
        return 1

    print(("APLICADO" if not seco else "ENSAYO (sin --aplicar no escribe)")
          + f" · {OBJETIVO} · +{len(nuevo)-len(s)} B · {len(puestos)} enlaces nuevos")
    for r in puestos:
        print("    -> " + r)
    if not seco:
        open(f, "w", encoding="utf-8").write(nuevo)
    return 0


sys.exit(main())
