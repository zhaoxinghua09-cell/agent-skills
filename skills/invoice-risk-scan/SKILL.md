---
name: invoice-risk-scan
description: 发票要素风险扫描 — 报销/入账前扫发票要素：税号格式、金额、日期合理性，异常即拦（零依赖）
slug: invoice-risk-scan
version: 1.0.0
display_name: 发票要素风险扫描
display_name_en: Invoice Risk Scan
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 发票要素风险扫描 / Invoice Risk Scan

**invoice-risk-scan** v1.0.0 · LGD 护城河家族 · 零依赖
域：金融/财税 · 三律映射：TH-LGD-017

## 痛点
报销发票税号抄错一位、日期离谱，财务退单反复折腾

## 用法
```bash
python scripts/invoice_risk_scan.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 金融/财税 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/invoice-risk-scan ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/invoice-risk-scan/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/invoice_risk_scan.py --help` |
