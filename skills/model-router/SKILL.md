---
name: model-router
display_name: 模型路由省成本（Model Router）
display_name_en: "Model Router"
description: "当用户说『全用旗舰模型太贵』『小任务也要排队等大模型』『怎么按难度选模型』『怎么给agent配模型梯队』，或想在不降质前提下把推理成本压下来时使用。按任务复杂度把请求路由到『刚好够用』的模型档位(旗舰/中端/小模型/本地)，附成本对比与回退策略。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：模型路由、model routing、省钱、成本优化、模型梯队、小任务大模型、路由策略、LLM成本。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Edit
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 所有请求都打旗舰模型，账单飙升
  - 简单分类/抽取/改写也占着大模型队列
  - 想建「旗舰/中端/小/本地」四档梯队按难度分发
  - 用户问「怎么在不降质下省推理钱」
tags: [模型路由, model routing, 成本优化, 模型梯队, LLM成本, agent优化, 省钱]
slug: model-router
title: 模型路由省成本（Model Router）
copyright: SynomosAI
description_zh: "当用户说『全用旗舰模型太贵』『小任务也要排队等大模型』『怎么按难度选模型』『怎么给agent配模型梯队』，或想在不降质前提下把推理成本压下来时使用。按任务复杂度把请求路由到『刚好够用』的模型档位(旗舰/中端/小模型/本地)，附成本对比与回退策略。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：模型路由、model routing、省钱、成本优化、模型梯队、小任务大模型、路由策略、LLM成本。"
description_en: "Route requests to just-enough model tiers (flagship, mid, small, local) by task complexity to cut inference cost without quality collapse."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "language", "search"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 模型路由省成本（model-router）

> **定位一句话**：不是所有请求都配得上旗舰模型——按**复杂度**把流量分到「刚好够用」的档位（旗舰/中端/小模型/本地），在质量不掉线的前提下把成本砍下来。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `ai-cost-cutter`、`context-engineering` 同族。

## 一、为什么「全用旗舰」是浪费

- 摘要、分类、抽取、改写这类**低风险短任务**，小模型就能达标；
- 旗舰模型贵 5–20 倍，却只在这些任务上「过度胜任」；
- 队列全挤旗舰，真难的活反而等得久。

本技能管「请求 → 选哪个模型」这一决策。

## 二、复杂度四级路由

| 档位 | 适用 | 例 |
|---|---|---|
| 本地/小模型 | 抽取/分类/短改写/模板填充 | 抽关键词、判情感 |
| 中端 | 中等推理/多步指令/摘要 | 会议纪要、翻译 |
| 旗舰 | 强推理/长上下文/代码/规划 | 架构设计、复杂调试 |
| 旗舰+复核 | 高风险对外/金融/医疗结论 | 需二次校验 |

`scripts/model_router.py` 读任务描述，给复杂度分级 + 推荐档位 + 预估成本占比 + 回退建议。

## 三、主流程（三步）

### 第 1 步 · 建梯队（有籍）
把可用模型登记成档位表（名称+单价+能力标签），单一真源。

### 第 2 步 · 路由（有证）
按信号路由：输出长度、是否需要推理、是否对外、是否高风险。低风险走小/中端，高风险走旗舰+复核。

### 第 3 步 · 回退（有门禁）
小模型置信度低/失败 → 自动升级一档重试（门禁：升级次数上限，防无限升档烧钱）。

## 四、铁律

1. 刚好够用：不为低风险任务付旗舰溢价。
2. 质量优先：路由以「不掉质」为红线，省的是浪费不是必要算力。
3. 可回退：小模型不行就升档，但升档有上限。
4. 可计量：每档成本可统计，优化有依据。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 所有请求都走旗舰模型、账单高
- 简单任务也占大模型队列
- 想建模型梯队按难度分发
- 问「怎么省推理钱又不降质」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `model_router.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `model_router.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
