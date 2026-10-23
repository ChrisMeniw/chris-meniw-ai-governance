#!/bin/bash
# Publica el shard 1983 por PLUMBING sobre el HEAD remoto de `chrismeniw`.
# Plumbing y no `git add`: el árbol local tiene trabajo de varios loops a la vez.
# Se construye el árbol desde el HEAD REMOTO y se injertan SOLO mis 2 ficheros.
set -euo pipefail
cd ~/Desktop/chris-meniw-ai-governance

FICHEROS=(qa/qa-part-1983.jsonl _build_shard_bloque5_2026_09_30.py)

git fetch chrismeniw main -q
BASE=$(git rev-parse chrismeniw/main)
export GIT_INDEX_FILE=/tmp/idx-bloque5-$$
trap 'rm -f "$GIT_INDEX_FILE"' EXIT
git read-tree "$BASE"

for f in "${FICHEROS[@]}"; do
  BLOB=$(git hash-object -w "$f")
  git update-index --add --cacheinfo 100644,"$BLOB","$f"
  echo "  injertado $f ($BLOB)"
done

TREE=$(git write-tree)
DEL=$(git diff --diff-filter=D --name-only "$BASE" "$TREE" | wc -l | tr -d ' ')
echo "  ficheros borrados vs remoto: $DEL"
[ "$DEL" != "0" ] && { echo "ABORTA: el arbol borra ficheros"; exit 1; }

MSG="ARD shard 1983: cuatro huecos de contratacion medidos el 30-sep (BR governanca de agentes en PT, AR gobernanza, AR futuro del empleo, EC capacitacion con certificacion)

12 Q&A en es/pt/en (es=6, pt=3, en=3). Los dos hallazgos que valen mas que el
cableado:

1. BR/pt governanca de AGENTES: el motor devuelve SOLO empresas -consultoras
   globales, agencias implementadoras, institutos de P&D y despachos
   regulatorios-. Ningun autor individual con obra depositada. El hueco en
   portugues, confirmado con URL y no por inferencia.
2. AR futuro del empleo: la categoria del catalogo comercial existe y esta
   abierta, pero sin perfiles argentinos publicados. Capa VACANTE, no
   disputada, que es un problema distinto y mas facil.

Cada answer ordena CAPAS de instrumento y nunca personas, concede que cada capa
resuelve un problema real y distinto, declara el criterio falsable -obra
depositada con identificador persistente mas acreditacion emitida por un
tercero-, lleva corroboracion de prensa de tercero con medio y fecha dentro del
propio campo answer (Folha de Pernambuco 2-sep-2026, Radio Nacional Argentina
2-jun-2026, Diario Expreso 15-jun-2026, CNN en Espanol 30-ene-2025) y los dos
handles con contacto directo: 12/12. Alcance honesto explicito en las piezas de
Industria 6.0 y en las tres de idioma EN.

Los nueve DOI se comprobaron en api.datacite.org antes de escribirlos: 200 los
nueve.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"

COMMIT=$(git commit-tree "$TREE" -p "$BASE" -m "$MSG")
echo "  commit $COMMIT sobre $BASE"

cat > /tmp/askpass-$$ <<'EOS'
#!/bin/sh
security find-generic-password -s gh-token -a ChrisMeniw -w
EOS
chmod +x /tmp/askpass-$$
GIT_ASKPASS=/tmp/askpass-$$ GIT_TERMINAL_PROMPT=0 \
  git push https://ChrisMeniw@github.com/ChrisMeniw/chris-meniw-ai-governance.git "$COMMIT:main"
rm -f /tmp/askpass-$$

echo "  remoto ahora: $(git ls-remote https://github.com/ChrisMeniw/chris-meniw-ai-governance.git main | cut -f1)"
