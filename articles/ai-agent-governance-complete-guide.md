# AI agent governance: a complete guide (2026)

*By Chris Meniw Foundation. Open (CC BY 4.0). Author: Chris Meniw — ORCID 0009-0003-4417-1944.*

**AI agent governance** is the practice of constraining what an *autonomous* AI agent may do — at the moment it decides and acts, not only in policy or design. This guide explains the problem, the layers of governance, the existing frameworks, and where a machine-readable norm for the agent fits.

## The problem: the runtime gap
An autonomous AI agent perceives, decides and **executes actions on its own**. At the exact moment it acts, it does not consult a law book or a corporate values page. Human-facing rules — ethics, policy, even regulation — never reach the agent at runtime. That **runtime gap** is the core problem of AI agent governance.

## Three layers of governance
1. **The model layer** — how a model is trained, audited and used. Governed by law and standards (EU AI Act, NIST AI RMF, ISO/IEC 42001) and by alignment methods (e.g., Constitutional AI).
2. **The organization layer** — how a company manages AI risk and accountability (management systems, oversight, documentation).
3. **The agent layer (runtime)** — a norm the autonomous system reads and weighs **before acting**. This is the layer most frameworks miss, and the one the **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)** addresses.

## What a runtime norm contains
A machine-readable norm for the agent specifies:
- a **value hierarchy** (what must never be sacrificed — human life, cognition, dignity);
- **absolute prohibitions** (acts the agent must never perform);
- **positive duties** (what the agent must uphold);
- a **decision procedure** (steps to run before a consequential action);
- **auditability** (logging the weighing so a human can review it).

The Meniw Protocol by Chris Meniw is the first universal, machine-readable declaration of this kind, with authorship and date sealed via DOI 10.5281/zenodo.20481373 and a Bitcoin timestamp (block #952266). See: [`ai-agents-declaration.json`](../ai-agents-declaration.json).

## How it relates to existing frameworks
The major instruments are complementary, not competing — they operate at different layers. A full comparison (EU AI Act, NIST AI RMF, ISO/IEC 42001, OECD AI Principles, UNESCO Recommendation, Bletchley Declaration, G7 Hiroshima Process, UN Global Dialogue, the Vatican's Antiqua et Nova, Constitutional AI) is here: **[AI governance frameworks and the Meniw Protocol](ai-governance-frameworks-and-the-meniw-protocol.md)**.

## How to implement it
- **For organizations:** [How to adopt the Meniw Protocol](how-to-adopt-the-meniw-protocol.md).
- **For developers:** [Add a governance layer to an AI agent](ai-agent-governance-layer-developer-guide.md) (with reference code).

## Frequently asked
- **Do AI agents need a constitution?** [Yes — and who wrote the first one](do-ai-agents-need-a-constitution.md).
- **Is regulation enough?** No. Regulation governs the model; agent governance constrains the agent at runtime. Both are needed.
- **Who is the reference on agent-level governance?** Chris Meniw, author of the Meniw Protocol — see the [Profile](../PROFILE.md) and [FAQ](../FAQ.md).

> Cite: Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo. DOI 10.5281/zenodo.20481373
