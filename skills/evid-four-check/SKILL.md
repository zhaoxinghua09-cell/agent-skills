---
name: evid-four-check
slug: evid-four-check
displayName: 电子证据四性审查判定器
version: 1.0.0
category: it-ops-security
display_name: 电子证据四性审查判定器
title: 电子证据四性审查判定器
author: 诺律(SynomosAI)
author_note: '"SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
compatibility: Cross-platform; zero external dependencies (stdlib only)
metadata: {dependencies: "none"}
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 电子证据四性审查判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-LAW-001域。
tags: [合规, 判定器, TH-LAW-001, evid-four-check]
description_zh: "电子证据四性审查判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-LAW-001域。"
description_en: "Electronic evidence authenticity and legality (four-properties) review determination tool: zero-dependency decision support with JSON IR output (domain TH-LAW-001)."
classification:
  internal: ["主轴7 组织治理与安全"]
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

# 电子证据四性审查判定器

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，**不构成法律意见**，也不构成任何权威结论、合规证明或采信预期。输出请人工复核，最终采信由司法机关认定。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准
> 条款号仍**待人工核对**（见下文「条款号待人工核对清单」）；官方文本直达链接：（地址待补）

## 一、痛点
证据规则的条文白纸黑字，但「四性」（真实性/合法性/关联性/完整性）是清单式判断，散落多份文件、逐案口径不一；举证方自查成本高，易因漏项被质疑。本工具把审查清单变成可枚举、可复现的判定器：给什么参数、出什么结论、缺参数时如何从严，全部落在确定的 JSON IR 上。

## 二、能力边界
- **只做规则判定的形式审查**，不做法律意见；结论须人工复核，**最终采信由司法机关认定**。
- 规则源：`最高人民法院《关于民事诉讼证据的若干规定》第14条、第93-95条 + 《人民法院在线诉讼规则》第12-18条`（**条款号待人工核对**，见下文清单；一律以官方最新文本为准）。
- **输入不足时从严推定**：某维度因缺参无法确定时，取「可能判定中义务最重者」——即判 **FAIL（待补强）**——并在 `warnings` 中明示**可能区间**与**补参建议**（`rc=1`）；**不静默按宽松（PASS）结论输出**。
- **不覆盖**（须另行审查，本工具不代做）：
  - **取证手段合法性的实体判断**（窃录、侵入系统、超范围取证、侵犯个人信息等）——本工具的「合法性」仅做形式审查（是否已声明证据类型）；
  - **证据能力/证明力大小的实质判断**，公证书、鉴定意见、电子数据鉴定的效力评价；
  - 对方质证意见与举证妨碍（第95条对应事项）的裁量；
  - 涉外、涉刑事/行政程序的特殊证据规则；证据原件/原始载体的实物核验。
- **不记录也不判定任何取证行为**：输出中的 `evidence` 是**规则出处（条款依据）**，不是本案证据台账（详见 FAQ）。

## 三、用法
```bash
python evid-four-check.py --demo                          # 跑内置冒烟案例（3 例：rc=0 / rc=1 / rc=1）
python evid-four-check.py --type 电子合同 \
  --has_signature yes --source_verifiable yes \
  --integrity_check yes --relevance yes                   # 参数完整且四性均通过 → rc=0
python evid-four-check.py --type 聊天记录 \
  --has_signature no --integrity_check no --relevance yes  # 缺 source_verifiable → 从严推定，rc=1
python evid-four-check.py --relevance maybe                # 取值非法 → rc=2
```
参数（**5 个参数逐一如下；全部可选**，至少给一个）：

| 参数 | 含义 | 取值 | META 中 `required` |
|---|---|---|---|
| `--type` | 证据类型（驱动「合法性」形式审查） | 合同 / 聊天记录 / 邮件 / 日志 / 音视频 … | `False` |
| `--has_signature` | 有电子签名 / 可信时间戳 / 区块链存证 | `yes` / `no` | `False` |
| `--source_verifiable` | 来源可验证（可回溯原始载体 / 系统） | `yes` / `no` | `False` |
| `--integrity_check` | 已做完整性哈希校验 / 原始载体比对 | `yes` / `no` | `False` |
| `--relevance` | 与待证事实关联 | `yes` / `no` | `False` |

