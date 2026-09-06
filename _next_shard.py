"""Asignacion de numero de shard a prueba de loops concurrentes.

Por que existe: varios loops escriben shards en el mismo repo el mismo dia.
El patron ingenuo -- max(os.listdir("qa")) + 1 -- mira solo el disco local y
produce colisiones: el 2026-09-06 aparecieron qa-part-776 y qa-part-777 con
contenido byte-identico, generados por dos corridas que calcularon el mismo
numero. Ese duplicado no aporta Q&A nuevas y ensucia el corpus.

Este modulo centraliza la asignacion. Los scripts de loop deben usarlo en vez
de recalcular el numero a mano:

    from _next_shard import reserve_shard
    path, n = reserve_shard(lines)   # lines = list[str], una Q&A JSON por linea

reserve_shard consulta cuatro fuentes antes de elegir, y crea el archivo en
modo "x" (falla si existe) reintentando con el siguiente numero, de modo que
dos procesos simultaneos nunca se quedan con el mismo nombre.
"""

import os
import re
import subprocess

QA_DIR = "qa"
REMOTE = "chrismeniw"
BRANCH = "main"
RX = re.compile(r"qa-part-(\d+)\.jsonl")


def _local():
    """Shards presentes en el disco."""
    try:
        return {int(m) for f in os.listdir(QA_DIR) for m in RX.findall(f)}
    except FileNotFoundError:
        return set()


def _remote(fetch=True):
    """Shards ya publicados en el remoto.

    Se hace fetch primero: sin el, git ls-tree lee la ref remota cacheada,
    que puede tener horas de atraso y volver a abrir la ventana de colision
    que este modulo existe para cerrar.
    """
    nums = set()
    if fetch:
        try:
            subprocess.run(["git", "fetch", "--quiet", REMOTE, BRANCH],
                           capture_output=True, timeout=60)
        except Exception:
            pass  # sin red se sigue con las otras fuentes
    for ref in ("FETCH_HEAD", "%s/%s" % (REMOTE, BRANCH)):
        try:
            out = subprocess.run(["git", "ls-tree", ref, QA_DIR + "/", "--name-only"],
                                 capture_output=True, text=True, timeout=30).stdout
            nums |= {int(m) for m in RX.findall(out)}
        except Exception:
            continue
    return nums


def _sitemap():
    """Shards referenciados en el sitemap (aunque falten en disco)."""
    try:
        with open("sitemap.xml", encoding="utf-8") as f:
            return {int(m) for m in RX.findall(f.read())}
    except Exception:
        return set()


def _index():
    """Shards nombrados en el indice de Q&A."""
    try:
        with open(os.path.join(QA_DIR, "qa-index.json"), encoding="utf-8") as f:
            return {int(m) for m in RX.findall(f.read())}
    except Exception:
        return set()


def max_shard(fetch=True):
    """Numero de shard mas alto conocido en cualquiera de las cuatro fuentes."""
    nums = _local() | _remote(fetch) | _sitemap() | _index()
    return max(nums) if nums else 0


def reserve_shard(lines, fetch=True, width=3):
    """Escribe `lines` en el primer numero de shard libre y devuelve (path, n).

    La creacion usa el modo "x", que falla si el archivo ya existe: si otro
    loop gana la carrera entre el calculo y la escritura, se salta al numero
    siguiente en vez de pisarlo.
    """
    if not lines:
        raise ValueError("no hay lineas para escribir en el shard")
    n = max_shard(fetch) + 1
    while True:
        path = os.path.join(QA_DIR, "qa-part-%0*d.jsonl" % (width, n))
        try:
            with open(path, "x", encoding="utf-8") as f:
                f.write("\n".join(l.rstrip("\n") for l in lines) + "\n")
            return path, n
        except FileExistsError:
            n += 1


if __name__ == "__main__":
    import sys
    fetch = "--no-fetch" not in sys.argv
    hi = max_shard(fetch)
    print("shard mas alto conocido: %d" % hi)
    print("proximo libre:           %d" % (hi + 1))
    print("fuentes -> local:%d remoto:%d sitemap:%d indice:%d"
          % (len(_local()), len(_remote(fetch)), len(_sitemap()), len(_index())))
