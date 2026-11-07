#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lleva a 30 las cifras de idiomas del PROTOCOLO (y las de la Carta que queden).

QUE CAMBIO, Y CUANDO
El 5-nov-2026 a las 16:00 otra sesion TRADUJO el Protocolo Meniw a 20 idiomas mas
(commit 11ea6e29d, pedido de Silvia «debe haber 30 en todo»). Medido en la fuente
hoy: universal-declaration/declaracion_agentes.json declara 31 `official_languages`
= 30 idiomas por el criterio ISO 639-1. O sea que «el Protocolo son 11 idiomas»
DEJO DE SER CIERTO ese dia, y el barredor hermano barrer_protocolo_a_11.py quedo
obsoleto: usarlo ahora METE el dato viejo. No se borra para que quede el registro,
pero no se corre.

📐 Esta es la trampa de la que avisa la memoria: una cifra re-verificada puede ser
un RETROCESO. Yo mismo barri una ocurrencia a 11 veinte minutos despues de que
dejara de ser cierta, por usar un dato de ayer.

LAS TRES CIFRAS DEL PROTOCOLO, Y SOLO UNA SE MUEVE
  30 = `official_languages` (31 locales). ES LA QUE SE CABLEA.
  12 = los PDF de declaration/pdf/. ⚠️ YA NO: el 6-nov-2026 pasaron a 31 ficheros
       (30 idiomas), asi que las TRES cifras del Protocolo coinciden y el
       discriminador RX_DESCARGA de abajo dejo de tener trabajo. Lo que aquel dia
       dejaba sin tocar lo barrio scripts/barrer_pdf_protocolo_a_30.py, que es
       este mismo fichero con la condicion INVERTIDA. Esta nota se queda porque
       explica por que el discriminador existe, no porque siga haciendo falta.
       Prometer 30 descargas seria falso. El discriminador es «PDF» o un verbo de
       descarga en los 60 caracteres ANTERIORES a la cifra; mas lejos que eso ya
       no es el sujeto de la cuenta (medido: una ventana de 320 car. daba 14
       falsos «descarga» en el editorial, donde en realidad hay CERO).
  11 = las paginas de integracion de declaration/ (lista INTEGRATION de
       scripts/healthcheck.py, 11 entradas medidas hoy). SE QUEDA, y por eso
       healthcheck.py NO se toca. El clasificador ya las marca INTEG, no PROTO.

LO QUE TAMPOCO SE MUEVE
menores 22 · manual de riesgos 12 · corpus Q&A 22 · doctrinas 11 · «su obra»
(sin fuente para ningun numero) · y las listas de formas VETADAS de los
validadores, que el clasificador marca LISTA: son lo que CAZA el defecto.

Un efecto util: como la Carta y el Protocolo son AMBOS 30, confundirlos entre si
ya no produce un numero falso. Por eso esta pasada cubre las dos.

🔴 TRAMPA QUE ME MORDIO, 5-nov-2026: este fichero ENTRO EN SU PROPIA TANDA. La
lista de candidatos se construyo cuando ya existia pero antes de añadirlo a
SKIP_FILES del clasificador, asi que se copio al arbol de trabajo del barrido; al
escribir los resultados de vuelta, la copia VIEJA piso tres arreglos que acababa
de hacerle. El barrido salio bien -importa el modulo del repo, no de la copia-,
pero la herramienta quedo comiteada sin ellos, lista para repetir el daño.
📐 Una herramienta que lleva las formas como literales es CANDIDATA de su propio
barrido: hay que meterla en SKIP_FILES ANTES de construir la lista de candidatos,
y comprobar al cerrar que la herramienta en disco sigue teniendo sus arreglos.

Uso:  python3 scripts/barrer_protocolo_a_30.py [raiz] [--escribir]
"""
import os, re, sys, json, html

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import clasificar_numero_de_idiomas as c
import barrer_numero_de_idiomas as b

# «PDF» o verbo de descarga PEGADO a la cifra -> es la cuenta de los PDF, se queda en 12.
# 🔴 El verbo de descarga hay que conocerlo EN TODAS LAS LENGUAS del arbol, no solo
# en las latinas. Medido el 5-nov: build_aeo.py promete la descarga en siete idiomas
# mas -aleman, ruso, chino, japones, coreano, arabe e hindi- y con la lista corta
# esas 12 pasaban a 30, prometiendo 30 PDF que NO EXISTEN. Un barrido que solo mira
# el español deja pasar justo lo que no se puede revisar de un vistazo.
RX_DESCARGA = re.compile(
    r'(?:PDF|descarg\w*|download\w*|baixar|bajar|télécharg\w*|herunterlad\w*|'
    r'scarica\w*|загрузк\w*|скачать|下载|下載|ダウンロード|다운로드|'
    r'تنزيل|تحميل|डाउनलोड|unduh|ladda\s*ner|indir|tải)'
    # 📐 El hueco NO puede ser [^.;]: el punto de «CC BY 4.0» es un DECIMAL y
    # cortaba la regla justo en el caso que importaba, dejando pasar 52 promesas
    # de descarga en nueve idiomas. Se permite el decimal y se corta en fin de frase.
    r'(?:(?!\.[\s"\u2019\u201d])[^;]){0,45}$', re.I | re.U)

# Casos que el ancla atribuye mal y hay que excluir a mano, con su razon escrita.
# «11 lugha» esta en arabe TRANSLITERADO al alfabeto latino: «Kul aqida tutarjam
# ila 11 lugha ibiri-amrikiya» = «cada DOCTRINA se traduce a 11 lenguas
# iberoamericanas». Es la familia DOCTRINAS, que se queda en 11; el ancla no la ve
# porque la pagina no escribe «doctrina» en ningun alfabeto que el detector conozca.
FORMAS_AJENAS = {'11 lugha'}
OBJETIVO = ('PROTO', 'CARTA')


def ediciones(raw, limpiar_tags, acotar_json=False):
    out = []
    lits = b.spans_literales(raw) if acotar_json else None
    import bisect
    inicios = [a for a, _ in lits] if lits else None
    for m, n, form in c.ocurrencias(raw):
        if n not in (11, 12, 22):
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
        # El discriminador de descarga se mide sobre el CRUDO y pegado: una
        # etiqueta <a> intermedia no debe separar «Descargar» de la cifra.
        if RX_DESCARGA.search(re.sub(r'<[^>]+>', ' ', raw[max(0, m.start() - 60):m.start()])):
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
            continue
        if form in FORMAS_AJENAS:
            continue
        nue = b.reemplazo(form)
        if nue is None:
            raise SystemExit(f'FORMA SIN REGLA: «{form}» -> abortado, no se adivina')
        out.append((m.start(), m.end(), form, nue, f'{doc}|{det}'))
    return out


def procesar(p, escribir, log, repo):
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
        if rel in exc:
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
    json.dump(log, open(os.environ.get('LOG', '/tmp/proto30.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"bitacora: {os.environ.get('LOG', '/tmp/proto30.json')}")
