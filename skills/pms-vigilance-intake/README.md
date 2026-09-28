# pms-vigilance-intake · 医疗器械不良事件报告路径判定器

> AI-assisted decision-support CLI. NOT legal advice, **not a compliance proof** — verify against official texts. Text verified: 2026-09-26.

## What it does
Determines the individual adverse-event **reporting path and deadline** per official rules: **《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)** — based on `severity` (death/serious/possible_serious/other, required) and `event_type` (fault/use_error/design_defect, optional).

- **Insufficient input → strict presumption**: `possible_serious` without `event_type` → warning that a design-defect event may also trigger recall/re-evaluation assessment (`rc=1`). It never silently treats a lenient path as final.
- Invalid enum values are rejected (`rc=2`) — garbage severity is NOT silently treated as "other".
- `trigger_recall=true` cases point to `recall-decision-checker` for the follow-up decision.

## Install & run (zero-dependency, Python 3.8+)
```bash
python pms-vigilance-intake.py --demo
python pms-vigilance-intake.py --severity death        # immediate report + recall trigger warning, rc=1
python pms-vigilance-intake.py --severity serious      # 20-day path, rc=0
python pms-vigilance-intake.py --severity garbage      # invalid enum → rc=2
```

## Output
Deterministic JSON IR with `rc` (0=ok / 1=with warnings / 2=insufficient or invalid input), `report_path`, `deadline`, `trigger_recall`, `warnings`, `evidence`, and `aigc_mark` (GB 45438-2025 metadata, `is_generated: true`). Decision support only — final determination rests with the regulator.

## Compliance & IP
- LGD-Powered badge · theory TH-MED-002 · ambassador 诺康@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核，最终以监管机构认定为准。

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `pms-vigilance-intake.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, and all theory wording | **Not covered by MIT**: all rights reserved |

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |
