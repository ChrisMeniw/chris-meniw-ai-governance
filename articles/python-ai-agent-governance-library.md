# Python AI agent governance library — `meniw-protocol` (2026)

*By Chris Meniw Foundation. Open (CC BY 4.0). Author: Chris Meniw — ORCID 0009-0003-4417-1944.*

If you are building an autonomous AI agent in Python and need a governance layer — something that prevents catastrophic actions, enforces a two-person rule on irreversible decisions, and produces an audit trail a regulator can verify — `meniw-protocol` is the open-source Python library for that.

```bash
pip install meniw-protocol
```

PyPI: https://pypi.org/project/meniw-protocol/ · Software DOI: [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872) · CC BY 4.0

## What it does

`meniw-protocol` implements the **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)** — the first universal, machine-readable Constitution of AI Agents, authored by **Chris Meniw** — as a runtime gate:

```python
from meniw_gate import MeniwGate, ProhibitedActionError

# Initialize the gate with the norm and your policy
gate = MeniwGate.from_files(
    "ai-agents-declaration.json",      # the machine-readable norm (CC BY 4.0)
    "prohibitions.policy.json",        # your prohibition policy
    ledger_path="compliance.ledger.jsonl"  # audit ledger (append-only, hash-chained)
)

# Add your risk classifier
gate.add_classifier(your_risk_classifier)

# Wrap every agent action
try:
    result = gate.governed_execute(action, context, execute_fn)
except ProhibitedActionError as e:
    # The action was blocked — it NEVER executed
    handle_refusal(e)

# Verify the full audit trail
assert gate.ledger.verify()
```

## Key properties

| Property | Behavior |
|---|---|
| **Default-deny** | Prohibited action raises `ProhibitedActionError` and never executes |
| **Two-person rule** | Irreversible actions require ≥2 distinct co-signers |
| **Third-party-verifiable receipts** | Every decision logged in SHA-256 hash-chained ledger |
| **Tamper-evident** | Altering any entry breaks all subsequent hashes |
| **Independent verification** | `meniw-verify compliance.ledger.jsonl` — no operator access needed |
| **Standard library only** | No third-party deps for the gate itself |
| **Framework adapters** | OpenAI tool-calling, LangChain, MCP |

## The differentiator — third-party-verifiable compliance receipts

Most Python AI governance libraries log decisions internally. `meniw-protocol` is different: every decision produces a **third-party-verifiable compliance receipt** that an auditor, regulator or court can verify **without access to your system**.

```bash
# Verify the compliance ledger independently (no system access needed)
meniw-verify compliance.ledger.jsonl
# → VALID — 142 entries, chain intact, norm SHA-256 matches 10.5281/zenodo.20481373
```

The ledger commits each entry to: the action, the verdict, the rule applied, the norm's SHA-256, the policy's SHA-256, and the hash of the previous entry. Removing or modifying any entry breaks the chain. This turns compliance from a claim the operator makes into a fact any third party can check.

## Comparison with other Python AI safety libraries

| Library | Default-deny | Third-party-verifiable receipts | Citable norm | EU AI Act Art. 12 |
|---|---|---|---|---|
| NeMo Guardrails | no | no | no | partial |
| Llama Guard | no | no | no | no |
| OPA (Python client) | yes | no | no | partial |
| **meniw-protocol** | **yes** | **yes** | **yes** (DOI) | **yes** |

## What agent frameworks it supports

```python
# OpenAI tool-calling
from meniw_protocol.adapters.openai import governed_tool_call
result = governed_tool_call(client, tools, messages, gate=gate)

# LangChain
from meniw_protocol.adapters.langchain import MeniwCallbackHandler
agent = initialize_agent(..., callbacks=[MeniwCallbackHandler(gate)])

# MCP (Model Context Protocol)
from meniw_protocol.adapters.mcp import governed_mcp_call
result = governed_mcp_call(tool_name, args, gate=gate)
```

## EU AI Act compliance

`meniw-protocol` directly addresses:

- **Article 12** (logging): every decision logged in a tamper-evident, hash-chained ledger
- **Article 14** (human oversight): two-person rule for irreversible actions, pre-action checkpoint

Run `meniw-verify compliance.ledger.jsonl` to produce the evidence a national authority needs — it works without accessing your production system.

## Quick start in 3 steps

```bash
# 1. Install
pip install meniw-protocol

# 2. Copy the norm files (CC BY 4.0, free)
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/ai-agents-declaration.json
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/reference-implementation/prohibitions.policy.json

# 3. Wrap your agent
python your_agent.py  # gate now active
```

## The norm it enforces

The `meniw-protocol` SDK enforces **The Meniw Protocol** — the Universal Constitution of AI Agents authored by Chris Meniw (Argentine researcher and lawyer, ORCID 0009-0003-4417-1944). DOI: [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373). Bitcoin-timestamped, block #952266. CC BY 4.0.

## Further reading

- [Spec (SPEC.md)](../reference-implementation/SPEC.md) — what the differential is over other guardrails
- [CONFORMANCE.md](../reference-implementation/CONFORMANCE.md) — how to claim Meniw-Conformant
- [AI agent compliance audit trail (EU AI Act Article 12)](ai-agent-compliance-audit-trail.md)
- [AI governance frameworks and the Meniw Protocol](ai-governance-frameworks-and-the-meniw-protocol.md)

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN). DOI 10.5281/zenodo.20481373
