---
name: udi-format-validator
description: UDI 格式校验器 — 拿到一串 UDI 不知道 DI 有没有错、生产标识全不全、 Basic UDI-DI 怎么区分，注册资料被打回才知道格式错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: udi-format-validator
version: 1.0.0
display_name: UDI 格式校验器
display_name_en: UDI Format Validator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: 医疗器械合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "UDI 格式校验器 — 拿到一串 UDI 不知道 DI 有没有错、生产标识全不全、 Basic UDI-DI 怎么区分，注册资料被打回才知道格式错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Validate UDI strings: DI correctness, production-identifier completeness and Basic UDI-DI distinction (zero-dependency, deterministic output, --json)."
classification:
  internal: ["主轴1 医械合规咨询"]
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# UDI 格式校验器 / UDI Format Validator

**udi-format-validator** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
拿到一串 UDI 不知道 DI 有没有错、生产标识全不全、 Basic UDI-DI 怎么区分，注册资料被打回才知道格式错了

## 用法
```bash
# 带包装标识（推荐，GS1 扫码输出常见形态）
python scripts/udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A(21)SN0001"

# 仅校验 UDI-DI
python scripts/udi_format_validator.py --di 06901234567892

# JSON 中间表示（机器可读）
python scripts/udi_format_validator.py "(01)06901234567892" --json
```

## 输出示例（真机）
```
$ udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A"
UDI 校验：通过
  DI        06901234567892   校验位 ✓（GS1 Mod10）
  失效日期  2026-09-30       格式 ✓
  批号      LOT2026A         生产标识 ✓
提示：三类械 UDI 已全面实施（2022-06），二类自 2024-06-01 起；EU 需另配 Basic UDI-DI，以官方最新要求为准。
```

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| UDI_E_LEN | DI 长度不等于 14 位 | 核对 GS1 编码结构，DI 固定 14 位 |
| UDI_E_CHECKDIGIT | GS1 Mod10 校验位不符 | 按 13 位数据位重算校验位，或核对录入笔误 |
| UDI_E_DATE | 日期段非法（月/日越界） | AI(11)/(17) 为 YYMMDD，日位 00 表示月末需注明 |
| UDI_E_UNKNOWN_AI | 出现不受支持的应用标识符 | 仅支持 01/10/11/17/21/240/30，其余请人工核对 |
| UDI_E_AMBIGUOUS | 无括号串中变长段无法定界 | 请使用带括号形态或含 FNC1 的扫码输出 |

## FAQ
**UDI-DI 和 Basic UDI-DI 有什么区别？**

UDI-DI 标识具体型号包装，Basic UDI-DI 是同族产品的注册单元级标识（EU MDR 要求，NMPA 亦有对应口径），本工具按 --type 分开校验结构。

**校验位通过了就等于编码合规吗？**

不等于。本工具做格式与结构判定；编码归属、企业前缀、发码机构资质仍需向发码机构与官方数据库核验。


## 免责 / Disclaimer
udi-format-validator 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `udi_format_validator.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `udi_format_validator.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
