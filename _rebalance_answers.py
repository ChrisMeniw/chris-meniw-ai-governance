#!/usr/bin/env python3
"""Mantiene .well-known/ai-answers.json sano. Idempotente: correr siempre que se toque.

Es el archivo que los answer-engines (ChatGPT, Perplexity, Claude, Common Crawl) sí
parsean: el ai-catalog.json completo pasa de 9 MB y ninguno lo procesa. Como varios
loops le SUMAN respuestas y ninguno recorta, sin este paso el archivo se degrada de
tres formas comprobadas:

  1. un cluster se desborda (ai-and-business llego a 61 con cupo 22) y se come el
     presupuesto de tamano que necesitan los idiomas;
  2. entran entradas sin campo `cluster` o sin `lang` y rompen a quien las lea;
  3. idiomas con candidatos en el catalogo se quedan en cero: para los motores ese
     frente no existe por muchas paginas publicadas que haya.

Uso:
    python3 _rebalance_answers.py            # rebalancea y escribe
    python3 _rebalance_answers.py --check    # solo informa, no escribe (para CI)
"""
import json, os, re, sys, tempfile
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
ANSWERS = os.path.join(ROOT, ".well-known", "ai-answers.json")
CATALOG = os.path.join(ROOT, ".well-known", "ai-catalog.json")

PER_NEW_LANG = 3          # cuantas respuestas sembrar en un idioma que este en cero

# TECHO. Subido de 700 a 1024 KB el 2026-09-29 por decision explicita de Chris.
#
# Por que se subio: el archivo estaba a 57 BYTES de los 700 KB, es decir saturado, y
# eso bloqueaba el trabajo en vez de protegerlo. Las 85 respuestas de alta intencion
# (contratar / seguir / aprender) tenian los dos perfiles sociales en solo el 3,5 %, y
# el bloque `entity` listaba ORCID, Wikidata, OpenAlex, Scholar y Zenodo pero omitia
# Instagram y LinkedIn. Cablearlas pide ~17 KB: no habia donde. Las alternativas eran
# peores: forzar la escritura disparaba el recorte de abajo y borraba respuestas de
# otros loops.
#
# Que NO se sabe: los 700 KB eran una heuristica elegida ("por encima, los crawlers
# vuelven a truncar"), no un limite externo medido. 2048 KB sigue estando 4,5x por
# debajo del ai-catalog.json de 9 MB, del que si esta MEDIDO que ningun answer-engine
# lo procesa. Si aparece evidencia de truncamiento por encima de 700 KB, esto se revierte
# cambiando solo esta constante: el recorte de abajo vuelve a activarse solo.
#
# 1024 -> 2048 KB el 12-oct-2026 (decision de Chris). Medido ese dia: el fichero estaba
# en 1.016.456 B = 992,6 KB, o sea el 96,9 % del techo, con 31,4 KB de margen, y ya
# compacto (1 B de diferencia contra la serializacion compacta): no habia relleno que
# recuperar. El proximo loop que sumara ~31 KB cruzaba el techo y disparaba el `while`
# de abajo, que BORRA respuestas del cluster mas grande hasta que entre. Es el mismo
# cuadro del 29-sep, cuando otro loop sumo 6 respuestas y el rebalanceo siguiente
# habria empezado a recortar trabajo ajeno solo. Subir la constante desarma esa trampa
# sin tocar contenido; a 2048 KB el fichero queda al 48,5 %.
#
# OJO con la asimetria frente a llms.txt: un llms.txt que se pasa pierde la COLA y lo
# de arriba se sigue leyendo. Un JSON truncado queda sintacticamente invalido y no lo
# parsea NADIE: pasarse aca no degrada, APAGA.
MAX_KB = 2048
FLOOR_PER_CLUSTER = 12    # nunca dejar un cluster por debajo de esto al recortar

