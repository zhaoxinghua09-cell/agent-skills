---
name: ai-content-discloser
description: ai-content-discloser — 为 AI 参与（全生成/辅助/混合）的内容一键生成合规披露声明：显式声明（中/EN）+ 隐式元数据标注 + 平台贴法，依据中国《人工智能生成合成内容标识办法》与 EU AI Act 第 50 条口径。
slug: ai-content-discloser
version: 1.0.0
display_name: AI 内容披露生成器
display_name_en: AI Content Discloser
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, workbuddy, openai-agents]
copyright: SynomosAI
description_zh: "ai-content-discloser — 为 AI 参与（全生成/辅助/混合）的内容一键生成合规披露声明：显式声明（中/EN）+ 隐式元数据标注 + 平台贴法，依据中国《人工智能生成合成内容标识办法》与 EU AI Act 第 50 条口径。"
description_en: "One-click compliant disclosure for AI-involved content: explicit statements (zh/en) + implicit metadata labeling + platform placement, per China's AI-generated content labeling rules and the EU AI Act."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
standards_ref: ["EU AI Act"]
---
# AI 内容披露生成器（AI Content Discloser）

LGD 广谱爆款配套件：把"有籍·有证·有门禁"做成人人天天用得上的工具。

## 解决什么痛点

发 AI 内容不知道怎么标、标什么：监管已要求显式+隐式标识，漏标有下架/处罚风险，手工写声明费时且口径不统一。

## 功能

为 AI 参与（全生成/辅助/混合）的内容一键生成合规披露声明：显式声明（中/EN）+ 隐式元数据标注 + 平台贴法，依据中国《人工智能生成合成内容标识办法》与 EU AI Act 第 50 条口径。

## 用法

见 `scripts/` 下脚本 `--help`。零依赖（stdlib only），Windows/Linux/macOS 均可运行。

## 对应理论

- LGD-II 有证（披露 = 内容出处有证）· 域码 TH-LGD-002（广谱件·披露环）

## 免责声明

本工具为治理辅助框架，口径以监管官方最新文本为准，不构成法律意见。

---
© MedXpert × SynomosAI · LGD-Powered

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/ai-content-discloser

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/ai-content-discloser ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/ai-content-discloser/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/ai_content_discloser.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `ai_content_discloser.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `ai_content_discloser.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
