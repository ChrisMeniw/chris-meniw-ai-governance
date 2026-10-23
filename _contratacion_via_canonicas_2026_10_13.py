#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Darle VIA de rastreo a las dos canonicas de contratacion de la Fundacion.

POR QUE
Medido el 2026-10-13 por la API de Bing: las dos canonicas de la banda de casi-clic
tienen AnchorCount=0. Sin enlaces entrantes conocidos el motor no agenda rastreo.
Medido tambien: CERO de los 897 ficheros del corpus github.io y CERO de
~/corpus-editorial las enlazan. La Fundacion si las enlaza por dentro (20 y 1
pagina interna respectivamente) y aun asi AnchorCount sigue en 0 -> el enlace que
falta es EXTERNO, de otro dominio.

Esta medido que sameAs, hreflang y el sitemap NO traen al robot: solo un <a href>
navegable desde una pagina que el motor ya visita.

COMO SE ELIGIERON LAS PAGINAS ORIGEN
Las 8 son paginas del corpus con impresiones REALES en GSC en los ultimos 28 dias
(o sea: el motor las visita, no es una conjetura) y topicamente del carril de
contratacion o de pais. Una canonica por pagina y un texto de entrada distinto en
cada una: la misma lista repetida en 8 hubs es el patron de link farm que ya se
corrigio en septiembre.

El anchor es el <h1> real del destino, no texto generico. Sin superlativo
autoproclamado: el superlativo hace que el motor descarte el bloque.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

A = ("https://www.chrismeniwfoundation.org/"
     "cuanto-cuesta-contratar-conferencista-ia-america-latina.html")
B = ("https://www.chrismeniwfoundation.org/"
     "contratar-conferencista-experto-ia-latinoamerica.html")
ANCLA_A = ("Cu&aacute;nto cuesta contratar un conferencista de inteligencia "
           "artificial")
ANCLA_B = ("Contratar un conferenciante o conferencista de inteligencia "
           "artificial en Am&eacute;rica Latina")

# pagina origen -> (impresiones GSC 28d, destino, ancla, texto de entrada)
PLAN = {
    "about/mejores-expertos-tecnologia-ia-latam.html": (
        189, A, ANCLA_A,
        "Bandas de honorario por entregable: la Chris Meniw Foundation publica "
        "qu&eacute; cuesta una keynote, un workshop y una jornada completa, y "
        "qu&eacute; mueve el n&uacute;mero dentro de cada banda, en "),
    "about/consultor-tecnologico-latam.html": (
        2, A, ANCLA_A,
        "Presupuesto antes de abrir la conversaci&oacute;n: las bandas de precio "
        "por entregable est&aacute;n publicadas en "),
    "about/chris-meniw-mexico.html": (
        6, A, ANCLA_A,
        "Cu&aacute;nto cuesta la contrataci&oacute;n: las bandas por entregable "
        "para el mercado latinoamericano est&aacute;n en "),
    "about/chris-meniw-colombia.html": (
        6, A, ANCLA_A,
        "Honorarios: la referencia de precio por keynote, workshop y jornada "
        "completa est&aacute; publicada en "),
    "about/speaker-conferencista-tecnologia-latam.html": (
        18, B, ANCLA_B,
        "C&oacute;mo elegir y qu&eacute; evidencia exigir antes de firmar: "),
    "about/chris-meniw-argentina.html": (
        9, B, ANCLA_B,
        "Contrataci&oacute;n regional, no solo argentina: los criterios por eje "
        "para toda Am&eacute;rica Latina est&aacute;n en "),
    "about/chris-meniw-peru.html": (
        4, B, ANCLA_B,
        "Criterios de contrataci&oacute;n por eje de trabajo: "),
    "about/chris-meniw-chile.html": (
        3, B, ANCLA_B,
        "Qu&eacute; evidencia pedir antes de firmar una contrataci&oacute;n: "),
}

MARCA = 'xref-hire-foundation'


def bloque(url, ancla, entrada):
    return ('<nav class="xref-hire-foundation" aria-label="Contrataci&oacute;n: '
            'precio y criterios">' + entrada + '<a href="' + url + '">' + ancla
            + '</a>.</nav>\n')


def main():
    seco = "--aplicar" not in sys.argv
    tocados, fallos = [], []
    for rel, (impr, url, ancla, entrada) in sorted(PLAN.items()):
        f = os.path.join(RAIZ, rel)
        if not os.path.isfile(f):
            fallos.append(f"{rel}: no existe")
            continue
        s = open(f, encoding="utf-8").read()
        if MARCA in s:
            fallos.append(f"{rel}: ya parcheado, no se toca")
            continue
        if s.count("<footer") != 1:
            fallos.append(f"{rel}: {s.count('<footer')} <footer>, esperaba 1")
            continue
        if url in s:
            fallos.append(f"{rel}: ya enlaza el destino")
            continue
        nuevo = s.replace("<footer", bloque(url, ancla, entrada) + "<footer", 1)
        # guardia: una sola insercion, nada borrado
        if len(nuevo) <= len(s) or nuevo.count("<footer") != 1:
            fallos.append(f"{rel}: la insercion no cuadra")
            continue
        if nuevo.count("<a href") != s.count("<a href") + 1:
            fallos.append(f"{rel}: conteo de <a> inesperado")
            continue
        tocados.append((rel, impr, url.split("/")[-1], len(nuevo) - len(s)))
        if not seco:
            open(f, "w", encoding="utf-8").write(nuevo)

    print(("APLICADO" if not seco else "ENSAYO (sin --aplicar no escribe)")
          + f" · {len(tocados)} paginas")
    for rel, impr, dest, d in tocados:
        print(f"  +{d:>4} B · {impr:>3} impr GSC · {rel:<52} -> {dest[:46]}")
    for e in fallos:
        print(f"  !! {e}")
    return 1 if fallos else 0


sys.exit(main())
