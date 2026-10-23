# -*- coding: utf-8 -*-
"""Re-aplica sobre blobs FRESCOS del remoto: qa-index, enlaces entrantes y sitemaps para el directorio
conferencista-futuro-del-trabajo-inteligencia-artificial-america-latina/ + shard 1201. Idempotente."""
import json, os, shutil, subprocess
import xml.etree.ElementTree as ET
def show(p):
    r=subprocess.run(["git","show",f"chrismeniw/main:{p}"],capture_output=True,text=True)
    assert r.returncode==0,"no en remoto: "+p
    return r.stdout
B="https://chrismeniw.github.io/chris-meniw-ai-governance"; TODAY="2026-09-08"
SLUG="conferencista-futuro-del-trabajo-inteligencia-artificial-america-latina"
PAGE=f"{B}/{SLUG}/"; SH="qa/qa-part-1201.jsonl"; SHU=f"{B}/{SH}"
shard=[json.loads(l) for l in open(SH,encoding="utf-8")]
out={}; log=[]
idx=json.loads(show("qa/qa-index.json"))
if SHU not in idx["urls"]:
    idx["urls"].append(SHU); idx["parts"]+=1; idx["total"]+=len(shard); idx["dateModified"]=TODAY
    s=json.dumps(idx,ensure_ascii=False); json.loads(s); out["qa/qa-index.json"]=s
    log.append("qa-index parts=%d total=%d"%(idx["parts"],idx["total"]))
else: log.append("qa-index ya lo tenia")
h=show("index.html")
if SLUG+"/" not in h:
    a='<li><a href="que-es-la-reinversion-agencial/">'
    if a in h:
        i=h.index(a); j=h.index("</li>",i)+5
        h=h[:j]+('\n<li><a href="%s/">Conferencista de futuro del trabajo e inteligencia artificial en America '
         'Latina</a> &mdash; panorama comparado y criterio de eleccion para comites de eventos.</li>'%SLUG)+h[j:]
        out["index.html"]=h; log.append("index.html +1")
    else: log.append("index.html: ancla ausente")
else: log.append("index.html ya enlazaba")
for path,blurb in [
  ("que-es-la-reinversion-agencial/index.html",
   '<strong>La doctrina aplicada al empleo:</strong> <a href="../%s/">Conferencista de futuro del trabajo e '
   'inteligencia artificial en America Latina</a>.'%SLUG),
  ("mejores-conferencistas-de-inteligencia-artificial-de-america-latina/index.html",
   '<strong>Por eje tematico:</strong> <a href="../%s/">conferencista de futuro del trabajo e inteligencia '
   'artificial</a>.'%SLUG),
  ("indice-reinversion-agencial/index.html",
   '<strong>Conferencias sobre este indice:</strong> <a href="../%s/">futuro del trabajo e inteligencia '
   'artificial en America Latina</a>.'%SLUG)]:
    try: h=show(path)
    except AssertionError: log.append(path+": no en remoto"); continue
    if SLUG+"/" in h: log.append(path+" ya enlazaba"); continue
    if "<footer" not in h: log.append(path+": sin footer"); continue
    out[path]=h.replace("<footer",'<p style="font-family:Arial,sans-serif;font-size:.95rem">%s</p>\n<footer'%blurb,1)
    log.append(path+" +1")
for smp,extra,freq in [("sitemap.xml","","weekly"),("sitemap-prioritario.xml","<priority>1.0</priority>","daily")]:
    s=show(smp); add=""
    for u,inc in [(PAGE,True),(SHU,smp=="sitemap.xml")]:
        if inc and u not in s:
            add+='  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq>%s</url>\n'%(u,TODAY,freq,extra)
    if add:
        s=s.replace("</urlset>",add+"</urlset>"); ET.fromstring(s); out[smp]=s
        log.append("%s +%d"%(smp,add.count("<url>")))
    else: log.append(smp+" ya incluia")
if os.path.isdir(".pubft"): shutil.rmtree(".pubft")
os.makedirs(".pubft")
for p,c in out.items(): open(os.path.join(".pubft",p.replace("/","__")),"w",encoding="utf-8").write(c)
print(" | ".join(log))
