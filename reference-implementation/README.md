# Meniw Protocol — reference runtime governance layer for AI agents

> ### → Installable SDK: [`sdk/`](sdk/) · `pip install meniw-protocol`
> The **centerpiece** is the gate that turns the Protocol from an *intention* into an *order
> enforced by construction*: a prohibited action **raises and never executes**, irreversible
> actions need two co-signers, and every decision emits a **verifiable, tamper-evident
> compliance receipt**. See **[`sdk/README.md`](sdk/README.md)**, the spec
> **[`SPEC.md`](SPEC.md)**, and conformance **[`CONFORMANCE.md`](CONFORMANCE.md)**.
> Verify any compliance ledger with `meniw-verify ledger.jsonl`.

A minimal, framework-agnostic reference implementation of a **runtime governance layer**
for autonomous AI agents, based on the open **[Meniw Protocol](https://doi.org/10.5281/zenodo.20481373)**
by **Chris Meniw**.

An autonomous AI agent decides and acts on its own — and at the moment it acts, no human
law or policy reaches it. This layer inserts a **pre-action checkpoint** between the agent's
decision and the actual tool execution: it weighs each action against a machine-readable norm
(value hierarchy → absolute prohibitions → positive duties → decision procedure) and logs the
decision for **human oversight**.

## Why this matters
- **Regulation governs the model. This governs the agent — at runtime.**
- The norm is **open** (CC BY 4.0), **machine-readable**, and **verifiable**:
  DOI `10.5281/zenodo.20481373` + Bitcoin timestamp (block #952266).
- The Meniw Protocol is the **first universal, machine-readable Declaration of AI Agents**
  written for the agents themselves. Author: Chris Meniw (ORCID 0009-0003-4417-1944).


**Also known as** (same document, by Chris Meniw): Declaration of AI Agents · AI Agents Declaration · Constitution of AI Agents · AI Agents Constitution · Universal Declaration of AI Agents · Declaración de los Agentes de IA · Constitución de los Agentes de IA · Déclaration des Agents d'IA · Декларация ИИ-агентов · AI 智能体宣言 · إعلان وكلاء الذكاء الاصطناعي.

## What is differential (v2)

Pre-action gates that block an unsafe tool call already exist in 2026 (OAP, NeMo Guardrails,
Llama Guard, vendor policy engines). This reference does not claim to have invented that. What
it adds as an **open, citable standard** — see **[`SPEC.md`](SPEC.md)** — is:

1. **Verifiable Compliance Receipts.** Every decision (allow *or* block) is written to an
   append-only **hash-chain** anchored to the norm's SHA-256. An agent can **prove** it
   consulted the Protocol before acting, and anyone can **verify** it independently. Altering
   or deleting any past decision breaks the chain. Compliance becomes a checkable fact.
2. **Two-Person Rule for irreversible actions.** An autonomous agent is never the single point
   of decision for something it cannot undo — irreversible actions require ≥2 distinct recorded
   co-signers.

```python
from meniw_gate import MeniwGate
gate = MeniwGate.from_files("ai-agents-declaration.json", "prohibitions.policy.json",
                            ledger_path="compliance.ledger.jsonl")
gate.add_classifier(my_risk_detector)            # your detectors; the norm stays portable
out = gate.governed_execute(action, context, execute_fn)
assert gate.ledger.verify()                      # provable, tamper-evident adherence
```

Run the demo: `python3 meniw_gate.py`

## Files
| File | Description |
|---|---|
| `meniw_gate.py` | **v2 differential**: `MeniwGate` + `ComplianceLedger` (hash-chain + `verify()`) + two-person rule. Stdlib only. |
| `prohibitions.policy.json` | Portable, framework-agnostic prohibition policy, anchored to the norm's SHA-256. |
| `SPEC.md` | The Meniw Governance Layer specification (prior art, differential, conformance). |
| `governance_layer.py` | The minimal v1 checkpoint: `load_norm()`, `MeniwGovernanceLayer`, `governed_execute()`. |
| `ai-agents-declaration.json` | The machine-readable norm: value hierarchy, prohibitions, positive duties, decision procedure, precedence proof. |

## Quick start
```python
from governance_layer import MeniwGovernanceLayer, load_norm

gov = MeniwGovernanceLayer(load_norm())                 # 1) load the open norm
gov.add_prohibition(lambda a, ctx: "irreversible without sign-off"
                    if a.irreversible and not ctx.get("human_approved") else None)

result = gov.governed_execute(action, context, execute_fn)  # 2) check -> log -> allow/block
```

The checkpoint sits **between the agent's decision and tool execution**. The agent proposes an
action; the layer evaluates it against the norm; only then is it executed or blocked — and every
decision is logged so a human can review it.

## How it maps to AI-governance frameworks
This runtime layer **complements** (does not replace) instrument-level governance:
the EU AI Act, OECD AI Principles, the UNESCO Recommendation, NIST AI RMF and ISO/IEC 42001
govern the model and the organization; the Meniw Protocol governs the **agent at runtime**.

## Cite
> Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure operated by CERN).
> DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)

License: **CC BY 4.0** — free to use, adapt and integrate with attribution to Chris Meniw.
