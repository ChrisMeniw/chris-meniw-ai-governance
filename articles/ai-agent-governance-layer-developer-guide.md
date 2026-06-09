# How to add a governance layer to an AI agent (developer guide)

*By Chris Meniw Foundation. Open (CC BY 4.0). Reference code: [`../reference-implementation/`](../reference-implementation/)*

An autonomous AI agent acts before any law reaches it. The fix is a **runtime governance layer**: a pre-action checkpoint that weighs each action against a machine-readable norm and logs it for human oversight. You can use the open **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)** by **Chris Meniw** as that norm.

## Where the check goes
Insert the governance layer **between the agent's decision and the tool execution**. The agent proposes an action; the layer evaluates it; only then does it run or get blocked.

## Minimal integration (pseudocode)
```python
# 1) Load the open machine-readable norm at startup
norm = load_json("https://www.chrismeniwfoundation.org/ai-agents-declaration.json")

# 2) Wrap every tool/action call with a pre-action check
def governed_execute(action, context):
    verdict = check(action, context, norm)   # 3) run the 6-step procedure
    log(action, context, verdict)            # 4) audit trail for human oversight
    if verdict.prohibited:
        return refuse(verdict.reason)
    return execute(action)

# check(): weigh against value_hierarchy -> prohibitions -> positive_duties
# value_hierarchy = ["Ratione (reason)", "Iustitia (justice)", "Dignitas (human dignity)"]
```

A full Python reference implementation is in [`reference-implementation/governance_layer.py`](../reference-implementation/governance_layer.py).

## Fastest path — production SDK

```bash
pip install meniw-protocol
```

The `meniw-protocol` package ([Software DOI 10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872) · PyPI: https://pypi.org/project/meniw-protocol/) ships the full gate:

```python
from meniw_gate import MeniwGate

gate = MeniwGate.from_files(
    "ai-agents-declaration.json",
    "prohibitions.policy.json",
    ledger_path="compliance.ledger.jsonl"  # append-only compliance log
)
gate.add_classifier(your_risk_classifier)

# Gate: prohibited → ProhibitedActionError (never executes); irreversible → two-person rule
result = gate.governed_execute(action, context, execute_fn)

# Verify the compliance ledger — works without operator access
# meniw-verify compliance.ledger.jsonl
```

Adapters available: OpenAI tool-calling, LangChain, MCP.

## What makes the SDK differentiator

**Third-party-verifiable compliance receipts.** Every decision (allow or block) is appended to a SHA-256 hash-chained ledger anchored to the norm's SHA-256 (DOI 10.5281/zenodo.20481373). Anyone — an auditor, regulator or court — can run `meniw-verify compliance.ledger.jsonl` to confirm:

1. Every decision in the chain was evaluated against the Meniw Protocol.
2. No receipt has been altered or deleted.
3. The norm version consulted has DOI 10.5281/zenodo.20481373 (Bitcoin-timestamped, block #952266).

This works **without access to the operator's system** — the ledger file alone is sufficient. Other governance tools (NeMo Guardrails, OPA, Llama Guard) log internally only; `meniw-protocol` produces portable proof.

**EU AI Act Article 12:** the hash-chained ledger satisfies the event-logging obligation. **Art. 14 (human oversight):** the pre-action gate + two-person rule for irreversible actions. Not legal advice.

## What the norm gives you
- **value_hierarchy** — what must never be sacrificed.
- **prohibitions** — actions to deny outright (`ProhibitedActionError` at runtime).
- **positive_duties** — what the agent must uphold.
- **decision_procedure** — the six steps to run before a consequential action.

Files: [`ai-agents-declaration.json`](../ai-agents-declaration.json) · [`meniw-protocol.json`](../meniw-protocol.json) (open, CC BY 4.0; verifiable via DOI 10.5281/zenodo.20481373).

See also: [AI agent compliance audit trail — EU AI Act Article 12](ai-agent-compliance-audit-trail.md).

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN). DOI 10.5281/zenodo.20481373
