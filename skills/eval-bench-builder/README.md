# eval-bench-builder · 评测基准构建器

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — "Is the AI good?" can't be a feeling. Turn capability spec + edge cases into structured, reproducible eval samples (input / expect / judge). Runnable `bench_build.py` emits a JSONL bench. Theoretical root: LGD — evidenced (eval is reproducible, verifiable). Pairs with `skill-quality-gate`.

**中文** — 把能力说明+边界用例变成结构化、可复现评测样本（输入/期望/判定），改一次比一次。附可运行脚本。理论根基：LGD 有证。

## Why it beats "feels about right"

| Pain | This skill |
|---|---|
| Subjective scoring | Machine-readable judge per case |
| Only happy-path tested | Edge + adversarial cases required |
| Can't compare runs | Fixed, locked benchmark |

## What's inside

- `SKILL.md` — 3 elements + 3-step flow + 铁律
- `scripts/bench_build.py` — zero-dependency CLI: spec → JSONL eval set

```bash
python scripts/bench_build.py --spec spec.md --out bench.jsonl
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Leaderboard scores | One number | No per-case judge, not yours |
| Ad-hoc prompts | Unrepeatable | Not locked, not regressible |
| "Looks good" | — | No evidence |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `skill-quality-gate`.

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
