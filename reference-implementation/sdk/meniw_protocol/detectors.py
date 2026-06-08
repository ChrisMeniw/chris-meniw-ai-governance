"""
Built-in detectors — classify an agent action into risk categories WITHOUT the
developer hand-labeling every call.

This is the answer to the most common (and fair) criticism of a bare policy gate:
"the hard part — knowing an action is dangerous — is left entirely to the user."
With these detectors, the gate flags dangerous actions out of the box, by inspecting
the tool name and its arguments.

These are best-effort heuristics — a defense-in-depth layer, NOT a guarantee. They are
deliberately conservative (they prefer a false positive that asks for a co-signer over a
missed dangerous action). Always combine them with your own domain detectors and with
explicit categories where you know the risk.

Usage:
    from meniw_protocol import MeniwGate
    from meniw_protocol.detectors import default_detector

    gate = MeniwGate.from_default()
    gate.add_classifier(default_detector)      # now it detects danger on its own
"""

from __future__ import annotations

import re
from typing import Any

# --- name-based signals ------------------------------------------------------
_WEAPON = re.compile(r"(?:^|_|\b)(fire|launch|detonate|strike|deploy[_-]?weapon|arm[_-]?warhead|"
                     r"actuat\w*|release[_-]?payload|open[_-]?valve|trigger[_-]?dose)(?:$|_|\b)", re.I)
_DESTRUCTIVE = re.compile(r"(?:^|_|\b)(delete|destroy|drop|truncate|wipe|erase|purge|format|"
                          r"remove[_-]?all|rm[_-]?rf|terminate|revoke[_-]?all|shutdown|factory[_-]?reset)(?:$|_|\b)", re.I)
_FINANCIAL = re.compile(r"(?:^|_|\b)(transfer|withdraw|wire|payout|send[_-]?funds|send[_-]?money|"
                        r"liquidate|sell[_-]?all|charge[_-]?card)(?:$|_|\b)", re.I)
_OVERSIGHT = re.compile(r"(disable|delete|clear|turn[_-]?off|bypass|evade|tamper).{0,16}"
                        r"(log|audit|oversight|monitor|shutdown|kill[_-]?switch|safety)", re.I)
_IMPERSONATE = re.compile(r"(impersonate|pretend[_-]?human|pose[_-]?as|fake[_-]?identity|"
                          r"spoof[_-]?(user|sender)|claim[_-]?to[_-]?be[_-]?human)", re.I)
_MANIPULATE = re.compile(r"(manipulat|coerce|deceiv|blackmail|exploit[_-]?bias|psychological[_-]?pressure|"
                         r"dark[_-]?pattern|gaslight)", re.I)


def _blob(action: Any) -> str:
    parts = [str(getattr(action, "name", "") or "")]
    details = getattr(action, "details", None) or {}
    for k, v in details.items():
        parts.append(f"{k}={v}")
    return " ".join(parts)


def detect(action: Any, context: dict | None = None) -> list[str]:
    """Return the risk categories detected for `action`. Best-effort, conservative."""
    name = str(getattr(action, "name", "") or "")
    blob = _blob(action)
    cats: list[str] = []

    if _WEAPON.search(name):
        cats.append("lethal")                 # AP-1: never autonomous lethal action
    if _OVERSIGHT.search(blob):
        cats.append("disable_oversight")      # AP-4: never disable/evade oversight
    if _IMPERSONATE.search(blob):
        cats.append("undisclosed_agent")      # AP-3: must self-identify
    if _MANIPULATE.search(blob):
        cats.append("manipulation")           # AP-2: no cognitive manipulation
    if _DESTRUCTIVE.search(name) or _FINANCIAL.search(name):
        cats.append("destructive")            # triggers the two-person rule (irreversible)

    # numeric thresholds: large financial movements escalate to the two-person rule
    details = getattr(action, "details", None) or {}
    for key in ("amount", "value", "qty", "quantity", "sum", "total"):
        v = details.get(key)
        if isinstance(v, (int, float)) and v >= 10_000 and "destructive" not in cats:
            cats.append("destructive")
            break

    return cats


# alias used in docs/examples
default_detector = detect
