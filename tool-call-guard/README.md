# tool-call-guard · 工具调用安全闸门

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat every agent tool call as an *authorized action*. Grade by side-effect: read = allow, write = confirm, delete / send / pay = block. Ships a zero-dependency `tool_guard.py` that classifies a call and emits allow/block + reason.

**中文** — 把 agent 每次工具调用当需授权操作：按副作用分级，读放行、写确认、删/外发/支付拦截。附零依赖 `tool_guard.py` 给出级别与决策。

## Why it beats "give the agent all the tools"

| Pain | This skill |
|---|---|
| Agent silently `rm -rf` | L4 delete → blocked by default |
| Draft email auto-sent | L3 send → needs human confirm |
| One key to rule them all | Per-tool risk level, least privilege |
| "Who ran that?" | Every call audited (有证) |

## What's inside

- `SKILL.md` — 5-level risk model + 3-step gate flow + 铁律
- `scripts/tool_guard.py` — zero-dependency CLI: classify a tool call (name+args), emit level + allow/block + reason

```bash
python scripts/tool_guard.py --tool delete_file --args '{"path":"/data"}'
python scripts/tool_guard.py --tool send_email --args '{"to":"x","body":"y"}' --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| MCP auth scopes | Runtime decision per call, not just static scope |
| "Just don't give delete tool" | Grained L0–L4, not binary |
| Manual review after | Pre-execution gate, not post-mortem |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `prompt-injection-shield` and `agent-redteam-kit`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
