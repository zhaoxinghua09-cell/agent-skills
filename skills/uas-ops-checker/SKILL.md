---
name: uas-ops-checker
slug: uas-ops-checker
displayName: 无人机运营合规分类判定器
version: 1.0.0
category: it-ops-security
display_name: 无人机运营合规分类判定器
title: 无人机运营合规分类判定器
author: 诺卫(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
compatibility: Cross-platform; zero external dependencies (stdlib only)
metadata: {dependencies: "none"}
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 无人机运营合规分类判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-UAS-001域。
tags: [合规, 判定器, TH-UAS-001, uas-ops-checker]
description_zh: "无人机运营合规分类判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-UAS-001域。"
description_en: "Drone operation compliance classification determination tool: zero-dependency decision support with JSON IR output (domain TH-UAS-001)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 无人机运营合规分类判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见，也不构成任何合规证明。输出请人工复核，并以主管部门认定为准。
> 文本核验日期：2026-09-26（本包文本自查日期）· 条款文本以官方最新发布为准 · 官方文本直达链接：（地址待补）

## 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`《无人驾驶航空器飞行管理暂行条例》(国务院令761号,2024-01-01施行) 第6/12/16/31/32条 + CCAR-92`（条款号待人工核对，见下表；一律以官方最新文本为准）。
- **输入不足时从严推定**：只给一个重量参数时，取「可能等级中义务最重者」作为结论，并在 `warnings` 中明示可能区间与补参建议（`rc=1`）——**不静默按宽松等级输出**。
- **不覆盖**：空域属性（适飞/管制）、运营主体资质、保险安排、涉外与商业运营的额外审查项；这些须另行判定。

## 三、用法
```bash
python uas-ops-checker.py --mtow 5                    # 仅给最大起飞重量 → 从严推定，rc=1
python uas-ops-checker.py --mtow 5 --empty_weight 4   # 参数完整 → 轻型，rc=0
python uas-ops-checker.py --demo                      # 跑内置冒烟案例（3 例）
```
参数：`mtow`（最大起飞重量 kg）/ `empty_weight`（空机重量 kg）；至少给一个。

## 四、真机输出（--demo 第 2 例节选）
> 实跑命令 `python uas-ops-checker.py --demo`（2026-09-26，Python 3.13.14）。为便于阅读，数组已折行压缩；**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "uas-ops-checker",
  "input": {"mtow": "5"},
  "result": {
    "grade": "小型",
    "grade_basis": "从严推定（输入不完整）",
    "possible_grades": ["微型", "轻型", "小型"],
    "obligations": ["操控员执照（视具体机型）", "实名登记", "强制责任保险", "在适飞空域外飞行需申请"],
    "evidence": ["暂行条例 第6条", "暂行条例 第16条", "CCAR-92"],
    "notes": ["…共 5 条，见源码 NOTES"],
    "warnings": [
      "输入不完整：仅提供单一重量参数（缺 empty_weight）；官方分类同时使用最大起飞重量与空机重量，建议补齐另一参数后复核。",
      "分类不确定（可能等级区间 微型～小型）：已按从严推定取『小型』（义务最重者），实际等级可能更宽松；请补齐参数后复核。",
      "该等级不适用微型/轻型的『适飞空域内免执照』简化路径：实际合规义务还取决于空域属性、运营主体资质与保险安排；涉管制空域、商业运营或涉外运营的须另行申请与审查（本工具不含该项判定）。"
    ]
  },
  "rc": 1,
  "clause_review_checklist": ["…共 7 条，逐条给出条款号与用途，见输出原文"],
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "uas-ops-checker@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（同一命令实测）：`{"mtow":"0.2"}` → 微型 / `{"mtow":"5"}` → 小型（从严推定，可能区间 微型～小型）/ `{"mtow":"120"}` → 中型（可能区间 微型～中型）；三者 `rc` 均为 1（均属「完成但带风险提示」）。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 参数完整且等级为微型/轻型：`--mtow 5 --empty_weight 4` → 轻型 |
| `1` | 完成但带风险提示（`warnings`） | 输入不完整按从严推定（`--mtow 5`）；或等级为小型/中型/大型需额外审查（`--mtow 120 --empty_weight 60`） |
| `2` | 输入不足/输入非法，无法判定 | 无参数、非数字、`empty_weight > mtow`、非正数 |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：只给一个重量参数会怎样？ A：按从严推定（取可能等级中义务最重者）出结论，并在 `warnings` 中给出可能区间与补参建议，`rc=1`；不会静默按宽松等级输出。
- Q：规则过期怎么办？ A：以官方最新条文为准；输出中的 `clause_review_checklist` 逐条给出「哪一条款用于什么判定」，便于人工核对。
- Q：条例里的识别信息报送 / 飞行动态上传，算本工具所说的「证据」吗？ A：不算。依 LGD 证据语义界定：Evidence（证据）＝治理状态转换的**可验证依据**，**非行为日志**；报送与动态上传属**行为日志**，不等同于本体系所称 Evidence。
- Q：`evidence` 字段是什么？ A：是**规则出处（条款依据）**，即该等级所引用的条款清单，不是运营行为记录。

## 理论依据
凡自治之物必先有籍、有证、有门禁——无人机分类即空中治理的出生登记。
- 本工具输出的是**分类判定依据**（规则出处清晰、可复核）。依 LGD 证据语义界定：**Evidence（证据）＝治理状态转换的可验证依据，非行为日志**；识别信息报送 / 飞行动态上传属**行为日志**，本工具不把日志当证据。
- 域站位件：TH-UAS-001 · 理论总账 REGISTRY（在线地址待补，实测 `medxpert.cn/theory` 不可达）。

## 条款号待人工核对清单
| 条款 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| 暂行条例 第6条 | 无人驾驶航空器分类（微型/轻型/小型/中型/大型）的规则来源 | 待人工核对 |
| 暂行条例 第12条 | 微型/轻型的实名登记与适飞空域（真高≤120m）内免执照义务 | 待人工核对 |
| 暂行条例 第16条 | 小型的执照/实名登记/责任保险义务（原实现引用，条号待核） | 待人工核对 |
| 暂行条例 第31条 / 第32条 | 中型/大型的运营合格证、适航与飞行活动申请义务 | 待人工核对 |
| CCAR-92 | 分类参数与运行要求（轻型/小型分支引用） | 待人工核对 |
| GB 45438-2025 | AIGC 标识字段 `aigc_mark` 的标注依据 | 待人工核对 |
| 阈值 0.25 / 4 / 7 / 15 / 25 / 150 (kg) | 分类级联判定的断点取值（空机重量与最大起飞重量） | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表条款号沿用原实现，未经人工核对不改动。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- UAS 域速查页：（地址待补）

## 家族合集
| 域 | 工具 | 大使 | 目录 |
|---|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker |
| AUT 驾驶 | aut-grade-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker |
| DAT 数据 | data-grade-checker | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker |
| BIO 生物 | hgrac-route-checker | 诺康 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/hgrac-route-checker |
| FIN 金融 | fin-ai-classifier | 诺丰 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier |
| LAW 法律 | evid-four-check | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `uas-ops-checker.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `uas-ops-checker.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺卫@UAS 域首席发声人 · TH-UAS-001 · SynomosAI（AI 辅助生成，非自然人）
