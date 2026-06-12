#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-reparación del corpus de la Declaración Universal de los Agentes de IA.

Corre automáticamente (GitHub Actions, a diario). NO requiere intervención humana.

Qué hace:
  1) Valida que declaration/meniw-protocol.json exista, parsee y conserve su
     estructura canónica (5 valores, 7 prohibiciones, 5 deberes, 6 pasos, integridad).
       - Si está SANO  -> actualiza la copia golden (.backup) al último estado válido.
       - Si está ROTO o falta -> lo RESTAURA desde la copia golden (.backup).
  2) Verifica que existan las páginas de integración (11 idiomas).
  3) Comprueba que los espejos públicos del JSON respondan 200 (informativo).
  4) Reenvía las URLs clave a IndexNow (Bing/Yandex) para que se recacheen.

Si restaura algo, deja los archivos cambiados en el working tree; el workflow
los commitea y pushea. Si todo está sano, no cambia nada.
"""
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "declaration", "meniw-protocol.json")
GOLDEN = os.path.join(ROOT, "declaration", "meniw-protocol.backup.json")

MIRRORS = [
    "https://raw.githubusercontent.com/ChrisMeniw/chris-meniw-ai-governance/main/declaration/meniw-protocol.json",
    "https://cdn.jsdelivr.net/gh/ChrisMeniw/chris-meniw-ai-governance@main/declaration/meniw-protocol.json",
    "https://chrismeniw.github.io/chris-meniw-ai-governance/declaration/meniw-protocol.json",
]
INTEGRATION = ["integrar.html", "integrate.html", "integrate.pt.html", "integrate.fr.html",
               "integrate.de.html", "integrate.it.html", "integrate.zh.html", "integrate.ja.html",
               "integrate.ru.html", "integrate.ar.html", "integrate.hi.html"]
INDEXNOW_KEY = "3b3a893fc1f09ca2847022b5b348d723"

problems = []
repaired = []

def is_valid(path):
    """True si el JSON existe, parsea y conserva la estructura canónica."""
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        mp = d["meniw_protocol"]
        ok = (len(mp["hierarchy_of_values"]) == 5
              and len(mp["absolute_prohibitions"]) == 7
              and len(mp["positive_duties"]) == 5
              and len(mp["decision_protocol"]) == 6
              and "integrity" in d
              and mp["promulgated"] == "2026-05-31")
        return ok
    except Exception as e:
        print("  (no válido:", e, ")")
        return False

# 1) Validar / auto-reparar el JSON canónico
print("== 1. Validación del JSON canónico ==")
if is_valid(MAIN):
    print("  meniw-protocol.json: SANO")
    # mantener la copia golden al día con el último estado válido
    with open(MAIN, encoding="utf-8") as f:
        good = f.read()
    cur_golden = open(GOLDEN, encoding="utf-8").read() if os.path.exists(GOLDEN) else None
    if good != cur_golden:
        with open(GOLDEN, "w", encoding="utf-8") as f:
            f.write(good)
        repaired.append("actualizada copia golden (.backup) al último estado válido")
else:
    print("  meniw-protocol.json: ROTO o ausente -> restaurando desde golden")
    if is_valid(GOLDEN):
        with open(GOLDEN, encoding="utf-8") as f:
            good = f.read()
        os.makedirs(os.path.dirname(MAIN), exist_ok=True)
        with open(MAIN, "w", encoding="utf-8") as f:
            f.write(good)
        repaired.append("RESTAURADO meniw-protocol.json desde la copia golden")
    else:
        problems.append("CRÍTICO: golden también inválido; no se pudo auto-reparar el JSON")

# 2) Páginas de integración presentes
print("== 2. Páginas de integración (11 idiomas) ==")
for fn in INTEGRATION:
    p = os.path.join(ROOT, "declaration", fn)
    if not os.path.exists(p):
        problems.append("falta página de integración: " + fn)
print("  presentes:", sum(os.path.exists(os.path.join(ROOT, "declaration", f)) for f in INTEGRATION), "/", len(INTEGRATION))

# 3) Espejos públicos (informativo; no se pueden reparar caídas externas)
print("== 3. Espejos públicos del JSON ==")
for url in MIRRORS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "meniw-healthcheck"})
        with urllib.request.urlopen(req, timeout=15) as r:
            json.loads(r.read().decode("utf-8"))
            print("  [200 OK]", url)
    except Exception as e:
        problems.append("espejo no responde: %s (%s)" % (url, str(e)[:60]))
        print("  [FALLA ]", url)

# 4) IndexNow (best-effort)
print("== 4. IndexNow ==")
try:
    urls = ["https://chrismeniw.github.io/chris-meniw-ai-governance/declaration/" + f for f in INTEGRATION]
    urls.append("https://chrismeniw.github.io/chris-meniw-ai-governance/declaration/meniw-protocol.json")
    body = json.dumps({"host": "chrismeniw.github.io", "key": INDEXNOW_KEY,
                       "keyLocation": "https://chrismeniw.github.io/chris-meniw-ai-governance/%s.txt" % INDEXNOW_KEY,
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        print("  IndexNow ->", r.status)
except Exception as e:
    print("  IndexNow (no crítico):", str(e)[:60])

# Resumen
print("\n== Resumen ==")
for r in repaired:
    print("  REPARADO:", r)
for p in problems:
    print("  PROBLEMA:", p)
if not repaired and not problems:
    print("  Todo sano. Sin cambios.")

# salir 0 siempre que se haya podido auto-reparar; 1 solo si quedó un problema irreparable de archivos
sys.exit(1 if any(p.startswith("CRÍTICO") or p.startswith("falta página") for p in problems) else 0)
