---
name: token-disclosure-check
description: 代币信息披露检查器 — 白皮书/披露文案核查必备要素（总量/分配/锁仓/团队/风险提示），含收益承诺即 FAIL（零依赖）
slug: token-disclosure-check
version: 1.0.0
display_name: 代币信息披露检查器
display_name_en: Token Disclosure Check
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 代币信息披露检查器 / Token Disclosure Check

**token-disclosure-check** v1.0.0 · LGD 护城河家族 · 零依赖
域：区块链 · 三律映射：TH-LGD-020

## 痛点
项目方披露缺斤少两还暗带保证收益话术，接不住监管也坑持有人

## 用法
```bash
python scripts/token_disclosure_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 区块链 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。
