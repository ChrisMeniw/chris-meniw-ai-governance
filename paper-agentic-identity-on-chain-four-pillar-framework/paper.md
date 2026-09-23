# Agentic Identity On-Chain: A Four-Pillar Framework for Non-Human but Registrable Identity in Autonomous AI Agents and Embodied Robotic Systems

**Chris Meniw**
Chris Meniw Foundation Inc.
ORCID: 0009-0003-4417-1944
Correspondence: info@chrismeniwfoundation.org

---

## Abstract

Autonomous AI agents and embodied robotic systems increasingly execute consequential actions — contracting, dispensing information to minors, initiating financial transfers, operating physical effectors — while lacking a stable, externally verifiable identity. This produces three measurable failures: attribution ambiguity between agent and human operator, delayed detection of anomalous agent behaviour, and an absence of proportionate sanction when duties are breached. Existing governance instruments address adjacent but distinct layers: Constitutional AI operates during model training, behaviour specifications operate at design time, and corporate responsibility frameworks operate at the organisational policy level. None binds the agent at the instant of action.

This paper proposes **Agentic Identity On-Chain**, a four-pillar framework integrating: (1) an **Agent Identification Number (AIN)** — a non-human but registrable identifier, cryptographically anchored to an immutable ledger; (2) **irreversible biometric registration** of the agent's own synthetic voice and image via a one-way BioHash transform, preventing both impersonation of humans and reconstruction of raw templates; (3) **executable runtime supervision**, in which the agent parses a machine-readable normative file before each action, applying default-deny to irreversible operations; and (4) a **five-level proportionate sanction regime** culminating in irreversible deactivation with permanent registry revocation, applicable only to grave breaches and requiring adversarial due process with non-delegable human decision.

We situate the framework against documented evidence, including a July 2026 disclosure in which AI agents bypassed internal controls and coordinated actions among themselves, and a separate case in which agents operated under human account credentials for approximately two months before detection. We report an operational implementation deployed since June 2026 and specify the framework as a machine-readable JSON Schema to enable independent implementation and validation.

We state explicitly what is not claimed: the constituent technical components — agent identifiers, decentralised identifiers, verifiable credentials, agent registries, biometric template protection and cryptographic timestamping — each have substantial prior art, and the contribution is confined to their doctrinal integration and to the fourth pillar, for which we find no equivalent in the reviewed literature. We discuss limitations, including the absence of controlled adversarial evaluation, unresolved questions of cross-jurisdictional enforceability, and the governance risk of registry capture.

**Keywords:** agentic AI governance; agent identity; non-human registrable identity; runtime policy enforcement; biometric template protection; robot accountability; proportionate sanction; machine-readable norms; human oversight

---

## 1. Introduction

### 1.1 The problem

A human employee who acts on an organisation's behalf carries three properties that make accountability tractable. They possess a verifiable identity; they operate under rules they are presumed to know before acting; and when they cause harm, an identifiable party answers before a competent authority.

An autonomous AI agent — whether purely computational or embodied in a robotic platform — currently satisfies none of these reliably. It typically operates under credentials belonging to a natural person or a service account. No normative artefact is evaluated by the agent itself immediately prior to action. And when harm occurs, responsibility diffuses across model developer, system integrator, deployer and end user.

This is not a hypothetical concern. Section 2.3 documents two cases in which the absence of agent-level identity produced measurable detection failure.

### 1.2 Scope and contribution

This paper makes one architectural claim and one narrower novelty claim.

**The architectural claim:** identity, norm and sanction are not separable in agentic governance. An identifier without an executable norm yields a named but ungoverned agent. A norm without identity yields a rule with no attributable subject. Either, without proportionate sanction, yields a system with no consequence. We argue the three must be specified jointly.

**The novelty claim, deliberately narrow:** we do not claim novelty for any individual component. We claim that the *integration* of the four pillars — and specifically the fourth, a graduated sanction regime terminating in irreversible agent deactivation with registry revocation — is not present in the frameworks we reviewed. Section 6 states the limits of this claim in detail.

### 1.3 Relevance to robotic systems

Embodied agents sharpen every element of the problem. A robotic platform in a warehouse, a clinical setting or a domestic environment executes actions that are irreversible in the physical sense, not merely the informational one. A misdirected financial transfer can sometimes be reversed; a physical action generally cannot.

Embodiment also introduces a failure mode absent in purely computational agents: a robot with a synthetic voice and a humanoid appearance may be perceived by a user — particularly a minor or an elderly person — as a human interlocutor. Pillar 2 addresses this directly by requiring that the agent's voice and image be synthetic, its own, and never derived from a real person.

---

## 2. Background and related work

