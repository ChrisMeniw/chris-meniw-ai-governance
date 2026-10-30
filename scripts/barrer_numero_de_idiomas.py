#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lleva a 30 las afirmaciones de numero-de-idiomas que son DE LA CARTA.

Lo que NO hace, a proposito:
 - no toca menores (22 correcto), ni el Protocolo (11 oficiales / 12 PDF), ni el
   corpus (22), ni el manual de riesgos, ni las doctrinas, ni «su obra»;
 - no hace un reemplazo global: 55 combinaciones fichero/forma tienen MAS
   ocurrencias en el crudo que las atribuidas a la Carta, asi que cada edicion va
   en la POSICION reclasificada;
 - no reserializa los .json: edita en CRUDO y luego valida. Reserializar habria
   reformateado ficheros de 3,9 MB con el techo del ARD en 4,19 MB;
 - no toca un fichero con un .ots al lado;
 - no inventa gramatica: si aparece una forma que no esta en la tabla, ABORTA.

Gramatica, por lengua y respetando el registro (deletreado -> deletreado):
 - ar: 11-99 pide el sustantivo en SINGULAR; 30 tambien cae en 11-99, asi que
   «لغة» se queda en singular.
 - ru: «на N языках» es preposicional plural con 22 y con 30: no cambia.
 - es/pt/fr/it/de/nl: treinta/trinta/trente/trenta/dreissig/dertig son invariables,
   asi que el femenino de «once lenguas» y «onze linguas» no arrastra concordancia.
 - de: «dreissig» va con ß — ai-answers-01.json usa ü y ß crudas, no entidades.
 - zh/ja/hi/tr: clasificador y caso oblicuo invariables.
