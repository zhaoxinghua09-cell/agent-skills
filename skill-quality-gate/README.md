# skill-quality-gate · 技能质量门禁

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — A skill isn't shippable just because it's written. 9-dimension gate: frontmatter fields · script compiles · icon · README · no secrets · bilingual · triggers · gate section · desensitized. Fail any → block publish. Runnable `quality_gate.py`. Theoretical root: LGD — gated (gate before publish).

**中文** — 9 维校验卡一道闸：frontmatter 八字段/脚本可编译/图标/README/无密钥/双语/触发词/门禁节/去敏。任一 fail 即拦截发布。附可运行脚本。理论根基：LGD 有门禁。

## Why it beats "publish and pray"

| Pain | This skill |
|---|---|
| Skill won't run | py_compile check |
| Leaks secrets | Secret-pattern scan |
| No docs / no zh-en | README + bilingual check |

## What's inside

- `SKILL.md` — 9 dimensions + 2-step flow + 铁律
- `scripts/quality_gate.py` — zero-dependency CLI: gate a skill dir

```bash
python scripts/quality_gate.py --dir ./my-skill
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Market auto-review | Opaque | Transparent 9-dim, local |
| "Looks fine" | Subjective | Deterministic pass/fail |
| Manual checklist | Forgetful | Scripted, repeatable |

Theoretical root: **LGD Three Laws** — gated. Pairs with `release-gate`.

---

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
