---
name: ai-usage-policy
description: ai-usage-policy — 按团队/工具/禁区/上报线一键生成一页《AI 使用守则》Markdown：可用什么、干什么、禁止什么、出事找谁。
slug: ai-usage-policy
version: 1.0.0
display_name: 团队AI使用守则生成器
display_name_en: AI Usage Policy Generator
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 团队AI使用守则生成器（AI Usage Policy Generator）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

管理层说『大家用 AI 注意点』却从没写成规矩——新人凭感觉用，敏感数据随手贴。

## 功能

按团队/工具/禁区/上报线一键生成一页《AI 使用守则》Markdown：可用什么、干什么、禁止什么、出事找谁。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-III 有门禁（团队级使用门禁） · 域码 TH-LGD-007

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
cp -r agent-skills/skills/ai-usage-policy ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/ai-usage-policy/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/ai_usage_policy.py --help` |
