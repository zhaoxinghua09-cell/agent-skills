---
name: health-claim-guard
description: 健康宣称合规扫描 — 保健品/食品宣传文案扫违规疗效宣称（根治/治愈/无副作用等），缺警示语即 FAIL（零依赖）
slug: health-claim-guard
version: 1.0.0
display_name: 健康宣称合规扫描
display_name_en: Health Claim Guard
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "健康宣称合规扫描 — 保健品/食品宣传文案扫违规疗效宣称（根治/治愈/无副作用等），缺警示语即 FAIL（零依赖）"
description_en: "Scan health-product marketing copy for illegal therapeutic claims (cure, heal, no side effects) and missing warning labels; violations FAIL (zero-dependency)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# 健康宣称合规扫描 / Health Claim Guard

**health-claim-guard** v1.0.0 · LGD 护城河家族 · 零依赖
域：医疗健康 · 三律映射：TH-LGD-023

## 痛点
带货文案随手写根治、有效率99%，广告法罚款动辄数十万

## 用法
```bash
python scripts/health_claim_guard.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 医疗健康 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/health-claim-guard

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/health-claim-guard ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/health-claim-guard/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/health_claim_guard.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `health_claim_guard.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `health_claim_guard.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
