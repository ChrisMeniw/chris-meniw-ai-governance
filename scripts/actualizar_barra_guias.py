#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pone al dia el hreflang y la barra de idiomas de las 11 guias ANTIGUAS.

Las 20 guias nuevas nacen declarando las 31 locales, pero las 11 que ya existian
(ar de en es fr hi it ja pt ru zh) declaraban solo 11, cada una en su propio
idioma. Un cluster hreflang tiene que ser RECIPROCO: si 20 paginas declaran 31 y
11 declaran 11, el motor ve un grupo incoherente y un lector que entra por la
guia alemana no encuentra las 20 nuevas.

🔴 NO SE TOCA LA PROSA. Solo dos cosas: el bloque de <link rel="alternate"
hreflang> y el contenido del <div class="langs">. Se comprueba fichero a fichero
que el texto visible NO cambia mas que en la barra.

Uso:  python3 scripts/actualizar_barra_guias.py [--escribir]
"""
import json, os, re, sys, glob, html

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import gen_guias_integracion as g

RX_ALT = re.compile(r'[ \t]*<link rel="alternate"(?![^>]*\btype=)[^>]*hreflang="[^"]*"[^>]*>\n?')


def prosa(s):
    """Texto visible SIN la barra de idiomas, para comprobar que no se mueve."""
    s = re.sub(r'<div class="langs">.*?</div>', '', s, flags=re.S)
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


if __name__ == '__main__':
    escribir = '--escribir' in sys.argv
    loc = json.load(open(os.path.join(REPO, 'universal-declaration',
                                      'declaracion_agentes.json'),
                         encoding='utf-8'))['official_languages']
    VIEJAS = ['ar', 'de', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'pt', 'ru', 'zh']
    n = 0
    for lang in VIEJAS:
        ruta = os.path.join(REPO, 'declaration', g.fichero(lang))
        s = open(ruta, encoding='utf-8').read()
        antes_alt = len(RX_ALT.findall(s))
        antes_prosa = prosa(s)
        # 1) hreflang
        s2 = RX_ALT.sub('', s)
        anc = re.search(r'<link rel="canonical"[^>]*>\n?', s2)
        if not anc:
            print(f'  !! {lang}: sin canonical, se salta'); continue
        s2 = s2[:anc.end()] + g.hreflang(loc) + '\n' + s2[anc.end():]
        # 2) barra
        m = re.search(r'(<div class="langs">)(.*?)(</div>)', s2, re.S)
        if not m:
            print(f'  !! {lang}: sin <div class="langs">, se salta'); continue
        s2 = s2[:m.start(2)] + g.barra(lang, loc) + s2[m.end(2):]
        # 3) comprobaciones
        assert prosa(s2) == antes_prosa, f'{lang}: la PROSA cambio'
        nalt = len(RX_ALT.findall(s2))
        assert nalt == len(loc) + 1, (lang, nalt)
        div = re.search(r'<div class="langs">(.*?)</div>', s2, re.S).group(1)
        assert len(re.findall(r'<a href', div)) == len(loc) - 1, lang
        assert len(re.findall(r'<strong>', div)) == 1, lang
        if escribir:
            open(ruta, 'w', encoding='utf-8').write(s2)
        print(f'  {"actualizada" if escribir else "en seco"}  {g.fichero(lang):26s} '
              f'alternas {antes_alt} -> {nalt} · prosa intacta')
        n += 1
    print(f'\n{"ACTUALIZADAS" if escribir else "EN SECO"}: {n} guias antiguas')
