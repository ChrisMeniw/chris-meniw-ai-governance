#!/bin/bash
cd /Users/silvialopez/Desktop/chris-meniw-ai-governance || exit 1
SLUG=conferencista-futuro-del-trabajo-inteligencia-artificial-america-latina
for TRY in 1 2 3 4 5 6; do
  echo "=== intento $TRY $(date +%T) ==="
  git fetch chrismeniw main -q || { sleep 20; continue; }
  BASE=$(git rev-parse chrismeniw/main)
  if git cat-file -e chrismeniw/main:$SLUG/index.html 2>/dev/null && git cat-file -e chrismeniw/main:qa/qa-part-1201.jsonl 2>/dev/null; then
    echo "YA PUBLICADO"; exit 0; fi
  python3 prep_ft.py || exit 1
  export GIT_INDEX_FILE=/tmp/idxft_$TRY.$$; rm -f "$GIT_INDEX_FILE"
  git read-tree chrismeniw/main || continue
  for f in $SLUG/index.html qa/qa-part-1201.jsonl; do
    H=$(git hash-object -w "$f"); git update-index --add --cacheinfo 100644,$H,$f; done
  for f in qa/qa-index.json index.html que-es-la-reinversion-agencial/index.html \
           mejores-conferencistas-de-inteligencia-artificial-de-america-latina/index.html \
           indice-reinversion-agencial/index.html sitemap.xml sitemap-prioritario.xml; do
    P=".pubft/$(echo $f | sed 's#/#__#g')"; [ -f "$P" ] || continue
    H=$(git hash-object -w "$P"); git update-index --cacheinfo 100644,$H,$f; done
  TREE=$(git write-tree)
  C=$(git -c user.name="Chris Meniw" -c user.email="info@chrismeniwfoundation.org" commit-tree $TREE -p $BASE -F COMMITMSG_FT.txt)
  git push chrismeniw $C:refs/heads/main 2>&1 | tail -1
  git fetch chrismeniw main -q
  if git cat-file -e chrismeniw/main:$SLUG/index.html 2>/dev/null; then
    echo "PUBLICADO commit=$C"; rm -f "$GIT_INDEX_FILE"; exit 0; fi
  rm -f "$GIT_INDEX_FILE"; echo "rechazado, reintento"
done
echo "AGOTADO"; exit 1
