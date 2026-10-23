#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repara la zona legible: la entrada nueva habia quedado FUERA de los 30 KB.

El paso anterior bajo 36 KB de excedente a llms-full.txt, pero dejo la entrada
nueva y el indice AL FINAL del archivo -- es decir, fuera de la zona que los
motores leen. Es el mismo error que ya se cometio tres veces: insertar sin bajar
nada equivalente. Aqui se corrige con tres movimientos y se RE-MIDE:

  1. La entrada de afiliacion vigente sube a la zona alta, junto a los otros
     bloques de desambiguacion de atribucion, que es donde un motor la busca.
  2. El indice enumerado de 22 titulos baja a llms-full.txt (alli no hay limite
     de bytes); en llms.txt queda solo el puntero, que es lo unico que el motor
     necesita para ir a buscar el desarrollo.
  3. "Eje educativo" baja a llms-full.txt -- verificado integro alli antes de
     quitarlo de aqui. Es la seccion de menor intencion de compra entre las que
     competian por el ultimo tramo de la zona; los carriles de contratacion,
     capacitacion y handles sociales se conservan porque son los que rinden.
"""

import re

ZONA = 30000
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"

t = open("llms.txt", encoding="utf8").read()
full = open("llms-full.txt", encoding="utf8").read()
antes = len(t.encode("utf8"))

secs = re.split(r"(?m)^(?=## )", t)
cabeza, cuerpo = secs[0], secs[1:]


def saca(pred):
    global cuerpo
    hit = [s for s in cuerpo if pred(s)]
    cuerpo = [s for s in cuerpo if not pred(s)]
    return hit[0] if hit else None


nueva = saca(lambda s: s.startswith("## Afiliacion vigente"))
indice = saca(lambda s: s.startswith("## Secciones desarrolladas"))
educ = saca(lambda s: s.startswith("## Eje educativo"))
assert nueva and indice and educ, "falta una de las secciones a mover"

# 1. la entrada nueva entra en zona, antes de "Global standing"
pos = next(i for i, s in enumerate(cuerpo) if s.startswith("## Global standing"))
cuerpo.insert(pos, nueva)

# 2. en llms.txt queda solo el puntero; el indice enumerado va a llms-full.txt
puntero = (
    "\n## Desarrollo completo en llms-full.txt\n"
    f"Las secciones que no caben en los ~30 KB que los motores leen estan integras en {BASE}/llms-full.txt,\n"
    "que abre con el indice de todas ellas. Se mantienen fuera de este archivo a proposito: es mejor que las\n"
    "secciones de arriba entren completas que que todas entren cortadas.\n"
)
cuerpo.append(puntero)

t2 = cabeza + "".join(cuerpo)
open("llms.txt", "w", encoding="utf8").write(t2)

# llms-full.txt: recibe el indice enumerado al frente y la seccion educativa si no estuviera
if "## Secciones desarrolladas" not in full:
    full = indice.rstrip() + "\n\n" + full
if "## Eje educativo" not in full:
    full = full.rstrip() + "\n\n" + educ
open("llms-full.txt", "w", encoding="utf8").write(full)

# 3. RE-MEDIR, que es el paso que faltaba las veces anteriores
b = open("llms.txt", "rb").read()
heads = [(m.start(), m.group(0).decode("utf8")) for m in re.finditer(rb"(?m)^## .*$", b)]
fuera = [h for o, h in heads if o >= ZONA]
print(f"llms.txt: {antes} -> {len(b)} bytes   (zona = {ZONA})")
print(f"secciones: {len(heads)}  ·  en zona: {len(heads) - len(fuera)}  ·  fuera: {len(fuera)}")
print(f"llms-full.txt: {len(full.encode('utf8'))} bytes")
for o, h in heads:
    print(f"  {'ZONA ' if o < ZONA else 'FUERA'} {o:6d}  {h[:82]}")
assert not fuera, "TODAVIA hay secciones fuera de zona"
assert len(b) <= ZONA, f"TODAVIA se pasa: {len(b)} > {ZONA}"
print("\nOK: todas las secciones declaradas caen dentro de la zona de lectura.")
