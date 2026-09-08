---
name: ai-decision-log
description: ai-decision-log — AI 参与的决策一键留痕（JSONL）：决策/模型/证据/人审人/时间；--report 统计模型使用与人审覆盖，无人审的决策重点标出。
slug: ai-decision-log
version: 1.0.0
display_name: AI决策留痕器
display_name_en: AI Decision Log
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# AI决策留痕器（AI Decision Log）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

出了问题才回头查『这个决定当时是谁让 AI 做的』——没有留痕，复盘全靠回忆。

## 功能

AI 参与的决策一键留痕（JSONL）：决策/模型/证据/人审人/时间；--report 统计模型使用与人审覆盖，无人审的决策重点标出。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-I/II 有籍+有证（AI 参与的决策可追溯） · 域码 TH-LGD-014

## 免责声明

本工具为治理辅助框架，口径以监管官方最新文本为准，不构成法律意见。

---
© MedXpert × SynomosAI · LGD-Powered

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/ai-decision-log ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/ai-decision-log/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/ai_decision_log.py --help` |
