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
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
