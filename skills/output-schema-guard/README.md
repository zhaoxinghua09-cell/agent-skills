# output-schema-guard · 结构化输出校验护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat model JSON as *untrusted external input*. Validate required fields · types · enums · nesting against a schema before it ever reaches your code; on failure emit an actionable fix hint (`{field, expected, got, hint}`) instead of a raw crash. Ships a zero-dependency `schema_guard.py`.

**中文** — 把模型 JSON 当不可信外部输入：进代码前用 schema 卡必填·类型·枚举·嵌套，失败吐可执行修复提示而非裸崩。附零依赖 `schema_guard.py`。

## Why it beats "just json.loads() and hope"

| Pain | This skill |
|---|---|
| LLM drops a required field → downstream None crash | Required-field gate fails *before* business code |
| Type drifts str↔int | Type check returns expected vs got |
| Enum out of range | Whitelist enum enforcement |
| "Works once, breaks next time" | Deterministic contract, not luck |

## What's inside

- `SKILL.md` — 4-dimension schema check + 2-step flow + schema example + 铁律
- `scripts/schema_guard.py` — zero-dependency CLI: validate JSON/text against a schema JSON, emit per-field pass/fail + fix hint

```bash
python scripts/schema_guard.py --schema schema.json --text '{"name":"x","status":"pending"}'
python scripts/schema_guard.py --schema schema.json --file out.jsonl --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| pydantic (python only) | No language-agnostic, no fix-hint for re-prompt |
| JSON Schema libs | Heavy, no LLM retry-gate pattern |
| "try/except json.loads" | Catches nothing semantic |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `context-engineering` and `skill-quality-gate`.

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
