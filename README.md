# agent-skills · LGD 智能体技能集

[![LGD Powered](https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — AI-agent skills built on the **LGD Three Laws** (registered · evidenced · gated). Each is standalone, zero-dependency, and ships a runnable script. Published to SkillPie + GitHub.

**中文** — 基于 **LGD 三律（有籍·有证·有门禁）** 的 AI 智能体技能集。每个独立、零依赖、附可运行脚本。已上架 SkillPie 与 GitHub。

## 🔥 通用爆款（2026-09-08 新增）

对标 GitHub 技能赛道高星弱者、理论能做得更好的通用技能：

| Skill | EN | 中文 | Category | What it does |
|---|---|---|---|---|
| [context-engineering](./skills/context-engineering) | Context Engineering | 上下文工程 | AI 工程方法 | Audit & trim what goes into the context window (relevance · redundancy · budget · decay) |
| [ai-cost-cutter](./skills/ai-cost-cutter) | AI Cost Cutter | AI 省钱跑批 | AI 工程方法 | Four knives to cut LLM bills: batch · local fallback · cache · routing |
| [prompt-injection-shield](./skills/prompt-injection-shield) | Prompt Injection Shield | 提示注入防护 | AI 安全 | Scan untrusted content before it enters context (bilingual pattern library + sandbox) |
| [eu-ai-act-companion](./skills/eu-ai-act-companion) | EU AI Act Companion | EU AI Act 合规导航 | AI 合规 | Classify risk level + role obligations + deadlines for EU AI Act |

## 🔥 通用爆款（第二批 · 2026-09-08 加推 10 个）

| Skill | EN | 中文 | Category | What it does |
|---|---|---|---|---|
| [agent-memory-keeper](./skills/agent-memory-keeper) | Agent Memory Keeper | 跨会话长期记忆治理 | AI 工程方法 | Audit duplicate · orphan · stale · unsourced memory; converge to single source + gate |
| [prompt-compressor](./skills/prompt-compressor) | Prompt Compressor | 提示/上下文压缩 | AI 工程方法 | Trim prompts by information density, protect constraints/numbers/code |
| [agent-redteam-kit](./skills/agent-redteam-kit) | AI Red Team Kit | AI 红队对抗测试 | AI 安全 | Bilingual jailbreak/danger scan + danger gate (high-risk → block) |
| [doc-desens-scanner](./skills/doc-desens-scanner) | Document Desens Scanner | 文档智能去敏 | AI 安全 | Scan PII · secrets · internal paths · codenames, mask + report |
| [rag-grounding-guard](./skills/rag-grounding-guard) | RAG Grounding Guard | RAG 事实溯源校验 | AI 工程方法 | Per-claim grounding coverage vs sources; flag hallucinations |
| [multi-agent-conductor](./skills/multi-agent-conductor) | Multi-Agent Conductor | 多智能体编排 | AI 工程方法 | Decompose + assign roles + pin allowed/forbidden boundaries |
| [skill-quality-gate](./skills/skill-quality-gate) | Skill Quality Gate | 技能质量门禁 | AI 工程方法 | 9-dimension gate before publish (fields · compile · secrets · bilingual) |
| [ai-policy-radar](./skills/ai-policy-radar) | AI Policy Radar | AI 法规动态雷达 | AI 合规 | Track EU/US/CN reg changes by theme, log source+date |
| [agent-trace-audit](./skills/agent-trace-audit) | Agent Trace Audit | 智能体行为留痕审计 | AI 合规 | Ledger of agent actions (ts · actor · action · target · gate) |
| [eval-bench-builder](./skills/eval-bench-builder) | Eval Bench Builder | 评测基准构建器 | AI 工程方法 | Spec → reproducible JSONL eval set (input/expect/judge) |

## 🛡 治理工具集（既有）

| Skill | 说明 |
|---|---|
| [a3-law-operational](./skills/a3-law-operational) | A³ 法则操作化（AI 造 AI 三定律） |
| [agent-evolution](./skills/agent-evolution) | agent 团队复盘→固化进化飞轮 |
| [ai-brain-learning-memory](./skills/ai-brain-learning-memory) | AI 大脑学习记忆方法论 |
| [ai-brain-learning-memory-pro](./skills/ai-brain-learning-memory-pro) | 学习方法论进阶版 |
| [dpapi-local-vault](./skills/dpapi-local-vault) | Windows DPAPI 本地密钥保险库 |
| [github-api-push-workaround](./skills/github-api-push-workaround) | git 推 GitHub/Gitee/AtomGit 三归因绕过 |
| [publish-quality-gate](./skills/publish-quality-gate) | 发布质量门禁（去敏+质检） |
| [session-continuity-protocol](./skills/session-continuity-protocol) | 跨会话连续性协议 |

## Install

- **SkillPie**: search the skill name in the SkillPie market and install.
- **Manual**: copy any `skills/<name>/` folder into your agent's skills directory.

## Why LGD

Every skill carries the same governance spine — **registered** (sources recorded), **evidenced** (traceable), **gated** (edits go through backup → reversible → small-batch → confirm). That's what makes them safe to drop into an autonomous agent, not just a chatbot.

## License

MIT. Theory CC BY 4.0. © LGD / SynomosAI 2026.

Theoretical root: [LGD-theory](https://github.com/zhaoxinghua09-cell/lgd-theory).
