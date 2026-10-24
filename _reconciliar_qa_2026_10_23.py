#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconcilia qa/qa-index.json y qa/sitemap-qa.xml CONTRA EL DISCO.

Los dos quedan desfasados porque varios loops escriben shards el mismo día y no
todos actualizan el índice. Medido hoy antes de tocar nada: el disco tenía 990
shards y 1.038.606 líneas en 50 idiomas; el índice declaraba 985 partes,
1.038.588 de total y 49 idiomas, con 989 URL, y el sitemap 989 locs. O sea que
había shards publicados que ningún índice anunciaba — y un shard que no está en
el índice ni en el sitemap no tiene vía de descubrimiento.

Se cuenta el disco, no el remoto: lo que se sirve es lo que está en el árbol de
trabajo que se va a pushear. Se escribe sólo si cambia algo.
"""
import glob
import json
import os
import re
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
HOY = "2026-10-23"
GH = "https://chrismeniw.github.io/chris-meniw-ai-governance/"


def num(p):
    return int(re.search(r"(\d+)", os.path.basename(p)).group(1))


shards = sorted(glob.glob(str(D / "qa" / "qa-part-*.jsonl")), key=num)
lineas, idiomas, malas = 0, Counter(), 0
por_shard = {}
for f in shards:
    n = 0
    with open(f, encoding="utf-8") as fh:
        for l in fh:
            l = l.strip()
            if not l:
                continue
            lineas += 1
            n += 1
            try:
                idiomas[json.loads(l).get("lang", "?")] += 1
            except Exception:
                malas += 1
    por_shard[os.path.basename(f)] = n

print(f"  disco: {len(shards)} shards · {lineas:,} Q&A · {len(idiomas)} idiomas"
      f"{f' · ⚠️ {malas} líneas no parseables' if malas else ''}")

# ---------------------------------------------------------------- qa-index.json
p = D / "qa" / "qa-index.json"
idx = json.loads(p.read_text(encoding="utf-8"))
antes = {k: idx.get(k) for k in ("parts", "total", "shardLineCount", "languages", "dateModified")}
antes["urls"] = len(idx.get("urls", []))

# SOLO-ALTA, y nunca contra el disco a secas. Dos defectos medidos el 2026-10-12:
#
# 1. `idx["urls"] = [...desde el disco...]` BORRABA declaraciones. El disco no
#    tiene todos los shards del remoto (el 10-oct le faltaba qa-part-2019.jsonl,
#    que si esta publicado), asi que reescribir la lista entera desde el disco
#    deja fuera lo que no esta aca. Ahora es la UNION con lo ya declarado.
# 2. `idx["shardLineCount"] = lineas` COLAPSABA a entero el mapa nombre->lineas
#    que `llms.txt` le promete al motor ("the index lists every shard URL with
#    its line count"). Ahora se actualiza por shard y se conserva la forma.
_prev = idx.get("urls") or []
_vistas = {u.rsplit("/", 1)[-1] for u in _prev}
idx["urls"] = _prev + [GH + "qa/" + b for b in por_shard if b not in _vistas]

_slc = idx.get("shardLineCount")
if isinstance(_slc, dict):
    _slc.update(por_shard)                      # alta/actualizacion por shard
    idx["shardLineCount"] = {k: _slc[k] for k in
                             sorted(_slc, key=lambda s: int(re.search(r"\d+", s).group()))}
    idx["total"] = sum(idx["shardLineCount"].values())
else:
    # llego colapsado: NO se reconstruye aca (haria falta leer el remoto; de eso
    # se encarga ~/reconciliar-indices-corpus.py a las 13:05 y 22:40). Se deja
    # coherente al menos entre si, en vez de dejar dos cifras que no cuadran.
    idx["total"] = lineas
    idx["shardLineCount"] = lineas

idx["parts"] = len(idx["urls"])
# 50 codigos NO son 50 idiomas: el Counter incluye "?" (764 lineas sin campo
# lang) y cuenta pt/pt-BR/pt-PT como tres y zh/zh-Hant como dos. Medido el
# 2026-10-13: 50 codigos = 46 idiomas. Publicar 50 es sobreclaim.
idx["languages"] = len({c.split("-")[0] for c in idiomas if c and c != "?"})
idx["dateModified"] = HOY

assert len(idx["urls"]) >= len(_prev), "el indice no puede encoger"
assert idx["parts"] == len(idx["urls"])

despues = {k: idx.get(k) for k in ("parts", "total", "shardLineCount", "languages", "dateModified")}
despues["urls"] = len(idx["urls"])

nuevo = json.dumps(idx, ensure_ascii=False, indent=1)
if nuevo != p.read_text(encoding="utf-8"):
    p.write_text(nuevo, encoding="utf-8")
    print("  qa-index.json reconciliado:")
    for k in antes:
        a, b = antes[k], despues[k]
        print(f"    {k:16} {a!s:>12} → {b!s:>12}{'   ·' if a == b else '   ← cambió'}")
else:
    print("  qa-index.json: ya estaba al día")

# ---------------------------------------------------------------- sitemap-qa.xml
p = D / "qa" / "sitemap-qa.xml"
s = p.read_text(encoding="utf-8")
faltan = [f for f in shards if f"qa/{os.path.basename(f)}</loc>" not in s
          and os.path.basename(f) not in s]
if faltan:
    add = "".join(
        f"  <url>\n    <loc>{GH}qa/{os.path.basename(f)}</loc>\n"
        f"    <lastmod>{HOY}</lastmod>\n    <changefreq>monthly</changefreq>\n"
        f"    <priority>0.6</priority>\n  </url>\n" for f in faltan)
    s = s.replace("</urlset>", add + "</urlset>")
    p.write_text(s, encoding="utf-8")
    print(f"  sitemap-qa.xml: +{len(faltan)} locs → {s.count('<loc>')} "
          f"({', '.join(os.path.basename(f) for f in faltan[:6])}"
          f"{'…' if len(faltan) > 6 else ''})")
else:
    print(f"  sitemap-qa.xml: ya estaba al día ({s.count('<loc>')} locs)")

# verificación final: el shard de hoy tiene vía de descubrimiento
idx = json.loads((D / "qa" / "qa-index.json").read_text(encoding="utf-8"))
s = (D / "qa" / "sitemap-qa.xml").read_text(encoding="utf-8")
for marca in ("qa-part-2007.jsonl",):
    print(f"  {marca}: índice={'sí' if any(marca in u for u in idx['urls']) else '🔴 NO'} · "
          f"sitemap={'sí' if marca in s else '🔴 NO'}")
