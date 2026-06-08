"""
`meniw` command-line tool.

    meniw verify <ledger.jsonl> [--hmac-key-file k]   # verify the tamper-evident chain
    meniw anchor <ledger.jsonl> [--out DIR] [--stamp]  # checkpoint/Bitcoin-anchor the head
    meniw audit  <tool> [<tool> ...]                   # dev-time policy advice
    meniw policy-lint <policy.json>                    # catch dangerous/broken policy
"""

from __future__ import annotations

import argparse
import sys

from .core import ComplianceLedger, MeniwGate


def _verify(args) -> int:
    key = open(args.hmac_key_file, "rb").read() if args.hmac_key_file else None
    ok, n, msg = ComplianceLedger.verify_file(args.ledger, hmac_key=key)
    print(f"[meniw verify] {'VALID' if ok else 'INVALID'}: {msg}")
    return 0 if ok else 1


def _anchor(args) -> int:
    from . import anchor as _a
    led = ComplianceLedger.load(args.ledger)
    rec = _a.checkpoint(led.head(), args.out, seq=len(led.receipts) - 1, stamp=args.stamp)
    print(f"[meniw anchor] head={rec['head'][:16]}… status={rec['status']}")
    if rec.get("howto"):
        print("  " + rec["howto"])
    return 0


def _audit(args) -> int:
    from .advisor import audit
    print(audit(list(args.tools), MeniwGate.from_default()).text())
    return 0


def _policy_lint(args) -> int:
    from .lint import lint_file
    ok, findings = lint_file(args.policy)
    for level, msg in findings:
        print(f"[{level}] {msg}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="meniw", description="Meniw Protocol governance layer CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="verify a compliance ledger")
    v.add_argument("ledger"); v.add_argument("--hmac-key-file"); v.set_defaults(fn=_verify)

    a = sub.add_parser("anchor", help="checkpoint / Bitcoin-anchor the ledger head")
    a.add_argument("ledger"); a.add_argument("--out", default="meniw_anchors")
    a.add_argument("--stamp", action="store_true", help="also OpenTimestamps-stamp (needs `ots`)")
    a.set_defaults(fn=_anchor)

    au = sub.add_parser("audit", help="dev-time policy advice for tool names")
    au.add_argument("tools", nargs="+"); au.set_defaults(fn=_audit)

    pl = sub.add_parser("policy-lint", help="lint a policy.json for fail-closed safety")
    pl.add_argument("policy"); pl.set_defaults(fn=_policy_lint)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
