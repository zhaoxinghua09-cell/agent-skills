# import-export-router · 医疗器械进出口路径判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts.

## What it does
Classifies `import-export-router` per official rules: **NMPA 进口医疗器械注册规定 + 出口销售证明办理 + FDA/EU MDR**.

## Install & run (zero-dependency, Python 3.8+)
```bash
python import-export-router.py --demo
python import-export-router.py --device_class III
```

## Output
Deterministic JSON IR with `rc` (0=ok, 1=with warnings, 2=insufficient input) and `aigc_mark` (GB45438-2025 metadata).

## Compliance & IP
- LGD-Powered badge · theory TH-MED-005 · ambassador 诺衡@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核。

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |
