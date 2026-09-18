# originality-check · 赛事作品原创性查重器

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with organizing committee.

## What it does
Classifies `originality-check` per UIBC rules: **UIBC 原创性规范 + 学术不端界定**.

## Install & run (zero-dependency, Python 3.8+)
```bash
python originality-check.py --demo
```

## Output
Deterministic JSON IR with `rc` (0=ok, 1=with warnings, 2=insufficient input) and `aigc_mark` (GB45438-2025 metadata).

## Compliance & IP
- LGD-Powered badge · theory TH-EVT-005 · ambassador 诺源@DAT 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |
