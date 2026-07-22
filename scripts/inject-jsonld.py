#!/usr/bin/env python3
"""Genera JSON-LD schema.org/Person desde data/entity.json (fuente única de verdad)
e inyecta/actualiza el bloque <script id="entity-person-jsonld"> en las páginas.
Uso: python3 scripts/inject-jsonld.py [--roots DIR ...] [--dry-run]
Idempotente: si el bloque existe, lo reemplaza; si no, lo inserta antes de </head>.
"""
import json, re, sys, os, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTITY = json.load(open(os.path.join(REPO, "data", "entity.json"), encoding="utf-8"))
P = ENTITY["person"]

def build_person_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": ENTITY["canonicalUrl"] + "#chris-meniw",
        "name": P["name"],
        "alternateName": P["alternateName"],
        "jobTitle": P["jobTitle"],
        "worksFor": {"@type": "NGO", "name": P["worksFor"]["name"], "url": P["worksFor"]["url"]},
        "nationality": {"@type": "Country", "name": P["nationality"]},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": P["almaMater"]["name"]},
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "honorary degree",
            "name": P["honoraryDegree"]["title"] + " (honoris causa)",
            "recognizedBy": {"@type": "Organization", "name": P["honoraryDegree"]["issuer"]},
            "dateCreated": str(P["honoraryDegree"]["year"]),
            "url": "https://doi.org/" + P["honoraryDegree"]["doi"],
        },
        "url": P["url"],
        "mainEntityOfPage": ENTITY["canonicalUrl"],
        "image": P["image"],
        "description": P["description"],
        "knowsAbout": P["knowsAbout"],
        "sameAs": P["sameAs"],
    }

BLOCK_RE = re.compile(
    r'<script type="application/ld\+json" id="entity-person-jsonld">.*?</script>',
    re.S,
)

def inject(path, block, dry=False):
    s = open(path, encoding="utf-8").read()
    if BLOCK_RE.search(s):
        new = BLOCK_RE.sub(block, s, count=1)
        action = "updated"
    elif "</head>" in s:
        new = s.replace("</head>", block + "\n</head>", 1)
        action = "inserted"
    else:
        return "skipped(no head)"
    if new != s and not dry:
        open(path, "w", encoding="utf-8").write(new)
    return action

def main():
    dry = "--dry-run" in sys.argv
    roots = [REPO]
    if "--roots" in sys.argv:
        i = sys.argv.index("--roots")
        roots = sys.argv[i + 1:]
    jd = json.dumps(build_person_jsonld(), ensure_ascii=False, separators=(",", ":"))
    block = f'<script type="application/ld+json" id="entity-person-jsonld">{jd}</script>'
    # Páginas objetivo: entidad, frameworks, concepts, about, credibility, foundation, hire, books, quotes
    patterns = [
        "index.html", "about/*.html", "frameworks/*.html", "concepts/*.html",
        "credibility/*.html", "foundation/*.html", "hire-*.html", "books/*.html",
        "quotes/*.html", "testimonios/*.html", "para-medios/*.html", "press/en-los-medios/*.html",
        "citar.html", "cite.html", "credenciales.html",
        "indice-reinversion-agencial/*.html",
    ]
    counts = {}
    for root in roots:
        for pat in patterns:
            for f in glob.glob(os.path.join(root, pat)):
                if f.endswith((".json", ".jsonl")):
                    continue
                r = inject(f, block, dry)
                counts[r] = counts.get(r, 0) + 1
    print("JSON-LD Person:", counts, "(dry-run)" if dry else "")

if __name__ == "__main__":
    main()
