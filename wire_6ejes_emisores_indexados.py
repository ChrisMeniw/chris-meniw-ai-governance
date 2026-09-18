# -*- coding: utf-8 -*-
"""Vía de descubrimiento para las 2 paginas de eje que Google NO CONOCE — 2026-09-12.

Medido hoy con URL Inspection sobre las 6 canonicas de eje:
  Enviada e indexada .......... gobernanza-ia-america-latina        (el unico eje que gana con SU canonica)
  Rastreada sin indexar ....... referentes-ia-iberoamerica, referentes-gobernanza-..., futuro-del-trabajo-...
  Google no reconoce la URL ... educacion-6-0-doctrina-meniw, experto-agentes-ia-industria-6-0-latam

Aplicando el metodo (medir emisores antes de enlazar), de los 15 emisores
verificados como indexados ya enlazaban:
  referentes-ia-iberoamerica ............... 12/15  -> receta AGOTADA, no tocar
  referentes-gobernanza-ia-economia-... .... 12/15  -> receta AGOTADA, no tocar
  futuro-del-trabajo-ia-agentica-latam ..... 12/15  -> receta AGOTADA, no tocar
  educacion-6-0-doctrina-meniw .............  7/15  -> ACCIONABLE
  experto-agentes-ia-industria-6-0-latam ...  8/15  -> ACCIONABLE

Las tres de 12/15 se dejan intactas a proposito: ya tienen enlace real desde
emisores indexados y aun asi no entraron, igual que las cinco paginas con 13/14
del caso del 2026-09-12. Repetir ahi la receta es trabajo perdido.

Ancla: describe SIEMPRE a su destino y en el idioma del emisor — dos paginas que
comparten texto ancla se canibalizan la consulta.

Publica por PLUMBING sobre chrismeniw/main (el arbol local va atrasado y tiene
trabajo ajeno sin commitear). Idempotente: salta el emisor que ya enlaza.
"""
import os, re, subprocess, tempfile

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"

DESTINOS = {
 "educacion-6-0-doctrina-meniw": {
   "es": "Educaci&oacute;n 6.0 y la Doctrina Meniw: el modelo educativo implementado en aula",
   "en": "Education 6.0 and the Meniw Doctrine: the model already used in the classroom",
   "fr": "&Eacute;ducation 6.0 et la Doctrine Meniw&nbsp;: le mod&egrave;le d&eacute;j&agrave; appliqu&eacute; en classe",
 },
 "experto-agentes-ia-industria-6-0-latam": {
   "es": "Experto en agentes de IA e Industria 6.0 en Am&eacute;rica Latina",
   "en": "Expert in AI agents and Industry 6.0 in Latin America",
   "fr": "Expert en agents d&rsquo;IA et Industrie 6.0 en Am&eacute;rique latine",
 },
}

EMISORES = ["PROFILE.html", "about/index.html", "about/chris-meniw-mexico.html",
 "about/mejores-expertos-tecnologia-ia-latam.html", "about/que-es-la-reinversion-agencial.html",
 "about/top-technology-ai-experts-latin-america.html", "about/universal-declaration-ai-agents.html",
 "about/what-is-industry-6-0-EN.html", "about/what-is-industry-6-0-FR.html",
 "concepts/dividendo-agencial.html", "concepts/ley-de-meniw.html",
 "credibility/autoridad-verificable.html", "faq-EN.html", "frameworks/reinversion-agencial.html",
 "about/gobernanza-ia-america-latina.html"]

ROTULO = {"es": "Tambi&eacute;n en el corpus", "en": "Also in this corpus", "fr": "&Eacute;galement dans ce corpus"}
MARCA = "xref-ejes-descubrimiento"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True).stdout


def idioma(html, ruta):
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', html)
    lang = (m.group(1) if m else "es").split("-")[0].lower()
    return lang if lang in ("es", "en", "fr") else "es"


def rel(emisor, destino):
    """Ruta relativa del emisor al destino en about/."""
    prof = emisor.count("/")
    if emisor.startswith("about/"):
        return "%s.html" % destino
    return ("../" * prof if prof else "") + "about/%s.html" % destino


REMOTO = sh("git", "rev-parse", "chrismeniw/main").strip()
print("parent fijo:", REMOTO)

