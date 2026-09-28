---
name: contest-submission-portal
slug: contest-submission-portal
displayName: 赛事作品提交合规校验器
version: 1.1.1
category: ai-agent
display_name: 赛事作品提交合规校验器
title: 赛事作品提交合规校验器
author: 诺声(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事作品提交合规校验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-001域。
tags: [赛事, 判定器, TH-EVT-001, contest-submission-portal]
---

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 赛事作品提交合规校验器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做赛事终裁；结论须人工复核。
- 规则源：`UIBC 赛事提交规范（四规范·提交章）v0.1`（必交项与格式白名单沿自原实现，待人工核对，见下方清单；以 UIBC 赛事章程最新版为准）。
- **不静默放行未校验项**：未提供 `format` 时主文件格式白名单不做判定，`warnings` 明示「未校验」并给补参建议（`rc=1`）——不静默按通过输出。
- **不静默改判未知赛道**：`track` 取值非 code/theory/design → 门禁错误（`rc=2`），不套用假必交项清单。
- **不覆盖**：报名资格、评审打分、查重、反作弊；这些由家族内其他判定器承担。

## 三、用法
```bash
python contest-submission-portal.py --track code --files "submission.uibc,seal.json,aigc-declaration.md,RUN.md,attack-report.md" --format py   # 必交项齐 → rc=0
python contest-submission-portal.py --track code --files "solution.py,readme.md" --format exe   # 缺必交项+格式违规 → rc=1
python contest-submission-portal.py --track music --files "a.md" --format md                    # 未知赛道 → rc=2
python contest-submission-portal.py --demo                                                      # 跑内置冒烟案例（3 例）
```
参数：`track`（code/theory/design，必填）+ `files`（逗号分隔清单）+ `format`（主文件格式）。

## 四、真机输出（--demo 第 1 例节选）
> 实跑命令 `python contest-submission-portal.py --demo`（2026-09-26，Python 3.13.12）。**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "contest-submission-portal",
  "input": {
    "track": "code",
    "files": "submission.uibc,seal.json,aigc-declaration.md,RUN.md,attack-report.md",
    "format": "py"
  },
  "result": {
    "track": "code",
    "required": ["uibc-package", "seal", "aigc", "run"],
    "provided": ["submission.uibc", "seal.json", "aigc-declaration.md", "run.md", "attack-report.md"],
    "missing": [],
    "valid": true,
    "format_ok": true,
    "warnings": [],
    "notes": [
      "必交项已与 SUBMISSION.md v0.1（提交章）对齐；以赛事章程最新版为准",
      "攻击自述为加分项（进 failure corpus 候选）：已检测到 attack-report.md",
      "离线可复现为硬约束：禁止外部网络依赖"
    ],
    "evidence": ["UIBC 赛事提交规范·提交章 v0.1"]
  },
  "rc": 0
}
```

三案例结论（同一命令实测）：code 全齐 → `valid=true` / `rc=0`；code 缺项+exe → `valid=false` / `rc=1`；theory 带 example → `valid=true` / `rc=0`。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--track code --files "submission.uibc,seal.json,aigc-declaration.md,RUN.md" --format py` |
| `1` | 完成但带风险提示（`warnings`） | 缺必交项 / 主文件格式不在白名单 / 检出可执行二进制 / 未提供 `format` |
| `2` | 输入不足/输入非法，无法判定 | 缺 `track`；`track` 非 code/theory/design |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，以组委会认定为准。
- Q：不提供 format 会怎样？ A：格式白名单不做判定，`warnings` 明示「未校验」，`rc=1`；不会静默按通过输出。
- Q：规则过期怎么办？ A：以 UIBC 章程最新版为准，本工具附规则源便于核对。

## 理论依据
公平始于可核验的入口——提交校验即把'谁在参赛'钉进可信起点。
域站位件：TH-EVT-001 · UIBC 赛事线。

## 规则源待人工核对清单
| 规则 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| UIBC 赛事提交规范·提交章 v0.1 | 各赛道必交项清单的规则来源 | 待人工核对 |
| code 赛道必交项：.uibc 密封包 + seal.json + AIGC 声明 + RUN.md | code 赛道完整性校验 | 待人工核对 |
| theory 赛道必交项：论文级提案 + 最小可执行示例 | theory 赛道完整性校验（章程硬要求） | 待人工核对 |
| design 赛道必交项：落地方案 + 失败模式分析 | design 赛道完整性校验（章程硬要求） | 待人工核对 |
| 格式白名单：code=md,py,json / theory=+pdf / design=md,pdf,png,svg | 主文件格式校验 | 待人工核对 |
| 禁止可执行二进制（.exe/.dll/.bat/.ps1/.so/.bin） | 提交门禁直接退回 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现，未经人工核对不改动。核对后如有变更，以 UIBC 章程最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/contest-submission-portal
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
| 代码 | `contest-submission-portal.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `contest-submission-portal.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺声@赛事首席发声人 · TH-EVT-001 · SynomosAI（AI 辅助生成，非自然人）
