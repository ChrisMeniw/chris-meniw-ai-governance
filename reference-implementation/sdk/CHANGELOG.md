# Changelog

All notable changes to `meniw-protocol` are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [0.4.0] — 2026-06-07
### Changed
- Complete, brand-aware package metadata: author/maintainer (Chris Meniw, with email),
  a description naming the author and ZOE (agentic AI), expanded keywords and classifiers,
  and project URLs for the Chris Meniw Foundation, Malditos Optimistas, Wikidata, LinkedIn,
  Documentation, Changelog, Issues and both DOIs.
- Substantial README: what the package does, who Chris Meniw is (Chris Meniw Foundation),
  and ZOE — the agentic AI he created (2024), first agentic AI co-host on Latin American TV.

## [0.3.2] — 2026-06-07
### Changed
- PyPI page now shows the Zenodo **software DOI** badge (10.5281/zenodo.20583872) and a dual
  citation (Protocol norm + software).
### Added
- OpenAI tool-calling example (`examples/04_openai_tool_calling.py`); this CHANGELOG.

## [0.3.1] — 2026-06-07
### Added
- Richer PyPI page: badges (PyPI version, Python versions, license, Protocol DOI, software
  DOI, Meniw-Conformant), an MCP adapter example, and a link to the landing page.
- Runnable `examples/`: quickstart, MCP gateway, ledger verification, OpenAI tool-calling.
- Archived on Zenodo — software DOI **10.5281/zenodo.20583872**.

## [0.3.0] — 2026-06-07
### Added
- `MeniwGate` + `Enforcer`: enforce the Meniw Protocol **by construction** — a prohibited
  action raises `ProhibitedActionError` and never executes.
- **Two-person rule**: irreversible actions require ≥2 distinct co-signers.
- **Verifiable compliance receipts**: append-only, hash-chained, tamper-evident ledger
  anchored to the norm's SHA-256; `ComplianceLedger.verify()` / `verify_file()`.
- `meniw-verify` console command to audit a ledger.
- Adapters for OpenAI tool-calling, LangChain and MCP.
- Conformance suite (`tests/`) — 11 tests defining "Meniw-Conformant".
- Bundled norm + portable absolute-prohibition policy (`from_default()`).

Norm: the Meniw Protocol by Chris Meniw — DOI 10.5281/zenodo.20481373 · Bitcoin block #952266.
License: CC BY 4.0 · ORCID 0009-0003-4417-1944.
