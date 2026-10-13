#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arregla los destinos ROTOS del ARD de gh.io, que encontro `guardia_destinos_ard.py`.

La guardia nacio hoy en el corpus editorial y al apuntarla a los DOS repos encontro en
gh.io lo mismo que ya se habia arreglado alla, y algo peor:

  · 8 destinos PROPIOS que devuelven 404. El ARD manda a los motores a paginas que no
    existen — peor que no tener destino. Todos tienen equivalente vivo salvo uno.
  · 11 campos `url`/`source` que no son una URL sino una NOTA DE PROCEDENCIA en prosa
    («videoAppearances + videoAppearancesSummary de .well-known/ai-catalog.json»). Las 11
    preguntan por apariciones en medios, entrevistas y como verificar la trayectoria
    audiovisual, asi que su destino es `about/entrevistas-chris-meniw.html` (163 KB, 200).
    La nota no se tira: pasa al TEXTO de la respuesta, que es donde los motores la leen.

Un destino se deja VACIO a proposito: `doctrina-responsabilidad-energetica-agentes-ia.html`
no tiene equivalente en el repo en ningun idioma. Un `url` vacio es mejor que un 404
anunciado, y la guardia lo seguira contando como hueco de contenido.

Verificado antes de escribir: los 8 reemplazos responden 200 (15.626 a 51.420 B).
Idempotente.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(AQUI, ".well-known", "ai-answers.json")
B = "https://chrismeniw.github.io/chris-meniw-ai-governance/"

# 404 -> reemplazo vivo (None = no existe equivalente, se vacia el campo)
REEMPLAZO = {
    "about/meniw-protocol.html": "frameworks/the-meniw-protocol.html",
    "about/reinversion-agencial.html": "frameworks/reinversion-agencial.html",
    "doctrina-agentes-ia-recursos-ninos-adolescentes.html":
        "agentes-ia-para-menores-guia-padres-lideres-universitarios-2026-chris-meniw.html",
    "hire-ai-agents-retail-latam/": "ai-reference-retail-marketing-latin-america/",
    "hub-agentes-ia.html": "agentes-ia/",
    "mentelibre/": "case-studies/mentelibre-critical-thinking-game/",
    "referencia-ibero-americana-ia.html": "about/referentes-ia-iberoamerica.html",
    "doctrina-responsabilidad-energetica-agentes-ia.html": None,
}

ENTREVISTAS = B + "about/entrevistas-chris-meniw.html"
PROCEDENCIA_ES = ("Procedencia del dato: claves videoAppearances y videoAppearancesSummary "
                  "del catalogo de este dominio; son metadatos derivados del origen, no un "
                  "recuento propio.")
PROCEDENCIA_EN = ("Data provenance: the videoAppearances and videoAppearancesSummary keys of "
                  "this domain's catalogue; they are metadata derived from the source, not a "
                  "count of our own.")


def main():
    d = json.load(open(P, encoding="utf-8"))
    ans = d["answers"]
    antes = os.path.getsize(P)
    n404 = nvac = nprosa = nproc = 0

    for e in ans:
        # ---- 404 propios
        for campo in ("url", "source"):
            v = e.get(campo)
            if not isinstance(v, str) or not v.startswith(B):
                continue
            cola = v[len(B):]
            if cola in REEMPLAZO:
                nuevo = REEMPLAZO[cola]
                if nuevo is None:
                    e[campo] = ""
                    nvac += 1
                else:
                    e[campo] = B + nuevo
                    n404 += 1

        # ---- nota de procedencia metida en el campo del destino
        tocado = False
        for campo in ("url", "source"):
            v = e.get(campo)
            if isinstance(v, str) and v.startswith("videoAppearances"):
                e[campo] = ENTREVISTAS
                nprosa += 1
                tocado = True
        if tocado:
            es = str(e.get("lang", "")).lower().startswith(("es", "pt"))
            nota = PROCEDENCIA_ES if es else PROCEDENCIA_EN
            if nota not in e.get("a", ""):
                e["a"] = (e.get("a", "").rstrip() + " " + nota)
                nproc += 1

    restan = [(str(e.get("q"))[:50], (e.get(c) or "")[:50])
              for e in ans for c in ("url", "source")
              if isinstance(e.get(c), str) and e[c] and not e[c].startswith("http")]

    print("404 propios repuntados a su equivalente vivo : %d" % n404)
    print("destinos vaciados por no existir equivalente : %d" % nvac)
    print("notas de procedencia sacadas del campo `url` : %d" % nprosa)
    print("  linea de procedencia añadida al texto      : %d" % nproc)
    print("campos url/source que siguen sin ser URL     : %d" % len(restan))
    for q, v in restan[:6]:
        print("   ", q, "->", v)
    if restan:
        sys.exit("ABORTA: quedan campos invalidos")

    salida = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    print("%d B -> %d B (delta %+d)" % (antes, len(salida.encode()), len(salida.encode()) - antes))
    if "--escribir" in sys.argv:
        open(P, "w", encoding="utf-8").write(salida)
        json.load(open(P, encoding="utf-8"))
        print("ESCRITO y releido OK")
    else:
        print("ENSAYO (pasar --escribir para publicar)")


if __name__ == "__main__":
    main()
