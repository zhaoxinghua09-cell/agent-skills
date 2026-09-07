# Agent Skills Collection（Agent 技能合集）

> 针对 GitHub 头部 Agent Skills 生态的实证弱点，提出并落地的一组差异化技能。方法论调研见 [`docs/`](docs/)。

## 这是什么

2026-09 对 GitHub 头部技能仓库（anthropics/skills、planning-with-files、claude-mem、distilly、alirezarezvani/claude-skills、addyosmani/agent-skills 等，头部集合仓库聚合数千个技能）做内容级弱点分析后，把自家已实战验证的技能按优先级整理发布。每个技能针对头部生态的一个实证弱点：

| 弱点（头部实证） | 对应技能 |
|---|---|
| 崩溃恢复只还原"文件快照"、跨项目被主动隔离 | **session-continuity-protocol** — 跨会话/跨工作区/跨项目连续性协议 |
| 记忆全量捕获无蒸馏、压缩有损丢过数据 | **ai-brain-learning-memory**（+pro）— 零丢失分层记忆蒸馏 |
| 本地服务无认证、API key 明文、无 secret 扫描 | **dpapi-local-vault** — DPAPI 密钥保险库 + 泄露哨兵 |
| 结构合规 ≠ 效果验证、无发布闸门 | **publish-quality-gate** — 四层敏感扫描 + TRACE 五维自测 |
| 无复盘→固化闭环 | **agent-evolution** — 复盘→固化进化飞轮 |
| 方法论碎片化 | **a3-law-operational** — AI 造 AI 三定律 |

## 目录

```
skills/    7 个技能源码包（每包含 SKILL.md，多数含 LICENSE.md / scripts / references）
release/   对应的打包 zip（去敏质检后版本，含 MD5 台账）
docs/      头部弱点调研报告 + 发布质检台账
```

## 安装

任选其一：
- 直接复制 `skills/<name>/` 到你的 Agent 技能目录（如 `~/.workbuddy/skills/` 或 Claude Code 的 skills 目录）；
- 或使用 `release/<name>-v<version>.zip` 解压。

## 版本与署名

各技能版本与归属见其 SKILL.md frontmatter（版本 + author + license）。LGD 理论线技能（agent-evolution / a3-law-operational / ai-brain-learning-memory-pro）© SynomosAI，理论 CC BY 4.0（DOI 10.5281/zenodo.22456647），参照声明回链 [LGD-theory](https://github.com/zhaoxinghua09-cell/lgd-theory)。

## License

- 代码与文档：MIT（各包附 LICENSE）
- LGD 理论内容：CC BY 4.0

本仓库零数据收集、零遥测；技能均为本地优先设计。
