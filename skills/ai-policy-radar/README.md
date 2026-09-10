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
