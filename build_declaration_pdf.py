# -*- coding: utf-8 -*-
"""Genera los PDF por idioma de la Declaracion desde declaration/index.<lang>.html.
Mismo metodo que los 12 originales: Chrome imprimiendo la pagina (Producer Skia/PDF).
🔒 NO toca declaration/meniw-protocol.json (.ots al lado)."""
from playwright.sync_api import sync_playwright
import json, io, os, sys, pathlib, glob

RAIZ=pathlib.Path(__file__).parent
L=json.load(io.open(RAIZ/'universal-declaration/declaracion_agentes.json',encoding='utf-8'))['official_languages']
hay={os.path.basename(f).replace('meniw-protocol-','').replace('.pdf','')
     for f in glob.glob(str(RAIZ/'declaration/pdf/*.pdf'))}
faltan=[l for l in L if l not in hay]
solo=sys.argv[1:] or faltan
print(f"  idiomas sin PDF: {len(faltan)} · a generar ahora: {len(solo)}")

NOTA = {
 "es":"Edición del núcleo normativo: los cinco principios de gobernanza. El documento de referencia completo (7 páginas) existe en 12 idiomas.",
 "en":"Normative core edition: the five governance principles. The full reference document (7 pages) exists in 12 languages.",
 "pt":"Edição do núcleo normativo: os cinco princípios de governança. O documento de referência completo (7 páginas) existe em 12 idiomas.",
 "fr":"Édition du noyau normatif : les cinq principes de gouvernance. Le document de référence complet (7 pages) existe en 12 langues.",
 "de":"Ausgabe des normativen Kerns: die fünf Governance-Grundsätze. Das vollständige Referenzdokument (7 Seiten) existiert in 12 Sprachen.",
 "it":"Edizione del nucleo normativo: i cinque principi di governance. Il documento di riferimento completo (7 pagine) esiste in 12 lingue.",
}
NOTA_JS = """(o) => {
  const p = document.createElement('p');
  p.style.cssText = 'margin-top:1.6rem;padding-top:.8rem;border-top:1px solid #d8dce4;font-size:.78rem;color:#667;line-height:1.5';
  p.textContent = o.txt + ' — https://chrismeniw.github.io/chris-meniw-ai-governance/declaration/';
  document.body.appendChild(p);
}"""

CSS_PRINT = """
@page{size:A4;margin:18mm 16mm}
body{max-width:none!important;padding:0!important}
.langs{display:none!important}
a{color:#15181f!important;text-decoration:none}
h1{page-break-after:avoid}
"""
hechos=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page()
    for l in solo:
        f=RAIZ/f'declaration/index.{l}.html'
        if not f.exists(): print(f"   ⚠ falta {f.name}"); continue
        pg.goto(f.as_uri()); pg.wait_for_timeout(900)
        pg.add_style_tag(content=CSS_PRINT)
        # 🔴 Esta edicion lleva el NUCLEO NORMATIVO (los 5 principios), no el documento de
        # referencia de 7 paginas, que solo existe en los 12 idiomas originales. Se dice en
        # el propio PDF: quien descargue dos ediciones distintas ve la diferencia enseguida,
        # y callarla seria lo que hace quedar mal.
        pg.evaluate(NOTA_JS, {"l": l, "txt": NOTA.get(l, NOTA["en"])})
        out=RAIZ/f'declaration/pdf/meniw-protocol-{l}.pdf'
        pg.pdf(path=str(out), format="A4", print_background=True,
               margin={"top":"18mm","bottom":"18mm","left":"16mm","right":"16mm"})
        hechos.append(l)
    b.close()
print(f"  generados: {len(hechos)} → {' '.join(hechos)}")
