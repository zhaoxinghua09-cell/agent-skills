# originality-check · 赛事作品原创性查重器

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with organizing committee. Text verified: 2026-09-26.

## What it does
Checks **submission originality** by fingerprint comparison against a known-hashes corpus, per **UIBC 原创性规范 + 学术不端界定** (rule source pending manual verification; latest UIBC charter prevails).

- **Insufficient input → strict presumption**: an empty/missing `known_hashes` corpus makes any "no duplicate" verdict **unreliable** — the tool states this in `warnings` (`rc=1`) instead of silently passing as original. Malformed `known_hashes` JSON → `rc=2`.
- Similarity is a placeholder algorithm (prefix comparison); real screening needs MinHash/SimHash + human review (noted in output `notes`).

## Install & run (zero-dependency, Python 3.8+)
```bash
python originality-check.py --submission_hash sha256:new999 --known_hashes '["sha256:aaa111","sha256:bbb222"]'   # clean w/ corpus → rc=0
python originality-check.py --submission_hash sha256:aaa111 --known_hashes '["sha256:aaa111"]'                   # duplicate hit → rc=1
python originality-check.py --submission_hash sha256:new999                                                      # empty corpus → strict warning, rc=1
python originality-check.py --submission_hash sha256:x --known_hashes '{bad'                                     # invalid JSON → rc=2
python originality-check.py --demo                                                                               # 3 built-in smoke cases
```
Params: `submission_hash` (required) / `known_hashes` (JSON string list).

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `similarity`, `is_duplicate`, `exact_match`, `matches`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`--demo`, case 3, verbatim warnings):
```json
{
  "input": {"submission_hash": "sha256:new999"},
  "result": {
    "similarity": 0.0, "is_duplicate": false, "exact_match": false, "matches": [],
    "warnings": ["known_hashes 为空（未提供对照指纹库）：本输出「无重复」不可靠，请提供历史/公开库指纹后复核；不静默按原创通过处理。"]
  },
  "rc": 1
}
```

## 规则源待人工核对清单
| 规则 / 数值 | 用途 | 状态 |
|---|---|---|
| UIBC 原创性规范 | 重复判定规则来源 | 待人工核对 |
| 相似度阈值 0.85 | 重复判定断点 | 待人工核对 |

## Compliance & IP
- LGD-Powered badge · theory TH-EVT-005 · ambassador 诺源@DAT 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。
- **Layered licence**: code `originality-check.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

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
