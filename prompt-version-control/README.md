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

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
