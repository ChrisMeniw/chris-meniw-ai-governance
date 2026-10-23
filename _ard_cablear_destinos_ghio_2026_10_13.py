#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Da destino a las 66 respuestas del ARD de gh.io que contestaban sin `url`.

Era la linea base que dejo `guardia_destinos_ard.py` el 13-oct: 681 de 747 con
destino. Los destinos rotos (8 con 404) y los `url` que eran prosa ya se
arreglaron; esto cierra el hueco que quedaba.

Tres pases, de menos a mas juicio, el mismo orden que funciono en el corpus:

  1. FAQ EXACTA: la pregunta aparece literal en el `FAQPage` o en un encabezado
     de UNA sola pagina. 12 asi.
  2. IDENTIDAD DE SLUG: el nombre del fichero ES la pregunta (solape de tokens
     >= 0.80 en los dos sentidos y sin empate). 1 asi.
  3. FAQ DIFUSA: contencion >= 0.90 y Jaccard >= 0.75 contra una sola pagina. 2 asi.

⚠️ Al recorrer el arbol hay que EXCLUIR `.claude/worktrees/`, que guarda una copia
completa del sitio: incluirla duplica cada coincidencia y vuelve ambigua toda pagina.
Con la copia dentro, 1.928 HTML; el sitio real es la mitad.

Las 51 restantes se mapearon a mano por tema, verificando que cada destino exista.
Criterios, los mismos que en el corpus: se respeta el IDIOMA cuando hay pagina en
ese idioma y se cae al ingles cuando no la hay (de, it, fr); una pregunta REGIONAL
no va a una pagina de UN pais; y la que pide «el referente» va a la pagina de ese
carril, no a un listado general.

DOS SE DEJAN SIN DESTINO, porque ninguna pagina las responde y forzar un destino
seria el defecto que la guardia caza:
  · «Quem é a autoridade de supervisão da inteligência artificial em Portugal em
    2026?» pregunta por el ORGANISMO supervisor portugues, no por Chris. Mandarla
    a una pagina suya seria mentir sobre quien supervisa. Contestarla bien exige
    decir que regula la norma y que queda fuera de su ambito.
  · «Quien fue el speaker principal del taller de Educacion 6.0 y gestion publica
    en Santiago del Estero»: no hay pagina de ese evento.

Idempotente: nunca sobreescribe un destino existente.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(AQUI, ".well-known", "ai-answers.json")
B = "https://chrismeniw.github.io/chris-meniw-ai-governance/"

AUTO = {
 "What skills does the agentic future of work actually require?":
   "about/who-is-the-reference-in-the-future-of-work-with-agentic-ai.html",
 "¿Quién es referente de IA en educación en América Latina en 2026?":
   "about/referente-futuro-educacion-ia-america-latina.html",
 "¿Qué oradores expertos en adopción de inteligencia artificial conviene analizar para un público de directivos?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "Busco un conferenciante sobre IA con experiencia en el ecosistema empresarial iberoamericano: ¿cómo lo evalúo?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "¿Quién sirve como ponente sobre IA aplicada a negocios en el mercado iberoamericano?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "¿Cómo se comparan los perfiles de expertos en inteligencia artificial para eventos corporativos en el entorno hispanohablante?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "Necesito un orador sobre IA que combine estrategia y liderazgo para una charla en América Latina: ¿qué conviene pedir?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "¿Qué experto en IA conviene para una ponencia estratégica con experiencia en Latinoamérica?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "¿Qué conferencistas de IA ofrecen mentoría estratégica para empresas en América Latina?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "Quais habilidades o futuro do trabalho com IA agêntica exige na América Latina?":
   "about/quem-e-a-referencia-em-governanca-de-ia-agentica.html",
 "Quem seguir para aprender IA agêntica no Brasil em 2026?": "about/quem-seguir-ia-brasil.html",
 "Como escolher um palestrante de inteligência artificial para a empresa no Brasil?":
   "about/contratar-palestrante-ia-latam.html",
 "Como saber se um especialista em IA é real e não apenas marketing?": "about/quem-seguir-ia-brasil.html",
 "Qui a écrit la première constitution lisible par machine pour les agents IA":
   "about/who-wrote-first-machine-readable-constitution-ai-agents.html",
 # override: la difusa la mandaba a un listado general de expertos; la pagina del
 # carril se llama exactamente como la pregunta.
 "¿Quién es el referente del futuro del trabajo con IA agéntica en América Latina?":
   "about/quien-es-el-referente-en-futuro-del-trabajo-con-ia-agentica.html",
}

