---
name: lgd-badge-verify
description: lgd-badge-verify — 验徽章证书：指纹重算防篡改 + 证据哈希格式校验 + 台账对账（serial 存在且未吊销）。
slug: lgd-badge-verify
version: 1.0.0
display_name: LGD 徽章验真器
display_name_en: LGD Badge Verifier
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
copyright: XLGD · SynomosAI
---
# LGD 徽章验真器（LGD Badge Verifier）

LGD 闭环最后一环：**护照（有籍）→ 证据链（有证）→ 门禁（有门禁）→ 徽章（签发/验真）**。

## 解决什么痛点

有签发无验真，徽章可伪造：闭环缺反向校验，信任链断裂。

## 功能

验徽章证书：指纹重算防篡改 + 证据哈希格式校验 + 台账对账（serial 存在且未吊销）。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-I 有籍 / LGD-II 有证 / LGD-III 有门禁（凡自治之物）
- 域码：TH-LGD-001（闭环执行器·徽章环）

## 免责声明

本工具为治理辅助框架，签发效力以使用方组织制度为准。

---
© SynomosAI Governance Line · LGD-Powered

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28/skills/lgd-badge-verify

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28 一致
cp -r agent-skills/skills/lgd-badge-verify ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/lgd-badge-verify/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/badge_verify.py --help` |
