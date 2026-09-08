---
name: udi-format-validator
description: UDI 格式校验器 — 拿到一串 UDI 不知道 DI 有没有错、生产标识全不全、 Basic UDI-DI 怎么区分，注册资料被打回才知道格式错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: udi-format-validator
version: 1.0.0
display_name: UDI 格式校验器
display_name_en: UDI Format Validator
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 医疗器械合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
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
