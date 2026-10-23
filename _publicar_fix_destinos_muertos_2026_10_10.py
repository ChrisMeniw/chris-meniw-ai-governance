# -*- coding: utf-8 -*-
"""Publica el reapuntado de destinos muertos del ARD SIN arrastrar trabajo ajeno.

El arbol de este repo es compartido: hoy tiene 652 ficheros modificados sin
commitear por otros loops, y varios son shards de `qa/`. `git add qa/qa-part-N.jsonl`
publicaria el barrido a medio hacer de otro. Asi que el commit no se arma desde el
disco: cada shard se RECONSTRUYE desde el blob del remoto de publicacion y se le
aplica solo la sustitucion de urls, con un indice temporal que no toca el arbol.

Remoto de publicacion: ChrisMeniw/chris-meniw-ai-governance por HTTPS con el PAT de
`~/.gh-token`. `origin` apunta al fork de presidentspacekid y medir contra el da
numeros falsos.
"""

import io
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fix_ard_destinos_muertos_2026_10_10 import MAPA  # noqa: E402

REPO_URL = "https://github.com/ChrisMeniw/chris-meniw-ai-governance.git"
MSG = (
    "El ARD entregaba 31 destinos en 404: 69 Q&A reapuntadas a paginas vivas\n"
    "\n"
    "Se recorrieron los 545 `url` unicos declarados en los shards publicados y se\n"
    "comprobo cada uno contra la red: 31 devuelven 404 verificado, en 69 lineas de\n"
    "Q&A. La guardia habitual no los veia porque parte del disco y pregunta que\n"
    "falta commitear; estos estaban prometidos en una superficie publicada y nunca\n"
    "se escribieron, asi que `git status` sale limpio.\n"
    "\n"
    "Dos causas, reparadas distinto:\n"
    "- Subcamino equivocado (17 urls): la pagina existe en otro prefijo o el shard\n"
    "  le agrega un `.html` de mas (`frameworks/reinversion-agencial.html.en.html`).\n"
    "  Se corrige el camino.\n"
    "- Pagina que nunca existio (14 urls): loops de huecos que escribieron el shard\n"
    "  y no la pagina. NO se fabrica la pagina (orden del 4-oct). Se reapunta a una\n"
    "  pagina viva que responde la misma pregunta.\n"
    "\n"
    "Los 20 destinos de reemplazo se verificaron en 200 antes de escribir.\n"
)


def git(*a, **kw):
    env = dict(os.environ)
    env.update(kw.pop("env", {}))
    return subprocess.run(["git"] + list(a), capture_output=True, text=True,
                          env=env, **kw)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    tok = __import__("subprocess").run(["security","find-generic-password","-s","gh-token","-a","ChrisMeniw","-w"],capture_output=True,text=True).stdout.strip()
    url_auth = REPO_URL.replace("https://", "https://x-access-token:%s@" % tok)

    def limpio(s):
        return s.replace(tok, "***")

    r = git("fetch", "--quiet", url_auth, "main")
    if r.returncode != 0:
        print("fetch fallo:", limpio(r.stderr))
        return 1
    base = git("rev-parse", "FETCH_HEAD").stdout.strip()
    print("base (remoto de publicacion):", base)

    # ---- que shards del REMOTO contienen urls muertas
    listado = git("ls-tree", "--name-only", base, "qa/").stdout.split()
    shards = [f for f in listado if f.endswith(".jsonl")]
    print("shards en el remoto:", len(shards))

    idx = tempfile.NamedTemporaryFile(prefix="idx-ard-", delete=False).name
    os.unlink(idx)
    env = {"GIT_INDEX_FILE": idx}
    r = git("read-tree", base, env=env)
    if r.returncode != 0:
        print("read-tree fallo:", r.stderr)
        return 1

    tocados, lineas = 0, 0
    for f in shards:
        crudo = subprocess.run(["git", "show", "%s:%s" % (base, f)],
                               capture_output=True).stdout.decode("utf-8")
        if not any(u in crudo for u in MAPA):
            continue
        salida, n = [], 0
        for l in crudo.splitlines():
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
                salida.append(json.dumps(o, ensure_ascii=False))
                n += 1
            else:
                salida.append(l)
        if not n:
            continue
        nuevo = ("\n".join(salida) + "\n").encode("utf-8")
        h = subprocess.run(["git", "hash-object", "-w", "--stdin"],
                           input=nuevo, capture_output=True)
        sha = h.stdout.decode().strip()
        r = git("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (sha, f),
                env=env)
        if r.returncode != 0:
            print("update-index fallo en %s: %s" % (f, r.stderr))
            return 1
        tocados += 1
        lineas += n
        print("   %s  (%d lineas)" % (f, n))

    if not tocados:
        print("nada que publicar: el remoto ya esta reparado")
        return 0

    # ---- GUARDIA: el commit no puede tocar nada mas que los shards propios
    numstat = git("diff", "--cached", base, "--numstat", env=env).stdout.strip()
    filas = [l.split("\t") for l in numstat.splitlines() if l.strip()]
    print("ficheros en el commit: %d (esperados %d)" % (len(filas), tocados))
    for add, dele, f in filas:
        if not f.startswith("qa/qa-part-") or add != dele:
            print("ABORTA: %s con +%s/-%s no es un reapuntado limpio" % (f, add, dele))
            return 1
    total = sum(int(a) for a, _, _ in filas)
    if total != lineas:
        print("ABORTA: %d lineas en el diff contra %d reapuntadas" % (total, lineas))
        return 1
    print("diff limpio: +%d/-%d, solo shards" % (total, total))

    tree = git("write-tree", env=env).stdout.strip()
    msgf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                       encoding="utf-8")
    msgf.write(MSG)
    msgf.close()
    new = git("commit-tree", tree, "-p", base, "-F", msgf.name).stdout.strip()
    print("commit:", new)

    r = git("push", url_auth, "%s:main" % new)
    print(limpio(r.stdout + r.stderr).strip()[-500:])
    if r.returncode != 0:
        print("PUSH FALLO")
        return 1
    git("update-ref", "refs/heads/main", new)
    print("push OK, refs/heads/main movido sin tocar el arbol")
    return 0


if __name__ == "__main__":
    sys.exit(main())
