---
name: api-resilience
display_name: API 韧性（API Resilience）
display_name_en: "API Resilience"
description: "当用户说『调外部API老超时』『被限流了』『接口抖一动就挂』『怎么给agent加重试退避』，或 agent 依赖的第三方服务(模型/搜索/数据库)不稳定、需要限流/退避/熔断/降级时使用。把外部调用当『会失败的对象』：指数退避+抖动重试、限流计数、熔断降级，失败可恢复不雪崩。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：API重试、限流、退避、熔断、降级、接口抖动、resilience、超时、调用不稳定。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, WebSearch
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - agent 依赖的模型/搜索/数据库接口偶发超时或 429
  - 一次失败就让整条链路崩
  - 想加指数退避/抖动/熔断/降级
  - 用户问「怎么让外部调用更稳」
tags: [API韧性, 重试退避, 限流, 熔断, 降级, resilience, 可靠性, 故障恢复, agent优化]
slug: api-resilience
title: API 韧性（API Resilience）
copyright: SynomosAI
description_zh: "当用户说『调外部API老超时』『被限流了』『接口抖一动就挂』『怎么给agent加重试退避』，或 agent 依赖的第三方服务(模型/搜索/数据库)不稳定、需要限流/退避/熔断/降级时使用。把外部调用当『会失败的对象』：指数退避+抖动重试、限流计数、熔断降级，失败可恢复不雪崩。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：API重试、限流、退避、熔断、降级、接口抖动、resilience、超时、调用不稳定。"
description_en: "Treat external API calls as failure-prone: retry with backoff, rate limiting, circuit breaking and graceful degradation patterns for agents relying on third-party services."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics", "search"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# API 韧性（api-resilience）

> **定位一句话**：外部 API 是「会失败的对象」——用**指数退避+抖动重试 · 限流计数 · 熔断降级**，让一次抖动可恢复、不雪崩。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `agent-loop-guard`、`skill-quality-gate` 同族。

## 一、为什么外部调用会「拖垮全场」

- **硬失败**：一次 500/超时没兜住，整条 agent 链路崩；
- **限流雪崩**：429 后立刻重试，反而把对方打挂、自己也卡死；
- **无熔断**：依赖服务挂了还猛冲，耗尽资源；
- **无降级**：主路没了，没有备用路，直接报错。

本技能管「agent → 外部服务」这条最脆的链路。

## 二、四道韧性

| 机制 | 作用 | 默认 |
|---|---|---|
| 指数退避+抖动 | 失败重试，间隔翻倍+随机 | 最多 5 次 |
| 限流计数 | 单位时间请求数封顶 | 令牌桶 |
| 熔断 | 连续失败超阈 → 暂停一阵 | 半开探测恢复 |
| 降级 | 主路失败 → 走备用/缓存 | 返回兜底 |

`scripts/resilience_demo.py` 演示带退避+熔断的调用包装（含模拟失败/恢复）。

## 三、主流程（三步）

### 第 1 步 · 包调用（有籍）
所有外部调用走统一包装，计次/计时有单一入口。

### 第 2 步 · 重试+退避（有证）
失败按指数退避+抖动重试（上限 N）；429 等可重试码才重试。

### 第 3 步 · 熔断+降级（有门禁）
连续失败超阈 → 熔断，暂停后半开探测；主路不通 → 走降级兜底，不裸崩。

## 四、铁律

1. 失败要重试：外部调用默认带退避重试，不一次就挂。
2. 退避要抖：间隔指数增长+随机抖动，避免重试风暴。
3. 失控要断：连续失败超阈必熔断，保护双方。
4. 主路要备：关键调用有降级兜底，不裸报错。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- agent 依赖的接口偶发超时/429
- 一次失败就整条崩
- 想加退避/限流/熔断/降级
- 问「怎么让外部调用更稳」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `resilience_demo.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `resilience_demo.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
