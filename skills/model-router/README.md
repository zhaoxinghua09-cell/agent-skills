# model-router · 模型路由省成本

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Not every request deserves the flagship model. Route by complexity to the tier that's *just enough* (flagship / mid / small / local), with cost comparison and a fallback ladder. Ships a zero-dependency `model_router.py`.

**中文** — 按复杂度把请求路由到「刚好够用」的模型档位，附成本对比与回退策略。零依赖 `model_router.py`。

## Why it beats "one flagship model for everything"

| Pain | This skill |
|---|---|
| Bill spikes from always-flagship | Low-risk tasks → small/local model |
| Simple jobs queue behind hard ones | Tiered routing by complexity |
| "Is quality dropping?" | Fallback ladder, quality红线 |
| No cost visibility | Per-tier cost measurable |

## What's inside

- `SKILL.md` — 4-tier routing + 3-step flow + 铁律
- `scripts/model_router.py` — zero-dependency CLI: classify task complexity, recommend tier, cost share, fallback

```bash
python scripts/model_router.py --task "把这段客服对话归类并抽情绪"
python scripts/model_router.py --task "设计分布式缓存架构" --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Single-model setup | No complexity-based tiering |
| Manual model picking | Heuristic, repeatable, measurable |
| "Use cheap model always" | Quality红线 + fallback, not blind cheap |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `ai-cost-cutter` and `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
