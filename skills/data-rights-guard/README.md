# data-rights-guard · 训练数据版权护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Every training datum is an *asset with ownership*. Check license · commercial right · attribution · traceable source; entries without permission don't enter the training set. Ships a zero-dependency `rights_guard.py`.

**中文** — 把每条数据当带权属的资产：查许可证·商用权·署名·来源，缺许可的不进训练集。零依赖 `rights_guard.py`。

## Why it beats "scrape and train"

| Pain | This skill |
|---|---|
| Scraped data, no license | No-license → excluded |
| Non-Commercial used commercially | NC flag → blocked from commercial |
| Attribution required, not given | Flagged,补全 before use |
| "Where did this come from?" | Source traced or quarantined |

## What's inside

- `SKILL.md` — 4-signal ownership model + 3-step gate + 铁律
- `scripts/rights_guard.py` — zero-dependency CLI: scan a manifest.json (license/source/commercial/attribution), rate trainable + advice

```bash
python scripts/rights_guard.py --manifest manifest.json
python scripts/rights_guard.py --manifest manifest.json --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| "Just use the dataset" | Per-entry license/commercial gate |
| Manual license reading | Repeatable lexical check |
| Post-infringement cleanup | Pre-training exclusion, not after |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `doc-desens-scanner` and `ai-policy-radar`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
