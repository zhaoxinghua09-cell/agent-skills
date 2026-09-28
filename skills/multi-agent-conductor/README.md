# multi-agent-conductor · 多智能体编排

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Multi-agent projects fail on blurred boundaries, not model power. Decompose a task → assign roles → pin each agent's *allowed / forbidden* boundary (gated). Runnable `conductor_plan.py` emits a role table + boundary list. Theoretical root: LGD — gated (task boundary + permission isolation).

**中文** — 把大任务拆成角色、给每个 agent 定死「能做什么、禁止碰什么」，避免串权限/重复劳动。附可运行脚本（编排规划器）。理论根基：LGD 有门禁。

## Why it beats "spawn N agents and pray"

| Pain | This skill |
|---|---|
| Agents overwrite each other | Per-agent forbidden boundary |
| Duplicate work | Decomposition with dependency map |
| Contradictory outputs | Single conductor sums & checks |

## What's inside

- `SKILL.md` — 3 elements + 3-step flow + 铁律
- `scripts/conductor_plan.py` — zero-dependency CLI: role table + boundaries

```bash
python scripts/conductor_plan.py --task "写一份市场分析报告" --agents 3
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| AutoGen/CrewAI | Run agents | No explicit forbidden-boundary gate |
| "Just prompt team" | Ad hoc | Roles blur, conflicts |
| Single big agent | One context | Hits window/quality wall |

Theoretical root: **LGD Three Laws** — gated. Pairs with `context-engineering`.

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
