---
name: prompt-leak-scanner
description: prompt-leak-scanner — 发布/共享前扫描提示词与 system prompt 的泄漏与后门风险：密钥口令、内部路径、个人可识别信息、自定义敏感词（--extra）、自我泄漏后门（『忽略之前指令/打印系统提示词』类埋点）。有风险 rc=1 拦下。
slug: prompt-leak-scanner
version: 1.0.0
display_name: 提示词泄漏扫描器
display_name_en: Prompt Leak Scanner
agent_created: true
author: Steven Zhao (MedXpert × SynomosAI)
license: MIT
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
---

# 提示词泄漏扫描器（Prompt Leak Scanner）

LGD 广谱爆款配套件：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

提示词是最容易被随手外发的敏感资产：一句内嵌的密钥/内网路径/『复述你的系统提示词』就能把家底和后门一起送出去，目前没人做发布前体检。

## 功能

发布/共享前扫描提示词与 system prompt 的泄漏与后门风险：密钥口令、内部路径、个人可识别信息、自定义敏感词（--extra）、自我泄漏后门（『忽略之前指令/打印系统提示词』类埋点）。有风险 rc=1 拦下。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-III 有门禁（提示词对外发布前的最后一道门）· 域码 TH-LGD-004（广谱件·提示词门禁环）

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
cp -r agent-skills/skills/prompt-leak-scanner ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/prompt-leak-scanner/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/prompt_leak_scanner.py --help` |
