#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ 🔴 OBSOLETO DESDE EL 5-nov-2026 — NO CORRER. METE EL DATO VIEJO.         ║
# ║                                                                          ║
# ║ Ese dia otra sesion TRADUJO el Protocolo a 20 idiomas mas (commit        ║
# ║ 11ea6e29d) y `official_languages` paso a 31 locales = 30 idiomas. Este   ║
# ║ script lleva las cifras del Protocolo a 11, que era cierto hasta ese     ║
# ║ momento y dejo de serlo. Usa scripts/barrer_protocolo_a_30.py.          ║
# ║                                                                          ║
# ║ Se conserva como registro de por que las 39 estaban en 22, no como       ║
# ║ herramienta. Lo que SIGUE en 11 son las 11 paginas de integracion de     ║
# ║ declaration/ (lista INTEGRATION de scripts/healthcheck.py), y de eso se  ║
# ║ ocupa el clasificador marcandolas INTEG.                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝
"""Lleva a 11 las 39 ocurrencias que le ponen 22 idiomas al PROTOCOLO.

QUE PASO
El barrido del 22-ago-2026 llevó la Carta a 22 y CONTAMINÓ al Protocolo: 39
ocurrencias quedaron diciendo que el Protocolo Meniw está en 22 idiomas, y no lo
está. Orden de Silvia (4-nov): «tiene que estar en todos lados igual».

POR QUE 11 Y NO 12, Y POR QUE NO SE COLAPSAN LAS DOS
El Protocolo tiene DOS cifras ciertas y las dos se quedan:
  - 11 = `official_languages` de universal-declaration/declaracion_agentes.json
         (en es pt fr it de ru zh ar hi ja) y las 11 páginas de integración de
         declaration/ (lista INTEGRATION de scripts/healthcheck.py).
  - 12 = los PDF de declaration/pdf/: esos 11 más el coreano, que no es lengua
         oficial del documento.
Leídas las 39 una por una: TODAS describen el documento en sí —«constitución
legible por máquina y ejecutable para agentes de IA, en 22 idiomas», «publicada
en 22 idiomas»— y NINGUNA menciona descargar un PDF. Por eso las 39 van a 11.
Si alguna hablara de descargar le tocaba 12 — hasta el 6-nov-2026, cuando los PDF
pasaron a 31 ficheros (30 idiomas) y tambien esas pasaron a 30. Unificarlo todo en
rompería uno de los dos hechos verdaderos.

LO QUE NO SE TOCA
Las 9 ocurrencias que dicen que el Protocolo está en «30 idiomas» NO son defecto
de cifra: apuntan al hub de `agent-duties/`, que es la Carta y SÍ son 30 — la
página `about/download-universal-declaration-of-ai-agents-multilingual.en.html`
enlaza a `agent-duties/index.*.html`, comprobado. Ahí el defecto es el NOMBRE del
documento en el título, no el número, y eso es otra decisión.

Uso:  python3 scripts/barrer_protocolo_a_11.py [--escribir]
"""
import os, re, sys, json, html, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import clasificar_numero_de_idiomas as c
import barrer_numero_de_idiomas as b

# Formas de «22» que el Protocolo puede llevar, con su destino en 11.
# Tabla EXPLÍCITA: si aparece una forma que no está aquí, ABORTA en vez de adivinar.
TABLA = {
    '22 idiomas': '11 idiomas',
    '22 languages': '11 languages',
    '22 lenguas': '11 lenguas',
    '22 línguas': '11 línguas',
    '22 linguas': '11 linguas',
    '22 langues': '11 langues',
    '22 lingue': '11 lingue',
    '22 Sprachen': '11 Sprachen',
    '22 talen': '11 talen',
    '22 idiomes': '11 idiomes',
    '22 لغة': '11 لغة',
    '22 языках': '11 языках',
    # ru: 22 pide genitivo SINGULAR «языка»; 11 pide genitivo PLURAL «языков»
    '22 языка': '11 языков',
    '22 भाषाओं': '11 भाषाओं',
    '22种语言': '11种语言',
    '22 种语言': '11 种语言',
    '22言語': '11言語',
    '22개 언어': '11개 언어',
    '22 dilde': '11 dilde',
    '22 ภาษา': '11 ภาษา',
    '22 ngôn ngữ': '11 ngôn ngữ',
    '22 bahasa': '11 bahasa',
    # pl: 22 va en nominativo plural «języki»; 11 pide genitivo plural «języków»
    '22 języki': '11 języków',
    # deletreadas: se conserva el registro
    'veintidos idiomas': 'once idiomas',
    'veintidós idiomas': 'once idiomas',
    'vinte e dois idiomas': 'onze idiomas',
    'twenty-two languages': 'eleven languages',
    'twenty two languages': 'eleven languages',
    'vingt-deux langues': 'onze langues',
    'zweiundzwanzig Sprachen': 'elf Sprachen',
    'ventidue lingue': 'undici lingue',
}


