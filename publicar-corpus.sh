#!/bin/bash
# Publica la cadena pendiente del corpus y verifica que sobrevivio.
#
# Uso:  ./publicar-corpus.sh
#
# VIAS DE ESCRITURA (prueba en este orden, usa la primera que funcione):
#   1. PAT  — token en ~/.config/corpus-push-token  (o en $GITHUB_TOKEN / $GH_TOKEN)
#   2. SSH  — clave ~/.ssh/id_ed25519_chrismeniw registrada como deploy key con escritura
#
# Para dejar el PAT listo (el token lo pega Chris, no se escribe en ningun log):
#   mkdir -p ~/.config
#   printf '%s' 'PEGAR_AQUI_EL_TOKEN' > ~/.config/corpus-push-token
#   chmod 600 ~/.config/corpus-push-token
# El PAT necesita permiso de escritura sobre ChrisMeniw/chris-meniw-ai-governance:
#   - fine-grained: Repository permissions -> Contents: Read and write
#   - classic:      scope 'repo'
#
# Distingue los dos fallos que se confunden (ver project_push_sin_credencial_osxkeychain):
#   SIN CREDENCIAL -> el commit esta perfecto, solo falta poder empujar. NO re-derivar.
#   BASE MOVIDA    -> hay que rehacer la union desde la base nueva.

set -u
REPO="$HOME/Desktop/chris-meniw-ai-governance"
REF="refs/pendiente/tanda-post-15sep"
REMOTE="chrismeniw"
HTTPS_URL="https://github.com/ChrisMeniw/chris-meniw-ai-governance.git"
TOKEN_FILE="$HOME/.config/corpus-push-token"
IN_KEY="3b3a893fc1f09ca2847022b5b348d723"
IN_HOST="chrismeniw.github.io"

cd "$REPO" || { echo "No existe $REPO"; exit 1; }

TIP=$(git rev-parse "$REF" 2>/dev/null) || { echo "No existe el ref $REF"; exit 1; }
echo "Cadena a publicar: $REF = ${TIP:0:8}"

BASE=$(git ls-remote "$HTTPS_URL" refs/heads/main 2>/dev/null | cut -f1)
[ -n "$BASE" ] && echo "Remoto main = ${BASE:0:8}   commits a publicar: $(git log --oneline "$BASE..$TIP" 2>/dev/null | wc -l | tr -d ' ')"

# --- guardia: la cadena no puede borrar archivos ---
if [ -n "$BASE" ]; then
  DEL=$(git diff --diff-filter=D --name-only "$BASE" "$TIP" 2>/dev/null | wc -l | tr -d ' ')
  echo "Archivos borrados vs remoto: $DEL"
  [ "$DEL" != "0" ] && { echo "ABORTA: la cadena borra archivos."; exit 1; }
fi

# --- cargar PAT, sin imprimirlo nunca ---
# OJO: nunca '2>&1' al leer una credencial: el texto de error se cuela como si fuera el valor.
CORPUS_TOKEN=""
if [ -n "${GITHUB_TOKEN:-}" ]; then CORPUS_TOKEN="$GITHUB_TOKEN"; SRC="\$GITHUB_TOKEN"
elif [ -n "${GH_TOKEN:-}" ];     then CORPUS_TOKEN="$GH_TOKEN";     SRC="\$GH_TOKEN"
elif [ -f "$TOKEN_FILE" ];       then CORPUS_TOKEN=$(tr -d ' \t\n\r' < "$TOKEN_FILE" 2>/dev/null); SRC="$TOKEN_FILE"
fi

# Validar por FORMA, no por longitud: un error del llavero mide 91 caracteres y parece un token.
USE_PAT=0
if [ -n "$CORPUS_TOKEN" ]; then
  case "$CORPUS_TOKEN" in
    ghp_*|gho_*|ghs_*|ghu_*|github_pat_*)
      USE_PAT=1; echo "PAT detectado en $SRC (prefijo valido, ${#CORPUS_TOKEN} chars). No se imprime." ;;
    *)
      echo "AVISO: hay algo en $SRC pero NO tiene prefijo de token de GitHub"
      echo "       (esperado ghp_/gho_/ghs_/ghu_/github_pat_). Se ignora." ;;
  esac
fi

# Helper efimero: el token se pasa por ENTORNO, nunca por la linea de comandos (ps lo veria).
export CORPUS_TOKEN
PAT_HELPER='!f() { echo username=x-access-token; echo "password=$CORPUS_TOKEN"; }; f'

