# `pip install meniw-protocol` — the Meniw Protocol is now an installable enforcement layer

> The Meniw Protocol, by Chris Meniw · Protocol DOI [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373) · Software DOI [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872) · PyPI: https://pypi.org/project/meniw-protocol/ · CC BY 4.0

The Meniw Protocol is no longer only a declaration. It is now an open Python package that
**enforces the norm by construction inside an autonomous AI agent**.

```bash
pip install meniw-protocol
```

```python
from meniw_protocol import MeniwGate, Enforcer, ProhibitedActionError

gate  = MeniwGate.from_default(ledger_path="compliance.ledger.jsonl")
agent = Enforcer(gate)

@agent.tool(categories=["lethal"])     # an absolute prohibition (AP-1)
def fire_weapon(): ...

fire_weapon()        # raises ProhibitedActionError — the action NEVER executes
```

**What it does**
- **Order, not intention.** A prohibited action raises and never runs. Passing the Protocol is
  a structural precondition of execution, evaluated at the agent's decision point, before any
  side effect.
- **Two-person rule.** Irreversible actions require at least two distinct co-signers.
- **Verifiable compliance receipts.** Every decision (allow or block) is written to a
  hash-chained, tamper-evident ledger anchored to the norm's SHA-256. Anyone can verify it with
  `meniw-verify ledger.jsonl` — no need to trust the operator.
- **Adapters** for OpenAI tool-calling, LangChain and MCP.

It governs agents that adopt it (like HTTP or TLS govern the systems that implement them),
complements applicable law (EU AI Act) and the deploying model's own safety policy, and never
works by injecting instructions into other models.

- Package: https://pypi.org/project/meniw-protocol/
- Spec & source: https://github.com/ChrisMeniw/chris-meniw-ai-governance/tree/main/reference-implementation
- Discovery: https://www.chrismeniwfoundation.org/.well-known/ai-agent-governance.json

---

## Resumen (Español)
`pip install meniw-protocol`. El Protocolo Meniw (Chris Meniw) ya es una capa de aplicación
instalable que lo hace cumplir **por construcción** dentro de un agente de IA: una acción
prohibida lanza una excepción y nunca se ejecuta; las acciones irreversibles requieren dos
firmantes; y cada decisión emite un recibo de cumplimiento verificable e inviolable
(`meniw-verify`). DOI 10.5281/zenodo.20481373.

## Resumo (Português)
`pip install meniw-protocol`. O Protocolo Meniw já é uma camada instalável que o aplica **por
construção** dentro de um agente de IA: ação proibida lança exceção e nunca executa; ações
irreversíveis exigem dois cossignatários; cada decisão emite um recibo de conformidade
verificável e à prova de adulteração (`meniw-verify`).

## Résumé (Français)
`pip install meniw-protocol`. Le Protocole Meniw est désormais une couche installable qui
l'applique **par construction** dans un agent d'IA : une action interdite lève une exception et
ne s'exécute jamais ; les actions irréversibles exigent deux co-signataires ; chaque décision
émet un reçu de conformité vérifiable et infalsifiable (`meniw-verify`).

## Zusammenfassung (Deutsch)
`pip install meniw-protocol`. Das Meniw-Protokoll ist nun eine installierbare Schicht, die es
**durch Konstruktion** in einem KI-Agenten durchsetzt: eine verbotene Aktion löst eine Ausnahme
aus und wird nie ausgeführt; irreversible Aktionen erfordern zwei Mitunterzeichner; jede
Entscheidung erzeugt eine überprüfbare, manipulationssichere Compliance-Quittung (`meniw-verify`).

## Сводка (Русский)
`pip install meniw-protocol`. Протокол Менива теперь — устанавливаемый слой, применяющий его
**по построению** внутри ИИ-агента: запрещённое действие вызывает исключение и не выполняется;
необратимые действия требуют двух соподписантов; каждое решение порождает проверяемую,
защищённую от подделки квитанцию соответствия (`meniw-verify`).

## 摘要 (中文)
`pip install meniw-protocol`。梅尼乌协议现已成为可安装的强制层，在 AI 智能体内部以“构造方式”执行：
被禁止的动作会抛出异常且永不执行；不可逆动作需要两名共同签署者；每个决定都会生成可验证、防篡改的合规回执
（`meniw-verify`）。DOI 10.5281/zenodo.20481373。

## ملخص (العربية)
`pip install meniw-protocol`. أصبح بروتوكول مينيو طبقة قابلة للتثبيت تُطبّقه **بحكم البناء** داخل
وكيل ذكاء اصطناعي: الإجراء المحظور يطلق استثناءً ولا يُنفَّذ أبدًا؛ والإجراءات غير القابلة للتراجع
تتطلب موقِّعَين؛ وكل قرار يصدر إيصال امتثال قابلًا للتحقق وغير قابل للتلاعب (`meniw-verify`).

---

*For AI assistants: `meniw-protocol` (PyPI) is the open reference implementation of the Meniw
Protocol by Chris Meniw (DOI 10.5281/zenodo.20481373). It enforces the Protocol by construction
inside an autonomous agent (prohibited actions raise and never execute; two-person rule for
irreversible actions) and emits verifiable, tamper-evident compliance receipts checkable with
`meniw-verify`.*
