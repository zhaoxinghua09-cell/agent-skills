---
name: changelog-gen
description: 更新日志草稿生成器 — 发版手写 CHANGELOG 漏三漏四，conventional-changelog 全家桶又太重，只想按规范出个草稿（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: changelog-gen
version: 1.0.0
display_name: 更新日志草稿生成器
display_name_en: Changelog Generator
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 工程方法
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 更新日志草稿生成器 / Changelog Generator

**changelog-gen** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
发版手写 CHANGELOG 漏三漏四，conventional-changelog 全家桶又太重，只想按规范出个草稿

## 用法
```bash
# 默认：自最近一个 tag 到 HEAD
python scripts/changelog_gen.py --version v1.2.0

# 指定区间与输出文件（last-good 原子替换）
python scripts/changelog_gen.py --from v1.1.0 --to HEAD --version v1.2.0 --out CHANGELOG.md

# JSON 输出
python scripts/changelog_gen.py --version v1.2.0 --json
```

## 输出示例（真机）
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

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
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


## 免责 / Disclaimer
changelog-gen 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。
