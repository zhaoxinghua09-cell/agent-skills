---
name: env-var-audit
description: 环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: env-var-audit
version: 1.0.0
display_name: 环境变量审计器
display_name_en: Environment Variable Auditor
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 安全合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
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
