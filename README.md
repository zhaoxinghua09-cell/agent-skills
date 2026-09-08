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

## 🔥 痛点型爆款（第三批 · 2026-09-08 加推 10 个 · 直击市场痛点）

| Skill | EN | 中文 | Category | 痛点 → 解法 |
|---|---|---|---|---|
| [output-schema-guard](./skills/output-schema-guard) | Output Schema Guard | 结构化输出校验护栏 | AI 工程方法 | 模型 JSON 缺字段/类型飘 → schema 卡必填·类型·枚举+修复提示 |
| [tool-call-guard](./skills/tool-call-guard) | Tool Call Guard | 工具调用安全闸门 | AI 安全 | agent 误删/误发/越权 → 按副作用分级，删/外发/支付拦截 |
| [model-router](./skills/model-router) | Model Router | 模型路由省成本 | AI 工程方法 | 全用旗舰模型烧钱 → 按复杂度分流到刚好够用的档位 |
| [fact-check-guard](./skills/fact-check-guard) | Fact Check Guard | 事实核查护栏 | AI 工程方法 | 幻觉/编造引用过审 → 逐声明标 已支撑/存疑/无来源 |
| [agent-loop-guard](./skills/agent-loop-guard) | Agent Loop Guard | 失控循环护栏 | AI 工程方法 | agent 跑飞无限循环烧 token → 步数/重复/无进展三路熔断 |
| [bias-auditor](./skills/bias-auditor) | Bias Auditor | 偏见审计 | AI 工程方法 | 输出带群体刻板印象 → 扫群体词/刻板表述+去偏建议 |
| [prompt-version-control](./skills/prompt-version-control) | Prompt Version Control | 提示版本管理 | AI 工程方法 | 提示改乱回不去 → 版本+diff+效果分，可回滚选优 |
| [api-resilience](./skills/api-resilience) | API Resilience | API 韧性 | AI 工程方法 | 外部接口抖动拖垮全场 → 退避重试+限流+熔断+降级 |
| [mcp-security-scan](./skills/mcp-security-scan) | MCP Security Scan | MCP 安全扫描 | AI 安全 | MCP 是新攻击面 → 扫命令执行/文件写/外联/凭证暴露 |
| [data-rights-guard](./skills/data-rights-guard) | Data Rights Guard | 训练数据版权护栏 | AI 合规 | 爬的数据侵权雷 → 查许可证/商用权/署名/来源，缺许可不出集 |

## 🏰 护城河旗舰 · LGD 三律治理系列（2026-09-08）

把「凡自治之物：有籍·有证·有门禁」做成可安装、可传播、可占位的技能集群——这是 LGD 理论的**标准定义权**，是别人抄功能抄不走的护城河。

| Skill | EN | 中文 | 三律 | 作用 |
|---|---|---|---|---|
| [lgd-three-laws-auditor](./skills/lgd-three-laws-auditor) | LGD Three-Laws Auditor | 三律合规自检器 | 总纲 | 把三律做成可自评标准 rubric，出评分卡（定义权载体） |
| [lgd-certify](./skills/lgd-certify) | LGD Certifier | 三律闭环认证 | 有籍+有证+有门禁 | 市场唯一 passport→证据链→门禁→徽章 闭环 CLI |
| [agent-output-registry](./skills/agent-output-registry) | Output Registry | 产出有籍登记器 | 有籍 | 给 AI 产出发"籍"（指纹+模型/版本/权属），可溯源可证 |
| [evidence-chain-builder](./skills/evidence-chain-builder) | Evidence Chain Builder | 论断有证证据链 | 有证 | 论断拆可验证证据链，治幻觉、强举证（不编造） |
| [gate-policy-generator](./skills/gate-policy-generator) | Gate Policy Generator | 权限有门禁生成器 | 有门禁 | 从能力清单生成权限门禁策略（四道门禁+预算闸），防越权/误删误发/失控循环 |
| [lgd-fin-guard](./skills/lgd-fin-guard) | Finance AI Compliance Guard | 金融AI合规守门 | 跨域·FIN | 把三律翻译进持牌机构语境（投顾/风控/反洗钱），占金融空白标准位 |
| [lgd-law-ethic](./skills/lgd-law-ethic) | Legal AI Ethics Guard | 法律AI伦理守门 | 跨域·LAW | 把三律翻译进法律伦理语境（检索/起草/意见辅助），占法律空白标准位 |
| [lgd-gov-guard](./skills/lgd-gov-guard) | Government AI Governance Guard | 政务AI治理守门 | 跨域·GOV | 把三律翻译进政务"不出域"语境（决策辅助/公开答复/数据治理），占政务空白标准位 |
| [lgd-crypto-guard](./skills/lgd-crypto-guard) | Privacy-Compute Guard | 隐私计算守门 | 跨域·CRYPT | 把三律翻译进密文/最小化语境（联邦/密文/脱敏），占隐私计算空白标准位 |
| [fin-reg-calc](./skills/fin-reg-calc) | Finance AI Compliance Calculator | 金融AI合规计算 | 跨域·FIN 纵深 | 把三律"有证/有门禁"落地为投资者适当性+大额阈值可执行计算 |
| [aml-sentinel](./skills/aml-sentinel) | AML Sentinel | 反洗钱哨兵 | 跨域·FIN 纵深 | 可疑交易模式检测（拆分/快进快出/跨境无KYC/大额未报备） |
| [evidence-chain-check](./skills/evidence-chain-check) | Legal Evidence-Chain Check | 法律证据链校验 | 跨域·LAW 纵深 | 证据链时间单调/主体一致/哈希链不断裂自动校验 |
| [gov-disclosure-check](./skills/gov-disclosure-check) | Gov Disclosure Check | 政务公开披露校验 | 跨域·GOV 纵深 | 强制披露字段（决策依据/责任部门/时限/救济/数据来源）校验 |
| [travel-rule-check](./skills/travel-rule-check) | Travel-Rule Check | 旅行规则校验 | 跨域·CRYPT 纵深 | VASP 转账收发方 KYC（姓名+账号/地址+地理）超阈强制校验 |

> **Batch C 跨域首占（2026-09-08 · P-045）**：把三律逐条翻译进金融/法律/政务/隐私计算四大空白域的本域合规语言，做成"标准定义权占位件"——别人可抄功能，抄不走本域翻译与评判权。域码锚定 TH-FIN/LAW/GOV/CRYPT-001。
> **Batch C 纵深工具（2026-09-08 · P-046）**：在占位守门件底座上产 5 个"能跑"的纵深合规工具（金融 calc/AML、法律证据链、政务披露、链上旅行规则），把标准定义权从占位升级为可执行能力。

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
