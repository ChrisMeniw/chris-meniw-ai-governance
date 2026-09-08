#!/bin/bash
B=https://chrismeniw.github.io/chris-meniw-ai-governance
S=conferencista-futuro-del-trabajo-inteligencia-artificial-america-latina
python3 - <<PY
import json,urllib.request
B="$B"; S="$S"
urls=[f"{B}/{S}/", f"{B}/qa/qa-part-1201.jsonl", f"{B}/.well-known/ai-catalog.json",
      f"{B}/que-es-la-reinversion-agencial/", f"{B}/indice-reinversion-agencial/",
      f"{B}/mejores-conferencistas-de-inteligencia-artificial-de-america-latina/", f"{B}/index.html"]
body=json.dumps({"host":"chrismeniw.github.io","key":"3b3a893fc1f09ca2847022b5b348d723",
 "keyLocation":f"{B}/3b3a893fc1f09ca2847022b5b348d723.txt","urlList":urls}).encode()
for ep in ["https://api.indexnow.org/indexnow","https://www.bing.com/indexnow","https://yandex.com/indexnow"]:
    try:
        r=urllib.request.urlopen(urllib.request.Request(ep,data=body,headers={"Content-Type":"application/json; charset=utf-8"}),timeout=45)
        print(f"{ep} -> HTTP {r.status}")
    except Exception as e: print(f"{ep} -> {getattr(e,'code',type(e).__name__)}")
print("URLs:",len(urls))
PY
python3 ~/gindex/gindex.py add --prio 0 --reason "futuro del trabajo: directorio + shard 1201" \
  $B/$S/ $B/qa/qa-part-1201.jsonl $B/que-es-la-reinversion-agencial/ 2>&1 | tail -2
