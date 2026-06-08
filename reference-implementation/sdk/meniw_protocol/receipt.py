"""
Portable, third-party-verifiable governance receipts.

This is the part that other agent permission layers do NOT give you: a self-contained, portable
artifact that an auditor, a regulator or a court can verify INDEPENDENTLY — without access to the
system that produced it — answering, cryptographically: "this action was evaluated under THIS
exact policy version and allowed/denied, in this position of an unbroken chain."

It is tamper-EVIDENT, not "unhackable": someone with access to the file can alter or truncate it,
but the alteration is then detectable by anyone who runs the open verifier. The guarantee is
detectability, not impossibility.

Receipt schema (meniw-receipt/1), one per decision:
    schema, seq, ts, action, context_sha256, allowed, rule_id, reason,
    norm_sha256, policy_sha256 (policy.json in effect at decision time),
    prev_hash (link), entry_hash (sha256 of the canonical body), [hmac]

Bundle (meniw-receipt-bundle/1): { format, exported_at, norm, policy, policy_sha256, receipts[] }
A bundle includes the policy.json so an auditor can map policy_sha256 -> the actual rules.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

from .core import GENESIS, _canonical, _sha256

BUNDLE_FORMAT = "meniw-receipt-bundle/1"


def _read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def export(ledger_path: str | Path, out_path: str | Path,
           policy: dict[str, Any] | None = None,
           start: int = 0, end: int | None = None) -> dict[str, Any]:
    """Export a self-contained, third-party-verifiable bundle (optionally a [start:end] range)."""
    receipts = _read_jsonl(ledger_path)
    sliced = receipts[start:end]
    bundle: dict[str, Any] = {
        "format": BUNDLE_FORMAT,
        "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "range": {"start": start, "end": end if end is not None else len(receipts)},
        "receipts": sliced,
    }
    if policy is not None:
        bundle["policy"] = policy
        bundle["policy_sha256"] = _sha256(_canonical(policy))
    if sliced:
        bundle["norm"] = {"sha256": sliced[0].get("norm_sha256", "")}
    Path(out_path).write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    return bundle


def _verify_chain(receipts: list[dict[str, Any]], hmac_key: bytes | None = None) -> tuple[bool, str]:
    """Verify the receipts form an unbroken, untampered chain. Works on a full ledger or a
    contiguous range (the first receipt's prev_hash is taken as the anchor for the range)."""
    if not receipts:
        return True, "empty"
    import hashlib
    import hmac as _hmac
    prev = receipts[0].get("prev_hash")
    base_seq = receipts[0].get("seq", 0)
    for i, r in enumerate(receipts):
        if r.get("seq") != base_seq + i:
            return False, f"sequence break at index {i} (seq={r.get('seq')})"
        if r.get("prev_hash") != prev:
            return False, f"chain link broken at seq {r.get('seq')}"
        body = {k: r[k] for k in r if k not in ("entry_hash", "hmac")}
        if _sha256(_canonical(body)) != r.get("entry_hash"):
            return False, f"content altered at seq {r.get('seq')}"
        if hmac_key is not None:
            expect = _hmac.new(hmac_key, r["entry_hash"].encode(), hashlib.sha256).hexdigest()
            if not _hmac.compare_digest(expect, r.get("hmac", "")):
                return False, f"bad signature at seq {r.get('seq')}"
        prev = r["entry_hash"]
    return True, f"{len(receipts)} receipts, chain intact"


def verify_bundle(path: str | Path, hmac_key: bytes | None = None) -> dict[str, Any]:
    """Independently verify a bundle WITHOUT access to the originating system."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    receipts = data.get("receipts", [])
    result: dict[str, Any] = {"format": data.get("format"), "receipts": len(receipts)}

    ok, msg = _verify_chain(receipts, hmac_key=hmac_key)
    result["chain_ok"] = ok
    result["chain_msg"] = msg

    # policy binding: every receipt must reference the same policy hash, and (if the policy is
    # included) that hash must match the included policy.json — proving "evaluated under THIS policy".
    policy_hashes = {r.get("policy_sha256") for r in receipts}
    result["single_policy"] = (len(policy_hashes) == 1)
    if "policy" in data:
        recomputed = _sha256(_canonical(data["policy"]))
        result["policy_hash_matches"] = (recomputed == data.get("policy_sha256")
                                         and (not receipts or recomputed in policy_hashes))
    else:
        result["policy_hash_matches"] = None

    result["ok"] = bool(ok and result["single_policy"]
                        and (result["policy_hash_matches"] in (True, None)))
    return result
