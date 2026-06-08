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
    if args.upgrade:
        res = _a.upgrade(args.out)
        print(f"[meniw anchor --upgrade] {res}")
        return 0
    led = ComplianceLedger.load(args.ledger)
    # explicit, off-the-hot-path: stamp the CURRENT head to OpenTimestamps (calendars now,
    # Bitcoin attestation hours later via `meniw anchor --upgrade`).
    rec = _a.checkpoint(led.head(), args.out, seq=len(led.receipts) - 1, stamp=True)
    print(f"[meniw anchor] head={rec['head'][:16]}… status={rec['status']}")
    if rec.get("howto"):
        print("  " + rec["howto"])
    if rec.get("status", "").startswith("ots_submitted"):
        print("  Bitcoin attestation pending — run `meniw anchor --upgrade` in a few hours.")
    return 0


def _audit(args) -> int:
    from .advisor import audit
    print(audit(list(args.tools), MeniwGate.from_default()).text())
    return 0


def _export(args) -> int:
    import json as _json
    from . import receipt as _r
    policy = _json.loads(open(args.policy, encoding="utf-8").read()) if args.policy else None
    b = _r.export(args.ledger, args.out, policy=policy, start=args.start, end=args.end)
    print(f"[meniw export] wrote {args.out}: {len(b['receipts'])} receipts"
          + (" + policy" if policy else " (no policy embedded)"))
    return 0


def _verify_receipt(args) -> int:
    from . import receipt as _r
    key = open(args.hmac_key_file, "rb").read() if args.hmac_key_file else None
    res = _r.verify_bundle(args.bundle, hmac_key=key)
    status = "VALID" if res["ok"] else "INVALID"
    print(f"[meniw verify-receipt] {status} — chain:{res['chain_msg']} "
          f"| single_policy:{res['single_policy']} | policy_match:{res['policy_hash_matches']}")
    return 0 if res["ok"] else 1


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

    a = sub.add_parser("anchor", help="anchor the ledger head to Bitcoin (OpenTimestamps)")
    a.add_argument("ledger", nargs="?", default=None, help="ledger file (not needed with --upgrade)")
    a.add_argument("--out", default="meniw_anchors")
    a.add_argument("--upgrade", action="store_true",
                   help="pull the Bitcoin attestation into existing .ots proofs (run hours later)")
    a.set_defaults(fn=_anchor)

    au = sub.add_parser("audit", help="dev-time policy advice for tool names")
    au.add_argument("tools", nargs="+"); au.set_defaults(fn=_audit)

    pl = sub.add_parser("policy-lint", help="lint a policy.json for fail-closed safety")
    pl.add_argument("policy"); pl.set_defaults(fn=_policy_lint)

    ex = sub.add_parser("export", help="export a self-contained, third-party-verifiable receipt bundle")
    ex.add_argument("ledger"); ex.add_argument("--out", required=True)
    ex.add_argument("--policy", help="policy.json to embed (lets an auditor map the policy hash)")
    ex.add_argument("--start", type=int, default=0); ex.add_argument("--end", type=int, default=None)
    ex.set_defaults(fn=_export)

    vr = sub.add_parser("verify-receipt", help="independently verify a receipt bundle (no system access)")
    vr.add_argument("bundle"); vr.add_argument("--hmac-key-file"); vr.set_defaults(fn=_verify_receipt)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