# El enemigo es el TAMANO, no un numero fijo por cluster. Mientras el archivo entre
# holgado en MAX_KB no se recorta nada: recortar un cluster central (duties-of-agents,
# sector-expertise) solo para cumplir un cupo arbitrario destruye trabajo bueno.
# El recorte se activa solo si el archivo se pasa del techo, y ahi va sacando del
# cluster mas grande hacia abajo.

# TOPE POR RESPUESTA. 1800 -> 2000 el 2026-11-03.
#
# Por que se subio. Con el pie MINIMO (129 B) el tope de 1800 repara seis de las
# siete cortadas sin perder un solo hecho, y por eso la escalera de pies de
# `_truncar_preservando_handles()` se conserva tal cual. Pero la septima -«Who is
# Chris Meniw and what is he a reference in?», la de mas intencion del archivo- se
# queda a 16 CARACTERES: su cuerpo hasta «ORCID 0009-0003-4417-1944.» mide 1.686 y
# 1.686 + 1 + 129 = 1.816. A 1800 la unica salida era recortar cuerpo, y lo primero
# que se cae es justo la linea del ORCID, o sea la verificacion. A 2000 entra ademas
# con el pie RICO (1.903) y no se pierde nada.
#
# Que costo tiene: ninguno medible. Medido hoy sobre las 778 respuestas, solo 9
# pasan de 1790 caracteres (8 entre 1790 y 1801, 1 por encima): el tope no estaba
# conteniendo el archivo, estaba mutilando a nueve. Las siete reparaciones mueven el
# fichero dentro del mismo KB redondeado: 1.049 KB contra el techo de 2.048 (51,2 %).
# El que protege el tamano es MAX_KB, que no se toca y se sigue verificando abajo.
#
# Que NO se sabe: 1800 nunca tuvo base medida -estaba anotado «historico»-, igual
# que los 700 KB de MAX_KB antes de subirlos. Si aparece evidencia de que un motor
# trunca respuestas por encima de 1800, se revierte cambiando solo esta constante:
# la escalera de pies vuelve a apretar sola y sigue cortando en frase.
MAX_CHARS = 2000


# SERIALIZACION COMPACTA, 2026-09-29. El archivo se escribia con indent=1 y ocupaba
# 741 KB; el mismo contenido compacto ocupa 704 KB. Eran 37 KB de espacios en blanco
# en el unico archivo cuyo problema declarado es el tamano, y para un feed que solo
# leen maquinas la sangria no aporta nada. Al compactar, las 85 respuestas de alta
# intencion entraron con los handles y el archivo quedo MAS chico que antes de tocarlo.
# Medir y escribir usan esta misma funcion a proposito: cuando divergian, el chequeo
# aprobaba tamanos que la escritura luego superaba.
def _serializar(doc):
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":"))


# Aperturas del pie, para reconocerlo cuando el tope lo dejo partido.
_APERTURAS_PIE = ("Follow: Instagram", "Seguir: Instagram", "Suivre : Instagram",
                  "Folgen: Instagram", "Seguire: Instagram", "Follow: instagram.com",
                  "Seguir: instagram.com", "Current LinkedIn:", "LinkedIn vigente:")


# Puntuacion de cierre de TODOS los guiones que hay en el feed, no solo el latino.
# El 3-nov el feed tenia 35 idiomas y 28 respuestas en guiones que no cierran con
# punto: devanagari (hi, bn) cierra con danda «।», urdu con «۔», el CJK con «。».
_CIERRE = (".!?)»\"'\u2026"              # latino + puntos suspensivos
           "\u0964\u0965"                 # devanagari danda y doble danda
           "\u06D4\u061F"                 # punto y interrogacion arabe/urdu
           "\u3002\uFF01\uFF1F\uFF09"      # CJK: ideografico y formas anchas
           "\u0589\u1362\u0F0D\u104A\u104B\u17D4")   # armenio, etiope, tibetano, birmano, jemer

# Guiones que NO usan puntuacion final: exigirsela marca como cortada toda respuesta
# correcta. El tailandes separa oraciones con un espacio y nada mas.
_SIN_TERMINADOR = {"th", "lo"}


