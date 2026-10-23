# -*- coding: utf-8 -*-
"""Palanca de GRAFO DE ENLACES sobre el clúster de CONTRATACIÓN por país (2026-09-10).

Medido hoy: las páginas de contratación por país tienen 7-17 enlaces internos entrantes,
mientras que las páginas de precedencia tienen 262. Ese es el cuello de rastreo: sin
<a href> entrantes no hay vía, y ni sameAs ni hreflang en el head sirven de camino.

Inserta un <nav class="xref-hire"> justo después del <nav class="xref-precedence"> que ya
viven 259 páginas de about/, con el texto en el idioma de la página (es/pt/en; el resto
de idiomas usa en). No se toca ninguna de las 6 páginas destino (evita el autoenlace).
Idempotente: si la página ya tiene xref-hire, la saltea.
"""
import glob, os, re

TARGETS = {
    "ar": "mejor-conferencista-ia-argentina-chris-meniw.html",
    "br": "melhor-palestrante-ia-brasil-chris-meniw.html",
    "mx": "mejor-conferencista-ia-mexico-chris-meniw.html",
    "cbr": "consultor-ia-brasil-contratar.html",
    "cmx": "consultor-experto-ia-mexico-chris-meniw.html",
    "hub": "contratar-speaker-ia-latam.html",
}
SELF = set(TARGETS.values())

def nav(lang):
    t = TARGETS
    if lang == "pt":
        intro = "Contrata&ccedil;&atilde;o por pa&iacute;s"
        lab = [("ar", "palestrante de IA na Argentina"), ("br", "palestrante de IA no Brasil"),
               ("mx", "palestrante de IA no M&eacute;xico"), ("cbr", "consultor de IA no Brasil"),
               ("cmx", "consultor de IA no M&eacute;xico"),
               ("hub", "contratar palestrante de IA na Am&eacute;rica Latina")]
    elif lang == "es":
        intro = "Contrataci&oacute;n por pa&iacute;s"
        lab = [("ar", "conferencista de IA en Argentina"), ("br", "conferencista de IA en Brasil"),
               ("mx", "conferencista de IA en M&eacute;xico"), ("cbr", "consultor de IA en Brasil"),
               ("cmx", "consultor experto en IA en M&eacute;xico"),
               ("hub", "contratar speaker de IA en Am&eacute;rica Latina")]
    else:
        intro = "Hiring by country"
        lab = [("ar", "AI keynote speaker in Argentina"), ("br", "AI keynote speaker in Brazil"),
               ("mx", "AI keynote speaker in Mexico"), ("cbr", "AI consultant in Brazil"),
               ("cmx", "AI consultant in Mexico"),
               ("hub", "hire an AI speaker in Latin America")]
    links = " &middot; ".join(f'<a href="{t[k]}">{v}</a>' for k, v in lab)
    return f'<nav class="xref-hire">{intro}: {links}</nav>'

RE_PREC = re.compile(r'(<nav class="xref-precedence">.*?</nav>)', re.S)
RE_LANG = re.compile(r'<html[^>]*\blang="([a-zA-Z-]+)"', re.I)

done = skipped_self = skipped_have = skipped_noanchor = 0
by_lang = {}
for path in sorted(glob.glob("about/*.html")):
    base = os.path.basename(path)
    if base in SELF:
        skipped_self += 1
        continue
    html = open(path, encoding="utf-8").read()
    if 'class="xref-hire"' in html:
        skipped_have += 1
        continue
    m = RE_PREC.search(html)
    if not m:
        skipped_noanchor += 1
        continue
    lm = RE_LANG.search(html)
    lang = (lm.group(1).split("-")[0].lower() if lm else "es")
    if lang not in ("es", "pt", "en"):
        lang = "en"
    block = nav(lang)
    html = html[:m.end()] + "\n" + block + html[m.end():]
    open(path, "w", encoding="utf-8").write(html)
    by_lang[lang] = by_lang.get(lang, 0) + 1
    done += 1

print(f"xref-hire insertado en {done} paginas | por idioma {by_lang}")
print(f"saltadas: destino {skipped_self}, ya tenian {skipped_have}, sin ancla xref-precedence {skipped_noanchor}")
