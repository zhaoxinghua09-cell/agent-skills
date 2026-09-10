# agent-memory-keeper · 跨会话长期记忆治理

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat agent long-term memory as an asset that is *sourced, auditable, and convergent*. Audit duplicate · orphan · stale · unsourced; ship a 2-step flow (converge to single source of truth → gate changes behind backup) plus a runnable `memory_audit.py` (memory auditor over a dir or JSONL). Memory isn't "can store" — it's "has provenance, no dup, reversible".

**中文** — 把 agent 长期记忆当成「有籍贯、可审计、能收敛」的资产：审计重复·孤儿·陈旧·无籍四维度，给出收敛(单一真源)+门禁(改前备份)两步流程，附可运行脚本（记忆审计器）。记忆不是「能存」，是「有籍、无重、可回滚」。

## Why it beats "just dump everything into memory"

| Pain | This skill |
|---|---|
| Memory contradicts itself | Duplicate detection → single source of truth |
| Can't tell who wrote what | Every entry carries source + updated (有籍) |
| Bulk edit destroyed history | Gate = backup first, reversible |
| Stale temp note still trusted | Stale-dim check flags old non-law entries |

## What's inside

- `SKILL.md` — 4-dimension audit + 2-step flow + entry template + 铁律
- `scripts/memory_audit.py` — zero-dependency CLI: scan dir/JSONL, flag duplicate/orphan/stale/unsourced, emit report

```bash
python scripts/memory_audit.py --dir ./memory --stale-days 30
python scripts/memory_audit.py --file entries.jsonl --json
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Obsidian/Notion mem | Store & link notes | No dup/contradiction governance |
| Vector DB memory | Retrieve by similarity | No provenance, no staleness |
| "Just append to log" | Append forever | Grows contradictions unbounded |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `context-engineering` and `memory-governance`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
