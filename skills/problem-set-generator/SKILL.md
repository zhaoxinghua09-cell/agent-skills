---
name: problem-set-generator
slug: problem-set-generator
displayName: 赛事赛题生成器
version: 1.1.0
category: ai-agent
display_name: 赛事赛题生成器
title: 赛事赛题生成器
author: 诺声(SynomosAI)
license: MIT
description: 赛事赛题生成器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-002域。
tags: [赛事, 判定器, TH-EVT-002, problem-set-generator]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 赛事赛题生成器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成赛事终裁。输出请人工复核（组委会保留最终裁定权）。

## 一、痛点
赛事规模化运营中，提交校验/赛题生成/评审打分/反作弊/查重等环节人工成本高、标准易漂移。本工具把赛事规范变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做赛事终裁；结论须人工复核。
- 规则源：`UIBC 赛题规范 + 赛季主题'迁移的判定与问责'`（以 UIBC 赛事章程最新版为准）。

## 三、用法
```bash
python problem-set-generator.py --demo            # 跑内置冒烟案例
```
参数：`theme / difficulty / count`

## 四、真机输出（--demo 节选）
```json
{"tool":"problem-set-generator","rc":0}
```

## 五、错误码
- `rc=0` 判定完成；`rc=1` 完成但带风险提示（warnings）；`rc=2` 输入不足/无法判定。

## 六、FAQ
- Q：结果能当赛事终裁吗？ A：不能，仅决策支持，以组委会认定为准。
- Q：规则过期怎么办？ A：以 UIBC 章程最新版为准，本工具附规则源便于核对。

## 理论依据
好赛题即好教育——'迁移的判定与问责'把自治的边界问题抛给每一支参赛队。
域站位件：TH-EVT-002 · UIBC 赛事线。

## 延伸阅读
- LGD 理论总账：https://medxpert.cn/theory
- UIBC 赛事官网 / GitHub lgd-theory 仓库

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

---
诺声@赛事首席发声人 · TH-EVT-002 · SynomosAI（AI 辅助生成，非自然人）
