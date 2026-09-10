# bias-auditor · 偏见审计

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Model output is a *viewpoint-bearing artifact*. Scan group terms · stereotypic phrasing · one-sided attribution, flag potential bias and suggest de-biased rewrites before publication. Ships a zero-dependency `bias_audit.py`.

**中文** — 把输出当带视角生产物：扫群体词·刻板表述·单边归因，标潜在偏见并给去偏改写。零依赖 `bias_audit.py`。

## Why it beats "it's just text"

| Pain | This skill |
|---|---|
| "Women aren't good at…" slips out | Group-generalization flag |
| Ability tied to gender/age/region | Stereotype-attribution flag |
| One-sided narrative | Missing-perspective hint |
| Silent bias ships | Pre-pub fairness gate |

## What's inside

- `SKILL.md` — 3-signal bias model + 3-step flow + 铁律
- `scripts/bias_audit.py` — zero-dependency CLI: scan text, flag bias signals + de-bias suggestion

```bash
python scripts/bias_audit.py --text "男生更适合做技术，女生适合沟通。"
python scripts/bias_audit.py --file article.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Sentiment only | No group/stereotype dimension |
| Manual review | Repeatable lexical audit |
| "Model is neutral" | Explicit flag + rewrite, not assumption |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `fact-check-guard` and `skill-quality-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
