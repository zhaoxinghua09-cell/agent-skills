# recall-decision-checker · 医疗器械召回级别判定器

> AI-assisted decision-support CLI. NOT legal advice, **not a compliance proof** — verify against official texts. Text verified: 2026-09-26.

## What it does
Determines the **recall level and notification deadline** per official rules: **《医疗器械召回管理办法》(总局令 第29号)** — based on `harm_level` (severe/reversible/none, required) and `use_phase` (on_market/in_use/sold, optional).

- 一级（severe）→ 1 日内通知；二级（reversible）→ 3 日内；三级（none）→ 7 日内；均须向省局报告。
- **Insufficient input → strict presumption**: `use_phase=in_use/sold` → warning that the notification scope must also cover distributors and users, and in-use units need follow-up per the recall plan (`rc=1`). It never silently skips in-market obligations.
- Invalid enum values are rejected (`rc=2`) — garbage `harm_level` is NOT silently treated as Level III.

## Install & run (zero-dependency, Python 3.8+)
```bash
python recall-decision-checker.py --demo
python recall-decision-checker.py --harm_level severe                 # Level 1, 1-day, rc=1
python recall-decision-checker.py --harm_level reversible             # Level 2, 3-day, rc=0
python recall-decision-checker.py --harm_level severe --use_phase sold  # in-market notice warning, rc=1
python recall-decision-checker.py --harm_level garbage                # invalid enum → rc=2
```

## Output
Deterministic JSON IR with `rc` (0=ok / 1=with warnings / 2=insufficient or invalid input), `recall_level`, `notify_within_days`, `obligations`, `warnings`, `evidence`, and `aigc_mark` (GB 45438-2025 metadata, `is_generated: true`). Decision support only — final determination rests with the regulator.

## Compliance & IP
- LGD-Powered badge · theory TH-MED-003 · ambassador 诺康@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核，最终以监管机构认定为准。

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `recall-decision-checker.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, and all theory wording | **Not covered by MIT**: all rights reserved |

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |
