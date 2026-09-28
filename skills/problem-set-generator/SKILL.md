---
name: problem-set-generator
slug: problem-set-generator
displayName: 赛事赛题生成器
version: 1.1.0
category: ai-agent
display_name: 赛事赛题生成器
title: 赛事赛题生成器
author: 诺声(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事赛题生成器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-002域。
tags: [赛事, 判定器, TH-EVT-002, problem-set-generator]
description_zh: "赛事赛题生成器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-002域。"
description_en: "Contest problem-set generator: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-002)."
classification:
  internal: ["主轴3 赛事与生态"]
  skillhub: ["community-events"]
  clawhub: ["productivity", "data-analytics", "development"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 赛事赛题生成器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**（结构化赛题底稿生成），不做赛事终裁；每道赛题 `review_status` 均为「待审」，须组委会人工审核后方可发布。
- 规则源：`UIBC 赛题规范 + 赛季主题'迁移的判定与问责'`（以 UIBC 赛事章程最新版为准）。
- **输入不足/偏离时从严推定**：`difficulty` 取值非法、`count` 非法直接判非法（`rc=2`），**不静默按 mid/3 兜底**；自定义主题（非当前赛季主题）属赛题适配风险，给出 `warnings`（`rc=1`）——**不静默按赛季主题通过输出**。
- **诚实边界**：底稿为三场景模板，难度经「难度要求段」区分；同一底稿在不同难度下要求不同，发布前须组委会精修去重（输出 `notes` 已注明）。

## 三、用法
```bash
python problem-set-generator.py --difficulty hard --count 1                    # 赛季主题默认底稿 → rc=0
python problem-set-generator.py --theme 跨境数据判定 --difficulty easy --count 1   # 自定义主题 → 适配性告警，rc=1
python problem-set-generator.py --difficulty banana                            # 难度非法 → rc=2
python problem-set-generator.py --count 11                                     # 数量越界 → rc=2
python problem-set-generator.py --demo                                         # 跑内置冒烟案例（3 例）
```
参数：`theme`（赛题主题，缺省为当前赛季主题'迁移的判定与问责'）/ `difficulty`（easy/mid/hard，缺省 mid；非法时 `rc=2`）/ `count`（1-10，缺省 3；非法或越界时 `rc=2`）。

## 四、真机输出（--demo 第 3 例节选）
> 实跑命令 `python problem-set-generator.py --demo`（2026-09-26，Python 3.13.12）。为便于阅读，`spec` 字段已折叠；**其余字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "problem-set-generator",
  "input": {"theme": "跨境数据判定", "difficulty": "easy", "count": "1"},
  "result": {
    "theme": "跨境数据判定",
    "difficulty": "easy",
    "count": 1,
    "problems": [
      {
        "index": 1, "theme": "跨境数据判定", "difficulty": "入门",
        "spec": "…（底稿全文见源码，此处折叠）",
        "review_status": "待审（组委会人工审核后方可发布）",
        "ai_note": "本赛题由 AI 按规范辅助生成（GB 45438-2025），须经组委会审核后发布"
      }
    ],
    "warnings": [
      "自定义主题「跨境数据判定」非当前赛季主题「迁移的判定与问责」：是否采用须组委会确认赛题适配性。"
    ],
    "notes": ["…共 4 条，见源码 NOTES"],
    "evidence": ["UIBC 赛题规范"]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "problem-set-generator@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：赛题底稿文本为 AI 辅助生成，属生成合成内容",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（同一命令实测）：赛季主题 mid×2 → rc=0 / 赛季主题 hard×1 → rc=0 / 自定义主题 easy×1 → 适配性告警，rc=1。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 生成完成，无风险提示 | 主题为当前赛季主题（或缺省）且参数合法 |
| `1` | 完成但带风险提示（`warnings`） | 自定义主题（非赛季主题）→ 适配性须组委会确认 |
| `2` | 输入非法，无法生成 | `difficulty` 非 easy/mid/hard；`count` 非 1-10 整数 |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，赛题须组委会人工审核后方可发布（每题 `review_status` 已标注）。
- Q：自定义主题会怎样？ A：正常生成，但给出 `warnings` 提示适配性须组委会确认（`rc=1`），不会静默按赛季主题通过。
- Q：`--difficulty beginner` 会怎样？ A：直接判非法（`rc=2`），不静默按 mid 兜底。
- Q：规则过期怎么办？ A：以 UIBC 章程最新版为准，本工具附规则源便于核对。

## 理论依据
好赛题即好教育——'迁移的判定与问责'把自治的边界问题抛给每一支参赛队。
域站位件：TH-EVT-002 · UIBC 赛事线。

## 条款号待人工核对清单
| 规则 | 用于什么判定 | 状态 |
|---|---|---|
| UIBC 赛题规范 | 赛题结构（背景/任务/约束/交付物/评分点）与难度分级的规则来源 | 待人工核对 |
| 赛季主题'迁移的判定与问责' | 默认主题与自定义主题告警的依据 | 待人工核对 |

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
| 代码 | `problem-set-generator.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `problem-set-generator.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺声@赛事首席发声人 · TH-EVT-002 · SynomosAI（AI 辅助生成，非自然人）
