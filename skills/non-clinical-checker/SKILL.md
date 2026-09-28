---
name: non-clinical-checker
slug: non-clinical-checker
displayName: 医疗器械非临床研究判定器
version: 1.0.0
category: it-ops-security
display_name: 医疗器械非临床研究判定器
title: 医疗器械非临床研究判定器
author: 诺康(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械非临床研究判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-001域（医疗器械全链路）。
tags: [医疗器械, 合规, 判定器, TH-MED-001, non-clinical-checker]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械非临床研究判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成医疗器械合规结论或法律/法规意见。输出请人工复核，最终以监管机构（NMPA/省局）认定为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 合规与免责声明（B 级 · YMYL 影响生命健康类）
- 本工具输出为**决策支持**，不构成注册、召回、不良事件报告等官方结论；正式结论须以主管部门（NMPA/省局）书面决定及官方最新条文为准。
- 规则源：`GB/T 16886 系列 / YY 0505 / GB 9706.1`，请以官方正式文本核对。
- 不得依据本工具输出直接做出临床、注册或召回决策。

## 一、痛点
医疗器械全链路规则白纸黑字但散落多份文件，企业自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见、不出具合规证明；结论须人工复核，最终以监管机构认定为准。
- 规则源：`GB/T 16886 系列 / YY 0505 / GB 9706.1`（以官方最新文本为准）。
- **输入不足时从严提示**：缺 `device_type` / `device_class` / `contact` 任一参数时，在 `warnings` 中明示可能漏项（如 EMC、电气安全、分析性能）与补参建议（`rc=1`）——**不静默按宽松清单输出**。
- **不覆盖**：具体产品的检测项目全集（须由产品技术要求与风险管理输出推导）、检测机构的选择与排期、临床评价路径；这些须另行判定。

## 三、用法
```bash
python non-clinical-checker.py --device_class III --device_type implant   # 按参数判定，rc=0
python non-clinical-checker.py --device_class II --device_type active     # 缺 contact → 从严提示，rc=1
python non-clinical-checker.py --demo                                     # 跑内置冒烟案例
```
参数：`device_class`（I/II/III）/ `device_type`（active/passive/implant/ivd）/ `contact`（surface/insert/implant）；`device_class` 与 `device_type` 至少给一个，非法枚举值拒绝判定（`rc=2`）。

## 四、真机输出（实跑节选）
> 实跑命令 `python non-clinical-checker.py --device_class II --device_type active`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "non-clinical-checker",
  "version": "1.0.0",
  "input": {"device_class": "II", "device_type": "active", "contact": null},
  "result": {
    "required_studies": [
      "生物学评价（细胞毒性/致敏/刺激等基础项，按接触性质+持续时间定终点）",
      "电磁兼容 EMC（YY 0505 / YY 9706.102）",
      "电气安全（GB 9706.1 通用+专用并列标准）"
    ],
    "obligations": ["委托具备 CMA/CNAS 资质的检测机构", "研究与风险管理输出同步", "结果纳入注册申报资料"],
    "notes": ["生物学评价终点以 GB/T 16886.1 表 A.1 接触性质+持续时间为准", "有源器械 EMC/安规为强制", "本判定为项目清单建议，非检测结论"],
    "evidence": ["GB/T 16886 系列", "YY 0505", "GB 9706.1"],
    "warnings": [
      "输入不完整：未提供 contact（接触性质）——生物学评价终点按 GB/T 16886.1 表 A.1 接触性质+持续时间判定，建议补参后按表 A.1 复核终点选择。"
    ]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "non-clinical-checker@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 参数完整：`--device_class III --device_type implant --contact implant` |
| `1` | 完成但带风险提示（warnings） | 输入不足从严提示（如 `--device_class II --device_type active` 缺 contact） |
| `2` | 输入不足/输入非法，无法判定 | 只给 `--contact` 不给类别/类型；或枚举值非法（如 `--device_class IV`） |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源条款号便于核对。
- Q：缺参数会怎样？ A：在 `warnings` 中明示可能漏项与补参建议（`rc=1`），不会静默按宽松清单输出。

## 理论依据
安全始于未上市——非临床研究即把'风险'写进数据，而非写进事故。
域站位件：TH-MED-001 · 理论总账 REGISTRY · 医疗器械全链路。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 医械注册知识库（免费公开层）：https://medxpert.cn/knowledge/
- 技能索引页：https://medxpert.cn/skills/

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `non-clinical-checker.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码（.py）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（理论文本保留所有权利）。** 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```

---
诺康@MED 域首席发声人 · TH-MED-001 · SynomosAI（AI 辅助生成，非自然人）
