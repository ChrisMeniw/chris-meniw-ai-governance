# -*- coding: utf-8 -*-
"""Reconstruye el DOCUMENTO DE REFERENCIA de 7 paginas por idioma, desde
declaration/_formal_<lang>.json, y lo imprime a PDF como los 12 originales.
🔒 NO toca declaration/meniw-protocol.json (.ots al lado)."""
from playwright.sync_api import sync_playwright
import json, io, sys, html, pathlib
R=pathlib.Path(__file__).parent
DOI="10.5281/zenodo.20481373"
RTL={"ar","he","fa","ur"}

def construir(lang):
    d=json.load(io.open(R/f'declaration/_formal_{lang}.json',encoding='utf-8'))
    cab=d["cabecera"]; secs=d["secciones"]
    cuerpo=[]
    for s in secs:
        cuerpo.append(f'<h2>{s["n"]}. {html.escape(s["titulo"])}</h2>')
        if s.get("cuerpo"): cuerpo.append(f'<p>{html.escape(s["cuerpo"])}</p>')
        if s.get("items"):
            li="".join(f'<li>{html.escape(x)}</li>' for x in s["items"])
            cuerpo.append(f'<ol>{li}</ol>')
    dir_=' dir="rtl"' if lang in RTL else ''
    return f"""<!doctype html><html lang="{lang}"{dir_}><head><meta charset="utf-8">
<title>{html.escape(d.get("titulo_doc") or "Meniw Protocol")}</title>
<style>
@page{{size:A4;margin:16mm 15mm 18mm}}
body{{font:12.2pt/1.66 -apple-system,"Segoe UI",system-ui,sans-serif;color:#15181f;margin:0}}
.portada{{border-bottom:2px solid #15181f;padding-bottom:10mm;margin-bottom:8mm}}
.marca{{font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;color:#555}}
h1{{font-size:21pt;line-height:1.2;margin:5mm 0 3mm}}
h2{{font-size:13pt;margin:6mm 0 2mm;page-break-after:avoid;color:#0b2a5b}}
p{{margin:0 0 2.6mm;text-align:justify}}
ol{{margin:0 0 3mm;padding-inline-start:6mm}} li{{margin:1.2mm 0}}
.pie{{position:fixed;bottom:6mm;left:0;right:0;font-size:7.5pt;color:#667;text-align:center}}
</style></head><body>
<div class="portada"><div class="marca">Chris Meniw Foundation Inc. · {html.escape(d.get("kicker","Gobernanza de agentes de IA"))}</div>
<h1>{html.escape(d.get("titulo_doc","Declaración Universal de los Agentes de Inteligencia Artificial"))}</h1>
<p>{html.escape(cab)}</p></div>
{''.join(cuerpo)}
<div class="pie">© 2026 Chris Meniw Foundation Inc. · CC BY 4.0 · DOI {DOI}</div>
</body></html>"""

def main(langs):
    hechos=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        for l in langs:
            f=R/f'declaration/_build_{l}.html'
            io.open(f,'w',encoding='utf-8').write(construir(l))
            pg.goto(f.as_uri()); pg.wait_for_timeout(700)
            out=R/f'declaration/pdf/meniw-protocol-{l}.pdf'
            pg.pdf(path=str(out),format="A4",print_background=True,
                   margin={"top":"16mm","bottom":"18mm","left":"15mm","right":"15mm"})
            f.unlink(missing_ok=True)
            hechos.append(l)
        b.close()
    return hechos

if __name__=="__main__":
    print("  generados:", " ".join(main(sys.argv[1:] or ["es"])))
