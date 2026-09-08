---
name: pmcf-plan-check
description: PMCF 计划完整性检查器 — PMCF 计划写了一半交上去，公告机构说缺方法缺终点缺统计考量，来回补件三个月（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: pmcf-plan-check
version: 1.0.0
display_name: PMCF 计划完整性检查器
display_name_en: PMCF Plan Completeness Checker
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 医疗器械合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# PMCF 计划完整性检查器 / PMCF Plan Completeness Checker

**pmcf-plan-check** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
PMCF 计划写了一半交上去，公告机构说缺方法缺终点缺统计考量，来回补件三个月

## 用法
```bash
# 按字段逐项检查
python scripts/pmcf_plan_check.py --fields objectives=随访生存率变化 methods=文献+登记库 endpoints=并发症发生率 follow_up_period=24个月 statistical_plan=单臂目标值法 benefit_risk_linkage=是 pms_linkage=是 cer_update_trigger=年度 responsible_person=RA经理 timeline=2026Q4启动

# 或用 JSON 计划文件
python scripts/pmcf_plan_check.py --plan pmcf.json --json
```

## 输出示例（真机）
```
$ pmcf_plan_check.py --plan pmcf.json
完整性 8/10（80%）
  缺失：statistical_plan（统计考量）
  存疑：follow_up_period 未含具体时长
建议补齐后重跑至 10/10 再提交公告机构。
```

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| PMCF_E_MISSING_FIELD | 核心要素缺失 | 按 README 要素表补齐对应字段 |
| PMCF_E_WEAK_FIELD | 字段有值但内容存疑（如随访期无数值） | 补充可核验的量化内容 |
| PMCF_E_NO_INPUT | 未提供 --plan 或 --fields | 任选其一提供计划内容 |

## FAQ
**检查通过等于公告机构认可吗？**

不等于。本工具核对的是 MDCG 2020-7/2019-8 提炼的核心要素完整性，公告机构还会审查方法学合理性。

**NMPA 侧能用吗？**

PMCF 概念源自 EU MDR；NMPA 上市后临床随访要求参照国内指导原则执行，本工具输出对两侧均为要素清单参考。


## 免责 / Disclaimer
pmcf-plan-check 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。
