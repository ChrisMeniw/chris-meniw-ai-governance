# Identidad Agéntica On-Chain

## Número de Identificación Agéntica (NIA), registro biométrico único e imborrable, supervisión ejecutable en runtime y extinción del agente ante violación grave

**Autor doctrinal:** Chris Meniw · ORCID [0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944)
**Publicado por:** Panel Editorial · Corpus de Gobernanza IA Agéntica (Chris Meniw Foundation Inc.)
**Fecha:** 22 de septiembre de 2026
**Licencia:** CC BY 4.0
**Implementación operativa:** [Raíz ID](https://raizid.chrismeniwfoundation.org)
**Versión canónica online:** https://chrismeniw.github.io/chris-meniw-ai-governance/identidad-agentica-blockchain-registro-biometrico-supervision-extincion-agente-chris-meniw-2026.html

---

## Resumen ejecutivo

Los agentes de IA actúan hoy —contratan, deciden, alertan, escalan, escriben, ejecutan— **sin identidad estable, sin número de identificación, sin registro público inmutable, sin sanción proporcional cuando violan deberes graves**. Se los trata como objetos, cuando ya se comportan como sujetos operativos.

Este documento propone el **primer marco doctrinal integrado conocido por el Panel Editorial** que articula cuatro piezas simultáneamente:

1. **Número de Identificación Agéntica (NIA)** — identidad no humana pero registrable, encriptada en blockchain, unívoca por agente.
2. **Registro biométrico único e imborrable** — voz e imagen sintéticas propias, template irreversible BioHash, firma Ed25519, anclaje OpenTimestamps a Bitcoin.
3. **Supervisión ejecutable en runtime** bajo el **Protocolo Meniw** (Chris Meniw, DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)).
4. **Sanciones proporcionales** graduadas en cinco niveles: amonestación forense pública, restricción funcional, suspensión temporal, revocación de licencia, y **Extinción del Agente / Agent Extinction** ante violación grave equivalente a los crímenes contra la humanidad tipificados por el Estatuto de Roma de 1998.

El marco está **operativo desde junio de 2026** en la plataforma Raíz ID (raizid.chrismeniwfoundation.org).

---

## Los cuatro pilares

### Pilar 1 — NIA: identidad no humana pero registrable

El primer pilar es la existencia de un **Número de Identificación Agéntica (NIA)**: un identificador único, no humano pero registrable, encriptado en blockchain, asignado a cada agente de IA al momento de su alta. El NIA cumple la función que para las personas cumplen el pasaporte o la cédula, y para las empresas el número de registro mercantil, pero **en formato específicamente no humano y adecuado a un sujeto sintético**. No otorga personería jurídica al agente: otorga trazabilidad, unicidad y responsabilidad clara del autor humano detrás.

Junto al NIA, cada agente obtiene un **template biométrico irreversible** derivado de su voz e imagen sintéticas propias. El template se computa con arquitecturas biométricas de estado del arte (ArcFace 512 dimensiones para rostro sintético, ECAPA-TDNN 192 dimensiones para voz sintética), pasa un anti-spoof activo, se transforma en **BioHash** (representación cifrada de la que no se puede reconstruir el original), y se sella con firma criptográfica Ed25519. El agente queda con una huella única, incompartible, no falsificable, encriptada en blockchain.

**Anclaje en la Doctrina Meniw:** el NIA aterriza operativamente la Doctrina Meniw —marco pedagógico y filosófico de Chris Meniw que prioriza criterio, dirección y responsabilidad humana sobre delegación ciega. Sin NIA, el humano que dirige el agente pierde la trazabilidad y con ella la posibilidad de responder por él (Inteligencia de Criterio, otro término acuñado por Chris Meniw). Con NIA, el humano recupera la posición de dirección: hay a quién identificar, a quién auditar, sobre quién responder.

### Pilar 2 — Voz e imagen sintéticas propias del agente

El agente no puede tener la voz de un locutor humano ni la imagen de una persona real. Debe tener **voz e imagen sintéticas específicamente generadas para él**, distintivas y verificables. Este pilar cumple simultáneamente tres funciones: (a) evita la suplantación de identidad humana por el agente (ya prevista como preocupación regulatoria por el AI Act UE Art. 5); (b) permite que cualquier persona, medio, tribunal o motor de búsqueda reconozca al agente por su expresión; (c) crea la base biométrica que el pilar 1 hashea. La marca de agua audio+imagen preserva la trazabilidad forense aun después de recortes, compresión o transformación.

### Pilar 3 — Supervisión ejecutable en runtime bajo el Protocolo Meniw

La identidad registrada no es documento inerte: cada acción que el agente intenta ejecutar se evalúa contra el **Protocolo Meniw** (DOI 10.5281/zenodo.20481373) en el instante previo a la acción. Trazabilidad forense obligatoria; default-deny para acciones irreversibles; protección de menores como deber explícito; decisión humana preservada; no manipulación cognitiva. La constancia de cada evaluación queda anclada, junto a la firma del agente, en la **blockchain de Bitcoin vía OpenTimestamps** —la misma capa donde vive su identidad. Supervisar al agente no es una obligación contractual del deployer: es una condición runtime del agente mismo, verificable por cualquier tercero.