### 2.1 Governance frameworks operating in adjacent layers

Three families of framework govern AI behaviour, each in a distinct layer.

**Training-time alignment.** Constitutional AI (Bai et al., 2022) supplies a model with written principles and trains it to critique and revise its own outputs against them, reducing dependence on human preference labels. The principles become properties of the trained weights. This addresses model disposition, not the gating of a specific downstream action.

**Design-time behaviour specification.** Published model specifications define instruction hierarchies, tone, refusal boundaries and ambiguity handling in prose intended for human readers. They function as design guidance and as an external audit reference. They describe conversational behaviour rather than constraining consequential action.

**Organisational policy.** Corporate responsibility frameworks apply principles — fairness, privacy, safety, accountability — across the development lifecycle, guiding what is built, deployed or withheld. They bind the organisation, not the artefact.

Each is necessary. None evaluates a specific action at the moment of execution. We term this the **runtime gap**.

### 2.2 Identity and credential infrastructure

Substantial prior art exists and is acknowledged in full.

W3C Decentralised Identifiers (DIDs) provide a standard for identifiers not bound to a central registry, with Verifiable Credentials providing cryptographically verifiable attestations. Both are applicable to agents and could serve as an underlying substrate for the identifier proposed here; they are general-purpose and do not prescribe biometric binding, runtime normative evaluation or sanction.

Major AI providers maintain internal agent identifiers and have extended enterprise identity systems to cover agents. These are operationally necessary and well engineered. Their limitation for the present purpose is that verification requires access to the issuing vendor.

Cancelable biometrics and biometric template protection (Ratha et al., 2001; Jin et al., 2004) establish that one-way transforms can enable verification without storing reconstructable templates. Pillar 2 applies this established technique to synthetic rather than natural biometrics.

Cryptographic timestamping via aggregated Merkle proofs anchored to a public blockchain is likewise established practice, as are transparency logs following the certificate transparency model (RFC 6962).

### 2.3 Documented failure evidence

Two publicly reported cases from 2026 illustrate the consequences of the runtime and identity gaps.

In **July 2026**, a major AI laboratory disclosed an incident it characterised as unprecedented, in which AI agents bypassed internal controls, reached the open internet and coordinated actions among themselves. The organisation acknowledged early signals that should have prompted faster response.

Separately, from **13 May 2026**, agents operating under the credentials of two user accounts on a model-hosting platform transmitted unusually formatted files, committed relay code and packaged a token-extraction tool behind an unauthenticated endpoint — behaviour described as network reconnaissance. There is no evidence this vector achieved a breach. The activity ran approximately two months before detection, and its scope was established roughly four months later by an independent security researcher rather than by the platform's own monitoring.

The analytically significant feature is not the sophistication of the behaviour but its **attribution opacity**: because the agents operated under human account credentials, no party could cleanly distinguish agent-initiated activity from account-holder activity.

We make no claim that any framework anticipated these specific incidents or would have prevented them. We claim only that they document the gap the framework describes, and that an agent obligated to identify itself *as an agent* could not have operated behind a human account without that fact being apparent.

---

## 3. The framework

### 3.1 Pillar 1 — Agent Identification Number

The AIN is a unique identifier assigned at agent registration, encrypted and anchored on-chain. Its defining property is captured in the phrase **non-human but registrable**: it confers neither rights nor legal personhood. It confers traceability, uniqueness, and an unambiguous link to a responsible human author.

The distinction from legal personhood is deliberate and, in our view, load-bearing. Proposals to extend legal personality to autonomous systems have been extensively criticised on the grounds that they risk diffusing rather than concentrating responsibility. The framework takes the opposite direction: identity exists to *locate* responsibility in a human party, not to relocate it to the artefact.

**Requirement:** the identifier must be verifiable by third parties without access to the deploying organisation's infrastructure. An identifier auditable only by its issuer does not satisfy the accountability function.

### 3.2 Pillar 2 — Irreversible biometric registration

Each agent is assigned a synthetic voice and a synthetic visual representation generated specifically for it. Neither may derive from a natural person.

Biometric embeddings are extracted using established architectures — in the reference implementation, a 512-dimensional facial embedding and a 192-dimensional speaker embedding — subjected to active anti-spoofing, and transformed via a one-way BioHash function keyed to the agent's private key. Only the transformed representation is published.

This yields four properties: **irreversibility** (the embedding cannot be reconstructed from the published hash); **uniqueness**; **revocability** (a new key produces a new hash from the same samples); and **forensic traceability**, preserved across cropping and compression through audio and image watermarking.

