# fact-check-guard · 事实核查护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat every factual claim as a *claim to be proven*. Match each against retrieved sources and label supported / dubious / unsourced; unsourced claims are not allowed out as fact. Ships a zero-dependency `fact_guard.py`.

**中文** — 把每条关键声明当待证主张，对照来源逐条标 已支撑/存疑/无来源，无来源不许当事实对外。零依赖 `fact_guard.py`。

## Why it beats "it sounds right, ship it"

| Pain | This skill |
|---|---|
| Fabricated citations | Unsourced claim → blocked as fact |
| Stale "facts" | Source match required, else dubious |
| "Studies show…" with no study | No source → downgrade wording |
| One wrong sentence in good text | Per-claim labeling, not whole-doc |

## What's inside

- `SKILL.md` — 3-state claim labeling + 3-step flow + 铁律
- `scripts/fact_guard.py` — zero-dependency CLI: given claims + sources, label each supported/dubious/unsourced

```bash
python scripts/fact_guard.py --claims claims.txt --sources refs.txt
python scripts/fact_guard.py --claims claims.txt --sources refs.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| RAG only | RAG retrieves; this gates *publication* on support |
| Manual proofread | Per-claim automated, repeatable |
| "Trust the model" | Explicit unsourced-block rule |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `rag-grounding-guard` and `doc-desens-scanner`.

---

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237) · 代码 MIT · 理论文本保留所有权利

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
