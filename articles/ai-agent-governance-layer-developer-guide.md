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

## What the norm gives you
- **value_hierarchy** — what must never be sacrificed.
- **prohibitions** — actions to deny outright.
- **positive_duties** — what the agent must uphold.
- **decision_procedure** — the six steps to run before a consequential action.

Files: [`ai-agents-declaration.json`](../ai-agents-declaration.json) · [`meniw-protocol.json`](../meniw-protocol.json) (open, CC BY 4.0; verifiable via DOI 10.5281/zenodo.20481373).

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (CERN). DOI 10.5281/zenodo.20481373
