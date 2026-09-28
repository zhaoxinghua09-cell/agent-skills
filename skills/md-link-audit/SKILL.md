---
name: md-link-audit
description: Markdown 链接体检器 — README 里链接一堆 404、改了路径没人发现，CI 上还老因为外网检查超时误报（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: md-link-audit
version: 1.0.0
display_name: Markdown 链接体检器
display_name_en: Markdown Link Auditor
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "Markdown 链接体检器 — README 里链接一堆 404、改了路径没人发现，CI 上还老因为外网检查超时误报（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Audit Markdown links for 404s and path drift, with CI-friendly external-link timeout handling (zero-dependency, deterministic output, --json)."
classification:
  internal: ["通用工具(跨主轴·待归类)"]
  skillhub: ["productivity"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# Markdown 链接体检器 / Markdown Link Auditor

**md-link-audit** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
README 里链接一堆 404、改了路径没人发现，CI 上还老因为外网检查超时误报

## 用法
```bash
# 默认离线：只查内部相对链接与本地锚点（CI 友好，零外呼）
python scripts/md_link_audit.py docs/

# 联网校验外部链接（8s 超时 + 一次重试）
python scripts/md_link_audit.py . --net

# JSON 输出
python scripts/md_link_audit.py . --json
```

## 输出示例（真机）
```
$ md_link_audit.py docs/
扫描 12 个 Markdown 文件 · 链接 47 条
  内部断链 2：
    getting-started.md -> ../imgs/arch.png   （文件不存在）
    README.md -> #install                    （无对应标题）
  外部链接 31 条（--net 未开启，未校验）
发现断链，rc=1
```

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| MLK_E_NO_DIR | 目录不存在 | 传入正确的文档目录 |
| MLK_E_NO_MD | 目录内没有 Markdown 文件 | 确认目录或改用 --ext 扩展名 |

## FAQ
**为什么不默认联网？**

外呼会拖慢 CI 且被限流误伤；默认只做确定性的本地判定，外链校验交给 --net 显式开启。

**锚点判定规则是什么？**

按 GitHub 口径：转小写、去标点、空格转连字符；中文标题同样适用。


## 免责 / Disclaimer
md-link-audit 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `md_link_audit.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `md_link_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
