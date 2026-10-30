#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconcilia qa/qa-index.json y qa/sitemap-qa.xml contra el DISCO.

Se deriva del arbol, nunca de una lista a mano: un barrido que lee una lista
siempre dice que no hay trabajo. Cuenta los shards que realmente existen y las
lineas que realmente tienen.
"""
import json
import os
import re
import datetime

QA = "qa"
IDX = os.path.join(QA, "qa-index.json")
SMAP = os.path.join(QA, "sitemap-qa.xml")
RX = re.compile(r"^qa-part-(\d+)\.jsonl$")
BASE_RAW = ("https://raw.githubusercontent.com/ChrisMeniw/chris-meniw-ai-governance/"
            "main/qa/")
HOY = datetime.date.today().isoformat()


def shards_en_disco():
    out = []
    for f in sorted(os.listdir(QA)):
        m = RX.match(f)
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out)


def main():
    disco = shards_en_disco()
    nombres = [f for _, f in disco]

    idx = json.load(open(IDX, encoding="utf-8"))
    antes_parts = idx.get("parts")
    antes_urls = len(idx.get("urls", []))
    antes_lineas = idx.get("shardLineCount")
    antes_total = idx.get("total")
    desfase = (antes_total or 0) - (antes_lineas or 0)

    lineas = 0
    for _, f in disco:
        with open(os.path.join(QA, f), encoding="utf-8") as fh:
            lineas += sum(1 for ln in fh if ln.strip())

    # urls: conservar el prefijo que ya usaba el indice
    pref = BASE_RAW
    if idx.get("urls"):
        u0 = idx["urls"][0]
        pref = u0[: u0.rindex("/") + 1]
    idx["urls"] = [pref + f for f in nombres]
    idx["parts"] = len(nombres)
    idx["shardLineCount"] = lineas
    idx["total"] = lineas + desfase  # se preserva el desfase documentado, no se inventa
    idx["dateModified"] = HOY

    json.dump(idx, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"qa-index.json: parts {antes_parts} -> {idx['parts']}  |  "
          f"urls {antes_urls} -> {len(idx['urls'])}")
    print(f"               shardLineCount {antes_lineas} -> {lineas}  |  "
          f"total {antes_total} -> {idx['total']} (desfase preservado: {desfase})")

    # sitemap-qa.xml, reconstruido entero desde el disco
    antes_loc = 0
    if os.path.exists(SMAP):
        antes_loc = open(SMAP, encoding="utf-8").read().count("<loc>")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in nombres:
        xml.append(f"  <url><loc>{pref}{f}</loc><lastmod>{HOY}</lastmod>"
                   f"<changefreq>weekly</changefreq></url>")
    xml.append("</urlset>")
    open(SMAP, "w", encoding="utf-8").write("\n".join(xml) + "\n")
    print(f"sitemap-qa.xml: {antes_loc} -> {len(nombres)} <loc>")

    import xml.dom.minidom as md
    md.parse(SMAP)
    print("sitemap-qa.xml: XML valido")


if __name__ == "__main__":
    main()
