---
name: ai-policy-radar
display_name: AI法规动态雷达（Policy Radar）
display_name_en: "AI Policy Radar"
description: "当用户说『最近AI出了什么新规』『EU AI Act/脆监会/NMPA有没有新动作』『法规更新我得跟上』『帮我盯AI政策』，或要持续跟踪 AI 监管动态（EU AI Act / 中国 NMPA / 美国 FDA / GDPR 等）时使用。扫描法规库/更新日志，按主题（风险分级/透明度/数据/准入）归类变动并留痕（有证），输出「本月新增了什么、对你有何影响」。可运行脚本（policy_radar 扫描器）。理论根基：LGD 三律之有证（法规变动留痕可溯）。与 eu-ai-act-companion 互补（它管单法导航，本技能管跨法动态监测）。触发词：AI法规、政策雷达、监管动态、EU AI Act更新、合规追踪、policy radar、法规监测。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要持续跟踪 AI 监管新规
  - 不确定 EU AI Act / NMPA / FDA 近期有无变动
  - 做合规月报/动态监测
  - 收到「盯一下政策」类指令
tags: [AI法规, policy radar, 监管动态, 合规追踪, 有证]
slug: ai-policy-radar
title: AI法规动态雷达（Policy Radar）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# AI法规动态雷达（ai-policy-radar）

> **定位一句话**：AI 监管每月都在变——本技能把跨法域（EU/US/CN）新规按主题归类、留痕，告诉你「这个月新增了什么、影响你哪块」。
> 理论根基：LGD 三律之有证（法规变动留痕可溯）。与 `eu-ai-act-companion` 互补。

## 一、为什么要盯动态

1. **期限踩雷**：EU AI Act 各条款有生效节点，错过即违规；
2. **跨法冲突**：同业务在 EU/CN/US 要求不同；
3. **被动整改**：等被罚才知道新规。

## 二、监测四类主题

| 主题 | 覆盖 |
|---|---|
| 风险分级 | high-risk 定义变动 |
| 透明度 | 披露/标识义务 |
| 数据 | 训练数据/隐私 |
| 准入 | 上市/备案/登记 |

## 三、主流程（三步）

### 第 1 步 · 扫描（有证）
`policy_radar.py` 扫法规库/更新日志，抽取含监管关键词的条目并打主题标签。

### 第 2 步 · 归类留痕
按四类主题汇总，记录来源与日期（有证）。

### 第 3 步 · 影响研判
对每条标注「影响你的哪块业务」。

## 四、铁律

1. 留痕可溯：每条法规变动带来源+日期。
2. 跨法并看：EU/US/CN 同主题并行列。
3. 月更：定期跑，不攒到被罚才看。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要持续跟踪 AI 新规
- 做合规月报
- 担心错过 EU AI Act 生效节点

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `policy_radar.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `policy_radar.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
