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

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
