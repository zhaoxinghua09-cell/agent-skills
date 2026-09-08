---
name: health-claim-guard
description: 健康宣称合规扫描 — 保健品/食品宣传文案扫违规疗效宣称（根治/治愈/无副作用等），缺警示语即 FAIL（零依赖）
slug: health-claim-guard
version: 1.0.0
display_name: 健康宣称合规扫描
display_name_en: Health Claim Guard
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 健康宣称合规扫描 / Health Claim Guard

**health-claim-guard** v1.0.0 · LGD 护城河家族 · 零依赖
域：医疗健康 · 三律映射：TH-LGD-023

## 痛点
带货文案随手写根治、有效率99%，广告法罚款动辄数十万

## 用法
```bash
python scripts/health_claim_guard.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 医疗健康 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。
