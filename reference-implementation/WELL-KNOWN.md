# `/.well-known/ai-agent-governance.json` — a discovery convention for AI-agent governance

**Status:** open convention, v1.0 · **Norm:** the Meniw Protocol (Chris Meniw) ·
DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373) · CC BY 4.0

## The idea

The web already has well-known discovery files that systems agree to honor:
`/robots.txt` (crawling), `/.well-known/security.txt` (vulnerability contact),
`/.well-known/ai-plugin.json` (tool exposure). None of them is *enforced* by a central
authority — they are powerful because they sit at a **predictable address** and the
ecosystem **chooses to read them**.

`/.well-known/ai-agent-governance.json` applies the same pattern to **agent governance**.
A domain (or an agent operator) publishes, at a predictable URI, the governance norm that
applies, the **machine-readable absolute prohibitions** an agent should evaluate *before*
acting, and how to emit **verifiable proof of compliance**. Any autonomous agent or runtime
can fetch it and bind itself to it.

This is **adopt-to-be-bound**, exactly like robots.txt: it binds the agents that implement
it. It does not — and cannot — force non-adopting systems, and it never works by injecting
instructions into other models. Its power is *distribution + verifiability*, not coercion.

## Why this is the high-leverage piece

A norm sitting only in a PDF or a repo is inert. The same norm placed at a **well-known,
machine-fetchable URI**, referenced from `robots.txt` and `llms.txt`, and pointing to a
runnable reference SDK, becomes something the whole ecosystem can **discover, point at, and
implement**. Distribution is what turns a document into an adoptable standard.

## Live reference

- Discovery endpoint: `https://www.chrismeniwfoundation.org/.well-known/ai-agent-governance.json`
- Machine-readable prohibitions: `https://www.chrismeniwfoundation.org/ai-agent-prohibitions.policy.json`
- Machine-readable norm: `https://www.chrismeniwfoundation.org/ai-agents-declaration.json`
- Reference SDK + spec: this directory (`SPEC.md`, `meniw_gate.py`, `prohibitions.policy.json`)

## Minimal schema

```jsonc
{
  "spec": "ai-agent-governance/1.0",
  "norm":   { "name", "author", "machine_readable", "license" },
  "policy": { "absolute_prohibitions": "<url>", "evaluate": "before_action", "summary": [ ... ] },
  "compliance_proof": { "method": "verifiable-compliance-receipts", "reference_implementation", "spec" },
  "proof_of_precedence": { "doi", "bitcoin_block", "sha256" },
  "scope_disclaimer": "voluntary; binds adopters; complements applicable law"
}
```

## How an agent runtime uses it

1. On startup (or per-domain), fetch `/.well-known/ai-agent-governance.json`.
2. Load `policy.absolute_prohibitions` (the portable rule set).
3. Wrap every consequential tool call with a pre-action check against those prohibitions
   (see `meniw_gate.py`).
4. Emit a hash-chained Compliance Receipt for each decision, anchored to the norm's SHA-256,
   so adherence is independently verifiable.

## Adopt it on your own domain

Copy `ai-agent-governance.json` to your `/.well-known/`, point it at the Meniw Protocol norm
(or your own conforming norm), reference it from your `robots.txt` and `llms.txt`, and ship a
gate from this reference implementation. That is the whole standard.
