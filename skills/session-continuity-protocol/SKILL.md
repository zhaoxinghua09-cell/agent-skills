---
name: session-continuity-protocol
description: "跨工作区 / 跨会话记忆连续性协议（潘布达首发）。触发场景：新会话开局、用户说「续上上下文 / 你还记得吗 / 你失忆了」、或要做任何连续性敏感任务（公众号发稿、品牌资产、发布阻塞、密钥投递、项目状态）之前。加载后严格跑「开局四步」把已固化事实回灌，避免在已定稿事项上重复问用户、避免失忆。真源 = 文件层（_ACTIVE_PROJECTS.md + 账号 MEMORY.md）优先于 localmem 语义层兜底。"
version: 1.0.0
agent_created: true
author: 潘布达 (Buda Pan) @SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit, WebFetch, WebSearch
category: 通用技能
platforms: [WorkBuddy, Claude Code, Windows, macOS, Linux]
read_when:
  - 新会话开始、用户还没说具体任务前（默认主动跑）
  - 用户质疑「你失忆了 / 怎么又忘了 / 昨天不是已经…」
  - 要做公众号发稿、品牌资产、发布阻塞、密钥投递类任务前
  - 跨工作区接续上一个会话的半成品（如推送草稿箱仍卡在哪）
tags: [continuity, memory, localmem, cross-session, 开局四步, 失忆, 跨工作区]
slug: session-continuity-protocol
displayName: 跨会话连续性协议（开局四步）
display_name: 跨会话连续性协议（开局四步）
title: 跨会话连续性协议（开局四步）
---

# session-continuity-protocol · 跨会话记忆连续性协议

> 作者：潘布达（内容发布运营团主理人）｜定稿：2026-09-04｜背景：Steven 多次指出「失忆」——根因不是方案缺失，而是**开局没按协议回灌已知事实**。

## 〇、为什么需要这个协议

GitHub 上 agent 记忆的基准结论（memory-systems 技能 + LoCoMo 基准）：**文件级记忆读取比专用记忆工具更可靠**——基础文件操作就能拿 74%，高于 Mem0 专用工具 68.5%。所以本机已搭的「本地优先最小栈」是对的，不用换方案、不用上云：

- ✅ `localmem-mcp`（已装 v0.1.1）：SQLite+FTS5+本地 fastembed，余弦+关键词混合检索，零 LLM/零 API
- ✅ 配置 `LOCALMEM_DB_PATH=<你的工作区根>/_localmem_memories.db`，**跨工作区/跨账号共享同一 db**
- ✅ 全局总索引 `<你的工作区根>/_ACTIVE_PROJECTS.md`
- ✅ 账号级真源 `~/.workbuddy/MEMORY.md`

**唯一缺口**：开局没按协议回灌。失忆 = 潘布达（连续性 Owner）没执行协议。本技能就是把这个协议变成可调用、可复用的动作。

## 一、开局四步（每次新会话必跑，顺序不可省）

> 动手做任何实质性任务**之前**先跑完这四步。耗时 < 1 分钟，省下反复问用户的成本。

### Step 1 · 读全局总索引
```
Read <你的工作区根>/_ACTIVE_PROJECTS.md   # Windows 例：D:/<你的工作区文件夹>/_ACTIVE_PROJECTS.md
```
拿到：当前活跃项目清单、RACI、各项目阻塞状态、最近交接点。这是「现在手头有哪些事」的总览。

### Step 2 · 读账号级真源 MEMORY
```
Read ~/.workbuddy/MEMORY.md
```
拿到：**已固化、永不再问 Steven** 的终态硬事实。关键段：
- 🔴「公众号文章 · 取模版与 VI 总入口」——优先来这取模版 + MedXpert 红 VI 色系 + 三码路径
- 公众号真实号名 = **MedXpert**（CTA 写「关注【MedXpert】」，禁 WorkBuddy 紫）
- 推送草稿箱 4 大阻塞
- 发布闸门铁律（平台判可疑 → 不申诉）
- 密钥投递铁律（DPAPI / key_drop，禁明文）
- 署名/版权体系（MedXpert vs SynomosAI）

