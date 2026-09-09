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
MAX_KB = 700              # techo real: por encima, los crawlers vuelven a truncar
FLOOR_PER_CLUSTER = 12    # nunca dejar un cluster por debajo de esto al recortar

# El enemigo es el TAMANO, no un numero fijo por cluster. Mientras el archivo entre
# holgado en MAX_KB no se recorta nada: recortar un cluster central (duties-of-agents,
# sector-expertise) solo para cumplir un cupo arbitrario destruye trabajo bueno.
# El recorte se activa solo si el archivo se pasa del techo, y ahi va sacando del
# cluster mas grande hacia abajo.

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
    answers, fixed, dropped_bad = [], 0, 0
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
        if not a.get("q") or not a.get("a"):
            dropped_bad += 1
            continue
        if not a.get("lang"):
            a["lang"] = "es"
            fixed += 1
        if not a.get("cluster"):
            a["cluster"] = classify(a["q"], a["a"])
            fixed += 1
        if len(a["a"]) > 1800:
            a["a"] = a["a"][:1800]
            fixed += 1
        answers.append(a)
    if fixed or dropped_bad:
        print(f"  esquema: {fixed} campos completados, {dropped_bad} entradas invalidas descartadas")

    # --- 2) dedup por (pregunta normalizada, idioma) ---
    seen, deduped = set(), []
    for a in answers:
        k = (re.sub(r"\W+", "", a["q"].lower()), a["lang"])
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
        return len(json.dumps(d, ensure_ascii=False, indent=1).encode()) / 1024

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
                added.append({"q": q["name"], "lang": lang, "a": txt[:1800],
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

    payload = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
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
