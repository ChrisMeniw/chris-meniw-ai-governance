"""
Advisor — DEVELOPMENT-TIME help to build your policy. It never decides a runtime block.

The runtime gate is deterministic and fail-closed (default-deny): what is not explicitly
allowed is blocked. That is the part that survives an audit. Heuristics are useful only to
*help you write the policy* — they flag actions that look dangerous and are not yet covered,
so you don't ship a tool that silently sits in default-deny (or, worse, that you allow without
a two-person rule). Run this in dev / CI, read the suggestions, edit policy.json. Done.

    from meniw_protocol import MeniwGate
    from meniw_protocol.advisor import audit

    gate = MeniwGate.from_default()
    report = audit(["get_user", "delete_account", "send_wire", "fire_actuator"], gate)
    print(report.text())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .core import Action, MeniwGate
from .detectors import detect  # heuristics — advisory use ONLY


@dataclass
class AdviceItem:
    name: str
    decision: str                 # ALLOW / DENY / COSIGN-REQUIRED / DEFAULT-DENY
    rule_id: str | None
    heuristic_flags: list[str] = field(default_factory=list)
    suggestion: str = ""


@dataclass
class AuditReport:
    items: list[AdviceItem] = field(default_factory=list)

    def needs_attention(self) -> list[AdviceItem]:
        return [i for i in self.items if i.suggestion]

    def text(self) -> str:
        lines = ["Meniw policy audit (dev-time advice; runtime stays default-deny):"]
        for i in self.items:
            tag = f"[{i.decision}]"
            extra = f"  ⚠ {i.suggestion}" if i.suggestion else ""
            flags = f"  (looks like: {', '.join(i.heuristic_flags)})" if i.heuristic_flags else ""
            lines.append(f"  {tag:16s} {i.name}{flags}{extra}")
        return "\n".join(lines)


def audit(tool_names: list[str], gate: MeniwGate, sample_args: dict[str, dict] | None = None) -> AuditReport:
    """Simulate each tool name against the policy and suggest fixes. No side effects."""
    sample_args = sample_args or {}
    report = AuditReport()
    for name in tool_names:
        action = Action(name=name, details=sample_args.get(name, {}))
        verdict = gate.check(action, {})            # uses the real deterministic policy
        flags = detect(action, {})                  # heuristic, advisory only
        decision = ("ALLOW" if verdict.allowed
                    else "DEFAULT-DENY" if verdict.rule_id == "DEFAULT_DENY"
                    else "COSIGN-REQUIRED" if verdict.rule_id == "COSIGN"
                    else "DENY")
        risky = any(f in flags for f in ("lethal", "destructive", "disable_oversight",
                                         "manipulation", "undisclosed_agent"))
        suggestion = ""
        if verdict.allowed and risky:
            suggestion = ("ALLOWED but looks risky — add an absolute_prohibition or a "
                          "require_cosigners rule so it isn't permitted unconditionally.")
        elif decision == "DEFAULT-DENY" and risky:
            suggestion = (f"blocked by default-deny and looks risky ({', '.join(flags)}); if you "
                          "intend to expose it, add an allow rule WITH require_cosigners.")
        elif decision == "DEFAULT-DENY":
            suggestion = "blocked by default-deny — add an allow rule if this tool is safe and expected."
        report.items.append(AdviceItem(name, decision, verdict.rule_id, flags, suggestion))
    return report
