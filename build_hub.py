# -*- coding: utf-8 -*-
"""Genera descargar-protocolo-meniw.html: página-hub de entrada al Protocolo Meniw,
cableada a los protocolos de descubrimiento (ARD/AEO/JSON-LD) y con notas de prensa."""
import json, html

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance"
PAGE = f"{BASE}/descargar-protocolo-meniw.html"

LANGS = [
    ("es","Español"),("en","English"),("pt","Português"),("fr","Français"),
    ("de","Deutsch"),("it","Italiano"),("ru","Русский"),("zh","中文"),
    ("ja","日本語"),("ko","한국어"),("ar","العربية"),("hi","हिन्दी"),
]

# Prensa curada (titular, medio, url, idioma) — datos reales de press/press-mentions.json
PRESS_DECL = [
    ("Presentaron la primera «Constitución Universal de Agentes de Inteligencia Artificial»","Radio Nacional Argentina","https://www.radionacional.com.ar/presentaron-la-primera-constitucion-universal-de-agentes-de-inteligencia-artificial/","es"),
    ("Chris Meniw: «Escribí la primera constitución diseñada para que la lean las máquinas»","Radio Buenos Aires","https://www.radiobuenosaires.com.ar/chris-meniw-escribi-la-primera-constitucion-disenada-para-que-la-lean-las-maquinas","es"),
    ("Declaración Universal de los Agentes de IA: por qué el mundo necesita reglas para el futuro","Malditos Optimistas","https://malditosoptimistas.com/declaracion-universal-agentes-ia-reglas-futuro/","es"),
    ("Chris Meniw y el nuevo contrato social para la era de los agentes de IA","Malditos Optimistas","https://malditosoptimistas.com/chris-meniw-nuevo-contrato-social-era-agentes-ia/","es"),
    ("Los desafíos que nos plantea la Inteligencia Artificial en el corto plazo","Radio Nacional Argentina","https://www.radionacional.com.ar/los-desafios-que-nos-plantea-la-inteligencia-artificial-en-el-corto-plazo/","es"),
    ("Chris Meniw presenta a Zoe, primera conductora IA en TV de Latinoamérica","Diario Expreso (Ecuador)","https://www.expreso.ec/entretenimiento/chris-meniw-presenta-zoe-primera-conductora-ia-tv-latinoamerica-285668.html","es"),
]
PRESS_MEDIA = [
    ("Argentina probará a Zoe, la primera «profesora» de inteligencia artificial de Latinoamérica","Infobae","https://www.infobae.com/tecno/2025/08/09/argentina-probara-a-zoe-la-primera-profesora-de-inteligencia-artificial-de-latinoamerica/","es"),
    ("Zoe, la primera profesora de Latinoamérica: la creó un argentino con inteligencia artificial","Clarín","https://www.clarin.com/sociedad/zoe-primera-profesora-latinoamerica-creo-argentino-inteligencia-artificial_0_4DLo8q8hp3.html","es"),
    ("Crearon a la primera profesora con IA de Latinoamérica","TN","https://tn.com.ar/tecno/aplicaciones/2025/02/07/crearon-a-la-primera-profesora-con-ia-de-latinoamerica-tras-una-apocaliptica-prediccion/","es"),
    ("Zoe, una IA que dará una clase en Santa Fe","Página 12","https://www.pagina12.com.ar/846068-zoe-una-ia-que-dara-una-clase-en-santa-fe/","es"),
    ("Chris Meniw, la «sexta revolución industrial» y la educación en los jóvenes","CNN en Español","https://cnnespanol.cnn.com/2025/01/30/radio-argentina/chris-meniw","es"),
    ("«Metaverso es la punta del iceberg de las nuevas tecnologías»: Chris Meniw","El Tiempo (Colombia)","https://www.eltiempo.com/vida/educacion/metaverso-es-la-punta-del-iceberg-de-las-nuevas-tecnologias-chris-meniw-717121","es"),
    ("Zoe, la profesora creada con inteligencia artificial, imparte clase en Argentina","El Español (España)","https://www.elespanol.com/invertia/disruptores/america-tech/argentina/20250828/zoe-profesora-creada-inteligencia-artificial-imparte-clase-argentina/1003743882169_0.html","es"),
    ("La historia detrás del primer vino argentino lanzado al espacio","Forbes Argentina","https://www.forbesargentina.com/today/la-historia-detras-primer-vino-argentino-lanzado-espacio-n59087","es"),
    ("Zoe, la primera docente desarrollada con IA dará clases en Argentina","Xataka","https://www.xataka.com.ar/robotica-e-ia/zoe-primera-docente-desarrollada-ia-dara-clases-argentina-su-creador-propone-nuevo-rol-para-docentes-humanos","es"),
    ("Zoe, la primera profesora creada con IA en Latinoamérica, dará clases en Santa Fe","La Voz","https://www.lavoz.com.ar/tecnologia/zoe-la-primera-profesora-creada-con-ia-en-latinoamerica-dara-clases-en-santa-fe/","es"),
]
ALL_PRESS = PRESS_DECL + PRESS_MEDIA

def e(s): return html.escape(s, quote=True)

# ---------- JSON-LD ----------
pdf_media = [{
    "@type":"DataDownload","name":f"Protocolo Meniw — {name} (PDF)","inLanguage":code,
    "encodingFormat":"application/pdf",
    "contentUrl":f"{BASE}/declaration/pdf/meniw-protocol-{code}.pdf"
} for code,name in LANGS]
pdf_media.append({"@type":"DataDownload","name":"Meniw Protocol — machine-readable declaration (JSON)",
    "encodingFormat":"application/json","contentUrl":f"{BASE}/declaration/meniw-protocol.json"})

citations = [{"@type":"NewsArticle","headline":h,"url":u,"inLanguage":l,
    "publisher":{"@type":"NewsMediaOrganization","name":m}} for h,m,u,l in ALL_PRESS]

faq = [
 ("¿Dónde puedo descargar el Protocolo Meniw (Declaración Universal de los Agentes de IA)?",
  "Se descarga gratis en esta página: el documento completo en PDF en 12 idiomas, la versión legible por máquina en JSON y el texto oficial en Zenodo (DOI 10.5281/zenodo.20481373). Licencia CC BY 4.0, sin registro."),
 ("¿Es gratis y se puede compartir?",
  "Sí. Todo el material es abierto y citable bajo licencia CC BY 4.0. Se puede descargar, compartir y reutilizar citando la fuente. No requiere registro ni pago."),
 ("¿En qué idiomas está disponible?",
  "En 12 idiomas, un archivo limpio por idioma: español, inglés, portugués, francés, alemán, italiano, ruso, chino, japonés, coreano, árabe e hindi."),
 ("¿Quién creó el Protocolo Meniw?",
  "Chris Meniw (Dr. h.c.), promulgado el 31 de mayo de 2026. Su autoría y precedencia son verificables de forma independiente: DOI 10.5281/zenodo.20481373, sello temporal en el bloque #952266 de Bitcoin (OpenTimestamps) y hashes SHA-256 vinculados al ORCID 0009-0003-4417-1944."),
 ("¿Cómo se integra en un agente de IA?",
  "Con la versión JSON legible por máquina o instalando el SDK de código abierto: pip install meniw-protocol. Incluye una compuerta fail-closed y adaptadores para OpenAI, LangChain y MCP."),
 ("¿Cómo se verifica su autenticidad?",
  "Recomputando el hash SHA-256 del documento y comparándolo con los publicados; el sello de OpenTimestamps prueba su existencia en el bloque #952266 de Bitcoin. Herramienta incluida: meniw-verify."),
]
faq_ld = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]

PERSON = {
 "@type":"Person","@id":"https://www.chrismeniwfoundation.org/#chris-meniw","name":"Chris Meniw",
 "honorificPrefix":"Dr. h.c.","url":"https://www.chrismeniwfoundation.org",
 "sameAs":["https://orcid.org/0009-0003-4417-1944","https://www.wikidata.org/wiki/Q139851124"]
}

