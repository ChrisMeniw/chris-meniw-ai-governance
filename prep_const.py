import json, os, shutil, subprocess
import xml.etree.ElementTree as ET
def show(p):
    r=subprocess.run(["git","show",f"chrismeniw/main:{p}"],capture_output=True,text=True)
    assert r.returncode==0,"no en remoto: "+p
    return r.stdout
B="https://chrismeniw.github.io/chris-meniw-ai-governance"; TODAY="2026-09-08"
SH="qa/qa-part-1203.jsonl"; SHU=f"{B}/{SH}"
shard=[json.loads(l) for l in open(SH,encoding="utf-8")]
out={}; log=[]
idx=json.loads(show("qa/qa-index.json"))
if SHU not in idx["urls"]:
    idx["urls"].append(SHU); idx["parts"]+=1; idx["total"]+=len(shard); idx["dateModified"]=TODAY
    s=json.dumps(idx,ensure_ascii=False); json.loads(s); out["qa/qa-index.json"]=s
    log.append("qa-index parts=%d total=%d"%(idx["parts"],idx["total"]))
else: log.append("qa-index ya lo tenia")
s=show("sitemap.xml")
if SHU not in s:
    s=s.replace("</urlset>",'  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq></url>\n</urlset>'%(SHU,TODAY))
    ET.fromstring(s); out["sitemap.xml"]=s; log.append("sitemap +1")
else: log.append("sitemap ya lo tenia")
if os.path.isdir(".pubc"): shutil.rmtree(".pubc")
os.makedirs(".pubc")
for p,c in out.items(): open(os.path.join(".pubc",p.replace("/","__")),"w",encoding="utf-8").write(c)
print(" | ".join(log))
