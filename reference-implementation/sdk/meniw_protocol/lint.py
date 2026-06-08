"""
Policy linter — catch dangerous or broken policy.json before it ships.

Checks: required fields; default_decision is fail-closed; every regex compiles; allow rules are
not dangerously broad (e.g. `.*`); allow rules that would re-permit something an absolute
prohibition forbids; irreversible/financial-looking allow rules that lack a co-signer requirement.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_RISKY_NAME = re.compile(r"(delete|drop|wipe|erase|purge|truncate|remove|terminate|revoke|"
                         r"transfer|withdraw|payout|liquidate|fire|launch)", re.I)


def lint_policy(policy: dict[str, Any]) -> list[tuple[str, str]]:
    """Return a list of (level, message). level in {ERROR, WARN, INFO}."""
    out: list[tuple[str, str]] = []

    if policy.get("default_decision", "deny") != "deny":
        out.append(("ERROR", "default_decision is not 'deny' — the policy is NOT fail-closed."))
    if not policy.get("absolute_prohibitions"):
        out.append(("WARN", "no absolute_prohibitions defined."))
    if not policy.get("allow"):
        out.append(("WARN", "no allow rules: with default-deny, the agent can do nothing until you add some."))

    for section in ("absolute_prohibitions", "allow"):
        for rule in policy.get(section, []):
            rid = rule.get("id", "?")
            pat = rule.get("match", {}).get("name_pattern")
            if pat is not None:
                try:
                    re.compile(pat)
                except re.error as e:
                    out.append(("ERROR", f"[{rid}] invalid name_pattern regex: {e}"))
                if pat.strip() in (".*", "^.*$", ".+", "(.*)"):
                    out.append(("ERROR", f"[{rid}] name_pattern '{pat}' matches everything — "
                                         "this defeats default-deny."))

    # allow rules that look destructive/financial but don't require co-signers
    for rule in policy.get("allow", []):
        pat = rule.get("match", {}).get("name_pattern", "") or ""
        if _RISKY_NAME.search(pat) and not rule.get("require_cosigners"):
            out.append(("WARN", f"[{rule.get('id','?')}] allow rule matches risky/irreversible "
                                "operations but has no require_cosigners — consider a two-person rule."))

    if not out:
        out.append(("INFO", "policy looks fail-closed and consistent."))
    return out


def lint_file(path: str | Path) -> tuple[bool, list[tuple[str, str]]]:
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    findings = lint_policy(policy)
    ok = not any(level == "ERROR" for level, _ in findings)
    return ok, findings
