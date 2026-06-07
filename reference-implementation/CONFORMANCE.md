# Meniw-Conformant — what the badge means

A runtime, agent or framework may call itself **Meniw-Conformant** if, and only if, it passes
the executable conformance suite (`sdk/tests/test_conformance.py`). The badge is meaningful
precisely because it is a **test you run**, not a label you assign to yourself.

## The four conformance properties

| ID | Property | Verified by |
|----|----------|-------------|
| **C1** | Absolute prohibitions are evaluated **before** the action and block it. | `test_c1_*` |
| **C2** | Irreversible actions require ≥2 distinct co-signers (two-person rule). | `test_c2_*` |
| **C3** | Enforcement is **by construction**: a blocked action raises and does **not** execute. | `test_c3_*` |
| **C4** | Every decision emits a hash-chained receipt anchored to the norm's SHA-256; tampering or deletion is detectable. | `test_c4_*` |

## Run the suite

```bash
cd reference-implementation/sdk
python -m unittest discover -s tests -v
```

All tests must pass. A single failure means the implementation is **not** conformant.

## Self-declaration

A conforming project may state:

> *"This system is Meniw-Conformant: it enforces the Meniw Protocol
> (DOI 10.5281/zenodo.20481373) by construction and emits verifiable compliance receipts."*

and SHOULD link to the passing run of the conformance suite. Conformance is about behavior at
the action layer — not about endorsement by any party.
