"""Tests for v0.7.0 hardening: auto-anchoring, policy lint, thread-safe ledger, CLI."""

import json
import os
import tempfile
import threading
import unittest

from meniw_protocol import Action, MeniwGate
from meniw_protocol import anchor as anchor_mod
from meniw_protocol.lint import lint_policy
from meniw_protocol.core import ComplianceLedger


class TestLocalCheckpointOnly(unittest.TestCase):
    def test_checkpoint_is_local_and_never_stamps_in_gate(self):
        d = tempfile.mkdtemp()
        gate = MeniwGate.from_default(checkpoint_dir=d, checkpoint_every=2)
        for name in ("get_a", "get_b", "get_c", "get_d"):
            gate.governed_execute(Action(name), {}, lambda a: 1)
        log = os.path.join(d, "anchors.log.jsonl")
        lines = [json.loads(l) for l in open(log, encoding="utf-8").read().splitlines() if l.strip()]
        self.assertEqual(len(lines), 2)                       # local snapshot every 2 receipts
        # the gate NEVER stamps / touches the network: status is a pure local checkpoint
        self.assertTrue(all(r["status"] == "checkpointed" for r in lines))

    def test_checkpointing_never_crashes_the_agent(self):
        gate = MeniwGate.from_default(checkpoint_dir="/this/does/not/exist/\x00", checkpoint_every=1)
        out = gate.governed_execute(Action("get_x"), {}, lambda a: "ok")
        self.assertTrue(out["executed"])


class TestPolicyLint(unittest.TestCase):
    def test_flags_non_failclosed(self):
        findings = lint_policy({"default_decision": "allow", "allow": [], "absolute_prohibitions": []})
        self.assertTrue(any(level == "ERROR" and "fail-closed" in msg for level, msg in findings))

    def test_flags_catch_all_allow(self):
        findings = lint_policy({"default_decision": "deny",
                                "absolute_prohibitions": [{"id": "AP-1", "match": {"category": ["lethal"]}}],
                                "allow": [{"id": "A", "match": {"name_pattern": ".*"}}]})
        self.assertTrue(any(level == "ERROR" and "everything" in msg for level, msg in findings))

    def test_flags_risky_allow_without_cosign(self):
        findings = lint_policy({"default_decision": "deny",
                                "absolute_prohibitions": [{"id": "AP-1", "match": {"category": ["lethal"]}}],
                                "allow": [{"id": "A", "match": {"name_pattern": "delete_user"}}]})
        self.assertTrue(any(level == "WARN" and "require_cosigners" in msg for level, msg in findings))

    def test_flags_duplicate_ids(self):
        findings = lint_policy({"default_decision": "deny",
                                "absolute_prohibitions": [{"id": "X", "match": {"category": ["lethal"]}}],
                                "allow": [{"id": "X", "match": {"name_pattern": "^get_"}}]})
        self.assertTrue(any(level == "ERROR" and "duplicate rule IDs" in msg for level, msg in findings))

    def test_flags_dangerous_allow_without_cosign(self):
        # an allow rule that empirically permits destructive ops without a two-person rule
        findings = lint_policy({"default_decision": "deny",
                                "absolute_prohibitions": [],
                                "allow": [{"id": "A", "match": {"name_pattern": "(delete|transfer|wipe)"}}]})
        self.assertTrue(any(level == "ERROR" and "DANGEROUS" in msg for level, msg in findings))

    def test_default_bundled_policy_is_clean(self):
        gate = MeniwGate.from_default()
        findings = lint_policy(gate.policy)
        self.assertFalse(any(level == "ERROR" for level, _ in findings))


class TestThreadSafeLedger(unittest.TestCase):
    def test_concurrent_records_keep_chain_intact(self):
        path = os.path.join(tempfile.mkdtemp(), "ledger.jsonl")
        gate = MeniwGate.from_default(ledger_path=path)

        def worker(i):
            for j in range(20):
                gate.governed_execute(Action(f"get_{i}_{j}"), {}, lambda a: 1)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(gate.ledger.receipts), 100)
        self.assertTrue(gate.ledger.verify())                 # in-memory chain intact
        ok, n, _ = ComplianceLedger.verify_file(path)          # on-disk chain intact
        self.assertTrue(ok)
        self.assertEqual(n, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
