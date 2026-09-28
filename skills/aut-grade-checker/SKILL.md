---
name: aut-grade-checker
slug: aut-grade-checker
displayName: 车辆驾驶自动化等级判定器
version: 1.0.1
category: it-ops-security
display_name: 车辆驾驶自动化等级判定器
title: 车辆驾驶自动化等级判定器
author: 诺卫(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 车辆驾驶自动化等级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-AUT-001域。
tags: [合规, 判定器, TH-AUT-001, aut-grade-checker]
description_zh: "车辆驾驶自动化等级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-AUT-001域。"
description_en: "Vehicle driving-automation level determination tool: zero-dependency decision support with JSON IR output (domain TH-AUT-001)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 车辆驾驶自动化等级判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见。输出请人工复核。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`GB/T 40429-2021《汽车驾驶自动化分级》表1`（条款号/表号待人工核对，见下方清单；以官方最新文本为准）。
- **输入不足时从严推定**：缺 `odd_limited` / `takeover_needed` / `both_axes` 时，取「可能等级中义务最重者」作为结论，并在 `warnings` 中明示可能区间与补参建议（`rc=1`）——**不静默按宽松等级输出**。
- **不静默吞掉非法输入**：`dd / oedr` 取值超出 system/vehicle/driver、可选参数取值非 yes/no → 门禁错误（`rc=2`）。
- **不覆盖**：准入公告/型式批准、事故责任划分、地区性法规差异；这些须另行判定。

## 三、用法
```bash
python aut-grade-checker.py --dd system --oedr system                                      # 参数不足 → 从严推定 L5，rc=1
python aut-grade-checker.py --dd vehicle --oedr driver --both_axes yes                     # 参数完整 → L2，rc=0
python aut-grade-checker.py --dd system --oedr system --odd_limited yes --takeover_needed yes   # L3，rc=1（L3+ 告警）
python aut-grade-checker.py --dd banana --oedr system                                      # 非法输入 → rc=2
python aut-grade-checker.py --demo                                                         # 跑内置冒烟案例（2 例）
```
参数：`dd / oedr`（必填，vehicle 视作 system）+ `odd_limited / takeover_needed / both_axes`（可选，yes/no）。

## 四、真机输出（单次调用实跑原文）
> 实跑命令 `python aut-grade-checker.py --dd system --oedr system`（2026-09-26，Python 3.13.12）。**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "aut-grade-checker",
  "input": {"dd": "system", "oedr": "system", "odd_limited": null, "takeover_needed": null, "both_axes": null},
  "result": {
    "grade": "L5",
    "responsibility": "系统在所有ODD执行全部DD+OEDR，无限制",
    "obligations": ["L3+ 须明示分级与责任边界", "宣传不得超实际等级标注"],
    "evidence": ["GB/T 40429-2021 表1"],
    "warnings": [
      "输入不完整：odd_limited/takeover_needed 未提供（官方分级同时使用 ODD 限定与接管要求），建议补齐后复核。",
      "分类不确定（可能等级区间 L3～L5）：odd_limited/takeover_needed 参数不足，已按从严推定取『L5』（义务最重者），实际等级可能更宽松；请补齐参数后复核。",
      "L3+ 不得宣称'自动驾驶/L2.9'等误导级别（'L2.9级'乱象可直接据此判定）"
    ]
  },
  "rc": 1
}
```

`--demo` 两案例结论（同一命令实测）：`{dd:system, oedr:system, odd_limited:yes, takeover_needed:yes}` → L3 / `rc=1`；`{dd:vehicle, oedr:driver, both_axes:yes}` → L2 / `rc=0`。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--dd vehicle --oedr driver --both_axes yes` → L2；`--dd driver --oedr driver` → L0 |
| `1` | 完成但带风险提示（`warnings`） | 参数不足按从严推定（`--dd system --oedr system`）；或判定为 L3+ 需额外审查 |
| `2` | 输入不足/输入非法，无法判定 | 缺 `dd` 或 `oedr`；取值非法（如 `--dd banana`）；可选参数非 yes/no |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：只给 dd/oedr 会怎样？ A：按从严推定（取可能等级中义务最重者）出结论，并在 `warnings` 中给出可能区间与补参建议，`rc=1`；不会静默按宽松等级输出。
- Q：'L2.9 级'宣传怎么判？ A：L3+ 判定自带告警：不得宣称'自动驾驶/L2.9'等误导级别。

## 理论依据
自治的边界须被标注——分级即把'谁在开车'写进责任契约。
域站位件：TH-AUT-001。

## 条款号待人工核对清单
| 条款 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| GB/T 40429-2021 表1 | 0-5 级分级判定（DD/OEDR/ODD/接管四要素）的规则来源 | 待人工核对 |
| 'vehicle 视作 system' 口径 | dd/oedr 参数归一化（原实现即有，语义见参数 help） | 待人工核对 |
| L3+ 告警口径 | 不得宣称'自动驾驶/L2.9'等误导级别的判定依据 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现，未经人工核对不改动。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- AUT 域速查页：（地址待补）

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
| 代码 | `aut-grade-checker.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

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

**本包补充（包级许可事实）**：本包代码文件 `aut-grade-checker.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺卫@AUT 域首席发声人 · TH-AUT-001 · SynomosAI（AI 辅助生成，非自然人）
