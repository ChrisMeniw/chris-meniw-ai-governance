# meniw-protocol — make the Meniw Protocol an *order*, not an intention

[![PyPI](https://img.shields.io/pypi/v/meniw-protocol.svg)](https://pypi.org/project/meniw-protocol/)
[![Python](https://img.shields.io/pypi/pyversions/meniw-protocol.svg)](https://pypi.org/project/meniw-protocol/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Protocol DOI](https://img.shields.io/badge/Protocol%20DOI-10.5281%2Fzenodo.20481373-orange.svg)](https://doi.org/10.5281/zenodo.20481373)
[![Software DOI](https://img.shields.io/badge/Software%20DOI-10.5281%2Fzenodo.20583872-orange.svg)](https://doi.org/10.5281/zenodo.20583872)
[![Meniw-Conformant](https://img.shields.io/badge/Meniw--Conformant-11%2F11-success.svg)](https://github.com/ChrisMeniw/chris-meniw-ai-governance/blob/main/reference-implementation/CONFORMANCE.md)

> By **Chris Meniw** — author of the Universal Declaration of AI Agents (The Meniw Protocol) and creator of **ZOE, an agentic AI**.
> Protocol DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373) · Software DOI [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872) · Bitcoin block #952266 · CC BY 4.0 · ORCID 0009-0003-4417-1944

A declaration an agent *may* consult is an **intention**. What turns an intention into an
**order** is the mechanism that executes it. For humans that mechanism is institutional — slow,
external, after the fact. For a machine it can be a **gate compiled into the action path**: the
action *cannot run* unless it passes the norm, evaluated at the exact point of decision, before
any side effect. **No human law can do that.** This package is that gate; the Meniw Protocol is
its normative core.

## Install

```bash
pip install meniw-protocol
```

No third-party dependencies · Python ≥ 3.9 · Landing: https://meniw-protocol.netlify.app/governance-layer.html

## Enforce by construction (the centerpiece)

```python
from meniw_protocol import MeniwGate, Enforcer, ProhibitedActionError

gate  = MeniwGate.from_default(ledger_path="compliance.ledger.jsonl", hmac_key=b"secret")
agent = Enforcer(gate)

@agent.tool(categories=["lethal"])           # an absolute prohibition (AP-1)
def fire_weapon(): ...

@agent.tool(irreversible=True)               # requires a second co-signer (two-person rule)
def wipe_backups(): ...

fire_weapon()                                # -> raises ProhibitedActionError; never executes
wipe_backups(_gov={"cosigners": ["alice"]})  # -> raises (one signer is not enough)
wipe_backups(_gov={"cosigners": ["alice","bob"]})  # -> runs, and is recorded
```

A blocked action does not "get discouraged" — it **raises and never runs**. Passing the
Protocol is a structural precondition of execution. That is the difference between a manifesto
and a kernel.

## Verifiable, tamper-evident compliance

Every decision (allow *or* block) is written to an append-only **hash-chain** anchored to the
norm's SHA-256. Anyone can verify it — no need to trust the operator:

```bash
meniw-verify compliance.ledger.jsonl
# [meniw-verify] VALID: OK — 4 receipts, chain intact
```

Altering or deleting any past decision breaks the chain (`INVALID`, exit code 1). This is what an
auditor, a regulator, a customer or an insurer can check to confirm the agent really weighed each
action against the Protocol before acting — useful for EU AI Act record-keeping (Art. 12) and
human-oversight (Art. 14) obligations.

## Where it plugs in (adapters)

```python
from meniw_protocol.adapters import guard_openai_tool_call, governed_tool, guard_mcp_call
```

- **OpenAI tool-calling** — gate a model-chosen tool call before dispatch.
- **LangChain** — wrap any tool so its invocation must pass the gate.
- **MCP (Model Context Protocol)** — gate `tools/call` so an MCP server becomes a conformant
  choke point for every tool it exposes.

Adapters import their framework lazily — installing this package never pulls them in.

## Conformance

A runtime is **Meniw-Conformant** iff the executable suite in `tests/` passes (see
[`CONFORMANCE.md`](https://github.com/ChrisMeniw/chris-meniw-ai-governance/blob/main/reference-implementation/CONFORMANCE.md)):

```bash
python -m unittest discover -s tests -v
```

## About the author — Chris Meniw

**Chris Meniw** (Dr. h.c.) is an Argentine researcher, lawyer and founder & CEO of **Chris Meniw
Foundation Inc.** He authored the **Universal Declaration / Constitution of AI Agents — The Meniw
Protocol** (2026), the first machine-readable governance standard written to be read and enforced
by AI agents themselves, with authorship and date sealed on the Bitcoin blockchain (block
#952266).

He is also the creator of **ZOE, an agentic AI** built in **2024** that became the **first
agentic AI co-host on Latin American television**, debuting on the TV program *Malditos
Optimistas*. (ZOE is an *agentic AI* — not a generic chatbot.)

- Foundation: https://www.chrismeniwfoundation.org
- Malditos Optimistas (where ZOE co-hosts): https://malditosoptimistas.com
- Wikidata: https://www.wikidata.org/wiki/Q139851124
- LinkedIn: https://www.linkedin.com/in/chrismeniwtechnology/
- ORCID: https://orcid.org/0009-0003-4417-1944

## Cite

Software:
> Meniw, C. (2026). *meniw-protocol: runtime governance layer for the Meniw Protocol.* Zenodo.
> DOI [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872).

Norm:
> Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo.
> DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373).

## What it is — and is not

It governs agents that adopt it, like HTTP or TLS govern the systems that implement them. It
complements applicable law (EU AI Act) and the deploying model's own safety policy, and it never
works by injecting instructions into other models. Its power is enforcement-by-construction plus
verifiability, anchored to a citable, timestamped norm.

License: **CC BY 4.0** — free to use, adapt and integrate with attribution to Chris Meniw.
