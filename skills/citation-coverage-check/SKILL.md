---
name: citation-coverage-check
description: citation-coverage-check — 扫描文章中含数字/日期/论断的句子，统计带来源标注（据/来源/source/链接/文献）的比例；低于阈值 rc=1，逐句列出缺出处清单。
slug: citation-coverage-check
version: 1.0.0
display_name: 引用覆盖率检查器
display_name_en: Citation Coverage Check
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 引用覆盖率检查器（Citation Coverage Check）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

AI 生成的研究/报告看着专业，但哪些数字有来源、哪些是编的没人检查——引用覆盖率一眼见底。

## 功能

扫描文章中含数字/日期/论断的句子，统计带来源标注（据/来源/source/链接/文献）的比例；低于阈值 rc=1，逐句列出缺出处清单。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-II 有证（论断要带出处） · 域码 TH-LGD-011

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
cp -r agent-skills/skills/citation-coverage-check ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/citation-coverage-check/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/citation_coverage_check.py --help` |
