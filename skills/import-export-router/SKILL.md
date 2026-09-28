---
name: import-export-router
slug: import-export-router
displayName: 医疗器械进出口路径判定器
version: 1.0.0
category: it-ops-security
display_name: 医疗器械进出口路径判定器
title: 医疗器械进出口路径判定器
author: 诺衡(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 医疗器械进出口路径判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-MED-005域（医疗器械全链路）。
tags: [医疗器械, 合规, 判定器, TH-MED-005, import-export-router]
---

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

# 医疗器械进出口路径判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成医疗器械合规结论或法律/法规意见。输出请人工复核。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

## 合规与免责声明（B 级 · YMYL 影响生命健康类）
- 本工具输出为**决策支持**，不构成注册、召回、不良事件报告等官方结论；正式结论须以主管部门（NMPA/省局）书面决定及官方最新条文为准。
- 规则源：`NMPA 进口医疗器械注册规定 + 出口销售证明办理 + FDA/EU MDR`（条款号待人工核对，见下表；一律以官方最新文本为准）。
- 不得依据本工具输出直接做出临床、注册或召回决策。

## 一、痛点
医疗器械全链路规则白纸黑字但散落多份文件，企业自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

## 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- **输入不足时从严推定**：`is_registered` 缺省时从严按「未注册」处理（走须先注册的路径并给出 `warnings`，`rc=1`）——**不静默按已注册的宽松路径输出**；`dest_region` 缺省按 `other`（依目的国法规办理）处理。
- **不覆盖**：产品分类界定（I/II/III 类）、注册检验细节、目的国准入的具体材料清单与时限；这些须另行判定。

## 三、用法
```bash
python import-export-router.py --direction import --is_registered yes                 # 参数完整 → 凭注册证进口，rc=0
python import-export-router.py --direction export --is_registered no                  # 未注册即出口 → 从严告警，rc=1
python import-export-router.py --direction banana                                     # 输入非法 → rc=2
python import-export-router.py --demo                                                 # 跑内置冒烟案例（4 例）
```
参数：`direction`（import/export，必填，缺失或非法时 `rc=2`）/ `is_registered`（yes/no，缺省从严按 no）/ `dest_region`（cn/us/eu/other，缺省按 other）。

## 四、真机输出（--demo 第 4 例节选）
> 实跑命令 `python import-export-router.py --demo`（2026-09-26，Python 3.13.12）。为便于阅读，部分数组已折行压缩；**字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "import-export-router",
  "input": {"direction": "export", "is_registered": "no", "dest_region": "eu"},
  "result": {
    "route": "须先取得境内注册/生产资质方可办理出口证明；境外上市须 CE 认证（EU MDR 技术文件+公告机构）",
    "required_docs": ["境内注册证/生产许可"],
    "obligations": ["…共 3 条，见源码"],
    "notes": ["…共 3 条，见源码"],
    "evidence": ["NMPA 进口规定", "出口销售证明办理", "FDA/EU MDR"],
    "warnings": [
      "境内未取得注册/生产资质：《医疗器械出口销售证明》无法办理，须先完成境内注册/取得生产资质后再出口"
    ]
  },
  "rc": 1,
  "aigc_mark": {
    "standard": "GB 45438-2025", "is_generated": true, "generator": "import-export-router@SynomosAI",
    "content_type": "decision_support_output",
    "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
    "disclaimer": "决策支持非权威结论，须人工复核"
  }
}
```

四案例结论（同一命令实测）：`{import, yes}` → 凭境内注册证进口（rc=0）/ `{import, no}` → 须先申请 NMPA 注册（rc=1）/ `{export, yes, us}` → 出口销售证明+FDA 路径（rc=0）/ `{export, no, eu}` → 须先取得境内资质+CE 路径（rc=1）。

## 五、错误码
| rc | 含义 | 触发条件（实测） |
|---|---|---|
| `0` | 判定完成，无风险提示 | `--direction import --is_registered yes`；或 `--direction export --is_registered yes` |
| `1` | 完成但带风险提示（`warnings`） | `--direction import --is_registered no`（未获注册证不得进口销售）；或 `--direction export --is_registered no`（从严推定告警） |
| `2` | 输入不足/输入非法，无法判定 | 缺 `direction`、`direction` 取值非法（如 `banana`） |

> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当合规证明吗？ A：不能，仅决策支持，以主管部门认定为准。
- Q：`is_registered` 不给会怎样？ A：从严按「未注册」处理（走须先注册的路径并给出 `warnings`，`rc=1`），不会静默按已注册的宽松路径输出。
- Q：规则过期怎么办？ A：以官方最新条文为准，本工具附规则源便于核对。

## 理论依据
跨境有界——进出口路径即把'合规'钉进国门内外。
域站位件：TH-MED-005 · 理论总账 REGISTRY · 医疗器械全链路。

## 条款号待人工核对清单
| 条款 / 规则 | 用于什么判定 | 状态 |
|---|---|---|
| NMPA 进口医疗器械注册规定 | 进口路径（凭注册证进口 vs 须先注册） | 待人工核对 |
| 《医疗器械出口销售证明》办理规定 | 出口路径（省级药监局办理条件与材料） | 待人工核对 |
| FDA 510(k)/PMA | 出口美国的境外上市路径 | 待人工核对 |
| EU MDR（CE 认证+公告机构） | 出口欧盟的境外上市路径 | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表沿用原实现所引规则源，未经人工核对不改动。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论总账：https://medxpert.cn/theory（实测可达性待核）
- 域速查页 / GitHub lgd-theory 仓库：（地址待补）

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `import-export-router.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码（.py）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（理论文本保留所有权利）。**

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

**本包补充（包级许可事实）**：本包代码文件 `import-export-router.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺衡@MED 域首席发声人 · TH-MED-005 · SynomosAI（AI 辅助生成，非自然人）
