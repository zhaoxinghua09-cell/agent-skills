---
name: contract-clause-check
description: 合同高危条款扫描器 — 签合同前扫必备条款（违约/争议/管辖）与高危表述（最终解释权/自动续期/高违约金），缺项即 FAIL（零依赖）
slug: contract-clause-check
version: 1.0.0
display_name: 合同高危条款扫描器
display_name_en: Contract Clause Check
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 合同高危条款扫描器 / Contract Clause Check

**contract-clause-check** v1.0.0 · LGD 护城河家族 · 零依赖
域：法律 · 三律映射：TH-LGD-022

## 痛点
合同不看条款直接签，违约金30%、单方解释权、没写管辖全踩坑

## 用法
```bash
python scripts/contract_clause_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 法律 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/contract-clause-check ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/contract-clause-check/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/contract_clause_check.py --help` |
