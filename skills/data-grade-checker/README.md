# data-grade-checker · 数据分类分级判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts.

## What it does
Classifies `data-grade-checker` per official rules: **GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)**.

## Install & run (zero-dependency, Python 3.8+)
```bash
python data-grade-checker.py --demo
python data-grade-checker.py --mtow 5
```

## Output
Deterministic JSON IR with `rc` (0=ok, 1=with warnings, 2=insufficient input) and `aigc_mark` (GB45438-2025 metadata).

## Compliance & IP
- LGD-Powered badge · theory TH-DAT-001 · ambassador 诺源@DAT 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |
