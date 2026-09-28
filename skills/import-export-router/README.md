# import-export-router · 医疗器械进出口路径判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## What it does
Routes medical-device **import/export compliance paths** per official rules: **NMPA 进口医疗器械注册规定 + 出口销售证明办理 + FDA/EU MDR** (rule sources pending manual verification; official texts prevail).

- **Insufficient input → strict presumption**: missing `is_registered` is treated as **not registered** (stricter path + `warnings`, `rc=1`) — never silently the lenient registered path.
- **Out of scope**: device classification (I/II/III), registration-testing details, destination-country document lists and timelines.

## Install & run (zero-dependency, Python 3.8+)
```bash
python import-export-router.py --direction import --is_registered yes   # complete args → rc=0
python import-export-router.py --direction export --is_registered no    # strict warning → rc=1
python import-export-router.py --direction banana                       # invalid input → rc=2
python import-export-router.py --demo                                   # 4 built-in smoke cases
```
Params: `direction` (import/export, required) / `is_registered` (yes/no) / `dest_region` (cn/us/eu/other).

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `route`, `required_docs`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`--demo`, case 4; arrays folded for readability; values verbatim):
```json
{
  "tool": "import-export-router",
  "input": {"direction": "export", "is_registered": "no", "dest_region": "eu"},
  "result": {
    "route": "须先取得境内注册/生产资质方可办理出口证明；境外上市须 CE 认证（EU MDR 技术文件+公告机构）",
    "required_docs": ["境内注册证/生产许可"],
    "warnings": ["境内未取得注册/生产资质：《医疗器械出口销售证明》无法办理，须先完成境内注册/取得生产资质后再出口"]
  },
  "rc": 1
}
```

## 条款号待人工核对清单
| 条款 / 规则 | 用途 | 状态 |
|---|---|---|
| NMPA 进口医疗器械注册规定 | 进口路径判定 | 待人工核对 |
| 《医疗器械出口销售证明》办理规定 | 出口路径判定 | 待人工核对 |
| FDA 510(k)/PMA | 出口美国准入 | 待人工核对 |
| EU MDR | 出口欧盟准入 | 待人工核对 |

## Compliance & IP
- LGD-Powered badge · theory TH-MED-005 · ambassador 诺衡@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。
- **Layered licence**: code `import-export-router.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

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
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
