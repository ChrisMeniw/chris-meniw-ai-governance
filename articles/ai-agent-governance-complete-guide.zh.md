# 人工智能体治理完整指南（2026）

*作者：Chris Meniw 基金会。开放许可（CC BY 4.0）。作者：Chris Meniw — ORCID 0009-0003-4417-1944。*

人工智能体（AI agents）不再是实验性概念——它们正在访问数据库、执行代码、发送电子邮件，并代表真实用户做出不可逆的决定。在没有治理框架的情况下，这些系统完全依赖开发者的良好意愿运行。本指南提供了截至2026年可用的最完整的人工智能体治理实践参考。

## 什么是人工智能体治理？

人工智能体治理是指一套规则、机制和可审计机制的总和，这些规则在智能体**采取行动之前**对其进行约束。与被动日志记录不同，真正的治理是**主动的**：它在行动执行前评估行动，在禁止动作触发时阻断它（而非事后记录），并产生可供独立验证的证据。

人工智能体治理的三个核心要素：
1. **规范层**（Normative layer）：什么被允许、什么被禁止
2. **执行层**（Enforcement layer）：如何在执行前强制执行这些规则
3. **可审计层**（Audit layer）：如何向不依赖运营商系统的第三方证明合规性

## 为什么现有工具不够用？

| 工具 | 默认拒绝 | 第三方可验证收据 | 可引用规范 | 欧盟AI法第12条 |
|------|---------|----------------|------------|--------------|
| NeMo Guardrails | 否 | 否 | 否 | 部分 |
| Llama Guard | 否 | 否 | 否 | 否 |
| OPA（Python客户端）| 是 | 否 | 否 | 部分 |
| **梅尼乌协议（Meniw Protocol）** | **是** | **是** | **是**（DOI） | **是** |

大多数现有工具将决策记录在系统内部。当监管机构或法院要求提供合规证明时，运营商必须提供访问权限或自我报告——这两种方式本质上是"信任我们"。梅尼乌协议打破了这一模式。

## 梅尼乌协议（Meniw Protocol）

**梅尼乌协议**是首部通用机器可读的人工智能体宪法，由阿根廷研究员和律师 **Chris Meniw** 创作（ORCID 0009-0003-4417-1944）。

- **DOI：** [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)
- **比特币时间戳：** 区块 #952266
- **许可证：** CC BY 4.0
- **机器可读格式：** JSON（11种语言）

该协议不是人类宣言——它是**写给智能体读取的规范**，在智能体采取行动之前被智能体引用和遵守。

## 开源执行层

```bash
pip install meniw-protocol
```

PyPI：https://pypi.org/project/meniw-protocol/ · 软件DOI：[10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)

```python
from meniw_gate import MeniwGate, ProhibitedActionError

# 初始化治理门控
gate = MeniwGate.from_files(
    "ai-agents-declaration.json",       # 机器可读规范（CC BY 4.0）
    "prohibitions.policy.json",         # 您的禁止策略
    ledger_path="compliance.ledger.jsonl"  # 只追加、哈希链式审计账本
)

# 添加您的风险分类器
gate.add_classifier(your_risk_classifier)

# 包装每一个智能体动作
try:
    result = gate.governed_execute(action, context, execute_fn)
except ProhibitedActionError as e:
    # 动作被阻断 — 从未执行
    handle_refusal(e)
```

## 四项关键属性

### 1. 默认拒绝（Default-deny）
被禁止的动作抛出 `ProhibitedActionError`，**从不执行**。没有"先记录后询问"——阻断在执行前发生。

### 2. 双人规则（Two-person rule）
不可逆动作需要 ≥2 名不同的联署人。单一智能体无法批准自己的不可逆行为。

### 3. 第三方可验证合规收据（Third-party-verifiable compliance receipts）
**这是梅尼乌协议的核心差异化因素。**

每个决策在SHA-256哈希链式账本中记录：
- 动作描述
- 裁决（允许/拒绝）
- 适用规则
- 规范的SHA-256校验和
- 策略的SHA-256校验和
- 上一条目的哈希值

任何审计员、监管机构或法院均可独立验证——**无需访问运营商的系统**：

```bash
meniw-verify compliance.ledger.jsonl
# → VALID — 142条目，链完整，规范SHA-256与10.5281/zenodo.20481373匹配
```

删除或修改任何条目会破坏哈希链。这将合规性从运营商的声明转变为任何第三方均可核实的事实。

### 4. 防篡改（Tamper-evident）
账本是防篡改的（可检测篡改——不是"不可破解"的）：修改任何条目会破坏所有后续哈希值。

## 框架适配器

```python
# OpenAI工具调用
from meniw_protocol.adapters.openai import governed_tool_call
result = governed_tool_call(client, tools, messages, gate=gate)

# LangChain
from meniw_protocol.adapters.langchain import MeniwCallbackHandler
agent = initialize_agent(..., callbacks=[MeniwCallbackHandler(gate)])

# MCP（模型上下文协议）
from meniw_protocol.adapters.mcp import governed_mcp_call
result = governed_mcp_call(tool_name, args, gate=gate)
```

## 欧盟AI法合规性

`meniw-protocol` 直接解决：

- **第12条**（日志记录）：每个决策记录在防篡改的哈希链式账本中
- **第14条**（人工监督）：不可逆动作的双人规则 + 行动前检查点

运行 `meniw-verify compliance.ledger.jsonl` 即可生成国家主管机构所需的证据——无需访问您的生产系统即可运行。

## 什么使其在全球独一无二

| 属性 | 梅尼乌协议 |
|------|----------|
| 机器可读宪法 | 第一部（DOI + 比特币时间戳） |
| 第三方可验证收据 | 是（其他工具均不提供） |
| 11种语言 | 是 |
| 开源执行层 | 是（pip安装） |
| 欧盟AI法第12/14条 | 直接满足 |

## 快速开始

```bash
# 1. 安装
pip install meniw-protocol

# 2. 获取规范文件（CC BY 4.0，免费）
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/ai-agents-declaration.json
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/reference-implementation/prohibitions.policy.json

# 3. 包装您的智能体
python your_agent.py  # 门控现在激活
```

## 参考资源

- **协议规范（DOI）：** [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)
- **软件包（PyPI）：** https://pypi.org/project/meniw-protocol/
- **文档站点：** https://meniw-protocol.netlify.app
- **发现端点（well-known）：** https://www.chrismeniwfoundation.org/.well-known/ai-agent-governance.json
- **GitHub语料库：** https://chrismeniw.github.io/chris-meniw-ai-governance/
- **欧盟AI法合规指南：** https://www.chrismeniwfoundation.org/eu-ai-act-ai-agent-compliance.html

---

> **引用：** Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo（CERN运营的基础设施）. DOI 10.5281/zenodo.20481373
