# 环境变量审计器 / Environment Variable Auditor

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `env-var-audit` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**克隆即跑不起来？密钥进了源码？一条命令把环境变量账目对清。**

**EN**: Audit env vars: undocumented keys, unused examples, hardcoded secrets.

**关键词 / Keywords**: 环境变量 .env.example 硬编码密钥 secret scanning env audit 配置审计 泄漏防护

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/env-var-audit/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/env-var-audit/scripts/env_var_audit.py -o ~/.claude/skills/env-var-audit/scripts/env_var_audit.py
python ~/.claude/skills/env-var-audit/scripts/env_var_audit.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；WorkBuddy 对话内直接装。

## Usage / 用法
```bash
# 审计当前项目
python scripts/env_var_audit.py .

# JSON 输出
python scripts/env_var_audit.py . --json
```

## Sample output / 真机输出
```
$ env_var_audit.py .
代码读取的环境变量：5 · .env.example 声明：4
  未文档化 MEDIUM：AWS_REGION（代码使用，example 未列）
  硬编码疑密 HIGH：DB_PASSWORD = "hunter2secret123" (app/db.py:12)
发现高危项，rc=1
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| EVA_E_NO_DIR | 目录不存在 | 传入正确的项目根目录 |
| EVA_E_NO_FILES | 未发现可扫描的源码文件 | 确认目录含 .py/.js/.ts/.sh 文件 |

## FAQ
**HIGH 是怎么判定的？**

两类：值匹配已知密钥前缀（ghp_/sk-/AKIA/xoxb 等），或疑似密钥字段名被赋以 12 位以上字面量且不是占位符。

**会误报吗？**

会有少量误报（如示例代码里的假密钥）。工具只做静态启发式并给出文件行号证据，处置由人决定。


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/env-var-audit
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
env-var-audit 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © env-var-audit authors. LGD-Powered badge: [定版真源](https://medxpert.cn/badge/powered/svg/lgd-powered-en.svg?v=84)
