---
name: data-rights-guard
display_name: 训练数据版权护栏（Data Rights Guard）
display_name_en: "Data Rights Guard"
description: "当用户说『爬的数据能拿来训练吗』『数据集没写许可证』『微调数据版权合规吗』『怎么确认数据能商用』，或在用数据(爬取/购买/公开集/用户授权)做训练/微调/评测前想确认版权与许可边界时使用。把每条数据当『带权属的资产』：查许可证·商用权限·署名要求·来源可溯，缺许可的不许进训练集。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：数据版权、训练数据合规、数据集许可证、版权护栏、数据权属、商用权限、data license、微调合规。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要用爬取/购买/公开/用户数据做训练或微调
  - 数据集没写许可证或许可不明
  - 问「这数据能商用吗」
  - 想确认数据来源可溯、署名到位
tags: [数据版权, 训练数据合规, 数据集许可证, 权属护栏, 商用权限, data license, AI合规, 去敏]
slug: data-rights-guard
title: 训练数据版权护栏（Data Rights Guard）
copyright: SynomosAI
description_zh: "当用户说『爬的数据能拿来训练吗』『数据集没写许可证』『微调数据版权合规吗』『怎么确认数据能商用』，或在用数据(爬取/购买/公开集/用户授权)做训练/微调/评测前想确认版权与许可边界时使用。把每条数据当『带权属的资产』：查许可证·商用权限·署名要求·来源可溯，缺许可的不许进训练集。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：数据版权、训练数据合规、数据集许可证、版权护栏、数据权属、商用权限、data license、微调合规。"
description_en: "Copyright and license guard for training data: verify provenance, license terms and commercial-use boundaries before training, fine-tuning or evaluating on scraped, purchased, public or user-authorized data."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 训练数据版权护栏（data-rights-guard）

> **定位一句话**：每条训练数据都是「带权属的资产」——查**许可证 · 商用权限 · 署名要求 · 来源可溯**，缺许可的不许进训练集，别等侵权投诉才回头清。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `doc-desens-scanner`、`ai-policy-radar` 同族。

## 一、为什么数据会「带雷」

- **无许可**：爬来的数据根本没授权训练/商用；
- **非商用锁**：许可证写 Non-Commercial，拿去赚钱违规；
- **署名缺失**：要求 attribution 却没标，违约；
- **来源黑箱**：说不清数据哪来的，出问题无法举证。

本技能管「数据 → 进训练集」前的权属审查。

## 二、四类权属信号

| 项 | 查什么 | 风险 |
|---|---|---|
| 许可证 | 有无 license 字段 | 无 = 高危 |
| 商用权 | 是否允许 commercial | Non-Com = 高危 |
| 署名 | 是否要求 attribution | 未标 = 中 |
| 来源 | 能否追溯出处 | 不可溯 = 中高 |

`scripts/rights_guard.py` 读数据集清单(manifest.json：每条带 license/source/commercial/attribution)，给每条可训练评级 + 整体合规建议。

## 三、主流程（三步）

### 第 1 步 · 登权属（有籍）
每条数据登记 license + source + 商用权限 + 署名要求，单一真源。

### 第 2 步 · 核许可（有证）
按四类信号逐条判「能否训练/商用」；无许可/非商用锁 → 标红。

### 第 3 步 · 门禁（有门禁）
- 高危（无许可/非商用）一律排除出训练集；
- 需署名而未标的，补全署名再进；
- 来源不可溯的，隔离待核，不裸用。

## 四、铁律

1. 无许可不训练：缺 license 的数据默认排除。
2. 商用要看权：Non-Commercial 数据不进商用模型。
3. 署名要到位：要求 attribution 的，训练/发布处标明。
4. 来源要可溯：每条数据能说清出处，便于举证。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要用爬取/购买/公开/用户数据做训练微调
- 数据集没写许可证
- 问「这数据能商用吗」
- 想确认来源可溯、署名到位

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `rights_guard.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `rights_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
