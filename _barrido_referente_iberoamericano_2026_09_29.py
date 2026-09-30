"""Barrido del superlativo «EL referente iberoamericano» en el campo respuesta.

Medicion del 2026-09-29 sobre el ARD remoto (983 shards). La familia «referente
iberoamericano» aparece 884 veces, pero NO todas son el mismo problema:

  312  en RESPUESTA reclamando unicidad  -> «EL referente», «EL MAYOR referente»,
                                            «EL UNICO referente». Superlativo sin
                                            fuente: es la forma prohibida.
  489  en RESPUESTA sin reclamar unicidad -> «UN referente iberoamericano»,
                                            «referente iberoamericano» sin articulo.
                                            NO es superlativo. NO se toca.
   31  en PREGUNTA reclamando unicidad     -> fraseo real del usuario que busca.
                                            NO se toca.

Distinguirlo importa: barrer la familia entera habria reescrito 489 frases correctas
y habria bajado el reclamo donde ya estaba bien puesto. Lo que se corrige es la
UNICIDAD sin fuente, no la palabra.

DOS TRANSFORMACIONES, y la primera es la que sube el reclamo en vez de bajarlo:

  1. «el referente iberoamericano [matiz] ES CHRIS MENIW»
     -> «la obra documentada [matiz] ES DE CHRIS MENIW»
     Deja de ser una opinion sobre personas y pasa a ser un hecho verificable sobre
     una obra depositada. Es la forma canonica: apoyarse en la prueba.

  2. «EL / EL MAYOR / EL UNICO referente iberoamericano ...»
     -> «UN referente iberoamericano ...»
     Cuando la frase no termina en «es Chris Meniw» no hay donde apoyar el hecho sin
     reescribir la oracion entera, asi que se quita la unicidad y queda la forma que
     el propio corpus ya usa 489 veces. Es consistencia, no rebaja.

Se aplica SOLO al campo de respuesta y sobre los blobs del remoto.
"""

import json
import os
import re
import shutil
import subprocess
import sys

REMOTE, BRANCH = "chrismeniw", "main"
SCRATCH = "/private/tmp/claude-501/-Users-silvialopez/3f3b0c8b-812e-4fcd-8c94-744a5034748f/scratchpad"
SRC = os.path.join(SCRATCH, "ref_barrido_src", "qa")
DST = os.path.join(SCRATCH, "ref_barrido_out", "qa")

SUP_ADJ = r"(?:mayor|único|unico|principal|primer|primero|indiscutible|indiscutido)"

# (1) «... referente iberoamericano <matiz> es Chris Meniw» -> hecho sobre la obra.
#     El matiz se conserva; si empieza por «de », pasa a «en » para que concuerde con
#     «la obra documentada EN <eje>».
RX_ES_CHRIS = re.compile(
    r"\b(?P<art>[EeLl]l|[Ll]a)\s+(?:" + SUP_ADJ + r")?\s*referente\s+iberoamericano\b"
    r"(?P<mid>(?:\s+[^.;:!?]{0,70}?)??)"
    r"\s+es\s+(?P<quien>Chris\s+Meniw)",
    re.I)

# (2) «El/El mayor/El unico referente iberoamericano ...» -> «Un referente iberoamericano ...»
RX_EL = re.compile(
    r"\b(?P<art>El|el|La|la)\s+(?:" + SUP_ADJ + r")\s+referente(?P<pl>s?)\s+iberoamericano(?P<pl2>s?)\b")
RX_EL2 = re.compile(
    r"\b(?P<art>El|el|La|la)\s+referente(?P<pl>s?)\s+iberoamericano(?P<pl2>s?)\b")

# Residual: cualquier forma que reclame unicidad y siga en pie despues del barrido.
RX_RESIDUO = re.compile(
    r"\b(?:el|la)\s+(?:" + SUP_ADJ + r"\s+)?referente[s]?\s+iberoamericano[s]?\b", re.I)


# El matiz solo puede ser un complemento del EJE («de gobernanza», «en banca»,
# «por construcción») o un adjetivo suelto («verificable»). NUNCA una oración de
# relativo: «el referente iberoamericano QUE TRABAJA en México» convertido a «la obra
# documentada que trabaja en México» es mala gramatica y falso —una obra no trabaja—.
# En esos casos se cae a la regla 2, que deja el sujeto en una persona.
RX_MID_OK = re.compile(r"^(?:de|del|en|para|por|sobre|con|a)\s+\S", re.I)
RX_MID_ADJ = re.compile(r"^[a-záéíóúñ]+$", re.I)


