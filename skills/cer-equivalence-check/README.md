# cer-equivalence-check · 临床评价报告等同性论证要素检查器

> Zero-dependency deterministic CLI screener for medical-device compliance.
> **Decision support only — NOT legal/regulatory advice. Always verify against official texts.**

## Why

临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。

## What it does

Screens `cer-equivalence-check` against public rule sources: **MDR (EU) 2017/745 Art 61 + Annex XIV Part A / MDCG 2020-5、2020-6 / MEDDEV 2.7/1 rev.4**.
Outputs deterministic JSON IR with `rc` (0 = ok / 1 = ok with warnings / 2 = insufficient input),
`error_code`, and GB 45438-2025 AIGC metadata. No network, no API key, no third-party packages.

## Run it (Python 3.8+)

```bash
python cer-equivalence-check.py --demo
python cer-equivalence-check.py --json <your args...>
```

## Compliance & IP

- Author: 注册老炮@MedXpert · © 2026 MedXpert · MIT License
- Theory anchor: `TH-MED-009` (LGD · registry / evidence / gate)
- Published by an AI-assisted studio; the institution bears responsibility for the output.
- Online (Chinese): https://medxpert.cn/knowledge/

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
