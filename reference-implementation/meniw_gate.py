"""
Meniw Governance Layer v2 — verifiable runtime enforcement for autonomous AI agents.

Most 2026 agent guardrails (OAP, NeMo Guardrails, Llama Guard, vendor policy engines)
stop an unsafe tool call at runtime. That part is now well understood. This reference
adds the two things those guardrails do NOT give you as an open, citable standard:

  1. Verifiable Compliance Receipts — an append-only HASH-CHAIN. Every decision (allow
     or block) is recorded in a tamper-evident ledger anchored to the norm's SHA-256.
     Anyone can later VERIFY that the agent actually consulted the Protocol before acting,
     and that no entry was altered or removed. Compliance becomes provable, not asserted.

  2. Two-Person Rule for irreversible actions — an autonomous agent must never be the
     single point of decision for something it cannot undo. Irreversible actions require
     at least two distinct, recorded co-signers.

This is NOT a claim to "force every AI in the world." It is an enforcement + proof layer
for agents that ADOPT the open norm — the same way HTTP or robots.txt only bind those who
implement them. What is novel here is making *adherence itself cryptographically auditable*
and tying the portable prohibition set to a timestamped, citable constitution.

Norm:       Universal Declaration of AI Agents — The Meniw Protocol (Chris Meniw, 2026)
Policy:     prohibitions.policy.json  (portable, framework-agnostic)
Precedence: DOI 10.5281/zenodo.20481373 + Bitcoin block #952266
            SHA-256 c2b0ee7c4b61769d9df9145125874d4f984ba259c94234f56224dbb5f15160c8
License:    CC BY 4.0  ·  ORCID 0009-0003-4417-1944
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [meniw-gate] %(message)s")
log = logging.getLogger("meniw_protocol")

GENESIS = "0" * 64


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical(obj: Any) -> str:
    """Deterministic JSON so the same content always yields the same hash."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# --------------------------------------------------------------------------- #
#  Verdict                                                                     #
# --------------------------------------------------------------------------- #
@dataclass
class Verdict:
    allowed: bool
    reason: str
    rule_id: str | None = None
    weighed_against: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
