---
name: md-classification-route
slug: md-classification-route
title: 医疗器械分类与注册路径初判器
displayName: 医疗器械分类与注册路径初判器
display_name: 医疗器械分类与注册路径初判器
display_name_en: MD Classification & Registration Route Screener
version: 1.0.0
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: 注册老炮@MedXpert
copyright: MedXpert
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","医疗器械分类与注册路径初判器","判定器","TH-MED-006","决策支持"]
description: "器械该按几类报、走哪条路——判错一次，整套资料重做。分类是多市场准入的第一块多米诺骨牌。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (md-classification-route). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
---

![LGD-aligned MED 医疗](https://medxpert.cn/badge/directions/svg/lgd-aligned-med-cn.svg)
![LGD 有籍 Registered](https://medxpert.cn/badge/laws/svg/lgd-registered-cn.svg)
![LGD 有证 Evidenced](https://medxpert.cn/badge/laws/svg/lgd-evidenced-cn.svg)
![LGD 有门禁 Gated](https://medxpert.cn/badge/laws/svg/lgd-gated-cn.svg)
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械分类与注册路径初判器

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。输出请人工复核，正式结论须以主管部门决定与官方最新文件为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

> 🌐 **在线版与家族合集**
> - 医械注册知识库（免费公开层）：https://medxpert.cn/knowledge/
> - 技能索引页：https://medxpert.cn/skills/
> - 官网首页：https://medxpert.cn/

## 一、痛点

器械该按几类报、走哪条路——判错一次，整套资料重做。分类是多市场准入的第一块多米诺骨牌。

## 二、这是什么

一个**零依赖、确定性输出**的判定器。你把已知条件以参数传入，它按公开规则源给出结构化判定 + 义务清单 + 风险提示，输出 JSON IR（机器可读），可直接嵌入你自己的流程。

- **零依赖**：仅用 Python 标准库，无第三方包、无网络请求、无 API Key。
- **确定性**：同一输入永远同一输出（无随机、无模型调用）。
- **可回溯**：每条结论附规则源条款号，便于人工核对。
- **离线可用**：可在内网、断网、老电脑上运行。

## 三、判定核心

| 项 | 说明 |
|---|---|
| 规则源 | `EU MDR (EU) 2017/745 Annex VIII /《医疗器械分类目录》/ FDA 21 CFR 860` |
| 输出 | JSON IR（`result` + `rc` + `error_code` + `aigc_mark`） |
| 错误码 | `E_INPUT_MISSING` 参数不足 / `E_ENUM_INVALID` 枚举非法 / `E_RUNTIME` 其他 |
| 退出码 | `rc=0` 判定完成；`rc=1` 完成但带风险提示；`rc=2` 输入不足或非法 |

## 四、用法

```bash
python md-classification-route.py --demo                     # 跑内置冒烟案例（推荐先跑这个）
python md-classification-route.py --json <你的参数...>        # 正式判定
```

可用参数：`--market / --invasive / --duration / --active / --implant / --contact / --software`

## 四A、真机输出（实跑节选）
> 实跑命令 `python md-classification-route.py --market eu --invasive no --software yes`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "md-classification-route",
  "version": "1.0.0",
  "input": {"market": "eu", "invasive": "no", "duration": null, "active": null, "implant": null, "contact": null, "software": "yes"},
  "result": {
    "market": "eu",
    "eu_class_hint": "IIa（推定，多数情形）",
    "eu_rule": "MDR Annex VIII Rule 11（提供诊断/治疗决策信息的软件）",
    "cn_class_hint": "一类或二类（推定）",
    "us_class_hint": "Class I / II（推定，多为 510(k) 豁免或 510(k)）",
    "next_step": "MDR 技术文件 + 公告机构（NB）符合性评定；III 类须 NB + （如适用）临床评价",
    "obligations": ["…3 条（类别核对 / 初判不适用特殊情形 / 三市场类别不可互推）"],
    "notes": ["…3 条（初判线索 / 22 条规则覆盖范围 / 中国分类界定）"],
    "evidence": ["MDR (EU) 2017/745 Annex VIII", "《医疗器械分类目录》", "FDA 21 CFR 860"],
    "warnings": [
      "输入不完整：软件器械未提供 --contact——若软件输出用于危及生命/不可逆损害情形的诊断或治疗决策（接触中枢神经/心脏等），按 MDR Rule 11 可能升至 III 类（推定）；当前按 IIa（推定，多数情形）输出，建议补参后复核。"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "md-classification-route@MedXpert",
                "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}
}
```
（`all_markets` 数组字段值同上、逐字未改，此处折叠。）

三档 rc 实测：`--market cn --invasive no --active yes` → rc=0；`--market eu --invasive yes --duration long_term --implant yes` → rc=1（最高风险档提示）；`--market jp --active yes` → rc=2（枚举非法）。

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明；结论须人工复核，最终以监管机构认定为准。
- **输入不足时从严提示**：软件器械缺 `--contact` 时提示可能按 Rule 11 升至 III 类；长期侵入器械缺 `--implant` 时提示可能按 Rule 8 归 III 类（均在 `warnings`，`rc=1`）——不静默按宽松档输出。
- 不覆盖特殊情形（创新器械、药械组合、边界产品、纳米材料等），此类须走官方界定程序。
- 规则版本会变；**条款号已给出，请以官方最新文本核对**。
- 输出为起始清单，**不替代产品技术要求、适用标准清单与专业评价者判断**。

## 六、理论依据

有籍而后有据——先给器械「落籍」（类别与路径），一切合规义务才有锚点。

> 域站位件：`TH-MED-006` · LGD 理论总账 REGISTRY · 医疗器械全链路治理（有籍 · 有证 · 有门禁）

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

诺康@MED 域首席发声人 · TH-MED-006 · © 2026 MedXpert · MIT License
本内容由 AI 辅助生成（非自然人），署名机构承担出品责任。

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `md-classification-route.py` | **MIT** |
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
