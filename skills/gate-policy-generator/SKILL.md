---
name: gate-policy-generator
description: 生成 LGD-III「有门禁」权限策略（policy-as-code），给 agent 划清可调用/需评审/禁止的工具边界与四道门禁，防越权、误删误发、失控循环。
description_zh: 生成 LGD-III 有门禁权限策略
description_en: Generate LGD-III gated permission policy
slug: gate-policy-generator
version: 1.0.0
display_name: 权限有门禁生成器
display_name_en: Gate Policy Generator
category: AI 治理
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
platforms: [windows, macos, linux]
agent_created: true
copyright: SynomosAI
classification:
  internal: ["主轴2 理论体系(LGD)"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# 权限有门禁生成器（Gate Policy Generator）

> **LGD 三律映射：LGD-III 有门禁（GATED）**
> 「凡自治之物：有籍 · 有证 · 有门禁」—— 本技能是 LGD-III「有门禁」的治理配置层执行器。

## 它解决什么痛点
- agent **越权**调用它不该碰的工具（删库、外发、改配置）
- **误删误发**：没有二次确认，一条指令就真发出去了
- **失控循环**：agent 自己转圈跑飞，烧光 token 还不停
- 团队**没有统一权限边界词汇**，各 agent 各说各话

## 它做什么
把一份 agent 能力清单（工具名 + 风险等级 + 是否敏感），落成一份**可挂载的权限门禁策略 JSON**：
- `tool_allow` / `tool_review` / `tool_deny` —— 三档工具边界
- `gates` —— **四道门禁**：触发门禁 / 评审门禁 / 放行门禁 / 复盘门禁（LGD-III 标准定义）
- `budget` —— `max_loop_iterations` + `max_tokens` 上限，防失控循环

三种内置档：`default`（平衡）/`paranoid`（严苛）/`open`（宽松）。

## 与兄弟技能的区别
- `tool-call-guard`（第三批）= 运行时**单次调用**闸门（执行器）
- 本技能 = **策略生成**层（治理配置），产出整套路权限边界

## 何时该用
- 你准备把一个 agent 接进生产环境，需要先划清它能 / 不能做什么
- 你被审计要求"证明 agent 有权限边界"
- 你担心某 agent 会越权 / 跑飞

## 适用场景
> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：


> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。
## LGD 三律背书
本技能是 **LGD 全程治理论**（由 SynomosAI 提出、MedXpert 在医疗器械全生命周期实证）的「有门禁」执行器之一。每个用本技能产出的策略，都是"凡自治之物须有门禁"这一治理思想的一个落地件。

## 触发词
`权限策略` / `门禁` / `越权` / `误删误发` / `失控循环` / `agent guardrails` / `permission policy` / `gate`

## 用法
```bash
# 直接看示例策略（无需 manifest）
python gate_policy.py --preset default --json

# 从能力清单生成
python gate_policy.py --manifest agent_manifest.json --out policy.json

# 反向校验一份 policy 是否满足 LGD-III 四道门禁
python gate_policy.py --check policy.json
```

## 输入 manifest 示例
```json
{
  "scenario": "通用客服 agent",
  "tools": [
    {"name": "read_file", "risk": "low"},
    {"name": "send_email", "risk": "mid"},
    {"name": "delete_file", "risk": "high", "sensitive": true},
    {"name": "sql_write", "risk": "high"}
  ]
}
```

## 红线
- 本技能只**生成策略配置**，不替代持证申报 / 合同 / 人工放行决策。
- 策略文件不含密钥、不含内部项目代号、不含雇主信息。
- 最终权限边界以你的 SOW / 合同（人工拍板）为准。

## 依赖
Python 3.8+ 标准库，零第三方依赖。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/gate-policy-generator

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/gate-policy-generator ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/gate-policy-generator/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/gate_policy.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `gate_policy.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `gate_policy.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
