# hgrac-route-checker · 人类遗传资源事项路径判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

## What it does
Routes human-genetic-resource matters (collect/store/use/transfer/coop) to 审批 or 备案 per **《人类遗传资源管理条例》(国务院令717号)+实施细则(2023-07-01施行) 第8-22条** (clause numbers pending manual verification; official texts prevail).

- **Insufficient input → strict presumption (从严推定)**: `collect` without `foreign_involved`/`scale` returns the **most obligation-heavy route** (审批), states the possible range in `warnings`, and sets `rc=1`. It never silently returns 备案.
- **No silent invalid input**: non-yes/no `foreign_involved`, non-big/normal `scale`, unknown `action` → gate error (`rc=2`).
- **Out of scope**: material checklists, ethics review detail, processing timelines.

## Install & run (zero-dependency, Python 3.8+)
```bash
python hgrac-route-checker.py --demo   # 3 built-in smoke cases
# rc=1 (strict presumption, incomplete args)
python hgrac-route-checker.py --action collect
# rc=0 (complete args → 备案)
python hgrac-route-checker.py --action collect --foreign_involved no --scale normal
# rc=2 (invalid input)
python hgrac-route-checker.py --action collect --scale huge
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `action` | yes | 事项：collect/store/use/transfer/coop |
| `foreign_involved` | no | 是否涉外：yes/no |
| `scale` | no | 重要种类/累计人份：big/normal |

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `route`, `obligations`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real output (`--action collect`, values verbatim):

```json
{
  "input": {"action": "collect", "foreign_involved": null, "scale": null},
  "result": {
    "route": "审批（科技部）",
    "evidence": ["条例 第8-11条"],
    "warnings": [
      "输入不完整：未提供 foreign_involved / scale；官方对采集按「重要种类/累计人份规模」与「是否涉外」区分审批与备案，建议补齐后复核。",
      "路径不确定（可能区间 备案～审批（科技部））：已按从严推定取『审批（科技部）』（义务最重者），实际路径可能更宽松；请补齐参数后复核。"
    ]
  },
  "rc": 1
}
```

## Clause review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| 条例 第8-11条 | 采集/保藏的审批与备案区分 | 待人工核对 |
| 条例 第12-13条 | 保藏审批路径 | 待人工核对 |
| 条例 第14-16条 | 利用（备案/审批）路径 | 待人工核对 |
| 条例 第17-22条 | 对外提供/国际合作审批路径 | 待人工核对 |

## Theory hook
生命之源须有籍——遗传资源审批/备案即对人类共同遗产的受托登记。域站位件：TH-BIO-001。

## Pointers
- LGD theory page: https://medxpert.cn/lgd.html · Skill library: https://medxpert.cn/skills/ · llms.txt: https://medxpert.cn/llms.txt
- LGD 理论总账 REGISTRY 在线页：(地址待补) · BIO 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `hgrac-route-checker.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, the 「理论依据」 section and all theory wording | **Not covered by MIT**: all rights reserved |

> 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）
**本包补充**：`hgrac-route-checker.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |
