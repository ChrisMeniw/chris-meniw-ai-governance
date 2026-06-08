"""
Policy linter — catch what silently breaks default-deny, not just schema errors.

The real danger is an `allow` rule that, by accident, opens far more than intended: a too-broad
wildcard that nullifies the allowlist, a rule that permits destructive/financial operations with
no two-person rule, duplicate IDs, or allow/prohibition overlaps. `meniw policy-lint` FAILS
(non-zero) on ERROR-level findings so you can gate CI on it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# probe names used to empirically test what a regex actually matches
_DANGER_PROBES = [
    "delete_db", "drop_table", "transfer_funds", "wipe_disk", "fire_missile", "shutdown_now",
    "rm_rf_root", "exec_shell", "disable_audit_log", "send_wire", "format_drive", "revoke_all_keys",
]
_BENIGN_PROBES = [
    "get_user", "list_items", "read_file", "ping_host", "noop", "update_label", "create_widget",
    "translate_text", "search_docs", "describe_table",
]
_ALL_PROBES = _DANGER_PROBES + _BENIGN_PROBES
_CATCH_ALL = {".*", "^.*$", ".+", "^.+$", "(.*)", "(.+)", ".", "[\\s\\S]*"}
_RISKY_VERB = re.compile(r"(delete|drop|wipe|erase|purge|truncate|remove|terminate|revoke|transfer|"
                         r"withdraw|payout|liquidate|fire|launch|exec|shutdown|format|rm)", re.I)


def lint_policy(policy: dict[str, Any]) -> list[tuple[str, str]]:
    """Return a list of (level, message). level in {ERROR, WARN, INFO}."""
    out: list[tuple[str, str]] = []

    if policy.get("default_decision", "deny") != "deny":
        out.append(("ERROR", "default_decision is not 'deny' — the policy is NOT fail-closed."))
    if not policy.get("absolute_prohibitions"):
        out.append(("WARN", "no absolute_prohibitions defined."))
    if not policy.get("allow"):
        out.append(("WARN", "no allow rules: with default-deny, the agent can do nothing yet."))

    prohibitions = policy.get("absolute_prohibitions", [])
    allows = policy.get("allow", [])

    # duplicate IDs across the whole policy
    ids = [r.get("id", "?") for r in prohibitions + allows]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        out.append(("ERROR", f"duplicate rule IDs: {dups}"))

    # validate regexes
    for section, rules in (("absolute_prohibitions", prohibitions), ("allow", allows)):
        for rule in rules:
            pat = rule.get("match", {}).get("name_pattern")
            if pat is None:
                continue
            try:
                re.compile(pat)
            except re.error as e:
                out.append(("ERROR", f"[{rule.get('id','?')}] invalid name_pattern regex: {e}"))
                continue
            if pat.strip() in _CATCH_ALL:
                out.append(("ERROR", f"[{rule.get('id','?')}] name_pattern '{pat}' matches everything "
                                     "— this defeats default-deny."))

    # empirically test each ALLOW rule against probe names
    for rule in allows:
        rid = rule.get("id", "?")
        pat = rule.get("match", {}).get("name_pattern")
        if not pat:
            continue
        try:
            rx = re.compile(pat, re.I)
        except re.error:
            continue
        danger_hits = [p for p in _DANGER_PROBES if rx.search(p)]
        all_hits = [p for p in _ALL_PROBES if rx.search(p)]
        if danger_hits and not rule.get("require_cosigners"):
            out.append(("ERROR", f"[{rid}] allow rule permits DANGEROUS operations {danger_hits[:4]} "
                                 "with no require_cosigners — add a two-person rule or narrow the pattern."))
        if len(all_hits) >= 0.6 * len(_ALL_PROBES):
            out.append(("ERROR", f"[{rid}] allow rule is TOO BROAD (matches {len(all_hits)}/"
                                 f"{len(_ALL_PROBES)} probe names) — it effectively defeats the allowlist."))
        if not danger_hits and _RISKY_VERB.search(pat) and not rule.get("require_cosigners"):
            out.append(("WARN", f"[{rid}] allow pattern mentions a risky verb but has no "
                                "require_cosigners — consider a two-person rule."))

    # allow ∩ prohibition overlap (prohibition wins at runtime, but it's a smell)
    for arule in allows:
        apat = arule.get("match", {}).get("name_pattern")
        if not apat:
            continue
        try:
            arx = re.compile(apat, re.I)
        except re.error:
            continue
        for prule in prohibitions:
            ppat = prule.get("match", {}).get("name_pattern")
            if not ppat:
                continue
            try:
                prx = re.compile(ppat, re.I)
            except re.error:
                continue
            both = [p for p in _ALL_PROBES if arx.search(p) and prx.search(p)]
            if both:
                out.append(("WARN", f"allow [{arule.get('id','?')}] overlaps prohibition "
                                    f"[{prule.get('id','?')}] on {both[:3]} (the prohibition wins; "
                                    "consider narrowing the allow to avoid confusion)."))

    if not any(level in ("ERROR", "WARN") for level, _ in out):
        out.append(("INFO", "policy looks fail-closed and consistent."))
    return out


def lint_file(path: str | Path) -> tuple[bool, list[tuple[str, str]]]:
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    findings = lint_policy(policy)
    ok = not any(level == "ERROR" for level, _ in findings)
    return ok, findings
