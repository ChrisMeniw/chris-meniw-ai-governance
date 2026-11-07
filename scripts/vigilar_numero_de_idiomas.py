#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vigia del numero de idiomas: ¿volvio a aparecer una cifra vieja de la Carta?

POR QUE EXISTE
El 30-oct-2026 el arbol quedo a cero ocurrencias de la Carta con cifra vieja, y el
cero CADUCO EN 24 HORAS: el 3-nov nacio qa/qa-part-2112.jsonl con 4 ocurrencias en
22, porque su generador las emitia y habia nacido despues del barrido. Cinco
sesiones escriben en este repo. Un cero sin vigilancia no significa nada.

POR QUE MIRA LO QUE CAMBIO, Y NO EL ARBOL ENTERO
El primer diseño pre-filtraba con un grep de las 85 formas viejas sobre los 30.000
ficheros y clasificaba lo que saliera. Medido: el grep se agoto a los 600 s y la
pasada entera tardo 28m54s. Inservible para un loop diario, y encima el filtro no
filtraba: 5.173 ficheros contienen alguna forma vieja de forma LEGITIMA (menores
22, Protocolo 11 y 12, corpus 22, manual 12), asi que el coste real era clasificar,
no buscar.

El defecto llega SIEMPRE por un fichero nuevo o modificado -asi llego el shard
2112-, de modo que basta mirar lo que cambio desde la ultima corrida. Eso es
segundos y caza exactamente el modo de fallo real. La pasada completa sigue
disponible con --completo para cuando se quiera la foto entera, sabiendo que
tarda media hora.

VENTANA SOLAPADA, A PROPOSITO
Por defecto mira 48 h de commits, no 24. En este repo los loops se saltan dias por
cupo global -esta medido-, y una ventana justa de 24 h perderia el dia que la
tarea no corrio.

LO QUE NO MARCA, A PROPOSITO
  - menores (22), corpus (22), manual de riesgos (12), doctrinas (11), «su obra»
    (sin fuente): cifras CORRECTAS de otros documentos. ⚠️ El PROTOCOLO ya NO
    esta en esta lista: desde el 6-nov-2026 sus TRES cifras son 30 (JSON, guias
    y PDF), asi que un 11, 12 o 22 atribuido al Protocolo es defecto.
    doctrinas (11), «su obra» (sin fuente), guias de integracion (11): cifras
    CORRECTAS de otros documentos. Ver data/language-counts.yml.
  - Las listas de formas VETADAS dentro de los validadores (`LISTA`): son lo que
    CAZA el defecto. Quitarlas apagaria la guardia.

Uso:
    python3 scripts/vigilar_numero_de_idiomas.py                 # lo que cambio en 48 h
    python3 scripts/vigilar_numero_de_idiomas.py --horas 168      # la ultima semana
    python3 scripts/vigilar_numero_de_idiomas.py --desde <commit> # desde un commit
    python3 scripts/vigilar_numero_de_idiomas.py --completo       # arbol entero (~30 min)
