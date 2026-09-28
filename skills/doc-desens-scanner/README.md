# doc-desens-scanner · 文档智能去敏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Scan a doc/code/log before it leaves the building: PII · secrets · internal paths · internal codenames, mask them and emit a `desens_report.json` (evidenced: what was redacted, when). Runnable `desens_scan.py`. Theoretical root: LGD — evidenced (desensitization is logged, accountable).

**中文** — 对外发布前扫描 PII·密钥·内部路径·内部项目代号，打码并输出脱敏清单（有证：脱敏动作可审计）。附可运行脚本。理论根基：LGD 有证。

## Why it beats "eyeball it"

| Pain | This skill |
|---|---|
| Secrets slip into public repos | Pattern lib catches `sk-` 前缀令牌 / `ghp_` / `password` 赋值 |
| Internal paths leak identity | Windows 用户目录 / home 目录 flagged |
| No record of what was redacted | `desens_report.json` (有证) |

## What's inside

- `SKILL.md` — 4 sensitive classes + 3-step flow + 铁律
- `scripts/desens_scan.py` — zero-dependency CLI: scan & mask, emit report

```bash
python scripts/desens_scan.py --file draft.md --mask ***
python scripts/desens_scan.py --text "密钥 sk-DEMO 示例路径 用户主目录" --report
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| GitLeaks | Secrets only | Misses PII / paths / codenames |
| Manual review | Slow | Not repeatable, no report |
| "Trust me" | — | No evidence trail |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `release-gate`.

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
