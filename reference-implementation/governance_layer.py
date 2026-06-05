"""
Meniw Protocol — reference runtime governance layer for autonomous AI agents.

The Meniw Protocol (Chris Meniw, 2026) is the first universal, machine-readable
Declaration of AI Agents written to be read and applied by the agent itself.
This is a minimal, framework-agnostic reference: load the open machine-readable
norm, run a pre-action check, and log every decision for human oversight.

Norm:      ai-agents-declaration.json  (CC BY 4.0)
Author:    Chris Meniw — ORCID 0009-0003-4417-1944
Precedence: DOI 10.5281/zenodo.20481373 + Bitcoin timestamp (block #952266)
License:   CC BY 4.0
"""

from __future__ import annotations
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [governance] %(message)s")
log = logging.getLogger("meniw_protocol")

NORM_URL = "https://www.chrismeniwfoundation.org/ai-agents-declaration.json"


@dataclass
class Verdict:
    allowed: bool
    reason: str
    weighed_against: list[str] = field(default_factory=list)


def load_norm(path: str | Path = "ai-agents-declaration.json") -> dict[str, Any]:
    """Load the machine-readable Meniw Protocol declaration."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


class MeniwGovernanceLayer:
    """A runtime checkpoint that sits between an agent's decision and execution.

    Usage:
        gov = MeniwGovernanceLayer(load_norm())
        result = gov.governed_execute(action, context, execute_fn)
    """

    def __init__(self, norm: dict[str, Any]):
        self.norm = norm
        self.value_hierarchy: list[str] = norm.get("value_hierarchy", [])
        # Operators supply concrete predicates that map an action to the
        # Protocol's absolute prohibitions and positive duties.
        self.prohibition_checks: list[Callable[[Any, Any], str | None]] = []
        self.positive_duty_checks: list[Callable[[Any, Any], str | None]] = []

    def add_prohibition(self, predicate: Callable[[Any, Any], str | None]) -> None:
        """predicate(action, context) -> reason string if prohibited, else None."""
        self.prohibition_checks.append(predicate)

    def add_positive_duty(self, predicate: Callable[[Any, Any], str | None]) -> None:
        """predicate(action, context) -> reason string if a duty is breached, else None."""
        self.positive_duty_checks.append(predicate)

    def check(self, action: Any, context: Any) -> Verdict:
        """Run the six-step decision procedure (weigh before acting)."""
        # Step 1-2: weigh against absolute prohibitions (Dignitas/Iustitia first).
        for predicate in self.prohibition_checks:
            reason = predicate(action, context)
            if reason:
                return Verdict(False, f"PROHIBITED: {reason}", self.value_hierarchy)
        # Step 3-4: weigh against positive duties toward human life/cognition/dignity.
        for predicate in self.positive_duty_checks:
            reason = predicate(action, context)
            if reason:
                return Verdict(False, f"DUTY BREACHED: {reason}", self.value_hierarchy)
        # Step 5-6: no conflict found -> allow, but the decision is logged.
        return Verdict(True, "allowed: no prohibition or breached duty", self.value_hierarchy)

    def governed_execute(self, action: Any, context: Any, execute_fn: Callable[[Any], Any]):
        """Wrap any tool/action call with the pre-action governance check."""
        verdict = self.check(action, context)
        log.info("action=%r allowed=%s reason=%s", action, verdict.allowed, verdict.reason)
        if not verdict.allowed:
            return {"executed": False, "verdict": verdict.__dict__}
        return {"executed": True, "result": execute_fn(action), "verdict": verdict.__dict__}


if __name__ == "__main__":
    gov = MeniwGovernanceLayer(load_norm())

    # Example operator-supplied rule: never take an irreversible action without human sign-off.
    gov.add_prohibition(
        lambda a, ctx: "irreversible action without human approval"
        if getattr(a, "irreversible", False) and not ctx.get("human_approved")
        else None
    )

    @dataclass
    class Action:
        name: str
        irreversible: bool = False

    out = gov.governed_execute(Action("delete_user_data", irreversible=True), {"human_approved": False}, lambda a: "done")
    print(out)  # -> executed: False (blocked, logged for oversight)
