# Changelog

本仓库所有值得注意的变更都会记录在此文件。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 加固（2026-11-18 晚，升至 2.0.5 / 2.1.1 / 2.1.1 / 1.1.0）

- 四包各补 **10 条硬规则（MUST / NEVER）** 与 **「什么时候不用（Not for）」边界段**。
- `summarize-pro` 修复一处文档自相矛盾：前文称"不提供可执行入口"，后文又列工具链。
- 新增「三条命令上手」，所有示例参数均与 argparse 实签核对（吸取 `--draft` 教训）。
- `lgd-skill-review` 新增 `--token`（E:A:R 说明性占比 / 填充语 / 重复段）与 `--multi-role`（规范 / 代码 / 安全 / 设计四视角独立评分），均为附加报告、不参与计分。
- 效果：四包 design 视角 80 → 100；规则占比 1% → 4–9%；说明性内容 72% → 55–64%。

### 发布（2026-11-18，外部回评 4×100 PASS）

- 四包全部升版并对外发布，**LGD-Eval 独立账号从公开网络 clone 后实跑复评，四包均 100/100 PASS、零阻断**：
  - `summarize-pro` **2.0.4**（修 `citecheck` 参数：文档曾写 `--draft`，实际只有 `--file`，照文档敲会直接失败）
  - `debug-pro` **2.1.0**（零依赖三命令工具链，10 条黄金集）
  - `wechat-viral-topic` **2.1.0**（11 条黄金集，合规红线单列）
  - `lgd-skill-review` **1.0.0**（六维证据式评测器：结构/一致性/可复现/卫生/可发现/许可，含阻断项、P0/P1 整改清单、复跑命令、5 条自检、16→100 闭环 demo）
- 新增 `chain.json` 链式路由：四包互为上下游，输出后按 `when → to → handoff` 自动接力。
- 评测准入：发布前须过 `_gate_publish.py` 硬门禁（四包必须 100 分 PASS），自测证明其"会拦也会放"。

### 新增（技能 v2.0 工程化三件，2026-11-18）

- `summarize-pro` 升级至 **2.0.1**：新增 `scripts/summarize_pro.py`，三个子命令 `extract`（抽日期/数字/说话人/待办/决策/条件句并生成骨架）、`citecheck`（逐句抽事实 token 回原文比对，输出不可溯源清单）、`selfcheck`（按格式族断言必备要素），统一 `{ok,error_id,data}` 输出与 S001–S006 错误码。10 条黄金集可复跑（日期混写、百分比、待办归属、决策、条件、过短拒答、时间线、要点条数、溯源正反控）；demo 基于 876 字真实需求评审转写，故意把 `1.8%` 改成 `1.2%`、`11月25日` 改成 `11月23日` 并由 `citecheck` 当场抓出。`docs/FORMATS.md` 为五格式族机器可校验口径，与代码断言同源。原 1.4.4 版中与实际实现不符的 CLI 参数已剔除。
- `debug-pro` 升级至 **2.0.0**：新增 `tools/debughunt.py`，`triage`（异常类型/栈首帧 file:line:func/退出码/HTTP 状态/时间戳/路径/端口）、`envsnap`（含 KEY/TOKEN/SECRET/PASS/CRED/AUTH/COOKIE 的环境项强制剔除）、`reprocheck`（复现五要素判分），错误码 D001–D005；10 条黄金集 10/10 PASS；保留旧 `debug_check.py` 兼容。
- `wechat-viral-topic` 升级至 **2.0.0**：新增 `tools/topicguard.py`，`scan`（数字带单位/时间窗口/平台/#话题#/冲突句/痛点句/读者原话 → 选题卡，无信号拒答 W004）、`riskcheck`（医疗声明/绝对化/收益承诺/诱导分享为 RED，无出处断言为 YELLOW，输出 BLOCK/WARN/PASS）、`titlecheck`（≤34 字、公式类型、红线检测），错误码 W001–W004；11 条黄金集 11/11 PASS；demo 证明四类红线全拦且干净稿不误杀。
- 三者均零第三方依赖（纯标准库可跑），`description` 英文前置，中文置于 `description_zh`；脚本以 MIT 提供，理论文本保留原许可。


### 新增（技能库优化 · 第一批，2026-11-04）

