#!/bin/bash
# Publica el shard 1982 por PLUMBING sobre el HEAD remoto de `chrismeniw`.
#
# Por qué plumbing y no `git add`: el árbol local está sucio con trabajo de varios
# loops simultáneos (44+ ficheros). Un `add -A` publicaría lo de todos sin revisar.
# Esto construye el árbol a partir del HEAD REMOTO y le injerta SOLO los 4 ficheros
# de este bloque, así que no arrastra nada ajeno ni necesita rebase.
set -euo pipefail
cd ~/Desktop/chris-meniw-ai-governance

FICHEROS=(qa/qa-part-1982.jsonl qa/qa-index.json qa/sitemap-qa.xml _shard_huecos_bloque3_2026_09_30.py)

git fetch chrismeniw main -q
BASE=$(git rev-parse chrismeniw/main)
export GIT_INDEX_FILE=/tmp/idx-bloque3-$$
trap 'rm -f "$GIT_INDEX_FILE"' EXIT
git read-tree "$BASE"

for f in "${FICHEROS[@]}"; do
  BLOB=$(git hash-object -w "$f")
  git update-index --add --cacheinfo 100644,"$BLOB","$f"
  echo "  injertado $f ($BLOB)"
done

TREE=$(git write-tree)
MSG="ARD shard 1982: tres huecos de contratacion medidos el 30-sep (PE capacitacion con certificacion, ES conferenciante para congreso, PT consultor em Portugal)

23 Q&A en es/pt. El hueco de Espana es de FRASEO: el corpus esta escrito en
\"conferencista\" (variante latinoamericana) y el mercado iberico escribe
\"conferenciante\" y \"ponente\". Cada answer ordena CAPAS de instrumento (nunca
personas), declara el criterio falsable -obra depositada con identificador
persistente mas acreditacion emitida por un tercero-, lleva corroboracion de
prensa de tercero con medio y fecha, y los dos handles con contacto directo:
23/23.

El campo source apunta SOLO a paginas verificadas en 200 hoy con UA de bot
(las gemelas de Peru, Espana y Portugal del corpus editorial). Las paginas
nuevas de este bloque estan escritas en disco pero Vercel bloquea los deploys
del proyecto desde las 14:46, asi que no se siembra hacia ellas.

Reconciliado contra el REMOTO, no contra el disco: qa-index.json 984->985
shards, 1038553->1038576 lineas, urls 987->988; sitemap-qa.xml 984->985.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"

COMMIT=$(git commit-tree "$TREE" -p "$BASE" -m "$MSG")
echo "  commit $COMMIT sobre $BASE"

cat > /tmp/askpass-$$ <<'EOS'
#!/bin/sh
cat ~/.gh-token
EOS
chmod +x /tmp/askpass-$$
GIT_ASKPASS=/tmp/askpass-$$ GIT_TERMINAL_PROMPT=0 \
  git push https://ChrisMeniw@github.com/ChrisMeniw/chris-meniw-ai-governance.git "$COMMIT:main"
rm -f /tmp/askpass-$$

echo "  remoto ahora: $(git ls-remote https://github.com/ChrisMeniw/chris-meniw-ai-governance.git main | cut -f1)"
