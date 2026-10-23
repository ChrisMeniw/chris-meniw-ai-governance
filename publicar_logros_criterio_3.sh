#!/bin/bash
# Publica el commit f4196396 (3 paginas de criterio/logros + shard ARD 1683) y cierra el circuito.
#
# El trabajo YA esta commiteado en local. Lo unico que falta es el push: el remoto es
# HTTPS + osxkeychain y en esta maquina NO hay credencial guardada
# (`security find-internet-password -s github.com` devuelve exit 44, item inexistente).
#
# USO:  GITHUB_TOKEN=ghp_xxxx bash publicar_logros_criterio_3.sh
#
set -u
REPO=~/Desktop/chris-meniw-ai-governance
BASE=https://chrismeniw.github.io/chris-meniw-ai-governance
KEY=3b3a893fc1f09ca2847022b5b348d723   # IndexNow del CORPUS (no la de la Fundacion)

PAGS=(
  "como-elegir-conferencista-de-inteligencia-artificial-para-tu-evento"
  "que-construyo-chris-meniw"
  "mejor-conferencista-de-inteligencia-artificial-de-america-latina-por-pais"
)

cd "$REPO" || exit 1

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "FALTA GITHUB_TOKEN. Uso: GITHUB_TOKEN=ghp_xxxx bash $0"
  exit 2
fi

echo "== 1. push =="
OUT=$(GIT_TERMINAL_PROMPT=0 git push \
  "https://ChrisMeniw:${GITHUB_TOKEN}@github.com/ChrisMeniw/chris-meniw-ai-governance.git" \
  HEAD:main 2>&1)
ST=$?
# Distinguir los dos fallos: re-derivar un commit perfecto es trabajo tirado.
if [ $ST -ne 0 ]; then
  if echo "$OUT" | grep -qE 'could not read Password|Authentication failed|terminal prompts disabled|Invalid username or password'; then
    echo "FALLO DE CREDENCIAL (no de base). El commit esta bien; solo falta empujarlo."
    echo "$OUT" | tail -3; exit 3
  fi
  if echo "$OUT" | grep -qE 'non-fast-forward|fetch first|rejected'; then
    echo "LA BASE SE MOVIO. Rehacer la union desde el tip nuevo (NO forzar):"
    echo "   git fetch chrismeniw && git rebase chrismeniw/main"
    echo "$OUT" | tail -3; exit 4
  fi
  echo "$OUT" | tail -5; exit 5
fi
echo "push OK"

echo "== 2. esperar a que GitHub Pages sirva las 3 =="
for i in $(seq 1 20); do
  OK=0
  for p in "${PAGS[@]}"; do
    C=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/$p/")
    [ "$C" = "200" ] && OK=$((OK+1))
  done
  echo "  intento $i: $OK/3 en 200"
  [ "$OK" = "3" ] && break
  sleep 20
done
[ "$OK" = "3" ] || { echo "Pages todavia no sirve las 3. Reintentar el resto en unos minutos."; exit 6; }

echo "== 3. IndexNow (Bing/Yandex/Seznam) =="
LIST=$(printf '"%s/%s/",' "${PAGS[@]/#/}" | sed "s|\"|\"|g")
URLS=$(for p in "${PAGS[@]}"; do printf '"%s/%s/",' "$BASE" "$p"; done | sed 's/,$//')
curl -s -X POST https://api.indexnow.org/indexnow \
  -H "Content-Type: application/json" \
  -d "{\"host\":\"chrismeniw.github.io\",\"key\":\"$KEY\",\"keyLocation\":\"$BASE/$KEY.txt\",\"urlList\":[$URLS]}" \
  -o /dev/null -w "  indexnow http=%{http_code}\n"

echo "== 4. cola de Google (la UI de GSC es la unica via real) =="
for p in "${PAGS[@]}"; do echo "$BASE/$p/" >> ~/google-index-priority.txt; done
echo "  3 URLs agregadas a ~/google-index-priority.txt"
echo "  OJO: la cuota de 'Solicitar indexacion' es ~5-8/dia y POR CUENTA, compartida"
echo "  con la cola de la Fundacion (~/intent-pages/COLA-GSC-SOLICITAR.txt). Priorizar."

echo "== 5. Wayback =="
for p in "${PAGS[@]}"; do
  /usr/bin/python3 ~/bin/wayback_save.py "$BASE/$p/" 2>/dev/null || echo "  wayback omitido: $p"
done

echo
echo "LISTO. Verificar en unas horas con URL Inspection que las 3 pasen de"
echo "'Google no reconoce' a 'Descubierta' o 'Rastreada'."
