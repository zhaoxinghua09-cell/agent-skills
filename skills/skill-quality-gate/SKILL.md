---
name: skill-quality-gate
display_name: 技能质量门禁（Skill Quality Gate）
display_name_en: "Skill Quality Gate"
description: "当用户说『这个技能能不能发』『发布前检查下质量』『技能缺什么字段』『提交市场前过一遍门禁』，或要把一个 skill/提示词/agent 配置提交到市场或上线前做质量校验时使用。9 维校验（frontmatter八字段/脚本可读/图标/README/无密钥/双语/触发词/门禁节/去敏），逐维 pass/fail，不过闸不发布（有门禁）。可运行脚本（quality_gate 校验器）。理论根基：LGD 三律之有门禁（发布前必过闸）。触发词：技能质检、质量门禁、发布前检查、skill检查、提交市场、quality gate、技能能不能发。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 要把 skill/提示词/agent 配置提交到市场或仓库前
  - 不确定技能是否缺字段、能否发布
  - 做发布闸门（去敏+质检）流程
  - 收到「发布前检查下」类指令
tags: [技能质检, quality gate, 发布前检查, 门禁, 有门禁]
slug: skill-quality-gate
title: 技能质量门禁（Skill Quality Gate）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 技能质量门禁（skill-quality-gate）

> **定位一句话**：技能不是写完就能发——本技能用 9 维校验卡一道闸，不过闸不许发布。
> 理论根基：LGD 三律之有门禁（发布前必过闸）。与 `release-gate`、`doc-desens-scanner` 同族。

## 一、为什么需要发布门禁

技能市场里大量「发了但跑不起来/泄密/无说明」的劣质件。门禁保证：能跑、说清、不泄。

## 二、9 维校验

| # | 维度 | pass 标准 |
|---|---|---|
| 1 | frontmatter 八字段 | name/display_name/display_name_en/description/slug/version/author/category 齐全 |
| 2 | 脚本可读 | scripts/ 下 .py 能被 py_compile 编译 |
| 3 | 图标 | icon.png 存在且 ≤512 可解 |
| 4 | README | 有双语简介 |
| 5 | 无密钥 | 全仓无 api_key/ghp_/password 明文 |
| 6 | 双语 | description 与 README 含中英 |
| 7 | 触发词 | SKILL.md 含 read_when 或触发词 |
| 8 | 门禁节 | 含「铁律」或「门禁」节 |
| 9 | 去敏 | 无 Windows 用户目录 / 内网路径 / 任职单位名 |

## 三、主流程（两步）

### 第 1 步 · 校验（有证）
`quality_gate.py` 跑 9 维，输出逐维结果与总评。

### 第 2 步 · 过闸（有门禁）
任意一维 fail → 拦截发布，列出修复项；全 pass → 放行。

## 四、铁律

1. 不过闸不发：任一 fail 即拦截。
2. 修复可追溯：fail 项带明确修复指引。
3. 留痕：每次门禁结果入发布清单（有证）。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要发布/提交一个技能到市场
- 不确定技能缺什么字段
- 建发布闸门流程

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `quality_gate.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `quality_gate.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
