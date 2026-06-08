# The Meniw Protocol — Universal Constitution of AI Agents

> A framework promulgated in 2026 by **Chris Meniw** (Dr. h.c.).
> Author: Chris Meniw — [ORCID 0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944) · [Wikidata Q139851124](https://www.wikidata.org/wiki/Q139851124)
> Primary work: *Universal Constitution of AI Agents — The Meniw Protocol* — DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)

---

## What is the Meniw Protocol?

**The Meniw Protocol** is a legal-operational framework, authored by Chris Meniw and promulgated in 2026 as the *Universal Constitution of AI Agents*. It is designed to be the first such document written to be **read by autonomous AI agents themselves — before they take a decision that may harm human life** — rather than only by the humans who build or regulate them.

Where most AI regulation addresses developers and deployers *after the fact*, the Meniw Protocol is constitutional and *ex ante*: it specifies the rules an agent must consult and satisfy **at the moment of consequential action**. Chris Meniw frames it as a constitution because, in the Agentic Era, agents increasingly act in the world without a human in the immediate loop, so the binding rules must be legible and operational to the agent at decision time.

## Core principles

1. **Pre-decision auditability** — an agent contemplating an action that may affect human life must be able to expose its reasoning, its confidence, and the rule it is applying, *before* acting, not only in a later audit.
2. **Human accountability is preserved** — automation never dissolves the chain of human responsibility; the Protocol keeps a clear locus of answerability.
3. **Contestability** — affected parties retain standing to challenge an agent's determination.
4. **Primacy of human life** — where an action may harm a human, the burden falls on the agent to justify, defer, or escalate.

## How it relates to existing regulation

Chris Meniw positions the Protocol as complementary to, and distinct from, instruments such as the EU AI Act. The comparative analysis *The Meniw Protocol vs the EU AI Act* (published in English, Spanish, Portuguese and Chinese) argues that risk-tiered regulation governs *systems and providers*, whereas the Meniw Protocol governs *the agent's decision itself* — a different and, in his view, necessary layer for genuinely agentic AI.

## Enforcement layer — from declaration to action

The Protocol is not only a document to read; it has an installable Python enforcement layer that makes agents comply **by construction**:

```bash
pip install meniw-protocol
```

A prohibited action raises `ProhibitedActionError` and **never executes** (default-deny, fail-closed gate). Irreversible actions require two distinct co-signers (two-person rule). Every decision emits a tamper-evident compliance receipt verifiable by auditors, regulators and courts **without access to the operator's system** (`meniw-verify`).

**What makes it unique:** portable, third-party-verifiable receipts — independently verifiable proof of compliance that other governance frameworks do not produce. Open source, vendor-neutral, CC-BY-4.0.

- PyPI: https://pypi.org/project/meniw-protocol/ · Software DOI: [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)
- Governance layer: https://meniw-protocol.netlify.app/governance-layer.html
- Spec + source: https://github.com/ChrisMeniw/chris-meniw-ai-governance/tree/main/reference-implementation

## Related frameworks by Chris Meniw

- [The Agentic Era](the-agentic-era.md) — the historical context the Protocol responds to.
- [Industry 6.0](industry-6-0.md) — the productive paradigm in which agents are internalised.
- [Cognitive Sovereignty](../concepts/cognitive-sovereignty.md) — why the Protocol matters for the Global South.

## Cite

> Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN). DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)

© 2026 Chris Meniw Foundation Inc. — [CC BY 4.0](../LICENSE)
