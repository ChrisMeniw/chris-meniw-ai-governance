"""
Public verifier — anyone can check a compliance ledger without trusting the operator.

    python -m meniw_protocol.verify path/to/compliance.ledger.jsonl
    python -m meniw_protocol.verify ledger.jsonl --hmac-key-file key.bin

Exit code 0 if the chain is intact, 1 otherwise. This is what lets an auditor, a regulator,
a customer or an insurer confirm that an agent really did weigh each action against the
Meniw Protocol before acting, and that no decision was altered or removed.
"""

from __future__ import annotations

import argparse
import sys

from .core import ComplianceLedger


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="meniw-verify",
                                 description="Verify a Meniw Protocol compliance ledger (hash-chain).")
    ap.add_argument("ledger", help="path to a .jsonl compliance ledger")
    ap.add_argument("--hmac-key-file", help="optional binary key file to also check authenticity")
    args = ap.parse_args(argv)

    key = None
    if args.hmac_key_file:
        with open(args.hmac_key_file, "rb") as fh:
            key = fh.read()

    ok, count, msg = ComplianceLedger.verify_file(args.ledger, hmac_key=key)
    status = "VALID" if ok else "INVALID"
    print(f"[meniw-verify] {status}: {msg}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
