---
name: fin-ai-classifier
slug: fin-ai-classifier
displayName: 金融 AI 应用分级判定器
version: 1.0.1
category: it-ops-security
display_name: 金融 AI 应用分级判定器
title: 金融 AI 应用分级判定器
author: 诺丰(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 金融 AI 应用分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-FIN-002域。
tags: [合规, 判定器, TH-FIN-002, fin-ai-classifier]
description_zh: "金融 AI 应用分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-FIN-002域。"
description_en: "Financial AI application tiering determination tool: zero-dependency decision support with JSON IR output (domain TH-FIN-002)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 金融 AI 应用分级判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见。输出请人工复核。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向`（分级口径待人工核对，见下方清单；以官方最新监管口径为准）。
- **输入不足时从严推定**：缺 `autonomy` / `impact` 时，取「可能等级中义务最重者」作为结论，并在 `warnings` 中明示可能区间与补参建议（`rc=1`）——**不静默按 I 级（低风险）输出**。缺省参数不影响结论时（如 `impact=low` 下各自主度均为 I 级）不额外告警。
- **不静默吞掉非法输入**：`autonomy` 非 full/human_in_loop/info、`impact` 非 high/mid/low、`target` 非 consumer/institution → 门禁错误（`rc=2`）。
- **不覆盖**：持牌资质判定、具体报送材料清单、算法备案的操作流程；这些须另行判定。

## 三、用法
```bash
python fin-ai-classifier.py                                     # 无参数 → 从严推定 III 级，rc=1
python fin-ai-classifier.py --autonomy info --impact low        # 参数完整 → I 级，rc=0
python fin-ai-classifier.py --autonomy full --impact high --target consumer   # III 级，rc=1
python fin-ai-classifier.py --autonomy full --impact extreme    # 非法输入 → rc=2
python fin-ai-classifier.py --demo                              # 跑内置冒烟案例（2 例）
```
参数：`autonomy / impact`（关键分级参数，缺省按从严推定）+ `target`（可选）。

## 四、真机输出（无参数单次实跑原文）
> 实跑命令 `python fin-ai-classifier.py`（2026-09-26，Python 3.13.12）。**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "fin-ai-classifier",
  "input": {"autonomy": null, "impact": null, "target": null},
  "result": {
    "grade": "III 级（高风险）",
    "obligations": ["算法备案", "人工兜底 + 可解释", "模型与数据合规审计", "监管报送"],
    "evidence": ["TH-FIN-002 母版", "金融AI监管导向"],
    "warnings": [
      "输入不完整：未提供 autonomy / impact；建议补齐后复核。",
      "分级不确定（可能区间 I 级（低风险）～III 级（高风险））：已按从严推定取『III 级（高风险）』（义务最重者），实际等级可能更宽松；请补齐参数后复核。",
      "全自动高影响面向消费者——须严格备案与人工兜底，禁止'AI 荐股/放贷'无资质经营"
    ]
  },
  "rc": 1
}
```

`--demo` 两案例结论（同一命令实测）：`{autonomy:full, impact:high, target:consumer}` → III 级 / `rc=1`；`{autonomy:info, impact:low}` → I 级 / `rc=0`。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--autonomy info --impact low` → I 级；`--autonomy human_in_loop --impact mid` → II 级 |
| `1` | 完成但带风险提示（`warnings`） | `autonomy`/`impact` 缺省按从严推定（无参数）；或判定为 III 级须严格备案与人工兜底 |
| `2` | 输入非法，无法判定 | `autonomy` 非 full/human_in_loop/info；`impact` 非 high/mid/low；`target` 非 consumer/institution |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：什么都不给会怎样？ A：按从严推定取「III 级（高风险）」（义务最重者），`warnings` 明示可能区间 I～III 级与补参建议，`rc=1`；不会静默按 I 级输出。
- Q：规则过期怎么办？ A：以官方最新监管口径为准，本工具附规则源便于核对。

## 理论依据
金融的自治须有级——分级即把'AI 能否替你做决定'钉进监管坐标。
域站位件：TH-FIN-002。

## 条款号待人工核对清单
| 条款 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| TH-FIN-002 母版 | I/II/III 级分级框架（FDA SaMD 分级思维平移金融）的规则来源 | 待人工核对 |
| 'full + high → III 级' 口径 | 最高级触发条件（待与官方监管口径核对） | 待人工核对 |
| 'human_in_loop + high/mid → II 级' 口径 | 中风险级触发条件 | 待人工核对 |
| '算法备案（依舆论属性）' 口径 | II 级义务引用（待与《互联网信息服务算法推荐管理规定》核对） | 待人工核对 |
| '禁止 AI 荐股/放贷无资质经营' 口径 | III 级告警依据（待与金融持牌经营规则核对） | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现，未经人工核对不改动。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- FIN 域速查页：（地址待补）

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
| 代码 | `fin-ai-classifier.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `fin-ai-classifier.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺丰@FIN 域首席发声人 · TH-FIN-002 · SynomosAI（AI 辅助生成，非自然人）
