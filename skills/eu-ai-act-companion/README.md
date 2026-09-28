# eu-ai-act-companion · EU AI Act 合规导航

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Turn the EU AI Act from hundreds of pages into a navigation map: classify risk (unacceptable / high / limited / minimal), list obligations by role (provider / deployer / importer / distributor), and surface the key deadlines (2024-08 entry into force → 2025-02 banned → 2026-08 high-risk → 2027-08 full). Ships a runnable `eu_ai_act_nav.py` that takes a use-case + role and returns the risk level, obligations, and milestones. Generalized from `eu-ai-act-check` (the medical-device crossover).

**中文** — 把 EU AI Act 落成导航：风险四级分类、按角色义务清单、关键时间节点、合格评定与 CE 路径。附可运行分类器，输入用例即输出风险级 + 义务 + 节点。泛化自 eu-ai-act-check。

## Why a companion, not a PDF

| Need | This skill |
|---|---|
| "Am I high-risk?" | `eu_ai_act_nav.py` classifies from your use-case |
| "What must I do?" | Role-based obligation list |
| "When's the deadline?" | Milestone timeline, not a wall of text |

## What's inside

- `SKILL.md` — 4-level risk table + role obligations + timeline + 铁律
- `scripts/eu_ai_act_nav.py` — zero-dependency CLI

```bash
python scripts/eu_ai_act_nav.py --use "招聘简历筛选AI" --role provider
# risk level = high  (高风险：须走合格评定 + CE 标志 + 全套义务)
```

## Benchmark

| Resource | It does | Gap this fills |
|---|---|---|
| EU AI Act full text | Authoritative | Unnavigable for builders |
| Law-firm summaries | Readable | Static, no classification |
| This skill | Classify + obligate + date, runnable | Actionable per use-case |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Companion to `eu-ai-act-check`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0 · 参考框架非法律意见

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
