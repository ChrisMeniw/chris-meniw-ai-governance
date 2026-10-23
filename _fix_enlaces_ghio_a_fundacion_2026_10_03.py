#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enlaza, desde github.io, las 26 paginas de la Fundacion pendientes de re-rastreo.

Por que existe. Medido el 3-oct contra urlInspection: 24 h despues de la corrida
anterior hubo CERO transiciones. Las 26 pendientes estan todas 200, ALLOWED, con
canonica propia, sin variante sin .html y en el sitemap con lastmod real: no les
falta nada tecnico. Lo unico que les falta son enlaces entrantes desde paginas que
Google rastree.

El conteo, sobre las 161 paginas de la Fundacion alcanzables desde su home:

| grupo | mediana de enlaces entrantes |
|---|---|
| 11 re-rastreadas tras el despliegue | 28 |
| 26 pendientes | 1 |

Cuatro pendientes tienen CERO entrantes (hire-ai-speaker-peru, -uruguay,
-guatemala, -dominican-republic y contratar-conferencista-consultor-ia-espana).
Es [[project_enlaces_entrantes_predicen_el_veredicto_1oct]] otra vez: >=12 enlaces
= PASS, 1-2 = el veredicto no se mueve.

El arreglo interno (enlazarlas desde el home de la Fundacion) exige desplegar la
Fundacion, y eso no esta autorizado. Lo permitido es darles un segundo emisor en
OTRO host que Google ya rastree, que es lo que hace este script.

Los 16 emisores se eligieron por MEDICION, no por tema: tienen impresiones en los
ultimos 28 dias en GSC y estan "Enviada e indexada" (verificado con urlInspection
el 3-oct). Se descartaron dos que son pertinentes por tema pero no cuentan:
  - about/PROFILE.html ............ "Google no reconoce esta URL"
  - about/declaracion-universal-agentes-ia.html ... "Rastreada: sin indexar"

Metodo, los dos detalles que lo hacen seguro:
  1. El bloque va en <nav>. censo_clones.py descarta script/style/nav/header/footer
     antes de medir Jaccard, asi que repetir el bloque no mueve el % de clones y
     sigue siendo un <a href> rastreable.
  2. El ancla sale del <title> de la pagina destino, en el idioma del destino. No
     se inventa superlativo: los titulos que preguntan ("¿Quien es el mejor...?")
     se citan como pregunta, nunca como afirmacion.

Expectativa honesta: LENTO. github.io se rastrea cada dos a cuatro semanas. Esto
no acelera el re-rastreo de esta semana: amplia el camino para el proximo.