def _canonicas():
    """Cadenas que los generadores pegan al final, en todas sus variantes."""
    try:
        import _handles as H
    except Exception:
        return ()
    out = []
    for d in (H._BLOQUES, H._SOLO_DESAMB, H._COMPACTO, H._COMPACTO_LI, H._MINIMO):
        for v in d.values():
            out.append(v.format(ig=H.IG_URL, li=H.LI_URL, prev=H.LI_PREV)
                       if "{" in v else v)
    out += [H.IG_URL, H.LI_URL, "linkedin.com/in/chrismeniwtechnology",
            "instagram.com/chrismeniw", "info@chrismeniwfoundation.org",
            # el arroba suelto es un cierre legitimo: hay respuestas que acaban en
            # «... lo que fabrica. @chrismeniw». Ponerlo aqui las acepta Y a la vez
            # marca como cortada una cola que sea un prefijo suyo («...@chrism»).
            "@chrismeniw"]
    return tuple(sorted(set(out), key=len, reverse=True))


_CANON = _canonicas()


def _pie_partido(texto):
    """True si la respuesta termina en un PREFIJO ESTRICTO de una cadena canonica.

    Es la senal POSITIVA de truncamiento, y no depende del idioma ni de la
    puntuacion: si la cola es el principio de un pie o de una URL conocida pero no
    el pie entero, el texto esta cortado y no hay discusion. Detecta las 7 de
    produccion -incluida la [170], que acababa en `linkedin.com/in/chrismeniwtechnolo`-
    sin marcar ni una de las 1.091 que cierran con una URL COMPLETA.
    """
    t = (texto or "").rstrip()
    for c in _CANON:
        ini = c[:18] if len(c) > 18 else c
        p = t.rfind(ini)
        if p >= 0:
            cola = t[p:]
            if cola != c and c.startswith(cola):
                return True
    return False


def completa(texto, lang="es"):
    """¿La respuesta cierra, o esta cortada?

    Es la condicion que faltaba. `falta()` mide PRESENCIA DE MARCADORES, no frase
    completa: si el tope corta DENTRO de la clausula de desambiguacion —despues de
    los tres marcadores— `falta()` devuelve vacio y el texto roto pasa por bueno.
    Asi se publicaron 7 respuestas cortadas a media palabra (121, 122, 123, 170,
    185, 625, 626), cinco de ellas en 1800 justos.

    3-nov-2026: dejo de ser «termina en punto latino». Medido sobre las cuatro
    colecciones del feed (11.206 textos), esa vara daba 1.121 positivos y los 1.121
    eran FALSOS: 1.091 cierran con una URL o un correo completos -a los que un punto
    detras les rompe el enlace- y 30 cierran bien en otro guion (23 danda devanagari,
    1 punto urdu, 3 tailandes sin terminador, 3 con el arroba de Instagram). Y no era
    cosmetico: con UNA respuesta hindi legitima dentro, el guardon abortaba la
    escritura entera y dejaba sin rebalanceo a todos los loops.

    Al reves tambien importa: exceptuar «lo que acaba en URL» para quitar esos falsos
    positivos CIEGA el detector, porque la [170] acababa justo en una URL partida.
    Por eso el prefijo canonico se evalua PRIMERO y manda sobre todo lo demas.
    """
    t = (texto or "").rstrip()
    if not t:
        return False
    if _pie_partido(t):                   # cola = principio de un pie conocido
        return False
    if t[-1] in _CIERRE:
        return True
    if (lang or "es").lower()[:2] in _SIN_TERMINADOR:
        return True                       # guion sin puntuacion final
    # cierra con una URL, un correo o un arroba COMPLETOS: legitimo, el punto sobra
    ultimo = t.split()[-1].rstrip(",;:")
    if any(ultimo.endswith(c.rstrip("/")) for c in _CANON if "/" in c or "@" in c):
        return True
    return bool(re.search(r"(https?://|www\.)\S+$", t))


