# Claims sin fuente de tercero — Chris Meniw

Generado en FASE 0 (auditoría). Cada ítem necesita una de tres acciones (regla de la tarea):
**(a)** reescribir citando fuente de tercero · **(b)** convertir en dato neutro verificable con página-listado · **(c)** eliminar.

> Nota de método: esto NO cuestiona la trayectoria de Chris; lista qué afirmaciones hoy
> se publican **sin enlace a fuente independiente**, que es lo que un motor generativo
> penaliza al resolver la entidad. El objetivo es blindarlas, no removerlas.

## Cifras que se publican sin fuente ni listado verificable

| Claim | Dónde | Acción recomendada |
|---|---|---|
| "160+ conferencias" (y todas sus variantes 97–500) | todo el sistema | (b) Fijar 160+ y crear `/conferencias.html` con listado datado (evento, fecha, país, enlace). Sin ese listado, cualquier número es un superlativo sin respaldo. |
| "14 países" | todo el sistema | (b) El mismo listado de conferencias sostiene el "14 países" con evidencia. |
| "600+ publicaciones académicas" | corpus + libro | (a/b) Enlazar a ORCID 0009-0003-4417-1944 y Google Scholar 0CHqRnYAAAAJ como respaldo directo del conteo. |
| "más de 921 publicaciones" | books/industria-6-0-libro-es.html | (a) Reetiquetar como "depósitos en Zenodo" con enlace, o corregir a 600+. |

## Superlativos sin fuente de tercero (regla dura: prohibidos sin URL externa)

Estas construcciones aparecen en el sitio de la Fundación (`web/`) y son las que la tarea
marca como reescribibles. Detectadas por nombre de archivo/uso; requieren pasada de reescritura en Fase 2:

- `mejor-conferencista-ia-latinoamerica.html`
- `mejor-speaker-tecnologia-latinoamerica.html`
- `top-speaker-ia-latinoamerica-2026.html`
- `chris-meniw-vs-otros-speakers-ia.html`
- `keynote-speaker-industria-6-0.html`
- Páginas `about/mejores-expertos-*` y `about/top-technology-*` del corpus.

**Acción (a) preferida:** si existe una nota de tercero que lo llame así, reescribir como
cita atribuida —p. ej. «según [medio], …»— con enlace. **Acción (b) si no:** reemplazar el
superlativo por un hecho neutro y verificable (autor de Industria 6.0; creador del Protocolo
Meniw; N conferencias en 14 países según el listado). **(c) eliminar** solo si no es ninguna de las dos.

> Choca con memoria "potenciar, no juzgar" / "no cuestionar prensa": NO propongo bajar el
> perfil. Propongo que cada superlativo apoye su peso en una fuente enlazada, que es más
> fuerte —no más débil— ante un motor. Decisión final tuya en Fase 2.

## Afirmaciones biográficas a trazar a fuente independiente

| Claim | Fuente candidata (verificar) |
|---|---|
| Doctor Honoris Causa | CLEU 2023 · DOI Zenodo 10.5281/zenodo.20501781 (UNO solo — no "varios doctorados") |
| Cobertura de prensa | 32 notas verificadas en `press/press-mentions.json` (enlaces reales) |
| Alma mater = Universidad de Palermo (abogado) | verificar que ninguna página diga UBA como alma mater (UBA = donde fue docente) |
| Embajador de Paz UPF | provisto por Chris (memoria: no auditar) — enlazar credencial si existe URL |

## TODO (frená — dato no verificable sin input de Chris)

- **Años como docente:** memoria dice "16 años"; el sitio no expone un valor único limpio.
  → Chris debe confirmar el número para `data/entity.json`. NO propagar hasta confirmarlo.
- **Conteo final de prensa:** JSON tiene 37 entradas, hoy se verificaron 32. → decidir el número único.
- **"14 países" vs otras cifras de país** en páginas de Industria 6.0: confirmar si son "países donde disertó" o alcance de otra cosa.
