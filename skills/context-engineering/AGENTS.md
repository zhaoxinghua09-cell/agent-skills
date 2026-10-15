# AGENTS.md — AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`context-engineering`
一句话定位：当用户说『AI越来越笨/答非所问/忘了前面的设定』『上下文太长』『token烧太快』『RAG召回不准』，或要设计/优化 agent 的提示、记忆、检索、工具编排时使用。把『上下文窗口里到底该放什么』当成一门工程：审计相关性·冗余·预算·衰减 四维度，给出裁剪/检索/记忆/门禁四步流程与可运行脚本（上下文预算计算器+审计清单生成器）。与 prompt engineering 的区别：prompt 是写一句话，context engineering 是设计 AI 每轮看到的全部信息。触发词：上下文工程、context engineering、上下文窗口、上下文污染、上下文衰减、context rot、token预算、RAG召回、记忆编排、agent上下文、长上下文优化。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员。调用入口为 `SKILL.md`：AI 代理应先读 `SKILL.md`，按其 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览（如存在） |
| `llms.txt` | 面向 AI 的轻量索引（如存在） |
| `scripts/`、`assets/` 等 | 技能执行所需资源（按需） |

## 三、可改 / 不可改边界（Editable / non-editable boundary）

### 可以改
- 本技能自身的文档、脚本与配置；按主题新增资产并同步更新 `SKILL.md` 说明。

### 不可改（改动即视为合规偏差）
- **许可与署名声明**：LICENSE / 许可口径（保留所有权利）不得删除或弱化。
- **任何"文件即证据"类声明**：版本号、日期、权属、DOI、徽章来源。

> 代理若判断某项改动触及上述边界，默认停下来并在变更记录里显式提问。

## 四、给代理的行为准则（Agent rules of engagement）

- **先读后写**：改任何文件前先读原文件，理解既有约定。
- **最小改动**：只做被要求的改动，不顺手重构。
- **不做远端写操作**：不执行 `git push`、不调用远端发布接口；远端写入是人工步骤。
- **如实报告**：无法确认的事项标为 TODO，不要编造。

<!-- 生成：2026-10-15 · agent-skills 骨架批量升级（豆包侧，零积分本地执行） -->
