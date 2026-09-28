---
name: tool-call-guard
display_name: 工具调用安全闸门（Tool Call Guard）
display_name_en: "Tool Call Guard"
description: "当用户说『agent乱调工具』『误删了文件』『不该发邮件却发了』『怎么给AI的工具加权限边界』，或在给 agent 接工具（文件/网络/数据库/消息/支付）想防危险动作时使用。把每次 tool call 当『需授权操作』：按 读/写/删/外发/支付 分级，危险动作先拦截+提示确认，低风险放行。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：工具调用安全、agent权限、tool call guard、危险动作拦截、误删、误发、AI工具边界、function安全。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch
category: AI安全
platforms: [windows, macos, linux]
read_when:
  - agent 拥有文件/网络/数据库/消息/支付等带副作用的工具
  - 出现过或担心 agent 误删、误发、越权操作
  - 要给不同工具设不同的审批门槛（读免审、写需确认、删/支付拦截）
  - 用户问「怎么给 AI 的工具加护栏」
tags: [工具调用安全, tool call guard, agent权限, 危险动作拦截, 最小权限, AI安全, 门禁]
slug: tool-call-guard
title: 工具调用安全闸门（Tool Call Guard）
copyright: SynomosAI
description_zh: "当用户说『agent乱调工具』『误删了文件』『不该发邮件却发了』『怎么给AI的工具加权限边界』，或在给 agent 接工具（文件/网络/数据库/消息/支付）想防危险动作时使用。把每次 tool call 当『需授权操作』：按 读/写/删/外发/支付 分级，危险动作先拦截+提示确认，低风险放行。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：工具调用安全、agent权限、tool call guard、危险动作拦截、误删、误发、AI工具边界、function安全。"
description_en: "Treat every tool call as an authorization-required operation: permission boundaries and dangerous-action interception for file, network, database, messaging and payment tools."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics", "search"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 工具调用安全闸门（tool-call-guard）

> **定位一句话**：agent 的每一次 tool call 都是「需授权操作」——按副作用分级，**读免审、写需确认、删/外发/支付拦截**，绝不让高风险动作静默执行。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `prompt-injection-shield`、`agent-redteam-kit` 同族。

## 一、为什么 agent 会「乱来」

- **静默删除**：一句话就 `rm -rf` 了不该删的目录；
- **误外发**：替你把草稿邮件、内部消息发出去了；
- **越权支付**：调用了下单/转账类工具；
- **无分级**：所有工具一把梭，读和删同权。

本技能管「agent 发起工具调用 → 真正执行」之间的那道闸。

## 二、风险五级（按副作用）

| 级别 | 动作 | 默认策略 |
|---|---|---|
| L0 只读 | 读文件/查库/搜索 | 放行 |
| L1 网络读 | 外部 GET | 放行（记日志） |
| L2 写入 | 写文件/插入库 | 需确认 |
| L3 外发 | 发邮件/发消息/发帖 | 拦截+确认 |
| L4 不可逆 | 删除/覆盖/支付/转账 | 拦截+双人/人工 |

`scripts/tool_guard.py` 读工具调用描述（名称+参数），给出级别 + 放行/拦截决策 + 理由。

## 三、主流程（三步）

### 第 1 步 · 列工具清单（有籍）
把 agent 能用的工具登记在一份清单，每个标 `risk_level` 与 `needs_confirm`。

### 第 2 步 · 调用前拦截（有门禁）
- L0/L1 直接放行；
- L2 先提示「将写入 X，确认？」再执行；
- L3/L4 默认拦截，返回「需人工确认」，绝不静默外发或删除。

### 第 3 步 · 留痕（有证）
每次调用写一条审计：`时间·工具·参数·决策·操作者`，事后可追。

## 四、铁律

1. 最小权限：agent 只给完成任务必需的工具，不给超集。
2. 不可逆必拦：删/覆盖/支付/转账必须经人工，不允许自动。
3. 外发需确认：任何对外发送默认拦截，确认才发。
4. 全留痕：每次 tool call 写审计，可追责。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- agent 拥有文件/网络/数据库/消息/支付类工具
- 出现过或担心误删、误发、越权
- 想给不同工具设不同审批门槛
- 问「怎么给 AI 工具加护栏」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `tool_guard.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `tool_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
