---
name: rag-grounding-guard
display_name: RAG事实溯源校验（Grounding Guard）
display_name_en: "RAG Grounding Guard"
description: "当用户说『RAG回答胡说八道/编造』『引用对不对』『回答有依据吗』『检索到的资料支撑不了结论』，或要给 RAG/检索增强回答做事实校验时使用。校验每条声明在检索来源里是否有支撑（ grounding 覆盖率），未覆盖的声明标红为幻觉风险，并要求来源带出处（有籍）。可运行脚本（grounding_check 校验器）。理论根基：LGD 三律之有籍(引用溯源)+有证(防幻觉可核验)。触发词：RAG校验、grounding、事实溯源、防幻觉、引用核查、检索支撑、hallucination、回答有依据吗。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, WebSearch
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - RAG/检索增强的回答出现编造或张冠李戴
  - 要核对 AI 声明是否有检索来源支撑
  - 上线一个知识库问答前做事实校验
  - 用户问「你这话有依据吗」
tags: [RAG校验, grounding, 事实溯源, 防幻觉, 引用核查, 有籍]
slug: rag-grounding-guard
title: RAG事实溯源校验（Grounding Guard）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# RAG事实溯源校验（rag-grounding-guard）

> **定位一句话**：RAG 不死在「检索不到」，死在「检索到了却没用上、还编了没检索到的」——本技能逐条校验声明是否被来源支撑，并强制来源带出处。
> 理论根基：LGD 三律之有籍(引用溯源)+有证(防幻觉可核验)。与 `context-engineering` 同族。

## 一、RAG 幻觉从哪来

1. **无支撑**：模型声明了检索材料里根本没有的内容；
2. **错溯源**：引用的出处与实际不符；
3. **软嫁接**：把 A 文档的结论安到 B 主题上。

## 二、校验两件事

| 校验 | 问 | fail 信号 |
|---|---|---|
| 覆盖 | 每条声明在来源里有支撑词吗？ | 声明的关键实体在来源中零命中 |
| 出处 | 引用带可核查链接吗？ | 引用无 source / 无法定位 |

## 三、主流程（三步）

### 第 1 步 · 抽取声明
把回答拆成可核验声明（含实体/数字/结论句）。

### 第 2 步 · 比对来源
`grounding_check.py` 逐声明在 sources 里查支撑词覆盖，输出覆盖率与未覆盖清单。

### 第 3 步 · 标红+补出处
未覆盖声明标「⚠️ 无来源」，要求补充检索或删除；引用强制带 source。

## 四、铁律

1. 无来源不输出：声明无支撑即标红，不得当作事实。
2. 引用可溯：每条引用带可定位出处。
3. 覆盖率公示：回答附 grounding 覆盖率（有证）。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- RAG 回答出现编造/张冠李戴
- 要核对声明是否有来源
- 上线知识库问答前做事实校验

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `grounding_check.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `grounding_check.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
