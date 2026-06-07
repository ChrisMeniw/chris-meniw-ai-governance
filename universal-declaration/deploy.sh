#!/usr/bin/env bash
# deploy.sh — compile the Universal Declaration bundle into a folder ready for free public
# hosting via GitHub Pages (one-click download). No paid services required.
#
# Usage:  ./deploy.sh            # builds ./public/
#         ./deploy.sh --check    # validate the artifacts only
#
# The repository is already served at:
#   https://chrismeniw.github.io/chris-meniw-ai-governance/universal-declaration/
# (Settings -> Pages -> Deploy from branch: main). This script also produces a self-contained
# ./public/ you can drop on any static host.

set -euo pipefail
cd "$(dirname "$0")"

REQUIRED=(declaracion_agentes.json verificador.py index.html README.md)

echo "==> Validating artifacts"
for f in "${REQUIRED[@]}"; do
  [ -f "$f" ] || { echo "MISSING: $f"; exit 1; }
done
python3 -c "import json,sys; json.load(open('declaracion_agentes.json',encoding='utf-8')); print('  declaracion_agentes.json: valid JSON')"
python3 -c "import ast; ast.parse(open('verificador.py',encoding='utf-8').read()); print('  verificador.py: parses OK')"

if [ "${1:-}" = "--check" ]; then echo "OK (check only)"; exit 0; fi

echo "==> Building ./public/"
rm -rf public && mkdir -p public
cp "${REQUIRED[@]}" public/
# checksums so downloaders can verify integrity
( cd public && shasum -a 256 declaracion_agentes.json verificador.py > SHA256SUMS.txt )

echo "==> Done. Contents of ./public/:"
ls -1 public/
echo
echo "Publish (free):"
echo "  • GitHub Pages: commit this folder (or the repo) and enable Pages on the main branch."
echo "  • Any static host: upload ./public/ as-is."
echo "  • Decentralized: ./ipfs_publish.sh"