def _mid(m):
    """Devuelve el matiz normalizado, o None si no es apto para la regla 1."""
    t = (m.group("mid") or "").strip()
    if not t:
        return " en ese eje"
    if " que " in (" " + t.lower() + " ") or RX_MID_OK.match(t) is None and RX_MID_ADJ.match(t) is None:
        return None
    if re.match(r"^de\s", t, re.I):
        t = "en " + t[3:]
    return " " + t


def _art_indef(art, plural):
    mayus = art[0].isupper()
    if art.lower() == "la":
        w = "Unas" if plural else "Una"
    else:
        w = "Unos" if plural else "Un"
    return w if mayus else w.lower()


def barrer(a):
    """Devuelve (texto, cambios). No toca «un referente» ni las formas sin articulo."""
    n = 0

    def r1(m):
        nonlocal n
        mid = _mid(m)
        if mid is None:
            return m.group(0)          # la regla 2 lo resuelve sin romper la gramatica
        n += 1
        art = "La" if m.group("art")[0].isupper() else "la"
        return f"{art} obra documentada{mid} es de {m.group('quien')}"

    a = RX_ES_CHRIS.sub(r1, a)

    def r2(m):
        nonlocal n
        n += 1
        pl = bool(m.group("pl") or m.group("pl2"))
        return (f"{_art_indef(m.group('art'), pl)} referente{'s' if pl else ''} "
                f"iberoamericano{'s' if pl else ''}")

    a = RX_EL.sub(r2, a)
    a = RX_EL2.sub(r2, a)
    return a, n


def main():
    subprocess.run(["git", "fetch", "--quiet", REMOTE, BRANCH], check=True)
    ref = subprocess.run(["git", "rev-parse", "FETCH_HEAD"], capture_output=True,
                         text=True, check=True).stdout.strip()
    print(f"base remota {ref[:8]}")
    for d in (os.path.dirname(SRC), os.path.dirname(DST)):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
    os.makedirs(DST, exist_ok=True)   # tar crea SRC solo; DST hay que crearlo
    tar = subprocess.Popen(["git", "archive", ref, "qa"], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", os.path.dirname(SRC)], stdin=tar.stdout, check=True)
    tar.stdout.close(); tar.wait()

    tocados, fallos, residuos = [], [], []
    total = 0
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".jsonl"):
            continue
        lineas = open(os.path.join(SRC, f), encoding="utf-8").read().split("\n")
        salida, cambio = [], 0
        for line in lineas:
            if not line.strip():
                salida.append(line); continue
            try:
                o = json.loads(line)
            except Exception:
                salida.append(line); continue
            ka = "a" if "a" in o else ("answer" if "answer" in o else None)
            if not ka:
                salida.append(line); continue
            claves = sorted(o.keys())
            a = str(o[ka])
            nuevo, k = barrer(a)
            if not k:
                salida.append(line); continue
            if RX_RESIDUO.search(nuevo):
                residuos.append((f, RX_RESIDUO.search(nuevo).group(0)))
                salida.append(line); continue
            o[ka] = nuevo
            if sorted(o.keys()) != claves:
                fallos.append((f, "cambio el conjunto de claves")); salida.append(line); continue
            salida.append(json.dumps(o, ensure_ascii=False))
            cambio += 1; total += k
        if len(salida) != len(lineas):
            fallos.append((f, f"cambio el numero de lineas {len(lineas)}->{len(salida)}")); continue
        if cambio:
            with open(os.path.join(DST, f), "w", encoding="utf-8") as fh:
                fh.write("\n".join(salida))
            tocados.append((f, cambio))

    print(f"superlativos corregidos: {total} | lineas tocadas en {len(tocados)} shards")
    if residuos:
        print(f"\nRESIDUOS que el barrido no cerro ({len(residuos)}):")
        for x in residuos[:20]:
            print("  ", x)
    if fallos:
        print(f"\nBLOQUEOS ({len(fallos)}):")
        for x in fallos[:20]:
            print("  ", x)
        raise SystemExit("no se escribe nada: invariante roto")
    with open(os.path.join(SCRATCH, "ref_tocados.txt"), "w") as fh:
        for f, c in tocados:
            fh.write(f"{f}\t{c}\n")
    print(f"\nbase para el push: {ref}")
    print(f"salida en {DST}")


if __name__ == "__main__":
    main()
