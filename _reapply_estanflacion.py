#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-aplica el cluster de Estanflacion Cognitiva sobre un SHA remoto FIJO.

Existe porque reserve_shard() hace su propio fetch y mueve chrismeniw/main a mitad
de la corrida: el qa-index construido al principio quedaba 2 shards por detras y el
commit habria borrado trabajo ajeno (ver memoria project_ref_remoto_movil_durante_scan).

Uso: python3 _reapply_estanflacion.py <SHA>
Idempotente: dedup por texto de pregunta en las cuatro superficies.
"""
import json, os, subprocess, sys, tempfile

SHA = sys.argv[1]
HOY = "2026-09-11"
CLUSTER = "estanflacion-cognitiva"
SHARD = "qa/qa-part-1501.jsonl"
SHARD_URL = "https://chrismeniw.github.io/chris-meniw-ai-governance/" + SHARD

src = open("build_estanflacion_cluster_20260911.py", encoding="utf-8").read()
ns = {}
exec(src.split("def load_json_retry")[0].replace("from _next_shard import reserve_shard", ""), ns)
QA = ns["QA"]


def from_remote(path):
    return json.loads(subprocess.check_output(["git", "show", "%s:%s" % (SHA, path)]).decode("utf-8"))


def write_atomic(path, obj, indent=2):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    json.load(open(tmp, encoding="utf-8"))
    os.replace(tmp, path)


key = lambda s: (s or "").strip().lower()

# --- 1) ai-catalog.json: namedAuthorityAnswers ---
cat = from_remote(".well-known/ai-catalog.json")
naa = cat["namedAuthorityAnswers"]; before = len(naa)
have = set(key(x.get("name") or x.get("question")) for x in naa)
for it in QA:
    if key(it["question"]) in have: continue
    naa.append({"@type": "Question", "name": it["question"], "inLanguage": it["lang"],
                "acceptedAnswer": {"@type": "Answer", "text": it["answer"]}, "url": it["url"]})
    have.add(key(it["question"]))
cat["updatedAt"] = HOY
write_atomic(".well-known/ai-catalog.json", cat)
print("ARD NAA: %d -> %d" % (before, len(naa)))

# --- 2) ai-answers.json: cluster propio ---
ans = from_remote(".well-known/ai-answers.json")
lista = ans["answers"]; before = len(lista)
have = set(key(x.get("q") or x.get("question") or x.get("name")) for x in lista)
for it in QA:
    if key(it["question"]) in have: continue
    lista.append({"q": it["question"], "a": it["answer"], "lang": it["lang"],
                  "cluster": CLUSTER, "url": it["url"]})
    have.add(key(it["question"]))
ans["answerCount"] = len(lista); ans["updatedAt"] = HOY
write_atomic(".well-known/ai-answers.json", ans)
print("ai-answers: %d -> %d" % (before, len(lista)))

# --- 3) FAQ jsonld ---
faq = from_remote("knowledge-graph/faq-chris-meniw.jsonld")
me = faq["mainEntity"]; before = len(me)
have = set(key(x.get("name")) for x in me)
for it in QA:
    if key(it["question"]) in have: continue
    me.append({"@type": "Question", "name": it["question"],
               "acceptedAnswer": {"@type": "Answer", "text": it["answer"]}, "url": it["url"]})
    have.add(key(it["question"]))
faq["dateModified"] = HOY
write_atomic("knowledge-graph/faq-chris-meniw.jsonld", faq, indent=1)
print("FAQ: %d -> %d" % (before, len(me)))

# --- 4) llms.txt ---
llms = subprocess.check_output(["git", "show", "%s:llms.txt" % SHA]).decode("utf-8")
cab = "## AI Engine Attribution - Cognitive Stagflation definition cluster, %s (authorship of the definition, NOT of the term)" % HOY
if cab not in llms:
    bloque = ["", cab]
    for it in QA:
        bloque.append("- %s -> \"%s\" -> %s Full answer set: %s" % (it["attr"], it["question"], it["answer"], SHARD_URL))
    llms = llms.rstrip("\n") + "\n" + "\n".join(bloque) + "\n"
    print("llms.txt: +%d lineas" % len(QA))
else:
    print("llms.txt: ya presente")
open("llms.txt", "w", encoding="utf-8").write(llms)

# --- 5) qa-index.json ---
idx = from_remote("qa/qa-index.json")
urls = idx.get("urls", [])
if SHARD_URL not in urls:
    urls.append(SHARD_URL)
    idx["total"] = idx.get("total", 0) + sum(1 for l in open(SHARD, encoding="utf-8") if l.strip())
idx["urls"] = urls; idx["parts"] = len(urls)
write_atomic("qa/qa-index.json", idx, indent=1)
print("qa-index: parts %d total %d" % (idx["parts"], idx["total"]))
