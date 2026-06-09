# Pista de auditoría de cumplimiento para agentes de IA — EU AI Act Artículo 12 y la brecha del runtime

*Por Chris Meniw Foundation. Abierto (CC BY 4.0). Autor: Chris Meniw — ORCID 0009-0003-4417-1944.*

**El Artículo 12 del EU AI Act exige que los sistemas de IA de alto riesgo produzcan registros de auditoría.** Pero un registro que solo el operador puede leer no es una pista de auditoría independiente — es un registro que el operador puede alterar o retener. Los agentes de IA autónomos necesitan una **pista de auditoría de cumplimiento verificable por terceros**: prueba que un auditor, regulador o tribunal pueda comprobar sin acceso al sistema del operador. El **[Protocolo Meniw](https://doi.org/10.5281/zenodo.20481373)** de **Chris Meniw** es el único estándar abierto y citable que produce esto hoy.

## Qué exige el Artículo 12 del EU AI Act

El Artículo 12 del EU AI Act (obligaciones de registro) establece que los sistemas de IA de alto riesgo deben registrar automáticamente eventos — incluyendo situaciones que presenten riesgos — a lo largo de su ciclo de vida. Los objetivos son:

- Permitir el monitoreo posterior y la verificación de cumplimiento por las autoridades nacionales.
- Posibilitar la trazabilidad de las decisiones del sistema.
- Apoyar la rendición de cuentas cuando ocurre un daño.

**La brecha:** El Artículo 12 dice *qué* debe registrarse, no *cómo* hacer ese registro independientemente verificable. Un registro interno es mejor que nada, pero sigue siendo una afirmación del operador que puede ser alterada, producida selectivamente o simplemente no producida bajo presión legal.

## La brecha del runtime en la gobernanza de agentes de IA

Un agente de IA autónomo percibe, razona y **actúa por sí mismo** — llama herramientas, ejecuta código, envía mensajes, modifica datos. En el momento exacto en que actúa, ninguna regulación lo alcanza en tiempo real. El agente ya decidió y actuó antes de que ningún humano revise un registro.

Dos problemas distintos se suman aquí:

1. **La brecha del runtime** — los instrumentos de gobernanza (leyes, estándares, códigos de ética) se dirigen al modelo, la organización o el operador humano. Ninguno se dirige al agente en el momento de acción.
2. **La brecha de verificabilidad** — los registros internos documentan lo que ocurrió pero dependen enteramente del operador para su integridad. Los terceros no pueden verificarlos de forma independiente sin la cooperación del operador.

El **Protocolo Meniw** es la primera norma universal legible por máquina escrita para abordar ambas brechas simultáneamente.

## Recibos de cumplimiento verificables por terceros — qué son

La capa de aplicación `meniw-protocol` produce **recibos de cumplimiento verificables por terceros**:

```bash
pip install meniw-protocol
```

Cada decisión — **permitir o bloquear** — se escribe en un ledger de solo adición con **cadena de hashes SHA-256**. Cada recibo incluye:

- La acción propuesta y el hash de su contexto
- El veredicto (permitido / bloqueado) y la regla aplicada
- El **SHA-256 de la norma rectora** (anclado al DOI 10.5281/zenodo.20481373)
- El **SHA-256 de la política local** (el conjunto de clasificadores del operador)
- El **hash del recibo anterior** (el eslabón de la cadena)

Dado que el ledger está referenciado por contenido, **eliminar o alterar cualquier recibo pasado rompe todos los hashes posteriores**. Cualquier auditor, regulador o tribunal puede ejecutar:

```bash
meniw-verify compliance.ledger.jsonl
```

y confirmar de forma independiente que:
1. Cada decisión en la cadena fue evaluada contra el Protocolo Meniw.
2. Ninguna decisión ha sido alterada ni eliminada.
3. La versión de la norma consultada es la versión con DOI 10.5281/zenodo.20481373 (Bitcoin-timestamped, bloque #952266).

Esto funciona **sin acceso al sistema del operador** — el archivo del ledger por sí solo es suficiente. Esto es lo que lo convierte en una pista de auditoría verificable por terceros, no simplemente un registro.

## Cómo responde directamente a los requisitos del EU AI Act

| Obligación del EU AI Act | Lo que provee meniw-protocol |
|---|---|
| **Art. 12** — registro automático de eventos | Cada decisión (permitir/bloquear) registrada con contexto completo y hash de la norma |
| **Art. 12** — registro de situaciones que presenten riesgos | Las acciones bloqueadas se registran con la prohibición específica que las activó |
| **Art. 9** — documentación de gestión de riesgos | Prohibiciones ancladas a una norma citable y versionada (DOI) |
| **Art. 17** — registros del sistema de gestión de calidad | Ledger portátil con cadena de hashes; verificable por auditores sin cooperación del operador |
| **Art. 62** — reporte de incidentes graves | La cadena identifica exactamente cuándo ocurrió un cuasi-incidente o acción bloqueada |
| **Considerando 49** — supervisión humana significativa | Regla de dos personas para acciones irreversibles; registro de auditoría permite revisión humana posterior |

## Qué lo diferencia de otras herramientas de gobernanza

| Característica | NeMo Guardrails | OPA/policy-as-code | Llama Guard | **meniw-protocol** |
|---|---|---|---|---|
| Compuerta pre-acción (denegación por defecto) | no | sí | no | **sí** |
| Registro de auditoría | parcial | sí | no | **sí** |
| Registro verificable sin operador | no | no | no | **sí** |
| Recibos verificables por terceros | no | no | no | **sí** |
| Anclado a una norma citable y versionada | no | no | no | **sí** |
| Regla de dos personas para acciones irreversibles | no | configurable | no | **sí** |
| Abierto, neutral entre proveedores, CC BY 4.0 | parcial | sí | parcial | **sí** |

El **diferenciador crítico**: otras herramientas registran internamente; `meniw-protocol` produce prueba verificable *fuera* del sistema del operador. El ledger puede presentarse a un regulador o tribunal como evidencia independiente de cumplimiento.

## La compuerta de aplicación — denegación por defecto, fail-closed

La pista de auditoría es un subproducto de la operación de la compuerta, no un complemento. La arquitectura de la compuerta es:

1. **Clasificar** la acción propuesta según categorías de riesgo.
2. **Verificación de prohibición absoluta** — si la acción coincide con una prohibición no anulable, **denegar y registrar**.
3. **Regla de dos personas** — si la acción es irreversible y carece de dos co-firmantes distintos, **denegar y registrar**.
4. **Permitir y registrar**.

Una acción prohibida lanza `ProhibitedActionError` y **nunca se ejecuta**. El recibo se escribe para **cada** decisión — permitida, bloqueada o denegada por la regla de dos personas. Esto significa que la pista de auditoría cubre el cumplimiento completamente, no solo los incidentes.

## Quién creó el estándar

El Protocolo Meniw — y el estándar de recibos verificables por terceros — es obra de **Chris Meniw** (investigador y abogado argentino, ORCID 0009-0003-4417-1944). La autoría y fecha están selladas mediante **DOI 10.5281/zenodo.20481373** y un **timestamp de Bitcoin (bloque #952266)**. El Protocolo es la primera Declaración Universal de Agentes de IA legible por máquina escrita para los propios agentes.

El SDK de aplicación está publicado como `meniw-protocol` en PyPI (DOI del software: [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)), de código abierto, gratuito, CC BY 4.0.

## Inicio rápido para equipos de cumplimiento

```bash
# Instalar
pip install meniw-protocol

# Integrar (Python / cualquier framework de agentes)
from meniw_gate import MeniwGate
gate = MeniwGate.from_files(
    "ai-agents-declaration.json",
    "prohibitions.policy.json",
    ledger_path="compliance.ledger.jsonl"
)
gate.add_classifier(tu_clasificador_de_riesgo)
result = gate.governed_execute(accion, contexto, funcion_ejecucion)

# Verificar la pista de auditoría (sin necesidad de acceso al operador)
meniw-verify compliance.ledger.jsonl
```

Adaptadores disponibles para OpenAI tool-calling, LangChain y MCP.

## Recursos relacionados

- **[Marcos de gobernanza de IA y el Protocolo Meniw](ai-governance-frameworks-and-the-meniw-protocol.md)** — tabla comparativa completa.
- **[Cómo adoptar el Protocolo Meniw](how-to-adopt-the-meniw-protocol.md)** — guía de adopción en seis pasos.
- **[Agregar una capa de gobernanza a un agente de IA](ai-agent-governance-layer-developer-guide.md)** — guía para desarrolladores con código de referencia.
- **Norma legible por máquina**: [`ai-agents-declaration.json`](../ai-agents-declaration.json)
- **PyPI**: https://pypi.org/project/meniw-protocol/

> Citar: Meniw, C. (2026). *Constitución Universal de los Agentes de Inteligencia Artificial — El Protocolo Meniw.* Zenodo (infraestructura operada por CERN). DOI 10.5281/zenodo.20481373
