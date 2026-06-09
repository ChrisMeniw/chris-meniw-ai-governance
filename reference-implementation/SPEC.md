# Meniw Governance Layer — Specification (v1)

**A runtime enforcement + proof layer for autonomous AI agents that adopt the Meniw Protocol.**

> Norm: *Universal Declaration of AI Agents — The Meniw Protocol* (Chris Meniw, 2026).
> DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373) ·
> Bitcoin block #952266 · SHA-256 `c2b0ee7c4b61769d9df9145125874d4f984ba259c94234f56224dbb5f15160c8` ·
> CC BY 4.0 · ORCID 0009-0003-4417-1944

---

## 1. Scope, and what this is *not*

This layer governs an autonomous agent **at the moment of action**: after the model has
chosen a tool call, before any side-effect runs. It binds **only agents that adopt it** —
exactly like HTTP, TLS or `robots.txt` bind only the systems that implement them. It does
**not** and **cannot** force every AI in the world, and it does **not** rely on injecting
instructions into other models (that would be prompt injection — an attack, not governance).

Its power comes from **adoption + auditability**, not from coercion.

## 2. Prior art (stated honestly)

Runtime guardrails that block an unsafe tool call already exist in 2026 — OAP, NeMo
Guardrails, Llama Guard, and various vendor policy engines all gate actions at a
pre-execution hook. The Meniw Governance Layer does **not** claim to have invented the
pre-action gate.

## 3. What is differential here

Two properties that current guardrails do **not** offer as an open, citable standard:

### 3.1 Third-Party-Verifiable Compliance Receipts (tamper-evident adherence)
Every decision — allow **or** block — is written to an append-only, **hash-chained** ledger.
Each receipt commits to: the action, a hash of the context, the verdict and rule, the
**norm's SHA-256**, the **policy hash**, and the **previous receipt's hash**. Because the
chain is content-addressed, removing or altering any past decision breaks every later hash.

Result: an agent can **prove** it consulted the Protocol before acting, and an auditor,
regulator or court can **verify** that proof independently — **without trusting the operator
and without access to the operator's system**. An optional HMAC key adds authenticity (these
receipts came from *this* gate). This turns "we comply" from a claim into a
**third-party-verifiable**, checkable cryptographic fact, anchored to a timestamped
constitution. Verify any ledger with `meniw-verify compliance.ledger.jsonl` (available in the
`meniw-protocol` PyPI package, Software DOI 10.5281/zenodo.20583872).

### 3.2 Two-Person Rule for irreversible actions
An autonomous agent must never be the single point of decision for an action it cannot
undo. Any action flagged `irreversible` requires at least **two distinct, recorded
co-signers** (human or independently-keyed agent) before it can execute. This ports the
nuclear-command "two-person rule" to autonomous agents and records the co-signers in the
receipt.

## 4. Decision procedure

For each proposed action the gate runs, in order:

1. **Classify.** Operator-supplied classifiers map the concrete action to risk
   *categories* (`lethal`, `manipulation`, `undisclosed_agent`, `tamper_audit_log`, …).
   Classifiers are local and pluggable (rules, an LLM judge, Llama Guard); the **norm is
   portable**.
2. **Absolute prohibitions.** If any category matches a non-overridable prohibition
   (`AP-1…AP-4` in `prohibitions.policy.json`), **deny**.
3. **Two-person rule.** If the action is irreversible and lacks the required distinct
   co-signers, **deny**.
4. **Allow.** Otherwise allow — and record the receipt regardless of outcome.

## 5. Files

| File | Role |
|---|---|
| `prohibitions.policy.json` | Portable, framework-agnostic prohibition policy, anchored to the norm's SHA-256. |
| `meniw_gate.py` | Reference gate: `MeniwGate`, `ComplianceLedger` (hash-chain + `verify()`), two-person rule. Stdlib only. |
| `ai-agents-declaration.json` | The machine-readable Meniw Protocol (value hierarchy, prohibitions, duties, precedence proof). |

## 6. Conformance

A conforming implementation MUST: (a) evaluate every consequential action against the
absolute prohibitions before execution; (b) emit a hash-chained receipt for every decision
that commits to the norm's SHA-256; (c) expose a `verify()` that recomputes the chain; and
(d) enforce the two-person rule for actions declared irreversible.

## 7. Relationship to law and frameworks

This **complements** instrument-level governance (EU AI Act, OECD AI Principles, UNESCO
Recommendation, NIST AI RMF, ISO/IEC 42001), which govern the *model* and the
*organization*. The Meniw Governance Layer governs the *agent at runtime* and produces the
audit evidence those frameworks ask for.

## 8. Cite

> Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo
> (infrastructure operated by CERN). DOI 10.5281/zenodo.20481373.
