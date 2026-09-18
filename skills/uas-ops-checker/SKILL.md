---
name: uas-ops-checker
slug: uas-ops-checker
displayName: 无人机运营合规分类判定器
version: 1.0.0
category: it-ops-security
display_name: 无人机运营合规分类判定器
title: 无人机运营合规分类判定器
author: 诺卫(SynomosAI)
license: MIT
description: 无人机运营合规分类判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-UAS-001域。
tags: [合规, 判定器, TH-UAS-001, uas-ops-checker]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 无人机运营合规分类判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见。输出请人工复核。

## 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`《无人驾驶航空器飞行管理暂行条例》(国务院令761号,2024-01-01施行) 第6/12/31/32条 + CCAR-92`（以官方最新文本为准）。

## 三、用法
```bash
python uas-ops-checker.py --mtow 5          # 按参数判定
python uas-ops-checker.py --demo            # 跑内置冒烟案例
```
参数：`mtow / empty_weight`

## 四、真机输出（--demo 节选）
```json
{"tool":"uas-ops-checker","result":{"grade":"示例等级"},"rc":0}
```

## 五、错误码
- `rc=0` 判定完成；`rc=1` 完成但带风险提示（warnings）；`rc=2` 输入不足/无法判定。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源条款号便于核对。

## 理论依据
凡自治之物必先有籍、有证、有门禁——无人机分类即空中治理的出生登记。
域站位件：TH-UAS-001 · 理论总账 REGISTRY。

## 延伸阅读
- LGD 理论总账：https://medxpert.cn/theory
- 域速查页 / GitHub lgd-theory 仓库

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |

---
诺卫@UAS 域首席发声人 · TH-UAS-001 · SynomosAI（AI 辅助生成，非自然人）
