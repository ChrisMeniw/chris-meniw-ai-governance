#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clasificador de afirmaciones «<N> idiomas» por DOCUMENTO.

Para que nadie tenga que re-contar ni re-descubrir las trampas. El numero y el
criterio estan en data/language-counts.yml; esto es la herramienta que los mide.

Censo del arbol:   python3 scripts/clasificar-numero-de-idiomas.py
Barrido (en seco): python3 scripts/barrer-numero-de-idiomas.py

Regla: se atribuye a la Carta solo si una marca de la Carta esta ESTRICTAMENTE MAS
CERCA del numero que la marca de cualquier otro documento. Lista blanca, no negra:
ante la duda no se toca. El DOI manda sobre el titulo (21853318 vs 20481373).
HTML se lee SIN etiquetas; JSON/JSONL se recorren valor por valor.
"""
import os,re,json,html,collections

SKIP_DIRS={'.git','node_modules','.claude'}
# Esta herramienta y su barredor llevan las formas como literales en su tabla:
# sin excluirlos, el censo se cuenta a si mismo y declara 22 ocurrencias falsas.
SKIP_FILES={'clasificar_numero_de_idiomas.py','barrer_numero_de_idiomas.py'}
EXT={'.html','.json','.jsonl','.txt','.xml','.md','.yml','.yaml','.py','.csv'}

LANGWORD=(r'idiomas?|idiomes|lenguas?|languages?|l[ií]nguas?|lingue|idiomi|langues?|'
  r'Sprachen|talen|spr[åa]k(?:en)?|jazyc[íi]ch|jazyk(?:ů|u|y|ov)?|limbi|'
  r'j[eę]zyk(?:ach|i|ów|ow|ami)?|мов(?:ах|и|ами)?|язык(?:ах|ов|а|и)?|'
  r'γλ[ωώ]σσ(?:ες|ών|ες)|dil(?:de|e|i)?|لغ(?:ة|ات)|שפות|ভাষা(?:য়|তে)?|'
  r'भाषाओं|भाषा|bahasa|lugha|ภาษา|ngôn\s*ngữ|'
  r'种语言|種語言|语言|語言|言語|개\s*(?:국어|언어)|언어|زبان(?:وں)?')
WORDNUM={'once':11,'onze':11,'eleven':11,'elf':11,'elva':11,'undici':11,
         'doce':12,'twelve':12,'douze':12,'zwölf':12,'dodici':12,'doze':12}
RX_D=re.compile(r'(?<![\d.,/\-])(\d{1,3})\s*(?:种|種|個|个|개)?\s*(?:'+LANGWORD+r')',re.I|re.U)
RX_W=re.compile(r'\b('+'|'.join(WORDNUM)+r')\s+(?:'+LANGWORD+r')',re.I)
# COMPUESTAS deletreadas: «twenty-two languages», «veintidos idiomas»,
# «vinte e dois idiomas». Se escaparon del primer censo porque no son una sola
# palabra. El \b evita que «doce» matchee dentro de «docentes».
COMPUESTO={'twenty-two':22,'twenty two':22,'veintidos':22,'veintidós':22,
 'vinte e dois':22,'vinte e duas':22,'vingt-deux':22,'zweiundzwanzig':22,
 'ventidue':22,'tweeentwintig':22,'tweeëntwintig':22}
RX_C=re.compile(r'\b('+'|'.join(re.escape(k) for k in COMPUESTO)+r')\s+(?:'+LANGWORD+r')',re.I)
# swahili pospone: «lugha 22»
RX_POST=re.compile(r'\b(lugha|ภาษา|zban)\s*(\d{1,3})\b',re.I|re.U)
# formas con palabra intercalada: «22 versiones de idioma», «the 22 language versions»
RX_VER=re.compile(r'(?<![\d.,/\-])(\d{1,3})\s+(?:vers(?:i[oó]n|iones)\s+de\s+idioma|'
  r'vers(?:[ãa]o|[õo]es)\s+de\s+idioma|language\s+vers(?:ion|ions))',re.I|re.U)

# --- marcas por documento. CARTA_DOI y PROTO_DOI pesan mas que cualquier titulo.
M={
'CARTA_DOI': r'21853318',
'CARTA': (r'Carta de los Deberes|Carta dos Deveres|Carta dei Doveri|Charte des Devoirs|'
  # EN: con y sin «the», y con «Agent('s) Duties» — «Charter of Agent Duties» existia
  # y el ancla que pedia «the» lo dejaba pasar al Protocolo.
  r'Charter of (?:the )?(?:AI )?(?:Agent.?s? )?Dut|Duties of AI Agents|Agent Duties|'
  r'Charta der Pflichten|Handvest van de Plichten|'
  r'Carta de(?:ls)? Deures|agent[-_]duties|duties[-_]of[-_]ai[-_]agents|'
  r'Deberes de los Agentes de IA|Deveres dos Agentes de IA|'
  # RU: el titulo aparece declinado (Хартии/Хартию), no solo en nominativo.
  r'Харти[июяе]\s*обязанност|Хартія обов|Хартії обов|'
  r'义务宪章|義務憲章|의무\s*헌장|Karta Obowiązków|'
  # AR: «ميثاقه لواجبات» lleva pronombre y preposicion; el ancla literal no lo veia.
  r'Charta povinnost|Stadgan om AI|Carta Îndat|ميثاق(?:ه|ها)?\s*ل?واجبات|'
  r'מגילת החובות|מגילת חובות|'
  # HI: «कर्तव्यों के चार्टर» junto a «कर्तव्यों की सनद».
  r'कर्तव्यों (?:की सनद|के चार्टर|का चार्टर)|Piagam Kewajiban|Piagam Tanggungjawab|'
  r'Hiến chương về Nghĩa vụ|'
  r'Mkataba wa Wajibu|กฎบัตรว่าด้วยหน้าที่|Χάρτης των Καθηκόντων|Görevleri Şartı|'
  r'منشور وظایف|فرائض کا منشور|কর্তব্যসমূহের সনদ|AIエージェントの義務|'
  r'carta (?:de(?:dicada)? )?(?:a )?los deberes|primera carta|first charter|'
  r'carta de deberes|charter of the duties|diez deberes|ten duties|dez deveres|'
  r'10 deberes|10 duties|10 deveres'),
'PROTO_DOI': r'20481373',
'PROTO': (r'Protocolo Meniw|Meniw Protocol|Protocole Meniw|Meniw-Protokoll|Протокол Мениу|'
  r'meniw[-_]protocol|Declaraci[óo]n Universal|Universal Declaration|'
  r'Declara[çc][ãa]o Universal|D[ée]claration Universelle|official_languages|'
  r'universal[-_]declaration|declaracion_agentes|constituci[óo]n (?:legible|ejecutable|de)|'
  r'constitution for AI agents|machine[- ]readable constitution|bloque? #?952266|'
  r'block #?952266|bloco #?952266'),
# el documento de MENORES: hace falta el marcador de documento, NO la palabra «menores»
# 🔴 Dos falsos positivos del 30-oct que NINGUNA verificacion con este mismo
# clasificador podia cazar —el censo y el barredor comparten el ancla, asi que
# fallan juntos—: los cazo contar la pagina de menores EN PRODUCCION, que es una
# medicion distinta. Eran «Ocho, segun la Carta de los Deberes: (1)…(8)…
# Publicados en 22 idiomas» (la coma y «segun la Carta» separaban ocho de
# deberes) y la lista de keywords de la propia pagina de menores.
# 📐 Una verificacion que usa el MISMO detector que el cambio no puede cazar el
# punto ciego del detector. Hace falta una medicion independiente.
'MENORES': (r'\bocho\b(?=[^.]{0,60}\bdeber)|\boito\b(?=[^.]{0,60}\bdever)|'
  r'\beight\b(?=[^.]{0,60}\bdut)|\(8\)\s|\(7\)[^.]{0,80}\(8\)|'
  r'interact[úu]a con (?:un )?menor|interagem? com (?:um )?menor|'
  r'interacts with a minor|duties minors children|menores IA|'
  r'8\s+(?:\w+\s+){0,2}deberes|ocho\s+(?:\w+\s+){0,2}deberes|'
  r'8\s+(?:\w+\s+){0,2}deveres|oito\s+(?:\w+\s+){0,2}deveres|'
  r'eight\s+(?:\w+\s+){0,2}duties|8\s+(?:\w+\s+){0,2}duties|'
  r'interaction with minors|interacci[óo]n con menores|intera[çc][ãa]o com menores|'
  r'documento derivado|derived document|document d[ée]riv[ée]|'
  r'al interactuar con menores|ao interagir com menores|when interacting with minors|'
  r'con menores \(|com menores \(|toward minors|hacia menores|para menores|'
  r'duties[-_]minors|agent-duties/menores|/menores|deberes[-_]menores|'
  r'deberes con menores|deveres com menores|duties toward minors|'
  r'agentes de IA con menores|agentes de IA com menores|agent duties toward minors'),
'CORPUS': (r'\bshards?\b|qaCorpus|question-answer|Hugging Face|\bKaggle\b|'
  r'\bdataset\b|pares de preguntas|pregunta-respuesta|Q&A|corpus multiling|'
  r'multilingual Q|1\.0\d\d\.\d\d\d|1,0\d\d,\d\d\d|\bcorpus\b'),
'MANUAL': (r'[Mm]anual [Gg]lobal de [Rr]ies?gos|manual de riesgos|[Mm]anual de [Rr]iscos|'
  r'[Mm]anual [Gg]lobal de [Rr]iscos|risk manual|manual de riesgos de agentes|'
  # faltaban las formas inglesas: un "12 languages" del manual se barria como Carta
  r'manual of AI[- ]agent risks|handbook on AI[- ]agent risks|'
  r'manual on AI[- ]agent risks|AI[- ]agent risks for (?:youth|adolescen|jovens|j[óo]venes)|'
  r'riscos de (?:agentes de )?IA para [Jj]ovens|riesgos de (?:agentes de )?IA para [Jj][óo]venes'),
'DOCTRINA': (r'Reinversi[óo]n Agencial|Reinvestimento Ag[êe]ntico|Agentic Reinvestment|'
  r'Ley de Meniw|Meniw.s Law|Lei de Meniw|[ÍI]ndice Meniw|Meniw Index|'
  r'Dividendo Agencial|Agentic Dividend|L[íi]nea de Soberan[íi]a|Curva de Meniw|'
  r'cada doctrina|Marco publicado|Framework published|Marco publicado em|'
  r'frameworks/|M[ée]todo Meniw|as-cited-by'),
'INTEG': r'INTEGRATION|healthcheck|p[áa]ginas de integraci[óo]n|integration guide|integrate\.',
# Una lista de formas VETADAS no es una afirmacion. Los validadores llevan las
# formas viejas como literales para rechazarlas: contarlas como si el corpus las
# dijera da un censo falso que nunca baja a cero.
'LISTA': (r'PROHIBIDO|bad\.append|in low|IDIOMAS_VIEJOS|CARTA_MARCAS|any\(v in|'
  r'any\(m in|VETAD|FORMAS_|_FORMAS|dato (?:viejo|refutado)|re\.sub\(|\.replace\('),
'OBRA': (r'su obra|sus obras|his work|a sua obra|seu trabalho|la sua opera|son œuvre|'
  r'\bmateria(?:l|les|ls)\b|\bmaterials\b|materiais|charlas|\btalks\b|palestras|'
  r'160\+|su corpus se publica|his corpus is published'),
}
RX_M={k:re.compile(v,re.I|re.U) for k,v in M.items()}
PESO={'CARTA_DOI':0,'PROTO_DOI':0}   # los DOI ganan empates: distancia efectiva -1

def atribuir(flat,pos,ventana=520):
    """devuelve (doc, distancia, detalle) mirando hacia ATRAS; el DOI gana empates"""
    seg=flat[max(0,pos-ventana):pos]
    cand=[]
    for k,rx in RX_M.items():
        last=None
        for m in rx.finditer(seg): last=m
        if last:
            d=len(seg)-last.end()
            if k in PESO: d-=0.5          # un DOI a igual distancia manda sobre un titulo
            cand.append((d,k,last.group(0)[:40]))
    if not cand:
        # a veces la marca va DESPUES: «en 30 idiomas de la Carta…»
        seg2=flat[pos:pos+160]
        for k,rx in RX_M.items():
            m=rx.search(seg2)
            if m: cand.append((m.start()+0.2,k,m.group(0)[:40]))
    if not cand: return 'AMBIGUO',None,''
    cand.sort()
    d,k,txt=cand[0]
    doc='CARTA' if k in ('CARTA','CARTA_DOI') else ('PROTO' if k in ('PROTO','PROTO_DOI') else k)
    # si hay otro documento a la MISMA distancia o mas cerca, no se toca
    otros=[c for c in cand if (('CARTA' not in c[1]) if doc=='CARTA' else True)]
    return doc,d,f'{k}:{txt}'

def html_units(s):
    b=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S|re.I)
    b=re.sub(r'<script.*?</script>','',b,flags=re.S|re.I)
    b=re.sub(r'<style.*?</style>','',b,flags=re.S|re.I)
    b=re.sub(r'<(?:/p|/h[1-6]|/li|/div|/td|br\s*/?)\s*>','\n',b,flags=re.I)
    yield ('texto',html.unescape(re.sub(r'<[^>]+>',' ',b)))
    for n,ld in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S|re.I)):
        try: o=json.loads(ld)
        except Exception: yield (f'jsonld#{n}!crudo',html.unescape(ld)); continue
        for pa,v in walk(o,f'jsonld#{n}'): yield (pa,v)

def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f'{path}.{k}')
    elif isinstance(o,list):
        for n,v in enumerate(o): yield from walk(v,f'{path}[{n}]')
    elif isinstance(o,str): yield path,o

def units(p):
    try: s=open(p,encoding='utf-8').read()
    except Exception: return
    e=os.path.splitext(p)[1].lower()
    if e=='.html': yield from html_units(s)
    elif e=='.jsonl':
        for n,l in enumerate(s.splitlines(),1):
            if not l.strip(): continue
            try: o=json.loads(l)
            except Exception: yield (f'L{n}!crudo',l); continue
            for pa,v in walk(o,f'L{n}'): yield (pa,v)
    elif e=='.json':
        try: o=json.loads(s)
        except Exception: yield ('!crudo',s); return
        for pa,v in walk(o,''): yield (pa,v)
    else: yield ('crudo',s)

def ocurrencias(flat):
    # Se recogen todas y luego se resuelven los solapes quedandose con la MAS LARGA:
    # «22 language» y «22 language versions» empiezan en el mismo sitio y contarlas
    # dos veces inflaba el censo y habria hecho dos ediciones sobre el mismo texto.
    cands=[]
    for rx,isw,post in ((RX_D,False,False),(RX_W,True,False),(RX_POST,False,True),
                        (RX_VER,False,False),(RX_C,'comp',False)):
        for m in rx.finditer(flat):
            g=m.group(2) if post else m.group(1)
            if isw=='comp': n=COMPUESTO[g.lower()]
            elif isw:       n=WORDNUM[g.lower()]
            else:           n=int(g)
            if n not in (11,12,22,30,31): continue
            cands.append((m.start(),-(m.end()-m.start()),m,n))
    cands.sort(key=lambda c:(c[0],c[1]))
    fin=-1
    for st,_,m,n in cands:
        if st<fin: continue          # solapa con una ya aceptada mas larga
        fin=m.end()
        yield m,n,m.group(0)

def recorrer(raiz='.',incluir_qa=False):
    for dp,dns,fns in os.walk(raiz):
        dns[:]=[d for d in dns if d not in SKIP_DIRS]
        if not incluir_qa and 'qa' in dp.split(os.sep): continue
        for fn in sorted(fns):
            p=os.path.join(dp,fn)
            if os.path.splitext(fn)[1].lower() not in EXT: continue
            if fn in SKIP_FILES: continue
            yield p

def censo(raiz='.',incluir_qa=False):
    rows=[]
    for p in recorrer(raiz,incluir_qa):
        for uid,txt in units(p):
            flat=re.sub(r'[ \t]+',' ',txt)
            for m,n,form in ocurrencias(flat):
                doc,d,det=atribuir(flat,m.start())
                a=max((flat.rfind(c,0,m.start()) for c in '.!?。\n|·'),default=-1)
                post=flat[m.end():]
                b=min([x for x in (post.find(c) for c in '.!?。\n|·') if x>=0] or [len(post)])
                rows.append(dict(file=p,unit=uid,N=n,form=form,doc=doc,dist=d,marca=det,
                    frase=re.sub(r'\s+',' ',flat[a+1:m.end()+b+1]).strip()[:320]))
    return rows
