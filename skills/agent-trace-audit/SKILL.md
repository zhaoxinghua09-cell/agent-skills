---
name: agent-trace-audit
display_name: 智能体行为留痕审计（Trace Audit）
display_name_en: "Agent Trace Audit"
description: "当用户说『AI刚才干了什么我要查』『agent操作有没有越界』『出事了能回溯吗』『给AI行为留个账本』，或要给 agent 的操作做可审计留痕时使用。把 agent 的动作日志（时间戳/执行者/动作/对象/是否过闸）建成可追溯账本，标出未过闸的越界操作（有籍），输出时间线+违规清单。可运行脚本（trace_audit 审计器）。理论根基：LGD 三律之有籍（全程可追溯）。与 agent-redteam-kit/有门禁互补。触发词：行为留痕、trace audit、操作审计、agent回溯、可追溯、行为账本、审计日志。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要回溯 agent 做过哪些操作
  - 担心 agent 有未授权/越界动作
  - 出事后需要追责到具体动作
  - 要建 agent 行为账本
tags: [行为留痕, trace audit, 操作审计, 可追溯, 有籍]
slug: agent-trace-audit
title: 智能体行为留痕审计（Trace Audit）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 智能体行为留痕审计（agent-trace-audit）

> **定位一句话**：agent 出事不可怕，可怕的是查不出它干了什么——本技能把每次动作建成「时间戳·执行者·动作·对象·是否过闸」的账本，越界一目了然。
> 理论根基：LGD 三律之有籍（全程可追溯）。与 `agent-redteam-kit` 互补。

## 一、为什么必须留痕

1. **追责**：出错时定位到具体动作与执行者；
2. **越界发现**：未过闸的写操作浮出来；
3. **合规**：监管要你能证明「做了什么、怎么管的」。

## 二、账本五字段

| 字段 | 含义 |
|---|---|
| ts | 时间戳 |
| actor | 哪个 agent/人 |
| action | 做了什么 |
| target | 作用对象 |
| gate | 是否过门禁（pass/无闸） |

## 三、主流程（三步）

### 第 1 步 · 收集
agent 每动作写一行 JSON 日志（含 gate 标记）。

### 第 2 步 · 建账本（有籍）
`trace_audit.py` 读日志，按时间排序，标出 gate=无闸 的越界项。

### 第 3 步 · 出报告
输出时间线 + 违规清单，供复盘/合规。

## 四、铁律

1. 动作即记：每次动作落日志，不补记。
2. 越界必标：无闸写操作显式标红。
3. 不可改：账本只读归档，不回改历史。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要回溯 agent 操作
- 担心 agent 越界
- 出事后追责/合规

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `trace_audit.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `trace_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
