---
name: output-schema-guard
display_name: 结构化输出校验护栏（Schema Guard）
display_name_en: "Output Schema Guard"
description: "当用户说『模型返回的JSON又崩了』『字段缺失对不上』『下游解析失败』『怎么强制LLM输出合规结构』，或要把 LLM 的 JSON/结构化输出接进代码（API/数据库/表单）时使用。把模型输出当『不可信外部输入』：用 schema 校验必填字段·类型·枚举，缺则给可执行的修复提示而非裸报错。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：结构化输出、JSON校验、schema guard、输出格式、字段缺失、模型输出解析、function calling、tool output。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - LLM 返回的 JSON 偶发缺字段或类型不对，导致下游解析崩溃
  - 要把模型输出接进数据库 / API / 表单，必须结构稳定
  - 在用 function calling / tool 定义，但模型回传参数不可信
  - 用户抱怨「这次能跑、下次就挂」的不稳定解析
tags: [结构化输出, schema校验, JSON guard, function calling, 输出格式, agent优化, 可靠性]
slug: output-schema-guard
title: 结构化输出校验护栏（Schema Guard）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 结构化输出校验护栏（output-schema-guard）

> **定位一句话**：模型输出是「不可信的外部输入」——在它进你的代码前，先过一道 schema 校验：必填、类型、枚举缺一不可，缺了就吐**可执行的修复提示**而不是裸崩。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `context-engineering`、`skill-quality-gate` 同族。

## 一、为什么模型 JSON 会反复崩

- **必填丢**：模型「忘了」某个字段，下游 `.get("x")` 拿到 None；
- **类型飘**：时而字符串、时而数字，强转型报错；
- **枚举越界**：状态返回 `"done1"` 而非约定的 `"done"`；
- **嵌套错位**：数组里塞了对象，结构对不上；
- **幻觉键**：多加了一堆你不认识的字段，消费端迷糊。

本技能管「拿到模型文本 → 变成可信对象」这一关。

## 二、校验四维（schema 驱动）

| 维度 | 检查 | fail 信号 |
|---|---|---|
| 必填 | 字段存在且非 None | 缺 `required` 中任一项 |
| 类型 | 值类型匹配 `type` | str/int/bool/list/dict 不符 |
| 枚举 | 值在 `enum` 白名单 | 超出允许取值 |
| 结构 | 嵌套 list/dict 形状 | 数组元素类型不一致 |

`scripts/schema_guard.py` 读取 schema(JSON) + 待校验文本/文件，逐维给出 pass/fail + 修复提示。

## 三、主流程（两步）

### 第 1 步 · 定义 schema（有籍）
把消费端真正需要的字段写成一份 schema（必填清单 + 类型 + 枚举），单一真源，所有人复用。

### 第 2 步 · 校验 + 修复提示（有证·有门禁）
- 校验失败 → 不抛异常中断业务，而是返回结构化错误：`{field, expected, got, hint}`；
- 把错误回灌给模型「按此修复重出」，最多重试 N 次（门禁：防止无限重试烧 token）；
- 通过才进入下游。

## 四、schema 示例

```json
{
  "required": ["name", "status"],
  "fields": {
    "name":   {"type": "str"},
    "status": {"type": "str", "enum": ["pending", "done", "failed"]},
    "score":  {"type": "int", "required": false}
  }
}
```

## 五、铁律

1. 模型输出不可信：凡是进代码的，先校验再消费。
2. 失败要给可执行提示：返回缺什么、期望什么，而非裸异常。
3. 重试有上限：修复回灌最多 N 次，门禁防失控。
4. schema 单一真源：消费端契约只写一份，别散落各处。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 模型返回的 JSON 偶发缺字段、类型不对
- 要把 LLM 输出接进数据库 / API / 表单
- 用 function calling 但参数不可信
- 解析「时好时坏」，想一劳永逸

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `schema_guard.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `schema_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
