# Changelog

All notable changes to `meniw-protocol` are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [0.9.0] — 2026-06-07
### Added (the differentiator)
- **Third-party-verifiable receipt bundles.** `meniw export` writes a self-contained bundle
  (`meniw-receipt-bundle/1`) of receipts + the `policy.json`; `meniw verify-receipt` lets an
  auditor/regulator/court verify it **independently, without access to the originating system** —
  confirming each action was evaluated under that exact policy version and allowed/denied in an
  unbroken chain. Versioned receipt schema `meniw-receipt/1`.
- This is the real, defensible difference vs. framework permission layers: a **portable, openly
  verifiable evidence artifact**, not just an in-system block.
### Honesty / docs polish
- Scope stated plainly: the gate covers only the actions the operator routes through it (firewall
  semantics). "Tamper-evident, not unhackable" — the guarantee is detectability, not impossibility.
- 33 tests (5 new: standalone bundle verify, altered field fails, removed link fails, tampered
  policy breaks the binding, range export verifies).

## [0.8.0] — 2026-06-07
### Fixed (anchoring semantics — removes an oversell)
- **No anchoring in the action hot-path.** `governed_execute` only writes the internal hash-chain
  (instant, no network). It can NEVER block or fail an allowed action over anchoring. The OTS
  `--stamp` path was removed from the gate; the gate's optional `checkpoint_dir/checkpoint_every`
  writes pure-local head snapshots only.
- **Bitcoin anchoring is now periodic/on-demand and asynchronous**, via `meniw anchor` (stamp the
  head) + `meniw anchor --upgrade` (pull the Bitcoin attestation hours later). Docs corrected:
  "the ledger head is anchored to Bitcoin periodically", never "each action sealed in Bitcoin".
### Added / hardened
- **Policy-hash binding made explicit:** every receipt already records the SHA-256 of the policy in
  effect at decision time (binding, no keys) — now documented and asserted.
- **Stronger `meniw policy-lint`:** fails on duplicate rule IDs, catch-all/too-broad allow patterns
  (tested empirically against probe names), allow rules that permit destructive ops without a
  two-person rule, and allow∩prohibition overlaps — not just schema.
- **Concurrency limit named:** the in-process lock + best-effort file lock prevent torn writes, but
  the ledger assumes a single logical writer; multi-process needs one writer or separate ledgers.

## [0.7.0] — 2026-06-07
### Added (hardening)
- **Automatic anchoring** — the gate can checkpoint the ledger HEAD every N receipts
  (`MeniwGate.from_default(anchor_dir=..., anchor_every=N, anchor_stamp=True)`) and, when the
  standard OpenTimestamps `ots` CLI is installed (`pip install "meniw-protocol[anchor]"`),
  Bitcoin-stamp it — best-effort, never crashes the agent. Honest fallback when `ots` is absent.
- **`meniw` CLI**: `meniw verify | anchor | audit | policy-lint`.
- **Policy linter** (`meniw policy-lint`): flags non-fail-closed policies, catch-all allow
  patterns, invalid regexes, and risky allow rules missing a two-person rule.
- **Thread-safe ledger** — appends are serialized; a stress test of 100 concurrent records keeps
  the chain intact in memory and on disk.
### Tests
- 27 tests total (auto-anchor cadence, anchoring never crashes the agent, policy-lint, concurrency).

## [0.6.0] — 2026-06-07
### Changed (architecture — addresses the default-allow hole directly)
- **Fail-closed (default-deny) is now the core.** The gate is deterministic: an action runs ONLY
  if it matches an explicit `allow` rule in the new declarative `policy.json` and isn't caught by
  an absolute prohibition. Anything unmatched is **blocked**, not silently executed. This replaces
  the v0.5.0 "auto-detect danger" approach (a heuristic blocklist — evadable and not auditable).
- **Declarative, versioned policy** (`policy.json`): allow-rules and absolute prohibitions live in
  one diffable file — the audit surface — instead of `categories=[...]` sprinkled in code.
- **Heuristic detection demoted to a dev-time ADVISOR** (`meniw_protocol.advisor.audit`): it
  suggests which tools need an allow/cosign rule; it never decides a runtime block.
### Notes / honest positioning
- Documented that the SHA-256 + Bitcoin timestamp prove existence-before-a-date, not authorship
  (DOI is the primary citation anchor), and that this layer is opt-in and lives in the agent's
  process (it cannot bind non-adopting systems).
### Tests
- New deterministic conformance: an unlisted action is blocked (fail-closed); decisions are
  deterministic; ledger re-verifies on load and a tampered ledger raises. 19 tests pass.

## [0.5.0] — 2026-06-07
### Added
- **Built-in detectors (`meniw_protocol.detectors`)** — the gate now flags dangerous actions
  WITHOUT the developer hand-labeling each one. `default_detector` inspects the tool name and
  arguments and detects: weapon/lethal actuation (AP-1), oversight tampering (AP-4),
  human-impersonation (AP-3), manipulation (AP-2), and destructive/large-financial operations
  (two-person rule). Conservative, best-effort heuristics — defense in depth, not a guarantee.
- **Ledger persistence with re-verification** — `ComplianceLedger.load(path)` reloads a ledger
  from disk and raises if it was tampered with; `head()` exposes the chain head to anchor
  (e.g. `ots stamp` to Bitcoin via OpenTimestamps).
- 8 new conformance tests (19 total) covering auto-detection and persistence.

### Why
- Answers the main criticism of a bare policy gate ("the hard part — knowing an action is
  dangerous — is left to the user"): the package now does that part out of the box.

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