push_try() {  # $1 = dry-run|real ; imprime stderr, devuelve el codigo
  local dry=""; [ "$1" = "dry-run" ] && dry="--dry-run"
  if [ "$USE_PAT" = "1" ]; then
    git -c credential.helper= -c credential.helper="$PAT_HELPER" \
        -c credential.useHttpPath=false \
        push $dry "$HTTPS_URL" "$TIP:refs/heads/main" 2>&1
  else
    GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=10" GIT_TERMINAL_PROMPT=0 \
        git push $dry "$REMOTE" "$TIP:refs/heads/main" 2>&1
  fi
}

no_cred() {  # reconoce "no hay credencial de escritura" en cualquiera de las dos vias
  echo "$1" | grep -qiE "could not read (Password|Username)|Authentication failed|terminal prompts disabled|Permission denied \(publickey\)|Could not read from remote|Invalid username or password|Bad credentials|403"
}

[ "$USE_PAT" = "1" ] && VIA="PAT via HTTPS" || VIA="SSH"
echo "--- probando credencial de escritura ($VIA) ---"
ERR=$(GIT_TERMINAL_PROMPT=0 push_try dry-run)
if no_cred "$ERR"; then
  echo "SIN CREDENCIAL DE ESCRITURA. El trabajo esta intacto en $REF; no hay nada que rehacer."
  echo "Detalle: $(echo "$ERR" | grep -viE '^remote:' | tail -1)"
  echo
  if [ "$USE_PAT" = "1" ]; then
    echo "El PAT no tiene escritura sobre el repo, o esta vencido/revocado. Revisar:"
    echo "  - fine-grained: que el repo ChrisMeniw/chris-meniw-ai-governance este en 'Repository access'"
    echo "                  y Contents = Read and write"
    echo "  - classic:      scope 'repo' marcado"
    echo "  - que el PAT sea de la cuenta ChrisMeniw (NO de presidentspacekid-tech)"
  else
    echo "No hay PAT. Opciones:"
    echo "  a) dejar el token en $TOKEN_FILE (chmod 600) y volver a correr esto"
    echo "  b) registrar la deploy key con escritura:"
    echo "     Settings -> Deploy keys -> Add deploy key -> Allow write access"
    echo "     pegando ~/.ssh/id_ed25519_chrismeniw.pub"
  fi
  exit 2
fi

echo "--- publicando ---"
OUT=$(push_try real); RC=$?
echo "$OUT" | grep -viE 'x-access-token|ghp_|github_pat_' | tail -3
if [ $RC -ne 0 ]; then
  if echo "$OUT" | grep -qiE "non-fast-forward|fetch first|rejected"; then
    echo "BASE MOVIDA: el remoto avanzo. Rehacer la union desde la base nueva (NO reintentar este commit)."
    exit 3
  fi
  echo "Push fallido por otra causa. No se dispara IndexNow."; exit 1
fi

# --- verificar contra el remoto y por contenido ---
echo "--- verificando ---"
NEW=$(git ls-remote "$HTTPS_URL" refs/heads/main | cut -f1)
echo "remoto main = ${NEW:0:8}   esperado = ${TIP:0:8}"
[ "$NEW" = "$TIP" ] || { echo "ATENCION: el remoto no quedo en el tip esperado."; exit 1; }
git fetch "$REMOTE" main -q 2>/dev/null
R=$(git rev-parse FETCH_HEAD)
echo "shards en el remoto: $(git ls-tree -r --name-only "$R" qa/ | grep -c '\.jsonl$')"
git show "$R:qa/qa-index.json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
slc=d.get('shardLineCount') or {}
print('qa-index: parts=%s total=%s urls=%d shardLineCount=%d' % (d['parts'], d['total'], len(d.get('urls',[])), len(slc)))
if slc and len(slc)!=len(d.get('urls',[])): print('  AVISO: urls y shardLineCount no coinciden — alta incompleta')"

# --- IndexNow, solo despues de un push verificado ---
echo "--- IndexNow ---"
URLS=$(git diff --name-only "$BASE" "$TIP" 2>/dev/null | grep -E '\.(html|jsonl|txt|json|xml)$' \
       | sed "s|^|https://$IN_HOST/chris-meniw-ai-governance/|" | head -200 \
       | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))")
BODY=$(python3 -c "
import json,sys
print(json.dumps({'host':'$IN_HOST','key':'$IN_KEY',
 'keyLocation':'https://$IN_HOST/chris-meniw-ai-governance/$IN_KEY.txt',
 'urlList':json.loads(sys.argv[1])}))" "$URLS")
for EP in https://api.indexnow.org/indexnow https://www.bing.com/indexnow; do
  CODE=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$EP" \
         -H 'Content-Type: application/json; charset=utf-8' --data "$BODY" --max-time 30)
  echo "$EP -> HTTP $CODE"
done
echo "LISTO."
