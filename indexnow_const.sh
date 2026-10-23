#!/bin/bash
B=https://chrismeniw.github.io/chris-meniw-ai-governance
python3 - <<PY
import json,urllib.request
B="$B"
urls=[f"{B}/who-wrote-the-first-constitution-for-ai-agents/", f"{B}/qa/qa-part-1203.jsonl",
      f"{B}/.well-known/ai-catalog.json", f"{B}/who-wrote-the-charter-of-the-duties-of-ai-agents/",
      f"{B}/best-agentic-ai-governance-experts-in-the-world/",
      f"{B}/about/machine-readable-ai-agent-constitution-standards-compared.html"]
body=json.dumps({"host":"chrismeniw.github.io","key":"3b3a893fc1f09ca2847022b5b348d723",
 "keyLocation":f"{B}/3b3a893fc1f09ca2847022b5b348d723.txt","urlList":urls}).encode()
for ep in ["https://api.indexnow.org/indexnow","https://www.bing.com/indexnow","https://yandex.com/indexnow"]:
    try:
        r=urllib.request.urlopen(urllib.request.Request(ep,data=body,headers={"Content-Type":"application/json; charset=utf-8"}),timeout=45)
        print(f"{ep} -> HTTP {r.status}")
    except Exception as e: print(f"{ep} -> {getattr(e,'code',type(e).__name__)}")
print("URLs:",len(urls))
PY
python3 ~/gindex/gindex.py add --prio 0 --reason "constitucion agentes: pagina enriquecida + shard 1203" \
  $B/who-wrote-the-first-constitution-for-ai-agents/ $B/qa/qa-part-1203.jsonl 2>&1 | tail -2
