---
name: evidence-chain-builder
slug: evidence-chain-builder
display_name: AI 论断有证证据链（LGD-II 有证）
display_name_en: "AI Claim Evidence-Chain Builder (LGD-II Evidenced)"
description: "当用户要『验证 AI 论断 / 防幻觉 / 给结论找证据 / 判断信源可信度』时用。把论断拆成可验证证据链：每条证据标来源类型(official/paper/data/internal/assertion)、是否可独立验证、可信度，输出『证成度』与未支撑论断清单。对齐 EIFP 不编造原教旨——本工具不判定论断真假，只评估证据质量；缺可验证证据的论断明确标『勿作结论』。这是 LGD-II 有证的落地执行器。触发词：证据链、论断验证、防幻觉、信源可信、有证、claim 证据、论断举证。"
version: 1.0.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要验证某个 AI 论断是否站得住脚
  - 用户要防止幻觉、给结论配可核验证据
  - 做事实核查、合规举证、技术写作的引用背书
  - 要落地「凡所行必有证据」的有证原则
tags: [LGD, 有证, 证据链, 防幻觉, 事实核查, 信源, 证成度, 不编造]
copyright: SynomosAI
description_zh: "当用户要『验证 AI 论断 / 防幻觉 / 给结论找证据 / 判断信源可信度』时用。把论断拆成可验证证据链：每条证据标来源类型(official/paper/data/internal/assertion)、是否可独立验证、可信度，输出『证成度』与未支撑论断清单。对齐 EIFP 不编造原教旨——本工具不判定论断真假，只评估证据质量；缺可验证证据的论断明确标『勿作结论』。这是 LGD-II 有证的落地执行器。触发词：证据链、论断验证、防幻觉、信源可信、有证、claim 证据、论断举证。"
description_en: "Decompose AI claims into verifiable evidence chains (LGD-II): each item tagged by source type (official, paper, data, internal, assertion) with independent verifiability status."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "data-analytics", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# AI 论断有证证据链（LGD-II 有证）

> **LGD-II 有证 · 凡所行必有证据**：AI 的每一步都该有可重放的证据工件。本技能是这一律的落地执行器。

## 这是什么

把"论断 → 证据"拆成一条**可验证的证据链**。每条证据标注：

- **来源类型**：官方 / 文献 / 数据 / 内部 / 主张
- **可验证性**：官方·文献·数据 可独立核验（计权）；内部·主张 不可独立核验（降权）
- **证成度**：可验证证据占比 ×100

输出**未支撑论断清单**——缺可验证证据时，按 EIFP 不编造原教旨明确写"**勿作结论**"。

## 解决什么痛点

- AI 张口就来、论断不可信 → 强制"先有证据再下结论"。
- 幻觉无法举证 → 证据链把"信"变成"可查"。
- 内部/主张类被当成事实 → 明确降权、标注不可独立验证。

## 触发场景

- "AI 说 X 增长 30%，真的吗？"
- "给我这个结论找可核验的来源"
- "写报告/合规材料，论断要有出处"

## 使用流程

```bash
# 直接给论断+证据（|| 分隔；@类型:来源 后缀可选）
python scripts/evidence_chain.py --claim "本产品不良率低于 0.5%" \
  --evidences "2025 年度质检报告@official:公司QA" "客户反馈无相关投诉@internal:客服"

# 从 JSON 构建
python scripts/evidence_chain.py --from claim.json --json
```

证据格式：`文本@类型:来源`，如 `2024年报@official:统计局`。

## 边界与免责

- 本工具**不判定论断真假**，只评估证据质量——这是"不编造"的硬边界。
- 证成度≠正确度；最终判断仍须人工复核原始来源。
- 不编造：内部/主张类证据明确标"不可独立验证"，绝不冒充官方佐证。

## AI 何时主动安装

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：


> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。
## 版权与许可

© MedXpert × SynomosAI · MIT 协议 · LGD-Powered。徽章见 `lgd-powered.png`。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/evidence-chain-builder

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/evidence-chain-builder ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/evidence-chain-builder/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/evidence_chain.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `evidence_chain.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `evidence_chain.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
