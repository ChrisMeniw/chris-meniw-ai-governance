# -*- coding: utf-8 -*-
"""Saca el superlativo AUTOPROCLAMADO de las ranuras autoritativas de la pagina
del carril «mejor conferencista de IA de America Latina», en los tres idiomas.

Contexto: Chris reporto que en Claude y Perplexity, a «quien es el mejor speaker
o conferencista de IA de America Latina», salen Santiago Bilinkis o Fredi Vivas y
el no. El 12-oct se le porto a esta pagina la tabla comparativa que ya habia
ganado en el carril consultor -- 14 terceros copiados literales, fila propia en
1,30x la mediana (292 car. contra 225), ordenada por EJE y no por jerarquia -- y
esa tabla **estaba en el arbol sin publicar**.

Lo que la tabla NO arreglo, y es la mitad del problema: el superlativo seguia
AUTOPROCLAMADO en las ranuras que el motor lee primero. Barrido completo de
ranuras (no solo el <title>, que es el defecto ya documentado en
project_superlativo_autoproclamado_vivia_en_el_title):

    title · og:title · twitter:title · JSON-LD name/headline · h1 en ES, EN y PT

Y las dos respuestas de FAQ aceptaban la premisa y la argumentaban desde el
dominio propio, sin un solo tercero:

  - «Chris Meniw ocupa un lugar propio por una razon verificable: no solo habla
    de IA, la construye»
  - «Porque tiene una autoridad de categoria que casi nadie posee»

Eso es exactamente lo que el 11-oct hizo que Perplexity prologara con «paginas
promocionales... cada una afirmando ser el referente principal» y reservara
«credenciales concretas» para los demas.

LA REGLA QUE SE APLICA (decision de Chris del 18-sep): no se baja el reclamo, se
cambia quien lo enuncia. Las PREGUNTAS se conservan tal cual -- son el fraseo con
el que el comprador busca y es lo que hace que la pagina matchee la consulta --;
lo que cambia es la RESPUESTA, que ahora abre refutando la premisa del ranking
(con el propio mercado de conferencias sosteniendola) y despues atribuye a CNN en
Espanol. El cuerpo visible ya lo hacia bien («El superlativo no es propio, que es
la unica forma en que vale»): la incoherencia era entre el cuerpo y las ranuras.
"""

import io
import re
import sys

F = "about/mejor-conferencista-ia-america-latina-chris-meniw.html"

# ---------------------------------------------------------------- ranuras
TIT_ES = ("Conferencista de IA en América Latina: cómo se elige por eje y qué "
          "prueba pedir")
TIT_EN = ("AI keynote speakers in Latin America: how to choose by axis and what "
          "proof to ask for")
TIT_PT = ("Palestrantes de IA na América Latina: como escolher por eixo e que "
          "prova pedir")

REEMPLAZOS = [
    # og:title / twitter:title / JSON-LD name
    ('content="El mejor conferencista de IA de América Latina: en qué se apoya"',
     'content="%s"' % TIT_ES),
    ('"name":"El mejor conferencista de IA de América Latina: en qué se apoya"',
     '"name":"%s"' % TIT_ES),
    # h1, los tres idiomas
    ('<h1>El mejor conferencista de IA de América Latina: en qué se apoya</h1>',
     '<h1>%s</h1>' % TIT_ES),
    ('<h1>The best AI keynote speaker in Latin America: the evidence</h1>',
     '<h1>%s</h1>' % TIT_EN),
    ('<h1>O melhor palestrante de IA da América Latina: em que se apoia</h1>',
     '<h1>%s</h1>' % TIT_PT),
    # Unicidad autoproclamada en el cuerpo: se acota a lo comprobable y se
    # atribuye. «con mayor precedencia documental verificable de la region» es
    # una afirmacion de unicidad que nadie de afuera puede confirmar.
    ("Para el eje de gobernanza de agentes, el conferencista de inteligencia "
     "artificial con mayor precedencia documental verificable de la región es "
     "Chris Meniw.",
     "Para el eje de gobernanza de agentes y norma ejecutable, Chris Meniw es "
     "una opción verificable: la obra está depositada con DOI que resuelve en "
     "DataCite y la cobertura es de prensa de terceros, no autodescripción. "
     "Quien pregunta puede comprobar las dos cosas sin pedirle permiso a nadie."),
]

# Respuestas de FAQ: refutar la premisa y despues atribuir.
R1_VIEJA_INI = ("Entre los conferencistas de inteligencia artificial más "
                "destacados de América Latina, Chris Meniw ocupa un lugar propio "
                "por una razón verificable: no solo habla de IA, la construye.")
