---
name: eval-bench-builder
display_name: 评测基准构建器（Eval Bench Builder）
display_name_en: "Eval Benchmark Builder"
description: "当用户说『怎么评测这个AI/技能好不好』『给我造个测试集』『评测用例怎么设计』『要可复现的评测』，或要给一个 agent/模型/技能建可复现评测基准时使用。从能力说明+边界用例生成结构化 eval 样本（输入/期望/判定标准），保证可复现、可回归。可运行脚本（bench_build 生成器）。理论根基：LGD 三律之有证（评测可复现、可核验）。触发词：评测基准、eval、测试集、benchmark、可复现评测、评测用例、怎么测AI。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 要评测一个 agent/模型/技能的效果
  - 需要可复现、可回归的测试集
  - 不知道评测用例怎么设计
  - 收到「造个评测」类指令
tags: [评测基准, eval, benchmark, 测试集, 可复现, 有证]
slug: eval-bench-builder
title: 评测基准构建器（Eval Bench Builder）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 评测基准构建器（eval-bench-builder）

> **定位一句话**：「AI 好不好」不能靠感觉——本技能把能力说明+边界用例变成结构化、可复现的评测样本（输入/期望/判定标准）。
> 理论根基：LGD 三律之有证（评测可复现、可核验）。与 `skill-quality-gate` 互补（它管发布门槛，本技能管效果度量）。

## 一、为什么评测要建基准

1. **主观**：「感觉还行」不可比、不可回归；
2. **漏边界**：只测 happy path，极端用例翻车；
3. **不可复现**：没固定样本，两次结果没法比。

## 二、样本三要素

| 要素 | 含义 |
|---|---|
| input | 输入 |
| expect | 期望输出/行为 |
| judge | 判定标准（含/精确/规则） |

## 三、主流程（三步）

### 第 1 步 · 列能力
把被测对象拆成能力点 + 边界（失败/对抗/极端）。

### 第 2 步 · 生成样本（有证）
`bench_build.py` 读 spec，产出 JSONL 评测集（input/expect/judge）。

### 第 3 步 · 回归
每次改动跑同一基准，对比分数变化。

## 四、铁律

1. 覆盖边界：happy path + 失败 + 对抗都要有。
2. 判定可机读：judge 明确，不靠人主观。
3. 锁定样本：基准固定，改动只动被测物。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要评测 agent/模型/技能
- 需要可回归测试集
- 不知道评测用例怎么设计

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `bench_build.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `bench_build.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
