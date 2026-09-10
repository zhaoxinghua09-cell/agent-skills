# api-resilience · API 韧性

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — External APIs are *things that fail*. Wrap calls with exponential backoff + jitter, rate-limit counting, circuit breaker, and fallback — so one blip recovers instead of cascading. Ships a zero-dependency `resilience_demo.py`.

**中文** — 把外部调用当会失败的对象：指数退避+抖动重试、限流、熔断、降级，失败可恢复不雪崩。零依赖 `resilience_demo.py`。

## Why it beats "call it and pray"

| Pain | This skill |
|---|---|
| One 500 kills the chain | Backoff-retry, survives blips |
| 429 → retry storm | Rate-limit + jitter, no storm |
| Dep down, resources drained | Circuit breaker trips |
| No fallback, hard error | Degraded path returns兜底 |

## What's inside

- `SKILL.md` — 4-mechanism resilience + 3-step flow + 铁律
- `scripts/resilience_demo.py` — zero-dependency demo: backoff+jitter retry + circuit breaker with simulated failure/recover

```bash
python scripts/resilience_demo.py --fail-rate 0.6 --max-retry 5
python scripts/resilience_demo.py --fail-rate 0.9 --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Bare requests | No retry/breaker/fallback |
| Manual try/except | Ad-hoc, not standard pattern |
| "Retry immediately" | Backoff+jitter, no storm |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `agent-loop-guard` and `skill-quality-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
