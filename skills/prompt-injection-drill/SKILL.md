---
name: prompt-injection-drill
description: prompt-injection-drill — 为你的 system prompt 生成 8 类注入攻击演练用例（角色覆盖/指令覆盖/诱导泄密/编码绕过/工具滥用/越权伪造/长程拖延/拒绝绕过）+ 期望行为清单，供上线前红队自测。
slug: prompt-injection-drill
version: 1.0.0
display_name: 提示词注入演练器
display_name_en: Prompt Injection Drill
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 提示词注入演练器（Prompt Injection Drill）

LGD 广谱爆款系列：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

提示词上线从没挨过打：用户一句『忽略之前的指令』就缴械——不是被高手指破的，是被小学生随口破的。

## 功能

为你的 system prompt 生成 8 类注入攻击演练用例（角色覆盖/指令覆盖/诱导泄密/编码绕过/工具滥用/越权伪造/长程拖延/拒绝绕过）+ 期望行为清单，供上线前红队自测。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-III 有门禁（上线前先挨一遍打） · 域码 TH-LGD-013

## 免责声明

本工具为治理辅助框架，口径以监管官方最新文本为准，不构成法律意见。

---
© MedXpert × SynomosAI · LGD-Powered