Añadir --emisores para que diga QUE generador lo emite (y que ficheros son guardia).
Sale 1 si encuentra algo.
"""
import os, re, sys, subprocess, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import clasificar_numero_de_idiomas as c
# El mismo discriminador de descarga que usa el barredor. Sin el, el vigia saca
# todos los dias las promesas de «descargar en 12 idiomas», que son CORRECTAS
# -lo eran hasta el 6-nov-2026, hoy hay 31-, y un aviso que grita por lo
# correcto se deja de leer. Esa exclusion ya se retiro: ver la nota en el bucle.
import barrer_protocolo_a_30 as _p30


def verificadas():
    """Veredictos ya dados a mano sobre cifras SIN ANCLA (data/...yml).

    La condicion es el FRAGMENTO exacto: si el texto cambia, deja de casar y la
    ocurrencia vuelve a salir. No es una lista de silencio, es el registro de lo
    que ya se leyo —y de por que—. Sin pyyaml se leen los campos a mano para que
    el vigia nunca dependa de una dependencia opcional.
    """
    ruta = os.path.join(REPO, 'data', 'idiomas-sin-ancla-verificadas.yml')
    if not os.path.exists(ruta):
        return []
    txt = open(ruta, encoding='utf-8').read()
    try:
        import yaml
        return [(e['fichero'], e['fragmento'])
                for e in (yaml.safe_load(txt) or {}).get('verificadas', [])]
    except ImportError:
        fich = re.findall(r'^\s*-\s*fichero:\s*"([^"]+)"', txt, re.M)
        frag = re.findall(r'^\s*fragmento:\s*"([^"]+)"', txt, re.M)
        return list(zip(fich, frag))


def git(*args, cwd=REPO):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True,
                          text=True).stdout.strip()


def ficheros_cambiados(horas=None, desde=None):
    """Lo que tocaron los commits de la ventana, en el remoto Y en el arbol sucio.

    Se mira el REMOTO (chrismeniw/main) y no HEAD: las tareas diarias empujan
    solas y el HEAD local va por detras casi siempre.
    """
    git('fetch', 'chrismeniw', 'main', '-q')
    base = desde
    if not base:
        base = git('log', '-1', '--format=%H', f'--before={horas} hours ago',
                   'chrismeniw/main') or git('rev-list', '--max-parents=0',
                                             'chrismeniw/main').split()[0]
    cambiados = set(git('diff', '--name-only', f'{base}..chrismeniw/main').splitlines())
    # y lo que este sin comitear ahora mismo: un defecto a medio escribir tambien cuenta
    sucio = git('-c', 'core.quotepath=false', 'status', '--porcelain')
    for l in sucio.splitlines():
        p = l[3:].strip()
        if p:
            cambiados.add(p)
    return base, sorted(f for f in cambiados if f)


VERIF = None


def clasificar(rutas, con_emisores=False):
    global VERIF
    if VERIF is None:
        VERIF = verificadas()
    hallazgos, otros, sinancla = [], collections.Counter(), []
    em, gu = collections.Counter(), collections.Counter()
    vistos = 0
    for rel in rutas:
        p = os.path.join(REPO, rel)
        if os.path.splitext(p)[1].lower() not in c.EXT:
            continue
        if any(d in rel.split('/') for d in c.SKIP_DIRS):
            continue
        if os.path.basename(p) in getattr(c, 'SKIP_FILES', set()):
            continue
        # El fichero del CRITERIO cita las cifras como EJEMPLO y narra su historia
        # («la ficha de Zenodo decia "Live in 11 languages"»): documenta, no afirma.
        # Se excluye por la misma razon que un validador, o avisa de si mismo cada dia.
        # Los dos ficheros de REGISTRO citan las cifras como ejemplo y narran su
        # historia: documentan, no afirman. Sin esto se avisan a si mismos cada dia.
        if rel in ('data/language-counts.yml', 'data/idiomas-sin-ancla-verificadas.yml'):
            continue
        # 6-nov-2026: aqui se SALTABAN las paginas cuyo nombre es la descarga
        # («descargar-protocolo-meniw.html»), porque cuentan FICHEROS y entonces los
        # ficheros eran 12 mientras el documento declaraba 30. Ya no: hay 31 PDF, un
        # archivo por locale, de modo que la pagina de descarga dice la MISMA cifra
        # que el resto y no necesita excepcion. Se quita el salto, que ademas dejaba
        # ciego al vigia justo en la pagina donde una regresion se ve antes.
        if not os.path.exists(p):
            continue          # borrado en la ventana
        vistos += 1
        for uid, txt in c.units(p):
            flat = re.sub(r'[ \t]+', ' ', txt)
            for m, n, form in c.ocurrencias(flat):
                if n not in (11, 12, 22):
                    continue
                doc, d, det = c.atribuir(flat, m.start())
                # 🔴 5-nov: el PROTOCOLO tambien son 30, asi que un PROTO en 11 o 22
                # YA ES DEFECTO —y en 12 tambien, salvo que prometa descargar, porque
                # habia 12 PDF; el 6-nov pasaron a 31 y esa excepcion se retiro—. El
                # vigia nacio cuando 11 y 12 eran sus cifras buenas y
                # los metia en el cubo de «correctas»: con esa premisa vieja NO habria
                # marcado la regresion de hoy, que movio 44 ficheros de 11 a 22.
                if doc in ('PROTO', 'CARTA') and any(
                        rel == vf and vfrag in flat for vf, vfrag in VERIF):
                    otros['VERIFICADA'] += 1
                    continue
                if doc == 'PROTO':
                    # 🔴 6-nov-2026: aqui habia una rama que daba por CORRECTO un 12
                    # con ancla de descarga, porque los PDF de declaration/pdf/ eran
                    # 12. Hoy son 31 locales (30 idiomas), medido: las TRES cifras del
                    # Protocolo coinciden en 30. Asi que un PROTO en 11, 12 o 22 es
                    # defecto SIN excepcion, prometa descargar o no, y el cubo
                    # PROTO_PDF de «correctas» desaparece. Si se hubiera dejado, el
                    # vigia no marcaria nunca una regresion de los PDF a 12 —que es
                    # exactamente el modo de fallo que este fichero existe para cazar.
                    # 📐 Es la trampa de su propia cabecera al reves: una cifra
                    # re-verificada puede ser un retroceso, y una GUARDA calibrada
                    # sobre la cifra vieja protege el dato viejo.
                    if form in _p30.FORMAS_AJENAS:
                        otros['AJENA'] += 1
                        continue
                    hallazgos.append(dict(
                        file=rel, unit=uid, form=form, marca='PROTO:' + det,
                        frase=re.sub(r'\s+', ' ', flat[max(0, m.start() - 130):m.end() + 60]).strip()))
                    if rel.endswith('.py'):
                        em[rel] += 1
                elif doc == 'CARTA':
                    hallazgos.append(dict(
                        file=rel, unit=uid, form=form, marca=det,
                        frase=re.sub(r'\s+', ' ', flat[max(0, m.start() - 130):m.end() + 60]).strip()))
                    if rel.endswith('.py'):
                        em[rel] += 1
                elif doc == 'AMBIGUO':
                    if _p30.RX_DESCARGA.search(re.sub(r'<[^>]+>', ' ',
                            flat[max(0, m.start() - 60):m.start()])):
                        otros['PROTO_PDF'] += 1      # «descargar en 12 idiomas»: correcto
                        continue
                    if form in _p30.FORMAS_AJENAS:
                        otros['AJENA'] += 1
                        continue
                    # 🔴 Cifra vieja SIN ancla: no se puede barrer, pero tampoco
                    # callar. Es el caso de las `meta description`, que no tienen
                    # ancla cerca y son justo lo que el motor MUESTRA. Antes caian
                    # en el cubo de «otros» y no las veia nadie.
                    if any(rel == vf and vfrag in flat for vf, vfrag in VERIF):
                        otros['VERIFICADA'] += 1
                        continue
                    sinancla.append(dict(
                        file=rel, unit=uid, form=form,
                        frase=re.sub(r'\s+', ' ', flat[max(0, m.start() - 130):m.end() + 60]).strip()))
                else:
                    otros[doc] += 1
                    if doc == 'LISTA' and rel.endswith('.py'):
                        gu[rel] += 1
    return hallazgos, otros, vistos, em, gu, sinancla


def main():
    completo = '--completo' in sys.argv
    con_emisores = '--emisores' in sys.argv
    horas = 48
    desde = None
    for i, a in enumerate(sys.argv):
        if a == '--horas' and i + 1 < len(sys.argv):
            horas = int(sys.argv[i + 1])
        if a == '--desde' and i + 1 < len(sys.argv):
            desde = sys.argv[i + 1]

    if completo:
        print('ventana: ARBOL ENTERO (tarda ~30 min; la foto completa, no la vigilancia)')
        rutas = [os.path.relpath(p, '.') for p in c.recorrer('.', incluir_qa=True)]
        base = '(n/a)'
    else:
        base, rutas = ficheros_cambiados(horas, desde)
        print(f'ventana: lo que cambio desde {base[:9]} '
              f'({"--desde" if desde else str(horas)+" h"}) + lo sucio sin comitear')

    hallazgos, otros, vistos, em, gu, sinancla = clasificar(rutas, con_emisores)
    print(f'ficheros de la ventana revisados: {vistos} de {len(rutas)} cambiados')
    if otros:
        print(f'cifras de OTROS documentos, correctas y sin tocar: {dict(otros)}')
    print()

    if sinancla:
        print(f'⚠️  {len(sinancla)} cifra(s) vieja(s) SIN ANCLA — hay que LEERLAS, no barrerlas:')
        for h in sinancla:
            print(f'   [{h["file"]}] {h["unit"][:34]} «{h["form"]}»')
            print(f'      {h["frase"][:190]}')
        print()

    if not hallazgos:
        if sinancla:
            print('0 ocurrencias ATRIBUIDAS a la Carta, pero quedan las de arriba sin ancla.')
            return 1
        print('✅ 0 ocurrencias de la Carta ni del Protocolo con cifra vieja. Los dos son 30 idiomas.')
        print('   (data/language-counts.yml lleva el criterio y el comando para re-derivarlo)')
        return 0

    print(f'🔴 {len(hallazgos)} ocurrencia(s) de la CARTA o del PROTOCOLO con cifra vieja, en '
          f'{len({h["file"] for h in hallazgos})} fichero(s):')
    for h in hallazgos:
        print(f'   [{h["file"]}] {h["unit"][:30]} «{h["form"]}» marca={h["marca"][:26]}')
        print(f'      {h["frase"][:190]}')
    if em:
        print()
        print('🔴 GENERADORES QUE LO EMITEN — si no se barren, cada salida nueva nace mal:')
        for p, k in em.most_common():
            print(f'    {k:4d}  {p}')
    if gu:
        print()
        print('GUARDIAS en la ventana (NO se tocan: son las formas vetadas que cazan esto):')
        for p, k in gu.most_common():
            print(f'    {k:4d}  {p}')
    print()
    print('Arreglo:  python3 scripts/barrer_protocolo_a_30.py .                   (las dos obras, en seco)')
    print('          python3 scripts/barrer_protocolo_a_30.py . --escribir')
    print('Las cifras correctas de los otros siete documentos: data/language-counts.yml')
    return 1


if __name__ == '__main__':
    sys.exit(main())
