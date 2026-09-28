---
name: originality-check
slug: originality-check
displayName: 赛事作品原创性查重器
version: 1.1.0
category: ai-agent
display_name: 赛事作品原创性查重器
title: 赛事作品原创性查重器
author: 诺源(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事作品原创性查重器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-005域。
tags: [赛事, 判定器, TH-EVT-005, originality-check]
description_zh: "赛事作品原创性查重器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-005域。"
description_en: "Contest submission originality and plagiarism checker: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-005)."
classification:
  internal: ["主轴3 赛事与生态"]
  skillhub: ["community-events"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 赛事作品原创性查重器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做赛事终裁；结论须人工复核。
- 规则源：`UIBC 原创性规范 + 学术不端界定`（以 UIBC 赛事章程最新版为准）。
- **输入不足时从严推定**：`known_hashes` 缺省（空指纹库）时，「无重复」结论**不可靠**——给出 `warnings` 明示告警与补参建议（`rc=1`），**不静默按原创通过输出**；`known_hashes` JSON 非法时直接判非法（`rc=2`），不静默按空库处理。
- **不覆盖**：语义级抄袭（相似度为示意算法，正式查重须用 MinHash/SimHash + 人工判定）、多作品交叉比对、申诉流程。

## 三、用法
```bash
python originality-check.py --submission_hash sha256:new999 --known_hashes '["sha256:aaa111","sha256:bbb222"]'   # 有对照库且无命中 → rc=0
python originality-check.py --submission_hash sha256:aaa111 --known_hashes '["sha256:aaa111"]'                   # 命中重复 → rc=1
python originality-check.py --submission_hash sha256:new999                                                      # 空指纹库 → 从严告警，rc=1
python originality-check.py --submission_hash sha256:x --known_hashes '{bad'                                     # JSON 非法 → rc=2
python originality-check.py --demo                                                                               # 跑内置冒烟案例（3 例）
```
参数：`submission_hash`（作品指纹，必填，缺失时 `rc=2`）/ `known_hashes`（历史/公开库指纹 JSON 字符串列表；缺省按空库从严告警）。

## 四、真机输出（--demo 第 3 例，逐字）
> 实跑命令 `python originality-check.py --demo`（2026-09-26，Python 3.13.12）。以下为该例完整 JSON，**字段值逐字未改**。

```json
{
  "tool": "originality-check",
  "input": {
    "submission_hash": "sha256:new999"
  },
  "result": {
    "similarity": 0.0,
    "is_duplicate": false,
    "exact_match": false,
    "matches": [],
    "warnings": [
      "known_hashes 为空（未提供对照指纹库）：本输出「无重复」不可靠，请提供历史/公开库指纹后复核；不静默按原创通过处理。"
    ],
    "notes": ["…共 2 条，见源码 NOTES"],
    "evidence": ["UIBC 原创性规范"]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "originality-check@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

三案例结论（同一命令实测）：精确命中 → `is_duplicate=true`，rc=1 / 新指纹+有对照库 → 无重复，rc=0 / 新指纹+空库 → 从严告警，rc=1。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 有对照指纹库且未命中重复 |
| `1` | 完成但带风险提示（`warnings`） | 命中重复（精确或相似度 ≥0.85）；或 `known_hashes` 为空（从严推定告警） |
| `2` | 输入不足/输入非法，无法判定 | 缺 `submission_hash`；`known_hashes` JSON 非法或非字符串列表 |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，以组委会认定为准。
- Q：不给 known_hashes 会怎样？ A：按空库从严处理——「无重复」结论不可靠，给出 `warnings`（`rc=1`），不会静默按原创通过输出。
- Q：相似度算法可信吗？ A：为示意算法（前缀比对），正式查重须用 MinHash/SimHash + 人工判定；输出 notes 已注明。

## 理论依据
原创须可被证明——指纹查重即把'这作品是谁的'写进可信账本。
域站位件：TH-EVT-005 · UIBC 赛事线。

## 条款号待人工核对清单
| 规则 / 数值 | 用于什么判定 | 状态 |
|---|---|---|
| UIBC 原创性规范 | 重复判定的规则来源 | 待人工核对 |
| 相似度阈值 0.85 | 重复判定断点（示意算法配套取值） | 待人工核对 |

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
| 代码 | `originality-check.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `originality-check.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺源@DAT 域首席发声人 · TH-EVT-005 · SynomosAI（AI 辅助生成，非自然人）
