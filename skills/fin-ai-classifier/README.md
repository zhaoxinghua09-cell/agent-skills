# fin-ai-classifier · 金融 AI 应用分级判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

## What it does
Classifies financial AI applications into I/II/III risk grades per **TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向** (pending manual verification; the latest regulatory guidance prevails).

- **Insufficient input → strict presumption (从严推定)**: with `autonomy`/`impact` missing, the tool returns the **most obligation-heavy grade** among the possible ones, states the possible range in `warnings`, and sets `rc=1`. It never silently returns I 级（低风险）.
- **No silent invalid input**: out-of-enum values → gate error (`rc=2`).
- **Out of scope**: licensing status, filing material lists, algorithm-filing workflow.

## Install & run (zero-dependency, Python 3.8+)
```bash
python fin-ai-classifier.py --demo   # 2 built-in smoke cases
# rc=1 (strict presumption, no args)
python fin-ai-classifier.py
# rc=0 (complete args → I 级)
python fin-ai-classifier.py --autonomy info --impact low
# rc=2 (invalid input)
python fin-ai-classifier.py --autonomy full --impact extreme
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `autonomy` | no* | 自主度：full/human_in_loop/info（缺省按从严推定） |
| `impact` | no* | 影响：high/mid/low（缺省按从严推定） |
| `target` | no | 对象：consumer/institution |

\* 语义上为分级关键参数；缺省时输出从严推定结论并告警，不阻塞执行。

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = invalid input), `grade`, `obligations`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real output (no args, values verbatim):

```json
{
  "input": {"autonomy": null, "impact": null, "target": null},
  "result": {
    "grade": "III 级（高风险）",
    "obligations": ["算法备案", "人工兜底 + 可解释", "模型与数据合规审计", "监管报送"],
    "warnings": [
      "输入不完整：未提供 autonomy / impact；建议补齐后复核。",
      "分级不确定（可能区间 I 级（低风险）～III 级（高风险））：已按从严推定取『III 级（高风险）』（义务最重者），实际等级可能更宽松；请补齐参数后复核。",
      "全自动高影响面向消费者——须严格备案与人工兜底，禁止'AI 荐股/放贷'无资质经营"
    ]
  },
  "rc": 1
}
```

## Rule-source review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| TH-FIN-002 母版 | I/II/III 级分级框架 | 待人工核对 |
| full + high → III 级 | 最高级触发条件 | 待人工核对 |
| human_in_loop + high/mid → II 级 | 中风险级触发条件 | 待人工核对 |
| 算法备案（依舆论属性） | II 级义务引用 | 待人工核对 |
| 禁止 AI 荐股/放贷无资质经营 | III 级告警依据 | 待人工核对 |

## Theory hook
金融的自治须有级——分级即把'AI 能否替你做决定'钉进监管坐标。域站位件：TH-FIN-002。

## Pointers
- LGD theory page: https://medxpert.cn/lgd.html · Skill library: https://medxpert.cn/skills/ · llms.txt: https://medxpert.cn/llms.txt
- LGD 理论总账 REGISTRY 在线页：(地址待补) · FIN 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `fin-ai-classifier.py` | **MIT** |
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
**本包补充**：`fin-ai-classifier.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |
