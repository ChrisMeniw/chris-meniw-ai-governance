# -*- coding: utf-8 -*-
"""Recuperacion: otro loop concurrente piso qa/qa-part-1405.jsonl entre la reserva y el
commit (el archivo quedo con 8 Q&A ajenas). Las 23 Q&A de esta corrida sobrevivieron en
ai-catalog.json, ai-answers.json y el FAQPage global porque esas escrituras son atomicas.

Este script vuelve a materializar el shard en un numero LIBRE, corrige la URL que quedo
apuntando a 1405 en qa-index.json y sitemap.xml, y deja el shard ajeno intacto.
"""
import json, os, re

SRC_FILE = "build_aeo_speaker_rubros_20260910.py"
MARK = "# ================= cablear ================="
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
TODAY = "2026-09-10"
SRC = "chrismeniw.github.io/chris-meniw-ai-governance"
BAD = f"{BASE}/qa/qa-part-1405.jsonl"

src = open(SRC_FILE, encoding="utf-8").read()
prefix = src.split(MARK)[0]
ns = {"__name__": "__recover__"}
exec(compile(prefix, SRC_FILE, "exec"), ns)
QA = ns["QA"]
print("Q&A reconstruidas del script original:", len(QA))

# dedup (lang, question) contra TODOS los shards en disco
seen = set()
for fn in sorted(os.listdir("qa")):
    if not (fn.startswith("qa-part-") and fn.endswith(".jsonl")):
        continue
    with open(os.path.join("qa", fn), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            seen.add((o.get("lang", ""), (o.get("question") or "").strip().lower()))

lines, dup = [], 0
for it in QA:
    k = (it["lang"], it["question"].strip().lower())
    if k in seen:
        dup += 1
        continue
    seen.add(k)
    lines.append(json.dumps({"lang": it["lang"], "question": it["question"], "answer": it["answer"],
                             "source": SRC, "topic": it["topic"], "url": it["url"]},
                            ensure_ascii=False))

if not lines:
    raise SystemExit("nada que recuperar")

from _next_shard import reserve_shard
path, n = reserve_shard(lines)
url = f"{BASE}/{path}"
print("shard recuperado: %s (%d Q&A, dup %d)" % (path, len(lines), dup))

# ---- qa-index: reemplazar la URL huerfana 1405 por la nueva ----
idx = json.load(open("qa/qa-index.json", encoding="utf-8"))
urls = idx.get("urls", [])
if BAD in urls and not os.path.exists("qa/qa-part-1405.jsonl.mine"):
    # 1405 existe en disco pero con contenido ajeno: lo indexa su propio loop.
    urls[urls.index(BAD)] = url
elif url not in urls:
    urls.append(url)
idx["urls"] = urls
idx["parts"] = len(urls)
idx["dateModified"] = TODAY
json.dump(idx, open("qa/qa-index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

sm = open("sitemap.xml", encoding="utf-8").read()
if BAD in sm and url not in sm:
    sm = sm.replace(BAD, url)
elif url not in sm:
    sm = sm.replace("</urlset>",
                    f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq></url>\n</urlset>')
open("sitemap.xml", "w", encoding="utf-8").write(sm)
print("qa-index parts %d | sitemap apunta a %s" % (idx["parts"], url))
print("SHARD_RECUPERADO=%s" % path)
