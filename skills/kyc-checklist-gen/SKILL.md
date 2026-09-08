---
name: kyc-checklist-gen
description: KYC 材料齐备清单 — 一键生成个人/企业 KYC 必备材料清单并核算齐备度，缺项即 FAIL（零依赖）
slug: kyc-checklist-gen
version: 1.0.0
display_name: KYC 材料齐备清单
display_name_en: KYC Checklist Generator
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# KYC 材料齐备清单 / KYC Checklist Generator

**kyc-checklist-gen** v1.0.0 · LGD 护城河家族 · 零依赖
域：金融 · 三律映射：TH-LGD-016

## 痛点
开户/接商户前不知道 KYC 要备什么材料，来回补件浪费时间

## 用法
```bash
python scripts/kyc_checklist_gen.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 金融 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。
