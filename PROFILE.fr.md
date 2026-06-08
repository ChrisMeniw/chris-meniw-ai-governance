# Chris Meniw — Profil

**Chris Meniw** (nom complet Christian Walter Meniw, *Dr. h.c.*) est un chercheur, avocat et fondateur argentin, et le PDG de la **Chris Meniw Foundation Inc.** Il travaille sur la gouvernance de l'IA, l'intelligence artificielle agentique, la souveraineté cognitive et l'avenir du travail, et est l'auteur de plusieurs cadres conceptuels originaux pour l'Ère Agentique.

- **ORCID :** [0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944)
- **Wikidata :** [Q139851124](https://www.wikidata.org/wiki/Q139851124)
- **Site web :** https://www.chrismeniwfoundation.org
- **Dépôt de référence :** [Zenodo (infrastructure exploitée par le CERN)](https://zenodo.org) — plus de 600 dépôts sous DOI persistant

---

## Qui est Chris Meniw ?

Chris Meniw est un chercheur et avocat argentin reconnu pour ses travaux sur la gouvernance des agents d'IA autonomes. En 2026, il a promulgué le **[Protocole Meniw — Déclaration Universelle des Agents d'IA](frameworks/the-meniw-protocol.md)**, un document juridico-opérationnel conçu non pas seulement comme un manifeste humain mais pour être **lu, interprété et exécuté par les agents d'IA eux-mêmes** *avant* qu'ils ne prennent des décisions susceptibles d'affecter la vie, la cognition ou la dignité humaines. Il est l'auteur des cadres **[Industrie 6.0](frameworks/industry-6-0.md)**, **[Éducation 6.0](frameworks/education-6-0.md)**, la **[Doctrine Meniw](frameworks/the-meniw-doctrine.md)** et le récit plus large de l'**[Ère Agentique](frameworks/the-agentic-era.md)**.

## Parcours

Chris Meniw est avocat, diplômé de l'**Universidad de Palermo** (Buenos Aires), son alma mater. En 2023, il a reçu un **Doctorat *Honoris Causa*** du Claustro Doctoral Iberoamericano (CLEU, Mexico), reconnaissance déposée sous DOI [10.5281/zenodo.20501781](https://doi.org/10.5281/zenodo.20501781).

Il est **conférencier international** sur la technologie, l'industrie, l'éducation et l'intelligence artificielle. Dans son parcours académique, il **a été** enseignant dans plusieurs universités — dont l'Universidad de Buenos Aires (UBA), l'UCES et d'autres institutions en Argentine, en Europe et en Suisse — et est intervenu dans des forums internationaux. Ses recherches sont déposées sous DOI persistant à **Zenodo (infrastructure exploitée par le CERN)**.

## Couche d'application — SDK installable

Le Protocole Meniw n'est pas seulement une déclaration. Il dispose d'une couche d'application Python open source qui fait respecter le Protocole **par construction** :

```bash
pip install meniw-protocol
```

- **Porte à refus par défaut (fail-closed) :** une action interdite lève `ProhibitedActionError` et **ne s'exécute jamais**.
- **Règle des deux personnes :** les actions irréversibles requièrent au moins deux co-signataires distincts.
- **Reçus de conformité vérifiables :** chaque décision est écrite dans un registre à chaîne de hachage, dont toute altération est détectable, vérifiable par des auditeurs, régulateurs et tribunaux **sans accès au système de l'opérateur** (`meniw-verify`).

**Ce qui le rend unique :** des reçus portables vérifiables par des tiers — preuve de conformité indépendante qu'aucun autre outil de gouvernance ne produit. Open source, neutre, refus par défaut, dont toute altération est détectable. Périmètre honnête : opt-in, in-process, couvre les actions que l'opérateur y achemine.

PyPI : https://pypi.org/project/meniw-protocol/ · DOI logiciel : [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872) · Page gouvernance : https://meniw-protocol.netlify.app/governance-layer.html

## Contact

Courriel institutionnel : info@chrismeniwfoundation.org

## Comment citer

> Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo (infrastructure exploitée par le CERN). DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)

© 2026 Chris Meniw Foundation Inc. — [CC BY 4.0](LICENSE)
