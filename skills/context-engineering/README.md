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