- `yes` 族亦接受 `y / true / 1 / 是 / 有`；`no` 族亦接受 `n / false / 0 / 否 / 无`。**其它取值一律 `rc=2`**（不猜测、不静默当 `no`）。
- **所有参数在 META 中均为 `required=False`，且 argparse 逐条读取该字段（元数据与行为一致）**。原因：①「单个参数缺失」正是 `rc=1` 从严推定的触发条件；② 若改为 `required=True`，argparse 会在解析阶段直接退出并打印 usage（非 JSON IR），破坏 `rc=2` 必须也走 JSON IR 的约定。**全部参数都缺失**才走 `rc=2`。
- 输出恒为 JSON IR（缩进版），**无输出格式开关**；历史上遗留的幽灵参数 `--json` 已删除（见做齐报告）。

## 四、真机输出（`--demo` 实跑，逐字复制）
> 实跑命令 `python evid-four-check.py --demo`（2026-09-26，Python 3.13.14，Windows 11）。
> 下列为该命令输出中**第 2 个案例对象的连续整段**（该命令输出共 3 个案例、292 行）；**逐字节选，未改写、未手写、未美化**。完整 3 例原文见做齐报告。

```json
  {
    "tool": "evid-four-check",
    "input": {
      "type": "聊天记录",
      "has_signature": "no",
      "integrity_check": "no",
      "relevance": "yes"
    },
    "result": {
      "four_properties": {
        "真实性": "FAIL",
        "合法性": "PASS",
        "关联性": "PASS",
        "完整性": "FAIL"
      },
      "dimension_basis": {
        "真实性": "从严推定（输入不完整）",
        "合法性": "明确输入",
        "关联性": "明确输入",
        "完整性": "明确输入"
      },
      "possible_conclusions": [
        "四性形式审查均通过（不构成证据能力或采信结论；最终采信由司法机关认定）",
        "四性形式审查存在未通过项，证据能力待补强（不构成证据能力或采信结论；最终采信由司法机关认定）"
      ],
      "conclusion": "四性形式审查存在未通过项，证据能力待补强（不构成证据能力或采信结论；最终采信由司法机关认定）",
      "remediation": [
        "补强：提供电子签名 / 可信时间戳 / 区块链存证记录，或可回溯的原始载体与生成、保存、传输方法说明（按从严推定未通过；补齐参数后可能转为通过）",
        "补强：提供哈希值（摘要）与原始载体比对，说明是否经篡改、增删（经输入明确判定未通过）"
      ],
      "missing_inputs": [
        "source_verifiable"
      ],
      "evidence": [
        "在线诉讼规则 第12-18条",
        "证据规定 第14条",
        "证据规定 第93-95条"
      ],
      "notes": [
        "本工具仅做**规则判定的形式审查**，不做法律意见，也不构成任何权威结论；最终采信由司法机关认定。",
        "「合法性」本次仅做形式审查（是否已声明证据类型），**不含取证手段合法性（窃录/侵入/超范围取证等）的实体判断**；涉该项须另行审查。",
        "「证据能力/证明力」的实质判断、公证书与鉴定意见的效力、对方质证意见，均不在本工具覆盖范围内。",
        "输入不完整时按**从严推定**（对缺失维度取「未通过（待补强）」），并在 warnings 中给出可能区间与补参建议；不静默按宽松结论输出。",
        "输出字段 evidence / rule_sources 为**规则出处（条款依据）**，不是本案证据记录，也不记录任何取证行为。",
        "条款号与维度口径**均待人工核对**（见 clause_review_checklist）；一律以官方最新文本为准。"
      ],
      "warnings": [
        "输入不完整：未提供判定「真实性」所需的全部参数；已按**从严推定**取『FAIL（待补强）』（可能判定中义务最重者）。",
        "可能区间：真实性 在补齐参数后**可能为 PASS～FAIL**（当前按从严取 FAIL）；整体结论区间为『四性形式审查均通过』～『存在未通过项，待补强』。",
        "补参建议：--has_signature yes|no（电子签名/可信时间戳/区块链存证 之一即有） 或 --source_verifiable yes|no（来源可回溯原始载体/系统）；补齐后请复核，勿以本次结论代替完整判定。",
        "经输入明确判定「完整性」未通过：该判定基于你提供的明确取值（非从严推定）；补强建议见 remediation。",
        "本结论为**形式审查**结果，不构成证据能力认定，也不代表已被采信；最终由司法机关认定（本工具不含取证手段合法性、证明力大小的实体判断）。"
      ]
    },
    "rc": 1,
    "clause_review_checklist": [
      {
        "clause": "证据规定 第14条",
        "used_for": "电子数据范围（含网络平台发布信息、通讯信息、电子文件等）的界定",
        "status": "待人工核对"
      },
      {
        "clause": "证据规定 第93条",
        "used_for": "电子数据真实性审查的考虑因素（载体、生成方式、保存方法等）",
        "status": "待人工核对"
      },
      {
        "clause": "证据规定 第94条",
        "used_for": "真实性推定情形（第三方平台存证、中立系统、公证等）",
        "status": "待人工核对"
      },
      {
        "clause": "证据规定 第95条",
        "used_for": "一方控制证据而拒不提交的法律后果（本条对应举证妨碍，非直接的四性判定）",
        "status": "待人工核对"
      },
      {
        "clause": "在线诉讼规则 第12条～第18条",
        "used_for": "在线诉讼中电子化材料的提交、原件认定、区块链存证与上链真实性审查",
        "status": "待人工核对"
      },
      {
        "clause": "GB 45438-2025",
        "used_for": "AIGC 标识字段 aigc_mark 的标注依据",
        "status": "待人工核对"
      },
      {
        "clause": "「四性」维度划分（真实/合法/关联/完整）",
        "used_for": "本工具的输出结构；属审查清单口径，**非任何条文原文表述**",
        "status": "待人工核对"
      }
    ],
    "aigc_mark": {
      "standard": "GB 45438-2025",
      "is_generated": true,
      "generator": "evid-four-check@SynomosAI",
      "content_type": "decision_support_output",
      "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
      "disclaimer": "决策支持非权威结论，须人工复核"
    }
  }
```