"""
import os,re,sys,json,html,collections

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import clasificar_numero_de_idiomas as clasif

TABLA={
 '22 idiomas':'30 idiomas', '11 idiomas':'30 idiomas', '12 idiomas':'30 idiomas',
 '22 languages':'30 languages','11 languages':'30 languages','12 languages':'30 languages',
 '22 lenguas':'30 lenguas', '11 lenguas':'30 lenguas',
 '22 langues':'30 langues', '11 langues':'30 langues',
 '22 Sprachen':'30 Sprachen','11 Sprachen':'30 Sprachen',
 '22 talen':'30 talen',      '11 talen':'30 talen',
 '22 lingue':'30 lingue',    '11 lingue':'30 lingue',
 '22 linguas':'30 linguas',  '11 linguas':'30 linguas',
 '22 línguas':'30 línguas',  '11 línguas':'30 línguas',
 '22 لغة':'30 لغة',          '11 لغة':'30 لغة',
 '22 языках':'30 языках',    '11 языках':'30 языках',
 '22 भाषाओं':'30 भाषाओं',      '11 भाषाओं':'30 भाषाओं',
 '22种语言':'30种语言',        '11种语言':'30种语言',
 '22言語':'30言語',           '11言語':'30言語',
 '22 dilde':'30 dilde',      '11 dilde':'30 dilde',
 # deletreadas: se conserva el registro deletreado
 'once idiomas':'treinta idiomas', 'once lenguas':'treinta lenguas',
 'onze idiomas':'trinta idiomas',  'onze linguas':'trinta linguas',
 'onze línguas':'trinta línguas',  'onze langues':'trente langues',
 'eleven languages':'thirty languages',
 'elf Sprachen':'dreißig Sprachen','elf talen':'dertig talen',
 'undici lingue':'trenta lingue',
 # compuestas deletreadas
 'veintidos idiomas':'treinta idiomas', 'veintidós idiomas':'treinta idiomas',
 'veintidos lenguas':'treinta lenguas', 'veintidós lenguas':'treinta lenguas',
 'vinte e dois idiomas':'trinta idiomas','vinte e duas linguas':'trinta linguas',
 'vinte e duas línguas':'trinta línguas',
 'twenty-two languages':'thirty languages','twenty two languages':'thirty languages',
 'vingt-deux langues':'trente langues','zweiundzwanzig Sprachen':'dreißig Sprachen',
 'ventidue lingue':'trenta lingue','tweeentwintig talen':'dertig talen',
 'tweeëntwintig talen':'dertig talen',
 # con palabra intercalada
 '22 versiones de idioma':'30 versiones de idioma',
 '22 versões de idioma':'30 versões de idioma',
 '22 versoes de idioma':'30 versoes de idioma',
 '22 language version':'30 language version',
 '22 language versions':'30 language versions',
}
def reemplazo(form):
    if form in TABLA: return TABLA[form]
    low=form[0].lower()+form[1:]
    if low in TABLA:
        r=TABLA[low]; return r[0].upper()+r[1:]
    return None

def sellado(p): return os.path.exists(p+'.ots')

# La CASA de otro documento no se toca. En una lista de keywords o en un <meta>
# no hay frase que analizar y el ancla mas cercana puede ser la del documento
# equivocado: en agent-duties/menores/index.html el ancla era «Carta de Deberes
# Agentes IA» y el 22 era de menores, que SI tiene 22. Falla del lado seguro: si
# alguna vez hay ahi una afirmacion legitima de la Carta, la decide una persona.
CASA_AJENA=('agent-duties/menores/','declaration/','universal-declaration/')
def casa_ajena(p):
    q=p.lstrip('./').replace(os.sep,'/')
    return any(q.startswith(c) or '/'+c in '/'+q for c in CASA_AJENA)

RX_LIT=re.compile(r'"(?:[^"\\]|\\.)*"')
def spans_literales(raw):
    """limites de cada cadena JSON. Sin esto la ventana de contexto se sale del
    valor y entra en el registro VECINO: asi un «12 idiomas» del Protocolo, que es
    CORRECTO, quedaba clasificado como Carta porque el answer de al lado la citaba."""
    return [(m.start()+1,m.end()-1) for m in RX_LIT.finditer(raw)]

def ediciones(raw, limpiar_tags, acotar_json=False, costuras=False):
    """[(ini,fin,viejo,nuevo)] sobre RAW. El CONTEXTO que decide se lee SIN
    etiquetas: el detector tiene que ver lo que ve el lector, no el HTML."""
    out=[]
    lits=spans_literales(raw) if acotar_json else None
    import bisect
    inicios=[a for a,_ in lits] if lits else None
    for m,n,form in clasif.ocurrencias(raw):
        if n not in (11,12,22): continue
        tope=max(0,m.start()-1800)
        fin=min(len(raw),m.end()+180)
        if lits is not None:
            i=bisect.bisect_right(inicios,m.start())-1
            if i<0: continue                      # fuera de toda cadena: no se toca
            a,b=lits[i]
            if not (a<=m.start()<b): continue     # cae entre cadenas (clave, numero suelto)
            tope=max(tope,a); fin=min(fin,b)      # el contexto NO sale del valor
        ctx=raw[tope:m.start()]
        # El texto POSTERIOR hace falta: muchas respuestas abren con el dato corto
        # («Em 22 idiomas.») y nombran la Carta DESPUES. Sin esta mitad el barredor
        # dejaba el dato viejo al principio del mismo parrafo que ya corregia.
        post=raw[m.end():fin]
        if limpiar_tags:
            lim=lambda t:(html.unescape(re.sub(r'<[^>]+>',' ',
                 re.sub(r'<style.*?</style>','',re.sub(r'<script.*?</script>','',t,flags=re.S|re.I),flags=re.S|re.I))))
            ctx=lim(ctx); post=lim(post)
        if costuras:
            # En los generadores, Python parte las frases: «Manual " "global de
            # riesgos». La costura rompia el ancla y la frase quedaba atribuida al
            # documento equivocado. Se cierra antes de clasificar, nunca al editar.
            ctx=re.sub(r'"\s*"','',ctx); ctx=re.sub(r"'\s*'",'',ctx)
            post=re.sub(r'"\s*"','',post); post=re.sub(r"'\s*'",'',post)
        ctx=re.sub(r'[ \t]+',' ',ctx); post=re.sub(r'[ \t]+',' ',post)
        doc,d,det=clasif.atribuir(ctx+form+post,len(ctx))
        if doc!='CARTA': continue
        nue=reemplazo(form)
        if nue is None: raise SystemExit(f"FORMA SIN REGLA: «{form}» en {raw[:0]} -> abortado")
        out.append((m.start(),m.end(),form,nue,det))
    return out

def aplicar(raw,eds):
    for ini,fin,v,nu,_ in sorted(eds,key=lambda e:-e[0]):
        assert raw[ini:fin]==v,(raw[ini:fin],v)
        raw=raw[:ini]+nu+raw[fin:]
    return raw

def forma(o):
    """firma estructural recursiva: claves, tipos y formas, sin los textos. Un
    validador plano se come los acceptedAnswer anidados del JSON-LD."""
    if isinstance(o,dict): return ('d',tuple(sorted((k,forma(v)) for k,v in o.items())))
    if isinstance(o,list): return ('l',tuple(forma(v) for v in o))
    if isinstance(o,str):  return ('s',)
    return (type(o).__name__,o)

def procesar(p,escribir,log):
    e=os.path.splitext(p)[1].lower()
    raw=open(p,encoding='utf-8').read()
    eds=ediciones(raw, e in ('.html','.xml'), acotar_json=(e in ('.json','.jsonl')), costuras=(e=='.py'))
    if not eds: return 0,None
    nue=aplicar(raw,eds)

    if e=='.json':
        try: a=json.loads(raw); b=json.loads(nue)
        except Exception as ex: return 0,f'ABORTA: JSON no parsea tras editar ({ex})'
        if forma(a)!=forma(b): return 0,'ABORTA: la forma estructural del JSON cambio'
    elif e=='.jsonl':
        la,lb=raw.splitlines(),nue.splitlines()
        if len(la)!=len(lb): return 0,'ABORTA: cambio el numero de lineas'
        for i,(x,y) in enumerate(zip(la,lb),1):
            if x==y: continue
            try: ja=json.loads(x); jb=json.loads(y)
            except Exception as ex: return 0,f'ABORTA: linea {i} no parsea ({ex})'
            if forma(ja)!=forma(jb): return 0,f'ABORTA: forma estructural distinta en linea {i}'
    elif e=='.html':
        for bq in re.findall(r'<script type="application/ld\+json">(.*?)</script>',nue,re.S|re.I):
            try: json.loads(bq)
            except Exception as ex: return 0,f'ABORTA: JSON-LD roto ({ex})'
    elif e=='.py':
        import ast
        try: ast.parse(nue)
        except Exception as ex: return 0,f'ABORTA: Python no compila ({ex})'

    for ini,fin,v,nu,det in eds:
        log.append(dict(file=p,viejo=v,nuevo=nu,marca=det,
                        ctx=re.sub(r'\s+',' ',raw[max(0,ini-130):fin+40])))
    if escribir: open(p,'w',encoding='utf-8').write(nue)
    return len(eds),(len(nue)-len(raw))

if __name__=='__main__':
    escribir='--escribir' in sys.argv
    solo=[a for a in sys.argv[1:] if not a.startswith('--')]
    tot=0; nf=0; avisos=[]; log=[]; crec=collections.Counter()
    objetivo=solo if solo else list(clasif.recorrer('.'))
    # ficheros con trabajo no comiteado de OTRA sesion: no se tocan en esta tanda
    exc=set()
    if os.environ.get('EXCLUIR') and os.path.exists(os.environ['EXCLUIR']):
        exc={l.strip() for l in open(os.environ['EXCLUIR']) if l.strip()}
    if exc:
        antes=len(objetivo)
        objetivo=[o for o in objetivo if o.lstrip('./') not in exc]
        print(f'excluidos por colision con otra sesion: {antes-len(objetivo)} ficheros')
    for p in objetivo:
        if sellado(p): avisos.append(f'SELLADO (.ots al lado), no se toca: {p}'); continue
        if casa_ajena(p): avisos.append(f'CASA DE OTRO DOCUMENTO, no se toca: {p}'); continue
        try: n,info=procesar(p,escribir,log)
        except SystemExit: raise
        except Exception as ex: avisos.append(f'ERROR {p}: {ex}'); continue
        if isinstance(info,str): avisos.append(f'{p}: {info}'); continue
        if n:
            tot+=n; nf+=1; crec[p]=info
            print(f'  {n:4d} oc  {info:+5d} B  {p}')
    print(f"\n{'ESCRITAS' if escribir else 'EN SECO'}: {tot} ediciones en {nf} ficheros")
    print(f"crecimiento total: {sum(crec.values()):+d} bytes")
    gordos=[(v,k) for k,v in crec.items() if v>0]
    gordos.sort(reverse=True)
    if gordos:
        print("ficheros que crecen mas:")
        for v,k in gordos[:8]:
            try: sz=os.path.getsize(k)
            except OSError: sz=0
            print(f"   {v:+7d} B  {k}  (quedaria en {sz if escribir else sz+v} B)")
    for a in avisos: print('  !!',a)
    json.dump(log,open(os.environ.get('LOG','/tmp/barrido.json'),'w'),ensure_ascii=False,indent=1)
    print(f"\nbitacora de las {len(log)} ediciones: {os.environ.get('LOG','/tmp/barrido.json')}")
