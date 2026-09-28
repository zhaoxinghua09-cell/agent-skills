# label-compliance-checker · 医疗器械标签合规核对器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## What it does
Checks medical-device **label/IFU mandatory elements** per official rules: **《医疗器械说明书和标签管理规定》(总局令 第6号) 第10-11条** (clause numbers pending manual verification; official texts prevail).

- **Insufficient input → strict presumption**: omitted `has_*` fields are **treated as missing** and stated in `warnings` (`rc=1`) — never silently counted as complete. Values other than yes/no → `rc=2`.
- **Out of scope**: consistency of label content with the registration certificate / technical requirements, UDI applicability, implant-specific items.

## Install & run (zero-dependency, Python 3.8+)
```bash
python label-compliance-checker.py --has_name yes --has_reg_no yes --has_manufacturer yes --has_indications yes --has_warnings yes --has_lot yes --has_udi yes   # all present → rc=0
python label-compliance-checker.py --has_name yes --has_reg_no no    # missing element → rc=1
python label-compliance-checker.py --has_name banana                 # invalid value → rc=2
python label-compliance-checker.py --demo                            # 3 built-in smoke cases
```
Params: `has_name / has_reg_no / has_manufacturer / has_indications / has_warnings / has_lot / has_udi` (yes/no; none given → `rc=2`).

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `compliant`, `missing_fields`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`--demo`, case 3, verbatim warnings):
```json
{
  "input": {"has_name": "yes", "has_reg_no": "yes", "has_manufacturer": "yes", "has_indications": "yes", "has_warnings": "yes", "has_lot": "yes"},
  "result": {
    "compliant": false,
    "missing_fields": ["UDI 标识（若适用）"],
    "warnings": ["以下要素未提供核对信息，从严按缺失处理：UDI 标识（若适用）；建议补齐后复核，避免核对范围不完整。"]
  },
  "rc": 1
}
```

## 条款号待人工核对清单
| 条款 | 用途 | 状态 |
|---|---|---|
| 说明书和标签管理规定 第6号 第10条 | 标签法定要素 | 待人工核对 |
| 说明书和标签管理规定 第6号 第11条 | 说明书法定要素 | 待人工核对 |

## Compliance & IP
- LGD-Powered badge · theory TH-MED-004 · ambassador 诺康@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。
- **Layered licence**: code `label-compliance-checker.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |

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