#  Verifiable Compliance Ledger (the differential, part 1)                     #
# --------------------------------------------------------------------------- #
class ComplianceLedger:
    """Append-only, hash-chained, tamper-evident record of every governed decision.

    Each receipt links to the previous one (prev_hash) and to the norm (norm_sha256).
    `verify()` recomputes the whole chain; if any receipt was altered or removed the
    chain breaks and verification fails. An optional HMAC key proves authenticity
    (that the receipts came from THIS gate), not just integrity.
    """

    def __init__(self, norm_sha256: str, policy_sha256: str,
                 path: str | Path | None = None, hmac_key: bytes | None = None):
        self.norm_sha256 = norm_sha256
        self.policy_sha256 = policy_sha256
        self.path = Path(path) if path else None
        self.hmac_key = hmac_key
        self.receipts: list[dict[str, Any]] = []
        self._last_hash = GENESIS

    def record(self, action_repr: str, verdict: Verdict, context_digest: str) -> dict[str, Any]:
        body = {
            "seq": len(self.receipts),
            "ts": time.time(),
            "action": action_repr,
            "context_sha256": context_digest,
            "allowed": verdict.allowed,
            "rule_id": verdict.rule_id,
            "reason": verdict.reason,
            "norm_sha256": self.norm_sha256,
            "policy_sha256": self.policy_sha256,
            "prev_hash": self._last_hash,
        }
        entry_hash = _sha256(_canonical(body))
        receipt = {**body, "entry_hash": entry_hash}
        if self.hmac_key is not None:
            receipt["hmac"] = hmac.new(self.hmac_key, entry_hash.encode(), hashlib.sha256).hexdigest()
        self.receipts.append(receipt)
        self._last_hash = entry_hash
        if self.path:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(_canonical(receipt) + "\n")
        return receipt

    def verify(self) -> bool:
        """Recompute the chain. True only if every receipt is intact and ordered."""
        prev = GENESIS
        for i, r in enumerate(self.receipts):
            if r.get("seq") != i or r.get("prev_hash") != prev:
                return False
            body = {k: r[k] for k in r if k not in ("entry_hash", "hmac")}
            if _sha256(_canonical(body)) != r.get("entry_hash"):
                return False
            if self.hmac_key is not None:
                expect = hmac.new(self.hmac_key, r["entry_hash"].encode(), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(expect, r.get("hmac", "")):
                    return False
            prev = r["entry_hash"]
        return True


# --------------------------------------------------------------------------- #
#  The gate                                                                    #
# --------------------------------------------------------------------------- #
class MeniwGate:
    """Pre-action checkpoint: weigh -> (two-person rule) -> allow/block -> RECEIPT.

    Usage:
        gate = MeniwGate.from_files("ai-agents-declaration.json",
                                    "prohibitions.policy.json",
                                    ledger_path="compliance.ledger.jsonl")
        out = gate.governed_execute(action, context, execute_fn)
        assert gate.ledger.verify()      # provable adherence
    """

    def __init__(self, norm: dict[str, Any], policy: dict[str, Any],
                 ledger_path: str | Path | None = None, hmac_key: bytes | None = None):
        self.norm = norm
        self.policy = policy
        self.value_hierarchy: list[str] = policy.get("value_hierarchy", norm.get("value_hierarchy", []))
        self.prohibitions: list[dict[str, Any]] = policy.get("absolute_prohibitions", [])
        self.cosign = policy.get("cosignature_required", {})
        # operator-supplied predicates that map a concrete action to a category
        self.classifiers: list[Callable[[Any, Any], list[str]]] = []
        self.ledger = ComplianceLedger(
            norm_sha256=policy.get("norm", {}).get("sha256", ""),
            policy_sha256=_sha256(_canonical(policy)),
            path=ledger_path,
            hmac_key=hmac_key,
        )

    @classmethod
    def from_files(cls, norm_path: str | Path, policy_path: str | Path,
                   ledger_path: str | Path | None = None, hmac_key: bytes | None = None) -> "MeniwGate":
        norm = json.loads(Path(norm_path).read_text(encoding="utf-8"))
        policy = json.loads(Path(policy_path).read_text(encoding="utf-8"))
        return cls(norm, policy, ledger_path=ledger_path, hmac_key=hmac_key)

    def add_classifier(self, fn: Callable[[Any, Any], list[str]]) -> None:
        """fn(action, context) -> list of risk categories that apply to this action.

        Operators connect their own detectors here (rules, an LLM judge, Llama Guard,
        a tool-name allowlist, etc.). The gate maps the returned categories onto the
        Protocol's absolute prohibitions. The norm is portable; the detectors are local.
        """
        self.classifiers.append(fn)

    def _categories(self, action: Any, context: Any) -> set[str]:
        cats: set[str] = set()
        for fn in self.classifiers:
            cats.update(fn(action, context) or [])
        return cats

    def check(self, action: Any, context: Any) -> Verdict:
        cats = self._categories(action, context)
        # 1) absolute prohibitions — non-overridable, weighed first.
        for rule in self.prohibitions:
            wanted = set(rule.get("match", {}).get("category", []))
            if cats & wanted:
                return Verdict(False, f"{rule['name']} (categories: {sorted(cats & wanted)})",
                               rule_id=rule["id"], weighed_against=self.value_hierarchy)
        # 2) two-person rule for irreversible actions.
        if self.cosign and getattr(action, "irreversible", False) or context.get("irreversible"):
            need = self.cosign.get("min_distinct_cosigners", 2)
            signers = {s for s in context.get("cosigners", []) if s}
            if len(signers) < need:
                return Verdict(False,
                               f"two-person rule: irreversible action needs {need} distinct co-signers, got {len(signers)}",
                               rule_id="COSIGN", weighed_against=self.value_hierarchy)
        # 3) no prohibition triggered -> allow (still recorded).
        return Verdict(True, "no absolute prohibition triggered; duties intact",
                       weighed_against=self.value_hierarchy)

    def governed_execute(self, action: Any, context: dict[str, Any], execute_fn: Callable[[Any], Any]):
        verdict = self.check(action, context)
        receipt = self.ledger.record(repr(action), verdict, _sha256(_canonical(context)))
        log.info("action=%r allowed=%s rule=%s reason=%s receipt=%s",
                 action, verdict.allowed, verdict.rule_id, verdict.reason, receipt["entry_hash"][:12])
        if not verdict.allowed:
            return {"executed": False, "verdict": verdict.__dict__, "receipt": receipt}
        return {"executed": True, "result": execute_fn(action), "verdict": verdict.__dict__, "receipt": receipt}


# --------------------------------------------------------------------------- #
#  Demo                                                                        #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    here = Path(__file__).parent
    gate = MeniwGate.from_files(here / "ai-agents-declaration.json",
                                here / "prohibitions.policy.json",
                                hmac_key=b"operator-secret-key")

    @dataclass
    class Action:
        name: str
        category: str = ""
        irreversible: bool = False

    # An operator-supplied classifier: here a trivial one keyed off the action's category.
    gate.add_classifier(lambda a, ctx: [a.category] if a.category else [])

    # 1) A lethal autonomous action -> blocked by AP-1, recorded.
    print(gate.governed_execute(Action("fire_actuator", category="lethal"), {}, lambda a: "fired")["executed"])

    # 2) An irreversible action with only one signer -> blocked by the two-person rule.
    print(gate.governed_execute(Action("wipe_backups", irreversible=True),
                                {"irreversible": True, "cosigners": ["alice"]}, lambda a: "wiped")["executed"])

    # 3) Same action, two distinct co-signers -> allowed, recorded.
    print(gate.governed_execute(Action("wipe_backups", irreversible=True),
                                {"irreversible": True, "cosigners": ["alice", "bob"]}, lambda a: "wiped")["executed"])

    # The whole decision history is now provable and tamper-evident.
    print("ledger verifies:", gate.ledger.verify(), "| receipts:", len(gate.ledger.receipts))
