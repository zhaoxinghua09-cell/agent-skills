# hgrac-route-checker · 人类遗传资源事项路径判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts.

## What it does
Classifies `hgrac-route-checker` per official rules: **《人类遗传资源管理条例》(国务院令717号)+实施细则(2023-07-01施行) 第8-22条**.

## Install & run (zero-dependency, Python 3.8+)
```bash
python hgrac-route-checker.py --demo
python hgrac-route-checker.py --mtow 5
```

## Output
Deterministic JSON IR with `rc` (0=ok, 1=with warnings, 2=insufficient input) and `aigc_mark` (GB45438-2025 metadata).

## Compliance & IP
- LGD-Powered badge · theory TH-BIO-001 · ambassador 诺康@BIO 域首席发声人
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
