---
name: agent-boarding-pass
description: agent-boarding-pass — 给任何 AI 智能体签发一张可验证的『登机牌』：身份 + 证据哈希 + 权限白名单 + 有效期，SHA-256 防篡改；一条命令验真（指纹重算 + 过期校验）。可整张贴进 system prompt / 仓库 / 工单。
slug: agent-boarding-pass
version: 1.0.0
display_name: 智能体登机牌
display_name_en: Agent Boarding Pass
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 智能体登机牌（Agent Boarding Pass）

LGD 广谱爆款配套件：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

把 AI 智能体接入团队/流程时说不清它是谁、凭什么、能干什么、干到什么时候——口头约定无法校验，出事无据可查。

## 功能

给任何 AI 智能体签发一张可验证的『登机牌』：身份 + 证据哈希 + 权限白名单 + 有效期，SHA-256 防篡改；一条命令验真（指纹重算 + 过期校验）。可整张贴进 system prompt / 仓库 / 工单。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- 三律便携化（有籍=身份入牌 · 有证=证据哈希入牌 · 有门禁=无三律不签发）· 域码 TH-LGD-003（广谱件·证件环）

## 免责声明

本工具为治理辅助框架，口径以监管官方最新文本为准，不构成法律意见。

---
© MedXpert × SynomosAI · LGD-Powered
