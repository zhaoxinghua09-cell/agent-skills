# ai-policy-radar · AI法规动态雷达

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — AI regulation moves monthly. Scan a regulatory library/changelog across EU/US/CN, tag items by theme (risk tier · transparency · data · market access), log source+date (evidenced), and tell you "what's new this month, what it hits". Runnable `policy_radar.py`. Theoretical root: LGD — evidenced (reg-change logged). Pairs with `eu-ai-act-companion`.

**中文** — 跨法域（EU/US/CN）扫描 AI 监管动态，按主题归类、留痕，输出「本月新增+对你影响」。附可运行脚本。理论根基：LGD 有证。与 eu-ai-act-companion 互补。

## Why it beats "read the news occasionally"

| Pain | This skill |
|---|---|
| Miss a compliance deadline | Themed scan + date log |
| Don't know which law hits you | Per-item impact tag |
| EU vs CN conflict unseen | Cross-jurisdiction side-by-side |

## What's inside

- `SKILL.md` — 4 themes + 3-step flow + 铁律
- `scripts/policy_radar.py` — zero-dependency CLI: scan a dir of md for reg keywords

```bash
python scripts/policy_radar.py --dir ./reg-notes --since 2026-09
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Newsletters | Narrative | No structured themed log |
| "Google it" | Ad hoc | Not logged, not repeatable |
| Single-law trackers | One jurisdiction | No cross-jurisdiction view |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `eu-ai-act-companion`.

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
