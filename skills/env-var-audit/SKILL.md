---
name: env-var-audit
description: 环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: env-var-audit
version: 1.0.0
display_name: 环境变量审计器
display_name_en: Environment Variable Auditor
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: 安全合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Audit environment-variable usage: find os.getenv calls missing from .env.example and hardcoded passwords in source code (zero-dependency, deterministic output, --json)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# 环境变量审计器 / Environment Variable Auditor

**env-var-audit** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码

## 用法
```bash
# 审计当前项目
python scripts/env_var_audit.py .

# JSON 输出
python scripts/env_var_audit.py . --json
```

## 输出示例（真机）
```
$ env_var_audit.py .
代码读取的环境变量：5 · .env.example 声明：4
  未文档化 MEDIUM：AWS_REGION（代码使用，example 未列）
  硬编码疑密 HIGH：DB_PASSWORD = "hunter2secret123" (app/db.py:12)
发现高危项，rc=1
```

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| EVA_E_NO_DIR | 目录不存在 | 传入正确的项目根目录 |
| EVA_E_NO_FILES | 未发现可扫描的源码文件 | 确认目录含 .py/.js/.ts/.sh 文件 |

## FAQ
**HIGH 是怎么判定的？**

两类：值匹配已知密钥前缀（ghp_/sk-/AKIA/xoxb 等），或疑似密钥字段名被赋以 12 位以上字面量且不是占位符。

**会误报吗？**

会有少量误报（如示例代码里的假密钥）。工具只做静态启发式并给出文件行号证据，处置由人决定。


## 免责 / Disclaimer
env-var-audit 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `env_var_audit.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `env_var_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
