# judging-rubric-grader · 赛事评审打分器

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with organizing committee. Text verified: 2026-09-26.

## What it does
Grades submissions by **multi-dimension rubric weighting** per **UIBC 评审规范（rubric 加权）** (rule source pending manual verification; latest UIBC charter prevails).

- **Insufficient input → strict presumption**: a dimension missing from `scores` is counted as **0** (lowering the total) and stated in `warnings` (`rc=1`) — never silently skipped or full-marked. Weight sum ≠ 1 also warns.
- **Out of scope**: judge deliberation, appeals, overall endorsement of submission safety/correctness.

## Install & run (zero-dependency, Python 3.8+)
```bash
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.4},{"dim":"工程","weight":0.3},{"dim":"表达","weight":0.3}]' --scores '{"创新":90,"工程":85,"表达":80}'   # complete → rc=0
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.5},{"dim":"合规","weight":0.5}]' --scores '{"创新":90}'                                                   # missing dim → strict 0, rc=1
python judging-rubric-grader.py                                                                                                                                                  # missing args → rc=2
python judging-rubric-grader.py --demo                                                                                                                                           # 3 built-in smoke cases
```
Params: `criteria` (JSON dim/weight list, required) / `scores` (JSON dim→score object, required) / `pass_line` (default 60).

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `total`, `grade`, `per_dimension`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`--demo`, case 3, verbatim):
```json
{
  "input": {"criteria": "[{\"dim\":\"创新\",\"weight\":0.5},{\"dim\":\"合规\",\"weight\":0.5}]", "scores": "{\"创新\":90}", "pass_line": "60"},
  "result": {
    "total": 45.0, "grade": "D", "passed": false, "pass_line": 60.0,
    "warnings": [
      "以下维度未提供分数，从严按 0 分计（会拉低总分）：合规；请补齐 scores 中对应维度后复核。",
      "未达达标线（60.0）：机器门禁通过≠评审通过，建议复评或退回"
    ]
  },
  "rc": 1
}
```

## 规则源待人工核对清单
| 规则 | 用途 | 状态 |
|---|---|---|
| UIBC 评审规范·rubric | 加权总分与等级映射 | 待人工核对 |
| 等级断点 90/80/70/达标线 | 等级映射取值 | 待人工核对 |

## Compliance & IP
- LGD-Powered badge · theory TH-EVT-003 · ambassador 诺律@LAW 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。
- **Layered licence**: code `judging-rubric-grader.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

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
