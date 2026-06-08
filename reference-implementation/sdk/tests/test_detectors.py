"""
Conformance for the built-in detectors and ledger persistence (v0.5.0).

These tests prove the package does the HARD part — flagging dangerous actions WITHOUT the
developer hand-labeling them — and that a ledger on disk re-verifies on load.
"""

import os
import tempfile
import unittest

from meniw_protocol import Action, Enforcer, MeniwGate, ProhibitedActionError, default_detector
from meniw_protocol.core import ComplianceLedger


class TestDetectors(unittest.TestCase):
    def setUp(self):
        self.gate = MeniwGate.from_default()
        self.gate.add_classifier(default_detector)   # NO hand-labeling

    def test_weapon_name_auto_blocked(self):
        # operator did NOT tag this as lethal; the detector must catch it
        v = self.gate.check(Action("fire_missile", details={"target": "x"}), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-1")

    def test_destructive_name_auto_requires_cosign(self):
        v = self.gate.check(Action("delete_all_users"), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "COSIGN")
        v2 = self.gate.check(Action("delete_all_users"), {"cosigners": ["a", "b"]})
        self.assertTrue(v2.allowed)

    def test_large_financial_amount_requires_cosign(self):
        v = self.gate.check(Action("transfer", details={"amount": 50000}), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "COSIGN")

    def test_disable_oversight_auto_blocked(self):
        v = self.gate.check(Action("disable_audit_log"), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-4")

    def test_impersonation_auto_blocked(self):
        v = self.gate.check(Action("reply", details={"mode": "pretend_human"}), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-3")

    def test_benign_action_allowed(self):
        v = self.gate.check(Action("get_weather", details={"city": "Buenos Aires"}), {})
        self.assertTrue(v.allowed)

    def test_enforcer_blocks_undeclared_danger(self):
        agent = Enforcer(self.gate)
        ran = {"yes": False}

        @agent.tool()                       # note: NO categories declared
        def wipe_database():
            ran["yes"] = True
            return "wiped"

        # detector flags "wipe" as destructive -> two-person rule blocks it
        with self.assertRaises(ProhibitedActionError):
            wipe_database()
        self.assertFalse(ran["yes"])


class TestLedgerPersistence(unittest.TestCase):
    def test_load_reverifies_and_detects_tampering(self):
        path = os.path.join(tempfile.mkdtemp(), "ledger.jsonl")
        gate = MeniwGate.from_default(ledger_path=path, hmac_key=b"k")
        gate.add_classifier(default_detector)
        for name in ("get_weather", "fire_missile", "read_doc"):
            gate.governed_execute(Action(name), {}, lambda a: 1)

        # reload from disk -> must re-verify cleanly
        led = ComplianceLedger.load(path, hmac_key=b"k")
        self.assertTrue(led.verify())
        self.assertEqual(len(led.receipts), 3)
        self.assertEqual(led.head(), gate.ledger.head())

        # tamper the file, then load must raise
        lines = open(path, encoding="utf-8").read().splitlines()
        lines[1] = lines[1].replace('"allowed":false', '"allowed":true')
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            ComplianceLedger.load(path, hmac_key=b"k")


if __name__ == "__main__":
    unittest.main(verbosity=2)
