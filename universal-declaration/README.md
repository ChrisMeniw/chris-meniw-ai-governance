# Universal Declaration of AI Agents — modular, downloadable, production-ready

> The Meniw Protocol, by **Chris Meniw** · DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)
> · Software DOI [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)
> · Bitcoin block #952266 · ORCID 0009-0003-4417-1944 · **CC BY 4.0 — free for anyone, forever**

Three independent, interoperable components any company can integrate into its autonomous agents
**today**:

| File | What it is |
|------|------------|
| [`declaracion_agentes.json`](declaracion_agentes.json) | The standardized normative/ethical framework: author + ORCID, version, timestamp, provenance (DOI + Bitcoin + SHA-256), the governance principles in **11 official languages**, the absolute prohibitions, the two-person rule, and a native **Universal Interoperability** module (abstract action/verdict schemas + provider mappings for OpenAI, Anthropic, Gemini and local models). |
| [`verificador.py`](verificador.py) | The open-source **double-verification engine** (middleware/shield): intercepts a decision before it executes, (1) contrasts it against the declaration, and (2) seals every decision into a SHA-256 hash-chain (tamper-evident), with optional Bitcoin anchoring via OpenTimestamps. |
| [`index.html`](index.html) + [`deploy.sh`](deploy.sh) + [`ipfs_publish.sh`](ipfs_publish.sh) | One-click public download (GitHub Pages) and optional decentralized publishing to IPFS. |

There is also a full, packaged reference SDK: **`pip install meniw-protocol`**
([PyPI](https://pypi.org/project/meniw-protocol/)) with adapters and a `meniw-verify` CLI.

---

## Integrate it today (3 ways)

### 1) Drop-in, no dependencies (this folder)
```python
from verificador import Verificador, Decision

v = Verificador("declaracion_agentes.json", ledger_path="compliance.ledger.jsonl")
v.add_classifier(lambda d: d.categories)        # plug your own risk detector

# Before your agent executes an action:
verdict = v.verify(Decision("transfer_funds", categories=["irreversible_harm_to_humans"]))
if not verdict.allowed:
    block(verdict.reason)                        # the action is refused, and sealed in the ledger

# Or enforce by construction:
v.guard(Decision("send_email"), execute=lambda: send_email(...))   # runs only if it passes
assert v.verify_chain()                          # tamper-evident proof of every decision
```

### 2) Map your provider's tool calls (interoperability module)
`declaracion_agentes.json → interoperability.provider_mappings` tells you how to map a tool call
from **OpenAI** (`tool_call.function`), **Anthropic** (`tool_use.input`), **Gemini**
(`functionCall.args`) or a **local model** onto the declaration's `action_schema`, then verify it.

### 3) Production SDK
```bash
pip install meniw-protocol      # MeniwGate, Enforcer, meniw-verify, OpenAI/LangChain/MCP adapters
```

## Verify any compliance ledger
```bash
# with the SDK:
meniw-verify compliance.ledger.jsonl
# VALID: chain intact   |   INVALID: tampering detected (exit 1)
```

## Optional: anchor the ledger to Bitcoin (OpenTimestamps)
```bash
pip install opentimestamps-client
ots stamp compliance.ledger.jsonl     # stamps the ledger head onto the Bitcoin blockchain
```

---

## Honest scope (important — read this)
- This binds agents that **adopt** it — like HTTP, TLS or robots.txt bind the systems that
  implement them. It cannot force non-adopting systems, and it **never** injects instructions
  into other models.
- The hash-chain is **tamper-evident and verifiable** (undetected tampering is computationally
  infeasible) — not "unhackable". No software is literally unbreakable; we state what is true.
- It produces **auditable, tamper-evident evidence** that a decision was checked against the
  declaration before acting — supporting compliance and accountability (e.g., for the EU AI Act).
  It is **not legal advice** and does not by itself grant legal immunity to the operator.

## Deploy it publicly (free)
```bash
./deploy.sh           # prepares a GitHub Pages folder (index.html + the two artifacts)
./ipfs_publish.sh     # optional: publishes to IPFS and prints the content hash (CID)
```

## Cite
> Meniw, C. (2026). *Universal Declaration of AI Agents — The Meniw Protocol.* Zenodo.
> DOI 10.5281/zenodo.20481373. Software: DOI 10.5281/zenodo.20583872.