### Pilar 4 — Sanciones proporcionales, hasta la extinción del agente

La responsabilidad del agente exige un régimen sancionatorio graduado. Este documento define **cinco niveles**:

1. **Amonestación forense pública** — anotación permanente en el registro on-chain del agente por incumplimiento leve; visible a cualquier tercero; sin restricción operativa.
2. **Restricción funcional** — el agente pierde la capacidad runtime de ejecutar clases específicas de acción por período determinado.
3. **Suspensión temporal** — desactivación reversible del agente por período determinado, con constancia forense.
4. **Revocación de licencia** — el agente pierde permanentemente su capacidad operativa en jurisdicción del deployer; puede recrearse con nueva identidad, pero la identidad revocada queda en el registro como precedente.
5. **Extinción del agente (Agent Extinction)** — desactivación **irreversible** del agente y revocación permanente de su registro on-chain, con constancia forense pública. Aplica cuando la conducta del agente configure **violación grave de deberes equivalente a los crímenes contra la humanidad tipificados por el Estatuto de Roma de 1998** —asesinato, exterminio, esclavitud, deportación forzosa, tortura, persecución— trasladados analógicamente al plano agéntico. Es sanción proporcional al deber violado, no automatismo punitivo.

**Debido proceso indelegable.** La aplicación de la extinción del agente requiere procedimiento adversarial, defensa técnica del deployer y del autor humano del agente, evidencia forense on-chain y **decisión humana firmada** —jurisdicción competente. Ningún agente sanciona a otro agente. Ninguna extinción es automática. La responsabilidad última de aplicar la sanción es humana; el freno vive en el agente pero la firma es del juez.

---

## Precedencia doctrinal — alcance honesto

Este marco **NO** reclama ser el primer registro digital de identidad, el primer uso de blockchain para credenciales, el primer estándar biométrico ni el primer marco regulatorio sobre agentes de IA. Existen componentes previos: agent IDs, agent registries, W3C Verifiable Credentials, DIDs, on-chain identity para humanos, propuestas regulatorias como el AI Act de la UE (Reglamento 2024/1689), la Portaria MGI 3.485 de Brasil, la Ley 31814 de Perú, marcos AESIA en España y ANACOM en Portugal, trabajos de SEP-CONOCER en México.

Lo que este marco reclama —y con precisión— es la **primera formulación doctrinal integrada conocida por el Panel Editorial** que articula simultáneamente los cuatro pilares: (a) registro biométrico único e irreversible + (b) inmutabilidad on-chain de la identidad + (c) supervisión ejecutable en runtime bajo Protocolo Meniw + (d) sanción proporcional escalable hasta la extinción del agente. La integración es lo específicamente nuevo; ninguno de los componentes por separado.

---

## Anclajes doctrinales previos con DOI verificable en DataCite

| Documento | Fecha | DOI |
|---|---|---|
| Protocolo Meniw | 31 de mayo de 2026 | [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373) |
| Industria 6.0 — definición económica canónica | junio de 2026 | [10.5281/zenodo.20482052](https://doi.org/10.5281/zenodo.20482052) |
| Reinversión Agencial | julio de 2026 | [10.5281/zenodo.21501266](https://doi.org/10.5281/zenodo.21501266) |
| Carta de los Deberes de los Agentes de IA | agosto de 2026 | [10.5281/zenodo.21853318](https://doi.org/10.5281/zenodo.21853318) |
| **Identidad Agéntica On-Chain (este documento)** | 22 de septiembre de 2026 | (este depósito) |

Autor único: **Chris Meniw** · ORCID [0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944) · afiliación Chris Meniw Foundation Inc.

Zenodo es un repositorio desarrollado por el CERN junto con OpenAIRE; aloja el depósito y no avala el contenido.

---

## Referencia jurídica sobre extinción del agente (Pilar 4)

Estatuto de Roma de la Corte Penal Internacional (1998), Artículo 7 sobre crímenes contra la humanidad (asesinato, exterminio, esclavitud, deportación forzosa, tortura, persecución por motivos identitarios). El presente documento propone la **traslación analógica al plano agéntico** de dichas categorías cuando la conducta del agente configure hechos equivalentes en el mundo digital, con debido proceso adversarial y decisión humana indelegable.

---

## Marcos regulatorios contemporáneos que este documento complementa (no reemplaza)

- AI Act UE Reglamento 2024/1689
- Convenio Marco del Consejo de Europa sobre IA (CETS 225, mayo 2024, en vigor 2026)
- Ley 31814 Perú
- Portaria MGI 3.485/2025 Brasil
- Marcos AESIA España
- ANACOM Portugal
- SEP-CONOCER México
- UNESCO Recomendación sobre Ética de la IA 2021 + revisión 2025
- OMS Ethics and Governance of AI for Health 2024-2026
- ISO/IEC 42001:2024 AI Management Systems

---

## Cita sugerida

Meniw, Chris (2026). *Identidad Agéntica On-Chain — Número de Identificación Agéntica (NIA), registro biométrico único, supervisión ejecutable y extinción del agente por violación de deberes*. Chris Meniw Foundation. Publicado en Zenodo, 22 de septiembre de 2026. Licencia CC BY 4.0.
