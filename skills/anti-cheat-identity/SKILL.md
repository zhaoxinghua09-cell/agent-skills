---
name: anti-cheat-identity
slug: anti-cheat-identity
displayName: 赛事反作弊身份核验器
version: 1.1.1
category: ai-agent
display_name: 赛事反作弊身份核验器
title: 赛事反作弊身份核验器
author: 诺卫(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事反作弊身份核验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-004域。
tags: [赛事, 判定器, TH-EVT-004, anti-cheat-identity]
---

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 赛事反作弊身份核验器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做赛事终裁；结论须人工复核。
- 规则源：`UIBC 反作弊规范 + 通用学术诚信原则`（条款号待人工核对，见下方清单；以 UIBC 赛事章程最新版为准）。
- **不静默吞掉非法输入**：`submit_count / time_gap_min` 非数字或为负、`prev_env_hashes` 非 JSON 数组 → 门禁错误（`rc=2`），不按默认宽松值继续判定。
- **不覆盖**：作品查重、评审打分、赛题生成；这些由家族内其他判定器承担。

## 三、用法
```bash
python anti-cheat-identity.py --author_id teamA --env_hash abc123 --prev_env_hashes '["abc123"]' --submit_count 1 --time_gap_min 120   # 低风险 → rc=0
python anti-cheat-identity.py --author_id teamB --env_hash xyz999 --prev_env_hashes '["a1","a2","a3","a4","a5"]' --submit_count 8 --time_gap_min 3   # 高风险 → rc=1
python anti-cheat-identity.py --author_id teamC --env_hash h1 --submit_count abc   # 非法输入 → rc=2
python anti-cheat-identity.py --demo   # 跑内置冒烟案例（2 例）
```
参数：`author_id / env_hash`（必填）+ `prev_env_hashes / submit_count / time_gap_min`（可选）。

## 四、真机输出（--demo 第 2 例节选）
> 实跑命令 `python anti-cheat-identity.py --demo`（2026-09-26，Python 3.13.12）。**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "anti-cheat-identity",
  "input": {
    "author_id": "teamB",
    "env_hash": "xyz999",
    "prev_env_hashes": "[\"a1\",\"a2\",\"a3\",\"a4\",\"a5\"]",
    "submit_count": "8",
    "time_gap_min": "3"
  },
  "result": {
    "author_id": "teamB",
    "risk_level": "high",
    "flags": [
      "环境指纹与历史不一致（疑似换设备/环境）",
      "历史环境指纹过多（疑似多环境轮换）",
      "同作者提交次数过高(8)",
      "相邻提交间隔过短(3分钟)"
    ],
    "advice": "高风险：冻结提交通道并人工核查（冻结≠撤销，处置记录须留痕）",
    "warnings": ["…与 flags 相同 4 条"]
  },
  "rc": 1
}
```

两案例结论（同一命令实测）：`teamA` → low / `rc=0`；`teamB` → high / `rc=1`。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--author_id teamA --env_hash abc123 --prev_env_hashes '["abc123"]' --submit_count 1 --time_gap_min 120` → low |
| `1` | 完成但带风险提示（`warnings` 非空） | 环境指纹不一致 / 历史指纹过多 / 提交次数过高 / 间隔过短（任一命中） |
| `2` | 输入不足/输入非法，无法判定 | 缺 `author_id` 或 `env_hash`；`submit_count` 非整数或 <1；`time_gap_min` 非数字或为负；`prev_env_hashes` 非 JSON 数组 |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，以组委会认定为准。
- Q：非法输入会怎样？ A：门禁拒绝（`rc=2`）并说明原因；不会静默按默认宽松值继续判定。
- Q：规则过期怎么办？ A：以 UIBC 章程最新版为准，本工具附规则源便于核对。

## 理论依据
可信始于身份——环境一致性核验即把'谁在参赛'锁进防作弊的围栏。
域站位件：TH-EVT-004 · UIBC 赛事线。

## 规则源待人工核对清单
| 规则 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| UIBC 反作弊规范 | 环境指纹一致性 / 多环境轮换的判定口径 | 待人工核对 |
| 阈值：历史指纹 >3 个 | 「疑似多环境轮换」触发线 | 待人工核对 |
| 阈值：同作者提交 >5 次 | 「提交次数过高」触发线 | 待人工核对 |
| 阈值：相邻提交间隔 <10 分钟 | 「间隔过短」触发线 | 待人工核对 |
| 分级处置口径 low/mid/high | 放行 / 人工抽检 / 冻结的处置建议 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表阈值沿用原实现，未经人工核对不改动。核对后如有变更，以 UIBC 章程最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/anti-cheat-identity
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- 赛事线速查页：（地址待补）

## 家族合集
| 赛事环节 | 工具 | 大使 | 目录 |
|---|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/contest-submission-portal |
| 赛题生成 | problem-set-generator | 诺声 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/problem-set-generator |
| 评审打分 | judging-rubric-grader | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/judging-rubric-grader |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/anti-cheat-identity |
| 作品查重 | originality-check | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/originality-check |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `anti-cheat-identity.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `anti-cheat-identity.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺卫@UAS/安全域首席发声人 · TH-EVT-004 · SynomosAI（AI 辅助生成，非自然人）
