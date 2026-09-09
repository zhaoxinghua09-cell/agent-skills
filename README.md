<div align="center">

<img src="lgd-powered.png" width="150" alt="LGD Powered"/>

# agent-skills · AI Agent 治理技能标准库

**开源版「AI 治理操作系统的 Skill 层」——让每一个 AI 输出：有籍 · 有证 · 有门禁**

[![Trendshift](https://img.shields.io/badge/Trendshift-submitting-14B8A6)](https://trendshift.io/)
[![GitHub stars](https://img.shields.io/github/stars/zhaoxinghua09-cell/agent-skills?style=social)](https://github.com/zhaoxinghua09-cell/agent-skills/stargazers)
[![last commit](https://img.shields.io/github/last-commit/zhaoxinghua09-cell/agent-skills)](https://github.com/zhaoxinghua09-cell/agent-skills/commits)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-87%2B-14B8A6)](#-lgd-护城河系列)
[![Zero-dependency](https://img.shields.io/badge/zero--dependency-stdlib%20only-0B1F3A)](#)
[![Platforms](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20WorkBuddy-blueviolet)](#-安装矩阵)

[安装](#-安装矩阵) · [LGD 护城河系列](#-lgd-护城河系列) · [通用技能](#-通用爆款2026-09-08-新增) · [理论](https://github.com/zhaoxinghua09-cell/lgd-theory) · [在线门户](https://zhaoxinghua09-cell.github.io/lgd-hub/) · [反馈](https://github.com/zhaoxinghua09-cell/agent-skills/issues)

`AI治理` `LGD三律` `Agent安全` `合规自动化` `提示词治理` `记忆治理` `技能工程` `金融合规` `区块链合规`

简体（本页） · English（各技能 README 自带 EN 段） · [LGD 理论总账](https://github.com/zhaoxinghua09-cell/lgd-theory)

</div>

## 安装矩阵

```bash
# 方式一：skills CLI 一条命令（推荐）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 方式二：手动克隆 + 拷贝需要的技能
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/<skill-name> ~/.claude/skills/   # Claude Code 示例
```

| Agent | 技能目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex CLI | `~/.codex/skills/`（或按官方 skills 路径） |
| Cursor | 项目 `.cursor/skills/` 或全局配置 |
| WorkBuddy | 连接器 → 本地技能目录导入 |
| 其他 Agent | 任何支持 SKILL.md 规范的目录均可，直接拷入 |

> 每个技能目录内 SKILL.md 亦附「安装与使用矩阵」小节，含该技能的运行示例。

---

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
| [lgd-badge-issuer](./skills/lgd-badge-issuer) | LGD Badge Issuer | 徽章签发器 | 闭环·徽章 | 三律全过才签发 lgd-certified 证书（SHA-256 指纹+签发台账），未过拒绝留痕 |
| [lgd-badge-verify](./skills/lgd-badge-verify) | LGD Badge Verifier | 徽章验真器 | 闭环·徽章 | 验证书三重校验：指纹重算防篡改+证据哈希+台账对账（未吊销/未伪造） |
| [ai-content-discloser](./skills/ai-content-discloser) | AI Content Discloser | AI 内容披露生成器 | 广谱·有证 | AI 参与（全生成/辅助/混合）内容一键生成合规披露声明（显式中/EN+隐式元数据+平台贴法），依据《AI生成合成内容标识办法》/EU AI Act Art.50 |
| [agent-boarding-pass](./skills/agent-boarding-pass) | Agent Boarding Pass | 智能体登机牌 | 广谱·三律便携 | 给任何智能体签发可验证『登机牌』：身份+证据哈希+权限白名单+有效期，SHA-256 防篡改，一条命令验真；缺律拒发 |
| [prompt-leak-scanner](./skills/prompt-leak-scanner) | Prompt Leak Scanner | 提示词泄漏扫描器 | 广谱·有门禁 | 提示词发布前扫五类风险：密钥/内网路径/PII/自定义敏感词/自我泄漏后门，高风险 rc=1 拦下 |
| [data-minimizer](./skills/data-minimizer) | Data Minimizer | 给AI前脱敏器 | 广谱·有门禁 | 手机/邮箱/证件/长号/指定人名一键打码再交给 AI，输出脱敏文本+报告 |
| [model-card-generator](./skills/model-card-generator) | Model Card Generator | 模型卡生成器 | 广谱·有籍 | 给任何 AI 系统生成一页身份卡：身份/用途/数据/限制/风险/联系人（MD+JSON） |
| [ai-usage-policy](./skills/ai-usage-policy) | AI Usage Policy Generator | 团队AI使用守则生成器 | 广谱·有门禁 | 按团队/工具/禁区/上报线一键生成一页《AI 使用守则》 |
| [ai-incident-log](./skills/ai-incident-log) | AI Incident Log | AI事故记录器 | 广谱·有证 | AI 失控/误操作事故 JSONL 台账：严重度/模型/处置/复盘字段+报表 |
| [agent-kill-switch](./skills/agent-kill-switch) | Agent Kill Switch | 智能体紧急制动卡 | 广谱·有门禁 | 部署前生成制动卡：停止条件/断权动作/责任人/恢复；--check 缺项 rc=1 拦上线 |
| [ai-reply-heuristics](./skills/ai-reply-heuristics) | AI Reply Heuristics | AI痕迹启发式检查器 | 广谱·有证 | AI 痕迹 0-100 启发式评分：套话/破折号/句长均匀度/排比（附免责，不构成判定） |
| [citation-coverage-check](./skills/citation-coverage-check) | Citation Coverage Check | 引用覆盖率检查器 | 广谱·有证 | 含数字/论断句子的来源标注覆盖率，低于阈值 rc=1 并逐句列缺口 |
| [ai-vendor-checklist](./skills/ai-vendor-checklist) | AI Vendor Checklist | AI供应商尽调清单 | 广谱·有籍 | 10 项 AI 采购尽调（数据权属/训练退出/事故SLA/审计/退出），--score 低于线 rc=1 |
| [prompt-injection-drill](./skills/prompt-injection-drill) | Prompt Injection Drill | 提示词注入演练器 | 广谱·有门禁 | 为 system prompt 生成 8 类注入攻击演练用例+期望行为，上线前红队自测 |
| [ai-decision-log](./skills/ai-decision-log) | AI Decision Log | AI决策留痕器 | 广谱·有籍+有证 | AI 参与决策 JSONL 留痕：决策/模型/证据哈希/人审人，report 标出无人审项 |
| [loan-rate-disclosure](./skills/loan-rate-disclosure) | Loan Rate Disclosure Check | 借贷利率披露校验 | 金融 | 借贷报价须年化口径披露 + 不超基准4倍司法上限，超线即拦（TH-LGD-015） |
| [kyc-checklist-gen](./skills/kyc-checklist-gen) | KYC Checklist Generator | KYC 材料齐备清单 | 金融 | 一键生成个人/企业 KYC 必备材料清单并核算齐备度，缺项即 FAIL（TH-LGD-016） |
| [invoice-risk-scan](./skills/invoice-risk-scan) | Invoice Risk Scan | 发票要素风险扫描 | 金融/财税 | 报销入账前扫税号格式/金额/日期合理性，异常即拦（TH-LGD-017） |
| [fund-fee-calc](./skills/fund-fee-calc) | Fund Fee & Net Return Calc | 资管费率净收益试算 | 金融 | 三费总成本+净收益试算；宣传含保本承诺即 FAIL（资管新规红线）（TH-LGD-018） |
| [wallet-address-check](./skills/wallet-address-check) | Wallet Address Check | 链上地址格式校验 | 区块链 | 转账前校验 EVM/BTC系/TRON 地址格式与链系归属，可疑即拦（TH-LGD-019） |
| [token-disclosure-check](./skills/token-disclosure-check) | Token Disclosure Check | 代币信息披露检查 | 区块链 | 白皮书必备要素核查（总量/分配/锁仓/团队/风险），含收益承诺即 FAIL（TH-LGD-020） |
| [contract-interact-checklist](./skills/contract-interact-checklist) | Contract Interact Checklist | 合约交互风险清单 | 区块链 | 交互前六项自检（审计/假合约/授权额度/撤销/私钥/小额试单），未完成即拦（TH-LGD-021） |
| [contract-clause-check](./skills/contract-clause-check) | Contract Clause Check | 合同高危条款扫描 | 法律 | 签前扫必备条款与高危表述（最终解释权/自动续期/违约金>30%），缺项即拦（TH-LGD-022） |
| [health-claim-guard](./skills/health-claim-guard) | Health Claim Guard | 健康宣称合规扫描 | 医疗健康 | 宣传文案扫违规疗效宣称（根治/治愈/无副作用），保健食品缺警示语即拦（TH-LGD-023） |
| [data-export-check](./skills/data-export-check) | Data Export Check | 数据出境合规自检 | 数据合规/政务 | 出境前五项义务自检（分级/单独同意/PIA/标准合同/留痕），缺项即拦（TH-LGD-024） |

> **Batch C 跨域首占（2026-09-08 · P-045）**：把三律逐条翻译进金融/法律/政务/隐私计算四大空白域的本域合规语言，做成"标准定义权占位件"——别人可抄功能，抄不走本域翻译与评判权。域码锚定 TH-FIN/LAW/GOV/CRYPT-001。
> **Batch C 纵深工具（2026-09-08 · P-046）**：在占位守门件底座上产 5 个"能跑"的纵深合规工具（金融 calc/AML、法律证据链、政务披露、链上旅行规则），把标准定义权从占位升级为可执行能力。
> **Batch E 广谱爆款（2026-09-08 · P-049）**：把三律做成人人天天用得上的广谱件——AI 内容披露（有证）、智能体登机牌（三律便携）、提示词泄漏扫描（有门禁），覆盖"发 AI 内容 / 接 AI 智能体 / 发提示词"三大高频场景。
> **Batch F 广谱爆款十连发（2026-09-08 · P-050）**：把三律铺进 AI 全使用周期——给 AI 发数据前脱敏、建 AI 有身份卡、管团队有守则、出事有台账、上线有制动卡、读文有痕迹提示、写报告查引用覆盖、采购有尽调清单、上线前注入演练、决策有留痕。
> **Batch G 行业爆款十连发（2026-09-08 · P-051）**：把三律扎进重点监管行业——金融（利率披露/KYC/发票/资管费率）、区块链（地址校验/代币披露/合约交互）、法律（合同条款）、医疗健康（疗效宣称）、数据出境（五项义务），每款都是行业刚需 + 即装即用。

### ⚡ 效率工具家族（Batch H · 广谱爆款 · 2026-09-08 · P-055）

> 调研 awesome-cli-apps 高星品类（批量重命名 f2 / 重复查找 fclones / 磁盘 dust / 批量替换 sd / JSON gron / CSV q / 统计 scc）后的十连发：人人天天用得上的文件与文本利器。**全系列零依赖、默认 dry-run 预览、--apply 才执行、--json 机器可读**。rc=0 成功 / rc=1 发现问题 / rc=2 用法错误。

| Skill | Name | 一句话 |
|---|---|---|
| [batch-renamer](./skills/batch-renamer) | Batch File Renamer | 规则式批量重命名（前缀/序号/查找替换），默认预览 |
| [dup-finder](./skills/dup-finder) | Duplicate File Finder | 三级哈希找重复文件，可一键清副本保留首个 |
| [dir-organizer](./skills/dir-organizer) | Directory Organizer | 按类型把杂乱目录归到 图片/文档/视频… 子目录 |
| [disk-scan](./skills/disk-scan) | Disk Usage Scan | Top N 大文件+子目录占用排行，只读定位空间杀手 |
| [json-tidy](./skills/json-tidy) | JSON Tidy | JSON 格式化/压缩/键排序，解析错误精确定位行列 |
| [csv-slice](./skills/csv-slice) | CSV Slice | CSV 取列/筛选/去重/计数，不打开 Excel 干完活 |
| [text-replace](./skills/text-replace) | Bulk Text Replace | 跨文件批量查找替换（字面量/正则），.bak 自动备份 |
| [text-stats](./skills/text-stats) | Text Stats | 字数/行数/词频TopN/阅读时长，目录批量汇总 |
| [regex-sandbox](./skills/regex-sandbox) | Regex Sandbox | 正则即写即测：匹配/分组/替换预览/标志位 |
| [hash-check](./skills/hash-check) | File Hash Check | 目录 SHA-256 清单生成/校验，防篡改验完整性 |

### 🏥 爆款精品批（Batch I · 医疗器械×3 + 通用×3 · 2026-09-08 · P-061）

> 质量优先精磨批：每款都带**真法规/真工程逻辑**与确定性判定树，非模板量产。医疗器械线（MedXpert 获客面）：UDI 格式校验（GS1 Mod10 + NMPA/EU 双口径）、临床评价路径选择（NMPA 73 号通告 + MDCG 2020-6 判定树）、PMCF 计划完整性检查（MDCG 2020-7 十要素）。通用线：Markdown 链接体检（默认离线 CI 友好）、conventional commits 更新日志生成（last-good 原子写）、环境变量审计（硬编码密钥 + .env.example 账目）。全系列零依赖、JSON IR、修复回执错误码。rc=0 成功 / rc=1 发现问题 / rc=2 用法错误。

| Skill | Name | 一句话 |
|---|---|---|
| [udi-format-validator](./skills/udi-format-validator) | UDI Format Validator | UDI 串体检：GS1 校验位/日期/生产标识/Basic UDI-DI 分型 |
| [clin-eval-route-picker](./skills/clin-eval-route-picker) | Clinical Eval Route Picker | 免临床目录/同品种/临床试验三条路确定性判定（NMPA+EU） |
| [pmcf-plan-check](./skills/pmcf-plan-check) | PMCF Plan Completeness Checker | PMCF 计划十要素过秤，交公告机构前补齐短板 |
| [md-link-audit](./skills/md-link-audit) | Markdown Link Auditor | README 断链就地现形，默认离线、--net 才外呼 |
| [changelog-draft-gen](./skills/changelog-draft-gen) | Changelog Draft Generator | conventional commits → 规范 CHANGELOG 草稿，原子写 |
| [env-var-audit](./skills/env-var-audit) | Env Var Auditor | 环境变量账目对清：未文档化/冗余/硬编码密钥一网打尽 |

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
