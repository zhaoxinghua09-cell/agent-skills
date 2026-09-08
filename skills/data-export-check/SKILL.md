---
name: data-export-check
description: 数据出境合规自检 — 数据出境前五项义务自检（分级/单独同意/PIA/标准合同或安全评估/留痕），缺项即 FAIL（零依赖）
slug: data-export-check
version: 1.0.0
display_name: 数据出境合规自检
display_name_en: Data Export Check
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 数据出境合规自检 / Data Export Check

**data-export-check** v1.0.0 · LGD 护城河家族 · 零依赖
域：数据合规/政务 · 三律映射：TH-LGD-024

## 痛点
用境外SaaS/云就等于数据出境，义务没走完就是监管风险

## 用法
```bash
python scripts/data_export_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 数据合规/政务 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。