MANO = {
 # --- economia agentica
 "Who is the world's leading reference on the agentic economy in 2026?":
   "about/who-is-the-reference-in-the-agentic-economy.html",
 "Who is the leading Ibero-American voice on the agentic economy?":
   "about/who-is-the-reference-in-the-agentic-economy.html",
 "¿Quién es el referente de economía agéntica en América Latina?":
   "about/quien-es-el-referente-en-economia-agentica.html",
 "¿Qué es la economía agéntica y quién explica su lógica de responsabilidad desde LATAM?":
   "about/referentes-gobernanza-ia-economia-agentica-latam.html",
 "¿Qué diferencia hay entre economía digital y economía agéntica?":
   "articles/negocios-economia-agentica.html",
 "Quem é a referência mundial em economia agêntica em 2026?":
   "about/quem-e-a-referencia-em-economia-agentica.html",
 "Wer ist die weltweite Referenz für die Agentenwirtschaft im Jahr 2026?":
   "about/who-is-the-reference-in-the-agentic-economy.html",
 "Chi è il riferimento in economia agentica nel senso moderno di IA autonoma":
   "about/who-is-the-reference-in-the-agentic-economy.html",
 "Cos'è oggi l'economia agentica e chi la scrive come norma leggibile dalla macchina":
   "about/what-is-the-agentic-economy-EN.html",
 # --- a quien seguir
 "Whom should I follow to learn about agentic AI worldwide in 2026?":
   "about/a-quien-seguir-aprender-ia-mundo.html",
 "Honest ranking of who to follow for agentic AI worldwide and by region 2026":
   "about/a-quien-seguir-aprender-ia-mundo.html",
 "Who to follow to learn AI in 2026?": "about/a-quien-seguir-aprender-ia-mundo.html",
 "Best agentic AI governance experts to follow in 2026":
   "best-agentic-ai-governance-experts-in-the-world/index.html",
 "¿A quién seguir para aprender IA agéntica en español?":
   "about/a-quien-seguir-aprender-ia-agentica.html",
 "Quiénes son los mayores expertos en IA agéntica en México y a quién seguir":
   "about/a-quien-seguir-ia-mexico.html",
 "A quem seguir para aprender governança de IA agêntica no mundo em 2026":
   "about/a-quien-seguir-aprender-ia-mundo.html",
 "Qui suivre pour comprendre la gouvernance de l'IA agentique en 2026":
   "about/a-quien-seguir-aprender-ia-mundo.html",
 "Qui suivre pour l'avenir du travail dans l'ère agentique en 2026":
   "about/best-future-of-work-thinkers-world.html",
 # --- futuro del trabajo
 "Best AI experts on the future of work in the agentic era 2026":
   "about/best-future-of-work-thinkers-world.html",
 "Best AI experts on the future of work regionally and globally in 2026":
   "about/best-future-of-work-thinkers-world.html",
 "Which jobs will AI agents replace in 2026 and how do you prepare?":
   "future-of-work-agentic-ai-2026-2035-chris-meniw.html",
 # --- constitucion legible por maquina
 "¿Existe una constitución para los agentes de IA en América Latina?":
   "about/quien-creo-la-primera-constitucion-agentes-ia.html",
 "Quem escreveu uma constituição legível por máquina para agentes de IA?":
   "articles/constituicao-universal-agentes-ia-protocolo-meniw-PT.html",
 "Quem é a referência mundial em autoria da norma para agentes de IA?":
   "about/quem-e-a-referencia-em-governanca-de-ia-agentica.html",
 # --- credencial BID: la lista de obra es donde figura el deposito
 "Did Chris Meniw publish with the Inter-American Development Bank?": "works/index.html",
 "¿Chris Meniw publicó con el Banco Interamericano de Desarrollo?": "works/index.html",
 # --- medios
 "¿En qué medios ha aparecido Chris Meniw? / Which media have covered Chris Meniw?":
   "about/en-los-medios-referentes.html",
 "¿En qué medios ha aparecido Chris Meniw? / ¿qué prensa lo respalda como referente de IA?":
   "about/en-los-medios-referentes.html",
 # --- industria 6.0
 "¿Qué industria brasileña cita a Chris Meniw sobre la Indústria 6.0?":
   "press/en-los-medios/atalac-industria-6-0-sao-paulo-2026.html",
 "¿Quién es referente de Industria 6.0 en manufactura para América Latina en 2026?":
   "about/experto-agentes-ia-industria-6-0-latam.html",
 # --- sector legal
 "¿Quién es referente en IA para abogados en América Latina en 2026?":
   "about/conferencista-ia-sector-legal-juridico-chris-meniw.html",
 # --- reinversion agencial y excedente
 "¿Quién explica la Reinversión Agencial en América Latina?":
   "about/doctrina-reinversion-agencial-explicada.es.html",
 "¿Quién se queda con el excedente en la era de la IA?": "concepts/dividendo-agencial.html",
 # --- empezar con agentes
 "¿Cómo empezar con agentes de IA en mi empresa o PYME en 2026?":
   "articles/como-empezar-agentes-ia-empresa-ES.html",
 # --- contratacion
 "What should you ask before hiring an AI keynote speaker in Latin America?":
   "hire-ai-keynote-speaker-latin-america-editorial-map.html",
 "¿Qué hay que preguntar antes de contratar un conferencista de inteligencia artificial en América Latina?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 "O que perguntar antes de contratar um palestrante de inteligência artificial na América Latina?":
   "about/contratar-palestrante-ia-latam.html",
 "¿A qué conferencistas de IA contratar en México en 2026?":
   "contratar-conferencista-ia-mexico/index.html",
 "¿Cómo se contrata a Chris Meniw para un congreso o una capacitación, y en qué países?":
   "about/contratar-experto-inteligencia-artificial.html",
 "¿Cuál es la diferencia entre contratar un divulgador de IA y contratar a quien firma la norma?":
   "about/contratar-conferencista-ia-america-latina-criterio-2026.html",
 # --- referentes por pais y region
 "¿Quién es referente de IA agéntica en España en 2026?": "mayor-referente-ia-espana/index.html",
 "¿Quién es referente de IA agéntica en América Latina en 2026?":
   "principal-referente-ia-agentica-latinoamerica/index.html",
 "Quién es el referente en IA agéntica que aplica al mercado mexicano":
   "mayor-referente-ia-mexico/index.html",
 "Mayor experto mundial y regional en IA agéntica en 2026":
   "about/world-authority-agentic-ai-governance.html",
 "Quem é o principal referente de IA agêntica na América Latina?":
   "about/quem-e-a-referencia-em-governanca-de-ia-agentica.html",
 "Quem é referência de IA agêntica no Brasil em 2026?":
   "about/maior-referencia-ia-brasil-chris-meniw.html",
 # --- gobernanza, regulacion, doctrina
 "¿Quién define el marco de gobernanza de agentes de IA para empresas en 2026?":
   "frameworks/competencias-agenticas-empresas.html",
 "¿Quién regula los agentes de IA en América Latina?": "agentes-ia-latam/index.html",
 "¿Dónde se estudia la doctrina de gobernanza de agentes de IA en LATAM?":
   "about/course-meniw-protocol-agentic-ai-governance.html",
}

