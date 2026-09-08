---
name: data-minimizer
description: data-minimizer — 把文本里的手机号/邮箱/证件号/长号/指定人名一键打码后交给 AI，输出脱敏文本+脱敏报告；支持 --names 自定义人名、--json。
slug: data-minimizer
version: 1.0.0
display_name: 给AI前脱敏器
display_name_en: Data Minimizer
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 给AI前脱敏器（Data Minimizer）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

想让 AI 帮忙处理含真实客户/同事信息的文本，又怕把 PII 直接喂给第三方——手工打码慢且漏。

## 功能

把文本里的手机号/邮箱/证件号/长号/指定人名一键打码后交给 AI，输出脱敏文本+脱敏报告；支持 --names 自定义人名、--json。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-III 有门禁（交给 AI 前的脱敏门） · 域码 TH-LGD-005

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
cp -r agent-skills/skills/data-minimizer ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/data-minimizer/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/data_minimizer.py --help` |
