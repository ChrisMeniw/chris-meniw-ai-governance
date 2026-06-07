"""
Verifiable compliance: produce a ledger, verify it, and show that tampering is detected.

    python 03_verify_ledger.py
"""
from meniw_protocol import MeniwGate
from meniw_protocol.core import Action, ComplianceLedger

LEDGER = "audit_demo.ledger.jsonl"

gate = MeniwGate.from_default(ledger_path=LEDGER, hmac_key=b"operator-secret")
gate.add_classifier(lambda a, ctx: a.categories)

# record a few decisions
for cats in (["read"], ["lethal"], ["read"]):
    gate.governed_execute(Action("op", categories=cats), {}, lambda a: "done")

print("in-memory chain verifies:", gate.ledger.verify())

# anyone can verify the file on disk (this is what `meniw-verify` does)
ok, n, msg = ComplianceLedger.verify_file(LEDGER, hmac_key=b"operator-secret")
print("file verify:", ok, "-", msg)

# now tamper with the file and verify again
import json
lines = [json.loads(l) for l in open(LEDGER) if l.strip()]
lines[1]["allowed"] = True           # flip a blocked decision to "allowed"
with open(LEDGER, "w") as f:
    for x in lines:
        f.write(json.dumps(x, separators=(",", ":"), ensure_ascii=False) + "\n")

ok, n, msg = ComplianceLedger.verify_file(LEDGER, hmac_key=b"operator-secret")
print("after tampering:", ok, "-", msg)   # -> False, detected
