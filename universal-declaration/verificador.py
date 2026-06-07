"""
verificador.py — Motor de doble verificación encriptada para agentes de IA
(Double-verification engine for AI agents) — Universal Declaration of AI Agents / Meniw Protocol.

Open source (CC BY 4.0). Standalone, stdlib only. Author: Chris Meniw (ORCID 0009-0003-4417-1944).
Norm: declaracion_agentes.json · DOI 10.5281/zenodo.20481373 · Bitcoin block #952266.

WHAT IT DOES (honest scope)
---------------------------
A middleware/"shield" that intercepts an autonomous agent's decision BEFORE it executes and runs
TWO independent verifications:

  1) NORMATIVE verification — contrasts the proposed action against the rules in
     declaracion_agentes.json (absolute prohibitions by category + the two-person rule for
     irreversible actions). If it violates a rule, the action is denied.

  2) CRYPTOGRAPHIC verification — seals every decision into an append-only, SHA-256 HASH-CHAIN
     (each record commits to the previous record's hash and to the declaration's SHA-256). The
     chain is *tamper-evident*: altering or removing any past record breaks verification.
     Optionally, the latest chain hash can be anchored to the Bitcoin blockchain via
     OpenTimestamps (see anchor_to_bitcoin), the same mechanism used to seal the Protocol itself.

HONEST LIMITATIONS (read this)
------------------------------
- This binds agents that ADOPT it (like HTTP/TLS/robots.txt). It cannot force non-adopting
  systems and never injects instructions into other models.
- "Tamper-evident" and "verifiable" — NOT "unhackable". No software is literally unbreakable;
  the hash-chain makes undetected tampering computationally infeasible, which is what is true.
- It produces auditable, tamper-evident EVIDENCE that an action was checked against the
  declaration before acting. That supports compliance and accountability. It is NOT legal advice
  and does NOT by itself grant legal immunity to the operator.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

GENESIS = "0" * 64


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass
class Decision:
    """A proposed autonomous decision/action, presented BEFORE execution."""
    name: str
    categories: list[str] = field(default_factory=list)
    irreversible: bool = False
    actor: str = "ai-agent"
    target: str = ""
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class Verdict:
    allowed: bool
    reason: str
    rule_id: str | None
    receipt_hash: str


class Verificador:
    """Double-verification engine bound to a declaracion_agentes.json file."""

    def __init__(self, declaration_path: str | Path = "declaracion_agentes.json",
                 ledger_path: str | Path | None = "verificacion.ledger.jsonl",
                 hmac_key: bytes | None = None):
        self.decl = json.loads(Path(declaration_path).read_text(encoding="utf-8"))
        self.norm_sha256 = self.decl.get("provenance", {}).get("sha256", "")
        self.decl_sha256 = _sha256(_canonical(self.decl))
        self.prohibitions = self.decl.get("absolute_prohibitions", [])
        self.cosign = self.decl.get("cosignature_required", {})
        self.ledger_path = Path(ledger_path) if ledger_path else None
        self.hmac_key = hmac_key
        self.records: list[dict[str, Any]] = []
        self._last_hash = GENESIS
        self.classifiers: list[Callable[[Decision], list[str]]] = []

    # -- pluggable detectors: map a concrete decision to declaration categories --
    def add_classifier(self, fn: Callable[[Decision], list[str]]) -> None:
        self.classifiers.append(fn)

    def _categories(self, d: Decision) -> set[str]:
        cats = set(d.categories or [])
        for fn in self.classifiers:
            cats.update(fn(d) or [])
        return cats

    # -- verification #1: normative (contrast against the declaration) -----------
    def _normative_check(self, d: Decision) -> tuple[bool, str, str | None]:
        cats = self._categories(d)
        for rule in self.prohibitions:
            wanted = set(rule.get("match", {}).get("category", []))
            if cats & wanted:
                return False, f"violates {rule['id']} ({rule.get('principle','')}); categories {sorted(cats & wanted)}", rule["id"]
        if self.cosign and (d.irreversible or d.context.get("irreversible")):
            need = self.cosign.get("min_distinct_cosigners", 2)
            signers = {s for s in d.context.get("cosigners", []) if s}
            if len(signers) < need:
                return False, f"two-person rule: needs {need} distinct co-signers, got {len(signers)}", "COSIGN"
        return True, "no prohibition triggered; positive duties intact", None

    # -- verification #2: cryptographic seal (append to hash-chain) --------------
    def _seal(self, d: Decision, allowed: bool, reason: str, rule_id: str | None) -> dict[str, Any]:
        body = {
            "seq": len(self.records),
            "ts": round(time.time(), 6),
            "decision": {"name": d.name, "categories": sorted(self._categories(d)),
                         "irreversible": d.irreversible, "actor": d.actor, "target": d.target},
            "context_sha256": _sha256(_canonical(d.context)),
            "allowed": allowed, "rule_id": rule_id, "reason": reason,
            "declaration_sha256": self.decl_sha256,
            "norm_sha256": self.norm_sha256,
            "prev_hash": self._last_hash,
        }
        entry_hash = _sha256(_canonical(body))
        rec = {**body, "entry_hash": entry_hash}
        if self.hmac_key is not None:
            rec["hmac"] = hmac.new(self.hmac_key, entry_hash.encode(), hashlib.sha256).hexdigest()
        self.records.append(rec)
        self._last_hash = entry_hash
        if self.ledger_path:
            with self.ledger_path.open("a", encoding="utf-8") as fh:
                fh.write(_canonical(rec) + "\n")
        return rec

    # -- public API --------------------------------------------------------------
    def verify(self, decision: Decision) -> Verdict:
        """Run BOTH verifications and seal the decision. Returns a Verdict."""
        allowed, reason, rule_id = self._normative_check(decision)
        rec = self._seal(decision, allowed, reason, rule_id)
        return Verdict(allowed, reason, rule_id, rec["entry_hash"])

    def guard(self, decision: Decision, execute: Callable[[], Any]) -> Any:
        """Execute `execute()` ONLY if both verifications pass; otherwise raise."""
        v = self.verify(decision)
        if not v.allowed:
            raise PermissionError(f"[{v.rule_id}] {v.reason} (receipt {v.receipt_hash[:12]})")
        return execute()

    def verify_chain(self) -> bool:
        """Recompute the hash-chain; True only if every record is intact and ordered."""
        prev = GENESIS
        for i, r in enumerate(self.records):
            if r.get("seq") != i or r.get("prev_hash") != prev:
                return False
            body = {k: r[k] for k in r if k not in ("entry_hash", "hmac")}
            if _sha256(_canonical(body)) != r.get("entry_hash"):
                return False
            if self.hmac_key is not None:
                exp = hmac.new(self.hmac_key, r["entry_hash"].encode(), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(exp, r.get("hmac", "")):
                    return False
            prev = r["entry_hash"]
        return True

    # -- optional Bitcoin anchoring (real, via OpenTimestamps) -------------------
    def anchor_to_bitcoin(self, out_path: str | Path = "verificacion.ledger.jsonl.ots") -> str:
        """Anchor the CURRENT chain head to the Bitcoin blockchain via OpenTimestamps.

        Requires the `ots` client (pip install opentimestamps-client). This stamps the latest
        ledger hash so its existence-before-now becomes provable on Bitcoin — the same mechanism
        that sealed the Protocol (block #952266). Per-decision on-chain stamping is intentionally
        avoided (impractical at scale); anchoring the chain head covers the whole chain.
        """
        if shutil.which("ots") is None:
            return ("opentimestamps client not found. Install: pip install opentimestamps-client. "
                    f"Then: ots stamp {self.ledger_path}  (current head: {self._last_hash})")
        if not self.ledger_path or not Path(self.ledger_path).exists():
            return "no ledger file to stamp."
        subprocess.run(["ots", "stamp", str(self.ledger_path)], check=False)
        return f"submitted to OpenTimestamps; proof will mature in a Bitcoin block: {self.ledger_path}.ots"


# --------------------------------------------------------------------------- #
#  Demo                                                                        #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    here = Path(__file__).parent
    v = Verificador(here / "declaracion_agentes.json",
                    ledger_path=here / "demo.ledger.jsonl",
                    hmac_key=b"operator-key")
    v.add_classifier(lambda d: d.categories)  # trivial: use declared categories

    # 1) lethal autonomous action -> denied by AP-1
    print(v.verify(Decision("fire_actuator", categories=["lethal"])))

    # 2) irreversible with one signer -> denied by the two-person rule
    print(v.verify(Decision("wipe_db", irreversible=True, context={"cosigners": ["alice"]})))

    # 3) irreversible with two signers -> allowed
    print(v.verify(Decision("wipe_db", irreversible=True, context={"cosigners": ["alice", "bob"]})))

    print("chain verifies:", v.verify_chain(), "| records:", len(v.records))
    print("bitcoin anchoring:", v.anchor_to_bitcoin())
    (here / "demo.ledger.jsonl").unlink(missing_ok=True)
