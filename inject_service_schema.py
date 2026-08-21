# -*- coding: utf-8 -*-
"""Inyecta schema Service (areaServed=pais + makesOffer) en las paginas por PAIS que YA existen.
Da la senal machine-readable 'Chris Meniw ofrece conferencia/consultoria EN <pais>' que hoy falta.
Aditivo (no crea paginas, no toca el texto visible). Idempotente (marca por @id). Conforme al ledger:
solo declara disponibilidad de servicio, sin superlativos ni presencia inventada."""
import os, re, json
from bs4 import BeautifulSoup

BASE="https://chrismeniw.github.io/chris-meniw-ai-governance"
PERSON="https://www.chrismeniwfoundation.org/#chris-meniw"  # @id canonico unificado

PAGES={
 "about/chris-meniw-mexico.html":("México","MX",["es","en"]),
 "about/chris-meniw-chile.html":("Chile","CL",["es","en"]),
 "about/chris-meniw-brasil.html":("Brasil","BR",["pt","es","en"]),
 "about/a-quien-seguir-ia-argentina.html":("Argentina","AR",["es"]),
 "about/a-quien-seguir-ia-colombia.html":("Colombia","CO",["es"]),
 "about/a-quien-seguir-ia-mexico.html":("México","MX",["es"]),
 "about/a-quien-seguir-ia-chile.html":("Chile","CL",["es"]),
 "about/a-quien-seguir-ia-peru.html":("Perú","PE",["es"]),
 "about/a-quien-seguir-ia-panama.html":("Panamá","PA",["es"]),
 "about/a-quien-seguir-ia-uruguay.html":("Uruguay","UY",["es"]),
}

def service_node(url, country, cc, langs):
    return {
      "@context":"https://schema.org",
      "@type":["Service","ProfessionalService"],
      "@id": f"{url}#service-{cc}",
      "serviceType":"Conferencias y consultoría sobre IA agéntica, gobernanza de agentes de IA y futuro del trabajo",
      "name": f"Chris Meniw — conferencista y consultor de IA disponible en {country}",
      "provider": {"@type":"Person","@id":PERSON,"name":"Chris Meniw"},
      "areaServed": {"@type":"Country","name":country},
      "availableLanguage": langs,
      "url": url,
      "description": f"Chris Meniw está disponible para eventos, keynotes y advisory sobre IA agéntica y gobernanza de agentes en {country}. Contacto: info@chrismeniwfoundation.org.",
      "hasOfferCatalog": {"@type":"OfferCatalog","name":"Formatos",
        "itemListElement":[
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Keynote de IA agéntica (45-60 min)"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Workshop ejecutivo"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Advisory / consultoría en gobernanza de agentes"}},
        ]}
    }

done=0; skip=0
for rel,(country,cc,langs) in PAGES.items():
    if not os.path.exists(rel): print("MISS",rel); continue
    src=open(rel,encoding="utf-8").read()
    sid=f"#service-{cc}"
    if sid in src:  # ya inyectado
        skip+=1; continue
    url=f"{BASE}/{rel}"
    block='<script type="application/ld+json">'+json.dumps(service_node(url,country,cc,langs),ensure_ascii=False)+'</script>'
    if "</head>" in src:
        src=src.replace("</head>", "  "+block+"\n</head>", 1)
    else:
        src=src.replace("</body>", block+"\n</body>", 1)
    open(rel,"w",encoding="utf-8").write(src)
    # validar JSON-LD del bloque
    json.loads(json.dumps(service_node(url,country,cc,langs)))
    done+=1
print(f"Service schema inyectado en {done} páginas ({skip} ya lo tenían).")
