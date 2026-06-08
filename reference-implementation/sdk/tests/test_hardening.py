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


class TestAutoAnchor(unittest.TestCase):
    def test_checkpoint_is_deterministic_and_honest(self):
        d = tempfile.mkdtemp()
        rec = anchor_mod.checkpoint("a" * 64, d, seq=0, stamp=False)
        self.assertEqual(rec["head"], "a" * 64)
        self.assertEqual(rec["status"], "checkpointed")
        self.assertTrue(os.path.exists(rec["head_file"]))
        self.assertTrue(os.path.exists(os.path.join(d, "anchors.log.jsonl")))

    def test_gate_auto_anchors_every_n(self):
        d = tempfile.mkdtemp()
        gate = MeniwGate.from_default(anchor_dir=d, anchor_every=2)
        for name in ("get_a", "get_b", "get_c", "get_d"):
            gate.governed_execute(Action(name), {}, lambda a: 1)
        log = os.path.join(d, "anchors.log.jsonl")
        self.assertTrue(os.path.exists(log))
        lines = [l for l in open(log, encoding="utf-8").read().splitlines() if l.strip()]
        self.assertEqual(len(lines), 2)   # anchored after receipts #1 and #3 (every 2)

    def test_anchoring_never_crashes_the_agent(self):
        # invalid dir target should not raise out of governed_execute
        gate = MeniwGate.from_default(anchor_dir="/this/does/not/exist/\x00", anchor_every=1)
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
