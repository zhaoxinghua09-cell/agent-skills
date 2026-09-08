---
name: contract-interact-checklist
description: 合约交互风险清单 — 智能合约交互前六项风险自检（审计/地址/授权额度/撤销/私钥/小额试单），未完成即 FAIL（零依赖）
slug: contract-interact-checklist
version: 1.0.0
display_name: 合约交互风险清单
display_name_en: Contract Interact Checklist
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 合约交互风险清单 / Contract Interact Checklist

**contract-interact-checklist** v1.0.0 · LGD 护城河家族 · 零依赖
域：区块链 · 三律映射：TH-LGD-021

## 痛点
无限授权、假合约、私钥贴网页——交互前没有一道标准自检流程

## 用法
```bash
python scripts/contract_interact_checklist.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 区块链 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。
