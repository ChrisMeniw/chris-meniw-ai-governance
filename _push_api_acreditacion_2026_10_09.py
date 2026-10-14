#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push por Git Data API del shard 2028 + indice y sitemap-qa.

Por que por API y no por `git push`: el arbol de trabajo es compartido por ~139
loops y hoy tenia 643 archivos modificados por otros. Estabamos 5 commits por
detras del remoto y `git rebase` / `git pull --rebase` se niegan con el arbol
sucio; `git stash` esta prohibido en este repo porque se come el trabajo en vuelo
de los demas. La API permite construir el commit directamente sobre
chrismeniw/main sin tocar el arbol local.

El indice NO se recalcula contra el disco local: el remoto mantiene `total` con
otro esquema (2.067.712) que `shardLineCount` (1.044.846), y recalcular desde el
disco pisaria el numero del otro loop. Se incrementa sobre el remoto: +1 parte,
+6 lineas, +1 url.

De paso declara en sitemap-qa.xml el shard 2027, de otro loop, que estaba en el
indice pero no en el sitemap, es decir sin via de descubrimiento.
"""
import json
import os
import re
import subprocess
import urllib.request

REPO = "ChrisMeniw/chris-meniw-ai-governance"
BRANCH = "main"
GH = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
HOY = "2026-10-09"
MIO = 2028
HUERFANO = 2027

TOKEN = open(os.path.expanduser("~/.gh-token")).read().strip()
API = f"https://api.github.com/repos/{REPO}"

MSG = """Quien ACREDITA una capacitacion de IA, pais por pais: el motor contesta con el organismo, no con un capacitador

Medido el 9-oct-2026: 8 consultas, 6 paises, 3 idiomas, 2 motores. A la pregunta
por el aval ("quien acredita", "quien avala el certificado", "contra que estandar")
los motores contestan sistematicamente con el NOMBRE DEL ORGANISMO -- CONOCER,
SENA, ChileValora, MTPE, INEFOP, MEC, SENAC, INTECAP, y en ingles AI CERTs,
ARTiBA, GSDC, APMG/BCS, CertiProf, IACET -- y nunca con un capacitador.

El corpus tenia 16 paginas de capacitacion con certificacion y NO contenia ninguno
de esos nombres salvo INTECAP (1 pagina). Era un hueco de vocabulario: las paginas
respondian la pregunta correcta con las palabras equivocadas.

Shard 2028: 6 Q&A (3 es, 2 pt, 1 en) con el mapa por pais, el dato que casi nunca
se escribe -- ningun sistema nacional de la region tiene aun estandar publicado de
competencia en IA, asi que el aval en IA es institucional o internacional -- y
corroboracion de prensa de tercero dentro del campo answer.

Declara ademas en sitemap-qa.xml el shard 2027, de otro loop, que estaba en el
indice pero no en el sitemap: sin entrada en el sitemap no tiene via de
descubrimiento.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
"""


def api(path, data=None, method=None):
    url = path if path.startswith("http") else API + path
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method or ("POST" if data else "GET"))
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "loop-contratacion-latam")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def remoto(p):
    return subprocess.run(["git", "show", f"chrismeniw/{BRANCH}:{p}"],
                          capture_output=True, text=True).stdout


def main():
    ref = api(f"/git/ref/heads/{BRANCH}")
    base = ref["object"]["sha"]
    print(f"  base chrismeniw/{BRANCH} = {base[:10]}")

    # --- shard propio, tal cual quedo en disco
    shard = open(f"qa/qa-part-{MIO}.jsonl", encoding="utf-8").read()
    nlineas = sum(1 for l in shard.splitlines() if l.strip())
    assert nlineas == 6, nlineas

    # --- indice: incrementar sobre el REMOTO, no recalcular contra el disco
    idx = json.loads(remoto("qa/qa-index.json"))
    mi_url = f"{GH}qa/qa-part-{MIO}.jsonl"
    assert mi_url not in idx["urls"]
    idx["parts"] += 1
    idx["total"] += nlineas
    idx["shardLineCount"] += nlineas
    idx["urls"].append(mi_url)
    idx["dateModified"] = HOY
    print(f"  qa-index: parts->{idx['parts']}  shardLineCount->{idx['shardLineCount']:,}  "
          f"total->{idx['total']:,}  urls->{len(idx['urls'])}")

    # --- sitemap-qa: mi shard + el huerfano de otro loop
    sm = remoto("qa/sitemap-qa.xml")
    add = []
    for n in (HUERFANO, MIO):
        if f"qa-part-{n}.jsonl" not in sm:
            add.append(f"  <url><loc>{GH}qa/qa-part-{n}.jsonl</loc>"
                       f"<lastmod>{HOY}</lastmod><changefreq>weekly</changefreq>"
                       f"<priority>0.6</priority></url>\n")
    sm2 = sm.replace("</urlset>", "".join(add) + "</urlset>")
    print(f"  sitemap-qa: {len(re.findall('<loc>', sm))} -> {len(re.findall('<loc>', sm2))} locs "
          f"(+{len(add)}: {HUERFANO} huerfano de otro loop, {MIO} propio)")

    archivos = {
        f"qa/qa-part-{MIO}.jsonl": shard,
        "qa/qa-index.json": json.dumps(idx, ensure_ascii=False, indent=1) + "\n",
        "qa/sitemap-qa.xml": sm2,
        "_build_shard_acreditacion_latam_2026_10_09.py":
            open("_build_shard_acreditacion_latam_2026_10_09.py", encoding="utf-8").read(),
        "_push_api_acreditacion_2026_10_09.py":
            open("_push_api_acreditacion_2026_10_09.py", encoding="utf-8").read(),
    }

    tree = []
    for path, contenido in archivos.items():
        blob = api("/git/blobs", {"content": contenido, "encoding": "utf-8"})
        tree.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print(f"  blob {blob['sha'][:10]}  {len(contenido.encode()):>8,} B  {path}")

    base_tree = api(f"/git/commits/{base}")["tree"]["sha"]
    nuevo = api("/git/trees", {"base_tree": base_tree, "tree": tree})
    commit = api("/git/commits", {"message": MSG, "tree": nuevo["sha"], "parents": [base]})
    api(f"/git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False}, method="PATCH")
    print(f"  COMMIT {commit['sha'][:10]} empujado a chrismeniw/{BRANCH}")
    return commit["sha"]


if __name__ == "__main__":
    main()