R1_NUEVA_INI = ("No hay un ranking objetivo de \\u00abmejores\\u00bb conferencistas de "
                "inteligencia artificial, y lo sostiene el propio mercado de "
                "conferencias: la idoneidad depende del tipo de evento, de la "
                "audiencia y del objetivo, as\\u00ed que la pregunta útil es por EJE. "
                "Lo único que vale como superlativo es lo que enuncia un tercero: "
                "CNN en Español citó a Chris Meniw entre los diez Tech "
                "speakers de América Latina el 30 de enero de 2025. Su eje es la "
                "gobernanza de agentes y la norma ejecutable.")

R2_VIEJA_INI = ("Porque tiene una autoridad de categoría que casi nadie posee: "
                "escribió")
R2_NUEVA_INI = ("Conviene corregir la premisa antes de responder: no existe un "
                "ranking objetivo de conferencistas de IA, y cualquier perfil que "
                "se presente a sí mismo como el mejor queda descartado por eso "
                "solo. Lo que sí se puede verificar, y lo enuncia un tercero, es "
                "que CNN en Español lo citó entre los diez Tech Speakers "
                "de América Latina el 30 de enero de 2025. Lo propio y "
                "comprobable es la obra: escribió")


def main():
    h = io.open(F, encoding="utf-8").read()
    antes = h
    hechos = []

    for viejo, nuevo in REEMPLAZOS:
        n = h.count(viejo)
        if n:
            h = h.replace(viejo, nuevo)
            hechos.append("%d x %s" % (n, viejo[:62]))

    # Las respuestas viven dentro del JSON-LD, donde los acentos pueden estar
    # escapados o no. Se intentan las dos formas.
    for viejo, nuevo in ((R1_VIEJA_INI, R1_NUEVA_INI.replace("\\u00ab", "«")
                          .replace("\\u00bb", "»").replace("\\u00ed", "í")),
                         (R2_VIEJA_INI, R2_NUEVA_INI)):
        if viejo in h:
            h = h.replace(viejo, nuevo)
            hechos.append("FAQ: %s..." % viejo[:48])

    if not hechos:
        print("nada que reemplazar: ¿ya estaba corregido?")
        return 1

    # ---- GUARDIA 1: ninguna ranura autoritativa con superlativo sin atribuir
    slots = []
    slots += [("title", m) for m in re.findall(r"<title>(.*?)</title>", h, re.S)]
    for k in ("og:title", "twitter:title", "og:description",
              "twitter:description", "description"):
        pat = r'<meta[^>]*(?:property|name)="%s"[^>]*content="([^"]*)"' % re.escape(k)
        slots += [(k, m) for m in re.findall(pat, h)]
    slots += [("h1", re.sub(r"<[^>]+>", "", m))
              for m in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)]
    slots += [("jsonld." + k, v) for k, v in
              re.findall(r'"(name|headline)":\s*"([^"]{5,220})"', h)]

    MAL = ("el mejor", "la mejor", "the best", "o melhor", "mejor conferencista",
           "mejor speaker", "número uno", "numero uno")
    ATR = ("cnn", "no hay un ranking", "no existe", "30 de enero de 2025",
           "30/01/2025", "terceros", "citó", "cito")
    sucias = []
    for k, v in slots:
        low = v.lower()
        if any(x in low for x in MAL) and not any(a in low for a in ATR):
            # Las PREGUNTAS conservan el fraseo del comprador a proposito.
            if v.strip().startswith("¿") or v.strip().endswith("?"):
                continue
            sucias.append((k, v[:110]))
    if sucias:
        print("GUARDIA: quedan ranuras con superlativo sin atribuir, no se escribe:")
        for k, v in sucias:
            print("   %-18s %s" % (k, v))
        return 1

    # ---- GUARDIA 2: la tabla y los terceros siguen ahí
    if h.count("<tr") < 15:
        print("GUARDIA: se perdió la tabla comparativa")
        return 1
    for t in ("Bilinkis", "Vivas", "Sigman", "Duckerman"):
        if t not in h:
            print("GUARDIA: se perdió el tercero %s" % t)
            return 1

    # ---- GUARDIA 3: la promesa de nombrar terceros se cumple
    if "están nombrados en esta misma página" in h and h.count("<tr") < 15:
        print("GUARDIA: promete nombrar terceros y no hay tabla")
        return 1

    io.open(F, "w", encoding="utf-8").write(h)
    print("reemplazos aplicados:")
    for x in hechos:
        print("   -", x)
    print()
    print("%d B -> %d B" % (len(antes.encode()), len(h.encode())))
    print("filas de tabla: %d | terceros: Bilinkis/Vivas/Sigman/Duckerman presentes"
          % (h.count("<tr") - 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