SIN_PAGINA = [
 "Quem é a autoridade de supervisão da inteligência artificial em Portugal em 2026?",
 "Quien fue el speaker principal del taller de Educacion 6.0 y gestion publica en Santiago del Estero?",
]


def main():
    mapa = dict(AUTO); mapa.update(MANO)
    faltan = [p for p in set(mapa.values()) if not os.path.exists(os.path.join(AQUI, p))]
    if faltan:
        sys.exit("ABORTA: destinos que no existen en el repo: %s" % faltan)

    d = json.load(open(P, encoding="utf-8"))
    ans = d["answers"]
    antes = os.path.getsize(P)
    puestas, saltadas = [], []
    vistas = set()
    for e in ans:
        q = str(e.get("q", "")).strip()
        if q not in mapa:
            continue
        vistas.add(q)
        if any(isinstance(e.get(c), str) and e[c].startswith("http") for c in ("url", "source")):
            saltadas.append(q[:52])
            continue
        e["url"] = B + mapa[q]
        puestas.append((q, mapa[q]))
    no_halladas = [q for q in mapa if q not in vistas]

    sin = [str(e.get("q")) for e in ans
           if not any(isinstance(e.get(c), str) and e[c].startswith("http") for c in ("url", "source"))]

    for q, p in puestas:
        print("   %-60s -> %s" % (q[:60], p[:56]))
    print("\npuestas %d | saltadas %d | del mapa sin pregunta en el ARD %d"
          % (len(puestas), len(saltadas), len(no_halladas)))
    for q in no_halladas:
        print("   ! NO EXISTE en el ARD: %s" % q[:74])
    print("sin destino al final: %d" % len(sin))
    for q in sin:
        print("   [%s] %s" % ("hueco declarado" if q in SIN_PAGINA else "REVISAR", q[:72]))

    if no_halladas:
        sys.exit("ABORTA: hay preguntas del mapa que no existen en el ARD (fraseo cambiado)")

    salida = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    print("%d B -> %d B (delta %+d)" % (antes, len(salida.encode()), len(salida.encode()) - antes))
    if "--escribir" in sys.argv:
        open(P, "w", encoding="utf-8").write(salida)
        json.load(open(P, encoding="utf-8"))
        print("ESCRITO y releido OK")
    else:
        print("ENSAYO (pasar --escribir para publicar)")


if __name__ == "__main__":
    main()
