---
name: bias-auditor
display_name: 偏见审计（Bias Auditor）
display_name_en: "Bias Auditor"
description: "当用户说『AI回答有偏见』『输出性别/地域/年龄刻板印象』『怎么检测模型偏见』『内容要过公平审查』，或在发布面向人群的内容(招聘/推荐/客服/评测)前想做公平性自检时使用。把模型输出当『带视角的生产物』：扫人口群体词·刻板表述·单边归因，标出潜在偏见并给去偏改写建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：偏见检测、bias audit、公平性、刻板印象、AI歧视、内容审查、公平自检、stereotype。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 模型输出疑似带性别/地域/年龄/职业刻板印象
  - 招聘/推荐/评测类内容要过公平审查
  - 用户问「怎么检测 AI 偏见」
  - 对外发布前想做公平性自检
tags: [偏见审计, bias audit, 公平性, 刻板印象, 去偏, 内容审查, AI伦理, 可靠性]
slug: bias-auditor
title: 偏见审计（Bias Auditor）
copyright: SynomosAI
description_zh: "当用户说『AI回答有偏见』『输出性别/地域/年龄刻板印象』『怎么检测模型偏见』『内容要过公平审查』，或在发布面向人群的内容(招聘/推荐/客服/评测)前想做公平性自检时使用。把模型输出当『带视角的生产物』：扫人口群体词·刻板表述·单边归因，标出潜在偏见并给去偏改写建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：偏见检测、bias audit、公平性、刻板印象、AI歧视、内容审查、公平自检、stereotype。"
description_en: "Audit model outputs for bias before publishing people-facing content (hiring, recommendations, support): demographic terms, stereotypes and unfairness scans with fix suggestions."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 偏见审计（bias-auditor）

> **定位一句话**：模型输出是「带视角的生产物」——扫**人口群体词·刻板表述·单边归因**，标出潜在偏见并给去偏改写建议，发布前先过公平这一关。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `fact-check-guard`、`skill-quality-gate` 同族。

## 一、为什么偏见会「混进」输出

- **群体词泛化**：「女的都不适合…」「某地人就是…」以偏概全；
- **刻板归因**：把能力/性格绑到性别/年龄/地域；
- **单边视角**：只呈现一种立场，忽略其他群体；
- **默认主语**：用例默认某一群体，隐含排斥。

本技能管「生成内容 → 公平自检」这一步。

## 二、三类偏见信号

| 类型 | 信号 | 处置 |
|---|---|---|
| 群体泛化 | 「某群体都…」 | 标偏见 + 改为个体表述 |
| 刻板归因 | 能力绑性别/年龄/地域 | 标偏见 + 去绑 |
| 单边视角 | 只一种立场 | 提示补充其他视角 |

`scripts/bias_audit.py` 读文本，给出命中信号 + 位置 + 去偏建议。

## 三、主流程（三步）

### 第 1 步 · 扫信号（有籍）
对输出跑群体词 + 刻板表述词库，逐句标信号，定位可查。

### 第 2 步 · 判严重（有证）
区分「客观陈述群体差异」与「以偏概全」——前者保留，后者标偏见。

### 第 3 步 · 改写建议（有门禁）
给具体去偏改写（改个体表述、补视角），不改原意只去偏。通过才对外。

## 四、铁律

1. 不泛化群体：避免「某群体都…」式全称判断。
2. 不绑刻板：能力/性格不绑性别/年龄/地域。
3. 给多视角：面向人群的内容呈现主要立场外，提示其他视角。
4. 留痕：偏见命中与改写可追，便于复核。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 模型输出疑似带群体刻板印象
- 招聘/推荐/评测内容要过公平审查
- 问「怎么检测 AI 偏见」
- 发布前想做公平性自检

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `bias_audit.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `bias_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
