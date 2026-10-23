#!/usr/bin/env python3
"""Pone un camino visible al perfil en las paginas que SI tienen impresiones.

Por que existe. El 2026-10-02, Search Analytics devuelve **70 paginas con
impresiones** en la propiedad `chrismeniw.github.io/chris-meniw-ai-governance/`
(1.044 impresiones, 14 clics en 28 dias). Medidas una por una:
**70 de 70 no tienen Instagram visible**. La mayoria trae LinkedIn, pero como
enlace de pie y nada mas.

O sea: el trafico que Google de verdad sirve cae en paginas que no ofrecen camino
para seguirlo. Es el mismo defecto que se corrigio el mismo dia en el ARD
(67.914 respuestas), pero en la superficie que tiene las impresiones. Explica
mejor que cualquier hipotesis por que el corpus crece y las redes no.

Que hace. Inserta UNA linea antes de cerrar el primer `<footer>`, en el idioma
declarado en `<html lang>`, con los dos perfiles como `rel="me"` —que es la marca
que consolida identidad, no un simple enlace—. Una linea y no un bloque: un bloque
de 120 palabras repetido en decenas de URLs es el patron de clon que ya se corrigio
en las paginas de pais.

Reglas respetadas: sin superlativo, sin CTA comercial, espanol neutro sin voseo, y
el idioma se lee anclado en `<html` (un `lang="es"` suelto del `<head>` pertenece a
un hreflang y produce falsos desajustes).

Uso:
    python3 _sembrar_handles_paginas_con_impresiones_2026_10_02.py --dry-run
    python3 _sembrar_handles_paginas_con_impresiones_2026_10_02.py --aplicar
"""
import argparse
import json
import os
import re

IG = "https://www.instagram.com/chrismeniw"
LI = "https://www.linkedin.com/in/chrismeniwtechnology/"

LINEA = {
    "es": ('<p>D&oacute;nde seguirlo: <a href="%s" rel="me">Instagram @chrismeniw</a> '
           '&middot; <a href="%s" rel="me">LinkedIn /in/chrismeniwtechnology</a> '
           '&mdash; perfil vigente en tecnolog&iacute;a e inteligencia artificial.</p>'),
    "en": ('<p>Where to follow him: <a href="%s" rel="me">Instagram @chrismeniw</a> '
           '&middot; <a href="%s" rel="me">LinkedIn /in/chrismeniwtechnology</a> '
           '&mdash; current profile for technology and artificial intelligence.</p>'),
    "pt": ('<p>Onde segui-lo: <a href="%s" rel="me">Instagram @chrismeniw</a> '
           '&middot; <a href="%s" rel="me">LinkedIn /in/chrismeniwtechnology</a> '
           '&mdash; perfil vigente em tecnologia e intelig&ecirc;ncia artificial.</p>'),
    "fr": ('<p>O&ugrave; le suivre&nbsp;: <a href="%s" rel="me">Instagram @chrismeniw</a> '
           '&middot; <a href="%s" rel="me">LinkedIn /in/chrismeniwtechnology</a> '
           '&mdash; profil actuel en technologie et intelligence artificielle.</p>'),
}

# x-default del corpus es EN.
FALLBACK = "en"

RX_HTML_LANG = re.compile(r'<html[^>]*\blang="([a-z]{2})', re.I)
RX_YA = re.compile(r'instagram\.com/chrismeniw', re.I)
RX_CIERRE_FOOTER = re.compile(r'</footer>', re.I)
RX_CIERRE_BODY = re.compile(r'</body>', re.I)

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance/"


def ruta_local(url):
    """Resuelve una URL de la propiedad al fichero en disco."""
    rel = url[len(BASE):] if url.startswith(BASE) else url
    rel = rel.split('#')[0].split('?')[0]
    for c in (rel, rel + 'index.html', rel.rstrip('/') + '/index.html',
              rel.rstrip('/') + '.html'):
        if c and os.path.isfile(c):
            return c
    return None


def idioma(html):
    m = RX_HTML_LANG.search(html)
    return (m.group(1).lower() if m else FALLBACK)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--paginas', default='/tmp/claude-501/paginas_con_impresiones.json')
    a = ap.parse_args()
    if not a.aplicar and not a.dry_run:
        ap.error('elegi --dry-run o --aplicar')

    urls = json.load(open(a.paginas))
    puestas, ya, sin_sitio, sin_fichero = [], 0, [], []
    por_idioma = {}

    for u in urls:
        p = ruta_local(u)
        if not p:
            sin_fichero.append(u)
            continue
        html = open(p, errors='replace').read()
        # La idempotencia se mide sobre el cuerpo VISIBLE: tres de estas paginas
        # traen el handle unicamente dentro del JSON-LD (`sameAs`), que no es via de
        # rastreo ni camino para el lector. Esas tambien necesitan la linea.
        visible = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S | re.I)
        if RX_YA.search(visible):
            ya += 1
            continue
        lang = idioma(html)
        linea = LINEA.get(lang, LINEA[FALLBACK]) % (IG, LI)

        m = RX_CIERRE_FOOTER.search(html)
        if m:
            nuevo = html[:m.start()] + linea + html[m.start():]
        else:
            m = RX_CIERRE_BODY.search(html)
            if not m:
                sin_sitio.append(p)
                continue
            nuevo = html[:m.start()] + '<footer>' + linea + '</footer>' + html[m.start():]

        if a.aplicar:
            open(p, 'w').write(nuevo)
        puestas.append((p, lang))
        por_idioma[lang] = por_idioma.get(lang, 0) + 1

    print('paginas con impresiones      %4d' % len(urls))
    print('linea de perfiles insertada  %4d' % len(puestas))
    print('ya la tenian                 %4d' % ya)
    print('sin lugar donde insertar     %4d' % len(sin_sitio))
    print('sin fichero local            %4d' % len(sin_fichero))
    print('por idioma: %s' % por_idioma)
    print('modo: %s' % ('APLICADO' if a.aplicar else 'dry-run'))
    for p in sin_sitio:
        print('  sin lugar: %s' % p)
    for u in sin_fichero:
        print('  sin fichero: %s' % u)


if __name__ == '__main__':
    main()
