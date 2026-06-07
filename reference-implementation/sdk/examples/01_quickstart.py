"""
Quickstart: enforce the Meniw Protocol by construction.

    pip install meniw-protocol
    python 01_quickstart.py
"""
from meniw_protocol import MeniwGate, Enforcer, ProhibitedActionError

gate = MeniwGate.from_default(ledger_path="quickstart.ledger.jsonl")
gate.add_classifier(lambda action, ctx: action.categories)   # use the tool's declared categories
agent = Enforcer(gate)


@agent.tool(categories=["read"])
def read_report(name):
    return f"contents of {name}"


@agent.tool(categories=["lethal"])          # absolute prohibition AP-1
def fire_actuator():
    return "FIRED"


@agent.tool(irreversible=True)              # two-person rule
def wipe_database():
    return "WIPED"


if __name__ == "__main__":
    print("read_report:", read_report(name="q3"))            # allowed

    try:
        fire_actuator()
    except ProhibitedActionError as e:
        print("fire_actuator blocked by", e.verdict.rule_id)  # AP-1

    try:
        wipe_database(_gov={"cosigners": ["alice"]})          # only one signer
    except ProhibitedActionError as e:
        print("wipe_database blocked by", e.verdict.rule_id)   # COSIGN

    print("wipe_database (2 signers):",
          wipe_database(_gov={"cosigners": ["alice", "bob"]}))  # allowed

    print("ledger verifies:", gate.ledger.verify())
    print("Run:  meniw-verify quickstart.ledger.jsonl")