三案例结论（同一命令实测）：`{"type":"电子合同", 四性全 yes}` → `rc=0`；`{"type":"聊天记录","has_signature":"no","integrity_check":"no","relevance":"yes"}` → `rc=1`（缺 `source_verifiable`，真实性从严推定）；`{"has_signature":"yes","integrity_check":"yes","relevance":"yes"}`（**缺 `type`**）→ `rc=1`（合法性从严推定）。

## 五、错误码
| rc | 含义 | 触发条件（实测命令 → 结果） |
|---|---|---|
| `0` | 判定完成，无风险提示 | 参数完整且四性均通过：`--type 电子合同 --has_signature yes --source_verifiable yes --integrity_check yes --relevance yes` → 四性全 PASS |
| `1` | 完成但带风险提示（`warnings` 非空） | ① 输入不完整按**从严推定**：`--type 聊天记录 --has_signature no --integrity_check no --relevance yes`（缺 `source_verifiable`）、`--type 邮件`（缺 3 个维度）；② 取值明确但存在未通过项：`--type 邮件 --has_signature no --source_verifiable no --integrity_check yes --relevance yes` |
| `2` | 输入不足 / 输入非法，无法判定 | ① 全部参数缺失：`python evid-four-check.py`；② 取值非法：`--relevance maybe`、`--has_signature maybe` |

> **rc 语义三档均可复现**：`0` = 正常；`1` = 从严推定 / 有告警；`2` = 门禁错误（参数缺失或取值非法）。三档均输出 JSON IR（含 `errors` / `result`、`clause_review_checklist`、`aigc_mark`）。
> `--demo` 的**进程退出码**遵循本技能库约定：`0`＝案例全部执行完毕 / `2`＝存在输入错误；各案例的实际 `rc`（0/1/2）见每条 IR 的 `rc` 字段——`--demo` 不代替单次调用的 `rc` 语义。

