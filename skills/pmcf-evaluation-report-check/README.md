# pmcf-evaluation-report-check · PMCF 评价报告完整性检查器

> Zero-dependency deterministic CLI screener for medical-device compliance.
> **Decision support only — NOT legal/regulatory advice. Always verify against official texts.** Text verified: 2026-09-26.

## Why

计划做完了，报告交上去还是被退——少一节「所采取措施」，或少一次年度周期，就得重来。

## What it does

Screens `pmcf-evaluation-report-check` against public rule sources: **MDR (EU) 2017/745 Annex XIV Part B + Art 86 / MDCG 2020-7、2020-8**.
Outputs deterministic JSON IR with `rc` (0 = ok / 1 = ok with warnings / 2 = insufficient input),
`error_code`, and GB 45438-2025 AIGC metadata. No network, no API key, no third-party packages.

- **Insufficient input → strict presumption**: missing report sections and the IIb-implant period ambiguity (annual PSUR vs biennial) are both spelled out in `warnings` (`rc=1`) — never silently outputs the lenient period.
- Measured: `--device_class IIa` + all six sections `yes` → rc=0; `--device_class IIb` alone → rc=1; `--device_class I` → rc=2 (invalid enum).

## Run it (Python 3.8+)

```bash
python pmcf-evaluation-report-check.py --demo
python pmcf-evaluation-report-check.py --json <your args...>
```

## Compliance & IP

- Author: 注册老炮@MedXpert · © 2026 MedXpert · MIT License
- Theory anchor: `TH-MED-008` (LGD · registry / evidence / gate)
- Published by an AI-assisted studio; the institution bears responsibility for the output.
- Online (Chinese): https://medxpert.cn/knowledge/

## License & attribution
**Layered licence** — `pmcf-evaluation-report-check.py` = **MIT**; this `README.md` / `SKILL.md` and the theory text therein are **not covered by MIT** (all rights reserved). Code (.py) is MIT; the SKILL.md and its theory text are outside the MIT scope.

## Family

| 环节 | 工具 | 位置 |
|---|---|---|
| 分类与路径 | `md-classification-route` | 本批 |
| 注册资料-技术文件 | `medxpert-reg-hub` | 存量枢纽 |
| 临床评价（选路） | `clin-eval-route-picker` | 存量 |
| 临床评价（证据要素） | `cer-equivalence-check` | 本批 |
| 检测项目与实验室匹配 | `test-lab-match-check` | 本批 |
| 申报前非临床研究 | `non-clinical-checker` | 存量 |
| UDI（格式校验） | `udi-format-validator` | 存量 |
| UDI（数据库提交） | `udi-db-submission-check` | 本批 |
| 上市后·PMCF 计划 | `pmcf-plan-check` | 存量 |
| 上市后·PMCF 评价报告 | `pmcf-evaluation-report-check` | 本批 |
| 上市后·不良事件 | `pms-vigilance-intake` | 存量 |
| 上市后·召回 | `recall-decision-checker` | 存量 |
| 标签与说明书 | `label-compliance-checker` | 存量 |
| 进出口路径 | `import-export-router` | 存量 |
