---
name: multi-agent-conductor
display_name: 多智能体编排（Multi-Agent Conductor）
display_name_en: "Multi-Agent Conductor"
description: "当用户说『这个任务好大要拆给多个AI』『多智能体怎么分工』『agent之间怎么不串权限』『编排几个agent协作』，或要把一个大任务拆成多个 agent 并行/串行协作时使用。把任务分解为子任务→分配角色→划清每个 agent 的边界与禁止项（有门禁），输出编排方案+边界清单。可运行脚本（conductor_plan 规划器）。理论根基：LGD 三律之有门禁（任务边界+权限隔离）。触发词：多智能体、multi-agent、agent编排、任务分解、协作agent、agent权限、并行agent、orchestration。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 一个大任务要拆给多个 agent 协作
  - 多 agent 出现权限串台/互相改对方产物
  - 要设计 agent 团队的分工与边界
  - 担心某个 agent 越权访问不该碰的资源
tags: [多智能体, multi-agent, 编排, 任务分解, 协作, 有门禁]
slug: multi-agent-conductor
title: 多智能体编排（Multi-Agent Conductor）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 多智能体编排（multi-agent-conductor）

> **定位一句话**：多 agent 协作翻车，几乎都因为「边界没划清」——本技能把大任务拆成角色、给每个 agent 定死「能做什么、禁止碰什么」。
> 理论根基：LGD 三律之有门禁（任务边界 + 权限隔离）。与 `context-engineering`、`agent-redteam-kit` 同族。

## 一、多 agent 怎么乱的

1. **串权限**：A agent 改了 B 的中间产物 → 结果不可控；
2. **重复劳动**：两个 agent 干同一件事；
3. **无总控**：没人汇总，输出互相矛盾。

## 二、编排三要素

| 要素 | 问 |
|---|---|
| 分解 | 大任务能拆成几个独立子任务？ |
| 角色 | 每个子任务要什么专长？ |
| 边界 | 每个 agent 禁止碰什么（文件/数据/其他 agent 产物）？ |

## 三、主流程（三步）

### 第 1 步 · 分解
把任务拆成可独立交付的子任务，标依赖（并行/串行）。

### 第 2 步 · 分配+划界（有门禁）
`conductor_plan.py` 输出角色表 + 每个 agent 的「允许/禁止」边界。

### 第 3 步 · 总控
设一个 conductor 汇总、校验冲突、拦截越界写操作。

## 四、铁律

1. 边界即门禁：每个 agent 明确禁止项，越界写操作拦截。
2. 产物隔离：agent 只写自己目录，不碰他人。
3. 单点汇总：conductor 唯一出口，避免多份矛盾结论。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 大任务要拆给多个 agent
- 多 agent 权限串台/产物冲突
- 要设计 agent 团队分工

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `conductor_plan.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `conductor_plan.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
