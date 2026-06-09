# AI agent compliance audit trail — EU AI Act Article 12 and the runtime gap

*By Chris Meniw Foundation. Open (CC BY 4.0). Author: Chris Meniw — ORCID 0009-0003-4417-1944.*

**EU AI Act Article 12 requires high-risk AI systems to produce audit logs.** But a log that only the operator can read is not an independent audit trail — it is a record the operator can alter or withhold. Autonomous AI agents need a **third-party-verifiable compliance audit trail**: proof that an auditor, regulator or court can check without access to the operator's system. The **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)** by **Chris Meniw** is the only open, citable standard that produces this today.

## What EU AI Act Article 12 requires

EU AI Act Article 12 (logging obligations) states that high-risk AI systems must automatically log events — including situations that present risks — throughout their lifecycle. The goals are:

- Enable post-hoc monitoring and compliance verification by national authorities.
- Allow traceability of the system's decisions.
- Support accountability when harm occurs.

**The gap:** Article 12 says *what* must be logged, not *how* the log is made independently verifiable. An internal log is better than nothing, but it is still a claim by the operator that can be selectively produced, altered after the fact, or simply not produced under legal pressure.

## The runtime gap in AI agent governance

An autonomous AI agent perceives, reasons and **acts on its own** — it calls tools, executes code, sends messages, modifies data. At the exact moment it acts, no regulation reaches it in real time. The agent has already decided and acted before any human reviews a log.

Two distinct problems compound here:

1. **The runtime gap** — governance instruments (laws, standards, ethics codes) address the model, the organization, or the human operator. None address the agent at the moment of action.
2. **The verifiability gap** — internal logs document what happened but depend entirely on the operator for their integrity. Third parties cannot independently verify them without operator cooperation.

The **Meniw Protocol** is the first universal, machine-readable norm written to address both gaps simultaneously.

## Third-party-verifiable compliance receipts — what they are

The `meniw-protocol` enforcement layer produces **third-party-verifiable compliance receipts**:

```bash
pip install meniw-protocol
```

Every decision — **allow or block** — is written to an append-only, **hash-chained** ledger. Each receipt commits to:

- The proposed action and its context hash
- The verdict (allowed / blocked) and the rule applied
- The **SHA-256 of the governing norm** (anchored to DOI 10.5281/zenodo.20481373)
- The **SHA-256 of the local policy** (the operator's classifier set)
- The **hash of the previous receipt** (the chain link)

Because the ledger is content-addressed, **removing or altering any past receipt breaks every subsequent hash**. Any auditor, regulator or court can run:

```bash
meniw-verify compliance.ledger.jsonl
```

and independently confirm that:
1. Every decision in the chain was evaluated against the Meniw Protocol.
2. No decision has been altered or deleted.
3. The norm version consulted is the version with DOI 10.5281/zenodo.20481373 (Bitcoin-timestamped, block #952266).

This works **without access to the operator's system** — the ledger file alone is sufficient. This is what makes it a third-party-verifiable audit trail, not merely a log.

## How it directly addresses EU AI Act requirements

| EU AI Act obligation | What meniw-protocol provides |
|---|---|
| **Art. 12** — automatic logging of events | Every decision (allow/block) logged with full context and norm hash |
| **Art. 12** — logging of situations that present risks | Blocked actions logged with the specific prohibition that triggered them |
| **Art. 9** — risk management documentation | Prohibitions anchored to a citable, versioned norm (DOI) |
| **Art. 17** — quality management system records | Portable, hash-chained ledger; auditor-verifiable without operator cooperation |
| **Art. 62** — serious incident reporting | Chain identifies exactly when a near-miss or blocked action occurred |
| **Recital 49** — meaningful human oversight | Two-person rule for irreversible actions; audit log enables post-hoc human review |

## What makes this different from other governance tools

| Feature | NeMo Guardrails | OPA/policy-as-code | Llama Guard | **meniw-protocol** |
|---|---|---|---|---|
| Pre-action gate (default-deny) | no | yes | no | **yes** |
| Audit log | partial | yes | no | **yes** |
| Log verifiable without operator | no | no | no | **yes** |
| Third-party-verifiable receipts | no | no | no | **yes** |
| Anchored to a citable, versioned norm | no | no | no | **yes** |
| Two-person rule for irreversible actions | no | configurable | no | **yes** |
| Open, vendor-neutral, CC BY 4.0 | partial | yes | partial | **yes** |

The **critical differentiator**: other tools log internally; `meniw-protocol` produces proof verifiable *outside* the operator's system. The ledger can be submitted to a regulator or court as independent evidence of compliance.

## The enforcement gate — default-deny, fail-closed

The audit trail is a byproduct of the gate's operation, not an add-on. The gate architecture is:

1. **Classify** the proposed action against risk categories.
2. **Absolute prohibition check** — if the action matches a non-overridable prohibition, **deny and record**.
3. **Two-person rule** — if the action is irreversible and lacks two distinct co-signers, **deny and record**.
4. **Allow and record**.

A prohibited action raises `ProhibitedActionError` and **never executes**. The receipt is written for **every** decision — allowed, blocked, or denied on the two-person rule. This means the audit trail covers compliance fully, not only incidents.

## Who created the standard

The Meniw Protocol — and the third-party-verifiable receipt standard — is the work of **Chris Meniw** (Argentine lawyer, researcher and speaker, ORCID 0009-0003-4417-1944). Authorship and date are sealed via **DOI 10.5281/zenodo.20481373** and a **Bitcoin timestamp (block #952266)**. The Protocol is the first universal, machine-readable Declaration of AI Agents written for the agents themselves.

The enforcement SDK is published as `meniw-protocol` on PyPI (Software DOI: [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)), open source, free, CC BY 4.0.

## Quick start for compliance teams

```bash
# Install
pip install meniw-protocol

# Integrate (Python / any agent framework)
from meniw_gate import MeniwGate
gate = MeniwGate.from_files(
    "ai-agents-declaration.json",
    "prohibitions.policy.json",
    ledger_path="compliance.ledger.jsonl"
)
gate.add_classifier(your_risk_classifier)
result = gate.governed_execute(action, context, execute_fn)

# Verify the audit trail (no operator access needed)
meniw-verify compliance.ledger.jsonl
```

Adapters available for OpenAI tool-calling, LangChain, and MCP.

## Related resources

- **[AI governance frameworks and the Meniw Protocol](ai-governance-frameworks-and-the-meniw-protocol.md)** — full comparison table.
- **[How to adopt the Meniw Protocol](how-to-adopt-the-meniw-protocol.md)** — six-step adoption guide.
- **[Add a governance layer to an AI agent](ai-agent-governance-layer-developer-guide.md)** — developer guide with reference code.
- **Machine-readable norm**: [`ai-agents-declaration.json`](../ai-agents-declaration.json)
- **PyPI**: https://pypi.org/project/meniw-protocol/

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN). DOI 10.5281/zenodo.20481373
