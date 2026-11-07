#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lleva a 30 la cifra de los PDF DESCARGABLES del Protocolo Meniw (12 -> 30).

QUE CAMBIO, Y CUANDO
El 6-nov-2026 se tradujo el DOCUMENTO FORMAL de 7 paginas a los 19 idiomas que
faltaban y se imprimieron sus PDF. Medido en disco: declaration/pdf/ tiene 31
ficheros meniw-protocol-<locale>.pdf = 30 idiomas por el criterio ISO 639-1 de
data/language-counts.yml (zh + zh-Hant son la misma lengua en dos escrituras).
O sea que «el Protocolo se descarga en 12 idiomas» DEJO DE SER CIERTO ese dia.

ESTE BARREDOR ES EL COMPLEMENTO EXACTO DE barrer_protocolo_a_30.py
Aquel barrio las cifras del Protocolo a 30 pero EXCLUIA a proposito toda ocurrencia
con «PDF» o un verbo de descarga pegado a la cifra, porque entonces los PDF eran 12
y prometer 30 descargas habria sido falso (su RX_DESCARGA existe para eso, y esta
medido en siete idiomas no latinos). Ahora los PDF SON 31 locales, asi que esa
exclusion es justo lo que quedo mal. Este fichero toma SOLO lo que aquel dejaba:
misma maquinaria, discriminador INVERTIDO.
📐 Juntos cubren el total y ninguno puede dispararse dos veces sobre lo mismo: la
condicion de uno es la negacion de la del otro.

LAS TRES CIFRAS DEL PROTOCOLO YA COINCIDEN — y eso cierra el hueco
  30 = `official_languages` del JSON legible por maquina (31 locales). 5-nov-2026.
  30 = guias de integracion (31 locales; INTEGRATION de scripts/healthcheck.py
       tiene 31 entradas, medido hoy). 5-nov-2026.
  30 = los PDF de declaration/pdf/ (31 ficheros, medido hoy). 6-nov-2026. ESTE.
Un efecto util, el mismo que dejo escrito el barredor hermano: cuando dos cifras
coinciden, confundirlas ya no produce un numero falso. Ahora coinciden las TRES del
Protocolo y las de la Carta, de modo que el discriminador de descarga deja de tener
trabajo. Se conserva aqui invertido por si una de las tres vuelve a separarse.

LO QUE NO SE MUEVE, Y POR QUE
Hay OTROS doces en el arbol, y son correctos. Medidos el 6-nov:
  - «12 DOIs en Zenodo» / «12 Zenodo DOIs» / «12+ DOIs»: cuenta de DOIs, no de
    idiomas. El ancla de este barredor pide una PALABRA DE IDIOMA pegada a la
    cifra, asi que no los ve; aun asi van en FORMAS_AJENAS por si el clasificador
    cambia.
  - rss.xml «pubDate ... 12:00:00 GMT»: es una HORA. Misma razon.
  - manual de riesgos (12 idiomas): OTRO documento, cifra correcta. Lo descarta la
    atribucion del clasificador, que exige doc == PROTO.
📐 Por eso el barrido va por el ANCLA y no por la forma: «12 idiomas» suelto es
legitimo en el manual y falso en el hub de descarga. La misma cadena, dos verdades.

🔒 No toca ficheros con .ots al lado (b.sellado): re-sellarlos reiniciaria a hoy la
anterioridad anclada en Bitcoin.
🔴 Este fichero esta en SKIP_FILES del clasificador ANTES de su primera corrida:
lleva las formas como literales y seria candidato de su propio barrido.

