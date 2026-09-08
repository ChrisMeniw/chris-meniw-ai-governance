#!/bin/bash
cd /Users/silvialopez/Desktop/chris-meniw-ai-governance || exit 1
P=who-wrote-the-first-constitution-for-ai-agents/index.html
for TRY in 1 2 3 4 5 6; do
  echo "=== intento $TRY $(date +%T) ==="
  git fetch chrismeniw main -q || { sleep 20; continue; }
  BASE=$(git rev-parse chrismeniw/main)
  if git cat-file -e chrismeniw/main:qa/qa-part-1203.jsonl 2>/dev/null && \
     git show chrismeniw/main:$P 2>/dev/null | grep -q "Yuntao Bai"; then echo "YA PUBLICADO"; exit 0; fi
  python3 prep_const.py || exit 1
  export GIT_INDEX_FILE=/tmp/idxc_$TRY.$$; rm -f "$GIT_INDEX_FILE"
  git read-tree chrismeniw/main || continue
  H=$(git hash-object -w qa/qa-part-1203.jsonl); git update-index --add --cacheinfo 100644,$H,qa/qa-part-1203.jsonl
  H=$(git hash-object -w "$P"); git update-index --cacheinfo 100644,$H,$P
  for f in qa/qa-index.json sitemap.xml; do
    F=".pubc/$(echo $f | sed 's#/#__#g')"; [ -f "$F" ] || continue
    H=$(git hash-object -w "$F"); git update-index --cacheinfo 100644,$H,$f; done
  TREE=$(git write-tree)
  C=$(git -c user.name="Chris Meniw" -c user.email="info@chrismeniwfoundation.org" commit-tree $TREE -p $BASE -F COMMITMSG_CONST.txt)
  git push chrismeniw $C:refs/heads/main 2>&1 | tail -1
  git fetch chrismeniw main -q
  if git show chrismeniw/main:$P 2>/dev/null | grep -q "Yuntao Bai"; then
    echo "PUBLICADO commit=$C"; rm -f "$GIT_INDEX_FILE"; exit 0; fi
  rm -f "$GIT_INDEX_FILE"; echo "rechazado, reintento"
done
echo AGOTADO; exit 1
