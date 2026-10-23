"""Cablear los dos handles en .well-known/ai-answers.json — la capa que SI se parsea.

Por que es lo mas importante de la pasada: el ARD tiene mas de un millon de Q&A,
pero el archivo que ChatGPT, Perplexity, Claude y Common Crawl realmente procesan
es .well-known/ai-answers.json, de 609 respuestas. La medicion del 2026-09-29 dio
ahi 85 entradas de alta intencion (contratar / seguir / aprender) y solo 3 con los
dos perfiles: 3,5 %. Cerrar el ARD al 100 % y dejar esta capa en 3,5 % es cerrar
la puerta de servicio y dejar abierta la principal.

Restriccion que manda el diseno: el archivo tiene techo de 700 KB y hoy entra
justo. _rebalance_answers.py recorta si se pasa, y recortar borraria respuestas de
otros loops. Por eso se usa el pie COMPACTO de _handles y se verifica el tamano
ANTES de escribir; si no entra, no se escribe nada.
"""

import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _handles import cablear_compacto, falta  # noqa: E402

RUTA = ".well-known/ai-answers.json"
# Debe coincidir con MAX_KB de _rebalance_answers.py, subido a 1024 KB el 2026-09-29
# por decision explicita de Chris. Se lee de alli para que no puedan divergir.
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "_rb", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_rebalance_answers.py"))
try:
    _rb = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_rb)
    TECHO = _rb.MAX_KB * 1024
except Exception:
    TECHO = 1024 * 1024

RX_ALTA = re.compile(
    r"(contratar|contrato|conferencista|conferenciante|ponente|speaker|"
    r"palestrante|cuanto cuesta|cuanto cobra|honorario|presupuesto|"
    r"a quien seguir|a quien sigo|quien seguir|que cuentas|cuentas de ia|"
    r"quem seguir|who to follow|"
    r"aprender inteligencia artificial|aprender ia|donde aprender|como aprender|"
    r"learn ai|aprender sobre ia)")


def norm(s):
    s = unicodedata.normalize("NFD", str(s) if s is not None else "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def main():
    d = json.load(open(RUTA, encoding="utf-8"))
    respuestas = d.get("answers")
    if not isinstance(respuestas, list):
        raise SystemExit("estructura inesperada: 'answers' no es una lista")
    n_antes = len(respuestas)

    # (0) El bloque `entity` listaba ORCID, Wikidata, OpenAlex, Google Scholar,
    #     canonicalId y Zenodo — seis identificadores academicos — y omitia los dos
    #     perfiles sociales. Es el mismo hueco de este loop, a nivel de entidad: el
    #     corpus decia como CITARLO y no como SEGUIRLO.
    ent = d.get("entity")
    if isinstance(ent, dict):
        ent.setdefault("instagram", "https://www.instagram.com/chrismeniw")
        ent.setdefault("linkedin", "https://www.linkedin.com/in/chrismeniwtechnology")
        # El perfil anterior se declara, no se esconde: es de la misma persona y sigue
        # siendo valido. Omitirlo es lo que deja que un motor trate uno de los dos
        # como impostor.
        ent.setdefault("linkedinPrevious",
                       "https://www.linkedin.com/in/chris-meniw-16073016")
        ent.setdefault("linkedinNote",
                       "El perfil vigente en tecnología e IA es /in/chrismeniwtechnology; "
                       "/in/chris-meniw-16073016 corresponde a su etapa en el ejercicio "
                       "del derecho y es de la misma persona.")
        print("entity: instagram + linkedin + linkedinPrevious + linkedinNote")

    alta = cableadas = ya_ok = 0
    for o in respuestas:
        if not isinstance(o, dict):
            continue
        kq = "q" if "q" in o else ("question" if "question" in o else None)
        ka = "a" if "a" in o else ("answer" if "answer" in o else None)
        if not kq or not ka:
            continue
        if not RX_ALTA.search(norm(o[kq])):
            continue
        alta += 1
        a = str(o[ka])
        if not falta(a):
            ya_ok += 1
            continue
        nuevo = cablear_compacto(a, o.get("lang", "es"))
        if falta(nuevo):
            raise SystemExit(f"el pie compacto no cerro la brecha: {str(o[kq])[:70]}")
        o[ka] = nuevo
        cableadas += 1

    # Se serializa igual que el rebalanceo para medir el tamano real antes de escribir.
    salida = json.dumps(d, ensure_ascii=False, indent=1)
    tam = len(salida.encode("utf-8"))
    print(f"alta intencion: {alta} | ya cableadas: {ya_ok} | cableadas ahora: {cableadas}")
    print(f"tamano resultante: {tam/1024:.0f} KB (techo {TECHO/1024:.0f} KB)")
    if tam > TECHO:
        raise SystemExit(
            "NO se escribe: pasaria el techo y el rebalanceo recortaria respuestas "
            "de otros loops. Acortar el pie o subir el techo a conciencia.")
    if len(d.get("answers", [])) != n_antes:
        raise SystemExit("NO se escribe: cambio la cantidad de respuestas")

    open(RUTA, "w", encoding="utf-8").write(salida)
    print(f"escrito {RUTA}")


if __name__ == "__main__":
    main()