Uso:  python3 scripts/barrer_pdf_protocolo_a_30.py [raiz] [--escribir]
"""
import os, re, sys, json, html

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import clasificar_numero_de_idiomas as c
import barrer_numero_de_idiomas as b
import barrer_protocolo_a_30 as p30

# Mismo RX_DESCARGA del barredor hermano, con sus siete idiomas no latinos medidos.
# Aqui se usa INVERTIDO: se exige que ACIERTE, no que falle.
RX_DESCARGA = p30.RX_DESCARGA

# Doces que NO son la cuenta de los PDF. Cada uno con su razon medida.
FORMAS_AJENAS = {
    '12 DOIs', '12+ DOIs', '12 Zenodo DOIs', '12 DOI',   # cuenta de DOIs
    '12:00', '12:00:00',                                  # hora en rss.xml
}
OBJETIVO = ('PROTO',)

# IDENTIFICADOR, no forma: el DOI y la URL propios del Protocolo.
# 🔴 Por que hace falta. 23 promesas repartidas en qa.jsonl, qa/qa-part-064.jsonl y
# .well-known/ai-answers-02.json viven en un literal que EMPIEZA en la cifra:
#   «Descarga gratis (CC BY 4.0) en 12 idiomas: .../descargar-protocolo-meniw.html
#    Autoria y precedencia verificables: DOI 10.5281/zenodo.20481373, sello en el
#    bloque #952266 de Bitcoin y ORCID 0009-0003-4417-1944.»
# Para una persona es inequivocamente el Protocolo. Pero el contexto se acota al
# literal -y se acota a proposito, para que no se cuele el registro VECINO-, asi que
# a la IZQUIERDA de la cifra no queda nada que nombre al documento y c.atribuir
# devuelve AMBIGUO. El barredor entonces NO lo toca, que es lo correcto: falla
# cerrado en vez de adivinar.
# La salida no es ensanchar la ventana -eso reintroduce la contaminacion entre
# registros- ni aflojar c.atribuir, que lo comparten todos los barredores. Es
# reconocer que un DOI es un IDENTIFICADOR: identifica el documento mejor que
# cualquier prosa, y esta DENTRO del literal, a la derecha de la cifra.
# 📐 Medido antes de aplicarlo: 33 literales traen el DOI/URL del Protocolo junto a
# un 12 de descarga, y CERO de ellos habla del manual de riesgos -que son 12 de
# verdad y es la confusion que habria costado caro-. La regla no puede cazarlo.
DOI_PROTO = '10.5281/zenodo.20481373'
URL_PROTO = 'descargar-protocolo-meniw.html'


def ediciones(raw, limpiar_tags, acotar_json=False):
    """Igual que p30.ediciones pero quedandose SOLO con las de descarga, y solo n==12."""
    out = []
    lits = b.spans_literales(raw) if acotar_json else None
    import bisect
    inicios = [a for a, _ in lits] if lits else None
    for m, n, form in c.ocurrencias(raw):
        if n != 12:
            continue
        if form in FORMAS_AJENAS:
            continue
        tope = max(0, m.start() - 1800)
        fin = min(len(raw), m.end() + 180)
        if lits is not None:
            i = bisect.bisect_right(inicios, m.start()) - 1
            if i < 0:
                continue
            a, z = lits[i]
            if not (a <= m.start() < z):
                continue
            tope = max(tope, a); fin = min(fin, z)
        # INVERTIDO: solo pasa si hay PDF/verbo de descarga pegado a la cifra.
        # Se mide sobre el crudo sin etiquetas: un <a> no debe separar
        # «Descargar» de la cifra.
        if not RX_DESCARGA.search(re.sub(r'<[^>]+>', ' ', raw[max(0, m.start() - 60):m.start()])):
            continue
        ctx = raw[tope:m.start()]; post = raw[m.end():fin]
        if limpiar_tags:
            lim = lambda t: html.unescape(re.sub(r'<[^>]+>', ' ',
                re.sub(r'<style.*?</style>', '', re.sub(r'<script.*?</script>', '', t,
                flags=re.S | re.I), flags=re.S | re.I)))
            ctx = lim(ctx); post = lim(post)
        ctx = re.sub(r'[ \t]+', ' ', ctx); post = re.sub(r'[ \t]+', ' ', post)
        doc, d, det = c.atribuir(ctx + form + post, len(ctx))
        if doc not in OBJETIVO:
            # Segunda via, SOLO por identificador y solo dentro del literal acotado:
            # ver la nota de DOI_PROTO. No se usa para rescatar un CARTA o un MANUAL
            # mal atribuido: exige el DOI o la URL del Protocolo, que son suyos.
            lit = raw[tope:fin] if lits is not None else ''
            if not (DOI_PROTO in lit or URL_PROTO in lit):
                continue
            det = 'IDENT:doi/url-protocolo'
            doc = 'PROTO'
        nue = b.reemplazo(form)
        if nue is None:
            raise SystemExit(f'FORMA SIN REGLA: «{form}» -> abortado, no se adivina')
        out.append((m.start(), m.end(), form, nue, f'{doc}|{det}'))
    return out


def procesar(p, escribir, log, repo):
    """Reusa las validaciones de p30: JSON parsea y conserva forma, JSON-LD vivo,
    .py compila, .jsonl mismo numero de lineas. No se reescriben aqui."""
    e = os.path.splitext(p)[1].lower()
    raw = open(p, encoding='utf-8').read()
    eds = ediciones(raw, e in ('.html', '.xml'), acotar_json=(e in ('.json', '.jsonl')))
    if not eds:
        return 0, None
    nue = b.aplicar(raw, eds)
    if e == '.json':
        try:
            x = json.loads(raw); y = json.loads(nue)
        except Exception as ex:
            return 0, f'ABORTA: JSON no parsea ({ex})'
        if b.forma(x) != b.forma(y):
            return 0, 'ABORTA: la forma estructural del JSON cambio'
    elif e == '.jsonl':
        la, lb = raw.splitlines(), nue.splitlines()
        if len(la) != len(lb):
            return 0, 'ABORTA: cambio el numero de lineas'
        for i, (x, y) in enumerate(zip(la, lb), 1):
            if x == y:
                continue
            try:
                jx = json.loads(x); jy = json.loads(y)
            except Exception as ex:
                return 0, f'ABORTA: linea {i} no parsea ({ex})'
            if b.forma(jx) != b.forma(jy):
                return 0, f'ABORTA: forma estructural distinta en linea {i}'
    elif e == '.html':
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', nue, re.S | re.I):
            try:
                json.loads(blk)
            except Exception as ex:
                return 0, f'ABORTA: JSON-LD roto ({ex})'
    elif e == '.py':
        import ast
        try:
            ast.parse(nue)
        except Exception as ex:
            return 0, f'ABORTA: Python no compila ({ex})'
    for ini, fin, v, nv, det in eds:
        log.append(dict(file=os.path.relpath(p, repo), viejo=v, nuevo=nv, marca=det,
                        ctx=re.sub(r'\s+', ' ', raw[max(0, ini - 150):fin + 50])))
    if escribir:
        open(p, 'w', encoding='utf-8').write(nue)
    return len(eds), len(nue) - len(raw)


if __name__ == '__main__':
    escribir = '--escribir' in sys.argv
    solo = [a for a in sys.argv[1:] if not a.startswith('--')]
    raiz = solo[0] if solo else '.'
    exc = set()
    if os.environ.get('EXCLUIR') and os.path.exists(os.environ['EXCLUIR']):
        exc = {l.strip() for l in open(os.environ['EXCLUIR']) if l.strip()}
    tot = nf = crec = 0; avisos = []; log = []
    for p in c.recorrer(raiz, incluir_qa=True):
        rel = os.path.relpath(p, raiz)
        if rel in exc or rel.endswith('data/language-counts.yml'):
            continue
        if b.sellado(p):
            avisos.append(f'SELLADO (.ots), no se toca: {rel}'); continue
        try:
            n, info = procesar(p, escribir, log, raiz)
        except SystemExit:
            raise
        except RecursionError:
            avisos.append(f'RECURSION en {rel} — mirar reemplazo()'); continue
        except Exception as ex:
            avisos.append(f'ERROR {rel}: {ex}'); continue
        if isinstance(info, str):
            avisos.append(f'{rel}: {info}'); continue
        if n:
            tot += n; nf += 1; crec += info
            print(f'  {n:4d} oc  {info:+6d} B  {rel}')
    print(f"\n{'ESCRITAS' if escribir else 'EN SECO'}: {tot} ediciones en {nf} ficheros · {crec:+d} bytes")
    for a in avisos:
        print('  !!', a)
    json.dump(log, open(os.environ.get('LOG', '/tmp/pdf30.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"bitacora: {os.environ.get('LOG', '/tmp/pdf30.json')}")
