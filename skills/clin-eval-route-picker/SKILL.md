---
name: clin-eval-route-picker
description: 临床评价路径选择器 — 免临床目录、同品种路径、临床试验三条路怎么选说不清，资料写到一半才发现路走错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读）
slug: clin-eval-route-picker
version: 1.0.0
display_name: 临床评价路径选择器
display_name_en: Clinical Evaluation Route Picker
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: 医疗器械合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
---
# 临床评价路径选择器 / Clinical Evaluation Route Picker

**clin-eval-route-picker** v1.0.0 · LGD-Powered 家族 · 零依赖 · 确定性输出（JSON IR）· 修复回执错误码

## 痛点
免临床目录、同品种路径、临床试验三条路怎么选说不清，资料写到一半才发现路走错了

## 用法
```bash
# NMPA：III 类、不在免临床目录、无同品种数据
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class III --in-catalog no --eq-data no

# NMPA：列入免临床目录
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes

# EU：IIa 类、属成熟技术（WET）
python scripts/clin_eval_route_picker.py --market eu --eu-class IIa --wet yes

# JSON 中间表示
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes --json
```

## 输出示例（真机）
```
$ clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes
推荐路径：免临床评价路径（列入《免于临床评价医疗器械目录》）
  依据：国家药监局 2021 年第 73 号通告
  需提交：与目录条目的对比说明、与同品种器械的对比资料
  提示：对比不符项需另行评价；以官方最新版目录为准
```

## 退出码与错误码
- rc=0 通过 / rc=1 发现问题 / rc=2 用法错误
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| CE_E_MISSING | 缺少必需输入（如 market=nmpa 但未给 --nmpa-class） | 按提示补齐对应市场的分类与条件输入 |
| CE_E_CONFLICT | 输入组合自相矛盾（如 I 类+植入+临床数据） | 核对产品实际分类与证据现状后重新输入 |
| CE_E_VALUE | 布尔类参数取值非法 | 布尔参数仅接受 yes/no |

## FAQ
**工具给的路径能直接当注册策略吗？**

不能。输出是基于现行规则文本的确定性推荐，供立项讨论与资料准备导航；注册策略需结合产品具体属性并由注册人员/法规顾问确认。

**为什么答案总带'以官方最新为准'？**

目录、通告与指南会更新，工具按发布时规则编写；本措辞是 YMYL 内容纪律，不是免责套话。


## 免责 / Disclaimer
clin-eval-route-picker 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `clin_eval_route_picker.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `clin_eval_route_picker.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
