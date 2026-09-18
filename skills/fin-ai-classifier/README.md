# fin-ai-classifier · 金融 AI 应用分级判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts.

## What it does
Classifies `fin-ai-classifier` per official rules: **TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向**.

## Install & run (zero-dependency, Python 3.8+)
```bash
python fin-ai-classifier.py --demo
python fin-ai-classifier.py --mtow 5
```

## Output
Deterministic JSON IR with `rc` (0=ok, 1=with warnings, 2=insufficient input) and `aigc_mark` (GB45438-2025 metadata).

## Compliance & IP
- LGD-Powered badge · theory TH-FIN-002 · ambassador 诺丰@FIN 域首席发声人
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
