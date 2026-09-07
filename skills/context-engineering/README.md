# context-engineering · 上下文工程

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Turn "what goes into the context window" into an auditable, trimmable, quantifiable engineering discipline. Audit relevance · redundancy · budget · decay; ship a 4-step flow (audit → trim → retrieve → gate) plus a runnable `context_budget.py` (token budget calculator + audit checklist generator). Prompting writes one sentence; context engineering designs everything the model sees each turn.

**中文** — 把「每轮喂给模型的信息」当成一门工程：审计相关性·冗余·预算·衰减四维度，给出裁剪/检索/记忆/门禁四步流程，附可运行脚本（上下文预算计算器 + 审计清单生成器）。prompt 是写一句话，context engineering 是设计 AI 每轮看到的全部信息。

## Why it beats "just write a better prompt"

| Pain | This skill |
|---|---|
| AI forgets early constraints in long chats | Key constraints pinned to system top; decay checklist |
| Token bill explodes | Budget template caps each block; redundancy detector |
| RAG hurts answers | Retrieval blocks carry source + relevance score |
| Memory chaos | Memory entries gated (backup → reversible → confirm) |

## What's inside

- `SKILL.md` — 4-dimension audit + 4-step flow + budget template + 铁律
- `scripts/context_budget.py` — zero-dependency CLI: token estimate per block, window %, cross-block redundancy, audit checklist

```bash
python scripts/context_budget.py --window 128000 --system sys.txt --memory mem.txt --retrieval retr.txt
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Prompt engineering guides | How to phrase one prompt | No system view of the whole window |
| LangChain/LLamaIndex memory | Store & retrieve | No governance: poison / dup / decay unchecked |
| Long-context "just use 200k" | Bigger window | Budget & relevance still matter; decay unsolved |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `memory-governance` and `release-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
