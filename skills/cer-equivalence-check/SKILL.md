---
name: cer-equivalence-check
slug: cer-equivalence-check
title: 临床评价报告等同性论证要素检查器
displayName: 临床评价报告等同性论证要素检查器
display_name: 临床评价报告等同性论证要素检查器
display_name_en: CER Equivalence Argument Element Checker
version: 1.0.0
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: 注册老炮@MedXpert
copyright: MedXpert
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","临床评价报告等同性论证要素检查器","判定器","TH-MED-009","决策支持"]
description: "临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (cer-equivalence-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
---

![LGD-aligned MED 医疗](https://medxpert.cn/badge/directions/svg/lgd-aligned-med-cn.svg)
![LGD 有籍 Registered](https://medxpert.cn/badge/laws/svg/lgd-registered-cn.svg)
![LGD 有证 Evidenced](https://medxpert.cn/badge/laws/svg/lgd-evidenced-cn.svg)
![LGD 有门禁 Gated](https://medxpert.cn/badge/laws/svg/lgd-gated-cn.svg)
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 临床评价报告等同性论证要素检查器

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。输出请人工复核，正式结论须以主管部门决定与官方最新文件为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

> 🌐 **在线版与家族合集**
> - 医械注册知识库（免费公开层）：https://medxpert.cn/knowledge/
> - 技能索引页：https://medxpert.cn/skills/
> - 官网首页：https://medxpert.cn/

## 一、痛点

临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。

## 二、这是什么

一个**零依赖、确定性输出**的判定器。你把已知条件以参数传入，它按公开规则源给出结构化判定 + 义务清单 + 风险提示，输出 JSON IR（机器可读），可直接嵌入你自己的流程。

- **零依赖**：仅用 Python 标准库，无第三方包、无网络请求、无 API Key。
- **确定性**：同一输入永远同一输出（无随机、无模型调用）。
- **可回溯**：每条结论附规则源条款号，便于人工核对。
- **离线可用**：可在内网、断网、老电脑上运行。

## 三、判定核心

| 项 | 说明 |
|---|---|
| 规则源 | `MDR (EU) 2017/745 Art 61 + Annex XIV Part A / MDCG 2020-5、2020-6 / MEDDEV 2.7/1 rev.4` |
| 输出 | JSON IR（`result` + `rc` + `error_code` + `aigc_mark`） |
| 错误码 | `E_INPUT_MISSING` 参数不足 / `E_ENUM_INVALID` 枚举非法 / `E_RUNTIME` 其他 |
| 退出码 | `rc=0` 判定完成；`rc=1` 完成但带风险提示；`rc=2` 输入不足或非法 |

## 四、用法

```bash
python cer-equivalence-check.py --demo                     # 跑内置冒烟案例（推荐先跑这个）
python cer-equivalence-check.py --json <你的参数...>        # 正式判定
```

可用参数：`--is_equivalent / --has_contract / --has_plan / --has_lit_search / --has_appraisal / --has_analysis / --has_conclusions / --has_gap / --has_qualification / --has_update`

## 四A、真机输出（实跑节选）
> 实跑命令 `python cer-equivalence-check.py --is_equivalent yes`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "cer-equivalence-check",
  "version": "1.0.0",
  "input": {"is_equivalent": "yes", "has_contract": null, "has_plan": null, "has_lit_search": null,
            "has_appraisal": null, "has_analysis": null, "has_conclusions": null, "has_gap": null,
            "has_qualification": null, "has_update": null},
  "result": {
    "path": "等同器械路径",
    "equivalence_conditions": [
      "技术等同：设计与制造、材料、性能、使用条件、灭菌方式等是否等同",
      "生物学等同：材料与生物相容性接触类型是否一致",
      "临床等同：临床使用场景、人群、部位、方法与预期效果是否一致"
    ],
    "missing_sections": ["临床评价计划（CEP）", "文献检索方案与检索结果", "数据评价与权重（appraisal）", "数据分析",
                         "结论与受益-风险判定", "临床缺口与 PMCF 衔接", "评价者资质", "更新计划与日期"],
    "complete": false,
    "obligations": ["…3 条（全生命周期更新 / 三条同时成立 / MDR 收紧边界）"],
    "notes": ["…3 条（要素在位≠论证成立 / NMPA 同品种比对不可直接互用 / 等同可用范围以法规原文为准）"],
    "evidence": ["MDR (EU) 2017/745 Art 61 / Annex XIV Part A", "MDCG 2020-5", "MDCG 2020-6", "MEDDEV 2.7/1 rev.4"],
    "warnings": [
      "走等同器械路径但未见「等同器械数据访问权/合同」——Annex XIV Part A 要求充分访问权，缺失属重大缺陷",
      "CER 要素缺失：临床评价计划（CEP）、…、更新计划与日期——技术评审高频发补点"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "cer-equivalence-check@MedXpert",
                "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}
}
```
（`obligations` / `notes` / `warnings` 第 2 条数组字段值逐字未改，此处折叠。）

三档 rc 实测：十项全 `yes` → rc=0；`--is_equivalent yes`（其余缺省）→ rc=1（访问权缺失 + 要素缺失，从严提示）；`--has_plan yes`（缺 `--is_equivalent`）→ rc=2。

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明；结论须人工复核，最终以监管机构/公告机构认定为准。
- **输入不足时从严提示**：要素缺项与等同器械数据访问权缺失均在 `warnings` 中明示（`rc=1`），不静默按「要素齐全」输出。
- 不覆盖特殊情形（创新器械、药械组合、边界产品、纳米材料等），此类须走官方界定程序。
- 规则版本会变；**条款号已给出，请以官方最新文本核对**。
- 输出为起始清单，**不替代产品技术要求、适用标准清单与专业评价者判断**。

## 六、理论依据

有证须可溯——等同不是「差不多」，而是三条证据链条条可追。

> 域站位件：`TH-MED-009` · LGD 理论总账 REGISTRY · 医疗器械全链路治理（有籍 · 有证 · 有门禁）

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

诺康@MED 域首席发声人 · TH-MED-009 · © 2026 MedXpert · MIT License
本内容由 AI 辅助生成（非自然人），署名机构承担出品责任。

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `cer-equivalence-check.py` | **MIT** |
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
