# prompt-version-control · 提示版本管理

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Prompts are *versionable assets*. Every edit keeps version + diff + bound eval score, so you can diff, roll back, and pick the best — no more copy-paste management. Ships a zero-dependency `prompt_vc.py`.

**中文** — 把提示当可版本化资产：每版留版本+差异+效果分，可 diff/回滚/选优。零依赖 `prompt_vc.py`。

## Why it beats "edit in place"

| Pain | This skill |
|---|---|
| Broke prompt, can't revert | Versioned, one-key rollback |
| "Which change helped?" | Per-version diff recorded |
| Score not tied to prompt | Version ↔ eval score bound |
| Two people overwrite each other | Sequential commit, no clobber |

## What's inside

- `SKILL.md` — version+diff+score 3-piece + 3-step flow + 铁律
- `scripts/prompt_vc.py` — zero-dependency CLI: diff two prompt files, append a version record (JSON)

```bash
python scripts/prompt_vc.py --old v1.txt --new v2.txt --score 0.82
python scripts/prompt_vc.py --old v1.txt --new v2.txt --score 0.82 --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Copy-paste backups | Structured version+score, not loose files |
| Notebook experiments | Diff + rollback, repeatable |
| "Just remember v2 was better" | Bound eval score, not memory |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `context-engineering` and `skill-quality-gate`.

---

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237) · 代码 MIT · 理论文本保留所有权利

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

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
