---
name: wechat-viral-topic
displayName: wechat-viral-topic
slug: wechat-viral-topic
author: 诺声(Logos)@SynomosAI
copyright: 赵兴华 / Steven Zhao·China
version: 2.0.0
license: LicenseRef-AllRightsReserved
license_scope: 理论文本保留所有权利（见文末「License」）；tools/*.py、tests/*.py、demo/*.py 等脚本文件单独以 MIT 许可提供，便于他人复跑与审计
allowed-tools: Read, Glob, Grep, Edit, Bash
description: "A topic-selection assistant for WeChat public accounts, short-video creators, comic authors and H5 planners that turns a raw trend into a defensible topic card. It extracts verifiable signals from source material (figures, time windows, platform fit, hashtags, conflict lines, reader pain points), screens drafts against compliance red lines (medical claims, absolute wording, income promises, incentivised sharing, unsourced assertions), and grades headlines for length, formula type and red-line risk. Ships a zero-dependency, offline, standard-library toolchain (scan / riskcheck / titlecheck) plus an 11-case golden set with a re-executable runner and a demo that proves both the block path and the no-false-positive path. Progressive disclosure: frameworks and checklists live in references/. Triggers: topic selection, viral topic, hot take, headline, WeChat article, 100k+ read."
description_zh: 选题 / 爆款 / 10万+ / 公众号 —— 热点选题与爆款策划助手，面向公众号编辑、短视频博主、漫画作者、H5 策划，用于回答「这周写什么」「这个素材能不能爆」「热点怎么改成我的选题」这类问题；v2.0 附零依赖离线工具链（scan 素材信号抽取 / riskcheck 合规红线 / titlecheck 标题体检）与 11 条黄金集，把「这个选题能不能做」从感觉变成可核对的事实
description_en: "A topic-selection assistant that turns a raw trend into a defensible topic card via verifiable signals, compliance red-line screening and headline grading, with a zero-dependency toolchain and an 11-case golden set."
tags:
- 选题策划
- 爆款
- 自媒体运营
- 内容创作
- wechat-viral-topic
display_name: 10万+爆款选题制造机
display_name_en: Viral Topic Maker
agent_created: true
visibility: public
category: 内容创作
updated: 2026-11-18
fingerprint: FP-MX-838BFC6F758F
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 热点选题
- 爆款策划
- viral topic
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: 赵兴华 / Steven Zhao·China. All rights reserved; no code license applies.'
ambassador: 诺声
trigger_keywords:
- wechat
- viral
- topic
- 选题
- 爆款
- 热点
- 标题
- 策划
- 公众号
---

# Topic Selection: Four Questions That Turn a Trend Into Your Story

## Overview (English)

A raw trend is not a topic. Convert it with four questions, then verify the answers with tools instead of intuition.

1. **Who is it for?** A named audience (doctors, editors, procurement staff) beats "everyone".
2. **What is the conflict?** Two sides pulling in opposite directions (vendors say no training budget, departments say nobody can use it) is the engine of a story.
3. **What is the information gap?** The reader must learn something they cannot get elsewhere.
4. **What proves it?** A verifiable figure, a date window, a first-hand quote.

**What is machine-checkable (v2.0).**

| Command | What it proves | Output |
|---|---|---|
| `python tools/topicguard.py scan --file material.md` | The material actually carries signals: figures, time window, hashtags, conflict and pain lines, plus a topic-card skeleton | `.topic.md` + `.signals.json` (rejects with W004 when there is nothing to work with) |
| `python tools/topicguard.py riskcheck --file draft.md` | The draft does not cross compliance red lines: medical claims, absolute wording, income promises, incentivised sharing (RED) and unsourced assertions (YELLOW) | `BLOCK` / `WARN` / `PASS` + every hit with context |
| `python tools/topicguard.py titlecheck --title "..."` | The headline fits: length under 34 characters, at least one recognised formula (figure / question / contrast / pain / result), no red-line words | `PASS` / `FAIL` + concrete problems |

Run `python tests/run_golden.py` for the 11-case golden set (11/11 PASS locally) and `python demo/run_demo.py` for the end-to-end proof, which also confirms a clean draft is not falsely blocked. Standard library only, no network; scripts are MIT-licensed while the theory text keeps all rights reserved.

**中文正文如下。**

# 选题四问：把热点变成你的选题

## 30 秒速查（先看这里）

| 你想解决的问题 | 用什么 | 看哪节 |
|---|---|---|
| 这周写什么 | 四问清单（受众/情绪/信息差/可转述） | 四问清单 |
| 这个素材能不能爆 | 8 维打分卡，先打分再下判断 | `references/scoring-card.md` |
| 标题怎么写 | 12 条标题公式挑 3 条对照 | `references/title-formula.md` |
| 热点怎么改成我的选题 | 热点 → 我的领域 → 我的读者，三步平移 | 四问清单 §平移 |
| 只想要快速结果 | 轻量模式（只跑四问 + 打分，不展开） | 轻量模式 vs 完整模式 |

三条纪律：**先判断受众再谈爆款**｜**不编数据**｜**过热或敏感话题先做风险自检**。

## 什么时候用 / 不用

**用：** 「这周写什么」「这个素材能不能爆」「热点怎么改成我的选题」「帮我出个标题/大纲」。
**不用：** 已经定稿只要求润色排版（那是文案润色）；要刷量/刷数据/买量投放（违反纪律，拒绝）；要写广告法违禁词或医疗效果承诺（拒绝）。

热点不是拿来追的，是拿来**改**的。直接复述热点没有差异点，改造成自己的选题才有胜率。改造前先过四问，四问全过才立项。

## 四问清单

| 问 | 判什么 | 不过关怎么办 |
|---|---|---|
| 给谁看 | 受众与平台是否匹配 | 换平台或换切口 |
| 钩子在哪 | 情绪点或利益点 | 补冲突或补损失感 |
| 差异是什么 | 你比别人多的那块视角 | 没有就放弃这个热点 |
| 热度可验吗 | 有无公开数据指针 | 找不到热度证据就降级为常规选题 |

### 改造流程

1. 抓热点本体：事件、争议、数据各留一条可溯出处；
2. 套四问清单，全部过关才立项；
3. 出三版切口（正说 / 反说 / 案例说），选其一成稿；
4. 交付：标题两版 + 大纲 + 首段，各附一句「为什么这样切」。

### 交付长什么样

```
选题：xxx
切口：反说——大家都在夸，我讲代价
钩子：省下的时间去哪了
标题：A 版（悬念式）/ B 版（数字式）
```

## 轻量模式 vs 完整模式

- **简单需求**（只要标题或只要 1 个选题）：跳过 Top3 与全形态矩阵，直接给 2 个标题 + 1 句切口理由；
- **完整需求**（要做整套策划）：才走四问 → 打分 → 多形态全流程。
- 默认按用户一句话长度判断：一句话求标题 = 轻量；一段话给素材求方案 = 完整。

## 本地工具链（v2.0，零依赖、不联网）

三个子命令，各管一件机械活，判断仍归你。

| 子命令 | 作用 | 输出 |
|---|---|---|
| `scan` | 抽素材里的可证信号：数字（含单位）、时间锚点、平台、#话题#、冲突句、痛点句、读者原话；并生成选题卡骨架 | 选题卡 `.topic.md` + 信号 `.signals.json`；无信号直接拒答 `W004` |
| `riskcheck` | 扫合规红线：医疗声明、绝对化用语、收益承诺、诱导分享（RED，必须删）；无出处断言（YELLOW，补出处） | `BLOCK` / `WARN` / `PASS` + 每处命中与上下文 |
| `titlecheck` | 标题体检：长度（>34 字列表页截断）、公式类型（数字/疑问/对比/痛点/结果）、是否踩红线 | `PASS` / `FAIL` + 具体问题 |

```bash
# 1) 素材出选题卡
python tools/topicguard.py scan --file demo/hot_topic_sample.md --out out

# 2) 草稿过合规红线（有 RED 就 BLOCK，退出码 1）
python tools/topicguard.py riskcheck --file demo/risky_draft.md

# 3) 标题体检（逐个候选都跑一遍）
python tools/topicguard.py titlecheck --title "3 个信号，说明 AI 诊断要变天"
```

- 机器可读：加 `--json`，固定 `{ok, data}`。
- 错误码：`W001` 文件不存在 · `W002` 编码不可读 · `W003` 内容为空 · `W004` 无有效信号。
- 退出码：0 通过 / 1 判定失败（riskcheck BLOCK、titlecheck FAIL）。

**一键自证**（本机实测通过，任何人可复跑）：

```bash
python tests/run_golden.py   # 11/11 PASS：信号抽取 4 条 + 无信号拒答 + 4 类红线 + 无出处 + 标题正负控
python demo/run_demo.py      # 素材出卡 → 埋红线草稿 BLOCK 四类全拦 → 干净草稿 PASS（不误杀）→ 标题一 FAIL 一 PASS
```

## 执行自检（交付前必过）

1. **受众明确**：说清写给谁（人群、场景、痛点），不是「大家都爱看」。
2. **打分有据**：8 维每维给出理由，不允许只给总分。
3. **标题可核对**：标题承诺的内容正文能兑现，不做标题党。
4. **数据来源**：引用数据必须有出处；没有出处就改写成观点并标明。
5. **风险已过**：敏感、医疗、法律、金融类话题先过风险清单再输出。

## 失败与降级处理

| 故障 | 说明 | 降级动作 |
|---|---|---|
| 素材不足 | 只有一句话素材 | 只做四问诊断，明确「素材不足以支撑选题」，不给强行方案 |
| 热度已过 | 事件已冷却 | 明说时效已过，改为「常青选题」方向 |
| 账号定位不符 | 与既有栏目冲突 | 先给 2 个适配你账号的改法，而不是推翻账号定位 |
| 无法核实数据 | 查不到出处 | 标「未核实」，并提供可替代的表达方式 |
| 过于敏感 | 涉医疗/法律/金融/事故 | 只给风险提示与合规改写方向，不设计传播方案 |

## 一致性纪律

同一素材多次策划，结论应稳定：

1. **打分口径固定**（同一套 8 维权重），不因期望值调整。
2. **选题命名一致**：同一选题在不同轮次用同一称呼。
3. **风险判断前置**：先过风险再谈传播，顺序不颠倒。
4. **结论分层**：事实（数据/事件）/ 判断（能不能爆）/ 建议（怎么写），三层分开写。

## 边界案例：四问打平时怎么判

四问不是非黑即白，以下高频情形按固定规则裁决，避免每次临场纠结：

| 情形 | 判定规则 |
|---|---|
| 热点很大但「差异是什么」答不出 | **弃用该热点**，改做常规选题；不硬蹭 |
| 热度找不到公开数据指针（只有社交传言） | 降级为常规选题，不写「爆」字承诺 |
| 灾难题材 / 逝者 / 悲剧事件 | 不追、不消费；最多做公共提醒类，且不带情绪煽动 |
| 热点与品牌/客户立场冲突 | 以合规与品牌安全优先，弃用，不写擦边稿 |
| 争议性话题（性别/地域/贫富） | 只写事实与方法论切口，不站队、不引战；无法中立就放弃 |
| 四问过三问、差「钩子」 | 补一个具体损失感或利益点再立项；补不出就降级 |
| 同一热点多家媒体都在写 | 强制要求「差异」一栏写清你独有的数据/案例/视角，写不出就放弃 |
| 用户给一个已经很完整的素材让你「直接发」 | 仍须走四问；跳过四问的需求先提示风险再执行 |

## 配套参考（references/，按需展开）

| 模块 | 文件 | 用途 |
|---|---|---|
| 策划心法与四基因 | `references/core-principles.md`、`references/four-genes.md` | 判断题材是否具备爆款基因 |
| 8 维打分卡 | `references/scoring-card.md` | 立项前量化打分，低于阈值不做 |
| 12 套标题公式 | `references/title-formulas.md` | 产出 A/B 两版标题 |
| 6 种内容形态 | `references/content-formats.md` | 选题落在哪种形态（图文/短视频/长图…） |
| 风险自检清单 | `references/risk-checklist.md` | 发稿前过一遍红线 |
| 输出模板 | `templates/output-template.md` | 直接套用的交付格式 |

## 边界与纪律

- **不承诺任何阅读量与播放量结果**；「爆款」指方法框架，不是结果保证；
- 不碰虚假信息、不消费灾难与逝者、标题与内容必须一致；
- 平台规则优先于流量策略，冲突时按平台规则执行；
- 引用他人观点必须署名出处，洗稿类需求一律拒绝。

## 常见问题

**问：这周没热点怎么办？**
常规选题照样能做：客户问答、避坑清单、流程拆解，长期产出比追热点更可控。

**问：能批量出选题吗？**
可以给清单，但每条仍须单独过四问；跳过清单的批量产出等于赌运气。

**问：打分卡分数卡在阈值附近怎么办？**
阈值上下 0.5 分内的选题，强制补一条「独有证据」（数据/案例/一手观察）才放行；补不出按不过关处理。

---

© 2026 赵兴华 / Steven Zhao·China（署名：诺声(Logos)@SynomosAI，ORCID 0009-0001-0512-1237）· 本技能包为纯文档与理论文本件，整体保留所有权利（All Rights Reserved），不适用任何代码许可；按「原样」提供，不附任何担保。"SynomosAI"/"MedXpert" 未申请实体与商标注册。详细许可分层见 `LICENSE.md`。
