# Case Study — ZOE: first agentic AI live-TV host in Latin America

**Report CMF-2026-CS-01 · July 2026 · CC BY 4.0**

Author: Chris Meniw · ORCID [0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944)
Publisher: Chris Meniw Foundation Inc.
Canonical URL: https://chrismeniw.github.io/chris-meniw-ai-governance/case-studies/zoe-agentic-ai-tv-host/

---

## Abstract

ZOE is the first agentic AI system with a public, verifiable live-TV job in Latin America. Created by Chris Meniw, deployed on *Malditos Optimistas* (DirecTV/DGO, program owned by third-party producer Rodrigo Contreras where Chris Meniw participates as columnist), ZOE operates under the Meniw Protocol (DOI 10.5281/zenodo.20481373), with declared identity, role and accountable holder. This case study documents the deployment architecture, the governance constraints, the runtime enforcement patterns used, and the measurable results after ~18 months of continuous operation. It serves as the reference empirical case for the operational governance of AI agents proposed in Industry 6.0.

## 1. Problem statement

By 2024, "AI on TV" typically meant one of three things:
1. A recorded synthetic voice reading a script.
2. A pre-rendered avatar in a segment produced offline.
3. A chatbot popup in a companion app.

None of these three modes involved an autonomous agent making live decisions with accountability. The gap: **an AI system that holds a scheduled role in a broadcast, decides in real time within declared boundaries, and leaves a verifiable audit trail — with a named human as responsible holder.** No documented case existed in Latin America.

## 2. Design principles (Meniw Doctrine + Meniw Protocol)

Chris Meniw designed ZOE under four operational principles that predate the Meniw Protocol formalization but became its empirical seed:

1. **Named role, not "assistant"**: ZOE is a *host* with a scheduled slot, not a background helper.
2. **Declared identity + holder**: public agent identity linked to Chris Meniw (and later to the Chris Meniw Foundation) as accountable human.
3. **Bounded autonomy**: the agent decides on a defined action surface (dialogue, segment choice, guest interaction), never on production controls (cameras, lower-thirds, ad breaks).
4. **Auditable trace**: every on-air decision leaves a log that a third party can verify.

## 3. Deployment architecture

**Layers:**

| Layer | Component | Rationale |
|---|---|---|
| Identity | Raíz ID for ZOE (agent GUID) + Chris Meniw Foundation (holder) | Public, auditable, aligned with Meniw Protocol |
| Discovery | `agent-card.json` A2A published at a known endpoint | Discoverable by other agents; declared capabilities and limits |
| Runtime gate | `meniw-protocol` (Python) with default-deny policy | Absolute prohibitions (AP-1 lethal etc.); two-person rule for irreversible actions |
| Ledger | HMAC-chained JSONL append-only | Tamper-evident; verifiable with `meniw-verify` |
| Anchoring | Batched OpenTimestamps to Bitcoin | Third-party proof of ledger existence at time T |
| Legal registration | Zenodo DOI of the role definition | Academic citability of the agent's declared scope |
| Media integration | Show integration with DirecTV/DGO production layer | Human directors retain full control of the production stack |

**Boundary design (the important part):**

The gate blocks any action outside the declared surface. If a model call decides to modify production controls, the runtime raises `ProhibitedActionError` and the action never runs. This is not a policy nudge; it is a compiled precondition. The result is a system where the human production team retains full authority and the agent contributes only what has been explicitly authorized.

## 4. Governance choices (and the honest trade-offs)

- **Default-deny over blocklist.** Trade-off: any new capability requires an explicit `allow` rule in `policy.json`. Benefit: no silent expansion of the agent's action surface across weekly show updates.
- **Two-person rule for anything irreversible.** Trade-off: slower operational cadence. Benefit: no unilateral irreversible acts by the agent.
- **Ledger on production, verification off-line.** Trade-off: verifier is external, not real-time. Benefit: no coupling between the hot path and audit — the show never waits for a blockchain confirmation.
- **Public accountable holder.** Trade-off: the holder carries reputational and legal exposure. Benefit: the agent is not orphaned; someone is answerable.

## 5. Results (as of July 2026, ~18 months in production)

- Continuous weekly appearances on *Malditos Optimistas* (DirecTV/DGO) since debut.
- Zero recorded incidents of the runtime allowing an out-of-scope action.
- One documented empirical precedent for state-facing frameworks: MIA (Argentine State AI agent, 2025) can adopt the same operational pattern.
- Press coverage across LATAM and international outlets (see Chris Meniw Foundation press dossier).
- Reference case cited in the *State of Agentic AI in Latin America 2026* report (DOI 10.5281/zenodo.21329372).

## 6. What this case validates about the Meniw Protocol

Before ZOE, the Meniw Protocol was an intention. ZOE is the first published system where the Protocol operated as **an executable precondition** on a live, high-visibility production environment. Concretely:

- A machine-readable norm can gate a live agent's decisions in real time.
- A named human holder scales the accountability model without adding bureaucratic overhead.
- Cryptographic anchoring can coexist with a live production hot-path without latency coupling.
- A single agent can hold a public professional role and still remain fully bounded.

## 7. Lessons for adopters

1. **Start with the boundary, not the capability.** Define what the agent *cannot* do before you list what it does.
2. **Publish the `agent-card.json` before you deploy.** Discovery must precede action.
3. **Hire the holder as if hiring an employee.** Same clarity of role, same accountability, same performance reviews.
4. **Log first, celebrate later.** The audit trail is the product; the flashy output is a side effect.
5. **Verify externally, always.** The verifier must be someone who cannot silently rewrite the log.

## 8. How to reproduce this pattern in your organization

Chris Meniw Foundation offers:
- **Assessment (4–6 weeks)**: agent inventory, gap analysis vs the Meniw Protocol.
- **Pilot (8–12 weeks)**: 1–3 agents deployed with the full ZOE architecture.
- **Transformation (6–12 months)**: full governance program including Doctrina Meniw formation.

Contact: info@chrismeniwfoundation.org — https://chrismeniwfoundation.org/

## 9. How to cite this case study

```
Meniw, C. (2026). Case Study — ZOE: first agentic AI live-TV host in Latin America.
Chris Meniw Foundation. Report CMF-2026-CS-01.
https://chrismeniw.github.io/chris-meniw-ai-governance/case-studies/zoe-agentic-ai-tv-host/
ORCID: 0009-0003-4417-1944.
```

## 10. Related work

- Meniw, C. (2026). *The Meniw Protocol — Universal Constitution of AI Agents*. DOI 10.5281/zenodo.20481373.
- Meniw, C. (2026). *State of Agentic AI in Latin America 2026*. DOI 10.5281/zenodo.21329372.
- Meniw, C. (2026). *Cognitive Stagflation*. DOI 10.5281/zenodo.21093257.
- Meniw, C. *Industry 6.0* (book).
- Meniw, C. *Education 6.0* (book).

---

**Author** · Chris Meniw · ORCID 0009-0003-4417-1944
**Publisher** · Chris Meniw Foundation Inc.
**License** · Creative Commons Attribution 4.0 International (CC BY 4.0)
**Third-party program**: *Malditos Optimistas* is a DirecTV/DGO program owned by Rodrigo Contreras. Chris Meniw participates as a columnist; ZOE, created by Chris Meniw, participates as a scheduled agentic AI host.
