# agent-loop-guard · 失控循环护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — An agent run is a *controlled process*. Monitor step cap · repeated actions · no-progress, and trip a circuit breaker before it burns tokens spinning in place. Ships a zero-dependency `loop_guard.py`.

**中文** — 把 agent 运行当受控进程：监控步数上限·重复动作·状态无进展，触发即熔断并出诊断。零依赖 `loop_guard.py`。

## Why it beats "hope it terminates"

| Pain | This skill |
|---|---|
| Infinite A↔B loop | Repeated (tool,args) → trip |
| Re-clicking same tool | k identical calls → break |
| Token bill explodes | Step cap hard-stops |
| "Why did it loop?" | Trajectory + diagnosis saved |

## What's inside

- `SKILL.md` — 3-signal breaker + 3-step flow + 铁律
- `scripts/loop_guard.py` — zero-dependency CLI: read action trace, rate loop risk, suggest break + diagnosis

```bash
python scripts/loop_guard.py --trace trace.txt --max-steps 30 --repeat 3
python scripts/loop_guard.py --trace trace.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Manual timeout | Detects *repetition*, not just wall-clock |
| "Just set a timeout" | No per-step loop diagnosis |
| Post-hoc log scan | Real-time gate, stop before burn |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `skill-quality-gate` and `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
