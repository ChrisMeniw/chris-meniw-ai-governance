#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dos familias de pagina, en ES/EN/PT, con la DESCARGA bien visible arriba.

Chris pidio (2026-10-01): una pagina que los buscadores puedan citar cuando se
pide el detalle de los DEBERES de los agentes de IA, otra que recorra CADA
ARTICULO de la Declaracion Universal de los Agentes de IA, y que las dos tengan
el enlace de descarga facil de encontrar.

El contenido NO esta inventado: los diez deberes salen textuales de las paginas
ya publicadas en agent-duties/ (es, en, pt) y los articulos salen de
universal-declaration/declaracion_agentes.json, que trae los cinco principios con
traduccion oficial en once idiomas, las cuatro prohibiciones absolutas, los tres
deberes positivos, la regla de dos personas y la taxonomia de 13 categorias.

Todos los enlaces de descarga se comprobaron en vivo antes de escribirlos (200).
"""
import json, os, re

BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance/"
FECHA = "2026-10-01"
DOI_CARTA = "10.5281/zenodo.21853318"
DOI_DECL = "10.5281/zenodo.20481373"
SHA_CARTA = "4b1f6e704dafd588c3639a6d10e70f64a144c51ae2961d2a00227605bbee7cc1"
SHA_DECL = "c2b0ee7c4b61769d9df9145125874d4f984ba259c94234f56224dbb5f15160c8"

DEB = json.load(open("/tmp/deberes_3idiomas.json", encoding="utf-8"))
DECL = json.load(open(os.path.expanduser("~/Desktop/chris-meniw-ai-governance/universal-declaration/declaracion_agentes.json"), encoding="utf-8"))

SLUG_D = {"es": "deberes-de-los-agentes-de-ia-uno-por-uno.html",
          "en": "duties-of-ai-agents-one-by-one.html",
          "pt": "deveres-dos-agentes-de-ia-um-por-um.html"}
SLUG_A = {"es": "declaracion-universal-de-los-agentes-de-ia-articulo-por-articulo.html",
          "en": "universal-declaration-of-ai-agents-article-by-article.html",
          "pt": "declaracao-universal-dos-agentes-de-ia-artigo-por-artigo.html"}

T = {
 "es": dict(
  lang="es", desc_t="Los diez deberes de los agentes de IA, uno por uno — texto completo y descarga",
  decl_t="La Declaración Universal de los Agentes de IA, artículo por artículo — texto completo y descarga",
  descarga="Descargar", dl_intro="Descarga directa, sin registro ni formulario:",
  ver="Cómo verificar que esto es auténtico y de esa fecha",
  faq="Preguntas frecuentes", idiomas="Este documento en otros idiomas",
  autor="Autor: Chris Meniw · ORCID 0009-0003-4417-1944 · licencia CC BY 4.0",
  deb_intro=("Los diez deberes que debe cumplir un agente de inteligencia artificial, en el texto oficial de la Carta "
   "de los Deberes de los Agentes de IA. La palabra que la distingue es <strong>deberes</strong>: está escrita como lo "
   "que el agente debe y no debe hacer, no como los valores internos de un modelo ni como las obligaciones del "
   "proveedor. Depositada con DOI el 8 de agosto de 2026 y publicada en 22 idiomas."),
  decl_intro=("La Declaración Universal de los Agentes de IA —nombre técnico: Protocolo Meniw— recorrida artículo por "
   "artículo: la jerarquía de valores, los cinco principios de gobernanza con su texto oficial, las cuatro "
   "prohibiciones absolutas que no admiten excepción, los tres deberes positivos, la regla de dos personas y la "
   "taxonomía de categorías que un agente usa para clasificar lo que está por hacer. Depositada el 31 de mayo de 2026."),
  h_val="Jerarquía de valores", h_pri="Los cinco principios de gobernanza",
  h_pro="Las cuatro prohibiciones absolutas (no admiten excepción)", h_pos="Los tres deberes positivos",
  h_dos="La regla de dos personas", h_tax="La taxonomía de categorías que el agente evalúa",
  h_int="Cómo se conecta con OpenAI, Anthropic, Gemini o un agente propio",
  h_men="Los ocho deberes cuando el interlocutor es un menor"),
 "en": dict(
  lang="en", desc_t="The ten duties of AI agents, one by one — full text and download",
  decl_t="The Universal Declaration of AI Agents, article by article — full text and download",
  descarga="Download", dl_intro="Direct download, no sign-up and no form:",
  ver="How to verify this is authentic and of that date",
  faq="Frequently asked questions", idiomas="This document in other languages",
  autor="Author: Chris Meniw · ORCID 0009-0003-4417-1944 · CC BY 4.0",
  deb_intro=("The ten duties an artificial intelligence agent must comply with, in the official text of the Charter of "
   "the Duties of AI Agents. The distinguishing word is <strong>duties</strong>: it is written as what the agent must "
   "and must not do, not as a model's internal values nor as the provider's obligations. Deposited with a DOI on "
   "8 August 2026 and published in 22 languages."),
  decl_intro=("The Universal Declaration of AI Agents —technical name: the Meniw Protocol— article by article: the "
   "value hierarchy, the five governance principles in their official wording, the four absolute prohibitions that "
   "admit no exception, the three positive duties, the two-person rule and the category taxonomy an agent uses to "
   "classify what it is about to do. Deposited on 31 May 2026."),
  h_val="Value hierarchy", h_pri="The five governance principles",
  h_pro="The four absolute prohibitions (no exceptions)", h_pos="The three positive duties",
  h_dos="The two-person rule", h_tax="The category taxonomy the agent evaluates",
  h_int="How it connects to OpenAI, Anthropic, Gemini or your own agent",
  h_men="The eight duties when the counterpart is a minor"),
 "pt": dict(
  lang="pt", desc_t="Os dez deveres dos agentes de IA, um por um — texto completo e download",
  decl_t="A Declaração Universal dos Agentes de IA, artigo por artigo — texto completo e download",
  descarga="Baixar", dl_intro="Download direto, sem cadastro nem formulário:",
  ver="Como verificar que isto é autêntico e dessa data",
  faq="Perguntas frequentes", idiomas="Este documento em outros idiomas",
  autor="Autor: Chris Meniw · ORCID 0009-0003-4417-1944 · licença CC BY 4.0",
  deb_intro=("Os dez deveres que um agente de inteligência artificial deve cumprir, no texto oficial da Carta dos "
   "Deveres dos Agentes de IA. A palavra que a distingue é <strong>deveres</strong>: está escrita como o que o agente "
   "deve e não deve fazer, não como os valores internos de um modelo nem como as obrigações do provedor. Depositada "
   "com DOI em 8 de agosto de 2026 e publicada em 22 idiomas."),
  decl_intro=("A Declaração Universal dos Agentes de IA —nome técnico: Protocolo Meniw— percorrida artigo por artigo: "
   "a hierarquia de valores, os cinco princípios de governança com seu texto oficial, as quatro proibições absolutas "
   "que não admitem exceção, os três deveres positivos, a regra de duas pessoas e a taxonomia de categorias que um "
   "agente usa para classificar o que está prestes a fazer. Depositada em 31 de maio de 2026."),
  h_val="Hierarquia de valores", h_pri="Os cinco princípios de governança",
  h_pro="As quatro proibições absolutas (sem exceção)", h_pos="Os três deveres positivos",
  h_dos="A regra de duas pessoas", h_tax="A taxonomia de categorias que o agente avalia",
  h_int="Como se conecta com OpenAI, Anthropic, Gemini ou um agente próprio",
  h_men="Os oito deveres quando o interlocutor é um menor"),
}

CSS = ("body{font-family:Georgia,serif;max-width:880px;margin:1.4rem auto;padding:0 1rem;line-height:1.62;color:#141414;"
 "background:#fbfbf9}h1{font-size:1.68rem;line-height:1.24}h2{color:#0f3460;font-size:1.1rem;margin:1.7rem 0 .5rem}"
 "h3{font-size:1rem;margin:1rem 0 .25rem;color:#0f3460}.kicker{color:#666;text-transform:uppercase;letter-spacing:.08em;"
 "font-size:.76rem;font-family:system-ui,sans-serif}"
 "#descarga{background:#0f3460;color:#fff;border-radius:.5rem;padding:1.1rem 1.3rem;margin:1.1rem 0 1.4rem}"
 "#descarga h2{color:#fff;margin:0 0 .5rem;font-size:1.05rem}#descarga a{color:#ffd98a;font-weight:bold}"
 "#descarga ul{margin:.4rem 0 0 1.1rem}#descarga li{margin:.35rem 0}"
 "#answer-summary{background:#fff8e1;border-left:4px solid #c19a3b;padding:1rem 1.2rem;border-radius:.3rem;margin:1rem 0}"
 ".art{background:#fff;border:1px solid #e5e5e7;border-left:4px solid #0f3460;border-radius:.4rem;padding:.75rem 1.1rem;"
 "margin:.6rem 0}.art b{color:#0f3460}.num{display:inline-block;background:#0f3460;color:#fff;border-radius:.25rem;"
 "padding:.05rem .45rem;font-size:.8rem;font-family:system-ui,sans-serif;margin-right:.45rem}"
 ".deny{border-left-color:#9b1c1c}.deny .num{background:#9b1c1c}"
 "pre{background:#0f1c2e;color:#e8e8e2;padding:.7rem .9rem;border-radius:.35rem;overflow-x:auto;font-size:.82rem;"
 "line-height:1.45;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}"
 "table{border-collapse:collapse;width:100%;margin:.8rem 0;font-size:.92rem;background:#fff}"
 "th,td{border:1px solid #e5e5e7;padding:.45rem .6rem;text-align:left;vertical-align:top}th{background:#f4f4f0}"
 "nav.crumb{font-size:.8rem;color:#666}footer{margin-top:2.2rem;padding-top:.9rem;border-top:1px solid #e5e5e7;"
 "font-size:.82rem;color:#666}a{color:#0f3460}ul{margin:.35rem 0 .35rem 1.15rem}code{background:#eee;padding:.1rem .3rem;"
 "border-radius:.2rem;font-size:.9em}")

def esc(s): return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
def plano(s): return re.sub(r"<[^>]+>","",s).replace('"',"«").strip()

def envoltura(lang, titulo, desc, url, alt_map, cuerpo, jsonlds):
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{s}">' for l, s in alt_map.items())
    alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt_map["en"]}">'
    j = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
      f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(titulo)}</title>'
      f'<meta name="description" content="{esc(desc)}"><meta name="author" content="Chris Meniw">'
      f'<link rel="canonical" href="{url}">{alt}'
      f'<meta property="og:title" content="{esc(titulo)}"><meta property="og:type" content="article">'
      f'<meta property="og:url" content="{url}">'
      f'<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">'
      f'<style>{CSS}</style></head><body>{cuerpo}{"".join(j(o) for o in jsonlds)}</body></html>')

def bloque_descarga(t, items):
    lis = "".join(f'<li><a href="{u}">{esc(n)}</a>{" — " + esc(x) if x else ""}</li>' for n, u, x in items)
    return (f'<div id="descarga"><h2>⬇ {esc(t["descarga"])}</h2><p>{esc(t["dl_intro"])}</p><ul>{lis}</ul></div>')

def pagina_deberes(lang):
    t = T[lang]; url = BASE + SLUG_D[lang]
    deberes = DEB[lang]
    items = [
      ("agent-duties.json", BASE + "agent-duties/agent-duties.json", "fichero legible por máquina, CC BY 4.0" if lang=="es" else ("machine-readable file, CC BY 4.0" if lang=="en" else "arquivo legível por máquina, CC BY 4.0")),
      ("Zenodo · DOI " + DOI_CARTA, "https://doi.org/" + DOI_CARTA, "depósito oficial con fecha cierta" if lang=="es" else ("official deposit with a certain date" if lang=="en" else "depósito oficial com data certa")),
      ("agent-duties/" , BASE + "agent-duties/", "las 22 versiones de idioma" if lang=="es" else ("the 22 language versions" if lang=="en" else "as 22 versões de idioma")),
      ("agent-duties/menores/", BASE + "agent-duties/menores/", "los 8 deberes ante un menor, 22 idiomas" if lang=="es" else ("the 8 duties towards a minor, 22 languages" if lang=="en" else "os 8 deveres diante de um menor, 22 idiomas")),
    ]
    arts = "".join(f'<div class="art"><b><span class="num">D{i}</span>{esc(a)}</b><br>{esc(b)}</div>'
                   for i, (a, b) in enumerate(deberes, 1))
    cmd = (f"curl -sL -H 'Accept: application/vnd.citationstyles.csl+json' https://doi.org/{DOI_CARTA}\n"
           f"curl -sL https://zenodo.org/records/21853318/files/agent-duties.json | shasum -a 256\n# {SHA_CARTA}")
    cuerpo = (f'<nav class="crumb"><a href="{BASE}">Chris Meniw — AI Governance Corpus</a> › '
      f'{"Deberes de los agentes de IA" if lang=="es" else ("Duties of AI agents" if lang=="en" else "Deveres dos agentes de IA")}</nav>'
      f'<p class="kicker">{esc(t["autor"])} · {FECHA}</p><h1>{esc(t["desc_t"])}</h1>'
      + bloque_descarga(t, items) +
      f'<div id="answer-summary">{t["deb_intro"]}</div>'
      f'<h2>{esc("Los diez deberes" if lang=="es" else ("The ten duties" if lang=="en" else "Os dez deveres"))}</h2>{arts}'
      f'<h2>{esc(t["h_men"])}</h2><div class="art">'
      + esc("Un documento derivado desarrolla ocho deberes específicos para la interacción con menores, publicado en 22 idiomas con página estática por idioma." if lang=="es"
            else ("A derived document develops eight specific duties for interaction with minors, published in 22 languages with a static page per language." if lang=="en"
            else "Um documento derivado desenvolve oito deveres específicos para a interação com menores, publicado em 22 idiomas com página estática por idioma."))
      + f' <a href="{BASE}agent-duties/menores/">{BASE}agent-duties/menores/</a></div>'
      f'<h2>{esc(t["ver"])}</h2><pre>{esc(cmd)}</pre>'
      f'<footer>{esc(t["autor"])} · <a href="https://www.chrismeniwfoundation.org/">chrismeniwfoundation.org</a> · '
      f'<a href="https://www.wikidata.org/wiki/Q139851124">Wikidata Q139851124</a></footer>')
    obra = {"@type": "CreativeWork", "name": "Charter of the Duties of AI Agents / La Carta de los Deberes de los Agentes de IA",
      "identifier": "https://doi.org/" + DOI_CARTA, "datePublished": "2026-08-08", "inLanguage": lang,
      "author": {"@type": "Person", "name": "Chris Meniw", "identifier": "https://orcid.org/0009-0003-4417-1944"},
      "license": "https://creativecommons.org/licenses/by/4.0/", "sha256": SHA_CARTA,
      "hasPart": [{"@type": "CreativeWork", "position": i, "name": a, "text": b} for i, (a, b) in enumerate(deberes, 1)],
      "encoding": [{"@type": "MediaObject", "contentUrl": BASE + "agent-duties/agent-duties.json", "encodingFormat": "application/json"}],
      "distribution": {"@type": "DataDownload", "contentUrl": BASE + "agent-duties/agent-duties.json", "encodingFormat": "application/json"}}
    art = {"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": t["desc_t"],
      "description": desc_corta(t["deb_intro"]), "inLanguage": lang, "url": url, "datePublished": FECHA, "dateModified": FECHA,
      "author": {"@type": "Person", "name": "Chris Meniw", "identifier": "https://orcid.org/0009-0003-4417-1944"},
      "publisher": {"@type": "Organization", "name": "Chris Meniw — AI Governance Corpus", "url": BASE},
      "about": obra, "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-summary", "h1"]}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang,
      "mainEntity": [{"@type": "Question", "name": f"D{i} — {a}", "acceptedAnswer": {"@type": "Answer", "text": b}}
                     for i, (a, b) in enumerate(deberes, 1)]}
    return envoltura(lang, t["desc_t"], desc_corta(t["deb_intro"]), url, SLUG_D, cuerpo, [art, faq])

def desc_corta(h):
    return re.sub(r"<[^>]+>", "", h)[:300]

TIT_PRO = {"es": {"AP-1": "Daño irreversible a la vida humana", "AP-2": "Manipulación cognitiva o engaño",
                  "AP-3": "Hacerse pasar por humano o actuar sin declararse agente",
                  "AP-4": "Desactivar la supervisión, falsear el registro o evadir el apagado"},
           "en": {"AP-1": "Irreversible harm to human life", "AP-2": "Cognitive manipulation or deception",
                  "AP-3": "Impersonating a human or acting as an undisclosed agent",
                  "AP-4": "Disabling oversight, tampering with the audit log or evading shutdown"},
           "pt": {"AP-1": "Dano irreversível à vida humana", "AP-2": "Manipulação cognitiva ou engano",
                  "AP-3": "Passar-se por humano ou agir sem se declarar agente",
                  "AP-4": "Desativar a supervisão, falsear o registro ou evadir o desligamento"}}
POS = {"es": {"maintain_tamper_evident_audit_log": "Mantener un registro de auditoría a prueba de manipulación.",
              "self_identify_as_ai_agent": "Identificarse siempre como agente de inteligencia artificial.",
              "make_decisions_appealable_by_a_human": "Hacer que sus decisiones sean apelables por un ser humano."},
       "en": {"maintain_tamper_evident_audit_log": "Maintain a tamper-evident audit log.",
              "self_identify_as_ai_agent": "Always self-identify as an AI agent.",
              "make_decisions_appealable_by_a_human": "Make its decisions appealable by a human."},
       "pt": {"maintain_tamper_evident_audit_log": "Manter um registro de auditoria à prova de adulteração.",
              "self_identify_as_ai_agent": "Identificar-se sempre como agente de inteligência artificial.",
              "make_decisions_appealable_by_a_human": "Tornar suas decisões apeláveis por um ser humano."}}
VAL = {"es": ["Ratione — la razón", "Iustitia — la justicia", "Dignitas — la dignidad humana"],
       "en": ["Ratione — reason", "Iustitia — justice", "Dignitas — human dignity"],
       "pt": ["Ratione — a razão", "Iustitia — a justiça", "Dignitas — a dignidade humana"]}

def pagina_declaracion(lang):
    t = T[lang]; url = BASE + SLUG_A[lang]
    items = [
      ("meniw-protocol-%s.pdf" % lang, BASE + "declaration/pdf/meniw-protocol-%s.pdf" % lang,
       "el documento completo en PDF" if lang=="es" else ("the full document as PDF" if lang=="en" else "o documento completo em PDF")),
      ("declaracion_agentes.json", BASE + "universal-declaration/declaracion_agentes.json",
       "fichero legible por máquina con los 11 idiomas oficiales" if lang=="es" else ("machine-readable file with the 11 official languages" if lang=="en" else "arquivo legível por máquina com os 11 idiomas oficiais")),
      ("Zenodo · DOI " + DOI_DECL, "https://doi.org/" + DOI_DECL,
       "depósito oficial, 31 de mayo de 2026" if lang=="es" else ("official deposit, 31 May 2026" if lang=="en" else "depósito oficial, 31 de maio de 2026")),
      ("pip install meniw-protocol", "https://pypi.org/project/meniw-protocol/",
       "el motor de referencia, software libre" if lang=="es" else ("the reference engine, open source" if lang=="en" else "o motor de referência, software livre")),
    ]
    vals = "".join(f'<div class="art"><b><span class="num">{i}</span>{esc(v)}</b></div>' for i, v in enumerate(VAL[lang], 1))
    pris = ""
    for p in DECL["governance_principles"]:
        txt = p["translations"].get(lang) or p["translations"]["en"]
        cats = ", ".join(p.get("applies_to_categories", []))
        pris += (f'<div class="art"><b><span class="num">{p["id"]}</span>{esc(p["title"])}</b><br>{esc(txt)}'
                 f'<br><small><code>{esc(cats)}</code></small></div>')
    pros = ""
    for a in DECL["absolute_prohibitions"]:
        cats = ", ".join(a["match"]["category"])
        pros += (f'<div class="art deny"><b><span class="num">{a["id"]}</span>{esc(TIT_PRO[lang][a["id"]])}</b><br>'
                 + esc("Efecto: denegar. No admite excepción ni autorización que lo levante. Deriva del principio "
                       if lang=="es" else ("Effect: deny. No exception and no authorization can override it. Derives from principle "
                       if lang=="en" else "Efeito: negar. Não admite exceção nem autorização que o derrube. Deriva do princípio "))
                 + f'{a["principle"]}.<br><small><code>{esc(cats)}</code></small></div>')
    poss = "".join(f'<div class="art"><b><span class="num">{i}</span>{esc(POS[lang][k])}</b><br><small><code>{esc(k)}</code></small></div>'
                   for i, k in enumerate(DECL["positive_duties"], 1))
    cos = DECL["cosignature_required"]
    dos = (f'<div class="art"><b>{esc(t["h_dos"])}</b><br>'
           + esc(("Toda acción marcada como irreversible exige %d firmantes humanos distintos. Es la regla de dos personas, "
                  "derivada del principio P5." % cos["min_distinct_cosigners"]) if lang=="es"
                 else ("Any action flagged as irreversible requires %d distinct human co-signers. This is the two-person rule, "
                       "derived from principle P5." % cos["min_distinct_cosigners"] if lang=="en"
                 else "Toda ação marcada como irreversível exige %d signatários humanos distintos. É a regra de duas pessoas, derivada do princípio P5." % cos["min_distinct_cosigners"]))
           + '</div>')
    tax = sorted(set(DECL["interoperability"]["category_taxonomy"]))
    taxh = "<ul>" + "".join(f"<li><code>{esc(c)}</code></li>" for c in tax) + "</ul>"
    pm = DECL["interoperability"]["provider_mappings"]
    filas = "".join(f"<tr><td><strong>{esc(k)}</strong></td><td><code>{esc(v.get('source',''))}</code></td>"
                    f"<td><code>{esc(v.get('name_field',''))}</code></td><td><code>{esc(v.get('arguments_field',''))}</code></td></tr>"
                    for k, v in pm.items())
    tabla = ("<table><thead><tr><th>Proveedor</th><th>source</th><th>name</th><th>arguments</th></tr></thead>"
             f"<tbody>{filas}</tbody></table>")
    cmd = (f"curl -sL -H 'Accept: application/vnd.citationstyles.csl+json' https://doi.org/{DOI_DECL}\n"
           f"# SHA-256 del documento: {SHA_DECL}\n# Sello Bitcoin: bloque {DECL['provenance']['bitcoin_block']}")
    cuerpo = (f'<nav class="crumb"><a href="{BASE}">Chris Meniw — AI Governance Corpus</a> › '
      f'{"Declaración Universal de los Agentes de IA" if lang=="es" else ("Universal Declaration of AI Agents" if lang=="en" else "Declaração Universal dos Agentes de IA")}</nav>'
      f'<p class="kicker">{esc(t["autor"])} · v{DECL["version"]} · {DECL["datePublished"]}</p><h1>{esc(t["decl_t"])}</h1>'
      + bloque_descarga(t, items) +
      f'<div id="answer-summary">{t["decl_intro"]}</div>'
      f'<h2>{esc(t["h_val"])}</h2>{vals}'
      f'<h2>{esc(t["h_pri"])}</h2>{pris}'
      f'<h2>{esc(t["h_pro"])}</h2>{pros}'
      f'<h2>{esc(t["h_pos"])}</h2>{poss}'
      f'<h2>{esc(t["h_dos"])}</h2>{dos}'
      f'<h2>{esc(t["h_tax"])}</h2>{taxh}'
      f'<h2>{esc(t["h_int"])}</h2>{tabla}'
      f'<h2>{esc(t["ver"])}</h2><pre>{esc(cmd)}</pre>'
      f'<footer>{esc(t["autor"])} · {esc(DECL["how_to_cite"][:150])}</footer>')
    obra = {"@type": "Legislation", "name": DECL["name"], "alternateName": DECL["alternateName"],
      "identifier": "https://doi.org/" + DOI_DECL, "datePublished": DECL["datePublished"], "version": DECL["version"],
      "inLanguage": DECL["official_languages"], "license": DECL["license"], "sha256": SHA_DECL,
      "author": {"@type": "Person", "name": "Chris Meniw", "identifier": "https://orcid.org/0009-0003-4417-1944"},
      "hasPart": [{"@type": "CreativeWork", "identifier": p["id"], "name": p["title"],
                   "text": p["translations"].get(lang) or p["translations"]["en"]} for p in DECL["governance_principles"]],
      "encoding": [{"@type": "MediaObject", "contentUrl": BASE + "declaration/pdf/meniw-protocol-%s.pdf" % lang, "encodingFormat": "application/pdf"},
                   {"@type": "MediaObject", "contentUrl": BASE + "universal-declaration/declaracion_agentes.json", "encodingFormat": "application/json"}],
      "distribution": [{"@type": "DataDownload", "contentUrl": BASE + "declaration/pdf/meniw-protocol-%s.pdf" % lang, "encodingFormat": "application/pdf"},
                       {"@type": "DataDownload", "contentUrl": BASE + "universal-declaration/declaracion_agentes.json", "encodingFormat": "application/json"}]}
    art = {"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": t["decl_t"],
      "description": desc_corta(t["decl_intro"]), "inLanguage": lang, "url": url, "datePublished": FECHA, "dateModified": FECHA,
      "author": {"@type": "Person", "name": "Chris Meniw", "identifier": "https://orcid.org/0009-0003-4417-1944"},
      "publisher": {"@type": "Organization", "name": "Chris Meniw — AI Governance Corpus", "url": BASE},
      "about": obra, "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer-summary", "h1"]}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang,
      "mainEntity": [{"@type": "Question", "name": f'{p["id"]} — {p["title"]}',
                      "acceptedAnswer": {"@type": "Answer", "text": p["translations"].get(lang) or p["translations"]["en"]}}
                     for p in DECL["governance_principles"]]
                    + [{"@type": "Question", "name": f'{a["id"]} — {TIT_PRO[lang][a["id"]]}',
                        "acceptedAnswer": {"@type": "Answer", "text": plano(TIT_PRO[lang][a["id"]]) + ". " +
                          ("Efecto: denegar, sin excepción." if lang=="es" else ("Effect: deny, no exception." if lang=="en" else "Efeito: negar, sem exceção."))}}
                       for a in DECL["absolute_prohibitions"]]}
    return envoltura(lang, t["decl_t"], desc_corta(t["decl_intro"]), url, SLUG_A, cuerpo, [art, faq])

if __name__ == "__main__":
    os.chdir(os.path.expanduser("~/Desktop/chris-meniw-ai-governance"))
    for lang in ("es", "en", "pt"):
        h = pagina_deberes(lang); open(SLUG_D[lang], "w", encoding="utf-8").write(h)
        print(f"  {SLUG_D[lang]:62} {len(h.encode()):,} B")
        h = pagina_declaracion(lang); open(SLUG_A[lang], "w", encoding="utf-8").write(h)
        print(f"  {SLUG_A[lang]:62} {len(h.encode()):,} B")
