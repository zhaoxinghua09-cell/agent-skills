---
name: agent-loop-guard
display_name: 失控循环护栏（Agent Loop Guard）
display_name_en: "Agent Loop Guard"
description: "当用户说『agent卡死了』『一直在重复同样动作』『跑飞了烧光token』『怎么给agent设步数上限』，或 agent 出现无限循环/重复调用/原地打转时使用。把 agent 的运行当『受控进程』：监控步数上限·重复动作·状态无进展，触发即熔断并产出诊断。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：agent卡死、无限循环、重复动作、跑飞、步数上限、loop guard、token烧光、失控循环。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - agent 疑似陷入无限循环或重复调用同一工具
  - token/费用异常飙升，怀疑 agent 跑飞
  - 想给 agent 设最大步数 / 无进展熔断
  - 用户抱怨「它一直在绕圈」
tags: [失控循环, loop guard, 步数上限, agent监控, token控制, 熔断, 可靠性, AI工程]
slug: agent-loop-guard
title: 失控循环护栏（Agent Loop Guard）
copyright: SynomosAI
description_zh: "当用户说『agent卡死了』『一直在重复同样动作』『跑飞了烧光token』『怎么给agent设步数上限』，或 agent 出现无限循环/重复调用/原地打转时使用。把 agent 的运行当『受控进程』：监控步数上限·重复动作·状态无进展，触发即熔断并产出诊断。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：agent卡死、无限循环、重复动作、跑飞、步数上限、loop guard、token烧光、失控循环。"
description_en: "Guard against runaway agent loops: step limits, repeated-action detection, budget alerts and controlled-intervention patterns for stuck, looping or burning agents."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 失控循环护栏（agent-loop-guard）

> **定位一句话**：agent 是一次「受控进程」——监控**步数上限 · 重复动作 · 状态无进展**，任一触发就熔断，别让它在原地烧光 token。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `skill-quality-gate`、`context-engineering` 同族。

## 一、为什么 agent 会「跑飞」

- **无限循环**：A 调 B、B 调 A，永不收敛；
- **重复动作**：同一工具同样参数连点 N 次，结果不变；
- **原地打转**：每步都说「再做一次」却无新进展；
- **无上限**：没设 max_steps，理论上能跑到天荒地老。

本技能管「agent 执行中」的实时熔断。

## 二、三路熔断信号

| 信号 | 触发 | 动作 |
|---|---|---|
| 步数超限 | steps > max_steps | 熔断 |
| 重复动作 | 连续 k 次相同 (tool,args) | 熔断 + 提示换策略 |
| 无进展 | 连续 k 步状态相似度 > 阈值 | 熔断 + 诊断 |

`scripts/loop_guard.py` 读动作轨迹（每行 `step tool args`），给循环风险评级 + 熔断建议 + 诊断。

## 三、主流程（三步）

### 第 1 步 · 装探针（有籍）
agent 每步把 `(step, tool, args, state_hash)` 写进轨迹，单一真源可查。

### 第 2 步 · 实时判（有证）
每步后查三路信号；命中即标记，不掩盖。

### 第 3 步 · 熔断（有门禁）
触发熔断 → 停止循环，返回诊断（哪一步开始重复/卡住）+ 建议（换策略/人工介入）。

## 四、铁律

1. 必有上限：每次运行强制 max_steps，无上限不许跑。
2. 重复即疑：连续相同动作大概率是死循环，先熔断。
3. 无进展即停：状态不动就该换路，别硬撑。
4. 留诊断：熔断带轨迹，便于复盘根因。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- agent 卡死 / 重复同样动作
- token 费用异常飙升
- 想给 agent 设步数上限
- 抱怨「它一直在绕圈」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `loop_guard.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `loop_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
