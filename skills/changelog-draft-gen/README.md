# 更新日志草稿生成器 / Changelog Generator

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `changelog-gen` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**conventional commits 进，符合规范的 CHANGELOG 草稿出，零依赖一条命令。**

**EN**: Turn conventional commits into a Keep a Changelog draft. Zero-dependency CLI.

**关键词 / Keywords**: changelog conventional-commits 发版 CHANGELOG git log release notes 版本发布

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/changelog-gen/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/changelog-gen/scripts/changelog_gen.py -o ~/.claude/skills/changelog-gen/scripts/changelog_gen.py
python ~/.claude/skills/changelog-gen/scripts/changelog_gen.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；WorkBuddy 对话内直接装。

## Usage / 用法
```bash
# 默认：自最近一个 tag 到 HEAD
python scripts/changelog_gen.py --version v1.2.0

# 指定区间与输出文件（last-good 原子替换）
python scripts/changelog_gen.py --from v1.1.0 --to HEAD --version v1.2.0 --out CHANGELOG.md

# JSON 输出
python scripts/changelog_gen.py --version v1.2.0 --json
```

## Sample output / 真机输出
```
$ changelog_gen.py --version v1.2.0
## v1.2.0 - 2026-09-08

### ⚠ Breaking / 破坏性变更
- `a1b2c3d` refactor(cli)!: rename --dry-run to --preview

### Added / 新增
- `e4f5a6b` feat: add --json output for machine readers

### Fixed / 修复
- `b7c8d9e` fix: correct check-digit weighting order

（草稿由 conventional commits 归类生成，发布前请人工润色）
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| CHG_E_NO_GIT | 目录不是 git 仓库 | 在仓库根目录运行或用 --repo 指定路径 |
| CHG_E_NO_COMMITS | 区间内没有提交 | 检查 --from/--to 区间或 tag 是否存在 |
| CHG_E_GIT_FAIL | git 命令执行失败 | 确认 git 可用且仓库可读 |

## FAQ
**支持中文提交信息吗？**

支持。分类只看 conventional 前缀（feat/fix/...），描述语言不限。

**会直接覆盖我的 CHANGELOG.md 吗？**

仅当显式传 --out 时写入，且走临时文件+原子替换；校验失败不会覆盖旧文件。


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/changelog-gen
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
changelog-gen 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © changelog-gen authors. LGD-Powered badge: [定版真源](https://medxpert.cn/badge/powered/svg/lgd-powered-en.svg?v=84)
