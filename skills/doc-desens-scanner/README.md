# doc-desens-scanner · 文档智能去敏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Scan a doc/code/log before it leaves the building: PII · secrets · internal paths · internal codenames, mask them and emit a `desens_report.json` (evidenced: what was redacted, when). Runnable `desens_scan.py`. Theoretical root: LGD — evidenced (desensitization is logged, accountable).

**中文** — 对外发布前扫描 PII·密钥·内部路径·内部项目代号，打码并输出脱敏清单（有证：脱敏动作可审计）。附可运行脚本。理论根基：LGD 有证。

## Why it beats "eyeball it"

| Pain | This skill |
|---|---|
| Secrets slip into public repos | Pattern lib catches `sk-` 前缀令牌 / `ghp_` / `password` 赋值 |
| Internal paths leak identity | Windows 用户目录 / home 目录 flagged |
| No record of what was redacted | `desens_report.json` (有证) |

## What's inside

- `SKILL.md` — 4 sensitive classes + 3-step flow + 铁律
- `scripts/desens_scan.py` — zero-dependency CLI: scan & mask, emit report

```bash
python scripts/desens_scan.py --file draft.md --mask ***
python scripts/desens_scan.py --text "密钥 sk-DEMO 示例路径 用户主目录" --report
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| GitLeaks | Secrets only | Misses PII / paths / codenames |
| Manual review | Slow | Not repeatable, no report |
| "Trust me" | — | No evidence trail |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `release-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
