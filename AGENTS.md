---
name: agent-skills
description: LGD/UIBC 治理技能标准库——AI Agent 治理技能生态（skills.sh 兼容，109+ 技能）。向在技能仓工作的 agent 提供完整操作手册：技能规范、验证命令、贡献流程与边界。
---

# AGENTS.md — agent-skills 仓操作手册（六区域版 · G-10 / AAIF 对齐）

> 本文件按 GitHub 官方 2500 仓研究「六核心区域」（commands / testing / project structure / code style / git workflow / boundaries）+ AAIF（agents.md 规范）编写，作为理论号 AGENTS.md 模板 SSOT。
> 语言：英文为主，中文要点补充（与仓双语惯例一致）。

## Persona / 角色

You are an expert contributor to the **agent-skills** standard library: you maintain SKILL.md artifacts, registry entries, docs and CI, and you never modify theory text or license claims without explicit approval.

## 1. Project overview / 项目概览

- **定位**：Agent 集成层（Integration）——把 LGD/UIBC 治理技能装入通用 Agent 技能生态，`skills.sh` 兼容（`npx skills add zhaoxinghua09-cell/agent-skills -g`）。
- **内容**：`skills/*/SKILL.md`（109+ 个技能，frontmatter 规范 + 何时用/用法/流程三节）；docs（规范件）；scripts（工具）；release（发布物）；teams（协作）；llms.txt（AI 索引）。
- **技术栈**：Markdown（SKILL.md）+ YAML frontmatter（agentskills.io 规范级字段）+ Python 3.x stdlib（scripts，零外部依赖）。无锁文件、无依赖清单。
- **许可分层**：代码（.py）MIT；理论文本（SKILL.md/README 文本）保留所有权利——**未经批准不得复制理论文本段落**。
- **关键文件**：`README.md`（入口）、`skills/`（技能本体）、`index.jsonld`（技能图谱）、`llms.txt`（AI 索引）、`CHANGELOG.md`（变更留痕）、`LICENSE`（分层许可）。

## 2. Commands / 可执行命令

```bash
# 技能 frontmatter / 结构全量校验（CI validate.yml 同逻辑，提交前必跑）
python scripts/validate_skills.py            # 109+ 技能全部通过 = 可合入

# 本地结构探针（新增技能后）
python scripts/validate_skills.py --skill skills/<name>

# 注册表/文档一致性（如脚本存在）
python scripts/check_links.py                 # 仓库内链接可达性

# 全量回归（若有测试目录）
python -m unittest discover tests -v          # 技能工具自测
```

> 命令以 `validate.yml`（`.github/workflows/validate.yml`）为权威；CI 与本地必须一致。

## 3. Project structure / 项目结构

| 路径 | 规则 |
|---|---|
| `skills/<skill-name>/SKILL.md` | 技能本体：frontmatter（name/description/license/compatibility/metadata）+ 何时用/用法/流程三节。**一个目录 = 一个技能** |
| `skills/<skill-name>/<脚本>.py` | 技能配套工具：stdlib only，带 `--selftest` 时必须在 CI 通过 |
| `scripts/` | 仓级工具（validate 等）：不可依赖第三方库 |
| `docs/` | 规范件与说明：理论文本，ARR，只可引用不可复制 |
| `release/` | 发布产物：由发布流程生成，禁止手改 |
| `teams/` | 团队/协作文档 |
| `llms.txt` | AI 索引：新增技能后必须同步（若含条目列表） |
| `index.jsonld` | 技能图谱：新增技能后必须同步 |

## 4. Code style & examples / 代码风格与示例

**SKILL.md frontmatter（规范级字段，agentskills.io）**：

```yaml
---
name: <skill-name>                  # 必选，小写连字符
description: "<何时用 + 用法信号词，≤300 字符，信息密度优先>"   # 必选
version: x.y.z
license: MIT                        # 代码许可；理论文本另行声明
compatibility: Cross-platform; zero external dependencies (stdlib only)
metadata: {dependencies: "none"}
---
```

- **正文三节固定**：`## 何时用`（触发条件）→ `## 用法`（步骤/命令）→ `## 流程`（或安全要点）。节名机器可解析，禁止改名。
- **双语惯例**：中文为主，英文要点（EN 段）补充；对外文本中性、无占位。
- **正确示例（描述）**：
  `description: "当用户要求审查合同或询问合同风险时使用；输出风险清单与修改建议，附法条依据与协商话术。"`
- **错误示例（描述）**：空泛、无触发词、超 300 字符、堆叠形容词。

## 5. Git workflow & testing / Git 工作流与测试

- **提交规范**：一行主题 + 影响域前缀（如 `skills(ai-cost-cutter): fix selftest`）；CHANGELOG.md 必须同步。
- **PR 规范**：分支名 `<area>-<change>`；PR 标题镜像提交主题；`validate.yml` 全绿前不得合并。
- **测试**：改技能脚本 → 跑 `--selftest`；改 validate 逻辑 → 全量 validate + 负对照（坏样例必须失败）。
- **合并纪律**：main 保护（ruleset/review）优先；作者不自行豁免保护；例外需留痕。

## 6. Boundaries / 边界（三级）

| 级别 | 内容 |
|---|---|
| ✅ **Always** | 跑 validate 后再提交；新技能遵循 frontmatter 规范与三节结构；CHANGELOG 同步；许可证声明原样保留 |
| ⚠️ **Ask first** | 修改理论文本段落（ARR 范围）；改动 LICENSE / TRADEMARK / CODE_OF_CONDUCT；删除或重命名技能目录；改 validate.yml 的通过门槛 |
| 🚫 **Never** | 提交任何密钥/token（仓库内零凭据）；把技能正文塞进 README 复制粘贴；添加第三方依赖（stdlib only）；伪造 frontmatter 必填字段；改写他人技能的描述而不留痕 |

## Definition of done / 完成定义

1. validate 全绿（本地 = CI）；2. 新/改技能有 CHANGELOG 行；3. frontmatter 字段齐（含 license/compatibility/metadata）；4. 描述 ≤300 字符且含触发信号词；5. 无密钥、无占位、无依赖新增；6. PR 描述写明验证输出。

## Escalation / 升级路径

- 验证失败 → 修到绿为止，不绕过（不 `|| true`、不跳过）。
- 涉及许可/理论文本/对外表述 → 停手，交 Steven 批准后再动。
- 不确定某技能归属 → 读 `docs/` 规范件或 `CONTRIBUTING.md`，仍不明则开 issue，不要猜。
