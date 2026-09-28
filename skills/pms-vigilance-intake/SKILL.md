---
name: pms-vigilance-intake
slug: pms-vigilance-intake
displayName: 医疗器械不良事件报告路径判定器
version: 1.0.0
category: it-ops-security
display_name: 医疗器械不良事件报告路径判定器
title: 医疗器械不良事件报告路径判定器
author: 诺康(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械不良事件报告路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-002域（医疗器械全链路）。
tags: [医疗器械, 合规, 判定器, TH-MED-002, pms-vigilance-intake]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械不良事件报告路径判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成医疗器械合规结论或法律/法规意见。输出请人工复核，最终以监管机构（NMPA/省局）认定为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 合规与免责声明（B 级 · YMYL 影响生命健康类）
- 本工具输出为**决策支持**，不构成注册、召回、不良事件报告等官方结论；正式结论须以主管部门（NMPA/省局）书面决定及官方最新条文为准。
- 规则源：`《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)`，请以官方正式文本核对。
- 不得依据本工具输出直接做出临床、注册或召回决策。

## 一、痛点
医疗器械全链路规则白纸黑字但散落多份文件，企业自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见、不出具合规证明；结论须人工复核，最终以监管机构认定为准。
- 规则源：`《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)`（以官方最新文本为准）。
- **输入不足时从严提示**：`severity=possible_serious` 但未提供 `event_type` 时，在 `warnings` 中明示「若属设计缺陷可能同样触发召回/再评价评估」（`rc=1`）——不静默按宽松路径输出。
- **不覆盖**：群体不良事件的完整应急处置流程、报告系统的实际账号操作、境外（FDA MDR / EU vigilance）报告路径；这些须另行判定。

## 三、用法
```bash
python pms-vigilance-intake.py --severity death               # 死亡 → 即时报告，rc=1（触发召回评估提示）
python pms-vigilance-intake.py --severity serious             # 严重伤害 → 20 日内，rc=0
python pms-vigilance-intake.py --severity possible_serious    # 缺 event_type → 从严提示，rc=1
python pms-vigilance-intake.py --demo                         # 跑内置冒烟案例
```
参数：`severity`（death/serious/possible_serious/other，必填）/ `event_type`（fault/use_error/design_defect，可选）；枚举值非法拒绝判定（`rc=2`）。

## 四、真机输出（实跑节选）
> 实跑命令 `python pms-vigilance-intake.py --severity possible_serious`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "pms-vigilance-intake",
  "version": "1.0.0",
  "input": {"severity": "possible_serious", "event_type": null},
  "result": {
    "report_path": "重点关注/定期汇总分析",
    "deadline": "按定期监测上报",
    "trigger_recall": false,
    "obligations": ["持有人为监测责任主体", "死亡/严重伤害事件须时限内上报", "开展风险评价与再评价"],
    "notes": ["群体不良事件→立即报告并采取紧急控制措施", "时限以官方最新规定为准", "本判定为报告路径建议，非监管结论"],
    "evidence": ["不良事件监测和再评价管理办法"],
    "warnings": [
      "输入不完整：severity=possible_serious 但未提供 event_type——若事件属 design_defect（设计缺陷），按从严推定可能同样触发召回/再评价评估；建议补参后复核（当前未计入 trigger_recall）。"
    ]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "pms-vigilance-intake@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（`--demo` 同命令实测）：`{"severity":"death"}` → 持有人立即报告（`trigger_recall=true`，rc=1）/ `{"severity":"serious"}` → 20 日内（rc=0）/ `{"severity":"possible_serious","event_type":"fault"}` → 定期汇总分析（rc=0）。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--severity serious`；或 `--severity possible_serious --event_type fault` |
| `1` | 完成但带风险提示（warnings） | `--severity death`（触发召回评估提示）；或 possible_serious 缺 event_type（从严提示） |
| `2` | 输入不足/输入非法，无法判定 | 缺 severity；或枚举值非法（如 `--severity garbage`） |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源条款号便于核对。
- Q：缺参数/参数写错会怎样？ A：缺 event_type 走从严提示（rc=1）；枚举非法拒绝判定（rc=2），不会把非法输入当「其他」静默处理。

## 理论依据
监测是信任的续约——不良事件上报即把'责任'钉进闭环。
域站位件：TH-MED-002 · 理论总账 REGISTRY · 医疗器械全链路。

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
| 代码 | `pms-vigilance-intake.py` | **MIT** |
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
诺康@MED 域首席发声人 · TH-MED-002 · SynomosAI（AI 辅助生成，非自然人）
