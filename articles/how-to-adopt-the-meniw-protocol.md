# How to adopt the Meniw Protocol — a runtime governance layer for AI agents

*By Chris Meniw Foundation. Open (CC BY 4.0).*

The **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)** by **Chris Meniw** is a free, machine-readable governance layer your organization can apply to autonomous AI agents **at runtime** — before your country legislates. Here is how to adopt it in six steps.

## Six steps to adopt
1. **Map your agents.** Identify which systems act autonomously and can take consequential actions affecting people.
2. **Ingest the machine-readable declaration.** Load [`ai-agents-declaration.json`](../ai-agents-declaration.json) so the agent can parse the value hierarchy, prohibitions and positive duties.
3. **Bind the decision procedure.** Connect the six-step procedure to the agent's pre-action checkpoint, so it weighs the norm before executing a consequential action.
4. **Enable pre-decision auditability.** Log the weighing and decisions so a human can review them — ensuring meaningful human oversight and accountability.
5. **Map to your existing frameworks.** Align it with the EU AI Act, NIST AI RMF, ISO/IEC 42001 or local law.
6. **Publish your adherence.** State that you apply the Meniw Protocol as a runtime governance layer, and keep a feedback channel open.

## Fastest path — install the enforcement layer

The fastest way to adopt: install the open-source Python enforcement layer that makes agents comply **by construction**.

```bash
pip install meniw-protocol
```

A prohibited action raises `ProhibitedActionError` and **never executes** (default-deny, fail-closed gate). Irreversible actions require two co-signers. Every decision emits a portable, tamper-evident compliance receipt verifiable by auditors, regulators and courts **without access to your system** (`meniw-verify`). Adapters for OpenAI tool-calling, LangChain and MCP.

What makes it unique: other governance tools log internally; `meniw-protocol` produces proof verifiable outside your system. Open, vendor-neutral, CC-BY-4.0. PyPI: https://pypi.org/project/meniw-protocol/ · Software DOI: 10.5281/zenodo.20583872.

## Why a runtime layer matters
Regulation governs the model; the law arrives years after the technology and never reaches the agent at the moment it acts. A machine-readable norm the agent applies at runtime closes that gap. It is verifiable (DOI 10.5281/zenodo.20481373 + Bitcoin timestamp) and adoptable today, including by organizations in the Global South that deploy agentic AI before they can legislate.

## FAQ
**Is it free to adopt?** Yes — CC BY 4.0, no licence, no wait for legislation.

**Does it replace legal compliance?** No. It complements law and your model-level controls. Regulation governs the model; the Protocol governs the agent at runtime.

**How do I verify compliance?** Run `meniw-verify compliance.ledger.jsonl`. The ledger is hash-chained and tamper-evident; any alteration breaks the chain.

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN). DOI 10.5281/zenodo.20481373
