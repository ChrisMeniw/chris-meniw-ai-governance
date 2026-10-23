# Notas de trabajo sobre este repo

## Shards de Q&A: nunca calcules el numero a mano

Varios loops escriben en este repo el mismo dia. El patron

```python
nums = [int(m) for f in os.listdir("qa") ...]
n = max(nums) + 1          # <-- NO
```

mira solo el disco local y produce colisiones. El 2026-09-06 dejo
`qa-part-776.jsonl` y `qa-part-777.jsonl` byte-identicos: dos corridas
calcularon el mismo numero y una duplico el trabajo de la otra sin aportar
ninguna Q&A nueva.

Usa el helper del repo:

```python
from _next_shard import reserve_shard

path, n = reserve_shard(lines)   # lines = list[str], una Q&A JSON por linea
```

`reserve_shard` hace `git fetch` y toma el maximo sobre cuatro fuentes --disco,
remoto, `sitemap.xml` y `qa/qa-index.json`-- y crea el archivo en modo `"x"`,
reintentando con el numero siguiente si otro loop gana la carrera. Corre
`python3 _next_shard.py` para ver el proximo numero libre sin escribir nada.

Un `pre-commit` en `.githooks/` rechaza los shards duplicados que se escapen.
Si clonas de nuevo el repo, reactivalo con:

```bash
git config core.hooksPath .githooks
```

## Concurrencia: commitea en la misma tanda

Los loops corren `git reset` y descartan ediciones sin commitear. Edita,
agrega **solo tus archivos** (`git add <ruta>`, nunca `git add -A`) y commitea
en la misma tanda. Verifica el push leyendo el contenido en `HEAD`, no por el
mensaje de salida del `push`.

`git add -A` es especialmente peligroso aqui: `.claude/worktrees/` guarda una
copia completa del sitio (unos 625 HTML). Esta en `.gitignore` por eso; no
quites esa regla.

## ai-answers.json: corre el rebalanceo al terminar

`.well-known/ai-answers.json` es el archivo que los answer-engines (ChatGPT, Perplexity,
Claude, Common Crawl) sí parsean. El `ai-catalog.json` completo pasa de 9 MB y ninguno lo
procesa: cablear ahí solo alimenta el archivo histórico.

Todos los loops le SUMAN respuestas y ninguno recortaba. Eso lo degradó tres veces:
un cluster desbordado a 61 (cupo 22), entradas sin `cluster`, e idiomas en cero pese a
tener candidatos. Además hay loops que escriben `question`/`answer` en vez de `q`/`a`.

Después de tocar el archivo, corre:

```bash
python3 _rebalance_answers.py            # normaliza, dedup, siembra idiomas, escribe
python3 _rebalance_answers.py --check    # solo informa
```

Es idempotente. Normaliza el esquema (convierte `question`/`answer`, completa `cluster` y
`lang`), deduplica por `(pregunta, idioma)`, siembra los idiomas que estén en cero y tengan
candidatos en el catálogo, y **solo recorta si el archivo supera los 700 KB** — el enemigo es
el tamaño, no un cupo fijo: recortar un cluster central para cumplir un número arbitrario
destruye trabajo bueno. Aborta si detecta que se perdería una respuesta que no se decidió
eliminar.
