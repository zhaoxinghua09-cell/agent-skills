# UDI 格式校验器 / UDI Format Validator

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `udi-format-validator` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**给 UDI 串做一次确定的、可复现的体检，别等打回才知道格式错。**

**EN**: A deterministic health check for UDI strings - catch format errors before regulators do.

**关键词 / Keywords**: UDI校验 UDI-DI Basic-UDI-DI GS1检查位 NMPA UDI MDR 医疗器械唯一标识 注册资料

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/udi-format-validator/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/udi-format-validator/scripts/udi_format_validator.py -o ~/.claude/skills/udi-format-validator/scripts/udi_format_validator.py
python ~/.claude/skills/udi-format-validator/scripts/udi_format_validator.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；WorkBuddy 对话内直接装。

## Usage / 用法
```bash
# 带包装标识（推荐，GS1 扫码输出常见形态）
python scripts/udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A(21)SN0001"

# 仅校验 UDI-DI
python scripts/udi_format_validator.py --di 06901234567892

# JSON 中间表示（机器可读）
python scripts/udi_format_validator.py "(01)06901234567892" --json
```

## Sample output / 真机输出
```
$ udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A"
UDI 校验：通过
  DI        06901234567892   校验位 ✓（GS1 Mod10）
  失效日期  2026-09-30       格式 ✓
  批号      LOT2026A         生产标识 ✓
提示：三类械 UDI 已全面实施（2022-06），二类自 2024-06-01 起；EU 需另配 Basic UDI-DI，以官方最新要求为准。
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
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


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/udi-format-validator
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
udi-format-validator 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © udi-format-validator authors. LGD-Powered badge: [定版真源](https://medxpert.cn/badge/powered/svg/lgd-powered-en.svg?v=84)
