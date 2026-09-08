---
name: ai-reply-heuristics
description: ai-reply-heuristics — 启发式估计一段文字的 AI 痕迹强度：套话密度/破折号频率/句长均匀度/排比结构 → 0-100 分与三档区间（启发式，不构成判定，附免责）。
slug: ai-reply-heuristics
version: 1.0.0
display_name: AI痕迹启发式检查器
display_name_en: AI Reply Heuristics
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# AI痕迹启发式检查器（AI Reply Heuristics）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

收到一篇『不知道是不是 AI 写的』文字：全文照信有风险，全盘怀疑也不公平——需要一个提示器而非审判器。

## 功能

启发式估计一段文字的 AI 痕迹强度：套话密度/破折号频率/句长均匀度/排比结构 → 0-100 分与三档区间（启发式，不构成判定，附免责）。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-II 有证（出处存疑要有提示） · 域码 TH-LGD-010

## 免责声明

本工具为治理辅助框架，口径以监管官方最新文本为准，不构成法律意见。

---
© MedXpert × SynomosAI · LGD-Powered
