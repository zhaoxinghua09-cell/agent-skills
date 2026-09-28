# non-clinical-checker · 医疗器械非临床研究判定器

> AI-assisted decision-support CLI. NOT legal advice, **not a compliance proof** — verify against official texts. Text verified: 2026-09-26.

## What it does
Derives the pre-market **non-clinical study checklist** per official rules: **GB/T 16886 系列（生物学评价）/ YY 0505（EMC）/ GB 9706.1（电气安全）** — based on `device_class` (I/II/III), `device_type` (active/passive/implant/ivd) and `contact` (surface/insert/implant).

- **Insufficient input → strict presumption**: when `device_type` / `device_class` / `contact` is missing, the tool states the possibly-missing studies (e.g. EMC, electrical safety, analytical performance) and the补参 suggestion in `warnings`, and sets `rc=1`. It never silently returns a lenient checklist.
- Invalid enum values are rejected (`rc=2`).
- **Out of scope**: full per-product test item set (must be derived from product technical requirements + risk management output), lab selection & scheduling, clinical evaluation route.

## Install & run (zero-dependency, Python 3.8+)
```bash
python non-clinical-checker.py --demo
python non-clinical-checker.py --device_class III --device_type implant   # rc=0
python non-clinical-checker.py --device_class II --device_type active     # missing contact → warnings, rc=1
python non-clinical-checker.py --device_class IV                          # invalid enum → rc=2
```

## Output
Deterministic JSON IR with `rc` (0=ok / 1=with warnings / 2=insufficient or invalid input), `required_studies`, `obligations`, `warnings`, `evidence`, and `aigc_mark` (GB 45438-2025 metadata, `is_generated: true`, label basis noted as pending verification). Decision support only — final determination rests with the regulator.

## Compliance & IP
- LGD-Powered badge · theory TH-MED-001 · ambassador 诺康@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核，最终以监管机构认定为准。

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `non-clinical-checker.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, and all theory wording | **Not covered by MIT**: all rights reserved |

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |
