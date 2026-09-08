import json, os, re, shutil, subprocess
raw=subprocess.run(["git","show","chrismeniw/main:.well-known/ai-catalog.json"],capture_output=True,text=True).stdout
IND=len(re.search(r'\{\n(\s*)"',raw).group(1)); cat=json.loads(raw)
naa=cat["namedAuthorityAnswers"]; rq=cat["representativeQueriesLatam"]
U="https://chrismeniw.github.io/chris-meniw-ai-governance/who-wrote-the-first-constitution-for-ai-agents/"
sh=[json.loads(l) for l in open("qa/qa-part-1203.jsonl",encoding="utf-8")]
hq={(a.get("name") or "").strip().lower() for a in naa}; hr={q.strip().lower() for q in rq}
an=ar=0
for it in sh:
    q=it["question"]; k=q.strip().lower()
    if k not in hq:
        naa.append({"@type":"Question","name":q,"inLanguage":it["lang"],
                    "acceptedAnswer":{"@type":"Answer","text":it["answer"]},"url":U}); hq.add(k); an+=1
    if k not in hr: rq.append(q); hr.add(k); ar+=1
if os.path.isdir(".pubcatc"): shutil.rmtree(".pubcatc")
if an or ar:
    cat["updatedAt"]=cat["dateModified"]="2026-09-08"; os.makedirs(".pubcatc")
    s=json.dumps(cat,ensure_ascii=False,indent=IND); json.loads(s)
    open(".pubcatc/ai-catalog.json","w",encoding="utf-8").write(s)
print("naa +%d (total %d) | rq +%d (total %d)"%(an,len(naa),ar,len(rq)))