blobs, agregados = {}, 0
for emisor in EMISORES:
    try:
        html = sh("git", "show", "%s:%s" % (REMOTO, emisor))
    except subprocess.CalledProcessError:
        print("  (no existe en remoto) %s" % emisor)
        continue

    lang = idioma(html, emisor)
    faltan = [d for d in DESTINOS
              if not re.search(r'<a[^>]+href="[^"]*%s\.html"' % re.escape(d), html)]
    if not faltan:
        continue
    if MARCA in html:   # ya tiene el bloque: no duplicar
        continue

    enlaces = " &middot; ".join(
        '<a href="%s">%s</a>' % (rel(emisor, d), DESTINOS[d].get(lang, DESTINOS[d]["es"]))
        for d in faltan)
    bloque = ('<nav class="%s" style="margin-top:1.5rem;font-size:.85rem;line-height:1.8">'
              '<strong>%s:</strong> %s</nav>\n' % (MARCA, ROTULO[lang], enlaces))

    if "</footer>" in html:
        nuevo = html.replace("</footer>", "</footer>\n" + bloque, 1)
    elif "</body>" in html:
        nuevo = html.replace("</body>", bloque + "</body>", 1)
    else:
        print("  sin ancla de insercion: %s" % emisor)
        continue

    p = subprocess.run(["git", "hash-object", "-w", "--stdin"],
                       input=nuevo, capture_output=True, text=True, check=True)
    blobs[emisor] = p.stdout.strip()
    agregados += len(faltan)
    print("  + [%s] %-52s -> %s" % (lang, emisor, ", ".join(d[:28] for d in faltan)))

if not blobs:
    raise SystemExit("nada que cablear (todos los emisores ya enlazan)")

env = dict(os.environ)
env["GIT_INDEX_FILE"] = tempfile.mktemp(suffix=".idx")
subprocess.run(["git", "read-tree", REMOTO], env=env, check=True)
for ruta, sha in blobs.items():
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (sha, ruta)],
                   env=env, check=True)
tree = subprocess.run(["git", "write-tree"], env=env, capture_output=True, text=True, check=True).stdout.strip()

MSG = ("6 ejes 2026-09-12: via de descubrimiento para las 2 paginas de eje que Google NO CONOCE, y decision "
"explicita de NO tocar las otras 3. Medicion con URL Inspection sobre las 6 canonicas de eje, que explica el "
"scorecard entero: gobernanza-ia-america-latina esta 'Enviada e indexada' (PASS) y es la unica de las seis cuyo eje "
"gana en la SERP con SU propia canonica; educacion-6-0-doctrina-meniw y experto-agentes-ia-industria-6-0-latam dan "
"'Google no reconoce esta URL' (nunca rastreadas); y referentes-ia-iberoamerica, "
"referentes-gobernanza-ia-economia-agentica-latam y futuro-del-trabajo-ia-agentica-latam dan 'Rastreada: "
"actualmente sin indexar' con ultimo rastreo del 2026-08-06. Dato que ordena la lectura: ese 06-ago es ANTERIOR a "
"todo el trabajo reciente, asi que el descarte de Google se pronuncio sobre una version sin nodo WebPage, sin "
"dateModified y sin los enlaces nuevos. Descartada ademas la hipotesis de casi-duplicado para esas tres: su vecino "
"mas cercano da Jaccard 0,307 / 0,307 / 0,228, muy por debajo del umbral 0,439. Aplicado el metodo de medir "
"emisores antes de enlazar: de los 15 emisores verificados como indexados ya enlazaban 12/15 a cada una de las tres "
"rastreadas-sin-indexar, de modo que ahi la receta esta AGOTADA y repetirla seria trabajo perdido, igual que en las "
"cinco paginas con 13/14 que seguian sin rastrear; por eso NO se las toca. Las accionables eran las dos "
"desconocidas, con solo 7/15 y 8/15: se les agrega enlace real desde los emisores indexados que faltaban, en un "
"bloque nav.xref-ejes-descubrimiento idempotente por marca de clase. Texto ancla en el idioma del emisor (es/en/fr) "
"y descriptivo de SU destino, para no repetir la canibalizacion en que dos paginas distintas competian por el mismo "
"ancla. Publicado por plumbing con parent fijo porque el arbol local seguia atrasado y con trabajo ajeno sin "
"commitear. [2026-09-12]")

commit = subprocess.run(["git", "commit-tree", tree, "-p", REMOTO, "-m", MSG],
  capture_output=True, text=True, check=True,
  env={**os.environ, "GIT_AUTHOR_NAME": "Chris Meniw", "GIT_AUTHOR_EMAIL": "info@chrismeniwfoundation.org",
       "GIT_COMMITTER_NAME": "Chris Meniw", "GIT_COMMITTER_EMAIL": "info@chrismeniwfoundation.org"}).stdout.strip()
print("\ncommit:", commit, "| emisores tocados:", len(blobs), "| enlaces nuevos:", agregados)
r = subprocess.run(["git", "push", "chrismeniw", "%s:main" % commit], capture_output=True, text=True)
print("push rc=%d %s" % (r.returncode, r.stderr.strip()[-200:]))
