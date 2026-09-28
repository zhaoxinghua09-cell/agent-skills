---
name: data-grade-checker
slug: data-grade-checker
displayName: 数据分类分级判定器
version: 1.0.1
category: it-ops-security
display_name: 数据分类分级判定器
title: 数据分类分级判定器
author: 诺源(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 数据分类分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-DAT-001域。
tags: [合规, 判定器, TH-DAT-001, data-grade-checker]
---

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 数据分类分级判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见。输出请人工复核。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)`（标准号与分级口径待人工核对，见下方清单；以官方最新文本为准）。
- **输入不足时从严推定**：未说明 `core_interest`（或行业/规模缺失）时，取「可能等级中义务最重者」作为结论，并在 `warnings` 中明示可能区间与补参建议（`rc=1`）——**不静默按「一般数据」输出**。
- **不静默吞掉非法输入**：`core_interest / cross_border` 非 yes/no、`scale` 非 high/mid/low → 门禁错误（`rc=2`）。
- **不覆盖**：行业敏感数据目录的具体条目、个人信息维度分级、跨境传输的完整申报流程；这些须另行判定。

## 三、用法
```bash
python data-grade-checker.py                                              # 无参数 → 从严推定核心数据，rc=1
python data-grade-checker.py --industry retail --core_interest no --scale low   # 参数完整 → 一般数据，rc=0
python data-grade-checker.py --industry finance --core_interest no --scale high --cross_border yes   # 重要数据+出境 → rc=1
python data-grade-checker.py --industry retail --scale huge               # 非法输入 → rc=2
python data-grade-checker.py --demo                                       # 跑内置冒烟案例（3 例）
```
参数：`industry / core_interest / scale / cross_border`（均可选；关键分级参数缺省时按从严推定）。

## 四、真机输出（--demo 第 2 例节选）
> 实跑命令 `python data-grade-checker.py --demo`（2026-09-26，Python 3.13.12）。**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "data-grade-checker",
  "input": {"industry": "finance", "scale": "high"},
  "result": {
    "grade": "核心数据",
    "obligations": ["出境安全评估 + 审批", "最高级保护义务", "原则上不得出境"],
    "evidence": ["GB/T 43697-2024"],
    "warnings": [
      "输入不完整：未说明是否涉及国家核心利益（core_interest），该参数可触发最高级；建议补齐 core_interest / industry / scale 后复核。",
      "分级不确定（可能区间 重要数据～核心数据）：已按从严推定取『核心数据』（义务最重者），实际等级可能更宽松；请补齐参数后复核。"
    ]
  },
  "rc": 1
}
```

三案例结论（同一命令实测）：`{core_interest:yes}` → 核心数据 / `rc=0`；`{industry:finance, scale:high}` → 核心数据（从严推定，可能区间 重要～核心）/ `rc=1`；`{industry:retail}` → 核心数据（从严推定，可能区间 一般～核心）/ `rc=1`。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 参数完整且非出境：`--industry retail --core_interest no --scale low` → 一般数据 |
| `1` | 完成但带风险提示（`warnings`） | 分级参数不足按从严推定（无参数 / 仅给 industry）；或出境且非一般数据（`--industry finance --core_interest no --scale high --cross_border yes`） |
| `2` | 输入非法，无法判定 | `core_interest / cross_border` 非 yes/no；`scale` 非 high/mid/low（如 `--scale huge`） |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：什么都不给会怎样？ A：按从严推定取「核心数据」（义务最重者），`warnings` 明示可能区间 一般数据～核心数据 与补参建议，`rc=1`；不会静默按「一般数据」输出。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源便于核对。

## 理论依据
数据须有籍、有级、有门禁——分类分级即数字世界的产权登记。
域站位件：TH-DAT-001。

## 条款号待人工核对清单
| 条款 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| GB/T 43697-2024 | 数据分类分级（核心数据/重要数据/一般数据）的规则来源 | 待人工核对 |
| 行业敏感清单（finance/energy/transport/bio/health/geo/population/gov/key_infra） | 重要数据行业判定（原实现引用，待与官方附录核对） | 待人工核对 |
| 'core_interest=yes → 核心数据' 口径 | 最高级触发条件 | 待人工核对 |
| '跨部门按就高原则' 口径 | 多属性数据定级 | 待人工核对 |
| 出境路径（安全评估/标准合同/认证） | 出境场景告警依据 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现，未经人工核对不改动。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- DAT 域速查页：（地址待补）

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
| 代码 | `data-grade-checker.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `data-grade-checker.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺源@DAT 域首席发声人 · TH-DAT-001 · SynomosAI（AI 辅助生成，非自然人）
