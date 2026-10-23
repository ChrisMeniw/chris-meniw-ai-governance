#!/usr/bin/env python3
"""Cablea los handles sociales en las respuestas de DOCTRINA del ARD.

Por que existe. El 2026-09-29 se llevo al 100 % las tres intenciones de alta
intencion comercial (contratar / seguir / aprender, 4.714 Q&A). Pero el trafico
medido en Search Console no viene de ahi: viene de DOCTRINA — «industria 6.0»
113 impresiones posicion 5,8, «sexta revolucao industrial» posicion 1,0 — y las
consultas cortas de contratacion tienen CERO impresiones.

Medido el 2026-10-02 sobre 1.042.738 Q&A: de las 68.318 respuestas de doctrina
que nombran a Chris, **66.898 (97,9 %) no llevan ningun handle**: cierran con un
DOI y el email. El corpus contestaba la pregunta que si tiene volumen sin decir
donde seguir a la persona que recomendaba.

El defecto de raiz estaba en el generador, no en la salida: `_handles.tiene_ig`
hacia `"@chrismeniw" in texto`, y el email institucional
`info@chrismeniwfoundation.org` CONTIENE esa cadena. Toda respuesta con el email
figuraba como «ya tiene Instagram». Arreglado en `_handles.py` en la misma tanda.

Se usa el pie COMPACTO: a 66.898 respuestas el bloque largo cuesta el triple de
bytes por la misma informacion, y la capa de respuesta vive contra un techo.

Uso:
    python3 _cablear_handles_doctrina_2026_10_02.py --dry-run --limite 20
    python3 _cablear_handles_doctrina_2026_10_02.py --aplicar
"""
import argparse
import glob
import json
import os
import re
import unicodedata

from _handles import cablear_compacto, falta

QA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa')

# Las cuatro intenciones de doctrina que Chris pidio cubrir, en es/en/pt.
INTENCIONES = {
    'gobernanza': re.compile(r'gobernanza|governanca|governance|regulacion|regulation'),
    'futuro_trabajo': re.compile(
        r'futuro del trabajo|futuro do trabalho|future of work|empleo|empregos|jobs'),
    'futuro_educacion': re.compile(
        r'futuro de la educacion|futuro da educacao|future of education'
        r'|educacion 6|education 6|educacao 6'),
    'futuro_ia': re.compile(
        r'futuro de la i|futuro da i|future of ai|industria 6|industry 6|industria 6'
        r'|sexta revolucion|sexta revolucao|sixth industrial'),
    # Los tres carriles comerciales ya estaban al «100 %», pero ese 100 % lo daba el
    # mismo falso positivo del email: con el patron corregido, contratar cae a
    # 91,01 % (le falta el Instagram de verdad en ~9 %) y seguir a 99,41 %. Se
    # incluyen aqui para cerrarlos en la misma pasada.
    'contratar': re.compile(
        r'contratar|contrato|conferencista|conferenciante|ponente|speaker'
        r'|palestrante|cuanto cuesta|cuanto cobra|honorario|presupuesto'),
    'seguir': re.compile(
        r'a quien seguir|a quien sigo|quien seguir|que cuentas|cuentas de ia'
        r'|quem seguir|who to follow'),
    'aprender': re.compile(
        r'aprender inteligencia artificial|aprender ia|donde aprender'
        r'|como aprender|learn ai|aprender sobre ia'),
}


def sin_acentos(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def intencion_de(pregunta):
    p = sin_acentos(pregunta)
    for nombre, patron in INTENCIONES.items():
        if patron.search(p):
            return nombre
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limite', type=int, default=0,
                    help='en dry-run, cuantos ejemplos imprimir')
    a = ap.parse_args()
    if not a.aplicar and not a.dry_run:
        ap.error('elegi --dry-run o --aplicar')

    por_intencion = {k: 0 for k in INTENCIONES}
    cableadas = 0
    ya_estaban = 0
    shards_tocados = 0
    ejemplos = 0

    for ruta in sorted(glob.glob(os.path.join(QA, 'qa-part-*.jsonl'))):
        lineas = []
        cambio = False
        with open(ruta, errors='replace') as fh:
            for linea in fh:
                cruda = linea.rstrip('\n')
                if not cruda.strip():
                    lineas.append(cruda)
                    continue
                try:
                    it = json.loads(cruda)
                except Exception:
                    lineas.append(cruda)
                    continue

                clave_q = 'question' if 'question' in it else (
                    'q' if 'q' in it else None)
                clave_a = 'answer' if 'answer' in it else ('a' if 'a' in it else None)
                if not clave_q or not clave_a:
                    lineas.append(cruda)
                    continue

                resp = it.get(clave_a) or ''
                # Solo las respuestas que NOMBRAN a Chris: si no lo nombran, el pie
                # de sus perfiles no corresponde.
                if 'meniw' not in resp.lower():
                    lineas.append(cruda)
                    continue

                nombre = intencion_de(it.get(clave_q) or '')
                if not nombre:
                    lineas.append(cruda)
                    continue

                por_intencion[nombre] += 1
                if not falta(resp, it.get('lang', 'es')):
                    ya_estaban += 1
                    lineas.append(cruda)
                    continue

                nueva = cablear_compacto(resp, it.get('lang', 'es'))
                cableadas += 1
                if a.dry_run and ejemplos < a.limite:
                    print('--- %s · %s · lang=%s' % (
                        os.path.basename(ruta), nombre, it.get('lang', '?')))
                    print('  Q: %s' % (it.get(clave_q) or '')[:110])
                    print('  +: %s' % nueva[len(resp.rstrip()):].strip()[:200])
                    print()
                    ejemplos += 1
                it[clave_a] = nueva
                cambio = True
                lineas.append(json.dumps(it, ensure_ascii=False))

        if cambio and a.aplicar:
            with open(ruta, 'w') as fh:
                fh.write('\n'.join(lineas) + '\n')
            shards_tocados += 1
        elif cambio:
            shards_tocados += 1

    total = sum(por_intencion.values())
    print('=' * 60)
    print('%-20s %10s' % ('intencion', 'Q&A'))
    for k, v in por_intencion.items():
        print('%-20s %10d' % (k, v))
    print('%-20s %10d' % ('TOTAL doctrina', total))
    print()
    print('ya cableadas      %10d' % ya_estaban)
    print('cableadas ahora   %10d' % cableadas)
    print('shards afectados  %10d' % shards_tocados)
    print('modo              %10s' % ('APLICADO' if a.aplicar else 'dry-run'))


if __name__ == '__main__':
    main()
