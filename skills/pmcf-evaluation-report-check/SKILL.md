---
name: pmcf-evaluation-report-check
slug: pmcf-evaluation-report-check
title: PMCF 评价报告完整性检查器
displayName: PMCF 评价报告完整性检查器
display_name: PMCF 评价报告完整性检查器
display_name_en: PMCF Evaluation Report Completeness Checker
version: 1.0.0
license: MIT
author: 注册老炮@MedXpert
copyright: MedXpert
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","PMCF 评价报告完整性检查器","判定器","TH-MED-008","决策支持"]
description: "计划做完了，报告交上去还是被退——少一节「所采取措施」，或少一次年度周期，就得重来。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (pmcf-evaluation-report-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
---

![LGD-aligned MED 医疗](https://medxpert.cn/badge/directions/svg/lgd-aligned-med-cn.svg)
![LGD 有籍 Registered](https://medxpert.cn/badge/laws/svg/lgd-registered-cn.svg)
![LGD 有证 Evidenced](https://medxpert.cn/badge/laws/svg/lgd-evidenced-cn.svg)
![LGD 有门禁 Gated](https://medxpert.cn/badge/laws/svg/lgd-gated-cn.svg)
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# PMCF 评价报告完整性检查器

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。正式结论须以主管部门决定与官方最新文件为准。**核验日期：2026-09-12**。

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

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明。
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
