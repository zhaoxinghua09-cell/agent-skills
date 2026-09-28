---
name: fact-check-guard
display_name: 事实核查护栏（Fact Check Guard）
display_name_en: "Fact Check Guard"
description: "当用户说『AI胡说八道』『内容发出去怕有错』『怎么验证模型给的事实』『引用要有出处』，或要把 agent 生成的内容(文章/报告/回复)对外发布、必须可溯源时使用。把每条关键声明当『待证主张』：对照检索来源逐条标注 已支撑/无来源/存疑，无来源的不许当事实对外。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：事实核查、fact check、幻觉检测、引用溯源、内容可证、AI胡说、出处校验、grounding。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 模型生成的内容要对外发布（文章/报告/客服回复）
  - 出现过事实错误、编造引用或数据
  - 要求「每条关键说法都有出处」
  - 用户问「怎么验证 AI 给的是真的」
tags: [事实核查, fact check, 幻觉检测, 引用溯源, 内容可证, grounding, 可靠性, AI安全]
slug: fact-check-guard
title: 事实核查护栏（Fact Check Guard）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 事实核查护栏（fact-check-guard）

> **定位一句话**：模型说的每句「事实」都是**待证主张**——对照检索来源逐条标 已支撑 / 无来源 / 存疑，无来源的不许当事实对外发。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `rag-grounding-guard`、`doc-desens-scanner` 同族。

## 一、为什么幻觉会「过审」

- **编造引用**：论文名、法条、数据看起来真，实则不存在；
- **过时事实**：模型记的是训练截止前的世界；
- **无出处断言**：「研究表明…」却说不出哪项研究；
- **混真带假**：大段正确里夹一句错的，读者难辨。

本技能管「生成内容 → 发布前」的最后一关。

## 二、声明三级标注

| 状态 | 含义 | 处置 |
|---|---|---|
| 已支撑 | 能在来源里找到对应 | 可发布，附出处 |
| 存疑 | 来源弱/部分矛盾 | 标注「待核实」或删除 |
| 无来源 | 检索无支撑 | 禁止当事实，改「据我所知/可能」或删除 |

`scripts/fact_guard.py` 读「声明列表 + 来源文本」，逐条给状态 + 建议。

## 三、主流程（三步）

### 第 1 步 · 抽声明（有籍）
把长文里的关键断言（数字/结论/引用/比较）抽成清单，逐条管理。

### 第 2 步 · 比对来源（有证）
每条声明去来源里查是否有实质支撑；命中记出处，未命中标无来源。

### 第 3 步 · 门禁放行（有门禁）
- 无来源的关键断言一律降级或删除，不许当事实；
- 存疑的显式标注，不混入确信语气；
- 通过才对外。

## 四、铁律

1. 无来源不发布：关键事实必须有可查出处，否则降级措辞。
2. 不编造：禁止生成看似真实但查无实据的引用/数据。
3. 存疑明示：不确定就说不确定，不假装确定。
4. 留痕：每条声明 ↔ 出处可追，事后可核。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 模型内容要对外发布（文章/报告/客服）
- 出现过编造引用或数据
- 要求每条说法都有出处
- 问「怎么验证 AI 给的是真的」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `fact_guard.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `fact_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
