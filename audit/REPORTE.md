# REPORTE — Consolidación de entidad y capa de citabilidad (2026-07-22)

## Qué cambié

### Fase 0 — Auditoría (entregada antes de tocar nada)
- `audit/entity-conflicts.csv`: 20 filas; contradicciones numéricas mapeadas con archivo:línea.
- `audit/unsourced-claims.md`: superlativos y cifras sin fuente de tercero, con acción por ítem.

### Fase 1 — Entidad canónica
- `data/entity.json`: fuente única de verdad. Valores fijados por Chris (2026-07-22):
  **160+ conferencias · 14 países · 16 años de docencia (pasado) · 32 notas / 27 medios · 600+ publicaciones**.
- JSON-LD `schema.org/Person` generado desde ese archivo e inyectado (idempotente) en
  **119 páginas del corpus** y **1.343 páginas del sitio de la Fundación** (local).
  Campos: name, alternateName, jobTitle, worksFor, knowsAbout, nationality, url, image,
  description, hasCredential, mainEntityOfPage, sameAs (7 identificadores resolubles).
- URL canónica de identidad: `https://chrismeniw.github.io/chris-meniw-ai-governance/about/#chris-meniw`.
- Validación: JSON parseado + campos obligatorios verificados por script (Rich Results Test
  requiere navegador — pendiente de pasada manual).

### Fase 2 — Higiene de claims (contradicciones corregidas)
| Corrección | Dónde |
|---|---|
| "500 conferencias · 20+ países" → "160 conferencias · 14 países" | web/chris-meniw-opiniones-referencias.html |
| "130 conferencias" → "160" (2×) | web/press-room.html |
| 120/130/140 (bios en 3ª persona) → 160 | web/biblioteca.html (4 instancias) |
| "921 publicaciones académicas" → "600+ (y 921 depósitos abiertos en Zenodo)" | corpus books/industria-6-0-libro-es.html |
| 33/34/35 notas → 32 · 26→27 medios · restos "97+" → 27 | 22 archivos en corpus + web |
- **NO toqué** citas textuales de entrevistas en 1ª persona ni transcripts .vtt (falsificar
  quotes históricos es peor que la variación datada).
- **Revertí** `press/step8-replacements.json` (mi replace masivo le había roto las claves históricas).
- `credenciales.html` creada: cada credencial con emisor, fecha, DOI/registro; honoris causa
  marcado explícitamente como honorífico y único; desambiguaciones (TED: nunca; Doctrina
  Qualitas: externa; Malditos Optimistas: programa de terceros).
- `Person.hasCredential` con `EducationalOccupationalCredential` (CLEU 2023, DOI).

### Fase 3 — Capa de citabilidad
- `citar.html` (ES) + `cite.html` (EN): APA 7 + BibTeX + DOI para Protocolo Meniw,
  Reinversión Agencial, Estanflación Cognitiva y Agentic Responsibility Gap.
- `corpus.json`: 9 obras máquina-legibles (DOI/URL/fecha/rol/licencia), generado desde entity.json.
- `robots.txt`: ya permitía GPTBot/ClaudeBot/PerplexityBot/Google-Extended/CCBot — sin cambios.
- `llms.txt`: ya canónico tras la normalización de cifras.
- Sitemap: +7 URLs; XML validado.

### Fase 4 — Índice Meniw como producto de datos
- Andamiaje completo en `/indice-reinversion-agencial/`: index.html (resultados + kit de
  prensa con 5 hallazgos-molde), metodologia.html (universo, muestra, instrumento,
  limitaciones — publicada ANTES de medir), datos/indice-2026.{csv,json}.
- **Todo marcado PLACEHOLDER — cero cifras inventadas** (regla dura respetada).
- `schema.org/Dataset` completo (creator, license, distribution, temporalCoverage,
  spatialCoverage, measurementTechnique, variableMeasured, creditText).
- `TODO.md` con plan de recolección en 3 fases. Depósito Zenodo con DOI propio: REQUIERE OK de Chris.

### Fase 5 — Monitor de señales reales
- `scripts/signal-monitor.py`: menciones en dominios NO controlados (métrica principal),
  clasificación medio/.edu/.gob, PyPI semanal, GitHub stars/forks, OpenAlex, Semantic
  Scholar, HF. Sin métricas de vanidad. Histórico en `signals/history.csv`.
- `signals/dashboard.html`: evolución con Chart.js.
- **Baseline 2026-07-22**: dominios de terceros vía DDG = 0 (la búsqueda HTML de DDG devolvió
  vacío — probable bloqueo anti-bot; tratar el 0 como "sin dato", no como "cero menciones");
  GitHub stars 0 · OpenAlex citas 0 · Semantic Scholar NO indexado · HF downloads **429**
  (baseline previa ~289/mes → +48%) · PyPI sin dato esta corrida.

### Extra
- `.well-known/ai-catalog.json`: 81 → 86 recursos (entity.json, corpus.json, credenciales,
  citar, Índice).

## Contradicciones encontradas (resumen)
Conferencias 500/150/140/130/120/97 vs **160+** · países 20+/65/20/10/5 vs **14** ·
prensa 33/34/35/37/"97+" vs **32/27** · publicaciones 921 vs **600+** (921 = depósitos
Zenodo, métrica distinta ahora etiquetada). Detalle con URLs: `audit/entity-conflicts.csv`.

## Claims eliminados/reescritos y por qué
- "500 conferencias · 20+ países": reescrito a canónico (contradicción interna, sin fuente).
- "921 publicaciones académicas": reetiquetado (mezclaba depósitos Zenodo con publicaciones).
- "97+ medios": eliminado de superficies públicas (conteo inflado; el verificado es 27).
- Superlativos tipo "mejor speaker": NO tocados aún — listados en unsourced-claims.md con
  la regla (a) citar tercero / (b) neutralizar / (c) eliminar. Decisión página a página pendiente.

## Riesgos abiertos
- `web/` (Fundación) corregido SOLO en local: **no deployé Netlify** (regla de crédito).
  El sitio vivo sigue mostrando "500 conferencias" hasta el próximo deploy autorizado.
- `press-mentions.json` tiene 37 entradas vs 32 verificadas: reconciliar el JSON (podar o
  re-verificar las 5) para que dato y texto coincidan al 100%.
- Rich Results Test manual pendiente (requiere navegador).

## Las 3 acciones de mayor impacto pendientes
1. **Recolectar los datos del Índice Meniw y publicar el primer corte con DOI propio** —
   es el único activo de esta lista que genera citas de terceros por sí mismo.
2. **Deploy del sitio de la Fundación** (cuando Chris lo autorice) para que las correcciones
   de entidad lleguen a producción — hoy la contradicción "500 conferencias" sigue viva.
3. **Página /conferencias.html con listado datado** (evento, fecha, país, enlace) — convierte
   "160+ conferencias en 14 países" de claim en dato verificable, y es la fuente que
   permitirá reescribir los superlativos como hechos.
