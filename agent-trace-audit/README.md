# agent-trace-audit · 智能体行为留痕审计

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — When an agent breaks, you must trace what it did. Build a ledger of ts · actor · action · target · gate, flag ungated (out-of-bounds) writes, emit timeline + violation list. Runnable `trace_audit.py`. Theoretical root: LGD — registered (fully traceable). Pairs with `agent-redteam-kit`.

**中文** — 把 agent 动作建成「时间戳·执行者·动作·对象·是否过闸」账本，标出越界操作，输出时间线+违规清单。附可运行脚本。理论根基：LGD 有籍。

## Why it beats "no log"

| Pain | This skill |
|---|---|
| Can't tell what agent did | Per-action ledger |
| Out-of-bounds write unseen | gate=ungated flagged red |
| Compliance can't prove control | Timestamped, read-only archive |

## What's inside

- `SKILL.md` — 5-field ledger + 3-step flow + 铁律
- `scripts/trace_audit.py` — zero-dependency CLI: build ledger from JSONL log

```bash
python scripts/trace_audit.py --log actions.jsonl
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| LangSmith/trace UI | Visual trace | No gate-violation flag, vendor lock |
| Print debugging | Ephemeral | Not archived, not auditable |
| "I think it did X" | — | No evidence |

Theoretical root: **LGD Three Laws** — registered. Pairs with `agent-redteam-kit`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
