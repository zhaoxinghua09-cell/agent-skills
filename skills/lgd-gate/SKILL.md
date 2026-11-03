---
name: lgd-gate
description: lgd-gate — LGD 门禁中枢（meta 薄分发器）。把 GovernanceOS 的 GATE 阶段 8 个门禁节点聚合成一个可检索、可一键探测的入口：质量门/发布门/准入门/评审门/放行门/技能发布门/人工监督门/门禁策略生成。只按 slug 路由到独立子技能，不搬运、不重实现任何子技能代码。 适用场景：当需要AI 智能体门禁/发布拦截/质量闸门能力时使用本技能；触发词：lgd-gate、门禁、质量门、发布门、准入。
slug: lgd-gate
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-skills-index/
display_name: LGD 门禁中枢
display_name_en: LGD Gate Hub
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本按 CC BY 4.0 授权（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
copyright: XLGD · SynomosAI
description_zh: "lgd-gate — LGD 门禁中枢（meta 薄分发器），把 GATE 阶段 8 个门禁节点聚合成可检索可探测入口。"
description_en: "LGD Gate Hub — a thin meta-dispatcher that aggregates the 8 GATE-phase governance nodes into one discoverable, self-verifying entry point."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "meta 薄分发器默认 medium：仅按 slug 路由并只读探测（--help），不代执行子技能、不对外写；若需经本技能触发实际门禁拦截/发布，须由被路由的子技能各自走其 own 风险评审。"
tags: [lgd-gate, AI 治理, 门禁, 质量门, 发布门]
ai_protocol: true

lineage: ["LGD-有籍", "LGD-有门禁", "GovernanceOS-GATE"]
---

# LGD 门禁中枢（lgd-gate）

> **薄分发器（thin dispatcher）**：本技能不搬运、不重实现任何门禁代码。它只是 GovernanceOS
> `SPEC → PLAN → GATE → AUDIT → EVO` 生命周期里 **GATE 阶段**的聚合入口——把 8 个独立发布的
> 门禁子技能按 slug 列出、一键探测可用性、给出调用说明。所有真实拦截由被路由的子技能完成。

## When to Use

- 你要给一个 AI 智能体/技能/发布流程**加门禁**，但不知道该用哪个门。
- 你需要**一键看清**当前 GATE 阶段有哪些门、哪些真的装上了、哪些只在生态/备份层。
- 你要在发布前跑**质量门 / 发布门 / 准入门**，但想先从一个入口总览。
- 触发词：`lgd-gate`、`门禁`、`质量门`、`发布门`、`准入`、`拦截发布`。

## 核心能力（GATE 阶段 8 节点）

| # | slug | 用途 | 预期产出 |
|---|------|------|----------|
| 1 | `skill-quality-gate` | 技能入库前质量门：结构/文档/安全/生态兼容五维评分，未过拦截 | 质量门判定 + 阻断项 |
| 2 | `publish-quality-gate` | 对外发布前发布门：四层扫描（密钥/注入/合规/完整性），阻断放行 | 发布门判定；任一阻断项则拦 |
| 3 | `skill-admission-gate` | 新技能申请入库的准入门：admit / conditional / reject | 准入判定 + 理由 |
| 4 | `publish-review-gate` | 发布前人工 + 自动评审门：checklist 覆盖 | 评审判定 + checklist 覆盖 |
| 5 | `release-gate-check` | 发布时 release 前置校验：发布就绪清单 pass/fail | 就绪清单 pass/fail |
| 6 | `skill-release-gate` | 技能包发布时的发布门：阻断放行 | 发布门判定；阻断项则拦 |
| 7 | `human-oversight-gate` | 高风险动作人工监督门：approver 决策记录 | 监督决策记录 + approver |
| 8 | `gate-policy-generator` | 为新风险类生成门禁策略文档 | 生成的门禁策略文档 |

## 真实可用性（诚实分级）

`lgd-gate --verify` 会**实探**每个节点的活动工作集目录与可执行脚本，给出三种状态：

- **LIVE**：活动工作集内有目录且有可运行脚本（`--help` 退出码 0）→ 真能拦。
- **ECOSYSTEM**：在 GovernanceOS 路由里声明、但当前活动工作集无目录（仅生态/备份层）→ 需
  `openclaw plugins install clawhub:<slug>` 或引用生态层后才可用。
- **ERROR**：目录在但脚本执行异常 → 需修复。

> 诚实声明：截至本技能发布快照，GATE 阶段 8 节点中**部分**在活动工作集（如 `skill-quality-gate`、
> `publish-quality-gate`、`skill-admission-gate`、`gate-policy-generator`），其余声明于路由/生态层。
> `--verify` 输出以**当前机器实际探测**为准，不以文档宣称。

## 用法

```bash
# 列出 GATE 阶段全部 8 个门禁节点
python lgd_gate.py --list

# 实探每个节点的真实可用性（活动工作集探测，不谎报）
python lgd_gate.py --verify --json-out evidence.json

# 查看某个门禁的调用说明
python lgd_gate.py --route publish-quality-gate
```

## 设计纪律（为什么是薄分发器）

- **零臃肿**：新增/下线一个门禁 = 改本技能 `NODES` 表里一行，不复制任何代码。
- **可插拔**：每个节点是独立 slug，各自版本独立、各自发布；本技能只引用。
- **诚实**：探测不到的节点如实标 ECOSYSTEM，绝不伪称"已实跑"或"全绿"。
- **只读**：`--verify` 仅以 `--help` 探针方式读取子技能元信息，不做任何拦截动作、不对外写。

## Known Limits

- 本技能**不替**子技能做拦截；它只路由与探测。真实门禁由 `governance_flow.py` 或各子技能 CLI 执行。
- 跨机/未安装子技能时，`--verify` 会显示 ECOSYSTEM，属预期，非缺陷。

## 参考

- 上游编排器：`governanceos` → `scripts/governance_flow.py`（PHASES["gate"] 为权威节点清单）。
- 三律：`有籍 / 有证 / 有门禁`（registered / evidenced / gated）。
