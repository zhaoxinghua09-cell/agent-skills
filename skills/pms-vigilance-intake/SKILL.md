---
name: pms-vigilance-intake
slug: pms-vigilance-intake
displayName: 医疗器械不良事件报告路径判定器
version: 1.0.0
category: it-ops-security
display_name: 医疗器械不良事件报告路径判定器
title: 医疗器械不良事件报告路径判定器
author: 诺康(SynomosAI)
license: MIT
description: 医疗器械不良事件报告路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-002域（医疗器械全链路）。
tags: [医疗器械, 合规, 判定器, TH-MED-002, pms-vigilance-intake]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械不良事件报告路径判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成医疗器械合规结论或法律/法规意见。输出请人工复核。

## 合规与免责声明（B 级 · YMYL 影响生命健康类）
- 本工具输出为**决策支持**，不构成注册、召回、不良事件报告等官方结论；正式结论须以主管部门（NMPA/省局）书面决定及官方最新条文为准。
- 规则源：`《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)`，请以官方正式文本核对。
- 不得依据本工具输出直接做出临床、注册或召回决策。

## 一、痛点
医疗器械全链路规则白纸黑字但散落多份文件，企业自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)`（以官方最新文本为准）。

## 三、用法
```bash
python pms-vigilance-intake.py --device_class III --device_type implant   # 按参数判定
python pms-vigilance-intake.py --demo                                    # 跑内置冒烟案例
```
参数：`severity / event_type`

## 四、真机输出（--demo 节选）
```json
{"tool":"pms-vigilance-intake","result":{"grade":"示例等级"},"rc":0}
```

## 五、错误码
- `rc=0` 判定完成；`rc=1` 完成但带风险提示（warnings）；`rc=2` 输入不足/无法判定。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源条款号便于核对。

## 理论依据
监测是信任的续约——不良事件上报即把'责任'钉进闭环。
域站位件：TH-MED-002 · 理论总账 REGISTRY · 医疗器械全链路。

## 延伸阅读
- LGD 理论总账：https://medxpert.cn/theory
- 域速查页 / GitHub lgd-theory 仓库

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |

---
诺康@MED 域首席发声人 · TH-MED-002 · SynomosAI（AI 辅助生成，非自然人）
