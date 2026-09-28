---
name: prompt-compressor
display_name: 提示/上下文压缩（Prompt Compressor）
display_name_en: "Prompt Compressor"
description: "当用户说『提示词太长/token烧太快』『上下文塞不下了』『把这段压缩一下还别丢重点』『长文档怎么塞进窗口』，或要压低 agent 每轮上下文成本时使用。基于「信息密度」裁剪：保留关键词密集/位置靠前的句子，删冗余/客套/复述，给出可运行脚本（提示压缩器，按密度+位置打分删句）。与 context-engineering 互补：context 管『放什么』，compressor 管『怎么压短』。理论根基：LGD 三律之收敛（删除冗余，单一有效信息）。触发词：提示压缩、prompt压缩、上下文压缩、压缩token、长文本精简、context压缩、省token、摘要进窗口、prompt shorten。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 提示词/上下文太长，token 成本或窗口吃紧
  - 要把长文档压成能进窗口的精华
  - 想在不丢重点的前提下砍掉冗余句子
  - 搭 agent 时每轮上下文预算超标
tags: [提示压缩, prompt compressor, 上下文压缩, 省token, 长文本精简, 收敛]
slug: prompt-compressor
title: 提示/上下文压缩（Prompt Compressor）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 提示/上下文压缩（prompt-compressor）

> **定位一句话**：压缩不是「删字」，是「按信息密度保留有效句、删冗余与复述」——本技能把长提示/长文档压成不丢重点的短版。
> 理论根基：LGD 三律之收敛（删除冗余，单一有效信息）。与 `context-engineering` 互补。

## 一、为什么需要压缩

1. **窗口吃紧**：长文档整篇塞 → 关键指令被稀释；
2. **钱白烧**：客套/复述句占 token 不贡献信息；
3. **质量反降**：噪声多 → 模型被带偏。

## 二、压缩三原则

| 原则 | 做法 |
|---|---|
| 密度优先 | 关键词密集的句子保留，水句删 |
| 位置加权 | 开头/结尾句权重高（常含约束/结论） |
| 不破结构 | 保留列表/代码/数字，只压叙述 |

## 三、主流程（三步）

### 第 1 步 · 分句打分
按「关键词命中数 + 长度适中 + 位置权重」给每句打分。

### 第 2 步 · 截断
按目标压缩比（默认 50%）从低分往高分页删，直到达标。

### 第 3 步 · 校验
人工/自动核对：约束句、数字、代码是否还在。

`scripts/compress_prompt.py` 自动完成 1-2 步并输出压缩版。

## 四、铁律

1. 约束不删：含「必须/禁止/默认」的句子最高优先级保留。
2. 数字/代码不压：保留原样，只压叙述。
3. 可回滚：压缩前留原文备份。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 提示/上下文太长、token 超标
- 要压长文档进窗口
- 想降本又不丢重点

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `compress_prompt.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `compress_prompt.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
