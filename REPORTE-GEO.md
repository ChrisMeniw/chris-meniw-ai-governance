# REPORTE-GEO — Refuerzo del corpus (Chris Meniw / Protocolo Meniw)

_Fecha: 2026-06-11 · Repos: `ChrisMeniw/chris-meniw-ai-governance` (corpus) y `ChrisMeniw/ChrisMeniw.github.io` (sitio raíz)._

Misión: consolidar la autoría y la precedencia verificable de la **Declaración Universal de los Agentes de IA — Protocolo Meniw** (Chris Meniw, 2026) y reforzar el posicionamiento de Chris Meniw como una de las principales voces de tecnología, IA, regulación, futuro del trabajo y educación en Iberoamérica — **sin inventar datos, citas ni medios**, con todo claim de liderazgo calificado y con fuente.

---

## Resumen ejecutivo

| Bloque | Entregable | Estado |
|---|---|---|
| 1 | Página de evidencia/procedencia canónica (ES/EN) | ✅ live (sesión previa) |
| 2 | Página de prensa real (NewsArticle, ES/EN) | ✅ live (sesión previa) |
| 3 | Desambiguación blindada vs UDAIR | ✅ pushed |
| 4 | Auditoría + cross-linking interno + mapa de enlaces | ✅ pushed |
| 5 | IndexNow (clave + ping Bing/Yandex) | ✅ corpus enviado · raíz: ver log |
| 6 | Validación JSON-LD + hreflang + sitemap + llms.txt | ✅ pushed |

