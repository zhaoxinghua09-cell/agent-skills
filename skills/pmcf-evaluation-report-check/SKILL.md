---
name: pmcf-evaluation-report-check
slug: pmcf-evaluation-report-check
title: PMCF 评价报告完整性检查器
displayName: PMCF 评价报告完整性检查器
display_name: PMCF 评价报告完整性检查器
display_name_en: PMCF Evaluation Report Completeness Checker
version: 1.0.0
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: 注册老炮@MedXpert
copyright: MedXpert
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","PMCF 评价报告完整性检查器","判定器","TH-MED-008","决策支持"]
description: "计划做完了，报告交上去还是被退——少一节「所采取措施」，或少一次年度周期，就得重来。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (pmcf-evaluation-report-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
description_zh: "计划做完了，报告交上去还是被退——少一节「所采取措施」，或少一次年度周期，就得重来。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
classification:
  internal: ["主轴1 医械合规咨询"]
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "development", "search"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD-aligned MED 医疗](https://medxpert.cn/badge/directions/svg/lgd-aligned-med-cn.svg)
![LGD 有籍 Registered](https://medxpert.cn/badge/laws/svg/lgd-registered-cn.svg)
![LGD 有证 Evidenced](https://medxpert.cn/badge/laws/svg/lgd-evidenced-cn.svg)
![LGD 有门禁 Gated](https://medxpert.cn/badge/laws/svg/lgd-gated-cn.svg)
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# PMCF 评价报告完整性检查器

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。输出请人工复核，正式结论须以主管部门决定与官方最新文件为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

> 🌐 **在线版与家族合集**
> - 医械注册知识库（免费公开层）：https://medxpert.cn/knowledge/
> - 技能索引页：https://medxpert.cn/skills/
> - 官网首页：https://medxpert.cn/

## 一、痛点

计划做完了，报告交上去还是被退——少一节「所采取措施」，或少一次年度周期，就得重来。

## 二、这是什么

一个**零依赖、确定性输出**的判定器。你把已知条件以参数传入，它按公开规则源给出结构化判定 + 义务清单 + 风险提示，输出 JSON IR（机器可读），可直接嵌入你自己的流程。

- **零依赖**：仅用 Python 标准库，无第三方包、无网络请求、无 API Key。
- **确定性**：同一输入永远同一输出（无随机、无模型调用）。
- **可回溯**：每条结论附规则源条款号，便于人工核对。
- **离线可用**：可在内网、断网、老电脑上运行。

## 三、判定核心

| 项 | 说明 |
|---|---|
| 规则源 | `MDR (EU) 2017/745 Annex XIV Part B + Art 86 / MDCG 2020-7、2020-8` |
| 输出 | JSON IR（`result` + `rc` + `error_code` + `aigc_mark`） |
| 错误码 | `E_INPUT_MISSING` 参数不足 / `E_ENUM_INVALID` 枚举非法 / `E_RUNTIME` 其他 |
| 退出码 | `rc=0` 判定完成；`rc=1` 完成但带风险提示；`rc=2` 输入不足或非法 |

## 四、用法

```bash
python pmcf-evaluation-report-check.py --demo                     # 跑内置冒烟案例（推荐先跑这个）
python pmcf-evaluation-report-check.py --json <你的参数...>        # 正式判定
```

可用参数：`--device_class / --implant / --has_scope / --has_method / --has_data / --has_conclusions / --has_actions / --has_signoff`

## 四A、真机输出（实跑节选）
> 实跑命令 `python pmcf-evaluation-report-check.py --device_class IIb`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "pmcf-evaluation-report-check",
  "version": "1.0.0",
  "input": {"device_class": "IIb", "implant": null, "has_scope": null, "has_method": null,
            "has_data": null, "has_conclusions": null, "has_actions": null, "has_signoff": null},
  "result": {
    "device_class": "IIb",
    "report_period": "至少每 2 年一次，必要时提高频次",
    "period_basis": "MDR Art 86：IIa 类及其他 IIb 类器械",
    "missing_sections": ["评价范围与适用器械标识", "数据来源与采集方法（含 PMCF 计划引用）", "数据汇总与分析",
                         "结论与对受益-风险比的影响", "所采取措施 / CAPA / 更新触发", "评价人资质、日期与签署"],
    "complete": false,
    "obligations": ["…3 条（与 PMCF 计划对应 / 不得超期 / 受益-风险结论）"],
    "notes": ["…3 条（结构完整性核查 / 内容充分性超出能力 / 周期以法规原文为准）"],
    "evidence": ["MDR (EU) 2017/745 Annex XIV Part B", "MDR Art 86", "MDCG 2020-7", "MDCG 2020-8"],
    "warnings": [
      "报告要素缺失：评价范围与适用器械标识、…、评价人资质、日期与签署——提交前须补齐，否则易被公告机构发补",
      "未填写「所采取措施」——PMCF 的价值在于闭环，缺此节等同于无输出",
      "输入不完整：IIb 类器械未提供 --implant——若为植入类 IIb，按 MDR Art 86 须至少每年一次 PSUR（从严推定下的可能区间）；当前按非植入 IIb（至少每 2 年一次）输出，建议补参后复核。"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "pmcf-evaluation-report-check@MedXpert",
                "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}
}
```
（`missing_sections` / `obligations` / `notes` / `warnings` 第 1 条数组字段值逐字未改，此处折叠。）

三档 rc 实测：`--device_class IIa` + 六要素全 `yes` → rc=0；`--device_class IIb`（要素缺省）→ rc=1（要素缺失 + 从严提示）；`--device_class I` → rc=2（枚举非法）。

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明；结论须人工复核，最终以监管机构/公告机构认定为准。
- **输入不足时从严提示**：要素缺项与「IIb 植入类周期歧义」均在 `warnings` 中明示（`rc=1`），不静默按宽松周期输出。
- 不覆盖特殊情形（创新器械、药械组合、边界产品、纳米材料等），此类须走官方界定程序。
- 规则版本会变；**条款号已给出，请以官方最新文本核对**。
- 输出为起始清单，**不替代产品技术要求、适用标准清单与专业评价者判断**。

## 六、理论依据

有证必闭环——上市后数据不是交差，是把受益-风险比持续钉在证据上。

> 域站位件：`TH-MED-008` · LGD 理论总账 REGISTRY · 医疗器械全链路治理（有籍 · 有证 · 有门禁）

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

诺康@MED 域首席发声人 · TH-MED-008 · © 2026 MedXpert · MIT License
本内容由 AI 辅助生成（非自然人），署名机构承担出品责任。

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `pmcf-evaluation-report-check.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码（.py）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（理论文本保留所有权利）。** 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
