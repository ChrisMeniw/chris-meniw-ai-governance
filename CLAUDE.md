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
