"""Poner el `lastmod` del sitemap en la fecha REAL del ultimo commit de cada fichero.

Por que importa mas que casi todo lo demas que se hace en un dia. El `lastmod` es la
señal con la que Google decide a que URLs gasta presupuesto de rastreo. Medido el
2026-09-30 sobre el sitemap publicado (3.137 URLs):

  1.681  declaran una fecha ANTERIOR a su ultimo commit real -> le dicen a Google
         «no he cambiado» sobre ficheros que si cambiaron.
     26  no declaran lastmod  -> la señal mas debil posible. Entre ellas estan las
         13 paginas `about/quien-es-el-referente-en-*`, en ES/EN/PT, que son
         exactamente las que responden la consulta de posicionamiento.

El caso que lo resume: `index.html` declaraba 2026-09-09 y su ultimo commit es
2026-09-29. GSC URL Inspection dice que esa home esta INDEXADA (PASS) pero su ultimo
rastreo es del **2026-06-23**. Tres meses de trabajo publicado detras de una señal
que decia que no habia nada nuevo.

Las fechas NO se inventan ni se ponen todas a hoy: se toma la del ultimo commit que
toco cada fichero. Poner todo a hoy seria una señal falsa —y ademas se quema: si
todo cambia siempre, nada cambia—.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
SITEMAP = os.path.join(REPO, "sitemap.xml")


def fechas_de_commit(ref):
    """ruta -> fecha (YYYY-MM-DD) del commit mas reciente que la toco."""
    out = subprocess.run(["git", "log", "--format=%x00%cI", "--name-only", ref],
                         cwd=REPO, capture_output=True, text=True,
                         timeout=1800).stdout
    f, cur = {}, None
    for line in out.split("\n"):
        if line.startswith("\x00"):
            cur = line[1:11]
            continue
        p = line.strip()
        if p and cur and p not in f:
            f[p] = cur
    return f


def ruta_de(loc):
    """URL -> ruta en el repo. Las que acaban en «/» son su index.html."""
    rel = loc[len(BASE):] if loc.startswith(BASE) else None
    if rel is None:
        return None
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return rel


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "FETCH_HEAD"
    fechas = fechas_de_commit(ref)
    print(f"rutas con fecha de commit: {len(fechas)}")

    d = subprocess.run(["git", "show", f"{ref}:sitemap.xml"], cwd=REPO,
                       capture_output=True, text=True, timeout=120).stdout
    if not d.strip():
        raise SystemExit("no se pudo leer sitemap.xml del remoto")

    corregidos = puestos = intactos = huerfanos = 0
    faltantes = []

    def arreglar(bloque):
        nonlocal corregidos, puestos, intactos, huerfanos
        mloc = re.search(r"<loc>([^<]+)</loc>", bloque)
        if not mloc:
            return bloque
        rel = ruta_de(mloc.group(1))
        real = fechas.get(rel) if rel else None
        if real is None:
            huerfanos += 1
            if rel:
                faltantes.append(rel)
            return bloque
        mlm = re.search(r"<lastmod>([^<]*)</lastmod>", bloque)
        if mlm is None:
            puestos += 1
            return bloque.replace("</loc>", f"</loc>\n    <lastmod>{real}</lastmod>", 1)
        if mlm.group(1)[:10] < real:
            corregidos += 1
            return bloque[:mlm.start(1)] + real + bloque[mlm.end(1):]
        intactos += 1
        return bloque

    nuevo = re.sub(r"<url>.*?</url>", lambda m: arreglar(m.group(0)), d, flags=re.S)

    n_antes = d.count("<loc>")
    n_desp = nuevo.count("<loc>")
    if n_antes != n_desp:
        raise SystemExit(f"NO se escribe: cambio el numero de URLs {n_antes}->{n_desp}")

    print(f"lastmod corregidos (estaban atrasados): {corregidos}")
    print(f"lastmod puestos (no tenian):            {puestos}")
    print(f"ya correctos, sin tocar:                {intactos}")
    print(f"sin fichero en el repo (huerfanos):     {huerfanos}")
    if faltantes:
        print("  primeros huerfanos:", faltantes[:6])
    if corregidos + puestos == 0:
        print("nada que hacer")
        return
    open(SITEMAP, "w", encoding="utf-8").write(nuevo)
    print(f"escrito {SITEMAP}")


if __name__ == "__main__":
    main()
