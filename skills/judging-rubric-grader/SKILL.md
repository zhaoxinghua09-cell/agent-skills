---
name: judging-rubric-grader
slug: judging-rubric-grader
displayName: 赛事评审打分器
version: 1.1.0
category: ai-agent
display_name: 赛事评审打分器
title: 赛事评审打分器
author: 诺律(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事评审打分器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-003域。
tags: [赛事, 判定器, TH-EVT-003, judging-rubric-grader]
description_zh: "赛事评审打分器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-003域。"
description_en: "Contest judging rubric scorer: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-003)."
classification:
  internal: ["主轴3 赛事与生态"]
  skillhub: ["community-events"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 赛事评审打分器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做赛事终裁；结论须人工复核。
- 规则源：`UIBC 评审规范（rubric 加权）`（以 UIBC 赛事章程最新版为准）。
- **输入不足时从严推定**：`scores` 缺少某维度分数时，从严按 **0 分**计（拉低总分），并在 `warnings` 中明示缺失维度与补参建议——**不静默按满分或跳过处理**；`criteria` 权重之和 ≠1 时亦给出 `warnings`（`rc=1`）。
- **不覆盖**：评委合议、申诉流程、作品安全性的整体背书；这些须另行处理。

## 三、用法
```bash
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.4},{"dim":"工程","weight":0.3},{"dim":"表达","weight":0.3}]' --scores '{"创新":90,"工程":85,"表达":80}'   # 参数完整且达标 → rc=0
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.5},{"dim":"合规","weight":0.5}]' --scores '{"创新":90}'                                                   # 缺维度分 → 从严按0计，rc=1
python judging-rubric-grader.py                                                                                                                                                 # 缺必填参数 → rc=2
python judging-rubric-grader.py --demo                                                                                                                                          # 跑内置冒烟案例（3 例）
```
参数：`criteria`（JSON 维度权重列表，必填）/ `scores`（JSON 各维度分数对象，必填）/ `pass_line`（达标线，默认 60）。必填缺失或 JSON 非法时 `rc=2`。

## 四、真机输出（--demo 第 3 例，逐字）
> 实跑命令 `python judging-rubric-grader.py --demo`（2026-09-26，Python 3.13.12）。以下为该例完整 JSON，**字段值逐字未改**。

```json
{
  "tool": "judging-rubric-grader",
  "input": {
    "criteria": "[{\"dim\":\"创新\",\"weight\":0.5},{\"dim\":\"合规\",\"weight\":0.5}]",
    "scores": "{\"创新\":90}",
    "pass_line": "60"
  },
  "result": {
    "total": 45.0,
    "grade": "D",
    "passed": false,
    "pass_line": 60.0,
    "per_dimension": [
      {"dim": "创新", "weight": 0.5, "score": 90.0, "weighted": 45.0},
      {"dim": "合规", "weight": 0.5, "score": 0.0, "weighted": 0.0}
    ],
    "warnings": [
      "以下维度未提供分数，从严按 0 分计（会拉低总分）：合规；请补齐 scores 中对应维度后复核。",
      "未达达标线（60.0）：机器门禁通过≠评审通过，建议复评或退回"
    ],
    "notes": ["…共 5 条，见源码 NOTES"],
    "evidence": ["UIBC 评审规范·rubric"]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "judging-rubric-grader@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（同一命令实测）：三维度齐备 85.5 分 → C（rc=0）/ 双维度未达标 45 分 → D（rc=1）/ 缺「合规」维度分 → 从严按 0 计（rc=1）。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 参数完整、权重和为 1、总分达标 |
| `1` | 完成但带风险提示（`warnings`） | 缺维度分从严按 0 计；权重和 ≠1；总分未达达标线 |
| `2` | 输入不足/输入非法，无法判定 | 缺 `criteria`/`scores`、JSON 非法、`scores` 非对象、`criteria` 为空列表 |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，以组委会认定为准。
- Q：某维度没给分会怎样？ A：从严按 0 分计并在 `warnings` 中明示（`rc=1`），不会静默跳过或按满分处理。
- Q：规则过期怎么办？ A：以 UIBC 章程最新版为准，本工具附规则源便于核对。

## 理论依据
评审须可被问责——rubric 加权即把'凭什么打分'写进可审计的记录。
域站位件：TH-EVT-003 · UIBC 赛事线。

## 条款号待人工核对清单
| 规则 | 用于什么判定 | 状态 |
|---|---|---|
| UIBC 评审规范·rubric | 加权总分与等级映射（S/A/B/C/D）的规则来源 | 待人工核对 |
| 等级断点 90/80/70/达标线 | 等级映射的取值 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现所引规则源，未经人工核对不改动。核对后如有变更，以 UIBC 章程最新版为准。

## 延伸阅读
- LGD 理论总账：https://medxpert.cn/theory（实测可达性待核）
- UIBC 赛事官网 / GitHub lgd-theory 仓库：（地址待补）

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `judging-rubric-grader.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码（.py）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（理论文本保留所有权利）。**

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `judging-rubric-grader.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺律@LAW 域首席发声人 · TH-EVT-003 · SynomosAI（AI 辅助生成，非自然人）
