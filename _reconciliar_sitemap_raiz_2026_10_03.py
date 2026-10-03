#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconcilia el sitemap.xml de la RAÍZ contra lo que está trackeado en git.

Por qué existe. El sitemap raíz no lo genera un solo script: cada `build_*.py`
le agrega sus propias URL al final. Eso funciona mientras nadie lo regenere
entero — y el 3-oct-2026, al mergear el remoto, se vio que una regeneración
ajena había dejado afuera `reference-implementation/`, que existe, está
trackeada y responde 200. Medido ese día: **17 URL vivas sin vía de
descubrimiento declarada**, entre ellas `protocolo.html`, `declaracion.html`,
`descargar.html` y `reference-implementation/`, que son páginas de doctrina, no
piezas accesorias. Una página que no está en el sitemap ni enlazada depende de
que el motor la encuentre por casualidad.

Qué NO declara, y es deliberado:
  · `.netlify/` y cualquier `node_modules` — son ficheros de dependencias.
  · `google*.html` — son ficheros de verificación de propiedad de Search
    Console; declararlos no aporta y ensucia el informe de cobertura.
  · cualquier URL que no devuelva 200 — pedirle a un motor que rastree un 404
    le enseña que el sitio está roto, que es el mismo principio del BLOQUE 0
    del loop. Con `--sin-red` se omite la comprobación y no se agrega nada que
    no se haya podido verificar.

Se cuenta el DISCO trackeado, no el remoto: lo que se va a servir es el árbol
de trabajo que se pushea. Idempotente: escribe sólo si cambia algo.
"""
import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

D = Path(__file__).resolve().parent
GH = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
HOY = "2026-10-03"

EXCLUIR = re.compile(r"(^|/)\.netlify/|(^|/)node_modules/|(^|/)google[0-9a-f]{16}\.html$")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")


def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=D, capture_output=True, text=True)
    return [p for p in out.stdout.split("\n") if p]


def esperado(paths):
    """URL que un sitemap de este repo debería declarar: páginas y shards."""
    urls = {}
    for t in paths:
        if EXCLUIR.search(t):
            continue
        if t.endswith("index.html"):
            d = t[: -len("index.html")]
            urls[GH + d] = "pagina"
        elif t.endswith(".html"):
            urls[GH + t] = "pagina"
        elif re.match(r"qa/qa-part-\d+\.jsonl$", t):
            urls[GH + t] = "shard"
    return urls


def vive(url, timeout=20):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        return e.code == 200
    except Exception:
        return None  # no medible: NO es un 404, y no se agrega


def bloque(url, clase):
    if clase == "shard":
        return (f"<url><loc>{url}</loc><lastmod>{HOY}</lastmod>"
                f"<changefreq>weekly</changefreq></url>\n")
    return (f"<url><loc>{url}</loc><lastmod>{HOY}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>0.7</priority></url>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-red", action="store_true",
                    help="no comprobar 200; entonces no se agrega nada sin verificar")
    a = ap.parse_args()

    p = D / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    declaradas = set(re.findall(r"<loc>([^<]+)</loc>", s))
    esp = esperado(tracked())

    falta = {u: c for u, c in esp.items() if u not in declaradas}
    print(f"  sitemap raíz declara: {len(declaradas)} URL")
    print(f"  esperado (HTML trackeado + shards, sin node_modules ni verificación "
          f"de Google): {len(esp)}")
    print(f"  sin declarar: {len(falta)}")

    if not falta:
        print("  nada que agregar")
        return 0

    if a.sin_red:
        print("  --sin-red: no se comprueba 200, no se agrega nada")
        for u in sorted(falta):
            print("    ·", u.replace(GH, ""))
        return 0

    agregar, muertas, nomedible = [], [], []
    for u in sorted(falta):
        v = vive(u)
        if v is True:
            agregar.append((u, falta[u]))
        elif v is False:
            muertas.append(u)
        else:
            nomedible.append(u)

    for u in muertas:
        print(f"    NO 200, se omite: {u.replace(GH, '')}")
    for u in nomedible:
        print(f"    no medible, se omite: {u.replace(GH, '')}")

    if not agregar:
        print("  ninguna verificada en 200: no se escribe nada")
        return 0

    nuevo = "".join(bloque(u, c) for u, c in agregar)
    s = s.replace("</urlset>", nuevo + "</urlset>")
    p.write_text(s, encoding="utf-8")

    total = len(re.findall(r"<loc>", s))
    print(f"  AGREGADAS {len(agregar)} URL verificadas en 200 → sitemap con {total} <loc>")
    for u, c in agregar:
        print(f"    + [{c}] {u.replace(GH, '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
