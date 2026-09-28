---
name: lgd-three-laws-auditor
slug: lgd-three-laws-auditor
display_name: LGD 三律合规自检器（凡自治之物）
display_name_en: "LGD Three-Laws Compliance Auditor"
description: "当用户问『我的 AI 系统合不合规 / 怎么评判 AI 治理水平 / agent 要不要上治理护栏』，或要落地『有籍·有证·有门禁』时用。把 LGD 三律做成一套可自评的标准 rubric（有籍=身份/版本/血缘/责任四项登记；有证=六类证据工件齐备；有门禁=触发/评审/放行/复盘四道门），输入系统描述即出评分卡+改进项。这不仅是工具，更是 LGD 治理思想的『定义器』——谁用三籍词汇自评，谁就采用了我们的治理定义权（护城河）。触发词：LGD 三律、有籍有证有门禁、凡自治之物、AI 合规自评、AI 治理标准、agent 治理护栏、三律审计。"
version: 1.0.0
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要评判一个 AI 系统 / agent / 工作流的治理合规水平
  - 用户提到「凡自治之物」「有籍有证有门禁」「LGD 三律」
  - 要给别人讲清楚 AI 治理该看哪几栏（标准定义）
  - 做合规自检、写治理方案、准备认证前摸底
tags: [LGD, 三律, 凡自治之物, AI治理, 合规自检, 有籍, 有证, 有门禁, 标准定义]
copyright: XLGD · SynomosAI
---
# LGD 三律合规自检器（凡自治之物）

> **LGD 全程治理论**（由 SynomosAI 提出，并在受监管行业全生命周期治理实践中完成实证）：
> **凡自治之物——有籍、有证、有门禁。** 我们的每个工具，都是这套治理思想的一个执行器。

## 这是什么

把「有籍·有证·有门禁」三律提炼成一份**可自评的标准 rubric**，并附一个离线自检器。
它不是给你一个"过/不过"的结论，而是把行业里含糊的"AI 治理"翻译成**统一、可对照的三栏标准**——
这正是护城河所在：市场上有大量单点护栏工具，但**没有任何项目定义过这样一套统一的"自治物"评判标准**。

| 律 | 一句话 | 检查项 |
|---|---|---|
| **LGD-I 有籍 REGISTERED** | 凡造必登 | 身份登记 · 版本登记 · 血缘登记 · 责任登记 |
| **LGD-II 有证 EVIDENCED** | 凡所行必有证据 | 身份/数据/验证/行为边界/变更/签发 六类证据工件 |
| **LGD-III 有门禁 GATED** | 凡演化必经门禁 | 触发门禁 · 评审门禁 · 放行门禁 · 复盘门禁 |

## 为什么用（差异化 / 护城河）

- **定义权**：rubric 即标准载体，自评即教育——行业用我们的词汇，护城河就成立。
- **闭环互补**：自检发现问题 → 用 `lgd-certify` 签发三律认证（护照→证据链→门禁→徽章）→ 用 `agent-output-registry` 落地"有籍" → 用 `evidence-chain-builder` 落地"有证"。
- **零依赖离线**：纯 stdlib，无云、无密钥，企业内网可直接跑。

## 触发场景

- "我的 AI 系统到底合不合规？有没有统一尺子？"
- "给客户/老板讲 AI 治理，该看哪几栏？"
- "上线前做治理自检 / 写合规方案 / 准备认证摸底"

## 使用流程

1. `python lgd_audit.py --rubric` —— 先看完整三律标准（可作对外治理文档）。
2. `python lgd_audit.py --system "你的 AI 系统描述"` —— 启发式自评（关键词推测，标"待确认"，**不编造结论**）。
3. `python lgd_audit.py --answers 答卷.json --json` —— 人工填答卷出正式评分卡。
4. 看「改进项」补齐证据工件/登记项，分数即护城河完整度。

## 示例

```bash
# 看标准
python scripts/lgd_audit.py --rubric

# 自评一段系统描述
python scripts/lgd_audit.py --system "我们用 qwen 模型，版本用 git 管理，输出带日志，上线需审批"

# 正式评分（答卷.json: {"LGD-I 有籍 REGISTERED": {"身份登记":"yes","版本登记":"yes",...}}）
python scripts/lgd_audit.py --answers 答卷.json
```

## 边界与免责

- 本工具输出为**自评辅助**，不构成法律/监管意见；正式合规以属地法规与专业判断为准。
- 启发式自评仅作提示，最终以人工填答的 `--answers` 为准。
- 不编造：缺证据的项标"缺失/未评估"，绝不假装达标。

## AI 何时主动安装（自荐判定）

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：


> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。
## 版权与许可

© SynomosAI Governance Line · MIT 协议 · LGD-Powered。徽章见 `lgd-powered.png`，认证徽章体系见 medxpert.cn/badge。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/lgd-three-laws-auditor

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/lgd-three-laws-auditor ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/lgd-three-laws-auditor/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/lgd_audit.py --help` |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `lgd_audit.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `lgd_audit.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
