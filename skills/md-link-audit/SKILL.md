---
name: md-link-audit
description: Markdown 链接体检器 — README 里链接一堆 404、改了路径没人发现，CI 上还老因为外网检查超时误报（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: md-link-audit
version: 1.0.0
display_name: Markdown 链接体检器
display_name_en: Markdown Link Auditor
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
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
