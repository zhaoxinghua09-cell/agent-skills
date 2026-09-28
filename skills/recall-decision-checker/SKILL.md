---
name: recall-decision-checker
slug: recall-decision-checker
displayName: 医疗器械召回级别判定器
version: 1.0.0
category: it-ops-security
display_name: 医疗器械召回级别判定器
title: 医疗器械召回级别判定器
author: 诺康(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械召回级别判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-003域（医疗器械全链路）。
tags: [医疗器械, 合规, 判定器, TH-MED-003, recall-decision-checker]
description_zh: "医疗器械召回级别判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-003域（医疗器械全链路）。"
description_en: "Medical device recall-level determination tool: zero-dependency decision support with JSON IR output (domain TH-MED-003, full device chain)."
classification:
  internal: ["主轴1 医械合规咨询"]
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械召回级别判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成医疗器械合规结论或法律/法规意见。输出请人工复核，最终以监管机构（NMPA/省局）认定为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 合规与免责声明（B 级 · YMYL 影响生命健康类）
- 本工具输出为**决策支持**，不构成注册、召回、不良事件报告等官方结论；正式结论须以主管部门（NMPA/省局）书面决定及官方最新条文为准。
- 规则源：`《医疗器械召回管理办法》(总局令 第29号)`，请以官方正式文本核对。
- 不得依据本工具输出直接做出临床、注册或召回决策。

## 一、痛点
医疗器械全链路规则白纸黑字但散落多份文件，企业自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见、不出具合规证明；结论须人工复核，最终以监管机构认定为准。
- 规则源：`《医疗器械召回管理办法》(总局令 第29号)`（以官方最新文本为准）。
- **输入不足时从严提示**：`use_phase=in_use/sold` 时在 `warnings` 中明示通知范围还须覆盖经营企业与使用单位、已使用部分须按召回计划评估（`rc=1`）——不静默略过流通/使用环节义务。
- **不覆盖**：召回计划的具体制定与实施、与省局的报告系统操作、境外主管当局的同步申报流程；这些须另行判定。

## 三、用法
```bash
python recall-decision-checker.py --harm_level severe                    # 一级召回，1 日内，rc=1
python recall-decision-checker.py --harm_level reversible                # 二级召回，3 日内，rc=0
python recall-decision-checker.py --harm_level severe --use_phase sold   # 已流通 → 通知范围提示，rc=1
python recall-decision-checker.py --demo                                 # 跑内置冒烟案例
```
参数：`harm_level`（severe/reversible/none，必填）/ `use_phase`（on_market/in_use/sold，可选）；枚举值非法拒绝判定（`rc=2`）。

## 四、真机输出（实跑节选）
> 实跑命令 `python recall-decision-checker.py --harm_level severe --use_phase sold`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "recall-decision-checker",
  "version": "1.0.0",
  "input": {"harm_level": "severe", "use_phase": "sold"},
  "result": {
    "recall_level": "一级（使用该器械可能或已经引起严重健康危害）",
    "notify_within_days": 1,
    "obligations": ["1 日内通知到有关单位", "启动一级召回", "向省局报告"],
    "notes": ["召回级别随危害严重程度与可逆性判定", "境外召回须同步上报", "时限以官方最新规定为准"],
    "evidence": ["医疗器械召回管理办法 第29号"],
    "warnings": [
      "一级召回为最高级——须立即控制流通与使用",
      "use_phase=sold：器械已进入使用/流通环节——召回通知范围还须覆盖经营企业与使用单位，已植入/已使用部分按召回计划评估随访与处置（当前不改变召回级别判定）。"
    ]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "recall-decision-checker@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（`--demo` 同命令实测）：`{"harm_level":"severe"}` → 一级（1 日内，rc=1）/ `{"harm_level":"reversible"}` → 二级（3 日内，rc=0）/ `{"harm_level":"none"}` → 三级（7 日内，rc=0）。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--harm_level reversible`；`--harm_level none` |
| `1` | 完成但带风险提示（warnings） | `--harm_level severe`（最高级提示）；或 `--use_phase in_use/sold`（流通/使用环节提示） |
| `2` | 输入不足/输入非法，无法判定 | 缺 harm_level；或枚举值非法（如 `--harm_level garbage`） |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源条款号便于核对。
- Q：参数写错会怎样？ A：枚举非法拒绝判定（rc=2），不会把非法输入当「三级」静默处理。

## 理论依据
召回不是终点而是担当——分级即把'危害'按可逆性分层处置。
域站位件：TH-MED-003 · 理论总账 REGISTRY · 医疗器械全链路。

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
| 代码 | `recall-decision-checker.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码（.py）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（理论文本保留所有权利）。** 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```

---
诺康@MED 域首席发声人 · TH-MED-003 · SynomosAI（AI 辅助生成，非自然人）
