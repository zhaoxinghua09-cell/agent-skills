---
name: agent-kill-switch
description: agent-kill-switch — 部署智能体前生成『制动卡』：停止条件/断权动作/责任人/恢复条件；--check 校验制动卡字段齐全，缺项 rc=1 不许上线。
slug: agent-kill-switch
version: 1.0.0
display_name: 智能体紧急制动卡
display_name_en: Agent Kill Switch
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 智能体紧急制动卡（Agent Kill Switch）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

智能体跑飞了才知道没人知道怎么停——停止条件、断权动作、责任人全是空白。

## 功能

部署智能体前生成『制动卡』：停止条件/断权动作/责任人/恢复条件；--check 校验制动卡字段齐全，缺项 rc=1 不许上线。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-III 有门禁（先想好怎么停，再放它跑） · 域码 TH-LGD-009

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
cp -r agent-skills/skills/agent-kill-switch ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/agent-kill-switch/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/agent_kill_switch.py --help` |
