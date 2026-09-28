# agent-memory-keeper · 跨会话长期记忆治理

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat agent long-term memory as an asset that is *sourced, auditable, and convergent*. Audit duplicate · orphan · stale · unsourced; ship a 2-step flow (converge to single source of truth → gate changes behind backup) plus a runnable `memory_audit.py` (memory auditor over a dir or JSONL). Memory isn't "can store" — it's "has provenance, no dup, reversible".

**中文** — 把 agent 长期记忆当成「有籍贯、可审计、能收敛」的资产：审计重复·孤儿·陈旧·无籍四维度，给出收敛(单一真源)+门禁(改前备份)两步流程，附可运行脚本（记忆审计器）。记忆不是「能存」，是「有籍、无重、可回滚」。

## Why it beats "just dump everything into memory"

| Pain | This skill |
|---|---|
| Memory contradicts itself | Duplicate detection → single source of truth |
| Can't tell who wrote what | Every entry carries source + updated (有籍) |
| Bulk edit destroyed history | Gate = backup first, reversible |
| Stale temp note still trusted | Stale-dim check flags old non-law entries |

## What's inside

- `SKILL.md` — 4-dimension audit + 2-step flow + entry template + 铁律
- `scripts/memory_audit.py` — zero-dependency CLI: scan dir/JSONL, flag duplicate/orphan/stale/unsourced, emit report

```bash
python scripts/memory_audit.py --dir ./memory --stale-days 30
python scripts/memory_audit.py --file entries.jsonl --json
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Obsidian/Notion mem | Store & link notes | No dup/contradiction governance |
| Vector DB memory | Retrieve by similarity | No provenance, no staleness |
| "Just append to log" | Append forever | Grows contradictions unbounded |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `context-engineering` and `memory-governance`.

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
