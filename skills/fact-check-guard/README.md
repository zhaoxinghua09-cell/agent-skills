# fact-check-guard · 事实核查护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat every factual claim as a *claim to be proven*. Match each against retrieved sources and label supported / dubious / unsourced; unsourced claims are not allowed out as fact. Ships a zero-dependency `fact_guard.py`.

**中文** — 把每条关键声明当待证主张，对照来源逐条标 已支撑/存疑/无来源，无来源不许当事实对外。零依赖 `fact_guard.py`。

## Why it beats "it sounds right, ship it"

| Pain | This skill |
|---|---|
| Fabricated citations | Unsourced claim → blocked as fact |
| Stale "facts" | Source match required, else dubious |
| "Studies show…" with no study | No source → downgrade wording |
| One wrong sentence in good text | Per-claim labeling, not whole-doc |

## What's inside

- `SKILL.md` — 3-state claim labeling + 3-step flow + 铁律
- `scripts/fact_guard.py` — zero-dependency CLI: given claims + sources, label each supported/dubious/unsourced

```bash
python scripts/fact_guard.py --claims claims.txt --sources refs.txt
python scripts/fact_guard.py --claims claims.txt --sources refs.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| RAG only | RAG retrieves; this gates *publication* on support |
| Manual proofread | Per-claim automated, repeatable |
| "Trust the model" | Explicit unsourced-block rule |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `rag-grounding-guard` and `doc-desens-scanner`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
