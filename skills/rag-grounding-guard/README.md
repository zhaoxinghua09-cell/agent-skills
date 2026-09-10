# rag-grounding-guard · RAG事实溯源校验

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — RAG dies not on "no retrieval" but on "retrieved yet unused, plus fabricated". Verify each claim against retrieved sources: coverage rate + uncovered claims flagged as hallucination risk; citations must carry a source (有籍). Runnable `grounding_check.py`. Theoretical root: LGD — registered (citation) + evidenced (verifiable).

**中文** — 逐条校验声明是否被检索来源支撑，未覆盖标红为幻觉风险，引用强制带出处。附可运行脚本。理论根基：LGD 有籍+有证。

## Why it beats "trust the retrieved docs"

| Pain | This skill |
|---|---|
| Model fabricates beyond sources | Per-claim coverage check |
| Citation points nowhere | Citations must carry source |
| No quality metric | Grounding coverage rate (有证) |

## What's inside

- `SKILL.md` — 2 checks + 3-step flow + 铁律
- `scripts/grounding_check.py` — zero-dependency CLI: claim-vs-source coverage

```bash
python scripts/grounding_check.py --claims claims.txt --sources sources.txt
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Vector rerank | Better top-k | No claim-level grounding |
| "It cited a doc" | Vague | Citation may be wrong doc |
| Human spot-check | Slow | Not per-claim, not scaled |

Theoretical root: **LGD Three Laws** — registered + evidenced. Pairs with `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
