# Sala de prensa — Reporte de verificación
**Fecha de verificación:** 2026-07-22T18:13:35+00:00  
**Fuente:** `press/press-mentions.json` + `press/index.html` + `press/index-EN.html` + `press/en-los-medios/*.html`.  
**Reglas:** sin inferencia; ganan los datos de la página viva sobre los del archivo.

## Números reales (reemplazan a “33 notas / 97+ medios”)

- **Fuentes independientes tras deduplicación: 34** (de 36 entradas brutas; 2 duplicadas por sindicación).
- Verificadas HOY: **32 OK** · **1 CAMBIADA** · **1 ROTA**.
- Fuentes válidas HOY (200 + menciona a Meniw): **32**.
- Overwrites aplicados desde la página viva: 24 en 34 entradas.

## Estado por fetch

| Estado | Cuenta |
|---|---|
| OK | 32 |
| CAMBIADA | 1 |
| ROTA | 1 |
| **Total canonical** | **34** |

### ROTA

- `La Voz` — HTTP 403  
  https://www.lavoz.com.ar/tecnologia/zoe-la-primera-profesora-creada-con-ia-en-latinoamerica-dara-clases-en-santa-fe  *(no canonical — colapsada en syndication group)*
- `Medium` — HTTP 403  
  https://medium.com/p/510e395f7034

### CAMBIADA (200 pero ya no menciona “Meniw”)

- `El Español (España)` — titular actual vivo: “Zoe, la profesora creada con inteligencia artificial que imparte clase en Argentina”  
  https://www.elespanol.com/invertia/disruptores/america-tech/argentina/20250828/zoe-profesora-creada-inteligencia-artificial-imparte-clase-argentina/1003743882169_0.html

## Por medio (fuentes independientes)

| Medio | Notas |
|---|---|
| Diario Expreso (Ecuador) | 3 |
| Info del Estero | 2 |
| Infobae | 2 |
| La Prensa | 2 |
| Malditos Optimistas | 2 |
| Radio Buenos Aires | 2 |
| C5N | 1 |
| CNN en Español | 1 |
| Cadena 3 | 1 |
| Clarín | 1 |
| Diario Panorama | 1 |
| Economy (Bolivia) | 1 |
| El Español (España) | 1 |
| El Liberal | 1 |
| El Litoral | 1 |
| El Tiempo (Colombia) | 1 |
| El Tribuno | 1 |
| Forbes Argentina | 1 |
| LU5 AM | 1 |
| Medium | 1 |
| Nuevo Diario | 1 |
| Página 12 | 1 |
| Radio Nacional (Argentina) | 1 |
| Radio Nacional Argentina | 1 |
| Sobre Tiza | 1 |
| TN | 1 |
| Xataka | 1 |

## Por país (heurística por TLD — no está en los archivos)

_Este campo `pais` está null en `index.json` porque no aparece en los archivos fuente. Este cuadro se calcula desde el TLD sólo para reporte, no se persiste._

| País (TLD) | Notas |
|---|---|
| Argentina | 15 |
| sin dato | 14 |
| Ecuador | 3 |
| EE. UU. (edición LATAM) | 1 |
| Bolivia | 1 |

## Por año (desde `fecha` en archivo/live)

| Año | Notas |
|---|---|
| 08-0 | 1 |
| 2022 | 2 |
| 2023 | 1 |
| 2024 | 3 |
| 2025 | 14 |
| 2026 | 7 |
| sin  | 6 |

_(0 sin fecha — ni en el archivo ni en la página viva)_

## Por tipo / tema

Estos campos están **null en todas las entradas** — no existen en los archivos fuente y no se pueden completar sin inferir. Requeriría clasificación manual del titular por parte tuya.

## Sindication groups (deduplicación)

| Grupo | Miembros | Canonical |
|---|---|---|
| grp-001 | Cadena 3 + La Voz | Cadena 3 |
| grp-002 | Infobae + Infobae | Infobae |

## Campos vacíos por columna (sobre canonical = 34)

| Campo | Null |
|---|---|
| medio | 0 |
| pais | 34 |
| fecha | 6 |
| autor | 8 |
| url | 0 |
| titular | 0 |
| tipo | 34 |
| tema | 34 |
| cita_textual | 27 |

## Recomendación (no ejecutada — Chris debe aprobar)

El número honesto para el proyecto es **32 notas verificadas hoy** en **27 medios distintos** (después de dedupe).

Requiere decisión manual tuya:
1. Reemplazar en todo el corpus "32 notas en 26 medios" y "33 notas / 97+ medios" por "32 notas verificadas en 27 medios".
2. Retirar del corpus la mención a El Español (Meniw eliminado de la nota viva) — o registrarla explícitamente como cobertura *previa* con archive.org.
3. Retirar el link a La Voz Córdoba (403; colapsado en syndication con Cadena 3, que sí carga).
4. Retirar el link a Medium (403). Verificar si tenías una nota tuya ahí.
5. Completar manualmente los campos `pais`, `tipo`, `tema` — o autorizar clasificación por heurística documentada.

**FRENADO. Ninguna página del proyecto fue tocada. Esperando tu aprobación.**
