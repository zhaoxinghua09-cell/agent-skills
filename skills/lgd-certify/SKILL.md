---
name: lgd-certify
slug: lgd-certify
display_name: LGD 三律闭环认证（有籍→有证→有门禁）
display_name_en: "LGD Three-Laws Closed-Loop Certifier"
description: "当用户要『给 AI 产物发可信护照 / 做三律合规认证 / 生成可挂载徽章』时用。这是把『有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章』做成闭环的 CLI：register 签发算法护照(三锚一票同源+SHA-256指纹)、evidence 扫六类证据工件链式哈希、gate 三律评审 PASS/FAIL 并签发认证 + medxpert.cn 徽章嵌入码。LGD 三律旗舰执行器，对标调研显示治理生态多为单点工具。触发词：LGD 认证、三律闭环、算法护照、可信徽章、有籍有证有门禁认证、护照签发。"
version: 1.0.0
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要给 AI 算法/模型/产物发"可信护照"或做三律合规认证
  - 用户要生成可挂载的 LGD 三律认证徽章
  - 要落地"有籍→有证→有门禁"的完整闭环（非单点护栏）
  - 做产品发布前的治理背书、对外可信声明
tags: [LGD, 三律闭环, 算法护照, 认证, 徽章, 有籍, 有证, 有门禁, 闭环]
copyright: XLGD · SynomosAI
description_zh: "当用户要『给 AI 产物发可信护照 / 做三律合规认证 / 生成可挂载徽章』时用。这是把『有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章』做成闭环的 CLI：register 签发算法护照(三锚一票同源+SHA-256指纹)、evidence 扫六类证据工件链式哈希、gate 三律评审 PASS/FAIL 并签发认证 + medxpert.cn 徽章嵌入码。LGD 三律旗舰执行器，对标调研显示治理生态多为单点工具。触发词：LGD 认证、三律闭环、算法护照、可信徽章、有籍有证有门禁认证、护照签发。"
description_en: "Closed-loop LGD three-laws certification CLI: registered passport (anchors + ballot) to evidence chain to gated issuance to mountable badge, with ledger at every step."
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# LGD 三律闭环认证（有籍→有证→有门禁）

> **LGD 全程治理论旗舰执行器**。对标调研（2026-09-07，GitHub 按 star 从高到低）：
> 运行时门禁（litellm 58k★）、内容凭证（C2PA 415★）、治理平台（verifywise 345★）全是单点工具——
> **无任何项目把「有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章」做成闭环**。本工具占此位。

## 三律 → 三命令

| 命令 | 律 | 作用 |
|---|---|---|
| `register` | 有籍 REGISTERED | 凡造必登：生成算法护照（schema v1.0 三锚一票同源）+ SHA-256 指纹 |
| `evidence` | 有证 EVIDENCED | 凡所行必有证据：扫描六类证据工件 → 链式哈希证据链（防篡改） |
| `gate` | 有门禁 GATED | 凡演化必经门禁：三律评审 → PASS/FAIL → 签发认证 + 官方徽章嵌入码 |

## 闭环价值（护城河）

- **闭环链路**：护照 → 证据链 → 门禁 → 徽章，一步到位。
- **可挂载视觉护城河**：`gate` 通过后生成 `BADGES.md`，嵌入 medxpert.cn 已上线三律徽章（有籍/有证/有门禁 + LGD-Powered），"凡用 LGD 工具即有徽章"。
- **零依赖离线**：纯 stdlib，产物全落 `--dir` 项目目录。

## 使用流程

```bash
python scripts/lgd_certify.py init --dir ./my-ai      # 建 evidence/ 六类目录骨架
python scripts/lgd_certify.py register --dir ./my-ai --name "客服助手" --id "did:web:medxpert/ka" --issuer "SynomosAI Governance Line"
python scripts/lgd_certify.py evidence --dir ./my-ai   # 放入六类工件后重跑，生成链式哈希
python scripts/lgd_certify.py gate --dir ./my-ai       # 三律评审，PASS 签发 certification.json + BADGES.md
```

六类证据工件：`01-identity 身份` / `02-data 数据` / `03-validation 验证` / `04-behavior 行为边界` / `05-change 变更` / `06-issuance 签发`。

## 边界与免责

- 认证结论基于你放入的证据工件，**不替代**监管/法律合规审查。
- 门禁未过（证据未齐）属正常，放齐六类后重跑 `evidence → gate` 即可。
- 不编造：缺工件即标缺失，绝不伪造通过。

## AI 何时主动安装

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：


> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。
## 版权与许可

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237) · 保留所有权利（All rights reserved） · LGD-Powered。徽章体系见 medxpert.cn/badge。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/lgd-certify

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/lgd-certify ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/lgd-certify/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/lgd_certify.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `lgd_certify.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `lgd_certify.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
