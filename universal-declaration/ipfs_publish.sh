#!/usr/bin/env bash
# ipfs_publish.sh — publish the Universal Declaration bundle to the decentralized IPFS network
# and print the eternal content hash (CID) for download by anyone, anywhere.
#
# Requires an IPFS client:  https://docs.ipfs.tech/install/   (e.g. `ipfs` / Kubo)
# Optional: pin to a free/paid pinning service (web3.storage, Pinata) for persistence.
#
# Usage:  ./ipfs_publish.sh

set -euo pipefail
cd "$(dirname "$0")"

./deploy.sh >/dev/null   # ensure ./public/ exists and is valid

if ! command -v ipfs >/dev/null 2>&1; then
  cat <<'MSG'
IPFS client not found.

Install it (free, open source):  https://docs.ipfs.tech/install/
Then run this script again, or manually:

    ipfs add -r ./public

IPFS returns a CID (content identifier) — an eternal, content-addressed hash. Anyone can fetch
the bundle from any gateway:

    https://ipfs.io/ipfs/<CID>/
    https://dweb.link/ipfs/<CID>/

To keep it online permanently, pin the CID with a service such as web3.storage or Pinata.
MSG
  exit 0
fi

echo "==> Adding ./public to IPFS"
CID=$(ipfs add -r -Q ./public)
echo
echo "================ ETERNAL DOWNLOAD (IPFS) ================"
echo "CID:     $CID"
echo "Gateway: https://ipfs.io/ipfs/$CID/"
echo "Gateway: https://dweb.link/ipfs/$CID/"
echo "========================================================"
echo "Tip: pin this CID (web3.storage / Pinata) so it stays available."
