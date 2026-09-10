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
