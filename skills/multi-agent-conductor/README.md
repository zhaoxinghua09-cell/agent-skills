# multi-agent-conductor · 多智能体编排

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Multi-agent projects fail on blurred boundaries, not model power. Decompose a task → assign roles → pin each agent's *allowed / forbidden* boundary (gated). Runnable `conductor_plan.py` emits a role table + boundary list. Theoretical root: LGD — gated (task boundary + permission isolation).

**中文** — 把大任务拆成角色、给每个 agent 定死「能做什么、禁止碰什么」，避免串权限/重复劳动。附可运行脚本（编排规划器）。理论根基：LGD 有门禁。

## Why it beats "spawn N agents and pray"

| Pain | This skill |
|---|---|
| Agents overwrite each other | Per-agent forbidden boundary |
| Duplicate work | Decomposition with dependency map |
| Contradictory outputs | Single conductor sums & checks |

## What's inside

- `SKILL.md` — 3 elements + 3-step flow + 铁律
- `scripts/conductor_plan.py` — zero-dependency CLI: role table + boundaries

```bash
python scripts/conductor_plan.py --task "写一份市场分析报告" --agents 3
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| AutoGen/CrewAI | Run agents | No explicit forbidden-boundary gate |
| "Just prompt team" | Ad hoc | Roles blur, conflicts |
| Single big agent | One context | Hits window/quality wall |

Theoretical root: **LGD Three Laws** — gated. Pairs with `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
