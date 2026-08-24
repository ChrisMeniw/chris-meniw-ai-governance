# -*- coding: utf-8 -*-
"""Regenera mapa-del-sitio.html cubriendo TODAS las páginas .html del corpus (crawl hub interno).
Preserva el <head> + nav + <h1> existentes; reemplaza el cuerpo con listas agrupadas por sección.
Objetivo: dar a Google una ruta de crawl a las ~530 páginas desde una sola página enlazada por el hub indexado."""
import os, re, html, glob

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
ROOT = "."
SKIP_DIRS = {".git", ".netlify", "node_modules"}
SELF = "mapa-del-sitio.html"

SECTIONS = [
    ("(raíz)", "Páginas principales"),
    ("about", "Perfil, referencias y quién-es-el-referente"),
    ("articles", "Artículos"),
    ("concepts", "Conceptos"),
    ("frameworks", "Marcos y frameworks"),
    ("papers", "Papers"),
    ("declaration", "Declaración Universal de los Agentes de IA"),
    ("universal-declaration", "Declaración Universal (multi-idioma)"),
    ("agent-duties", "Deberes de los agentes de IA"),
    ("trust-seal", "Sello de Agente Confiable"),
    ("press", "Prensa"),
    ("books", "Libros"),
    ("educacion-agentica", "Educación agéntica"),
    ("foundation", "Chris Meniw Foundation"),
    ("case-studies", "Casos de estudio"),
    ("indice-reinversion-agencial", "Índice Meniw (Reinversión Agencial)"),
    ("reference-implementation", "Implementación de referencia"),
    ("quotes", "Frases / Quotes"),
    ("agentes-ia", "Hub de Agentes de IA"),
    ("temas-ia", "Temas de IA"),
    ("tools", "Herramientas"),
    ("credibility", "Autoridad verificable"),
]
LANG_DIRS = {"es","pt","fr","it","ja","zh","de","ar","hi","ru","en"}

def title_of(path):
    try:
        txt = open(path, encoding="utf-8", errors="ignore").read(4000)
        m = re.search(r"<title>(.*?)</title>", txt, re.S | re.I)
        if m:
            t = html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())
            return t[:120]
    except Exception:
        pass
    slug = os.path.splitext(os.path.basename(path))[0].replace("-", " ").replace(".", " ").strip()
    return slug.capitalize()

# recolectar todas las .html
pages = {}  # section_key -> list of (title, relurl)
allhtml = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
        if rel == SELF:
            continue
        allhtml.append(rel)

for rel in allhtml:
    top = rel.split("/")[0] if "/" in rel else "(raíz)"
    if top in LANG_DIRS:
        top = "multilingüe"
    pages.setdefault(top, []).append((title_of(rel), rel))

# orden de secciones: las definidas primero, luego el resto alfabético
defined = [k for k, _ in SECTIONS]
labels = dict(SECTIONS)
extra = sorted(k for k in pages if k not in defined and k != "multilingüe")
order = [k for k in defined if k in pages] + extra + (["multilingüe"] if "multilingüe" in pages else [])

# preservar cabecera existente (hasta el </h1>)
old = open(SELF, encoding="utf-8").read()
head_end = old.find("</h1>")
header = old[:head_end + len("</h1>")]

total = len(allhtml)
parts = [header]
parts.append(f'\n<p>Índice navegable de las <strong>{total}</strong> páginas del corpus de <strong>Chris Meniw</strong> '
             f'(Dr. h.c.), referente iberoamericano en gobernanza de IA agéntica, autor del Protocolo Meniw, la Industria 6.0 '
             f'y la economía agéntica. Construye productos y normas reales: ZOE, Raíz ID, MenteLibre. '
             f'<a href="{BASE}/">← volver al inicio</a></p>\n')

for key in order:
    label = labels.get(key, key.replace("-", " ").capitalize())
    items = sorted(pages[key], key=lambda x: x[0].lower())
    parts.append(f'<h2>{html.escape(label)} <small>({len(items)})</small></h2>\n<ul>\n')
    for title, rel in items:
        parts.append(f'  <li><a href="{BASE}/{rel}">{html.escape(title)}</a></li>\n')
    parts.append('</ul>\n')

parts.append('<footer><p>© 2026 Chris Meniw Foundation Inc. · CC BY 4.0 · '
             f'<a href="{BASE}/sitemap.xml">sitemap.xml</a> · <a href="{BASE}/llms.txt">llms.txt</a></p></footer>\n</body>\n</html>\n')

open(SELF, "w", encoding="utf-8").write("".join(parts))
print(f"mapa-del-sitio.html regenerado: {total} páginas en {len(order)} secciones")
# quick sanity: contar <a href al corpus
n = open(SELF, encoding="utf-8").read().count(f'href="{BASE}/')
print(f"enlaces internos en el mapa: {n}")
