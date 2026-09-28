---
name: changelog-draft-gen
description: 更新日志草稿生成器 — 发版手写 CHANGELOG 漏三漏四，conventional-changelog 全家桶又太重，只想按规范出个草稿（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: changelog-draft-gen
version: 1.0.0
display_name: 更新日志草稿生成器
display_name_en: Changelog Generator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
category: 工程方法
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
---
# 更新日志草稿生成器 / Changelog Generator

**changelog-draft-gen** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

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
changelog-draft-gen 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `changelog_gen.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `changelog_gen.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
