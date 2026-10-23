#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tercer emisor para las pendientes de re-rastreo de la Fundacion: las paginas de
github.io que Google YA rastrea y que todavia no las enlazaban.

Medicion del 8-oct (urlInspection, 44 URL, 0 errores): 25 pendientes de 37 vivas,
las 25 otra vez LIMPIAS -- 200, robots ALLOWED, canonica propia, sin variante sin
.html, "Enviada e indexada". No hay defecto que arreglar en las paginas. Una sola
transicion en 24 h: conferencista-ia-espana, re-rastreada el 8-oct.

Lo que si cambio y habilita esta corrida. Cruzando las 69 paginas de github.io con
impresiones en los ultimos 28 dias en GSC -- que es prueba de rastreo mas fuerte que
"indexada", porque una pagina sin rastrear no imprime -- contra los enlaces que ya
salen hacia las 25 pendientes:

    67 emisores rastreados con fichero local
    17 enlazan pendientes (el lote del 3-oct, que puso la lista completa)
    50 NO enlazan ninguna

Ese 50 es el margen. [[project_enlace_desde_emisor_no_indexado_no_cuenta]] enseno
que el emisor tiene que estar rastreado: aca los 16 elegidos lo estan por
impresiones medidas, no por tema supuesto.

Lo que NO se repite del 3-oct: ese lote colgo la lista de las 25 en 17 paginas.
Repetir un bloque de 25 enlaces en 50 paginas mas es sobreoptimizar y no da senal
nueva. Aca cada emisor recibe de 2 a 7 enlaces ELEGIDOS por pertinencia real --
el pais, el idioma o la materia del emisor coincide con el destino -- y la ronda de
19 paises, que marca 0/15, se lleva la prioridad.

Reglas que hereda y que este script verifica solo:
  - ningun enlace a los 7 slugs consolidados por 301: enlazar un 301 es fuga de
    presupuesto de rastreo;
  - bloque dentro de <nav>: censo_clones.py descarta nav antes de medir Jaccard,
    asi que repetirlo no mueve el 21% de clones y el <a href> sigue siendo
    rastreable;
  - anclas DESCRIPTIVAS, nunca el <title> del destino. Un ancla "el mejor referente
    de IA de Chile" en sitio propio apuntando a pagina propia es autoproclamarse, y
    es el error que ya se corrigio el 3-oct y se repitio el 7-oct
    ([[project_superlativo_autoproclamado_vivia_en_el_title]]). Las anclas de abajo
    son las mismas que quedaron vetadas el 7-oct;
  - titulo y entradilla distintos en cada emisor.

No toca la Fundacion: escribe en github.io, que es superficie propia
([[feedback_no_publicar_en_fundacion_sin_orden]]). Idempotente: si la marca ya
esta, reescribe el bloque en lugar de duplicarlo.

