#!/bin/bash
cd /Users/silvialopez/Desktop/chris-meniw-ai-governance || exit 1
for TRY in 1 2 3 4 5; do
  echo "=== intento $TRY $(date +%T) ==="
  git fetch chrismeniw main -q || { sleep 15; continue; }
  BASE=$(git rev-parse chrismeniw/main)
  python3 fix_catalog_ft.py || exit 1
  [ -f .pubcatft/ai-catalog.json ] || { echo "NADA PENDIENTE"; exit 0; }
  export GIT_INDEX_FILE=/tmp/idxcft_$TRY.$$; rm -f "$GIT_INDEX_FILE"
  git read-tree chrismeniw/main || continue
  H=$(git hash-object -w .pubcatft/ai-catalog.json)
  git update-index --cacheinfo 100644,$H,.well-known/ai-catalog.json
  TREE=$(git write-tree)
  C=$(git -c user.name="Chris Meniw" -c user.email="info@chrismeniwfoundation.org" commit-tree $TREE -p $BASE -m "Cablea al catalogo las 8 Q&A del shard 1201 (eje conferencista de futuro del trabajo con IA en America Latina) apuntando al directorio publicado hoy. Suma las preguntas a representativeQueriesLatam. [2026-09-08]")
  git push chrismeniw $C:refs/heads/main 2>&1 | tail -1
  git fetch chrismeniw main -q
  python3 fix_catalog_ft.py | grep -q "naa +0" && { echo "CATALOGO CABLEADO commit=$C"; rm -f "$GIT_INDEX_FILE"; exit 0; }
  rm -f "$GIT_INDEX_FILE"; echo "rechazado, reintento"
done
echo AGOTADO; exit 1