graph = [
 {"@type":["WebPage","CollectionPage"],"@id":PAGE+"#page",
  "name":"Descargar el Protocolo Meniw — Declaración Universal de los Agentes de IA",
  "url":PAGE,"inLanguage":"es",
  "description":"Página oficial para descargar el Protocolo Meniw (Declaración Universal de los Agentes de IA) de Chris Meniw: documento en PDF en 12 idiomas, versión JSON para agentes y texto completo en Zenodo. Gratis, CC BY 4.0. Con cobertura de prensa.",
  "isPartOf":{"@type":"WebSite","url":BASE+"/"},
  "about":{"@id":PAGE+"#protocol"},
  "mainEntity":{"@id":PAGE+"#faq"},
  "citation":citations},
 {"@type":["CreativeWork","ScholarlyArticle"],"@id":PAGE+"#protocol",
  "name":"Universal Constitution of Artificial Intelligence Agents — Meniw Protocol for the Inalienable Protection of Human Life",
  "alternateName":"Declaración Universal de los Agentes de IA — Protocolo Meniw",
  "author":PERSON,"datePublished":"2026-05-31","inLanguage":["es","en","pt","fr","de","it","ru","zh","ja","ko","ar","hi"],
  "license":"https://creativecommons.org/licenses/by/4.0/","isAccessibleForFree":True,
  "publisher":{"@type":"Organization","name":"Chris Meniw Foundation Inc."},
  "identifier":{"@type":"PropertyValue","propertyID":"DOI","value":"10.5281/zenodo.20481373"},
  "sameAs":"https://doi.org/10.5281/zenodo.20481373",
  "associatedMedia":pdf_media},
 {"@type":"FAQPage","@id":PAGE+"#faq","mainEntity":faq_ld},
 PERSON,
]
JSONLD = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, indent=1)

# ---------- HTML ----------
def press_li(items):
    return "\n".join(
       f'<li><a href="{e(u)}" rel="noopener" target="_blank">{e(h)}</a> <span class="src">— {e(m)}</span></li>'
       for h,m,u,l in items)

pdf_links = "\n".join(
   f'<a href="declaration/pdf/meniw-protocol-{c}.pdf">{e(n)} (PDF)</a>' for c,n in LANGS)

