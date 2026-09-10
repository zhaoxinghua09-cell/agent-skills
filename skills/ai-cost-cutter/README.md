# ai-cost-cutter · AI 省钱跑批

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Stop burning money on LLM API calls. Four knives to cut cost: **batching** (off-peak / async 50% off), **local-model fallback** (cheap tasks run locally, flagships only for hard work), **cache layer** (never pay twice for the same request), **model routing** (pick model by task difficulty). Ships a runnable `cost_estimator.py` that turns task volume + prices into a monthly bill and the savings gap across 3 downgrade tiers. Born from the GOSIM entry *cross-machine-offline-taskbox* (offline batch on low-spec machines).

**中文** — 大模型不是越用越贵，是「怎么用」决定账单。四把刀降本：批处理 / 本地模型回退 / 缓存层 / 模型路由分级。附可运行成本估算脚本，输入任务量+单价即输出月度账单与三档降本方案的差额。源自 GOSIM 参赛作 cross-machine-offline-taskbox 的离线跑批思路。

## Why it beats "just use a cheaper model"

| Naive fix | Problem | This skill |
|---|---|---|
| Switch everything to cheap model | Quality collapses on hard tasks | Route by difficulty, keep flagship where it pays |
| Manually cache | Forgotten, inconsistent | Cache policy as a step in the flow |
| "Run at night" | No structure | Offline batch orchestration pattern |

## What's inside

- `SKILL.md` — 3 leak points + 4 knives + routing table + 铁律
- `scripts/cost_estimator.py` — zero-dependency CLI: baseline vs A/B/C tiers

```bash
python scripts/cost_estimator.py --calls 50000 --avg-in 800 --avg-out 400 \
    --price-flagship 0.01 --price-mid 0.003 --batch-disc 0.5 --local-frac 0.6
```

## Benchmark

| Approach | It does | Gap this fills |
|---|---|---|
| Provider pricing calculator | Single-model cost | No routing / batch / local mix |
| "Use local LLM" guides | Install Ollama | No decision rule on what to offload |
| This skill | Full cost architecture | Routes + batches + caches + offloads |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Companion to `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
