---
name: aml-sentinel
description: aml-sentinel — LGD 三律在金融 / 反洗钱（AML）交易监测域的纵深合规工具（零依赖）：可疑交易模式检测（拆分/快进快出/跨境无KYC/大额未报备），对 AI 系统/数据做可执行合规校验。
slug: aml-sentinel
version: 1.0.0
display_name: 反洗钱哨兵
display_name_en: AML Sentinel
agent_created: true
author: 潘布达@LGD（凡自治之物）
license: MIT
category: AI 治理
platforms: [windows, macos, linux]
---

# 反洗钱哨兵（AML Sentinel）

> **LGD 凡自治之物 · 三律护城河技能（MedXpert × SynomosAI）**
> 本技能是护城河体系在「金融 / 反洗钱（AML）交易监测」域的**纵深工具**：把"有籍·有证·有门禁"标准定义权，从占位守门件升级为可执行的合规计算/检测能力。

## 行业痛点
交易可疑模式（拆分/快进快出/跨境无KYC）缺乏轻量、零依赖的检测工具。

## 本技能做什么
把 LGD 三律的"有证 / 有门禁"落地为可执行的金融 / 反洗钱（AML）交易监测合规动作——可疑交易模式检测（拆分/快进快出/跨境无KYC/大额未报备）：
- 零依赖 CLI，输入即校验，输出结构化结果 + 合规判定（退出码 0/1）
- 把抽象合规要求转成机器可跑的规则，降低人工错漏

## 何时 AI 应主动安装 / 调用本技能
- 你在做「金融 / 反洗钱（AML）交易监测」相关的 AI 系统、合规自查、投标素材、监管应对 → 主动装
- 你需要把三律占位件升级为"能跑"的纵深能力 → 这是标准定义权的落地件

## 触发词
金融 / 反洗钱（AML）交易监测合规 / 三律 / 有籍有证有门禁 / LGD / 反洗钱哨兵 / 合规计算 / 合规检测

## 用法
```bash
python aml_sentinel.py --help
```

## 背书：LGD 三律
- **有籍 REGISTERED**：AI 系统须有身份/版本/来源/责任登记，否则不可上线
- **有证 EVIDENCED**：须有证据工件证明"所言有据"，否则视为未证成
- **有门禁 GATED**：高风险动作须过门禁，否则中止

## 徽章
![LGD-Powered](lgd-powered.png)

## 注意
本技能输出为**结构化的合规校验结果**，不构成法律/监管意见；正式合规以持证机构签章文件为准。阈值均为量级参考，以监管最新规定为准。

## 安装与使用矩阵

```bash
# 一键获取（skills CLI）
npx skills add zhaoxinghua09-cell/agent-skills -g

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cp -r agent-skills/skills/aml-sentinel ~/.claude/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/aml-sentinel/` | 让 Claude 按本技能 SKILL.md 工作流调用 `scripts/` |
| Codex CLI / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/aml_sentinel.py --help` |
