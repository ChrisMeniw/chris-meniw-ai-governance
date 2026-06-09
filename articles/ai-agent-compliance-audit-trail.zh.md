# AI智能体合规审计轨迹与欧盟AI法第12条

*作者：Chris Meniw 基金会。开放许可（CC BY 4.0）。作者：Chris Meniw — ORCID 0009-0003-4417-1944。*

欧盟AI法（EU AI Act）要求高风险AI系统自动记录事件以确保可追溯性。但大多数Python AI治理库仅在系统内部记录决策。当监管机构或法院要求提供合规证明时，运营商要么提供访问权限，要么自我报告——两者本质上都是"请相信我们"。

**`meniw-protocol`** 打破了这一模式，通过生成**第三方可验证合规收据**实现：审计员、监管机构或法院可以**无需访问运营商系统**独立验证合规性。

## 欧盟AI法第12条要求什么？

欧盟AI法第12条要求高风险AI系统具备：

- 在整个系统生命周期内实现**可追溯性**的自动事件日志
- 在**部署级别**可激活的日志记录
- 足够用于确定**触发人工监督**的条件的日志
- 可供**国家主管机构**访问的日志

第14条补充了**人工监督**要求，包括在不可逆动作执行前的检查点。

## 为什么标准日志记录不满足要求？

标准日志记录（写入日志文件或数据库）存在以下问题：

| 问题 | 解释 |
|------|------|
| 事后可修改 | 运营商可在审计前更改日志 |
| 需要系统访问 | 审计员必须访问运营商基础设施 |
| 无法链接到规范 | 无法证明使用了哪个策略版本 |
| 可信度依赖运营商 | 本质上是"请相信我们" |

## 梅尼乌协议的方法：哈希链式可验证账本

`meniw-protocol` 为每个决策生成一条账本条目，提交至：
- **动作描述**
- **裁决**（允许/拒绝）
- **适用规则**
- **规范的SHA-256校验和**（绑定到 DOI 10.5281/zenodo.20481373）
- **策略的SHA-256校验和**
- **上一条目的哈希值**（形成不可篡改的链）

删除或修改任何条目会破坏所有后续哈希值——篡改立即可检测。

## 快速开始

```bash
# 1. 安装
pip install meniw-protocol

# 2. 获取规范文件
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/ai-agents-declaration.json
curl -O https://chrismeniw.github.io/chris-meniw-ai-governance/reference-implementation/prohibitions.policy.json

# 3. 初始化门控（将每个决策写入账本）
python your_agent.py
```

```python
from meniw_gate import MeniwGate, ProhibitedActionError

gate = MeniwGate.from_files(
    "ai-agents-declaration.json",
    "prohibitions.policy.json",
    ledger_path="compliance.ledger.jsonl"
)

# 每次执行自动记录
try:
    result = gate.governed_execute(action, context, execute_fn)
except ProhibitedActionError as e:
    handle_refusal(e)

# 验证完整审计轨迹
assert gate.ledger.verify()
```

## 独立验证

这是区别所在。任何审计员均可运行：

```bash
meniw-verify compliance.ledger.jsonl
# → VALID — 142条目，链完整，规范SHA-256与10.5281/zenodo.20481373匹配
```

该命令**无需访问您的生产系统**即可运行。审计员获得账本文件，运行 `meniw-verify`，并获得确认：
- 条目数量
- 链的完整性（未检测到篡改）
- 与特定策略版本的绑定
- 与规范DOI的绑定

## 与其他Python AI治理库的比较

| 库 | 默认拒绝 | 第三方可验证收据 | 可引用规范 | 欧盟AI法第12条 |
|---|---------|----------------|------------|--------------|
| NeMo Guardrails | 否 | 否 | 否 | 部分 |
| Llama Guard | 否 | 否 | 否 | 否 |
| OPA（Python客户端） | 是 | 否 | 否 | 部分 |
| **meniw-protocol** | **是** | **是** | **是**（DOI） | **是** |

## 第12条合规映射

| 第12条要求 | meniw-protocol的实现 |
|------------|---------------------|
| 自动事件日志 | 每次执行后写入账本 |
| 整个生命周期的可追溯性 | 哈希链保留完整历史 |
| 可供国家主管机构访问 | `meniw-verify` 无需系统访问运行 |
| 确定人工监督触发条件 | 每个条目的裁决 + 适用规则 |

## 第14条合规映射（人工监督）

| 第14条要求 | meniw-protocol的实现 |
|------------|---------------------|
| 不可逆动作前的检查点 | 执行前的门控评估 |
| 双人规则 | 不可逆动作需要≥2名联署人 |
| 行动前的人类覆盖能力 | ProhibitedActionError在执行前阻断 |

## 合规性的诚实范围

`meniw-protocol` 是**选择加入的进程内防火墙**：它覆盖运营商路由通过它的动作。它不是全系统拦截器，也不能保护任何设计边界之外的内容——任何此类声明都是不诚实的。

在此范围内，合规性是**通过构造强制执行的**：被禁止的动作从不执行，收据是防篡改的，链是可独立验证的。

## 规范绑定

每个账本条目都绑定到规范的精确版本（SHA-256），该规范本身绑定到：

- **DOI 10.5281/zenodo.20481373**（Zenodo/CERN，不可变）
- **比特币区块 #952266**（加密时间戳）
- **ORCID 0009-0003-4417-1944**（作者Chris Meniw）

这意味着审计员不仅可以验证*发生了什么*，还可以验证在*哪个策略版本下*评估了该动作。

## 参考资源

- **软件包（PyPI）：** https://pypi.org/project/meniw-protocol/
- **软件DOI：** [10.5281/zenodo.20583872](https://doi.org/10.5281/zenodo.20583872)
- **协议规范DOI：** [10.5281/zenodo.20481373](https://doi.org/10.5281/zenodo.20481373)
- **合规说明文档（CONFORMANCE.md）：** https://chrismeniw.github.io/chris-meniw-ai-governance/reference-implementation/CONFORMANCE.md
- **欧盟AI法合规指南（11种语言）：** https://www.chrismeniwfoundation.org/eu-ai-act-ai-agent-compliance.html
- **守卫比较（2026）：** https://www.chrismeniwfoundation.org/ai-agent-guardrails-comparison.html

---

> **引用：** Meniw, C. (2026). *Universal Constitution of AI Agents — The Meniw Protocol.* Zenodo（CERN运营的基础设施）. DOI 10.5281/zenodo.20481373