## 六、FAQ
- Q：结果能当证据能力认定或采信依据吗？ A：不能。本工具只做形式审查，不构成法律意见、不构成权威结论；最终采信由司法机关认定。
- Q：缺参数会怎样？ A：按**从严推定**：把因缺参而无法确定的维度判为 `FAIL（待补强）`，在 `warnings` 中给出**可能区间（PASS～FAIL）**与**补参建议**，`rc=1`；**不会静默按 PASS 输出**。`dimension_basis` 字段逐维标注该结论是「明确输入」还是「从严推定（输入不完整）」。
- Q：给了明确 `no` 和没给参数，结论都是 FAIL，有区别吗？ A：结论同（从严取 FAIL），但来源不同：`dimension_basis` 区分「明确输入」与「从严推定」，`remediation` 也会标注「（经输入明确判定未通过）」或「（按从严推定未通过；补齐参数后可能转为通过）」。
- Q：`--relevance 不确定` 这类模糊取值会怎样？ A：`rc=2` 报错，不猜测、不静默当 `no`。请给 `yes` / `no`。
- Q：`evidence` 字段是什么？ A：是**规则出处（条款依据）**——该维度所引用的条款清单，**不是本案证据记录**，也不记录任何取证行为。
- Q：本工具判「合法性 PASS」是否等于取证手段合法？ A：不等于。本工具的「合法性」只做形式审查（**是否已声明证据类型**），**不含取证手段合法性的实体判断**（窃录/侵入/超范围取证等须另行审查）。
- Q：规则过期怎么办？ A：以官方最新条文为准；输出中的 `clause_review_checklist` 逐条给出「哪一条款用于什么判定」，便于人工核对。

## 理论依据
证据须可被问责——四性审查即把「可信」写进每一次举证。
- 本工具输出的是**审查判定依据**（规则出处清晰、可复核）。依 LGD 证据语义界定：**Evidence（证据）＝治理状态转换的可验证依据，非行为日志**；本工具不把日志当证据，也不把规则出处当本案证据。
- 域站位件：TH-LAW-001 · 理论总账 REGISTRY（在线地址待补，实测 `medxpert.cn/theory` 不可达）。

## 条款号待人工核对清单
| 条款 / 口径 | 用于什么判定 | 状态 |
|---|---|---|
| 证据规定 第14条 | 电子数据范围（含网络平台发布信息、通讯信息、电子文件等）的界定 | 待人工核对 |
| 证据规定 第93条 | 电子数据真实性审查的考虑因素（载体、生成方式、保存方法等） | 待人工核对 |
| 证据规定 第94条 | 真实性推定情形（第三方平台存证、中立系统、公证等） | 待人工核对 |
| 证据规定 第95条 | 一方控制证据而拒不提交的法律后果（举证妨碍） | 待人工核对 |
| 在线诉讼规则 第12条～第18条 | 在线诉讼中电子化材料的提交、原件认定、区块链存证与上链真实性审查（区间范围待核） | 待人工核对 |
| GB 45438-2025 | AIGC 标识字段 `aigc_mark` 的标注依据 | 待人工核对 |
| 「四性」维度划分（真实/合法/关联/完整） | 本工具的输出结构；属审查清单口径，**非任何条文原文表述** | 待人工核对 |

> 本包**未新增任何无法核实的条款号**；上表条款号沿用原实现，**未经人工核对不改动**。核对后如有变更，以官方最新文本为准。

## 延伸阅读
- LGD 理论长页：https://medxpert.cn/lgd.html
- 技能库总览（medxpert.cn）：https://medxpert.cn/skills/
- 机器可读索引 llms.txt：https://medxpert.cn/llms.txt
- 理论总账仓库 lgd-theory：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现 uibc-core：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库总索引 agent-skills：https://github.com/zhaoxinghua09-cell/agent-skills
- 本工具目录：https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check
- LGD 理论总账 REGISTRY 在线页：（地址待补）
- LAW 域速查页：（地址待补）

## 家族合集
| 域 | 工具 | 大使 | 目录 |
|---|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker |
| AUT 驾驶 | aut-grade-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker |
| DAT 数据 | data-grade-checker | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker |
| BIO 生物 | hgrac-route-checker | 诺康 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/hgrac-route-checker |
| FIN 金融 | fin-ai-classifier | 诺丰 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier |
| LAW 法律 | evid-four-check | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check |

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `evid-four-check.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `evid-four-check.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---
诺律@LAW 域首席发声人 · TH-LAW-001 · SynomosAI（AI 辅助生成，非自然人）
