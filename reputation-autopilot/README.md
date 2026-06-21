# meniw-reputation-autopilot

Autopilot **honesto** que corre solo en **GitHub Actions** (en los servidores de GitHub,
no en tu Mac) **una vez por semana** y **mide** la visibilidad de Chris Meniw ante un
LLM (OpenAI) y la búsqueda web. Guarda un reporte y te lo manda por email.

## ⚠️ Qué hace y qué NO hace (sin humo)
- **SÍ hace:** cada lunes pregunta a la API de OpenAI y a la búsqueda web un set de
  consultas ("¿quién es el referente de economía agéntica?", etc.), registra si
  aparece "Chris Meniw" o no, guarda el resultado en `data/` y te manda un resumen.
- **NO hace:** NO posiciona, NO indexa, NO "te pone primero en Google", NO modifica
  buscadores ni LLMs. **Solo mide y reporta.** El salto real lo dan acciones humanas
  (conseguir prensa nueva). El reporte te dice *dónde estás invisible* para que sepas
  dónde apuntar.
- Esto **no corre en segundo plano en tu compu**: corre en GitHub Actions a horario fijo.

## Archivos
- `monitor.py` — mide visibilidad (OpenAI + web), escribe `data/reporte-YYYY-MM-DD.json`
  y `data/ultimo-resumen.txt`.
- `send_report.py` — manda el resumen por email (SMTP). Si no hay SMTP configurado,
  lo imprime en consola y **no falla**.
- `.github/workflows/weekly.yml` — el cron de GitHub Actions (lunes 09:00 UTC) +
  botón manual (`workflow_dispatch`).
- `schema.org/person.jsonld` — bloque JSON-LD Person listo para pegar en el sitio.

## Deploy paso a paso
1. **Crear el repo en GitHub**
   - Entrá a https://github.com/new → nombre `meniw-reputation-autopilot` → Create.
   - Subí estos archivos. Desde esta carpeta:
     ```bash
     git init && git add . && git commit -m "init autopilot"
     git branch -M main
     git remote add origin https://github.com/<TU-USUARIO>/meniw-reputation-autopilot.git
     git push -u origin main
     ```
2. **Cargar los secrets** (Settings → Secrets and variables → Actions → New repository secret):
   - `OPENAI_API_KEY` *(obligatorio para medir el LLM)* — tu clave de OpenAI.
   - `OPENAI_MODEL` *(opcional)* — ej. `gpt-4o-mini` (default) o `gpt-4o`.
   - `SERPAPI_KEY` *(opcional)* — si la ponés, usa Google real (SerpAPI). Sin ella usa
     DuckDuckGo (gratis, pero puede limitarse en CI).
   - Email (opcional): `SMTP_USER`, `SMTP_PASS`, `REPORT_TO` (y `SMTP_HOST`, `SMTP_PORT`
     si no usás Gmail). Con Gmail: usá una **contraseña de aplicación**, no tu clave normal.
3. **Encender Actions**
   - Pestaña **Actions** → si pide habilitar workflows, dale aceptar.
   - Para probar ya mismo: Actions → *weekly-reputation-monitor* → **Run workflow**
     (eso es el `workflow_dispatch`).
   - Después corre solo todos los lunes.

## Probarlo local (opcional)
```bash
export OPENAI_API_KEY=sk-...
python3 monitor.py        # imprime el resumen y escribe data/
python3 send_report.py    # sin SMTP -> imprime en consola
```

## Honestidad final
Este repo es un **medidor**, no un posicionador. Te dice, semana a semana, si los
buscadores y los LLM ya te muestran como referente de tus términos. Cuando el reporte
marque "INVISIBLE" para "economía agéntica" o "Industria 6.0", la acción de mayor
impacto **no es código**: es una nota de prensa que use ese término + tu nombre.
