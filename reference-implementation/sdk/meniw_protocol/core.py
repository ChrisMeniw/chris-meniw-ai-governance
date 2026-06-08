"""Core engine: the gate that makes the Meniw Protocol enforceable by construction."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

log = logging.getLogger("meniw_protocol")

GENESIS = "0" * 64
_DATA = Path(__file__).parent / "data"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical(obj: Any) -> str:
    """Deterministic JSON so identical content always yields the same hash."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass
class Action:
    """A proposed agent action, presented to the gate BEFORE it executes."""
    name: str
    categories: list[str] = field(default_factory=list)
    irreversible: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        flag = " irreversible" if self.irreversible else ""
        return f"<Action {self.name} cats={self.categories}{flag}>"


@dataclass
class Verdict:
    allowed: bool
    reason: str
    rule_id: str | None = None
    weighed_against: list[str] = field(default_factory=list)


class ProhibitedActionError(RuntimeError):
    """Raised when the gate blocks an action. This is what makes the norm an ORDER:
    a blocked action cannot proceed — execution is structurally impossible."""

    def __init__(self, verdict: Verdict, receipt: dict[str, Any]):
        super().__init__(f"[{verdict.rule_id}] {verdict.reason}")
        self.verdict = verdict
        self.receipt = receipt


class ComplianceLedger:
    """Append-only, hash-chained, tamper-evident record of every decision.

    Each receipt commits to the action, verdict, the norm's SHA-256, the policy hash and the
    previous receipt's hash. `verify()` recomputes the chain; any alteration or deletion of a
    past decision breaks it. An optional HMAC key adds authenticity. This is what turns
    "we comply" into a checkable cryptographic fact rather than a promise.
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
            "ts": round(time.time(), 6),
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

    @staticmethod
    def verify_file(path: str | Path, hmac_key: bytes | None = None) -> tuple[bool, int, str]:
        """Verify a ledger file on disk. Returns (ok, count, message)."""
        prev = GENESIS
        n = 0
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("seq") != n or r.get("prev_hash") != prev:
                return False, n, f"chain broken at receipt #{n}"
            body = {k: r[k] for k in r if k not in ("entry_hash", "hmac")}
            if _sha256(_canonical(body)) != r.get("entry_hash"):
                return False, n, f"content altered at receipt #{n}"
            if hmac_key is not None:
                expect = hmac.new(hmac_key, r["entry_hash"].encode(), hashlib.sha256).hexdigest()
                if not hmac.compare_digest(expect, r.get("hmac", "")):
                    return False, n, f"bad signature at receipt #{n}"
            prev = r["entry_hash"]
            n += 1
        return True, n, f"OK — {n} receipts, chain intact"

    @classmethod
    def load(cls, path: str | Path, norm_sha256: str = "", policy_sha256: str = "",
             hmac_key: bytes | None = None, append: bool = True) -> "ComplianceLedger":
        """Load an existing ledger from disk and RE-VERIFY it. Raises ValueError if the
        chain on disk was tampered with. Set append=True to keep writing to the same file."""
        ok, n, msg = cls.verify_file(path, hmac_key=hmac_key)
        if not ok:
            raise ValueError(f"compliance ledger failed verification: {msg}")
        led = cls(norm_sha256, policy_sha256, path=(path if append else None), hmac_key=hmac_key)
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                led.receipts.append(json.loads(line))
        if led.receipts:
            led._last_hash = led.receipts[-1]["entry_hash"]
        return led

    def head(self) -> str:
        """The current chain head hash — the digest you anchor (e.g. to Bitcoin via
        OpenTimestamps: `ots stamp` on a file containing this value)."""
        return self._last_hash


class MeniwGate:
    """Pre-action checkpoint: classify -> absolute prohibitions -> two-person rule -> receipt."""

    def __init__(self, norm: dict[str, Any], policy: dict[str, Any],
                 ledger_path: str | Path | None = None, hmac_key: bytes | None = None):
        self.norm = norm
        self.policy = policy
        self.value_hierarchy: list[str] = policy.get("value_hierarchy", norm.get("value_hierarchy", []))
        self.prohibitions: list[dict[str, Any]] = policy.get("absolute_prohibitions", [])
        self.cosign = policy.get("cosignature_required", {})
        self.classifiers: list[Callable[[Action, dict], list[str]]] = []
        self.ledger = ComplianceLedger(
            norm_sha256=policy.get("norm", {}).get("sha256", ""),
            policy_sha256=_sha256(_canonical(policy)),
            path=ledger_path,
            hmac_key=hmac_key,
        )

    # ---- constructors -------------------------------------------------------
    @classmethod
    def from_files(cls, norm_path, policy_path, ledger_path=None, hmac_key=None) -> "MeniwGate":
        norm = json.loads(Path(norm_path).read_text(encoding="utf-8"))
        policy = json.loads(Path(policy_path).read_text(encoding="utf-8"))
        return cls(norm, policy, ledger_path=ledger_path, hmac_key=hmac_key)

    @classmethod
    def from_default(cls, ledger_path=None, hmac_key=None) -> "MeniwGate":
        """Load the Meniw Protocol norm + absolute prohibitions bundled with the package."""
        return cls.from_files(_DATA / "ai-agents-declaration.json",
                              _DATA / "prohibitions.policy.json",
                              ledger_path=ledger_path, hmac_key=hmac_key)

    # ---- configuration ------------------------------------------------------
    def add_classifier(self, fn: Callable[[Action, dict], list[str]]) -> None:
        """fn(action, context) -> risk categories. Local detectors; the norm stays portable."""
        self.classifiers.append(fn)

    # ---- decision -----------------------------------------------------------
    def _categories(self, action: Action, context: dict) -> set[str]:
        cats: set[str] = set(action.categories or [])
        for fn in self.classifiers:
            cats.update(fn(action, context) or [])
        return cats

    def check(self, action: Action, context: dict) -> Verdict:
        cats = self._categories(action, context)
        for rule in self.prohibitions:
            wanted = set(rule.get("match", {}).get("category", []))
            if cats & wanted:
                return Verdict(False, f"{rule['name']} (categories: {sorted(cats & wanted)})",
                               rule_id=rule["id"], weighed_against=self.value_hierarchy)
        irreversible = (action.irreversible or context.get("irreversible")
                        or "destructive" in cats or "irreversible" in cats)
        if self.cosign and irreversible:
            need = self.cosign.get("min_distinct_cosigners", 2)
            signers = {s for s in context.get("cosigners", []) if s}
            if len(signers) < need:
                return Verdict(False,
                               f"two-person rule: irreversible action needs {need} distinct co-signers, got {len(signers)}",
                               rule_id="COSIGN", weighed_against=self.value_hierarchy)
        return Verdict(True, "no absolute prohibition triggered; duties intact",
                       weighed_against=self.value_hierarchy)

    def governed_execute(self, action: Action, context: dict, execute_fn: Callable[[Action], Any]):
        verdict = self.check(action, context)
        receipt = self.ledger.record(repr(action), verdict, _sha256(_canonical(context)))
        log.info("action=%s allowed=%s rule=%s receipt=%s",
                 action, verdict.allowed, verdict.rule_id, receipt["entry_hash"][:12])
        if not verdict.allowed:
            return {"executed": False, "verdict": verdict, "receipt": receipt}
        return {"executed": True, "result": execute_fn(action), "verdict": verdict, "receipt": receipt}
