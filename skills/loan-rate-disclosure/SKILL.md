---
name: loan-rate-disclosure
description: 借贷利率披露校验器 — 校验借贷报价是否按年化口径披露、是否超基准利率4倍司法保护上限（零依赖）
slug: loan-rate-disclosure
version: 1.0.0
display_name: 借贷利率披露校验器
display_name_en: Loan Rate Disclosure Check
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 借贷利率披露校验器 / Loan Rate Disclosure Check

**loan-rate-disclosure** v1.0.0 · LGD 护城河家族 · 零依赖
域：金融 · 三律映射：TH-LGD-015

## 痛点
给AI/人工写借贷宣传时，不报年化、超4倍LPR红线，一眼翻车

## 用法
```bash
python scripts/loan_rate_disclosure.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 金融 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/loan-rate-disclosure ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/loan-rate-disclosure/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/loan_rate_disclosure.py --help` |
