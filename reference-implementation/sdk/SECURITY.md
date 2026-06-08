# Security & threat model

`meniw-protocol` is an **opt-in, in-process policy-enforcement + tamper-evident audit layer** for
AI-agent tool-calls. This document states plainly what it defends against and what it does **not** —
because a guardrail that oversells its guarantees is worse than none.

## What it defends against

- **A misbehaving, jailbroken or prompt-injected agent that still dispatches its tool-calls through
  the gate.** Under default-deny, an action runs only if an explicit `allow` rule matches; anything
  else is blocked. An injected instruction cannot add itself to your allowlist, so the destructive
  tool-call it triggers does not execute. This is the primary, real value.
- **Silent non-compliance.** Every decision (allow/deny) is recorded in a hash-chained ledger and
  can be exported as a portable bundle a third party verifies independently (`meniw verify-receipt`).

## What it does NOT defend against (named, not hidden)

1. **Arbitrary code execution on the host.** This is an **in-process** library. If the agent (or an
   attacker) can run arbitrary Python in your process, it can monkeypatch the gate, call the
   underlying tool function directly, or rewrite the ledger. No in-process control survives full code
   execution. **For that threat, run enforcement out-of-process** — at an MCP server, an API proxy,
   or a sidecar the agent must talk to over IPC — so the agent never holds the gate in its own memory.
   The adapters (OpenAI tool-calling, LangChain, MCP) are designed to support that boundary.
2. **Tools you don't route through it (firewall scope).** Like a firewall, it only sees the traffic
   that traverses it. A tool the operator never wires to the gate is uncovered. Run `meniw policy-lint`
   and `meniw audit` to find gaps; covering all dangerous tools is the operator's responsibility.
3. **Forged co-signers.** The two-person rule checks for two *distinct co-signer identities*. Those
   identities **must be injected by your trusted control plane, never derived from model/agent
   output.** If you let the agent populate `cosigners`, it can self-approve and the rule is theater.
   Treat `_gov={"cosigners": [...]}` like a privileged credential. (Signed/authenticated approvals are
   the recommended production pattern.)
4. **Full ledger rewrite without an anchor.** A plain hash-chain detects edits and removals, but
   someone who controls the file can recompute the *entire* chain and it will still verify. To detect
   a full rewrite you need **authenticity** (an HMAC key kept out of the agent's reach) **or an
   external anchor** (Bitcoin via OpenTimestamps on the head). `verify-receipt` reports the assurance
   level (`hmac-authenticated` vs `integrity-only`) so you never mistake one for the other.
5. **Name-based evasion of allow rules.** Matching on tool *name* is a convenience. For
   security-critical tools, declare explicit `categories=[...]` (capability-based) rather than relying
   on name patterns, so a renamed tool can't slip into an allow rule.

## Hardening checklist for operators

- Run the gate **out-of-process** for adversarial threat models (MCP/proxy/sidecar).
- Supply an **HMAC key** the agent cannot read, and **anchor the ledger head** periodically
  (`meniw anchor`).
- Source **co-signers from a trusted control plane**, not from the model.
- Keep the **policy in a versioned file**, gate CI on `meniw policy-lint` (it fails on dangerous or
  too-broad allow rules).
- Prefer **explicit categories** over name patterns for irreversible/lethal tools.

## Scope of guarantees, in one line

Deterministic enforcement and tamper-EVIDENT audit for the tool-calls an operator routes through it.
Not "unhackable", not a defense against a fully compromised host, not binding on non-adopting systems.

## Responsible disclosure

Found a vulnerability or a way the guarantees break? Email **info@chrismeniwfoundation.org**. Please
do not open a public issue for security-sensitive reports until we have had a chance to respond.