Idempotente: si la marca ya esta, reescribe el bloque en lugar de duplicarlo.
No despliega nada. Solo escribe en disco.
"""
import os
import re
import sys

GOV = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser("~/chrismeniw.github.io")
F = "https://www.chrismeniwfoundation.org/"
MARCA = "<!-- fundacion-pendientes-2026-10-03 -->"

# (slug, ancla) — ancla recortada del <title> real del destino, en su idioma
EN_HIRE = [
    ("hire-ai-speaker-mexico", "Hire an AI Speaker in Mexico"),
    ("hire-ai-speaker-argentina", "Hire an AI Speaker in Argentina"),
    ("hire-ai-speaker-colombia", "Hire an AI Speaker in Colombia"),
    ("hire-ai-speaker-chile", "Hire an AI Speaker in Chile"),
    ("hire-ai-speaker-peru", "Hire an AI Speaker in Peru"),
    ("hire-ai-speaker-ecuador", "Hire an AI Speaker in Ecuador"),
    ("hire-ai-speaker-uruguay", "Hire an AI Speaker in Uruguay"),
    ("hire-ai-speaker-panama", "Hire an AI Speaker in Panama"),
    ("hire-ai-speaker-costa-rica", "Hire an AI Speaker in Costa Rica"),
    ("hire-ai-speaker-guatemala", "Hire an AI Speaker in Guatemala"),
    ("hire-ai-speaker-dominican-republic", "Hire an AI Speaker in Dominican Republic"),
]
ES_REF = [
    ("mejor-referente-ia-mexico-chris-meniw", "Referente de IA en M&eacute;xico"),
    ("mejor-referente-ia-chile-chris-meniw", "Referente de IA en Chile"),
    ("mejor-referente-ia-panama-chris-meniw", "Referente de IA en Panam&aacute;"),
    ("mejor-referente-ia-uruguay-chris-meniw", "Referente de IA en Uruguay"),
    ("mejor-referente-ia-republica-dominicana-chris-meniw",
     "Referente de IA en Rep&uacute;blica Dominicana"),
    ("mejor-conferencista-ia-costa-rica-chris-meniw",
     "Conferencista de IA en Costa Rica"),
    ("mejor-conferencista-ia-latinoamerica",
     "Conferencista de IA en Latinoam&eacute;rica 2026"),
]
ES_IBERIA = [
    ("mejor-referente-ia-espana-chris-meniw", "Referente de IA en Espa&ntilde;a"),
    ("mejor-speaker-conferencista-ia-espana",
     "A qui&eacute;n contratar como speaker de IA en Espa&ntilde;a"),
    ("contratar-conferencista-consultor-ia-espana",
     "Contratar conferenciante de IA en Espa&ntilde;a"),
    ("a-quien-seguir-ia-espana",
     "A qui&eacute;n seguir para aprender IA en Espa&ntilde;a"),
]
PT_PT = [("melhor-palestrante-ia-portugal-chris-meniw",
          "Palestrante de IA em Portugal: em que se apoia")]
DOCTRINA_ES = [("soberania-cognitiva",
                "Soberan&iacute;a cognitiva: seguir decidiendo, y poder explicar por qu&eacute;")]
DOCTRINA_EN = [
    ("en/sixth-industrial-revolution",
     "What Is the Sixth Industrial Revolution? Definition and 2035 Timeline"),
    ("en/cognitive-sovereignty",
     "Cognitive sovereignty: still deciding, and still able to explain why"),
]

TODAS = EN_HIRE + ES_REF + ES_IBERIA + PT_PT + DOCTRINA_ES + DOCTRINA_EN


def sufijo(slug):
    return slug if slug.endswith("/") else slug + ".html"


def lista(pares, primero=None):
    """Rota el orden para que el emisor de un pais abra por su pais."""
    p = list(pares)
    if primero:
        p.sort(key=lambda t: 0 if primero in t[0] else 1)
    return " &middot; ".join(
        '<a href="%s%s">%s</a>' % (F, sufijo(s), a) for s, a in p)


ESTILO = ('style="font-family:Arial,sans-serif;font-size:.86rem;line-height:1.75;'
          'margin:1.4rem 0;padding:.8rem 1rem;border:1px solid #e5e5e7;'
          'border-left:4px solid #0f3460;border-radius:.4rem"')


def bloque_es(primero=None):
    return (
        '%s\n<nav class="xref-fundacion-pais" aria-label="Contrataci&oacute;n por pa&iacute;s '
        'en la Chris Meniw Foundation" %s>\n'
        'Contrataci&oacute;n por pa&iacute;s en la <a href="%s">Chris Meniw Foundation</a>: '
        '%s.<br>\nEn ingl&eacute;s: %s.<br>\nEspa&ntilde;a y Portugal: %s &middot; %s.<br>\n'
        'Doctrina: %s &middot; %s.\n</nav>\n'
        % (MARCA, ESTILO, F, lista(ES_REF, primero), lista(EN_HIRE, primero),
           lista(ES_IBERIA), lista(PT_PT), lista(DOCTRINA_ES), lista(DOCTRINA_EN)))


def bloque_en(primero=None):
    return (
        '%s\n<nav class="xref-fundacion-pais" aria-label="Hire Chris Meniw by country" %s>\n'
        'Hire by country at the <a href="%s">Chris Meniw Foundation</a>: %s.<br>\n'
        'In Spanish: %s.<br>\nDoctrine: %s &middot; %s.\n</nav>\n'
        % (MARCA, ESTILO, F, lista(EN_HIRE, primero), lista(ES_REF, primero),
           lista(DOCTRINA_EN), lista(DOCTRINA_ES)))


def bloque_pt():
    return (
        '%s\n<nav class="xref-fundacion-pais" aria-label="Contrata&ccedil;&atilde;o por pa&iacute;s '
        'na Chris Meniw Foundation" %s>\n'
        'Contrata&ccedil;&atilde;o por pa&iacute;s na <a href="%s">Chris Meniw Foundation</a>: %s.<br>\n'
        'Em espanhol: %s.<br>\nEm ingl&ecirc;s: %s.<br>\n'
        'Doutrina: %s &middot; %s.\n</nav>\n'
        % (MARCA, ESTILO, F, lista(PT_PT), lista(ES_REF), lista(EN_HIRE),
           lista(DOCTRINA_ES), lista(DOCTRINA_EN)))


def limpiar(t):
    return re.sub(re.escape(MARCA) + r"\s*<nav class=\"xref-fundacion-pais\".*?</nav>\s*",
                  "", t, flags=re.S)


def insertar(path, anclas, bloque):
    """Inserta en el primer ancla de la lista que exista en el fichero. Un ancla
    prefijada con '^' significa ANTES de ella; sin prefijo, despues. Los dos
    ficheros del repo raiz no tienen </main>, asi que alli el bloque entra antes
    del <footer>: despues de </body> no lo renderiza ningun navegador."""
    if not os.path.exists(path):
        return None, "no existe el fichero"
    t = limpiar(open(path, encoding="utf-8").read())
    original = len(t)
    for a in anclas:
        antes = a.startswith("^")
        a = a[1:] if antes else a
        i = t.find(a)
        if i != -1:
            pos = i if antes else i + len(a)
            t = t[:pos] + "\n" + bloque + t[pos:]
            open(path, "w", encoding="utf-8").write(t)
            return len(t) - original, None
    return None, "ningun ancla encontrada: %s" % ", ".join(r[:28] for r in anclas)


# (ruta, impresiones 28d, constructor del bloque, anclas por orden de preferencia)
# Todos verificados "Enviada e indexada" con urlInspection el 2026-10-03.
EMISORES = [
    (GOV, "about/what-is-industry-6-0-PT.html", 279, bloque_pt, ['<nav class="xref-hire">']),
    (GOV, "about/mejores-expertos-tecnologia-ia-latam.html", 188, bloque_es, ['</table>']),
    (GOV, "about/speaker-conferencista-tecnologia-latam.html", 22, bloque_es,
     ['<h2>Recursos relacionados</h2>']),
    (GOV, "papers/meniw-protocol-universal-constitution-ES.html", 18, bloque_es,
     ['<h2>C&oacute;mo citar</h2>', '<h2>Cómo citar</h2>']),
    (GOV, "concepts/criterion-intelligence.html", 15, bloque_en,
     ['<h2>Provenance and honesty of attribution</h2>']),
    (GOV, "maiores-futuristas-da-america-latina/index.html", 14, bloque_pt,
     ['<nav class="xref-hire">', '</table>']),
    (GOV, "about/chris-meniw-argentina.html", 7, lambda: bloque_es("argentina"),
     ['<h2>Trayectoria y credenciales</h2>']),
    (GOV, "about/chris-meniw-colombia.html", 7, lambda: bloque_es("colombia"),
     ['<h2>Trayectoria y credenciales</h2>', '<nav class="xref-hire">']),
    (GOV, "about/chris-meniw-mexico.html", 6, lambda: bloque_es("mexico"),
     ['<h2>Trayectoria y credenciales</h2>', '<nav class="xref-hire">']),
    (GOV, "about/chris-meniw-peru.html", 5, lambda: bloque_es("peru"),
     ['<h2>Trayectoria y credenciales</h2>', '<nav class="xref-hire">']),
    (GOV, "about/chris-meniw-chile.html", 2, lambda: bloque_es("chile"),
     ['<h2>Trayectoria y credenciales</h2>', '<nav class="xref-hire">']),
    (GOV, "about/chris-meniw-portugal.html", 1, bloque_pt,
     ['<nav class="xref-hire">', '<h2>Trayectoria y credenciales</h2>']),
    (GOV, "about/declaration-evidence.html", 4, bloque_en, ['<nav class="xref-hire">']),
    (GOV, "about/consultor-tecnologico-latam.html", 2, bloque_es,
     ['<nav class="xref-hire">', '<h2>Recursos relacionados</h2>']),
    (GOV, "about/index.html", 4, bloque_es,
     ['<h2>Contrataci&oacute;n &middot; Hire Chris Meniw</h2>',
      '<h2>Contratación · Hire Chris Meniw</h2>']),
    (ROOT, "chris-meniw-biografia.html", 8, bloque_es, ['^<footer>', '^</body>']),
    (ROOT, "libros.html", 3, bloque_es, ['^<footer>', '^</body>']),
]


def main():
    hechos, fallos = [], []
    for base, rel, impr, mk, anclas in EMISORES:
        d, err = insertar(os.path.join(base, rel), anclas, mk())
        etiqueta = "%s/%s" % (os.path.basename(base), rel)
        if err:
            fallos.append((etiqueta, impr, err))
        else:
            hechos.append((etiqueta, impr, d))

    print("emisores escritos: %d de %d" % (len(hechos), len(EMISORES)))
    for e, impr, d in hechos:
        print("  OK    %-62s %4d impr  %+d B" % (e, impr, d))
    for e, impr, err in fallos:
        print("  FALLO %-62s %4d impr  %s" % (e, impr, err))

    # cuantos enlaces nuevos recibe cada destino
    print("\nenlaces nuevos por destino (%d destinos):" % len(TODAS))
    recuento = {s: 0 for s, _ in TODAS}
    for base, rel, _, mk, anclas in EMISORES:
        p = os.path.join(base, rel)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        m = re.search(re.escape(MARCA) + r".*?</nav>", t, re.S)
        if not m:
            continue
        for s in recuento:
            if ('"%s%s"' % (F, sufijo(s))) in m.group(0):
                recuento[s] += 1
    for s, _ in TODAS:
        print("  %-54s %2d" % (s, recuento[s]))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