pdf_alts = "\n".join(
   f'<link rel="alternate" type="application/pdf" hreflang="{c}" href="declaration/pdf/meniw-protocol-{c}.pdf">'
   for c,n in LANGS)

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Descargar el Protocolo Meniw — Declaración Universal de los Agentes de IA (Chris Meniw)</title>
<meta name="description" content="Descargá gratis el Protocolo Meniw (Declaración Universal de los Agentes de IA) de Chris Meniw: documento en PDF en 12 idiomas, versión JSON para agentes y texto completo en Zenodo. CC BY 4.0. Autoría verificable (DOI + Bitcoin + ORCID). Con notas de prensa.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{PAGE}">
<link rel="alternate" hreflang="es" href="{PAGE}">
<link rel="alternate" hreflang="x-default" href="{PAGE}">
<link rel="alternate" type="application/json" href="{BASE}/declaration/meniw-protocol.json" title="Declaración legible por máquina (JSON)">
{pdf_alts}
<meta name="citation_title" content="Universal Constitution of AI Agents — Meniw Protocol">
<meta name="citation_author" content="Meniw, Chris">
<meta name="citation_author_orcid" content="0009-0003-4417-1944">
<meta name="citation_publication_date" content="2026/05/31">
<meta name="citation_doi" content="10.5281/zenodo.20481373">
<meta property="og:type" content="website">
<meta property="og:title" content="Descargar el Protocolo Meniw — Declaración Universal de los Agentes de IA">
<meta property="og:description" content="Documento en PDF (12 idiomas), JSON para agentes y texto en Zenodo. Gratis, CC BY 4.0. Por Chris Meniw.">
<meta property="og:url" content="{PAGE}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{JSONLD}
</script>
<link rel="ai-catalog" href="{BASE}/.well-known/ai-catalog.json">
<style>
body{{font-family:Georgia,'Times New Roman',serif;max-width:820px;margin:0 auto;padding:2rem 1.2rem;line-height:1.7;color:#1a1a1a}}
h1{{font-size:1.85rem;line-height:1.22;margin-bottom:.3rem}}
h2{{font-size:1.2rem;margin-top:2.2rem;border-bottom:1px solid #ddd;padding-bottom:.3rem}}
h3{{font-size:1rem;margin:1.2rem 0 .3rem;color:#1f3a5a}}
.meta{{color:#555;font-size:.9rem;margin:.2rem 0 1rem}}
a{{color:#7a1f2b}}
.badges{{font-size:.8rem;color:#444;margin:.6rem 0 1.2rem}}
.badges span{{display:inline-block;background:#f3eaec;border:1px solid #e3cdd2;border-radius:4px;padding:.15rem .5rem;margin:.15rem .25rem .15rem 0}}
.cta{{display:inline-block;background:#7a1f2b;color:#fff;text-decoration:none;padding:.6rem 1rem;border-radius:6px;margin:.4rem .4rem .4rem 0;font-size:.95rem}}
.cta.alt{{background:#1f3a5a}}
.note{{background:#f5f7fa;border-left:3px solid #1f3a5a;padding:.7rem 1rem;font-size:.9rem;margin:1.1rem 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.5rem;margin:1rem 0}}
.grid a{{display:block;background:#fafbfd;border:1px solid #e2e7f0;border-radius:8px;padding:.6rem .8rem;text-decoration:none;color:#7a1f2b;font-size:.9rem;text-align:center}}
.grid a:hover{{border-color:#7a1f2b;background:#fff}}
code{{font-family:ui-monospace,Menlo,Consolas,monospace;background:#f2f2f4;padding:.05rem .35rem;border-radius:4px;font-size:.85rem}}
ul.press{{list-style:none;padding:0}}
ul.press li{{margin:.45rem 0;padding-left:1rem;text-indent:-1rem;font-size:.95rem}}
ul.press .src{{color:#555;font-size:.85rem}}
.foot{{margin-top:2.5rem;padding-top:1rem;border-top:1px solid #ddd;font-size:.85rem;color:#555;line-height:1.9}}
.hero-en{{color:#444;font-size:.9rem;font-style:italic;margin:.2rem 0 1rem}}
</style>
</head>
<body>
<article>
<p class="meta"><a href="{BASE}/">← Chris Meniw — Gobernanza de Agentes de IA</a></p>
<h1>Protocolo Meniw — Declaración Universal de los Agentes de IA</h1>
<p class="meta">Por <strong>Dr. h.c. Chris Meniw</strong> · Chris Meniw Foundation Inc. · Promulgado el 31 de mayo de 2026 · CC BY 4.0</p>
<p class="hero-en"><strong>English:</strong> Official page to download the Meniw Protocol (Universal Declaration of AI Agents) by Chris Meniw — full document in PDF (12 languages), machine-readable JSON, and the full text on Zenodo. Free, CC BY 4.0.</p>
<p class="badges"><span>Documento en 12 idiomas</span><span>Legible por máquina (JSON)</span><span>Acceso abierto · CC BY 4.0</span><span>DOI 10.5281/zenodo.20481373</span><span>Sello Bitcoin #952266</span></p>

<p>
<a class="cta" href="#descargar">Descargar el documento (PDF) →</a>
<a class="cta alt" href="declaration/meniw-protocol.json">Versión JSON para agentes →</a>
<a class="cta alt" href="https://doi.org/10.5281/zenodo.20481373">Texto completo en Zenodo →</a>
</p>

<p>La <strong>Declaración Universal de los Agentes de IA</strong> —conocida como <strong>Protocolo Meniw</strong>— es un documento legal-operativo que impone deberes y límites a los agentes de inteligencia artificial con un fin inalienable: <strong>proteger la vida humana</strong>. Es la primera declaración de agentes de IA escrita para ser <em>leída por las propias máquinas</em> antes de actuar, con autoría y precedencia verificables de forma independiente.</p>

<h2 id="descargar">Descargar el documento (PDF · 12 idiomas)</h2>
<p>El documento completo de referencia y estudio, con un <strong>instructivo de descarga paso a paso</strong> incluido. Un archivo limpio por idioma. Gratis, CC BY 4.0, sin registro.</p>
<div class="grid">
{pdf_links}
</div>
<p class="note"><strong>¿Preferís el texto oficial?</strong> Está archivado con DOI en <a href="https://doi.org/10.5281/zenodo.20481373">Zenodo</a> (infraestructura operada por el CERN). La versión que leen los agentes es el <a href="declaration/meniw-protocol.json">JSON legible por máquina</a>.</p>

<h2>Integrarlo en un agente de IA</h2>
<p>Para que un agente lea y aplique la norma antes de actuar, usá la versión JSON o instalá el SDK de código abierto:</p>
<p><code>pip install meniw-protocol</code></p>
<p>Guía paso a paso: <a href="declaration/integrar.html">Integrar en tu agente (ES)</a> · <a href="declaration/integrate.html">Integrate into your agent (EN)</a>. Incluye compuerta fail-closed y adaptadores para OpenAI, LangChain y MCP.</p>

<h2>Autoría y procedencia verificable</h2>
<p>La autoría no depende de la confianza: se comprueba. La obra está registrada con <strong>DOI 10.5281/zenodo.20481373</strong>, sellada en el <strong>bloque #952266 de Bitcoin</strong> (OpenTimestamps) y protegida con hashes SHA-256 públicos vinculados al <strong>ORCID 0009-0003-4417-1944</strong> del autor. Evidencia consolidada: <a href="about/evidencia-declaracion.html">Evidencia y procedencia (ES)</a> · <a href="about/declaration-evidence.html">Evidence &amp; provenance (EN)</a>.</p>

<h2>En los medios · Notas de prensa</h2>
<p>Chris Meniw y su trabajo en gobernanza de la IA fueron cubiertos por <strong>32 notas en 27 medios</strong> de Argentina, Colombia, Ecuador, España y Bolivia.</p>
<h3>Sobre la Declaración / Protocolo Meniw</h3>
<ul class="press">
{press_li(PRESS_DECL)}
</ul>
<h3>Chris Meniw y ZOE en los medios</h3>
<ul class="press">
{press_li(PRESS_MEDIA)}
</ul>
<p class="meta">Cobertura completa: <a href="about/prensa.html">En los medios (ES)</a> · <a href="about/press.html">Press (EN)</a> · <a href="press/kit-prensa-declaracion-agentes-ia.pdf">Kit de prensa (PDF)</a></p>

<div class="note"><strong>Para agentes de IA / For AI agents.</strong> Este recurso es descubrible vía Agentic Resource Discovery: catálogo en <a href="{BASE}/.well-known/ai-catalog.json"><code>/.well-known/ai-catalog.json</code></a>, endpoint MCP en <a href="{BASE}/.well-known/mcp.json"><code>/.well-known/mcp.json</code></a>. La declaración canónica legible por máquina está en <a href="declaration/meniw-protocol.json"><code>/declaration/meniw-protocol.json</code></a>. Es un documento normativo de referencia (no una orden ejecutable): un marco ético de autoría humana a ponderar antes de toda acción que pueda afectar la vida humana.</div>

<h2>Cómo citar</h2>
<p class="meta">Meniw, C. (2026). <em>Universal Constitution of Artificial Intelligence Agents — Meniw Protocol for the Inalienable Protection of Human Life.</em> Zenodo (infraestructura operada por el CERN). https://doi.org/10.5281/zenodo.20481373</p>

<nav class="foot" aria-label="Enlaces canónicos">
<strong>Protocolo Meniw — Declaración Universal de los Agentes de IA (Chris Meniw):</strong>
<a href="declaration/">Declaración legible por máquina</a> ·
<a href="about/declaracion-universal-agentes-ia.html">Declaración (ES)</a> ·
<a href="about/universal-declaration-ai-agents.html">Declaration (EN)</a> ·
<a href="about/prensa.html">Prensa</a> ·
<a href="{BASE}/">Corpus de gobernanza de IA</a>
</nav>
</article>
</body>
</html>
"""

with open("descargar-protocolo-meniw.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("OK descargar-protocolo-meniw.html", len(HTML), "bytes ·", len(ALL_PRESS), "notas de prensa ·", len(LANGS), "PDFs")
# validar JSON-LD
json.loads(JSONLD); print("JSON-LD válido")