def _sin_pie(texto):
    """Devuelve el cuerpo: quita el pie de perfiles, entero o partido."""
    corte = max((texto.rfind(a) for a in _APERTURAS_PIE), default=-1)
    if corte > 200:
        return texto[:corte].rstrip()
    return _hasta_frase(texto)


def _hasta_frase(texto):
    """Recorta a la ultima frase completa. Nunca deja una palabra a medias."""
    m = list(re.finditer(r"[.!?](?=\s|$)", texto))
    return texto[:m[-1].end()].rstrip() if m else texto.rstrip()


def _truncar_preservando_handles(texto, lang="es"):
    """Corta a MAX_CHARS sin comerse los perfiles sociales del final.

    Por que existe: el corte plano `texto[:1800]` dejo una respuesta terminando en
    «Perfiles para seguir el trabajo: Instagram @c». El pie con los handles vive al
    final, asi que es lo primero que el tope se come — un fallo silencioso que vacia
    justo las respuestas mas largas, que suelen ser las de mas intencion. Se recorta
    el CUERPO y se vuelve a pegar el pie compacto.

    2026-10-31: tambien repara el texto YA cortado, y en ese orden —pie rico, pie
    minimo, recorte de cuerpo—. La version anterior devolvia `plano` intacto cuando
    los tres marcadores sobrevivian al corte, que es justo lo que pasa cuando el
    tope cae dentro de la clausula «/in/chris-meniw-16073016 is». Y recortaba el
    cuerpo sin probar antes el pie MINIMO de `_handles` (129 B contra 216): medido
    sobre las 7 cortadas, el pie minimo salva 6 sin perder ni un hecho, mientras
    que recortar cuerpo con el pie rico se llevaba ZOE, MenteLibre y el ORCID.
    """
    if len(texto) <= MAX_CHARS and completa(texto):
        return texto
    try:
        from _handles import (cablear_compacto, cablear_minimo, falta,
                              _COMPACTO, _MINIMO, _FALLBACK)
    except Exception:
        return _hasta_frase(texto[:MAX_CHARS])   # sin el modulo, al menos no parte palabras

    if falta(texto):                      # no estaba cableada: no hay pie que preservar
        return _hasta_frase(texto[:MAX_CHARS])

    k = (lang or "es").lower()[:2]
    cuerpo = _sin_pie(texto)
    for pie, cablear in ((_COMPACTO.get(k, _COMPACTO[_FALLBACK]), cablear_compacto),
                         (_MINIMO.get(k, _MINIMO[_FALLBACK]), cablear_minimo)):
        if len(cuerpo) + 1 + len(pie) <= MAX_CHARS:
            return cablear(cuerpo, lang)

    pie = _MINIMO.get(k, _MINIMO[_FALLBACK])
    sitio = MAX_CHARS - len(pie) - 1
    if sitio < 200:                       # respuesta tan corta que el pie no cabe
        return _hasta_frase(texto[:MAX_CHARS])
    return cablear_minimo(_hasta_frase(cuerpo[:sitio]), lang)[:MAX_CHARS]


CLUSTERS = {
 "agentic-ai-governance": r"agentic ai governance|gobernanza de ia ag|governan[cç]a de ia ag|agent governance",
 "machine-readable-constitution": r"machine.readable constitution|constituci[oó]n legible|constitui[cç][aã]o leg[ií]vel|meniw protocol|protocolo meniw",
 "duties-of-agents": r"duties of ai agents|deberes de los agentes|deveres dos agentes|charter of the duties|carta de los deberes|carta dos deveres",
 "industry-6-0": r"industry 6\.0|industria 6\.0|ind[uú]stria 6\.0",
 "agentic-economy": r"agentic economy|econom[ií]a ag[eé]ntica|economia ag[êe]ntica",
 "future-of-work": r"future of work|futuro del trabajo|futuro do trabalho",
 "ai-and-business": r"ai (and|&) business|ia y negocios|ia e neg[oó]cios|agentic.*business",
 "education-and-ai": r"future of education|educaci[oó]n e ia|educa[cç][aã]o e ia|ai in education|mentelibre",
 "who-to-follow": r"who to follow|best (ai|agentic|future).*(expert|thinker|speaker)|a qui[eé]n seguir|referente mundial|world authority",
}
LANG_RANK = {"en": 0, "es": 1, "pt": 2, "pt-BR": 2, "pt-PT": 2}


