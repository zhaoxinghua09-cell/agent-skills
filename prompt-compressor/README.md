# prompt-compressor · 提示/上下文压缩

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Compress by *information density*, not by cutting chars: keep keyword-dense & position-weighted sentences, drop filler/repetition. Runnable `compress_prompt.py` scores sentences and trims to a target ratio while protecting constraints, numbers, and code. Pairs with `context-engineering` (it decides *what* to put in; this decides *how short*).

**中文** — 按信息密度压缩：保留关键词密集/位置靠前的句子，删冗余与复述。附可运行脚本（按密度+位置打分删句），护住约束句/数字/代码。与 `context-engineering` 互补。

## Why it beats "just truncate"

| Pain | This skill |
|---|---|
| Truncating loses the key sentence | Density+position scoring keeps constraints |
| Numbers/code get mangled | Structural tokens protected |
| Blind ratio cut | Target-ratio trim from lowest score up |

## What's inside

- `SKILL.md` — 3 principles + 3-step flow + 铁律
- `scripts/compress_prompt.py` — zero-dependency CLI: score & trim sentences to a ratio

```bash
python scripts/compress_prompt.py --text "长文本..." --ratio 0.5
python scripts/compress_prompt.py --file doc.txt --ratio 0.4
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Manual copy-edit | Slow, subjective | Scored, repeatable |
| Head/tail truncate | Cuts mid-thought | Keeps high-value sentences |
| LLM summarize | Costs a call | Local, free, deterministic |

Theoretical root: **LGD Three Laws** — convergence (drop redundancy). Pairs with `context-engineering`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
