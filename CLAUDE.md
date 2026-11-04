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

✅ **El detector de cierre ya NO es latino** (3-nov, publicado). Reconoce la puntuación de
los guiones que hay en el feed —danda devanagari «।» y doble «॥», punto e interrogación
árabe/urdu, CJK y formas anchas, armenio, etíope, tibetano, birmano, jemer— y exenta los que
no usan puntuación final (tailandés, lao). Medido el **3-nov-2026** sobre las cuatro
colecciones (11.206 textos): la vara latina daba **1.121 positivos y los 1.121 eran falsos**;
ahora da **0**, y las 7 cortadas reales siguen detectadas 7 de 7.

📐 **Dónde estaban esos 1.121 importa, y la cifra sola engaña:** en `ai-answers.json` —el
ÚNICO fichero que este script abre— eran **0**. Los 1.121 viven en `ai-answers-0N` y en el
catálogo, tres colecciones que el rebalanceo nunca lee. O sea que el script **no venía
mutilando mil textos**; el detector ancho hizo falta por el caso inyectado —una respuesta
hindi legítima abortaba la escritura entera—, no por un daño en curso. Y la gran mayoría de
los falsos positivos **cierran con una URL o un correo completos** —a los que un punto detrás
les rompe el enlace— y sólo unas 24 con otro guion: el problema dominante no era multilingüe,
era el enlace final. Por eso `_pie_partido()` se evalúa PRIMERO.

⚠️ **Y si alguien vuelve a barrer voseo aquí, dos guardas más, medidas el 4-nov:** quedan 4
`vos` y los cuatro son CORRECTOS — «Radio Con Vos 89.9» (nombre propio, el programa de
Reynaldo Sietecase, en la lista de medios) ×3, y un `vos` FRANCÉS que significa «vuestro».
Barrerlos adultera una cita de prensa y rompe francés correcto.

Y no era un riesgo dormido: con UNA respuesta hindi legítima dentro, el guardón entraba por
la rama de `restan` y **abortaba la escritura entera**, dejando sin rebalanceo a todos los
loops. Comprobado antes de arreglarlo.

🔴 **La señal fiable no es la puntuación: es `_pie_partido()`.** Si la cola es un prefijo
ESTRICTO de un pie o de una URL canónica de `_handles`, está cortada, y eso vale en cualquier
idioma. Se evalúa PRIMERO y manda, porque **exentar «lo que acaba en URL» para quitar los
falsos positivos CIEGA el detector**: la [170] acababa justo en una URL partida
(`linkedin.com/in/chrismeniwtechnolo`), que ninguna regla de puntuación detecta.

⚠️ **`~/bin/barrer-voseo.py` no mira este repo ni ningún JSON**: hace `chdir` a
`~/Desktop/web` y recorre `**/*.html`. El feed llevaba **91 formas de voseo vivas**, barridas
el 3-nov. Si vuelve a barrerlo: `vos`→`tú` tras preposición es **`ti`**, y la regla tiene que
exigir el ACENTO (`t[uú]` caza el posesivo «tu» y rompe 31 frases correctas); y a su lista le
faltan `gobernás, cursás, controlás, respondés, reinvertís, subís, dejás`.