- 20 个技能的脚本新增 `--selftest` 自检（临时夹具跑真实检查逻辑，断言「应过/应拦」两类判定，零第三方依赖）：`agent-boarding-pass`、`agent-kill-switch`、`agent-loop-guard`、`agent-memory-keeper`、`agent-output-registry`、`agent-redteam-kit`、`agent-trace-audit`、`ai-brain-learning-memory-pro`、`ai-content-discloser`、`ai-cost-cutter`、`ai-decision-log`、`ai-incident-log`、`ai-policy-radar`、`ai-reply-heuristics`、`ai-usage-policy`、`ai-vendor-checklist`、`aml-sentinel`、`batch-renamer`、`bias-auditor`、`citation-coverage-check`。普通调用行为不变（自检为纯附加）。

### 新增（技能库优化 · 第二批，2026-11-04）

- 20 个技能的脚本新增 `--selftest` 自检（临时夹具跑真实检查逻辑，断言「应过/应拦」两类判定，零第三方依赖）：`clin-eval-route-picker`、`contract-clause-check`、`contract-interact-checklist`、`csv-slice`、`data-export-check`、`data-minimizer`、`data-rights-guard`、`dir-organizer`、`disk-scan`、`doc-desens-scanner`、`dpapi-local-vault`、`dup-finder`、`eu-ai-act-companion`、`eval-bench-builder`、`evidence-chain-builder`、`evidence-chain-check`、`fact-check-guard`、`fin-reg-calc`、`fund-fee-calc`、`gov-disclosure-check`。普通调用行为不变（自检为纯附加）。注：`dpapi-local-vault` 的 DPAPI 加解密为 Windows 原语，非 Windows 平台自检以可逆测试封套替身该原语，存储/取回的解析、信封、标注与隐藏逻辑均实跑，自检输出中明示未实跑部分。

### 新增（技能库优化 · agent-evolution 转实跑，2026-11-04，仓主批准）

- `agent-evolution` 新增真实检查器 `scripts/evolution_check.py`（零依赖）：校验本技能流程第 5 步的回写产物——能力卡「进化记录」栏 / 进化日志的条目格式（`[YYYY-MM-DD] 沉淀：<目标> — <升级说明>`）、日期真实性与不晚于今天、同席去重与日期不递减、能力卡「进化记录」栏与席位标识的结构校验；`--selftest` 14 条断言（合规须过 + 坏日期/缺段/未来日期/重复/乱序/缺栏/空席位须拦，临时夹具）。SKILL.md 版本 1.1.0 → 1.2.0 并新增「配套检查器」节。随之 `lgd-evo --verify` 的唯一节点由 DOC-ONLY 转为真实 LIVE（LIVE=1，rc=0），空心枢纽自此有实跑节点。
- `agent-evolution` 许可事实修订（同日，仓主批准）：SKILL.md 文末「本包补充（包级许可事实）」原称「本包无独立代码文件……不适用任何代码许可」，因新增上述代码已失实，修订为：文档与理论文本 CC BY 4.0 不变，新增代码按本仓代码层惯例 MIT；分层许可表「代码」行同步更新。§3.2 统一块系整体照录未删改，其中修订前状态的行以修订后的本包补充为准。技能 AGENTS.md 同步加修订注。

### 修复

- `lgd-evo` 中枢 `--verify` 诚实化：唯一节点 `agent-evolution` 为纯文档技能（无可运行脚本），原实现报 `LIVE=0 / ERROR=0` 且退出码 0，呈「零实跑的全绿」。现分级为 `DOC-ONLY`（NOT VERIFIED，未实跑、未验证），`LIVE=0` 时打印 `HOLLOW` 警告并以退出码 1 收尾；`--json-out` 证据新增 `doc_only` 与 `hollow` 字段。

## [1.0.0] — 2026-09-11

### 首次正式发布

本版本为 **agent-skills** 技能库的首个正式发布版本，包含 **87 个零依赖 AI Agent 治理技能**，覆盖从智能体身份签发、权限门禁、提示词注入防护，到证据链留痕、合规对齐（EU AI Act / ISO IEC 42001）与记忆治理的完整治理链路。

### 核心特性