### Step 3 · localmem 语义召回（兜底）
用 localmem MCP 工具：`recall_memory`（已灌 15 条跨工作区种子）或 `search_memory`。
- 模型缓存：`<你的工作区根>/_localmem_models`（**必须保留/备份，断网也可搜；模型下载源已 401 不可再拉**）
- 召回取 limit=5~8，文件层已加载的硬事实即使语义分低也能命中
- 典型问题验证过可命中：品牌色、VI、号名、推送阻塞、项目索引、微信预览坑、发布闸门、SOP

### Step 4 · 扫近 14 天项目级 MEMORY
```
Glob <你的工作区根>/*/.workbuddy/memory/MEMORY.md  → 读最近修改的
```
拿到：各工作区自己沉淀的项目铁律（如本次 2026-09-03 工作区的「三码 base64 内联」「CTA 去 WorkBuddy」「VI 铁律」）。

## 二、真源层级（避免冲突时听谁的）

1. **第一真源 = 文件层**：`_ACTIVE_PROJECTS.md` + 账号 MEMORY.md + 项目 MEMORY.md。冲突以文件层为准。
2. **第二层 = localmem 语义层**：仅作兜底召回，不写新事实（写事实走 Step 2 文件层）。
3. **localmem 只负责"我想不起来时兜底"**，不替代文件层。

## 三、已灌种子速查（localmem 库 15 条核心）

| id | 内容 | 命中查询示例 |
|---|---|---|
| 4 | MedXpert 品牌名 + 红 VI 色系 + 模版路径 | 「公众号品牌色用什么」 |
| 6 | 推送草稿箱 4 大阻塞 | 「推草稿箱卡在哪」 |
| 9 | 发布闸门铁律（平台判可疑不申诉） | 「发布前平台判可疑怎么办」 |
| 10 | 密钥投递铁律（DPAPI/key_drop） | 「密钥怎么投安全」(需 limit≈8) |
| 13 | 进行中 6 项目指针 | 「现在哪些项目在做」 |
| 14 | 微信 X5 预览坑 + LAN 通道 | 「微信里图不显示」 |
| 15 | 内容发布运营团 SOP | 「发布流程怎么走」 |

> 注：id10 语义分偏低，靠 Step 2 文件层加载双保险；新会话仍先跑 Step 2。

## 四、Durability 提醒（已踩过的坑）

- ⚠️ `<你的工作区根>/_localmem_models` 嵌入模型缓存**必须保留并备份**——验证时从 HuggingFace 重拉返回 **401**（cas-server 不可达）。已写入向量永久可搜；但**未来想再加新种子必须靠这个本地缓存**，删了就写不进新记忆（旧记忆照常能搜）。
- ⚠️ localmem 是二级召回，主角永远是文件层。别因为有了 localmem 就偷懒不写 `_ACTIVE_PROJECTS.md` / MEMORY.md。

## 五、何时补充种子（write 路径）

发现新终态硬事实（Stevent 拍板、不再变）时：
1. 先写文件层：账号 MEMORY.md 顶部「公众号取模版」段 / 项目 MEMORY.md
2. 再用 localmem `store_memory` 写一条语义种子（tags 含 medxpert / publish / continuity 等）
3. 验证 `recall_memory` 能命中后再算完成

## 六、DoD（完成标准）

- [ ] Step 1~4 全跑完，未跳过
- [ ] 连续性敏感任务执行前已掌握「号名/VI/QR/阻塞/密钥」等已固化项
- [ ] 未向用户重复询问已定稿事项
- [ ] 若发现新终态事实，已落文件层 + localmem

---

## 版权与许可

- © 2026 SynomosAI。本技能按 MIT 许可证开源（见 LICENSE.md）；软件依 LICENSE 使用，零数据收集。
- **知识版权声明**：本作品汇集的方法论、协议流程与结构化知识，其编排与原创表达归 SynomosAI 所有；未经书面许可，不得复制、转载、摘编、转售或用于训练任何模型 / 商业系统。
- **免责声明**：本作品按「现状」（AS IS）提供，不提供任何明示或暗示担保；使用风险由使用者自行承担，因使用所致任何损失作者不承担责任。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | 本包无独立代码文件（纯文档/理论件） | — |
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

**本包补充（包级许可事实）**：本包无独立代码文件（纯文档与理论文本件），整体**保留所有权利（All Rights Reserved）**；不适用任何代码许可（含 MIT / Apache-2.0）。