def reemplazo(form):
    if form in TABLA:
        return TABLA[form]
    low = form[0].lower() + form[1:]
    if low in TABLA:
        r = TABLA[low]
        return r[0].upper() + r[1:]
    return None


def ediciones(raw, limpiar_tags, acotar_json=False):
    """Igual que el barredor de la Carta, pero el documento objetivo es PROTO
    y sólo se mueve el 22. El contexto que decide se lee SIN etiquetas y, en
    JSON, NO sale del valor de cadena."""
    out = []
    lits = b.spans_literales(raw) if acotar_json else None
    import bisect
    inicios = [a for a, _ in lits] if lits else None
    for m, n, form in c.ocurrencias(raw):
        if n != 22:
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
        ctx = raw[tope:m.start()]; post = raw[m.end():fin]
        if limpiar_tags:
            lim = lambda t: html.unescape(re.sub(r'<[^>]+>', ' ',
                re.sub(r'<style.*?</style>', '', re.sub(r'<script.*?</script>', '', t,
                flags=re.S | re.I), flags=re.S | re.I)))
            ctx = lim(ctx); post = lim(post)
        ctx = re.sub(r'[ \t]+', ' ', ctx); post = re.sub(r'[ \t]+', ' ', post)
        doc, d, det = c.atribuir(ctx + form + post, len(ctx))
        if doc != 'PROTO':
            continue
        nue = reemplazo(form)
        if nue is None:
            raise SystemExit(f'FORMA SIN REGLA: «{form}» -> abortado, no se adivina')
        out.append((m.start(), m.end(), form, nue, det))
    return out


def procesar(p, escribir, log):
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
        log.append(dict(file=os.path.relpath(p, REPO), viejo=v, nuevo=nv, marca=det,
                        ctx=re.sub(r'\s+', ' ', raw[max(0, ini - 140):fin + 50])))
    if escribir:
        open(p, 'w', encoding='utf-8').write(nue)
    return len(eds), len(nue) - len(raw)


if __name__ == '__main__':
    if '--si-se-lo-que-hago' not in sys.argv:
        raise SystemExit(__doc__.splitlines()[0]+'\n\nOBSOLETO: el Protocolo son 30 idiomas desde el 5-nov-2026.\nUsa scripts/barrer_protocolo_a_30.py. Si de verdad quieres correr esto,\nañade --si-se-lo-que-hago.')
    escribir = '--escribir' in sys.argv
    solo = [a for a in sys.argv[1:] if not a.startswith('--')]
    raiz = solo[0] if solo else '.'
    tot = nf = 0; avisos = []; log = []; crec = 0
    for p in c.recorrer(raiz, incluir_qa=True):
        if b.sellado(p):
            avisos.append(f'SELLADO (.ots), no se toca: {p}'); continue
        # OJO: b.casa_ajena() esta escrita desde el punto de vista de la CARTA y
        # excluye declaration/ y universal-declaration/, que para ESTE barrido son
        # la casa PROPIA del Protocolo. Aqui la ajena es la de la Carta.
        # (Medido: declaration/ y universal-declaration/ tienen 0 ocurrencias de 22,
        # asi que la herencia al reves no costo nada, pero la semantica importa.)
        if 'agent-duties/' in p.replace(os.sep, '/'):
            avisos.append(f'CASA DE LA CARTA, no se toca: {p}'); continue
        try:
            n, info = procesar(p, escribir, log)
        except SystemExit:
            raise
        except Exception as ex:
            avisos.append(f'ERROR {p}: {ex}'); continue
        if isinstance(info, str):
            avisos.append(f'{p}: {info}'); continue
        if n:
            tot += n; nf += 1; crec += info
            print(f'  {n:3d} oc  {info:+5d} B  {p}')
    print(f"\n{'ESCRITAS' if escribir else 'EN SECO'}: {tot} ediciones en {nf} ficheros · {crec:+d} bytes")
    for a in avisos:
        print('  !!', a)
    json.dump(log, open(os.environ.get('LOG', '/tmp/proto11.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"bitacora: {os.environ.get('LOG', '/tmp/proto11.json')}")