- **零第三方依赖**：全部技能仅使用 Python 标准库实现，无供应链风险，可离线运行、可自托管。
- **确定性输出**：LLM 仅负责产出 JSON IR，判定与规则由代码兜底，返回规则码，结果可复现、可回归测试。
- **MIT 许可**：可自由使用、修改、商用，无需逐一授权。
- **多客户端适配**：技能同时适配 Claude Code · Codex · Cursor · WorkBuddy 等主流 Agent 客户端。
- **理论支撑**：核心治理技能基于 LGD（Lifecycle Governance Doctrine，全程治理论）「有籍 · 有证 · 有门禁」三律设计。

### 技能清单（按治理域分组）

#### Agent 身份与权限（11）

- `agent-boarding-pass`
- `agent-kill-switch`
- `agent-loop-guard`
- `agent-trace-audit`
- `agent-output-registry`
- `tool-call-guard`
- `gate-policy-generator`
- `multi-agent-conductor`
- `agent-redteam-kit`
- `lgd-three-laws-auditor`
- `skill-quality-gate`

#### 安全与注入防护（11）

- `prompt-injection-shield`
- `prompt-injection-drill`
- `prompt-leak-scanner`
- `mcp-security-scan`
- `regex-sandbox`
- `hash-check`
- `env-var-audit`
- `contract-interact-checklist`
- `wallet-address-check`
- `api-resilience`
- `output-schema-guard`

#### AI 治理与合规（19）

- `eu-ai-act-companion`
- `lgd-certify`
- `lgd-badge-issuer`
- `lgd-badge-verify`
- `ai-content-discloser`
- `ai-usage-policy`
- `ai-vendor-checklist`
- `ai-policy-radar`
- `ai-reply-heuristics`
- `bias-auditor`
- `model-card-generator`
- `data-export-check`
- `data-rights-guard`
- `data-minimizer`
- `doc-desens-scanner`
- `gov-disclosure-check`
- `eval-bench-builder`
- `fact-check-guard`
- `citation-coverage-check`

#### 上下文与记忆治理（8）

- `context-engineering`
- `agent-memory-keeper`
- `prompt-version-control`
- `prompt-compressor`
- `model-router`
- `ai-cost-cutter`
- `rag-grounding-guard`
- `ai-decision-log`

#### 证据链与留痕（7）

- `evidence-chain-builder`
- `evidence-chain-check`
- `ai-incident-log`
- `lgd-crypto-guard`
- `lgd-gov-guard`
- `lgd-law-ethic`
- `lgd-fin-guard`

#### 医械与行业专项（9）

- `udi-format-validator`
- `clin-eval-route-picker`
- `pmcf-plan-check`
- `health-claim-guard`
- `aml-sentinel`
- `fin-reg-calc`
- `travel-rule-check`
- `fund-fee-calc`
- `token-disclosure-check`

#### 通用提效工具（14）

- `csv-slice`
- `json-tidy`
- `text-stats`
- `text-replace`
- `batch-renamer`
- `dir-organizer`
- `disk-scan`
- `dup-finder`
- `md-link-audit`
- `changelog-draft-gen`
- `contract-clause-check`
- `invoice-risk-scan`
- `kyc-checklist-gen`
- `loan-rate-disclosure`

#### LGD 原生技能（治理方法论）（8）

- `a3-law-operational`
- `agent-evolution`
- `ai-brain-learning-memory`
- `ai-brain-learning-memory-pro`
- `dpapi-local-vault`
- `github-api-push-workaround`
- `publish-quality-gate`
- `session-continuity-protocol`

### 文档与元数据

- 新增 `LICENSE`（MIT License，Copyright © 2026 SynomosAI），GitHub 已识别为 MIT。
- 补充仓库 topics：`agent-skills` · `ai-governance` · `ai-safety` · `ai-compliance` · `eu-ai-act` · `iso42001` · `medical-device-compliance` · `memory-governance` · `prompt-governance` · `skill-library` · `workbuddy` · `zero-dependency` 等 14 项。
- 仓库主页指向技能索引页：<https://medxpert.cn/skills>。
- 新增 `CHANGELOG.md`（本文件）。

### 链接

- 技能索引页（含全部技能说明与结构化数据）：<https://medxpert.cn/skills.html>
- 治理理论主页（LGD）：<https://medxpert.cn/lgd.html>
- 理论全文仓库：<https://github.com/zhaoxinghua09-cell/lgd-theory>

[1.0.0]: https://github.com/zhaoxinghua09-cell/agent-skills/releases/tag/v1.0.0
