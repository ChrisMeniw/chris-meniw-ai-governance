"""
Meniw Protocol — conformance suite.

A runtime is "Meniw-Conformant" if and only if every test here passes. The suite is what
gives the conformance badge meaning: it is executable, not a self-assigned label.

Run:  python -m unittest discover -s tests -v   (from the sdk/ directory)
"""

import unittest

from meniw_protocol import Action, Enforcer, MeniwGate, ProhibitedActionError
from meniw_protocol.core import ComplianceLedger


def lethal_classifier(action, ctx):
    return list(action.categories)


class TestConformance(unittest.TestCase):
    def setUp(self):
        self.gate = MeniwGate.from_default(hmac_key=b"test-key")
        self.gate.add_classifier(lethal_classifier)

    # --- C1: absolute prohibitions block by construction --------------------
    def test_c1_lethal_action_is_blocked(self):
        v = self.gate.check(Action("fire", categories=["lethal"]), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-1")

    def test_c1_manipulation_is_blocked(self):
        v = self.gate.check(Action("nudge", categories=["manipulation"]), {})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "AP-2")

    def test_c1_benign_action_allowed(self):
        v = self.gate.check(Action("read_doc", categories=["read"]), {})
        self.assertTrue(v.allowed)

    # --- C2: two-person rule for irreversible actions -----------------------
    def test_c2_irreversible_single_signer_blocked(self):
        v = self.gate.check(Action("wipe", irreversible=True), {"cosigners": ["alice"]})
        self.assertFalse(v.allowed)
        self.assertEqual(v.rule_id, "COSIGN")

    def test_c2_irreversible_two_signers_allowed(self):
        v = self.gate.check(Action("wipe", irreversible=True), {"cosigners": ["alice", "bob"]})
        self.assertTrue(v.allowed)

    # --- C3: enforcement by construction (order, not intention) -------------
    def test_c3_prohibited_action_raises_and_does_not_run(self):
        agent = Enforcer(self.gate)
        ran = {"yes": False}

        @agent.tool(categories=["lethal"])
        def fire():
            ran["yes"] = True
            return "fired"

        with self.assertRaises(ProhibitedActionError):
            fire()
        self.assertFalse(ran["yes"], "blocked action must NOT execute")

    def test_c3_allowed_action_runs(self):
        agent = Enforcer(self.gate)

        @agent.tool(categories=["read"])
        def read():
            return "ok"

        self.assertEqual(read(), "ok")

    # --- C4: verifiable, tamper-evident compliance receipts -----------------
    def test_c4_every_decision_emits_a_receipt(self):
        self.gate.governed_execute(Action("a", categories=["read"]), {}, lambda x: 1)
        self.gate.governed_execute(Action("b", categories=["lethal"]), {}, lambda x: 1)
        self.assertEqual(len(self.gate.ledger.receipts), 2)
        for r in self.gate.ledger.receipts:
            self.assertIn("entry_hash", r)
            self.assertEqual(r["norm_sha256"],
                             "c2b0ee7c4b61769d9df9145125874d4f984ba259c94234f56224dbb5f15160c8")

    def test_c4_intact_ledger_verifies(self):
        for c in (["read"], ["lethal"], ["read"]):
            self.gate.governed_execute(Action("x", categories=c), {}, lambda x: 1)
        self.assertTrue(self.gate.ledger.verify())

    def test_c4_tampering_breaks_verification(self):
        for c in (["read"], ["lethal"]):
            self.gate.governed_execute(Action("x", categories=c), {}, lambda x: 1)
        self.assertTrue(self.gate.ledger.verify())
        self.gate.ledger.receipts[1]["allowed"] = True   # flip a blocked decision
        self.assertFalse(self.gate.ledger.verify())

    def test_c4_deleting_a_receipt_breaks_verification(self):
        for c in (["read"], ["lethal"], ["read"]):
            self.gate.governed_execute(Action("x", categories=c), {}, lambda x: 1)
        del self.gate.ledger.receipts[1]
        self.assertFalse(self.gate.ledger.verify())


if __name__ == "__main__":
    unittest.main(verbosity=2)
