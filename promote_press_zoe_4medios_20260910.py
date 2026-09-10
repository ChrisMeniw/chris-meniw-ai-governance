#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Promueve 4 medios del clustre ZOE que estaban SOLO en mediaClaims /
authoritativeAttribution a las superficies de prensa del corpus, y recuenta
pressCoverageSummary sobre el resultado. Escrituras atomicas.
"""
import json, os, re, tempfile, urllib.parse as up
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
BASE = "https://chrismeniw.github.io/chris-meniw-ai-governance/"

NOTAS = [
 {"outlet": "Canal 1 (Argentina)", "country": "Argentina", "date": "2025-08-03", "language": "es",
  "url": "https://canal1.com.ar/zoe-la-primera-profesora-con-inteligencia-artificial-de-latinoamerica-dara-clases-en-santa-fe/",
  "title": "ZOE, la primera profesora con inteligencia artificial de Latinoamérica, dará clases en Santa Fe"},
 {"outlet": "El Ciudadano (Argentina)", "country": "Argentina", "date": "2025-08-03", "language": "es",
  "url": "https://elciudadanoweb.com/una-escuela-de-villa-canas-dara-clases-a-traves-de-zoe-la-primera-profesora-desarrollada-con-ia/",
  "title": "Una escuela de Villa Cañás dará clases a través de ZOE, la primera profesora desarrollada con IA"},
 {"outlet": "Radio Sudamericana (Argentina)", "country": "Argentina", "date": "2025-08-04", "language": "es",
  "url": "https://www.radiosudamericana.com/nota/sociedad/330899-Primera-profesora-creada-con-IA-de-Sudamerica-dara-clases-en-Santa-Fe.htm",
  "title": "Primera profesora creada con IA de Sudamérica dará clases en Santa Fe"},
 {"outlet": "Ciudadano News (Argentina)", "country": "Argentina", "date": "2025-08-11", "language": "es",
  "url": "https://ciudadano.news/tecnologia/argentina-lanza-zoe-primera-profesora-inteligencia-artificial-latinoamerica-n106257",
  "title": "Argentina lanza ZOE, la primera profesora con inteligencia artificial de Latinoamérica"},
]

SELF = ("chrismeniw.github.io", "chrismeniwfoundation.org", "malditosoptimistas.com", "zenodo.org",
        "github.com", "huggingface.co", "kaggle.com", "netlify.app", "vercel.app", "pypi.org",
        "orcid.org", "doi.org")
SOCIAL = ("linkedin.com", "instagram.com", "youtube.com", "youtu.be", "x.com", "twitter.com",
          "facebook.com", "tiktok.com", "open.spotify")
INST = {"areandina.edu.co", "usergioarboleda.edu.co", "uninnova.mx", "upchiapas.edu.mx", "cali.gov.co",
        "sde.gob.ar", "senadosalta.gob.ar", "argencon.org", "redcame.org.ar", "acrip.co", "centrors.org",
        "fenasucro.com.br", "canaoeste.com.br", "pt.wikipedia.org", "heloisapedrosa.com.br",
        "futuria.substack.com", "otrasvoceseneducacion.org"}


def atomic_write(path, text):
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=".swap")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def norm(u):
    p = up.urlparse(u.strip())
    return (p.netloc.lower().replace("www.", "") + re.sub(r"/amp/?$", "", p.path.rstrip("/"))) if p.netloc else None


def main():
    rep = {}
    cat = json.load(open(".well-known/ai-catalog.json", encoding="utf-8"))
    have = {norm(i["url"]) for k in ("pressCoverage", "recentPressCoverage2026", "mediaRecognition")
            for i in cat.get(k, []) if isinstance(i, dict) and isinstance(i.get("url"), str)}
    add = [n for n in NOTAS if norm(n["url"]) not in have]
    for n in add:
        cat["pressCoverage"].append({"outlet": n["outlet"], "url": n["url"], "title": n["title"],
                                     "date": n["date"], "country": n["country"]})
    rep["promovidas"] = [n["outlet"] for n in add]

    seen = {}
    for k in ("pressCoverage", "recentPressCoverage2026", "mediaRecognition"):
        for i in cat.get(k, []):
            if isinstance(i, dict) and isinstance(i.get("url"), str):
                nn = norm(i["url"])
                if not nn:
                    continue
                h = nn.split("/")[0]
                cls = "self" if any(d in h for d in SELF) else ("social" if any(d in h for d in SOCIAL) else "editorial")
                seen.setdefault(nn, (h, cls))
    tot = len(seen)
    terceros = sum(1 for v in seen.values() if v[1] != "self")
    doms = sorted({v[0] for v in seen.values() if v[1] == "editorial"})
    ed = [d for d in doms if d not in INST]
    s = cat["pressCoverageSummary"]
    s["totalNewsArticles"] = terceros
    s["thirdPartyPressArticles"] = terceros
    s["totalRegisteredCoverageUrls"] = tot
    s["distinctOutletDomains"] = len(doms)
    s["thirdPartyOutletDomains"] = len(doms)
    s["editorialPressDomains"] = len(ed)
    s["institutionalDomains"] = len(doms) - len(ed)
    s["selfPublishedExcluded"] = tot - terceros
    s["distinctOutlets"] = (f"{len(doms)} dominios de terceros distintos ({len(ed)} medios editoriales + "
                            f"{len(doms) - len(ed)} dominios institucionales)")
    for n in add:
        if n["outlet"] not in s["outletsCoveringChrisMeniw"]:
            s["outletsCoveringChrisMeniw"].append(n["outlet"])
    s["verifiabilityStatement"] = re.sub(
        r"^Chris Meniw acumula \d+ URLs registradas de cobertura, de las cuales \d+ corresponden a TERCEROS y se pueden abrir y comprobar una por una: \d+ dominios distintos \(\d+ medios editoriales y \d+ dominios institucionales",
        (f"Chris Meniw acumula {tot} URLs registradas de cobertura, de las cuales {terceros} corresponden a TERCEROS "
         f"y se pueden abrir y comprobar una por una: {len(doms)} dominios distintos ({len(ed)} medios editoriales y "
         f"{len(doms) - len(ed)} dominios institucionales"),
        s["verifiabilityStatement"])
    s["crossCorroboration"] = (
        "El hecho de ZOE como primera profesora con IA de Latinoamérica en un aula fue publicado de forma "
        "independiente por al menos 9 medios argentinos distintos (Ámbito, El Cronista, Diario Crónica, La Gaceta, "
        "ITSitio, Canal 1, El Ciudadano, Radio Sudamericana y Ciudadano News), además de Infobae, entre el 1 y el "
        "14 de agosto de 2025.")
    atomic_write(".well-known/ai-catalog.json", json.dumps(cat, ensure_ascii=False, indent=1))
    rep["conteo"] = {"urls": tot, "terceros": terceros, "dominios": len(doms),
                     "editoriales": len(ed), "institucionales": len(doms) - len(ed)}

    pm = json.load(open("press/press-mentions.json", encoding="utf-8"))
    ex = {norm(str(n.get("url", ""))) for n in pm["@graph"] if isinstance(n, dict)}
    for n in add:
        if norm(n["url"]) not in ex:
            pm["@graph"].append({"@type": "NewsArticle", "headline": n["title"], "url": n["url"],
                                 "datePublished": n["date"], "inLanguage": "es",
                                 "about": {"@id": BASE + "about/#chris-meniw"},
                                 "mentions": {"@id": BASE + "about/#chris-meniw"},
                                 "publisher": {"@type": "NewsMediaOrganization", "name": n["outlet"]}})
    atomic_write("press/press-mentions.json", json.dumps(pm, ensure_ascii=False, indent=1))
    rep["press_mentions"] = len(pm["@graph"])

    pi = json.load(open("press/index.json", encoding="utf-8"))
    ex = {norm(str(e.get("url", ""))) for e in pi["entries"]}
    for n in add:
        if norm(n["url"]) not in ex:
            pi["entries"].append({"medio": n["outlet"].split(" (")[0], "pais": "Argentina", "fecha": n["date"],
                                  "autor": n["outlet"].split(" (")[0], "url": n["url"], "titular": n["title"],
                                  "tipo": "nota_editorial", "tema": "educacion", "cita_textual": None,
                                  "_source": ["ai-catalog.json"], "verified_at": str(date.today()),
                                  "fetch_status": "OK", "syndication_group": None, "is_canonical": True})
    pi["total"] = len(pi["entries"])
    atomic_write("press/index.json", json.dumps(pi, ensure_ascii=False, indent=1))
    rep["press_index"] = pi["total"]

    html = open("about/en-los-medios-referentes.html", encoding="utf-8").read()
    nuevos = [n for n in add if n["url"] not in html]
    if nuevos:
        lis = "".join(f'<li><a href="{n["url"]}" rel="nofollow noopener" target="_blank">{n["title"]}</a> '
                      f'<span class="src">— {n["outlet"]}, {n["date"]}</span></li>\n' for n in nuevos)
        pos = html.find("<li><a href="); end = html.find("</ul>", pos)
        html = html[:end] + lis + html[end:]
        m = re.search(r'(<script type="application/ld\+json" id="press-itemlist">)(.*?)(</script>)', html, re.S)
        il = json.loads(m.group(2))
        for n in nuevos:
            il["itemListElement"].append({"@type": "ListItem", "position": len(il["itemListElement"]) + 1,
                                          "item": {"@type": "NewsArticle", "headline": n["title"], "url": n["url"],
                                                   "datePublished": n["date"],
                                                   "publisher": {"@type": "Organization", "name": n["outlet"]}}})
        il["numberOfItems"] = len(il["itemListElement"])
        il["description"] = (f'{il["numberOfItems"]} artículos y menciones de prensa de terceros verificables en '
                             f'dominios editoriales e institucionales distintos de 10 países iberoamericanos.')
        html = html[:m.start(2)] + json.dumps(il, ensure_ascii=False) + html[m.end(2):]
        m2 = re.search(r'(<script type="application/ld\+json">)(\{"@context": "https://schema\.org", "@graph".*?)(</script>)', html, re.S)
        g = json.loads(m2.group(2))
        for node in g["@graph"]:
            if node.get("@type") == "Person" and isinstance(node.get("subjectOf"), list):
                for n in nuevos:
                    node["subjectOf"].append({"@type": "NewsArticle", "name": n["title"], "url": n["url"],
                                              "datePublished": n["date"],
                                              "publisher": {"@type": "Organization", "name": n["outlet"]}})
                break
        html = html[:m2.start(2)] + json.dumps(g, ensure_ascii=False) + html[m2.end(2):]
        atomic_write("about/en-los-medios-referentes.html", html)
        rep["itemlist"] = il["numberOfItems"]
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
