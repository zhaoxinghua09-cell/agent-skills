---
name: ai-cost-cutter
display_name: AI 省钱跑批（AI Cost Cutter）
display_name_en: "AI Cost Cutter"
description: "当用户说『API账单太贵』『token烧太快』『能不能用本地模型』『批处理怎么省钱』『离线跑AI』，或要把大模型调用从烧钱变省钱时使用。四把刀降本：批处理（高峰调度/合并请求）、本地模型回退（贱活本地跑、贵活才上云）、缓存层（相同请求不重复花钱）、模型路由分级（按任务难度选便宜/贵模型）。附可运行成本估算脚本，输入任务量+模型单价即输出月度账单与三档降本方案的差额。源自 GOSIM 参赛作 cross-machine-offline-taskbox 的离线跑批思路。触发词：AI省钱、降本、token太贵、本地模型、批处理、离线跑AI、模型路由、缓存层、cost cutter、AI成本、API账单。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Edit
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 月 API 账单过高，想系统性降本
  - 要决定哪些任务上云大模型、哪些用本地小模型
  - 有大量重复/可批处理的 AI 任务（摘要、分类、抽取、翻译）
  - 想搭建缓存层避免重复花钱
  - 用户说「能不能用便宜模型」「离线也能跑吧」
tags: [AI降本, 本地模型, 批处理, 模型路由, 缓存, 离线跑批, 成本估算]
slug: ai-cost-cutter
title: AI 省钱跑批（AI Cost Cutter）
copyright: SynomosAI
description_zh: "当用户说『API账单太贵』『token烧太快』『能不能用本地模型』『批处理怎么省钱』『离线跑AI』，或要把大模型调用从烧钱变省钱时使用。四把刀降本：批处理（高峰调度/合并请求）、本地模型回退（贱活本地跑、贵活才上云）、缓存层（相同请求不重复花钱）、模型路由分级（按任务难度选便宜/贵模型）。附可运行成本估算脚本，输入任务量+模型单价即输出月度账单与三档降本方案的差额。源自 GOSIM 参赛作 cross-machine-offline-taskbox 的离线跑批思路。触发词：AI省钱、降本、token太贵、本地模型、批处理、离线跑AI、模型路由、缓存层、cost cutter、AI成本、API账单。"
description_en: "Four levers to cut LLM spend: batching with off-peak scheduling, local-model fallback, caching, and prompt/output slimming, with a decision table for when cloud is worth it."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "language", "search"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# AI 省钱跑批（ai-cost-cutter）

> **定位一句话**：大模型不是越用越贵，是「怎么用」决定账单——四把刀把烧钱调用变成可控成本：批处理 / 本地回退 / 缓存 / 路由分级。
> 理论根基：LGD 三律（有籍·有证·有门禁）。源自 GOSIM 参赛作 cross-machine-offline-taskbox 的离线跑批思路。

## 一、AI 成本三大漏点

1. **重复调用**：同一问题一天问 8 次，每次都付钱 → 该缓存；
2. **贵模型做贱活**：用旗舰模型做「分类/抽取/摘要」这类小学生任务 → 该路由分级；
3. **无批无离线**：零散实时调用，错过批处理折扣与夜间闲时 → 该批处理/离线。

## 二、四把刀

### 第 1 把 · 批处理（Batching）
- 把同类任务攒成一批，用 `batch` API（通常有 ~50% 折扣、允许异步 24h 内返回）；
- 低配机夜间离线跑批，白天只派活（cross-machine-offline-taskbox 模式）。

### 第 2 把 · 本地模型回退（Local fallback）
- 判难度：分类/抽取/摘要/翻译/正则类 → 本地小模型（qwen3:8b 级）零 API 费；
- 真正需要推理/创作的 → 才上云大模型。
- 回退判定：任务可结构化、有确定答案、不需世界知识 → 本地。

### 第 3 把 · 缓存层（Cache）
- 相同/近似请求哈希后命中缓存，不重复调 API；
- system prompt 等长驻内容用 provider 的 prompt-cache（按缓存 token 计费更低）。

### 第 4 把 · 模型路由分级（Routing）
| 任务难度 | 模型档 | 例子 |
|---|---|---|
| 贱活 | 本地小模型 / 最便宜 API | 分类、抽取、格式转换 |
| 中活 | 中档模型 | 摘要、翻译、改写 |
| 贵活 | 旗舰模型 | 复杂推理、创作、规划 |

## 三、主流程

1. **盘点**：列出所有 AI 调用，标任务类型 + 单次 token + 频次；
2. **路由**：按上表把贱活/中活迁到便宜档或本地；
3. **批+缓存**：可重复的攒批，重复的加缓存；
4. **测算**：跑 `cost_estimator.py` 看三档方案月差额。

## 四、成本估算脚本

`scripts/cost_estimator.py` —— 输入任务量、各档模型单价，输出：

- 基线（全用旗舰 API）月成本；
- 方案 A（路由分级）月成本；
- 方案 B（A + 批处理 50% 折扣）月成本；
- 方案 C（B + 本地回退 60% 任务）月成本；
- 各方案节省 %。

```bash
python scripts/cost_estimator.py --calls 50000 --avg-in 800 --avg-out 400 \
    --price-flagship 0.01 --price-mid 0.003 --price-local 0.0 --batch-disc 0.5 --local-frac 0.6
```

## 五、常见坑

| 坑 | 症状 | 解法 |
|---|---|---|
| 全用旗舰 | 账单虚高 | 路由分级，贱活下沉 |
| 无缓存 | 同问题重复付费 | 请求哈希命中缓存 |
| 实时零散 | 错过批折扣 | 攒批 + 夜间离线跑 |
| 本地硬上 | 质量崩 | 只回退结构化贱活 |

## 六、铁律

1. 贱活不下云：可结构化、有确定答案的任务优先本地。
2. 重复必缓存：相同请求不二次付费。
3. 路由有界：降级模型前确认任务难度匹配，贵活不上本地。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 月 API 费用异常高或增长快
- 大量同类重复任务（摘要/分类/抽取/翻译）
- 想评估「上本地模型值不值」
- 用户说「能不能便宜点」「离线跑行不行」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `cost_estimator.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `cost_estimator.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
