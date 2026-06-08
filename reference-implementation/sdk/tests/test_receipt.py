"""
Third-party-verifiable receipt bundle (the real differentiator).

Proves: a valid bundle verifies WITHOUT access to the originating system; an altered field fails;
a removed link fails; and the policy hash in the receipts binds them to the exact policy version.
"""

import json
import os
import tempfile
import unittest

from meniw_protocol import Action, MeniwGate
from meniw_protocol import receipt as R


class TestReceiptBundle(unittest.TestCase):
    def _make_ledger(self):
        d = tempfile.mkdtemp()
        ledger = os.path.join(d, "ledger.jsonl")
        gate = MeniwGate.from_default(ledger_path=ledger)
        for name in ("get_user", "delete_db", "list_items", "send_email"):
            gate.governed_execute(Action(name), {}, lambda a: 1)
        return d, ledger, gate

    def test_valid_bundle_verifies_standalone(self):
        d, ledger, gate = self._make_ledger()
        bundle = os.path.join(d, "bundle.json")
        R.export(ledger, bundle, policy=gate.policy)
        # verify with ONLY the bundle file — no gate, no ledger, no DB
        res = R.verify_bundle(bundle)
        self.assertTrue(res["ok"])
        self.assertTrue(res["chain_ok"])
        self.assertTrue(res["single_policy"])
        self.assertTrue(res["policy_hash_matches"])
        self.assertEqual(res["receipts"], 4)

    def test_altered_field_fails(self):
        d, ledger, gate = self._make_ledger()
        bundle = os.path.join(d, "bundle.json")
        R.export(ledger, bundle, policy=gate.policy)
        data = json.loads(open(bundle, encoding="utf-8").read())
        data["receipts"][1]["allowed"] = True            # flip a blocked decision
        open(bundle, "w", encoding="utf-8").write(json.dumps(data))
        self.assertFalse(R.verify_bundle(bundle)["ok"])

    def test_removed_link_fails(self):
        d, ledger, gate = self._make_ledger()
        bundle = os.path.join(d, "bundle.json")
        R.export(ledger, bundle, policy=gate.policy)
        data = json.loads(open(bundle, encoding="utf-8").read())
        del data["receipts"][1]                          # remove a link from the chain
        open(bundle, "w", encoding="utf-8").write(json.dumps(data))
        self.assertFalse(R.verify_bundle(bundle)["ok"])

    def test_tampered_policy_text_fails_binding(self):
        d, ledger, gate = self._make_ledger()
        bundle = os.path.join(d, "bundle.json")
        R.export(ledger, bundle, policy=gate.policy)
        data = json.loads(open(bundle, encoding="utf-8").read())
        data["policy"]["allow"].append({"id": "SNEAKY", "match": {"name_pattern": ".*"}})
        open(bundle, "w", encoding="utf-8").write(json.dumps(data))
        res = R.verify_bundle(bundle)
        # the embedded policy no longer hashes to what the receipts were decided under
        self.assertFalse(res["policy_hash_matches"])
        self.assertFalse(res["ok"])

    def test_range_export_verifies(self):
        d, ledger, gate = self._make_ledger()
        bundle = os.path.join(d, "range.json")
        R.export(ledger, bundle, policy=gate.policy, start=1, end=3)
        res = R.verify_bundle(bundle)
        self.assertTrue(res["ok"])
        self.assertEqual(res["receipts"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