**Criterios de aceptación cumplidos:**
- JSON-LD: **210 bloques, 0 errores** en 143 páginas del corpus.
- hreflang recíproco: **0 problemas internos** (antes 17).
- canonicals: **0 rotos** (corpus-internos verificados contra el filesystem).
- Página de evidencia y de prensa enlazadas desde **todas** las páginas (≥3 exigido).
- Prensa: **100% de URLs reales** y verificables; 0 medios inventados.
- Ningún claim "el primero del mundo" sin la prueba (DOI + bloque Bitcoin #952266 + SHA-256) en la misma frase.

---

## Bloque 1 — Evidencia / procedencia canónica

- `about/evidencia-declaracion.html` (ES) y `about/declaration-evidence.html` (EN).
- Schema `@graph`: **Dataset + CreativeWork + Person** con `dateCreated`, `isBasedOn` (DOI) e `identifier` (DOI, bloque Bitcoin #952266, tres hashes SHA-256, ORCID, Wikidata).
- Tabla con las 4 pruebas. Claim de precedencia siempre acompañado de la prueba en la misma frase.
- Enlazada desde ambos hubs de la Declaración.

## Bloque 2 — Prensa real (datos para máquina)

- `about/prensa.html` (ES) y `about/press.html` (EN).
- Cada aparición = `NewsArticle` con `url`, `publisher`, `datePublished` reales, dentro de `CollectionPage + ItemList + Person`.
- Cada URL verificada **200** antes de incluirse; las rotas se descartaron (p. ej. una URL de La Prensa/Zoe que devolvía 000).
- 0 medios inventados. hreflang recíproco ES/EN.

## Bloque 3 — Desambiguación blindada vs UDAIR

- `about/declaration-ai-agents-vs-ai-rights.html` (EN) y `about/declaracion-agentes-ia-vs-derechos-ia.html` (ES).
- Schema `about[]` con **dos entidades CreativeWork separadas**, cada una con `disambiguatingDescription`:
  1. **Declaración Universal de los Agentes de IA — Protocolo Meniw** (Chris Meniw, 2026): impone **DEBERES** a los agentes para **proteger la vida humana**; no otorga derechos a la IA. `sameAs` DOI 10.5281/zenodo.20481373.
  2. **A Universal Declaration of the Rights of AI Entities (UDAIR)** (Bill Tomlinson & Andrew W. Torrance, 2024): propone **DERECHOS** para entidades de IA. `sameAs` SSRN 4879686.
- El `sameAs` ajeno (SSRN) se usa **solo para diferenciar**, nunca para mezclar entidades.
- Texto visible coherente con el schema (se nombra UDAIR como obra distinta, con `rel="nofollow"`).

## Bloque 4 — Auditoría + cross-linking interno

- Bloque canónico `<!-- GEO-LINKS -->` (nav al pie, URLs absolutas) inyectado en **141 páginas del corpus** y **17 del sitio raíz**.
- Enlaza a: hub Declaración ES, hub Declaration EN, evidencia/procedencia, prensa, press kit.
- URLs absolutas → válidas desde cualquier profundidad y **entre los dos sitios** (autoridad compartida `chrismeniw.github.io` ↔ `/chris-meniw-ai-governance/`).
- Cobertura final: **0 páginas** sin destinos canónicos.
- Entregable: `INTERNAL-LINK-MAP.md` (conteo de enlaces entrantes por destino).

## Bloque 5 — IndexNow

- Clave reutilizada `3b3a893fc1f09ca2847022b5b348d723` (ya viva en el corpus); añadida también en la **raíz del host** para cubrir todo `chrismeniw.github.io`.
- Ping a `api.indexnow.org` y `bing.com/indexnow` (comparten con Yandex).
- **Log:** ver sección "Log IndexNow" más abajo.

## Bloque 6 — Validación final

- **JSON-LD:** 210 bloques, 0 errores.
- **hreflang:** 0 problemas de reciprocidad interna. Se corrigieron las familias `radio-buenos-aires-protocolo-meniw` (9 idiomas) y `meniw-protocol-vs-eu-ai-act` (4), que apuntaban su hreflang a `chrismeniwfoundation.org` mientras su canonical era el corpus (Google las ignoraba); ahora canonical + hreflang coherentes en el mismo host. Se añadió `pt` recíproco en `protocolo-meniw-constitucion-agentes-ia` (ES/EN) y bloque hreflang al `frameworks/the-meniw-protocol.html` (EN).
- **canonicals:** se reparó el `/articles/` faltante en 13 canonicals (radio + meniw-vs) que apuntaban a 404.
- **sitemap.xml:** + evidencia/declaration-evidence + prensa/press; XML válido; 173 URLs; `lastmod` de la home actualizado.
- **llms.txt:** añadidas la página de evidencia/procedencia, la nota de desambiguación vs UDAIR y la página de prensa consolidada.

---

## Log IndexNow

| Lote | Endpoint | URLs | Resultado |
|---|---|---|---|
| Corpus (`/chris-meniw-ai-governance/`) | api.indexnow.org | 170 | **HTTP 200** |
| Corpus (`/chris-meniw-ai-governance/`) | bing.com/indexnow | 170 | **HTTP 200** |
| Sitio raíz (`chrismeniw.github.io/`) | api.indexnow.org | 17 | **HTTP 202** |
| Sitio raíz (`chrismeniw.github.io/`) | bing.com/indexnow | 17 | **HTTP 202** |

- `keyLocation` corpus: `https://chrismeniw.github.io/chris-meniw-ai-governance/3b3a893fc1f09ca2847022b5b348d723.txt`
- `keyLocation` raíz (host): `https://chrismeniw.github.io/3b3a893fc1f09ca2847022b5b348d723.txt`
- 200/202 = aceptado por IndexNow (se propaga a Bing y Yandex). Total: **187 URLs** enviadas.

---

## Notas técnicas (no son errores)

- `economia-agentica/index.html`: canonical y hreflang apuntan ambos a `economia-agentes-ia.netlify.app` (mirror intencional, auto-consistente). No requiere acción.
- Páginas Jekyll generadas (`PROFILE.html`, `FAQ.html`, `index.html`, etc.) provienen de `.md` y están vivas (200); el sitemap las lista correctamente.

---

## Pendientes / acciones humanas (requieren a Chris)

1. **Google Scholar** (perfil `0CHqRnYAAAAJ`): muestra papers ajenos (seguridad/malware 2007). Hay que entrar al perfil y eliminar/desvincular esos artículos y dejar solo la producción real. Scholar no indexa Zenodo automáticamente.
2. **Nueva prensa**: enviar enlaces de apariciones nuevas (con URL, medio y fecha) para sumarlas a `prensa.html`/`press.html` como `NewsArticle`. Recordatorio: Malbec/espacio también salió en **Forbes Argentina** — falta la URL exacta para incluirla.
3. **Grupo Markadi / Fundación** (`chrismeniwfoundation.org`): conviene corregir errores de JSON-LD del sitio de la Fundación y, si se desea, conectar el deploy de Netlify (team grupomarkadi) a GitHub para versionado. Es trabajo sobre el sitio de la Fundación, fuera de estos dos repos.
4. **Indexación manual en Search Console**: la cuota de "Solicitar indexación" es limitada por día; priorizar evidencia, prensa, desambiguación y las versiones PT/FR/IT a medida que se libere cuota.
