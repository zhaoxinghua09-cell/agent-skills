---
name: test-lab-match-check
slug: test-lab-match-check
title: 医疗器械检测项目与实验室匹配器
displayName: 医疗器械检测项目与实验室匹配器
display_name: 医疗器械检测项目与实验室匹配器
display_name_en: MD Test Item Derivation & Lab Match Checker
version: 1.0.0
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: 注册老炮@MedXpert
copyright: MedXpert
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","医疗器械检测项目与实验室匹配器","判定器","TH-MED-010","决策支持"]
description: "送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (test-lab-match-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
---

![LGD-aligned MED 医疗](https://medxpert.cn/badge/directions/svg/lgd-aligned-med-cn.svg)
![LGD 有籍 Registered](https://medxpert.cn/badge/laws/svg/lgd-registered-cn.svg)
![LGD 有证 Evidenced](https://medxpert.cn/badge/laws/svg/lgd-evidenced-cn.svg)
![LGD 有门禁 Gated](https://medxpert.cn/badge/laws/svg/lgd-gated-cn.svg)
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械检测项目与实验室匹配器

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。输出请人工复核，正式结论须以主管部门决定与官方最新文件为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

> 🌐 **在线版与家族合集**
> - 医械注册知识库（免费公开层）：https://medxpert.cn/knowledge/
> - 技能索引页：https://medxpert.cn/skills/
> - 官网首页：https://medxpert.cn/

## 一、痛点

送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。

## 二、这是什么

一个**零依赖、确定性输出**的判定器。你把已知条件以参数传入，它按公开规则源给出结构化判定 + 义务清单 + 风险提示，输出 JSON IR（机器可读），可直接嵌入你自己的流程。

- **零依赖**：仅用 Python 标准库，无第三方包、无网络请求、无 API Key。
- **确定性**：同一输入永远同一输出（无随机、无模型调用）。
- **可回溯**：每条结论附规则源条款号，便于人工核对。
- **离线可用**：可在内网、断网、老电脑上运行。

## 三、判定核心

| 项 | 说明 |
|---|---|
| 规则源 | `GB/T 16886 系列 / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304` |
| 输出 | JSON IR（`result` + `rc` + `error_code` + `aigc_mark`） |
| 错误码 | `E_INPUT_MISSING` 参数不足 / `E_ENUM_INVALID` 枚举非法 / `E_RUNTIME` 其他 |
| 退出码 | `rc=0` 判定完成；`rc=1` 完成但带风险提示；`rc=2` 输入不足或非法 |

## 四、用法

```bash
python test-lab-match-check.py --demo                     # 跑内置冒烟案例（推荐先跑这个）
python test-lab-match-check.py --json <你的参数...>        # 正式判定
```

可用参数：`--device_type / --material / --contact / --sterile / --steril_method / --has_software / --dest`

## 四A、真机输出（实跑节选）
> 实跑命令 `python test-lab-match-check.py --device_type active --sterile yes`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "test-lab-match-check",
  "version": "1.0.0",
  "input": {"device_type": "active", "material": null, "contact": null, "sterile": "yes",
            "steril_method": null, "has_software": null, "dest": null},
  "result": {
    "device_type": "active",
    "required_tests": [
      "生物学评价·基础终点（细胞毒性/致敏/刺激，按接触性质与时长选做）",
      "电气安全（GB 9706.1 通用 + 适用专用并列标准）",
      "电磁兼容 EMC（YY 0505 / YY 9706.102）",
      "灭菌验证（须先确定灭菌方式：eo / radiation / steam）",
      "无菌屏障系统与包装验证（ISO 11607 / GB/T 19633）"
    ],
    "lab_qualification": ["CMA（检验检测机构资质认定）", "CNAS（实验室认可）"],
    "ref_cycle": "5–15 周（视项目数量与实验室排期，属量级参考）",
    "destination": "cn",
    "obligations": ["…3 条（认可范围核对 / 样品定型一致 / 项目由技术要求+风险推导）"],
    "notes": ["…3 条（推导结果 / 周期不构成承诺 / 出口需境外认可报告）"],
    "evidence": ["GB/T 16886 系列", "GB 9706.1", "YY 0505", "ISO 11135/11137/17665", "ISO 11607", "IEC 62304"],
    "warnings": [
      "未提供 --material：材料类别直接影响生物相容性终点与化学表征，缺失将降低清单精度",
      "已声明无菌但未指定灭菌方式，无法给出确定的验证标准"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "test-lab-match-check@MedXpert",
                "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}
}
```
（`obligations` / `notes` 数组字段值逐字未改，此处折叠。）

三档 rc 实测：`--device_type implant --material metal --contact implant --sterile yes --steril_method eo --dest cn` → rc=0；`--device_type active --sterile yes` → rc=1（缺材料/灭菌方式从严提示）；`--device_type ivd --contact garbage` / `--dest jp` → rc=2（枚举非法）。

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明；结论须人工复核，最终以监管机构/公告机构认定为准。
- **输入不足时从严提示**：缺 `--material`、声明无菌但缺灭菌方式等均在 `warnings` 中明示（`rc=1`），不静默按宽松清单输出。
- 不覆盖特殊情形（创新器械、药械组合、边界产品、纳米材料等），此类须走官方界定程序。
- 规则版本会变；**条款号已给出，请以官方最新文本核对**。
- 输出为起始清单，**不替代产品技术要求、适用标准清单与专业评价者判断**。

## 六、理论依据

有门禁先立标准——检测是把「合规」变成可复核数据的那道闸。

> 域站位件：`TH-MED-010` · LGD 理论总账 REGISTRY · 医疗器械全链路治理（有籍 · 有证 · 有门禁）

## 七、家族合集（按注册全流程）

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

---

诺衡@MED 域·合规核查 · TH-MED-010 · © 2026 MedXpert · MIT License
本内容由 AI 辅助生成（非自然人），署名机构承担出品责任。

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `test-lab-match-check.py` | **MIT** |
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
