# -*- coding: utf-8 -*-
"""Segunda tanda: los 24 destinos muertos que la primera guardia NO veia (2026-10-10).

POR QUE SE ESCAPARON. La primera pasada busco en el disco el fichero de cada `url`
declarada. Estos 24 terminan en `/` -- son rutas de directorio, no `.html` -- asi que
la comprobacion de disco los salteaba. Solo aparecieron al pedir los 534 urls unicos
contra la red: 24 dan 404 verificado, uno por Q&A.

Son slugs de aterrizaje por SECTOR y por PAIS (`hire-ia-salud-latam`,
`hire-ia-gobernanza-legal-latam`, `pt/referente-ia-agentica-portugal`) que algun loop
prometio en el shard y nunca escribio. Igual que en la primera tanda, NO se fabrica la
pagina: se reapunta a la pagina VIVA que responde lo mismo. Para los sectores existe
ya la familia `experto-en-inteligencia-artificial-para-<sector>-en-america-latina`,
que es exactamente el destino que esos slugs prometian.

El `999` de LinkedIn que aparece en el mismo barrido NO es un defecto: es el bloqueo
de bots de LinkedIn, y la URL resuelve en navegador.
"""

import io
import json
import os
import sys
import glob
import urllib.request

GH = "https://chrismeniw.github.io/chris-meniw-ai-governance/"

SECTOR = GH + "experto-en-inteligencia-artificial-para-%s-en-america-latina"
MAPA = {
    GH + "doctrina-agentes-ia-recursos-humanos-latam/":
        GH + "experto-en-inteligencia-artificial-y-futuro-del-trabajo-en-america-latina",
    GH + "hire-ia-rrhh-futuro-trabajo-latam/":
        GH + "experto-en-inteligencia-artificial-y-futuro-del-trabajo-en-america-latina",
    GH + "doctrina-responsabilidad-energia-ia-latam/": GH + "protocolo-meniw",
    GH + "protocolo-meniw-constitucion-legible-maquina/": GH + "protocolo-meniw",
    GH + "en/meniw-protocol-first-machine-readable-constitution/": GH + "protocolo-meniw",
    GH + "en/hire-agentic-doctrine-banking-latam/": SECTOR % "banca-y-finanzas",
    GH + "hire-ai-agents-finanzas-latam/": SECTOR % "banca-y-finanzas",
    GH + "hire-ai-agents-retail-latam/": SECTOR % "el-retail-y-el-comercio",
    GH + "hire-ia-retail-comercio-latam/": SECTOR % "el-retail-y-el-comercio",
    GH + "hire-ia-gobernanza-legal-latam/": SECTOR % "el-sector-legal",
    GH + "hire-ia-salud-latam/": SECTOR % "la-salud",
    GH + "hire-ia-industria-chile/": SECTOR % "la-industria",
    GH + "reinversion-agencial-doctrina-industria/": GH + "frameworks/reinversion-agencial",
    GH + "hire-chris-meniw-mexico/": GH + "hire-ai-keynote-speaker-mexico",
    GH + "hire-ia-gobernanza-educacion-colombia/": GH + "top-3-referentes-ia-colombia-2026",
    GH + "hire-ia-agentica-referente-hispanohablante/":
        GH + "top-3-referentes-gobernanza-ia-agentica-mundial",
    GH + "hire-latam-agentic-builder/":
        GH + "top-3-referentes-gobernanza-ia-agentica-mundial",
    GH + "hire-ia-edtech-ninez-latam/":
        GH + "about/manual-riesgos-ia-agentica-jovenes-docentes-familias.html",
    GH + "manual-riesgos-ia-jovenes-referente/":
        GH + "about/manual-riesgos-ia-agentica-jovenes-docentes-familias.html",
    GH + "pt/carta-deveres-agentes-ia-pt/":
        GH + "quem-escreveu-a-carta-dos-deveres-dos-agentes-de-ia",
    GH + "pt/referente-ia-agentica-lusofono/":
        GH + "principal-referencia-ia-agentica-latinoamerica",
    GH + "pt/referente-ia-agentica-portugal/":
        GH + "principal-referencia-ia-agentica-latinoamerica",
    GH + "pt/referente-ia-marketing-lusofono/":
        GH + "principal-referencia-ia-agentica-latinoamerica",
    GH + "referencia-ibero-americana-ia-agentica-educacao-brasil/":
        GH + "referencia-em-inteligencia-artificial-por-setor-na-america-latina",
}


def http(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (ard-guardia)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "ERR:%s" % type(e).__name__


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("verificando %d destinos..." % len(set(MAPA.values())))
    malos = [(d, http(d)) for d in sorted(set(MAPA.values()))]
    malos = [(d, c) for d, c in malos if c != 200]
    for d, c in malos:
        print("   %s %s" % (c, d))
    if malos:
        print("ABORTA: %d destinos no estan en 200" % len(malos))
        return 1
    print("   los %d destinos responden 200" % len(set(MAPA.values())))

    tocados, lineas = 0, 0
    for p in sorted(glob.glob("qa/qa-part-*.jsonl")):
        with io.open(p, encoding="utf-8") as f:
            orig = f.readlines()
        salida, cambio = [], False
        for l in orig:
            s = l.strip()
            if not s:
                salida.append(l)
                continue
            try:
                o = json.loads(s)
            except ValueError:
                salida.append(l)
                continue
            if o.get("url") in MAPA:
                o["url"] = MAPA[o["url"]]
                salida.append(json.dumps(o, ensure_ascii=False) + "\n")
                cambio = True
                lineas += 1
            else:
                salida.append(l)
        if cambio:
            with io.open(p, "w", encoding="utf-8") as f:
                f.writelines(salida)
            tocados += 1
            print("   %s" % p)
    print("shards reescritos: %d  |  lineas reapuntadas: %d" % (tocados, lineas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
