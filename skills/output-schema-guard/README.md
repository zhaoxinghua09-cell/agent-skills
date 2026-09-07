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
