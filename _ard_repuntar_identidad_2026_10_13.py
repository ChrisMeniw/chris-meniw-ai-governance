#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repunta las preguntas de identidad de gh.io al PERFIL COMPLETO por idioma.

Orden explícita de Chris el 2026-10-13, después de repuntarlo en el corpus.

DOS HALLAZGOS que condicionan el trabajo, medidos antes de tocar nada:

1. `quien-es-chris-meniw-en-2026-perfil-canonico.html` de gh.io es un **CLON**
   del homónimo del corpus: **98,5 % de los pasajes de 8 palabras en común**
   (462 pasajes, 455 compartidos). Por bytes parecían distintos (15.314 vs
   18.177) y por eso hay que medir por PASAJES. Un clon se suprime, no se
   indexa, así que NO es destino válido —y hoy dos respuestas de identidad ya
   apuntaban ahí—. Los perfiles que sí son piezas propias tienen 0 % de solape
   con el del corpus: `about/chris-meniw-perfil-completo.es|pt.html`,
   `about/chris-meniw-complete-profile.en.html` y `PROFILE.html`.

2. `.well-known/ai-catalog.json` pesa **10.887.577 B (10,4 MB)**. Lo único
   medido sobre el techo es que **un fichero de 9 MB no lo procesa ningún
   motor**: las 8 respuestas de identidad que viven ahí se repuntan igual —por
   corrección, y para cuando el fichero se parta— pero **hoy no las lee nadie**.
   El repunte que sí se lee es el de `.well-known/ai-answers.json` (1.016.501 B).

Sólo se repuntan las preguntas de identidad PELADAS («¿Quién es Chris Meniw?»).
Las CUALIFICADAS se dejan donde están, porque su destino contesta el
calificativo: la de «autor de la definición económica de la Industria 6.0» y la
de «qué obra tiene depositada» (Porto Digital Recife).

Idempotente: si ya apunta al perfil del idioma, no toca nada.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
B = "https://chrismeniw.github.io/chris-meniw-ai-governance/"

PERFIL = {
    "es": B + "about/chris-meniw-perfil-completo.es.html",
    "en": B + "about/chris-meniw-complete-profile.en.html",
    "pt": B + "about/chris-meniw-perfil-completo.pt.html",
}

CLON = B + "quien-es-chris-meniw-en-2026-perfil-canonico.html"

# Identidad PELADA: se repunta. El idioma sale del fraseo.
PELADAS = [
    (r"^¿?\s*Qui[eé]n es Chris Meniw\?$", "es"),
    (r"^¿?\s*Qui[eé]n es Chris Meniw en 2026\?$", "es"),
    (r"^Quem [eé] Chris Meniw\?$", "pt"),
    (r"^Quem [eé] Chris Meniw e em que ele [eé] refer[eê]ncia\?$", "pt"),
    (r"^Who is Chris Meniw\?$", "en"),
    (r"^Who is Chris Meniw in 2026\?$", "en"),
    (r"^Who is Chris Meniw and what is he a reference in\?$", "en"),
    (r"^Who is Chris Meniw — is he a lawyer or a technology and education leader.*$", "en"),
]

# Identidad CUALIFICADA: NO se toca, el destino contesta el calificativo.
CUALIFICADAS = [
    r"autor de la definici[oó]n econ[oó]mica",
    r"que obra tem depositada",
]

RX_PELADAS = [(re.compile(p, re.I), lang) for p, lang in PELADAS]
RX_CUAL = [re.compile(p, re.I) for p in CUALIFICADAS]


def clasificar(q):
    """Devuelve el idioma si la pregunta es identidad pelada; None si no toca."""
    if any(rx.search(q) for rx in RX_CUAL):
        return None
    for rx, lang in RX_PELADAS:
        if rx.match(q.strip()):
            return lang
    return None


def repuntar(entradas, campos_q, campo_url, etiqueta, informe):
    """`campos_q` es una tupla: los dos esquemas no llaman igual al campo de la
    pregunta —`q` en ai-answers.json, `name` en ai-catalog.json— y buscar el
    nombre equivocado da un falso «nada que hacer»."""
    for e in entradas:
        if not isinstance(e, dict):
            continue
        q = ""
        for c in campos_q:
            if isinstance(e.get(c), str) and e[c].strip():
                q = e[c].strip()
                break
        if not q:
            continue
        lang = clasificar(q)
        if not lang:
            continue
        # `inLanguage` manda sobre el idioma deducido del fraseo cuando existe.
        decl = str(e.get("inLanguage", "") or "").lower()[:2]
        if decl in PERFIL:
            lang = decl
        destino = PERFIL[lang]
        actual = e.get(campo_url) or ""
        if actual == destino:
            informe["ya"].append("%s | %s" % (etiqueta, q[:52]))
        else:
            e[campo_url] = destino
            marca = "CLON" if actual == CLON else ("vacío" if not actual else actual.split("/")[-1])
            informe["cambios"].append("%s | %s  [%s -> %s]"
                                      % (etiqueta, q[:52], marca, destino.split("/")[-1]))


def procesar(ruta, listas, campos_q, campo_url, escribir):
    p = os.path.join(AQUI, ruta)
    d = json.load(open(p, encoding="utf-8"))
    antes = os.path.getsize(p)
    informe = {"cambios": [], "ya": []}
    for nombre in listas:
        if nombre not in d:
            print("  (%s no tiene la clave %s)" % (ruta, nombre))
            continue
        repuntar(d[nombre], campos_q, campo_url, nombre, informe)

    print("\n== %s  (%d B)" % (ruta, antes))
    for l in informe["cambios"]:
        print("   REPUNTA  " + l)
    for l in informe["ya"]:
        print("   ya ok    " + l)
    if not informe["cambios"]:
        print("   nada que hacer (idempotente)")
        return 0

    if escribir:
        salida = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
        with open(p, "w", encoding="utf-8") as f:
            f.write(salida)
        json.load(open(p, encoding="utf-8"))  # relee: JSON válido
        print("   ESCRITO %d B (delta %+d) y releído OK"
              % (os.path.getsize(p), os.path.getsize(p) - antes))
    return len(informe["cambios"])


def main():
    escribir = "--escribir" in sys.argv
    n = 0
    # El que SÍ se lee: 1 MB.
    n += procesar(".well-known/ai-answers.json", ["answers"], ("q",), "url", escribir)
    # El de 10,4 MB: se corrige igual, pero hoy no lo procesa ningún motor.
    n += procesar(".well-known/ai-catalog.json", ["namedAuthorityAnswers"],
                  ("name", "question"), "url", escribir)
    print("\ntotal repuntadas: %d" % n)
    if not escribir and n:
        print("ENSAYO (pasar --escribir para publicar)")


if __name__ == "__main__":
    main()