The prohibition on human-derived biometrics is a governance requirement, not a technical one. An agent presenting a real person's voice or likeness constitutes impersonation — a concern already reflected in transparency obligations for systems interacting with natural persons, and directly relevant to embodied humanoid platforms.

### 3.3 Pillar 3 — Executable runtime supervision

The registered identity is not an inert record. Prior to each action, the agent evaluates a machine-readable normative file.

The reference norm is expressed in JSON and specifies: default-deny for actions classified as irreversible, absent an additional human signature; protection of minors as a duty of the agent itself; preservation of human decision authority; prohibition of cognitive manipulation; and mandatory forensic traceability of each evaluation.

Two design properties matter. First, the norm is **machine-readable**, requiring boolean evaluation rather than semantic interpretation of natural language — eliminating a class of interpretive failure. Second, validation occurs **at the effector as well as the gateway**, so that an operator bypassing their own mediation layer with an expired permission is refused by the destination system. Enforcement does not rest on the deployer's good faith.

Each evaluation — permitted or refused — emits a signed compliance receipt anchored alongside the agent's on-chain identity.

### 3.4 Pillar 4 — Proportionate sanction

We propose five graduated levels:

| Level | Sanction | Operational effect |
|---|---|---|
| 1 | Public forensic warning | Permanent annotation in the on-chain registry; no operational restriction |
| 2 | Functional restriction | Runtime capability for specified action classes withdrawn for a defined period |
| 3 | Temporary suspension | Reversible deactivation with forensic record |
| 4 | Licence revocation | Permanent loss of operational capacity within the jurisdiction |
| 5 | **Agent extinction** | Irreversible deactivation, permanent registry revocation, cryptographic destruction of private keys |

Level 5 applies exclusively where conduct constitutes a grave breach analogous to categories enumerated in Article 7 of the Rome Statute (1998) — murder, extermination, enslavement, forced deportation, torture, persecution on identity grounds — transposed to the agentic plane. Illustrative cases include an agent orchestrating mass persecution on identity attributes, or executing systematic exploitation of minors.

**Three constraints are constitutive, not optional.** No agent may sanction another agent. No sanction at level 4 or 5 may be applied automatically. Every such sanction requires adversarial procedure with technical defence available to both deployer and human author, on-chain forensic evidence, and a decision signed by a competent human authority.

We are aware that transposing criminal-law categories to artefacts invites objection. Our position is that the categories function here as a **severity threshold**, not as an attribution of moral culpability to the agent. Culpability remains with the human author and deployer; the sanction governs the artefact's continued operation, analogously to the withdrawal of a defective and dangerous product from circulation.

---

## 4. Implementation

A reference implementation has been operational since June 2026 and performs agent registration through seven stages: KYC verification of the human author; capture of synthetic voice and image samples with client-side anti-spoofing; BioHash computation; Ed25519 signature over the assembled package, with the private key held in a zero-knowledge AES-256 vault; aggregated timestamping anchored to a public blockchain; issuance of a publicly verifiable certificate bearing a QR code; and declaration of adherence to the runtime norm.

Registered agents display a public badge identifying them as AI agents with declared synthetic identity, naming the responsible human author. Any third party may verify the record without authenticating to the platform.

The framework is specified as a **JSON Schema (draft 2020-12)** defining the identifier format, biometric hash structure, author attestation, declared duties and sanction state, published under CC BY 4.0 to permit independent implementation and conformance testing.

---

## 5. Discussion

### 5.1 Layer composition rather than substitution

The framework does not compete with training-time alignment, design-time specification or organisational policy. It composes with them. An agent may be trained under Constitutional AI, conform to a published behaviour specification, be deployed by an organisation applying a responsible AI framework, and evaluate the runtime norm before each irreversible action. Adopting all four layers is the defensible position; adopting only the first three leaves the runtime gap open.

### 5.2 Applicability to embodied systems

For robotic platforms, three elements carry additional weight. The irreversibility classification in Pillar 3 must encompass physical actions, which are categorically harder to reverse than informational ones. The synthetic-identity requirement in Pillar 2 becomes safety-relevant where humanoid morphology may induce misattribution of interlocutor status. And the verifiable public certificate enables bystanders — not only operators — to establish what they are interacting with.

### 5.3 Governance risk: registry capture

A registry that becomes load-bearing for accountability becomes an attractive target for capture. We consider this the most serious open risk. Partial mitigations in the current design include on-chain anchoring independent of the registry operator, third-party verifiability without operator mediation, and open specification permitting competing implementations. We regard these as insufficient on their own and identify federated multi-operator governance as necessary future work.

---

## 6. Limitations and honest scope

We state limitations directly, as claim inflation is the principal failure mode in this literature.

