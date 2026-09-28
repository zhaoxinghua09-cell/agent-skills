---
name: doc-desens-scanner
display_name: 文档智能去敏（Desens Scanner）
display_name_en: "Document Desensitization Scanner"
description: "当用户说『这篇文档有敏感信息要发出去』『先脱敏再发』『别把内部路径/密钥/人名露出去』『对外发布前扫一遍隐私』，或要把文档/代码/日志对外前做去敏时使用。扫描 个人标识(PII)·密钥·内部路径·内部项目代号 四类敏感项并打码/留痕，输出去敏版+清单（有证：脱敏动作可审计）。可运行脚本（desens_scan 扫描器）。理论根基：LGD 三律之有证（脱敏留痕，可追责）。触发词：去敏、脱敏、desensitize、脱敏扫描、隐私打码、密钥泄露、内部路径、对外发布前检查、PII。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI安全
platforms: [windows, macos, linux]
read_when:
  - 文档/代码/日志要对外发布或发给客户前
  - 担心泄露密钥、内部路径、人名、内部项目代号
  - 要做隐私合规的发布前检查
  - 收到「先脱敏」类指令
tags: [去敏, 脱敏, desensitize, 隐私打码, PII, 密钥, 发布前检查]
slug: doc-desens-scanner
title: 文档智能去敏（Desens Scanner）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# 文档智能去敏（doc-desens-scanner）

> **定位一句话**：对外发布前扫一遍——把 PII/密钥/内部路径/内部项目代号找出来打码，并留一份脱敏清单（有证：谁脱了什么、何时）。
> 理论根基：LGD 三律之有证（脱敏动作可审计、可追责）。与 `release-gate`、`prompt-injection-shield` 同族。

## 一、为什么要去敏

对外文档/代码/日志常混入：

1. **PII**：姓名、手机、身份证、邮箱；
2. **密钥**：api key / token / password；
3. **内部路径**：Windows 用户目录 / home 目录 / 内网域名；
4. **内部项目代号**：未公开项目名、任职单位标识。

泄漏即事故。发布闸门第一环就是去敏。

## 二、扫描四类敏感项

| 类 | 模式 |
|---|---|
| PII | 手机号/身份证/邮箱/中文姓名( heuristics) |
| 密钥 | 以 `sk-`/`ghp_` 前缀的令牌 / `api_key=`/`password` 赋值 |
| 路径 | Windows 用户目录 / home 目录 / 内网 `.local` 域 |
| 代号 | 用户自定义敏感词表（内部项目代号） |

## 三、主流程（三步）

### 第 1 步 · 扫描（有证）
`desens_scan.py` 跑四类模式，列出命中位置与类型。

### 第 2 步 · 打码
默认替换为 `***` 或 `[REDACTED]`；密钥/路径优先删而非留痕。

### 第 3 步 · 留痕
输出 `desens_report.json`：每条命中类型+位置+处理方式（有证）。

## 四、铁律

1. 对外必扫：任何对外文档先过本技能。
2. 密钥即删：密钥/密码不保留掩码，直接删除。
3. 留痕可溯：脱敏清单随文档归档。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要对外发文档/代码/日志
- 文档里可能有密钥或内部路径
- 做隐私合规发布前检查

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `desens_scan.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `desens_scan.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
