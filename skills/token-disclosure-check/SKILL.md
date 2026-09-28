---
name: token-disclosure-check
description: 代币信息披露检查器 — 白皮书/披露文案核查必备要素（总量/分配/锁仓/团队/风险提示），含收益承诺即 FAIL（零依赖）
slug: token-disclosure-check
version: 1.0.0
display_name: 代币信息披露检查器
display_name_en: Token Disclosure Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "代币信息披露检查器 — 白皮书/披露文案核查必备要素（总量/分配/锁仓/团队/风险提示），含收益承诺即 FAIL（零依赖）"
description_en: "Check token whitepapers and disclosure copy for required elements: total supply, allocation, lockup, team and risk warnings; return promises FAIL (zero-dependency)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# 代币信息披露检查器 / Token Disclosure Check

**token-disclosure-check** v1.0.0 · LGD 护城河家族 · 零依赖
域：区块链 · 三律映射：TH-LGD-020

## 痛点
项目方披露缺斤少两还暗带保证收益话术，接不住监管也坑持有人

## 用法
```bash
python scripts/token_disclosure_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

## 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

## LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在 区块链 场景的落地件：让 AI 的每一次输出**有籍可查、有证可依、有门禁可控**。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/token-disclosure-check

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/token-disclosure-check ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/token-disclosure-check/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/token_disclosure_check.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `token_disclosure_check.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `token_disclosure_check.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