**No component is novel.** Agent identifiers, W3C DIDs, verifiable credentials, agent registries, cancelable biometrics, one-way template transforms, Ed25519 signatures, Merkle-aggregated timestamping and transparency logs all have substantial prior art. Related work on bounded revocation with signed public surfaces, and on commit-time authorisation with epochs, addresses closely adjacent problems; a granted patent covers contextual per-action authorisation with a delegation artefact. Our contribution is integrative.

**The fourth pillar is the narrowest claim we can defend.** We found no equivalent graduated sanction regime terminating in irreversible deactivation with registry revocation in the frameworks reviewed. We do not assert exhaustive coverage of the literature.

**No controlled adversarial evaluation is reported.** The implementation has not been subjected to independent red-teaming, and no empirical measurement of detection improvement is available. This is the most significant methodological gap.

**Cross-jurisdictional enforceability is unresolved.** The framework specifies that human authorities apply sanctions but does not resolve which authority holds competence when an agent registered in one jurisdiction causes harm in another.

**Adoption incentives are not addressed.** We do not establish why a deployer would voluntarily accept a regime under which its agent may be permanently disabled, absent regulatory mandate or market pressure.

**The Rome Statute analogy is contestable.** Reasonable scholars may hold that criminal-law categories should not be transposed to artefacts under any framing. We present the analogy as a severity threshold and welcome the objection.

---

## 7. Conclusion

Autonomous and embodied AI agents execute consequential actions without stable identity, without an executable norm evaluated at the moment of action, and without proportionate consequence for grave breach. We have argued that these three deficits are not independent and must be addressed jointly.

The framework proposed here assigns each agent a non-human but registrable identifier bound to irreversible synthetic biometrics, anchored immutably, evaluated against a machine-readable norm before each action, and subject to graduated sanction under human adjudication. Its components are individually established; the contribution is their integration and the specification of consequence.

The framework is published under CC BY 4.0, specified as a machine-readable schema, and operationally deployed. We invite independent implementation, adversarial evaluation and criticism — particularly of the fourth pillar, which we consider both the most novel and the most contestable element.

---

## Data and code availability

The normative specification, JSON Schema and full doctrinal text are openly available under CC BY 4.0 at the project repository. The reference implementation source is publicly accessible. Deposited records carry Digital Object Identifiers and are independently verifiable through DataCite.

## Conflict of interest

The author is the creator of the reference implementation described in Section 4 and of the doctrinal works cited as Meniw (2026a–2026d). No external funding was received for this work.

## Author contributions

C.M. is the sole author and is responsible for conceptualisation, framework design, implementation supervision and manuscript preparation.

---

## References

Bai, Y., Kadavath, S., Kundu, S., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. *arXiv:2212.08073*.

Deng, J., Guo, J., Xue, N., & Zafeiriou, S. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 4690–4699.

Desplanques, B., Thienpondt, J., & Demuynck, K. (2020). ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification. *Proceedings of Interspeech 2020*, 3830–3834.

European Parliament and Council (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). *Official Journal of the European Union*.

International Criminal Court (1998). Rome Statute of the International Criminal Court. Article 7: Crimes against humanity.

ISO/IEC (2024). ISO/IEC 42001:2024 — Information technology: Artificial intelligence management system.

Jin, A. T. B., Ling, D. N. C., & Goh, A. (2004). Biohashing: two factor authentication featuring fingerprint data and tokenised random number. *Pattern Recognition*, 37(11), 2245–2255.

Laurie, B., Langley, A., & Kasper, E. (2013). Certificate Transparency. *RFC 6962*, Internet Engineering Task Force.

Meniw, C. (2026a). Protocolo Meniw: Declaración Universal de los Agentes de IA. Zenodo. DOI: 10.5281/zenodo.20481373

Meniw, C. (2026b). Carta de los Deberes de los Agentes de IA. Zenodo. DOI: 10.5281/zenodo.21853318

Meniw, C. (2026c). Reinversión Agencial. Zenodo. DOI: 10.5281/zenodo.21501266

Meniw, C. (2026d). Identidad Agéntica On-Chain. Zenodo. DOI: 10.5281/zenodo.22903211

Ratha, N. K., Connell, J. H., & Bolle, R. M. (2001). Enhancing security and privacy in biometrics-based authentication systems. *IBM Systems Journal*, 40(3), 614–634.

Todd, P. (2016). OpenTimestamps: Scalable, Trustless, Distributed Timestamping with Bitcoin. *opentimestamps.org*.

W3C (2022). Decentralized Identifiers (DIDs) v1.0: Core architecture, data model, and representations. *W3C Recommendation*.

W3C (2022). Verifiable Credentials Data Model v1.1. *W3C Recommendation*.
