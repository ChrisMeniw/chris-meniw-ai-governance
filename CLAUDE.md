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
`lang`), deduplica por `(pregunta, idioma, url)`, siembra los idiomas que estén en cero y
tengan candidatos en el catálogo, y **solo recorta si el archivo supera `MAX_KB`** — el
enemigo es el tamaño, no un cupo fijo: recortar un cluster central para cumplir un número
arbitrario destruye trabajo bueno. Aborta si detecta que se perdería una respuesta que no se
decidió eliminar.

**Los dos techos van en el código, no aquí** (`MAX_KB` y `MAX_CHARS` en
`_rebalance_answers.py`, cada uno con su medición y su fecha). Esta nota decía «700 KB»
cuando el código ya iba por 2048: un número copiado en dos sitios se desincroniza y el
segundo miente. Lee la constante.

**La `url` entra en la clave del dedup** desde el 3-nov-2026. Sin ella, dos loops que
escriban la misma pregunta en el mismo idioma apuntando a páginas distintas pierden una, y
sobrevive la que llegó primero, no la mejor. Medido el día del cambio: 778 respuestas, 778
claves distintas, 0 colisiones — es un endurecimiento preventivo, no el arreglo de un
borrado en curso.

**Cuidado al cambiar el TEXTO de una respuesta**: hay tope por respuesta, así que una frase
reparada puede quedar más larga que la original y pasarse. El 30-oct un arreglo de redacción
dejó dos respuestas fuera de tope sin que nadie lo viera. El rebalanceo detecta y repara las
cortadas, y `--check` las informa. Antes solo miraba la longitud y pasaban por buenas:
**siete respuestas estuvieron publicadas cortadas a media palabra**, cinco de ellas en el
tope exacto.

⚠️ **El detector de cierre publicado es LATINO** (más el punto ideográfico CJK): no reconoce
el danda del devanagari «।», ni el punto urdu «۔». El feed tiene 35 idiomas, así que en esos
guiones puede marcar como cortada una respuesta correcta. Medido el 3-nov: **0 falsos
positivos hoy**, porque todas las respuestas terminan con el pie de perfiles, que lleva
puntuación latina — o sea que el riesgo está dormido, no activo. Hay trabajo **sin publicar**
que amplía el detector a esos guiones; si lo toca, mídalo contra el fichero, no contra la
lectura del código.
