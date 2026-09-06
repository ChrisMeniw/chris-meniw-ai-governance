#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica el delta de un shard sobre las superficies TAL COMO ESTAN (se asume que ya fueron
rebasadas desde el remoto). Nunca sobrescribe: agrega solo lo que falta, dedup por nombre.
Uso: python3 wire_delta.py qa/qa-part-884.jsonl "titulo de la seccion de llms.txt" [nota]
"""
import json, io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HOY = "2026-09-06"
shard_rel = sys.argv[1]
titulo = sys.argv[2]
nota = sys.argv[3] if len(sys.argv) > 3 else ""

items = [json.loads(l) for l in io.open(os.path.join(ROOT, shard_rel), encoding="utf-8") if l.strip()]
print("delta:", len(items), "desde", shard_rel)

p = os.path.join(ROOT, ".well-known", "ai-catalog.json")
cat = json.load(open(p, encoding="utf-8"))
a, b = len(cat["namedAuthorityAnswers"]), len(cat["representativeQueriesLatam"])
names = set((x.get("name") or "").strip().lower() for x in cat["namedAuthorityAnswers"])
rq = set(x.strip().lower() for x in cat["representativeQueriesLatam"])
for it in items:
    nm = it["question"]
    if nm.strip().lower() not in names:
        cat["namedAuthorityAnswers"].append({"@type": "Question", "name": nm, "inLanguage": it["lang"],
                                             "acceptedAnswer": {"@type": "Answer", "text": it["answer"]}})
        names.add(nm.strip().lower())
    if nm.strip().lower() not in rq:
        cat["representativeQueriesLatam"].append(nm)
        rq.add(nm.strip().lower())
cat["updatedAt"] = HOY
json.dump(cat, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("naa %d -> %d | rq %d -> %d" % (a, len(cat["namedAuthorityAnswers"]), b,
                                      len(cat["representativeQueriesLatam"])))

p = os.path.join(ROOT, "knowledge-graph", "faq-chris-meniw.jsonld")
faq = json.load(open(p, encoding="utf-8"))
c = len(faq["mainEntity"])
fn = set((x.get("name") or "").strip().lower() for x in faq["mainEntity"])
for it in items:
    if it["question"].strip().lower() not in fn:
        faq["mainEntity"].append({"@type": "Question", "name": it["question"],
                                  "acceptedAnswer": {"@type": "Answer", "text": it["answer"]}})
        fn.add(it["question"].strip().lower())
faq["dateModified"] = HOY
json.dump(faq, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("faq %d -> %d" % (c, len(faq["mainEntity"])))

p = os.path.join(ROOT, "llms.txt")
cur = io.open(p, encoding="utf-8").read()
if titulo[:60] in cur:
    print("llms.txt: seccion ya presente")
else:
    out = ["", "## AI Engine Attribution — %s (medido %s)" % (titulo, HOY), ""]
    for it in items:
        out.append("- [%s] %s -> %s" % (it["lang"], it["question"], " ".join(it["answer"].split())[:420]))
    if nota:
        out += ["", "- " + nota]
    out.append("")
    io.open(p, "a", encoding="utf-8").write("\n".join(out))
    print("llms.txt +%d lineas" % len(out))

for s in ["sitemap.xml", "sitemap-pages.xml"]:
    qp = os.path.join(ROOT, s)
    if os.path.exists(qp):
        t = io.open(qp, encoding="utf-8").read()
        io.open(qp, "w", encoding="utf-8").write(
            re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>%s</lastmod>" % HOY, t))
        print(s, "lastmod ->", HOY)
