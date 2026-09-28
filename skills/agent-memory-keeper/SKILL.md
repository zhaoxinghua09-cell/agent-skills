---
name: agent-memory-keeper
display_name: 跨会话长期记忆治理（Memory Keeper）
display_name_en: "Agent Memory Keeper"
description: "当用户说『AI又忘了我之前说的』『记忆越来越乱/重复/互相矛盾』『长期记忆怎么管』『记忆库该清理了』，或要设计/治理一个 agent 的跨会话记忆（笔记/知识库/偏好/项目约定）时使用。把记忆当成『有籍贯、可审计、能收敛』的资产：审计重复·孤儿·陈旧·无溯源四维度，给出收敛(单一真源)+门禁(改前备份)两步流程与可运行脚本（记忆审计器）。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：长期记忆、跨会话记忆、memory governance、记忆治理、记忆重复、记忆冲突、记忆溯源、agent记忆、知识库去重、记忆清理。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - AI 在关掉对话后丢失了用户之前明确说过的约定/偏好
  - 记忆库里出现多条互相矛盾或高度重复的内容
  - 要搭建或清理一个 agent 的长期记忆（笔记/知识库/项目约定）
  - 用户抱怨「你上次记的不算数」或「记忆怎么乱了」
  - 想给记忆条目加溯源（谁、何时、从哪来）
tags: [长期记忆, memory governance, 记忆治理, 记忆去重, 跨会话, 记忆溯源, agent优化]
slug: agent-memory-keeper
title: 跨会话长期记忆治理（Memory Keeper）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 跨会话长期记忆治理（agent-memory-keeper）

> **定位一句话**：记忆不是「能存」，而是「**有籍贯、可审计、能收敛**」——本技能把 agent 的长期记忆变成可追溯、无重复、可回滚的资产。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `context-engineering`、`memory-governance` 同族。

## 一、为什么记忆会越存越乱

长周期使用 agent，记忆必然劣化：

1. **重复**：同一约定在不同笔记里各写一遍 → 改一处另一处还是旧的；
2. **矛盾**：新旧偏好叠加，库里同时存在「爱用红色」「别用红色」；
3. **无籍**：条目没写来源/时间 → 真出问题无法追溯是谁记的、哪来的；
4. **陈旧**：三个月前的临时约定还当真源 → 误导当前决策。

本技能管「记忆入库后」这一层，不管模型本身。

## 二、记忆审计四维度

对记忆库每条目打分（pass / warn / fail）：

| 维度 | 问自己 | fail 信号 |
|---|---|---|
| 重复 | 这条和别的重复吗？ | 同一约定出现 ≥2 次 |
| 孤儿 | 它有归属吗？ | 无 category / 无项目归属 |
| 陈旧 | 还有效吗？ | 超过 N 天未更新且非长期铁律 |
| 无籍 | 谁/何时/从哪来？ | 缺 source / 缺 updated |

`scripts/memory_audit.py` 可自动扫目录/JSONL 并产出问题清单。

## 三、主流程（两步）

### 第 1 步 · 收敛（单一真源）
- 重复条目合并为一份，旧副本标 `deprecated` 或删除；
- 矛盾条目保留最新一条，其余加「已作废」注释；
- 每条记忆强制带 `source` + `updated` 字段（有籍）。

### 第 2 步 · 门禁（有门禁）
改记忆结构 / 批量删条目前走保险操作：
- 先备份整个记忆目录；
- 列清单确认「删哪些、合并哪些」再动；
- 关键铁律（用户硬偏好）单独置顶文件，不与普通笔记混。

## 四、记忆条目模板（推荐）

```yaml
- title: 用户偏好-回复语言
  source: 用户 2026-09-01 会话
  updated: 2026-09-01
  category: 偏好
  content: 默认用简体中文回答
```

## 五、铁律

1. 单一真源：同一约定只存一份，重复即删。
2. 必有籍：每条记忆带 source + updated，否则视为临时草稿。
3. 改前备份：批量动记忆结构走门禁，可逆零损失。
4. 铁律隔离：用户硬偏好单独置顶，不与普通笔记混淆。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 关掉对话后 AI 丢失了你之前说过的约定
- 记忆库里出现矛盾或重复内容
- 要搭/清理 agent 的长期记忆或知识库
- 想给记忆条目加溯源以便追责

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `memory_audit.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `memory_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