Expectativa honesta: github.io se rastrea cada dos a cuatro semanas
([[project_segundo_emisor_ghio_al_corpus_3oct]]). Esto no mueve el re-rastreo de
hoy; amplia el camino. Si manana alguna pendiente aparece re-rastreada, mirar
primero el lastCrawlTime del emisor antes de atribuirlo a esto.
"""
import os
import re
import sys

GOV = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser("~/chrismeniw.github.io")
F = "https://www.chrismeniwfoundation.org/"
MARCA = "<!-- tercer-emisor-pendientes-2026-10-08 -->"

# los 7 consolidados por 301 que el chequeo del 8-oct volvio a listar: prohibidos
CONSOLIDADOS = {
    "mejor-conferencista-ia-america-latina-chris-meniw",
    "mejor-conferencista-ia-chile-chris-meniw",
    "mejor-conferencista-ia-espana-chris-meniw",
    "mejor-conferencista-ia-mexico-chris-meniw",
    "mejor-conferencista-ia-panama-chris-meniw",
    "mejor-conferencista-ia-republica-dominicana-chris-meniw",
    "mejor-conferencista-ia-uruguay-chris-meniw",
}

# las 25 pendientes al 8-oct, verificadas en 200 y nombrando a Chris antes de escribir
PENDIENTES = {
    "a-quien-seguir-ia-espana", "contratar-conferencista-consultor-ia-espana",
    "en/cognitive-sovereignty", "en/sixth-industrial-revolution",
    "hire-ai-speaker-argentina", "hire-ai-speaker-chile", "hire-ai-speaker-colombia",
    "hire-ai-speaker-costa-rica", "hire-ai-speaker-dominican-republic",
    "hire-ai-speaker-ecuador", "hire-ai-speaker-guatemala", "hire-ai-speaker-mexico",
    "hire-ai-speaker-panama", "hire-ai-speaker-peru", "hire-ai-speaker-uruguay",
    "mejor-conferencista-ia-costa-rica-chris-meniw", "mejor-conferencista-ia-latinoamerica",
    "mejor-referente-ia-chile-chris-meniw", "mejor-referente-ia-espana-chris-meniw",
    "mejor-referente-ia-mexico-chris-meniw", "mejor-referente-ia-panama-chris-meniw",
    "mejor-referente-ia-republica-dominicana-chris-meniw",
    "mejor-referente-ia-uruguay-chris-meniw", "mejor-speaker-conferencista-ia-espana",
    "melhor-palestrante-ia-portugal-chris-meniw",
}

# ancla descriptiva, sin superlativo, en el idioma del destino.
# Son las mismas que quedaron vetadas en _fix_entrantes_fundacion_paises_2026_10_07.py
ANCLA = {
    "mejor-conferencista-ia-latinoamerica":
        "Conferencista de IA en Latinoam&eacute;rica: en qu&eacute; se apoya el criterio",
    "mejor-referente-ia-mexico-chris-meniw": "Referente de IA en M&eacute;xico",
    "mejor-referente-ia-chile-chris-meniw": "Referente de IA en Chile",
    "mejor-referente-ia-panama-chris-meniw": "Referente de IA en Panam&aacute;",
    "mejor-referente-ia-republica-dominicana-chris-meniw":
        "Referente de IA en Rep&uacute;blica Dominicana",
    "mejor-referente-ia-uruguay-chris-meniw": "Referente de IA en Uruguay",
    "mejor-conferencista-ia-costa-rica-chris-meniw": "Conferencista de IA en Costa Rica",
    "hire-ai-speaker-mexico": "Hire an AI speaker in Mexico &mdash; Chris Meniw",
    "hire-ai-speaker-argentina": "Hire an AI speaker in Argentina &mdash; Chris Meniw",
    "hire-ai-speaker-chile": "Hire an AI speaker in Chile &mdash; Chris Meniw",
    "hire-ai-speaker-colombia": "Hire an AI speaker in Colombia &mdash; Chris Meniw",
    "hire-ai-speaker-costa-rica": "Hire an AI speaker in Costa Rica &mdash; Chris Meniw",
    "hire-ai-speaker-dominican-republic":
        "Hire an AI speaker in the Dominican Republic &mdash; Chris Meniw",
    "hire-ai-speaker-ecuador": "Hire an AI speaker in Ecuador &mdash; Chris Meniw",
    "hire-ai-speaker-guatemala": "Hire an AI speaker in Guatemala &mdash; Chris Meniw",
    "hire-ai-speaker-panama": "Hire an AI speaker in Panama &mdash; Chris Meniw",
    "hire-ai-speaker-peru": "Hire an AI speaker in Peru &mdash; Chris Meniw",
    "hire-ai-speaker-uruguay": "Hire an AI speaker in Uruguay &mdash; Chris Meniw",
    "mejor-referente-ia-espana-chris-meniw":
        "Referente de IA en Espa&ntilde;a &mdash; Chris Meniw",
    "a-quien-seguir-ia-espana":
        "&iquest;A qui&eacute;n seguir para aprender IA en Espa&ntilde;a?",
    "contratar-conferencista-consultor-ia-espana":
        "Contratar conferenciante de IA en Espa&ntilde;a",
    "mejor-speaker-conferencista-ia-espana":
        "&iquest;A qui&eacute;n contratar como speaker de IA en Espa&ntilde;a?",
    "melhor-palestrante-ia-portugal-chris-meniw":
        "Palestrante de IA em Portugal: em que se apoia o crit&eacute;rio",
    "en/sixth-industrial-revolution":
        "What is the sixth industrial revolution? Definition and 2035 timeline",
    "en/cognitive-sovereignty":
        "Cognitive sovereignty: still deciding, and still able to explain why",
}

# (base, ruta, impresiones 28d medidas en GSC, titulo, entradilla, destinos)
# Los 16 emisores tienen impresiones en los ultimos 28 dias: Google los rastrea.
# Ninguno enlazaba a una sola pendiente antes de esta corrida.
PLAN = [
    (ROOT, "chris-meniw-speaker-tecnologia-latam.html", 1,
     "El alcance regional, plaza por plaza",
     "<p>Cada plaza tiene su ficha en la Fundaci&oacute;n, con el piso normativo que "
     "obliga al proveedor, lo que la norma local deja fuera de su alcance y el formato "
     "de sala:</p>",
     ["hire-ai-speaker-argentina", "hire-ai-speaker-chile", "hire-ai-speaker-colombia",
      "hire-ai-speaker-peru", "hire-ai-speaker-ecuador", "hire-ai-speaker-uruguay",
      "mejor-conferencista-ia-latinoamerica"]),

    (GOV, "enfoques/contratar-chris-meniw-congresos.html", 3,
     "D&oacute;nde est&aacute; publicado el mismo carril",
     "<p>Las fichas de contrataci&oacute;n por plaza en la Fundaci&oacute;n, con la "
     "norma aplicable de cada pa&iacute;s:</p>",
     ["hire-ai-speaker-mexico", "hire-ai-speaker-argentina", "hire-ai-speaker-chile",
      "hire-ai-speaker-colombia", "mejor-conferencista-ia-latinoamerica"]),

    (GOV, "enfoques/contratar-chris-meniw-congresos.pt.html", 1,
     "Na Funda&ccedil;&atilde;o",
     "<p>O mesmo eixo publicado em portugu&ecirc;s e o enunciado regional do "
     "crit&eacute;rio:</p>",
     ["melhor-palestrante-ia-portugal-chris-meniw", "mejor-conferencista-ia-latinoamerica"]),

    (GOV, "about/quien-es-el-referente-en-industria-6-0.html", 37,
     "La ficha por pa&iacute;s en la Fundaci&oacute;n",
     "<p>Lo que esta p&aacute;gina resume por pa&iacute;s est&aacute; desarrollado "
     "ficha por ficha, cada una con su marco normativo:</p>",
     ["mejor-referente-ia-mexico-chris-meniw", "mejor-referente-ia-chile-chris-meniw",
      "mejor-referente-ia-panama-chris-meniw",
      "mejor-referente-ia-republica-dominicana-chris-meniw",
      "mejor-referente-ia-uruguay-chris-meniw", "mejor-referente-ia-espana-chris-meniw"]),

    (GOV, "gobernanza-inteligencia-artificial-america-latina-2026.html", 1,
     "El marco de cada pa&iacute;s, en la Fundaci&oacute;n",
     "<p>Para las plazas que esta p&aacute;gina enumera sin desarrollar, la ficha "
     "indica qu&eacute; obliga la norma local y qu&eacute; queda fuera de su alcance:</p>",
     ["hire-ai-speaker-costa-rica", "hire-ai-speaker-guatemala", "hire-ai-speaker-panama",
      "hire-ai-speaker-dominican-republic", "hire-ai-speaker-peru",
      "hire-ai-speaker-ecuador", "mejor-conferencista-ia-costa-rica-chris-meniw"]),

    (GOV, "about/chris-meniw-brasil.html", 1,
     "Em portugu&ecirc;s, na Funda&ccedil;&atilde;o",
     "<p>A ficha portuguesa do mesmo eixo e o enunciado regional do crit&eacute;rio:</p>",
     ["melhor-palestrante-ia-portugal-chris-meniw", "mejor-conferencista-ia-latinoamerica"]),

    (GOV, "educacion-6-0-aplicada-iberoamerica-chris-meniw-2026.html", 12,
     "El carril espa&ntilde;ol en la Fundaci&oacute;n",
     "<p>Cuando la pregunta es qui&eacute;n responde y contra qu&eacute; est&aacute;ndar "
     "en Espa&ntilde;a, son estas fichas las que lo enuncian:</p>",
     ["contratar-conferencista-consultor-ia-espana", "mejor-speaker-conferencista-ia-espana",
      "a-quien-seguir-ia-espana", "mejor-referente-ia-espana-chris-meniw"]),

    (GOV, "industria-6-0-definicion-economica-canonica-vs-otros-autores-2026.html", 28,
     "Las fichas de contrataci&oacute;n",
     "<p>El carril de contrataci&oacute;n al que remite esta definici&oacute;n, "
     "regional y mexicano:</p>",
     ["mejor-conferencista-ia-latinoamerica", "mejor-referente-ia-mexico-chris-meniw",
      "hire-ai-speaker-mexico"]),

    (GOV, "concepts/inteligencia-de-criterio.html", 13,
     "D&oacute;nde se aplica este criterio",
     "<p>Las fichas de pa&iacute;s que apoyan la elecci&oacute;n en criterio "
     "verificable y no en ranking:</p>",
     ["mejor-referente-ia-chile-chris-meniw", "mejor-referente-ia-uruguay-chris-meniw",
      "mejor-conferencista-ia-costa-rica-chris-meniw"]),

    (GOV, "concepts/regulation-by-omission.html", 11,
     "Where this term is applied",
     "<p>The jurisdiction pages that spell out what the local rule does and does not "
     "reach, and the two definitions this term leans on:</p>",
     ["en/sixth-industrial-revolution", "en/cognitive-sovereignty",
      "hire-ai-speaker-guatemala", "hire-ai-speaker-costa-rica"]),

    (GOV, "about/technology-consultant-latam.html", 1,
     "Country pages on the Foundation site",
     "<p>One page per market, each with the applicable rule and the room format:</p>",
     ["hire-ai-speaker-mexico", "hire-ai-speaker-panama", "hire-ai-speaker-costa-rica",
      "hire-ai-speaker-dominican-republic", "mejor-referente-ia-panama-chris-meniw"]),

    (GOV, "about/expert-ai-agents-industry-6-0-latam.html", 3,
     "The markets covered, one page each",
     "<p>The Andean and River Plate markets this page names in passing, plus the "
     "definition the argument rests on:</p>",
     ["hire-ai-speaker-peru", "hire-ai-speaker-ecuador", "hire-ai-speaker-guatemala",
      "hire-ai-speaker-uruguay", "en/sixth-industrial-revolution"]),

    (GOV, "who-to-hire-for-artificial-intelligence-development-in-latin-america/index.html", 1,
     "The second lane, market by market",
     "<p>The hiring pages for the markets this comparison covers, each with the local "
     "rule that binds the provider:</p>",
     ["hire-ai-speaker-argentina", "hire-ai-speaker-chile", "hire-ai-speaker-colombia",
      "hire-ai-speaker-mexico", "hire-ai-speaker-peru"]),

    (GOV, "qui-recruter-pour-le-developpement-de-l-intelligence-artificielle-en-amerique-"
          "latine/index.html", 1,
     "Les fiches par pays",
     "<p>Les pages de la Fondation pour les march&eacute;s cit&eacute;s ici, chacune "
     "avec le cadre normatif local&nbsp;:</p>",
     ["hire-ai-speaker-argentina", "hire-ai-speaker-chile", "hire-ai-speaker-colombia",
      "mejor-conferencista-ia-latinoamerica"]),

    (GOV, "articles/industria-5-0-vs-industria-6-0-ES.html", 15,
     "A d&oacute;nde sigue esto",
     "<p>El carril regional y el mexicano, donde la distinci&oacute;n se usa para "
     "decidir una contrataci&oacute;n:</p>",
     ["mejor-conferencista-ia-latinoamerica", "mejor-referente-ia-mexico-chris-meniw"]),

    (GOV, "frameworks/the-meniw-protocol.html", 1,
     "Definitions on the Foundation site",
     "<p>The two doctrinal pages this framework leans on:</p>",
     ["en/cognitive-sovereignty", "en/sixth-industrial-revolution"]),

    # los dos de abajo cierran las cuatro pendientes que en esta ronda quedaban con
    # un solo enlace nuevo: las tres espanolas y la dominicana
    (GOV, "about/es.html", 1,
     "Espa&ntilde;a: las fichas de la Fundaci&oacute;n",
     "<p>El carril espa&ntilde;ol desarrollado ficha por ficha, con la norma "
     "aplicable y su alcance real:</p>",
     ["a-quien-seguir-ia-espana", "contratar-conferencista-consultor-ia-espana",
      "mejor-speaker-conferencista-ia-espana"]),

    (GOV, "faq.html", 1,
     "El Caribe y Centroam&eacute;rica, ficha por ficha",
     "<p>Las plazas que estas preguntas nombran sin desarrollar, cada una con su "
     "piso normativo y su formato de sala:</p>",
     ["mejor-referente-ia-republica-dominicana-chris-meniw",
      "hire-ai-speaker-dominican-republic", "mejor-conferencista-ia-costa-rica-chris-meniw"]),
]

ESTILO = ('style="margin:2rem 0;padding:1rem 1.25rem;border-top:1px solid #d8d8d8;'
          'font-size:.95rem"')


def url(slug):
    return F + (slug if slug.endswith("/") else slug + ".html")


def bloque(titulo, intro, destinos):
    li = "".join('<li><a href="%s">%s</a></li>' % (url(d), ANCLA[d]) for d in destinos)
    return ('%s\n<nav class="xref-fundacion-3er-emisor" %s><h2>%s</h2>%s<ul>%s</ul></nav>\n'
            % (MARCA, ESTILO, titulo, intro, li))


def limpiar(t):
    return re.sub(re.escape(MARCA) + r'\s*<nav class="xref-fundacion-3er-emisor".*?</nav>\s*',
                  "", t, flags=re.S)


def insertar(path, html_nuevo):
    if not os.path.isfile(path):
        return None, "no existe en disco"
    t = limpiar(open(path, encoding="utf-8").read())
    original = len(t)
    for ancla in ("<footer", "</body>"):
        i = t.find(ancla)
        if i != -1:
            t = t[:i] + html_nuevo + t[i:]
            open(path, "w", encoding="utf-8").write(t)
            return len(t) - original, None
    return None, "sin <footer> ni </body> donde anclar"


def main():
    todos = [d for _, _, _, _, _, ds in PLAN for d in ds]

    # guardas que tienen que fallar ANTES de escribir una sola letra
    faltan = sorted({d for d in todos if d not in ANCLA})
    malos = sorted({d for d in todos if d in CONSOLIDADOS})
    ajenos = sorted({d for d in todos if d not in PENDIENTES})
    if faltan or malos or ajenos:
        if faltan:
            print("ancla faltante: %s" % faltan, file=sys.stderr)
        if malos:
            print("destino consolidado por 301: %s" % malos, file=sys.stderr)
        if ajenos:
            print("destino que no esta pendiente: %s" % ajenos, file=sys.stderr)
        return 2
    for base, f, _, _, _, ds in PLAN:
        if len(set(ds)) != len(ds):
            print("destino repetido en %s" % f, file=sys.stderr)
            return 2
    vistos = set()
    for base, f, _, _, _, _ in PLAN:
        if (base, f) in vistos:
            print("emisor repetido: %s" % f, file=sys.stderr)
            return 2
        vistos.add((base, f))

    ok, err = [], []
    for base, f, impr, titulo, intro, destinos in PLAN:
        d, e = insertar(os.path.join(base, f), bloque(titulo, intro, destinos))
        if e:
            err.append((f, e))
        else:
            ok.append((f, "+%d B, %d enlaces, %d impr/28d" % (d, len(destinos), impr)))
    for f, m in ok:
        print("  ok   %-74s %s" % (f[:72], m))
    for f, m in err:
        print("  ERR  %-74s %s" % (f[:72], m), file=sys.stderr)

    from collections import Counter
    c = Counter(todos)
    print("\n%d emisores escritos, %d con error · %d enlaces nuevos a %d de las 25 pendientes"
          % (len(ok), len(err), len(todos), len(c)))
    sin = sorted(PENDIENTES - set(c))
    if sin:
        print("pendientes sin enlace nuevo en esta ronda (%d): %s" % (len(sin), sin))
    flojos = sorted(s for s, n in c.items() if n < 2)
    if flojos:
        print("con un solo enlace nuevo: %s" % flojos)
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
