# Markdown 链接体检器 / Markdown Link Auditor

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `md-link-audit` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**README 断链在 CI 里就地现形——默认离线、快而确定。**

**EN**: Find broken links in your Markdown before your readers do. Offline-first.

**关键词 / Keywords**: markdown链接检查 断链 404 README CI docs 锚点 链接审计

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/md-link-audit/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/md-link-audit/scripts/md_link_audit.py -o ~/.claude/skills/md-link-audit/scripts/md_link_audit.py
python ~/.claude/skills/md-link-audit/scripts/md_link_audit.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；WorkBuddy 对话内直接装。

## Usage / 用法
```bash
# 默认离线：只查内部相对链接与本地锚点（CI 友好，零外呼）
python scripts/md_link_audit.py docs/

# 联网校验外部链接（8s 超时 + 一次重试）
python scripts/md_link_audit.py . --net

# JSON 输出
python scripts/md_link_audit.py . --json
```

## Sample output / 真机输出
```
$ md_link_audit.py docs/
扫描 12 个 Markdown 文件 · 链接 47 条
  内部断链 2：
    getting-started.md -> ../imgs/arch.png   （文件不存在）
    README.md -> #install                    （无对应标题）
  外部链接 31 条（--net 未开启，未校验）
发现断链，rc=1
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| MLK_E_NO_DIR | 目录不存在 | 传入正确的文档目录 |
| MLK_E_NO_MD | 目录内没有 Markdown 文件 | 确认目录或改用 --ext 扩展名 |

## FAQ
**为什么不默认联网？**

外呼会拖慢 CI 且被限流误伤；默认只做确定性的本地判定，外链校验交给 --net 显式开启。

**锚点判定规则是什么？**

按 GitHub 口径：转小写、去标点、空格转连字符；中文标题同样适用。


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/md-link-audit
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
md-link-audit 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © md-link-audit authors. LGD-Powered badge: [定版真源](https://medxpert.cn/badge/powered/svg/lgd-powered-en.svg?v=84)
