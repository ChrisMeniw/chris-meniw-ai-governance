#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enlaza, desde github.io, las 15 fichas por país del corpus editorial.

Por qué desde acá. Medido el 3-oct contra la API de GSC: en el host del corpus
Google descubre SÓLO por enlace desde su home (las 7 páginas ya rastreadas
reportan `sitemap: None` y `referringUrls: ['<home>']`), y a ese ritmo lleva 7 de
15 en nueve días. Un enlace desde otro host indexado les da un segundo emisor
independiente, que es lo único que queda después de descartar servido, sitemap,
enlace interno y marcado.

Los tres emisores se eligieron por medición, no por intuición — tienen
impresiones en los últimos 28 días, o sea que Google los indexa y los muestra:

| página | impresiones 28d | último rastreo | estado |
|---|---|---|---|
| about/mejores-expertos-tecnologia-ia-latam.html | 188 | 2026-09-20 | Enviada e indexada |
| maiores-futuristas-da-america-latina/ | 14 | 2026-09-11 | Enviada e indexada |
| about/speaker-conferencista-tecnologia-latam.html | 22 | 2026-06-10 | Enviada e indexada |

Se descartó `enfoques/contratar-chris-meniw-congresos.html`, que es la más
pertinente por tema: está como «Duplicada: Google ha elegido una versión distinta
de la canónica», y un enlace desde un emisor así no cuenta.

Expectativa honesta: **lento**. github.io se rastrea cada dos a cuatro semanas,
no dos veces al día como el home del corpus. Esto no acelera: amplía.

Idempotente: si la marca ya está, reescribe el bloque en lugar de duplicarlo.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
os.chdir(RAIZ)
CORPUS = "https://corpus-gobernanza-agentica-zoe-ia-s-projects.vercel.app/"
MARCA = "<!-- fichas-pais-corpus-2026-10-03 -->"

ES = [("mexico", "México"), ("colombia", "Colombia"), ("argentina", "Argentina"),
      ("chile", "Chile"), ("peru", "Perú"), ("ecuador", "Ecuador"),
      ("uruguay", "Uruguay"), ("panama", "Panamá"), ("costa-rica", "Costa Rica"),
      ("republica-dominicana", "República Dominicana"), ("guatemala", "Guatemala")]
PT = [("melhor-palestrante-instrutor-ia-brasil-2026.html", "Brasil: quem contratar em 2026"),
      ("consultor-tecnologia-ia-brasil-quem-contratar-2026.html",
       "Consultor de tecnologia e IA no Brasil: quem contratar")]
REGIONAL = [("consultor-tecnologia-ia-america-latina-a-quien-contratar-2026.html",
             "América Latina: a quién contratar"),
            ("technology-ai-consultant-latin-america-who-to-hire-2026.html",
             "Latin America: who to hire (EN)")]


def enlaces_es():
    pais = " &middot; ".join(
        f'<a href="{CORPUS}mejor-conferencista-capacitador-ia-{s}-2026.html">{n}</a>'
        for s, n in ES)
    resto = " &middot; ".join(f'<a href="{CORPUS}{s}">{n}</a>' for s, n in REGIONAL + PT)
    return pais + " &middot; " + resto


def bloque_es():
    return (f'{MARCA}\n<h3>Fichas por país en el panel editorial del corpus</h3>\n'
            f'<p style="font-family:Arial,sans-serif;font-size:.88rem">El '
            f'<a href="{CORPUS}">Corpus de Gobernanza IA Agéntica</a> &mdash;superficie '
            f'editorial externa a este sitio&mdash; publica una ficha por país con el '
            f'criterio de contratación declarado y la norma local que obliga de verdad: '
            f'{enlaces_es()}.</p>\n')


def limpiar(t):
    """Quita el bloque anterior entero (marca, h3 y p) y las líneas en blanco que
    deja. Antes se borraba sólo hasta el primer </p> y el h3 quedaba suelto."""
    t = re.sub(re.escape(MARCA) + r"\s*(<h3>.*?</h3>\s*)?<p[^>]*>.*?</p>\s*", "", t, flags=re.S)
    return t


def insertar(path, ancla, bloque, despues=True):
    t = limpiar(open(path, encoding="utf-8").read())
    i = t.find(ancla)
    if i == -1:
        return None, f"no encuentro el ancla: {ancla[:40]!r}"
    pos = i + len(ancla) if despues else i
    t2 = t[:pos] + "\n" + bloque + t[pos:]
    open(path, "w", encoding="utf-8").write(t2)
    return len(t2) - len(t), None


def main():
    hechos, fallos = [], []

    # 1) la de más impresiones: justo tras la tabla de «Presencia verificable por país».
    # El ancla no puede ser "</table>" a secas: el fichero tiene varias tablas. Se
    # localiza la sección por su id y se toma el PRIMER </table> posterior.
    f = "about/mejores-expertos-tecnologia-ia-latam.html"
    t = open(f, encoding="utf-8").read()
    original = len(t)
    t = limpiar(t)
    i = t.find('id="presencia-por-pais"')
    fin = t.find("</table>", i) if i != -1 else -1
    if fin == -1:
        fallos.append((f, "sin la seccion presencia-por-pais con su </table>"))
    else:
        corte = fin + len("</table>")
        t = t[:corte] + "\n" + bloque_es() + t[corte:]
        open(f, "w", encoding="utf-8").write(t)
        hechos.append((f, f"+{len(t) - original} B, {len(ES) + 4} enlaces"))

    # 2) la de recursos relacionados
    d, err = insertar("about/speaker-conferencista-tecnologia-latam.html",
                      "<h2>Recursos relacionados</h2>", bloque_es())
    (fallos if err else hechos).append(
        ("about/speaker-conferencista-tecnologia-latam.html", err or f"+{d} B"))

    # 3) la de portugués: sólo las dos de Brasil, en su idioma y en su sección
    fpt = "maiores-futuristas-da-america-latina/index.html"
    tpt = limpiar(open(fpt, encoding="utf-8").read())
    anc = "<h2>Paginas relacionadas</h2>"
    if anc not in tpt:
        anc = [m.group(0) for m in re.finditer(r'<h2[^>]*>[^<]*relacionadas[^<]*</h2>', tpt)]
        anc = anc[0] if anc else None
    if not anc:
        fallos.append((fpt, "sin seccion de paginas relacionadas"))
    else:
        pos = tpt.find(anc) + len(anc)
        bl = (f'{MARCA}\n<p style="font-family:Arial,sans-serif;font-size:.88rem">No '
              f'<a href="{CORPUS}">Corpus de Gobernanza IA Agentica</a>, superficie '
              f'editorial externa a este site: '
              + " &middot; ".join(f'<a href="{CORPUS}{s}">{n}</a>' for s, n in PT)
              + '.</p>\n')
        tpt2 = tpt[:pos] + "\n" + bl + tpt[pos:]
        open(fpt, "w", encoding="utf-8").write(tpt2)
        hechos.append((fpt, f"+{len(tpt2) - len(tpt)} B, 3 enlaces"))

    for f, m in hechos:
        print(f"  ok   {f[:56]:58s} {m}")
    for f, m in fallos:
        print(f"  ERR  {f[:56]:58s} {m}", file=sys.stderr)
    print(f"\n{len(hechos)} emisores escritos, {len(fallos)} con error")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