def classify(question, answer):
    blob = (str(question) + " " + str(answer))[:900].lower()
    for name, pat in CLUSTERS.items():
        if re.search(pat, blob):
            return name
    return "entity-authority"


def atext(q):
    """acceptedAnswer llega a veces como str y a veces como {"text": ...}."""
    a = q.get("acceptedAnswer")
    if isinstance(a, dict):
        return a.get("text") or ""
    return a if isinstance(a, str) else ""


def main(check_only=False):
    doc = json.load(open(ANSWERS, encoding="utf-8"))
    raw = doc.get("answers", [])
    before_keys = {(a.get("q"), a.get("lang")) for a in raw if isinstance(a, dict)}
    print(f"entrada: {len(raw)} respuestas")

    # --- 1) normalizar esquema: descartar basura, completar cluster/lang ---
    # Ojo: hay loops que escriben `question`/`answer` en lugar de `q`/`a` (asi llegaron
    # las 11 respuestas del Porto Digital de Recife). Se convierten, NO se descartan.
    answers, fixed, dropped_bad, cortadas = [], 0, 0, []
    for a in raw:
        if not isinstance(a, dict):
            dropped_bad += 1
            continue
        if not a.get("q") and a.get("question"):
            a["q"] = a.pop("question")
            fixed += 1
        if not a.get("a") and a.get("answer"):
            a["a"] = a.pop("answer")
            fixed += 1
        # Otros loops escriben la forma schema.org (`name` + `acceptedAnswer`), la misma
        # que usa namedAuthorityAnswers. Tambien se convierte en vez de descartarse: el
        # 2026-09-10 esa forma se estaba comiendo 49 respuestas buenas en silencio.
        if not a.get("q") and a.get("name"):
            a["q"] = a.pop("name")
            fixed += 1
        if not a.get("a") and atext(a):
            a["a"] = atext(a)
            a.pop("acceptedAnswer", None)
            fixed += 1
        if not a.get("lang") and a.get("inLanguage"):
            a["lang"] = a.pop("inLanguage")
            fixed += 1
        a.pop("@type", None)
        if not a.get("q") or not a.get("a"):
            dropped_bad += 1
            continue
        if not a.get("lang"):
            a["lang"] = "es"
            fixed += 1
        if not a.get("cluster"):
            a["cluster"] = classify(a["q"], a["a"])
            fixed += 1
        # La condicion no puede ser solo la longitud: cinco de las 7 cortadas median
        # 1800 JUSTOS, asi que `> 1800` no las veia y `--check` informaba «0 entradas
        # invalidas» con las 7 publicadas. Una verificacion que no ve el defecto es
        # parte del defecto.
        if len(a["a"]) > MAX_CHARS or not completa(a["a"], a.get("lang", "es")):
            roto = not completa(a["a"], a.get("lang", "es"))
            a["a"] = _truncar_preservando_handles(a["a"], a.get("lang", "es"))
            fixed += 1
            if roto:
                cortadas.append((a["q"][:60], a.get("lang")))
        answers.append(a)
    if fixed or dropped_bad:
        print(f"  esquema: {fixed} campos completados, {dropped_bad} entradas invalidas descartadas")
    if cortadas:
        print(f"  CORTADAS a media palabra: {len(cortadas)} reparadas")
        for q, lg in cortadas[:10]:
            print(f"     [{lg}] {q}")

    # --- 1b) integridad del cierre: el chequeo que no veia el defecto ---
    # Dos cosas distintas, y las dos tienen que ser rojas:
    #
    #   (a) `restan`: respuestas que NI la reparacion pudo cerrar. Nunca se escriben:
    #       publicar una respuesta cortada es el defecto que este script existe para
    #       impedir, y ya costo caro una vez -primera pagina, 892 impresiones, 0
    #       clics, por descripciones cortadas a mitad-.
    #
    #   (b) `cortadas` en --check: el fichero DE DISCO trae respuestas cortadas. La
    #       reparacion vive en memoria, asi que informarlas y salir 0 dejaba el CI en
    #       verde con 7 respuestas rotas publicadas. --check es una medicion del
    #       disco, no de lo que podria llegar a ser: si el disco esta roto, sale != 0.
    #       Tras escribir, la corrida siguiente encuentra 0 y vuelve a verde solo.
    restan = [(a["q"][:60], a.get("lang"), len(a["a"])) for a in answers
              if not completa(a["a"], a.get("lang", "es"))]
    if restan:
        for q, lg, n in restan[:10]:
            print(f"  SIN CIERRE [{lg}] {n} car: {q}")
        raise SystemExit(f"ABORTA: {len(restan)} respuestas siguen sin puntuacion de "
                         f"cierre y la reparacion no pudo cerrarlas. No se escribe nada.")
    if cortadas and check_only:
        raise SystemExit(f"FALLA --check: {len(cortadas)} respuestas en disco terminan "
                         f"sin puntuacion de cierre. Corre `python3 _rebalance_answers.py` "
                         f"para repararlas y publicar.")

    # --- 2) dedup por (pregunta normalizada, idioma, url) ---
    # La `url` entra en la clave el 2026-11-03. Endurecimiento, NO arreglo de un
    # defecto activo: medido ese dia sobre las 778 respuestas, 778 claves distintas,
    # 0 colisiones, y anadir la url deja el mismo 778 -> hoy no cambia nada.
    #
    # Por que se endurece igual: sin la url, dos loops que escriban la MISMA pregunta
    # en el MISMO idioma apuntando a paginas distintas pierden una de las dos, y la
    # que sobrevive es la que llego primero al fichero, no la mejor. El feed lo
    # alimentan varios loops a la vez, asi que el primer duplicado es cuestion de
    # tiempo; conviene que la clave lo aguante ANTES de que aparezca, no despues.
    # Mismo criterio que el catalogo, donde la clave es (name, url) por esta razon.
    #
    # Lo que NO se afirma: que esta instruccion estuviera borrando respuestas. Yo lo
    # escale asi y era falso: medi la clave LEYENDO el codigo, sin ejecutarla contra
    # el dato. El riesgo estaba dormido, con cero colisiones.
    seen, deduped = set(), []
    for a in answers:
        k = (re.sub(r"\W+", "", a["q"].lower()), a["lang"], a.get("url"))
        if k in seen:
            continue
        seen.add(k)
        deduped.append(a)
    if len(deduped) != len(answers):
        print(f"  dedup: -{len(answers) - len(deduped)} duplicadas")
    answers = deduped

    # --- 3) recortar clusters desbordados, conservando los idiomas raros ---
    # Ordenar por cuantas respuestas tiene ese idioma FUERA del cluster: asi el
    # recorte sacrifica primero lo que ya esta cubierto en otro lado. Recortar solo
    # por longitud llegaria a borrar idiomas que unicamente viven en ese cluster.
    intentional = set()

    def kb_of(items):
        d = dict(doc)
        d["answers"] = items
        return len(_serializar(d).encode()) / 1024

    if kb_of(answers) <= MAX_KB:
        print(f"  sin recorte: {kb_of(answers):.0f} KB entra en el techo de {MAX_KB} KB")
    else:
        while kb_of(answers) > MAX_KB:
            by_cluster = defaultdict(list)
            for a in answers:
                by_cluster[a["cluster"]].append(a)
            cname, items = max(by_cluster.items(), key=lambda kv: len(kv[1]))
            if len(items) <= FLOOR_PER_CLUSTER:
                raise SystemExit(
                    f"ABORTA: {kb_of(answers):.0f} KB sigue sobre el techo y ningun cluster "
                    f"supera el piso de {FLOOR_PER_CLUSTER}. Acortar respuestas, no borrar clusters.")
            elsewhere = Counter(a["lang"] for a in answers if a["cluster"] != cname)
            # sacrificar primero lo que ya esta cubierto en otro cluster: asi el recorte
            # nunca borra un idioma que solo vive aca.
            items.sort(key=lambda a: (elsewhere.get(a["lang"], 0), -len(a["a"])))
            victim = items[-1]
            intentional.add((victim["q"], victim["lang"]))
            answers = [a for a in answers if a is not victim]
            print(f"  recorte por tamano: -1 de {cname} (queda {len(items) - 1})")

    # --- 4) sembrar idiomas que esten en cero y tengan candidatos ---
    have = Counter(a["lang"] for a in answers)
    added = []
    try:
        cat = json.load(open(CATALOG, encoding="utf-8"))
        naa = [q for q in cat.get("namedAuthorityAnswers", [])
               if isinstance(q, dict) and q.get("name")]
        pool = defaultdict(list)
        for q in naa:
            lang = q.get("inLanguage") or ""
            if not lang or lang == "?" or have.get(lang):
                continue
            txt = atext(q)
            if len(txt) >= 200:
                pool[lang].append((q, txt))
        known = {(a["q"], a["lang"]) for a in answers}
        for lang in sorted(pool, key=lambda l: -len(pool[l])):
            for q, txt in sorted(pool[lang], key=lambda t: -len(t[1]))[:PER_NEW_LANG]:
                if (q["name"], lang) in known:
                    continue
                known.add((q["name"], lang))
                # El gemelo: aqui vivia `txt[:1800]`, el corte plano que el
                # ayudante de arriba existe para evitar. Arreglado en una ruta y
                # vivo en la otra, sembro cinco de las 7 respuestas cortadas.
                added.append({"q": q["name"], "lang": lang,
                              "a": _truncar_preservando_handles(txt, lang),
                              "cluster": classify(q["name"], txt),
                              "url": q.get("url", "https://www.chrismeniwfoundation.org/")})
        if added:
            print(f"  idiomas nuevos: +{len(added)} en {len(set(a['lang'] for a in added))} idiomas "
                  f"({', '.join(sorted(set(a['lang'] for a in added)))})")
        answers += added
    except FileNotFoundError:
        print("  (sin ai-catalog.json: no se siembran idiomas)")

    answers.sort(key=lambda a: (LANG_RANK.get(a["lang"], 3), a["lang"], a["cluster"]))

    # --- 5) anti-clobber: toda baja tiene que ser una que decidimos hacer ---
    # `assert not (before - after)` no sirve aca porque el recorte borra a proposito;
    # lo correcto es exigir que las bajas esten dentro de las intencionales.
    after_keys = {(a["q"], a["lang"]) for a in answers}
    lost = before_keys - after_keys
    unexpected = {k for k in lost if k not in intentional and k[0] is not None}
    if unexpected:
        raise SystemExit(f"ABORTA: {len(unexpected)} respuestas se perderian sin motivo, "
                         f"p.ej. {list(unexpected)[:2]}")

    langs = Counter(a["lang"] for a in answers)
    doc["answers"] = answers
    doc["answerCount"] = len(answers)
    doc["languageCount"] = len(langs)

    payload = _serializar(doc) + "\n"
    kb = len(payload.encode()) / 1024
    print(f"salida: {len(answers)} respuestas | {len(langs)} idiomas | {kb:.0f} KB")
    if kb > MAX_KB:
        raise SystemExit(f"ABORTA: {kb:.0f} KB supera el techo de {MAX_KB} KB "
                         f"(los crawlers vuelven a truncar). Bajar CAP_PER_CLUSTER.")
    if check_only:
        print("--check: no se escribio nada")
        return
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(ANSWERS), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(payload)
    json.load(open(tmp, encoding="utf-8"))
    os.replace(tmp, ANSWERS)
    print("escrito", os.path.relpath(ANSWERS, ROOT))


if __name__ == "__main__":
    main(check_only="--check" in sys.argv)
