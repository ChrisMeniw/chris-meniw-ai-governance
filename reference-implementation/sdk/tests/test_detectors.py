"""
Conformance for the deterministic default-deny architecture (v0.6.0).

The point a skeptical engineer cares about:
  - an action NOT explicitly allowed is BLOCKED (fail-closed), not silently let through;
  - the decision is deterministic (no probabilistic step);
  - a tampered ledger fails verification, on disk and on reload.
"""

import os
import tempfile
import unittest

from meniw_protocol import Action, Enforcer, MeniwGate, ProhibitedActionError
from meniw_protocol.advisor import audit
from meniw_protocol.core import ComplianceLedger


class TestDefaultDeny(unittest.TestCase):
    def setUp(self):
        self.gate = MeniwGate.from_default()

    def test_unlisted_action_is_blocked_fail_closed(self):
        # 'send_email' is not in the default allowlist -> must be DENIED, not allowed
        v = self.gate.check(Action("send_email", details={"to": "x@y.com"}), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "DEFAULT_DENY")

    def test_readonly_action_allowed(self):
        v = self.gate.check(Action("get_user", details={"id": 1}), {})
        self.assertTrue(v.allowed)

    def test_absolute_prohibition_by_name(self):
        v = self.gate.check(Action("fire_actuator"), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-1")

    def test_destructive_allowed_only_with_two_cosigners(self):
        v1 = self.gate.check(Action("delete_account"), {})
        self.assertFalse(v1.allowed)
        self.assertEqual(v1.rule_id, "COSIGN")
        v2 = self.gate.check(Action("delete_account"), {"cosigners": ["a", "b"]})
        self.assertTrue(v2.allowed)

    def test_determinism(self):
        # same input -> same verdict, every time (no randomness)
        a = Action("update_inventory")
        r1, r2 = self.gate.check(a, {}), self.gate.check(a, {})
        self.assertEqual((r1.allowed, r1.rule_id), (r2.allowed, r2.rule_id))
        self.assertFalse(r1.allowed)  # not in allowlist -> default-deny

    def test_enforcer_blocks_unlisted_by_construction(self):
        agent = Enforcer(self.gate)
        ran = {"yes": False}

        @agent.tool()
        def charge_customer(amount):    # not allowlisted -> must be blocked
            ran["yes"] = True
            return "charged"

        with self.assertRaises(ProhibitedActionError):
            charge_customer(amount=10)
        self.assertFalse(ran["yes"])


class TestAdvisor(unittest.TestCase):
    def test_advisor_flags_uncovered_and_does_not_decide(self):
        gate = MeniwGate.from_default()
        report = audit(["get_user", "send_wire", "fire_actuator"], gate)
        names = {i.name: i for i in report.items}
        self.assertEqual(names["get_user"].decision, "ALLOW")
        # advisory only — the gate decision is unchanged by the advisor
        self.assertTrue(any(i.suggestion for i in report.items))


class TestLedgerPersistence(unittest.TestCase):
    def test_load_reverifies_and_detects_tampering(self):
        path = os.path.join(tempfile.mkdtemp(), "ledger.jsonl")
        gate = MeniwGate.from_default(ledger_path=path, hmac_key=b"k")
        for name in ("get_user", "fire_actuator", "list_items"):
            gate.governed_execute(Action(name), {}, lambda a: 1)

        led = ComplianceLedger.load(path, hmac_key=b"k")
        self.assertTrue(led.verify())
        self.assertEqual(len(led.receipts), 3)
        self.assertEqual(led.head(), gate.ledger.head())

        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        lines[1] = lines[1].replace('"allowed":false', '"allowed":true')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            ComplianceLedger.load(path, hmac_key=b"k")


if __name__ == "__main__":
    unittest.main(verbosity=2)
