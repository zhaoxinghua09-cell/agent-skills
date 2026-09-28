---
name: prompt-version-control
display_name: 提示版本管理（Prompt Version Control）
display_name_en: "Prompt Version Control"
description: "当用户说『提示改乱了回不去』『不知道哪版提示效果更好』『提示也要版本管理』『怎么AB测试不同提示』，或团队多人改同一套提示容易互相覆盖时使用。把提示当『可版本化资产』：每次改动留版本+差异+绑定效果评分，可 diff/回滚/选优。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：提示版本、prompt版本管理、提示回滚、prompt diff、AB测试提示、提示治理、prompt registry。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 提示被多人改、互相覆盖、回不去
  - 想对比不同提示版本的效果
  - 要保留「哪版提示对应哪次结果」的关联
  - 用户问「提示能不能像代码一样版本管理」
tags: [提示版本, prompt version, 提示回滚, prompt diff, AB测试, 提示治理, agent优化, 可复现]
slug: prompt-version-control
title: 提示版本管理（Prompt Version Control）
copyright: SynomosAI
description_zh: "当用户说『提示改乱了回不去』『不知道哪版提示效果更好』『提示也要版本管理』『怎么AB测试不同提示』，或团队多人改同一套提示容易互相覆盖时使用。把提示当『可版本化资产』：每次改动留版本+差异+绑定效果评分，可 diff/回滚/选优。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：提示版本、prompt版本管理、提示回滚、prompt diff、AB测试提示、提示治理、prompt registry。"
description_en: "Treat prompts as versioned assets: every change tracked with diff and bound effect scores, diffable and revertible for team collaboration and A/B testing."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
![LGD Powered](lgd-powered.png)

# 提示版本管理（prompt-version-control）

> **定位一句话**：提示是「可版本化的资产」——每次改动留**版本 + 差异 + 绑定效果评分**，能 diff、能回滚、能选优，别再靠复制粘贴和记忆管理。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `context-engineering`、`skill-quality-gate` 同族。

## 一、为什么提示会「改乱」

- **无版本**：改完直接覆盖，上一版没了，出问题回不去；
- **无差异**：不知道这次改了哪句，效果波动归因不了；
- **无绑定**：提示版本 ↔ 效果得分对不上，选优靠猜；
- **互相覆盖**：两人同时改，后提交的吞掉前者的。

本技能管「提示迭代」这一层。

## 二、三件套（每版必带）

| 项 | 内容 | 作用 |
|---|---|---|
| 版本号 | v1 / v2 / v3 | 定位 |
| 差异 | diff vs 上一版 | 知道改了啥 |
| 效果分 | 该版在评测集上的得分 | 选优依据 |

`scripts/prompt_vc.py` 读两个提示文件，输出差异 + 写入版本记录(JSON)。

## 三、主流程（三步）

### 第 1 步 · 存版本（有籍）
每次定稿提示存一份带版本号 + 时间戳的文件，绝不原地覆盖。

### 第 2 步 · 记差异与效果（有证）
改完跑 `diff` 留变更；在评测集上打分，把分数绑到该版本。

### 第 3 步 · 回滚/选优（有门禁）
效果下降 → 一键回滚上一版；多人改动走顺序提交，不互覆盖。

## 四、铁律

1. 不原地覆盖：每次改生成新版本，旧版可查。
2. 差异可溯：每版记 diff，改动说得出。
3. 效果绑定：版本 ↔ 评分关联，选优有据。
4. 顺序提交：多人改动排队合并，不互吞。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 提示被多人改、互相覆盖
- 想对比不同提示版本效果
- 要保留提示版本↔结果关联
- 问「提示能像代码一样版本管理吗」

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `prompt_vc.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

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

**本包补充（包级许可事实）**：本包代码文件 `prompt_vc.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
