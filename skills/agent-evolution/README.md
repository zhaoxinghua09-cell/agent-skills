[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

# agent-evolution

AI 团队「复盘→固化」进化飞轮。当某席数字员工完成一单任务、或用户要求「复盘/进化/沉淀经验/固化经验」时调用。提取本次可复用经验，判定沉淀为技能(SkillManage,动作型)还是记忆(memory,信息型)，并回写该席能力卡的进化记录，使团队下次更强。触发词：复盘、进化、沉淀经验、固化经验、agent-evolution、能力提升。

## 使用

- **AI 代理**：读取 `SKILL.md`（frontmatter 的 name/description 决定是否适用；正文为执行步骤）。
- **人类读者**：读取 `SKILL.md` 与 `AGENTS.md`。

## 文件

- `SKILL.md` — 主说明书
- `AGENTS.md` — AI 代理说明书
- `llms.txt` — AI 可读索引
- `scripts/evolution_check.py` — 能力卡进化记录检查器（2026-11-04 新增，代码 MIT）
- `LICENSE` / `LICENSE.md` — 许可声明

<!-- 生成：2026-10-15 · agent-skills 骨架批量升级 -->

---

🛡️ **Part of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos)** — the 24-node AI-agent governance lifecycle (SPEC → PLAN → GATE → AUDIT → EVO): red-team, injection shield, leak scan, hard gates, LGD three-law badges.
One-command install: `openclaw plugins install clawhub:governanceos`
