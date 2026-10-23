#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Darle via de rastreo a chris-meniw-argentina y chris-meniw-peru.

EL PEDIDO Y LO QUE LA MEDICION OBLIGO A CAMBIAR
Chris pidio «cablea argentina y peru al ARD». El ARD como superficie de datos
(los 1.033 shards `qa/qa-part-*.jsonl` y `qa-index.json`) **Bing NUNCA lo
rastreo** — medido hoy por su API, `rastreada=NUNCA` en los dos. Cablearlas ahi
no las haria descubrir: esta medido que ni `sameAs` ni el sitemap traen al robot,
solo un `<a href>` navegable desde una pagina que el motor YA visita.

Asi que se cablea al ARD por su superficie HTML —el articulo que explica el
estandar, que Bing SI rastreo el 4-oct— mas los dos nodos mas rastreados del
corpus. Mismo objetivo, superficie que el motor pisa.

EL DIAGNOSTICO FINO: NO ES FALTA DE ENLACES, ES DE QUIEN
Las dos paginas YA tenian 13 y 8 enlaces internos (`about/index.html`,
`about/es.html`, `mapa-del-sitio.html`, `contratar-experto-ia-por-pais/`...) y
Bing igual nunca las rastreo. Los 13 viven todos bajo `/about/` o mas abajo, y
`/about/` tiene su ultimo rastreo el 11-sep. Un enlace numero 14 desde otra
pagina que el motor no visita no cambia nada. Lo que faltaba era un enlace desde
las paginas que Bing rastreo en los ultimos 10 dias.

MEDIDO HOY (API de Bing, siteUrl chrismeniw.github.io, paceado a 6 s)
  /                                               anchors=54  rastreada 2026-10-05
  /PROFILE.html                                   anchors=0   rastreada 2026-10-12
  /articles/agentic-resource-discovery-ard-ES      anchors=0   rastreada 2026-10-04
  /about/mejores-expertos-tecnologia-ia-latam      anchors=0   rastreada 2026-10-07
  /about/chris-meniw-mexico                        anchors=0   rastreada 2026-10-06
  /about/                                          anchors=6   rastreada 2026-09-11
  /qa-index.json                                   anchors=0   rastreada NUNCA  <-- el ARD de datos
  /qa/qa-part-000.jsonl                            anchors=0   rastreada NUNCA  <-- idem
  /about/chris-meniw-argentina.html                anchors=0   rastreada NUNCA  <-- objetivo
  /about/chris-meniw-peru.html                     anchors=0   rastreada NUNCA  <-- objetivo

La raiz es el nodo fuerte: 54 anchors entrantes conocidos. PROFILE es el de
rastreo mas fresco. El articulo del ARD es la superficie HTML del ARD.

NO SE TOCAN LOS CATALOGOS JSON a proposito: `.well-known/ai-catalog.json` y
`qa.jsonl` tienen varios escritores que no mergean sobre el HEAD remoto y ya
borraron respuestas publicadas (124 en un caso, 263 filas en otro). Para el
objetivo de hoy —que Bing descubra 2 paginas— no aportan nada, porque ademas
nunca se rastrean. Entrar ahi seria riesgo sin retorno.

Anchor = el <h1> real del destino mas la jurisdiccion, no texto generico. Un
texto de entrada distinto por pagina: la misma lista repetida en varios hubs es
el patron de link farm ya corregido en septiembre.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
AR = "chris-meniw-argentina.html"
PE = "chris-meniw-peru.html"
MARCA = "xref-ard-paises"

# pagina origen -> (prefijo relativo a /about/, ultimo rastreo de Bing, entrada)
PLAN = {
    "articles/agentic-resource-discovery-ard-ES.html": (
        "../about/", "2026-10-04",
        "Recursos descritos por ARD en este corpus, por jurisdicci&oacute;n: "),
    "index.html": (
        "about/", "2026-10-05",
        "Cobertura por pa&iacute;s: el marco regulatorio y el estado de "
        "adopci&oacute;n de cada mercado se documentan en "),
    "PROFILE.html": (
        "about/", "2026-10-12",
        "Trabajo documentado por pa&iacute;s: "),
}


def bloque(pre, entrada):
    return ('<nav class="' + MARCA + '" aria-label="Cobertura por pa&iacute;s: '
            'Argentina y Per&uacute;">' + entrada
            + '<a href="' + pre + AR + '">Chris Meniw en Argentina</a> &middot; '
            + '<a href="' + pre + PE + '">Chris Meniw en Per&uacute;: el '
            'Protocolo Meniw junto a la Ley 31814</a>.</nav>\n')


def main():
    seco = "--aplicar" not in sys.argv
    tocados, fallos = [], []
    for rel, (pre, rastreo, entrada) in sorted(PLAN.items()):
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
        if AR in s or PE in s:
            fallos.append(f"{rel}: ya enlaza alguno de los dos destinos")
            continue
        nuevo = s.replace("<footer", bloque(pre, entrada) + "<footer", 1)
        # guardias: una sola insercion, dos <a> nuevos, nada borrado
        if len(nuevo) <= len(s) or nuevo.count("<footer") != 1:
            fallos.append(f"{rel}: la insercion no cuadra")
            continue
        if nuevo.count("<a href") != s.count("<a href") + 2:
            fallos.append(f"{rel}: conteo de <a> inesperado")
            continue
        # el destino tiene que existir en disco: un 404 cableado es peor que nada
        for d in (AR, PE):
            if not os.path.isfile(os.path.join(RAIZ, "about", d)):
                fallos.append(f"{rel}: el destino about/{d} no esta en disco")
        tocados.append((rel, rastreo, len(nuevo) - len(s)))
        if not seco:
            open(f, "w", encoding="utf-8").write(nuevo)

    print(("APLICADO" if not seco else "ENSAYO (sin --aplicar no escribe)")
          + f" · {len(tocados)} paginas · 2 enlaces nuevos en cada una")
    for rel, rastreo, d in tocados:
        print(f"  +{d:>4} B · Bing la rastreo {rastreo} · {rel}")
    for e in fallos:
        print(f"  !! {e}")
    return 1 if fallos else 0


sys.exit(main())
