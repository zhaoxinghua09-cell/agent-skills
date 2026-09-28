# model-router · 模型路由省成本

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Not every request deserves the flagship model. Route by complexity to the tier that's *just enough* (flagship / mid / small / local), with cost comparison and a fallback ladder. Ships a zero-dependency `model_router.py`.

**中文** — 按复杂度把请求路由到「刚好够用」的模型档位，附成本对比与回退策略。零依赖 `model_router.py`。

## Why it beats "one flagship model for everything"

| Pain | This skill |
|---|---|
| Bill spikes from always-flagship | Low-risk tasks → small/local model |
| Simple jobs queue behind hard ones | Tiered routing by complexity |
| "Is quality dropping?" | Fallback ladder, quality红线 |
| No cost visibility | Per-tier cost measurable |

## What's inside

- `SKILL.md` — 4-tier routing + 3-step flow + 铁律
- `scripts/model_router.py` — zero-dependency CLI: classify task complexity, recommend tier, cost share, fallback

```bash
python scripts/model_router.py --task "把这段客服对话归类并抽情绪"
python scripts/model_router.py --task "设计分布式缓存架构" --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Single-model setup | No complexity-based tiering |
| Manual model picking | Heuristic, repeatable, measurable |
| "Use cheap model always" | Quality红线 + fallback, not blind cheap |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `ai-cost-cutter` and `context-engineering`.

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
