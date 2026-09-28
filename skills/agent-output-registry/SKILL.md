---
name: agent-output-registry
slug: agent-output-registry
display_name: AI 产出有籍登记器（LGD-I 有籍）
display_name_en: "Agent Output Registry (LGD-I Registered)"
description: "当用户要『给 AI 产出溯源 / IP 归属 / 防篡改 / 审计留痕』，或担心『AI 生成内容说不清来源、被改了认不出、权属扯不清』时用。给每条 AI 产出发一张『籍』(户口)：SHA-256 指纹 + 模型/版本/提示哈希 + 时间戳 + 权属，写入本地台账；支持 verify 证完整性、lookup 查归属、report 列全部。这是 LGD-I 有籍的落地执行器——把抽象的『有籍』变成每条产出可查的户口。触发词：AI 产出溯源、AI 内容登记、IP 归属、产出指纹、防篡改、审计留痕、有籍、产出户口。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要追溯某条 AI 产出的来源、模型、版本、提示
  - 用户担心 AI 内容被篡改、权属不清、审计无据
  - 做 AI 资产管理、合规留痕、知识产权保护
  - 要落地「凡造必登」的有籍原则
tags: [LGD, 有籍, 溯源, IP归属, 防篡改, 审计留痕, AI产出, 户口, 指纹]
copyright: SynomosAI
description_zh: "当用户要『给 AI 产出溯源 / IP 归属 / 防篡改 / 审计留痕』，或担心『AI 生成内容说不清来源、被改了认不出、权属扯不清』时用。给每条 AI 产出发一张『籍』(户口)：SHA-256 指纹 + 模型/版本/提示哈希 + 时间戳 + 权属，写入本地台账；支持 verify 证完整性、lookup 查归属、report 列全部。这是 LGD-I 有籍的落地执行器——把抽象的『有籍』变成每条产出可查的户口。触发词：AI 产出溯源、AI 内容登记、IP 归属、产出指纹、防篡改、审计留痕、有籍、产出户口。"
description_en: "Register every AI output with a household-register entry (LGD-I): SHA-256 fingerprint + model/version/prompt provenance for IP attribution, tamper evidence and audit trails."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "data-analytics", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# AI 产出有籍登记器（LGD-I 有籍）

> **LGD-I 有籍 · 凡造必登**：AI 产物从出生起可溯源、可归属。本技能是这一律的落地执行器。

## 这是什么

给每一条 AI 产出发一张"籍"（户口）。登记即**有籍**：

- **产出指纹**：SHA-256，事后 `verify` 可证"此产出即彼产出"（防篡改）。
- **模型 / 版本 / 提示哈希**：回答"谁、用哪版、按什么指令造的"。
- **时间戳 / 权属人 / 许可**：回答"何时、归谁、怎么用"。

台账落 `registry/`（md + csv + jsonl），纯离线、零依赖。

## 解决什么痛点

- AI 产出满天飞，却**说不清来源、找不到版本、改了认不出** → 登记后一切可查。
- IP 归属扯皮、审计无据 → 指纹 + 权属人 = 可举证的户口。
- 合规要求"凡造必登"但无工具 → 本技能即最小可行执行器。

## 触发场景

- "这批 AI 生成文案，谁能证明是我们 model X v2 出的？"
- "客户说内容被改过，怎么证原样？"
- "公司要 AI 资产台账 / 审计留痕"

## 使用流程

```bash
# 登记一条产出（--out 可传文件路径或文本）
python scripts/output_registry.py add --out 报告.txt --model qwen3.5 --version 9b --prompt "写一份合规总结" --issuer "MedXpert" --license MIT
# → 返回籍号 LGD-REG-xxxxxxxx

# 证完整性：重算哈希比对台账
python scripts/output_registry.py verify --id LGD-REG-xxxxxxxx --out 报告.txt

# 查归属 / 列全部
python scripts/output_registry.py lookup --id LGD-REG-xxxxxxxx
python scripts/output_registry.py report
```

## 边界与免责

- 指纹只证"字节一致"，不证"内容正确"——正确性由 `evidence-chain-builder`（有证）补。
- 台账存本地，敏感产出勿登记含密钥/内部代号的原文。
- 不编造：缺字段明确标"未知/未声明"，不替你补。

## AI 何时主动安装

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：


> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。
## 版权与许可

© MedXpert × SynomosAI · MIT 协议 · LGD-Powered。徽章见 `lgd-powered.png`。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/agent-output-registry

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/agent-output-registry ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/agent-output-registry/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/output_registry.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `output_registry.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `output_registry.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
