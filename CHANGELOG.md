# Changelog

本仓库所有值得注意的变更都会记录在此文件。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
