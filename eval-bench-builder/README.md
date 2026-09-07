# eval-bench-builder · 评测基准构建器

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — "Is the AI good?" can't be a feeling. Turn capability spec + edge cases into structured, reproducible eval samples (input / expect / judge). Runnable `bench_build.py` emits a JSONL bench. Theoretical root: LGD — evidenced (eval is reproducible, verifiable). Pairs with `skill-quality-gate`.

**中文** — 把能力说明+边界用例变成结构化、可复现评测样本（输入/期望/判定），改一次比一次。附可运行脚本。理论根基：LGD 有证。

## Why it beats "feels about right"

| Pain | This skill |
|---|---|
| Subjective scoring | Machine-readable judge per case |
| Only happy-path tested | Edge + adversarial cases required |
| Can't compare runs | Fixed, locked benchmark |

## What's inside

- `SKILL.md` — 3 elements + 3-step flow + 铁律
- `scripts/bench_build.py` — zero-dependency CLI: spec → JSONL eval set

```bash
python scripts/bench_build.py --spec spec.md --out bench.jsonl
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Leaderboard scores | One number | No per-case judge, not yours |
| Ad-hoc prompts | Unrepeatable | Not locked, not regressible |
| "Looks good" | — | No evidence |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `skill-quality-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
