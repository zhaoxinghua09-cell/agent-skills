# 发布前审查报告 · udi-db-submission-check v1.0.1

审查日期：2026-10-29 ｜ 出规格：Muse ｜ 执行：WorkBuddy ｜ 独立席：redteam-checker（红队）+ outsider-checker（外人视角）
状态：**文档/指纹项已修复归零；判定逻辑项 1 项留待终核（规格冻结，见 §5）**

## 1. 规格符合性（v1.0.0 → v1.0.1）

| 规格项 | 状态 | 证据 |
|---|---|---|
| EU `submit_timing` 逐字替换（2026-05-28 强制使用 + 2026-11-28 存量登记截止） | DONE | 实跑 EU 案例输出逐字含两日期 |
| EU `obligations` 增补存量登记截止条目 | DONE | 仅 EU 分支出现第 4 条，cn/us 无 |
| 新增 `rules_verified_on`（与 rc 同级，全案例一致） | DONE | demo 3 案例 + 主流程成功/错误路径均存在且同值 |
| 版本 1.0.1（SKILL.md frontmatter / 脚本 META / manifest.json） | DONE | 全仓 grep 无 1.0.0 残留 |
| CHANGELOG 增行 | DONE | CHANGELOG.md v1.0.1 条目（含审查修正段） |
| 判定逻辑、rc 语义不动 | DONE | demo_exit=0 / cn_full=0 / us=1 / jp=2 与改前一致 |

## 2. EU 硬日期独立复核（2026-10-29 当日）

- 欧委会 EUDAMED 总览页原文：「As of 28 May 2026, the following 4 modules of EUDAMED became mandatory to use」（依据 Commission Decision (EU) 2025/2371，OJEU 2025-11-27 刊载，6 个月过渡）。链接直达（HTTP 200）。
- 欧委会过渡期时间表 PDF（Legacy and Regulation devices）+ HPRA 官方公告双源确认：「28 November 2026 — Deadline to register the device in the UDI/Dev module」（12 个月过渡，仅限强制使用日前已上市器械）。
- 措辞红线验证：包内无 11-27 截止表述（grep 归零）；MDR 原生器械常规时点未扩大表述；无杜撰罚则。

## 3. 双席独立测试结果

### 红队（redteam-checker）：FAIL → 修复后归零
| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| 1 | 枚举未识别值（如 `--has_di 1` / `on`）静默放行：既不按 yes 也不触发警告，可能 rc=0 输出「可提交」，违反 SKILL.md「从严/不静默」声称 | 高 | **未改**（判定逻辑，规格冻结）→ 列入 §5 待终核 |
| 2 | SKILL.md 错误码表列了 `E_INPUT_MISSING`，代码从未使用 | 中 | 已修：表对齐实际实现 |
| 3 | `--market ""` 打印帮助 exit 0，无 JSON 输出 | 低 | 接受（空参=看用法，合理路径） |
| 4 | manifest.json 指纹过期（LICENSE.md 在本次改动前已 stale，README/SKILL/py 改动后未更新） | 中 | 已修：全量重算，算法=按 manifest 顺序拼接各文件 sha256 hex（无分隔符）再整体 sha256；复检 7/7 全匹配 |
| 5 | demo/README.md 模板残留：「文档型、无可执行代码、不提供 python 入口」与本 CLI 包直接矛盾 | 中 | 已修：重写为真实走查指引 |
| 6 | README 与 SKILL.md LGD 统一块「生产参考部署」字段矛盾（无 vs MedXpert） | 低 | 已修：README 对齐 SKILL.md（MedXpert，self-reported） |
| 7 | `--demo` 输出缺 `version`/`aigc_mark`，与 SKILL.md 输出表不符 | 低 | 已修：demo 成功/错误路径补齐（仅输出格式，不触判定逻辑） |

### 外人视角（outsider-checker）：PASS · 4/5 星
- 冷启动可用：仅凭 README+SKILL.md 即可正确跑通；声称的实测行为逐条复现成功。
- 事实抽查：两个 EU 硬日期独立核验与欧盟官方口径一致（11-28 正确）。
- 意见：文档 LGD 治理内容对外人偏重；免责声明与许可分层自洽，无夸大声明。

## 4. 外链直达性（2026-10-29 快照）

13/13 可达（curl 实测）：5 徽章 svg、lgd-skills-index、medxpert.cn 四页、NMPA UDI 门户、AccessGUDID（202）、EUDAMED 工具页均 200/202。`github.com/zhaoxinghua09-cell/lgd-theory` 网页端本机 000（网络限制），经 GitHub API 复核 `private: false`、仓库存在——链接有效。SKILL.md frontmatter `verified_links` 已更新为 2026-10-29 · 13/13。
注：规格附件中的 eur-lex / EC 时间表 PDF / 总览页 3 条源链接本机实测可达（202/200），仅作依据引用未写入包内文档。

## 5. 待终核（判定逻辑项，规格冻结）

**枚举从严化（红队高危 #1）**：建议 v1.0.2 将未识别枚举值按「缺失」处理（触发 warnings、rc=1），与「从严推定、不静默按可提交输出」的声称对齐。改动点约 10 行，不动 rc 语义框架。**需 Muse/Steven 批准后实施**（超出 v1.0.1 规格范围）。

## 6. 可视化与人读

- assets/overview.svg 有效、与本技能相关；SKILL.md 5 徽章全部可达渲染。
- 文档结构（痛点→是什么→判定核心→用法→真机输出→边界→家族）表格化，外人评测确认可读性 PASS。

## 7. 发布门禁结论

- 代码/文档/指纹/外链/实测：**全部归零**。
- **尚未 git commit / push**（按 E2 对外动作门禁 + 终核=用户）：待 Steven 确认 §5 决策与发布指令后执行；推送后须登记 github-uploads.md 台账。

## 8. R10 第二轮补强回执（2026-10-29 22:53，「做到最好了吗」自查后补齐）

| 缺口 | 处置 |
|---|---|
| 两席审查报告原文只在会话里，未落盘存证 | 已归档：`evidence/redteam_report_v101_20261029.md`、`evidence/outsider_report_v101_20261029.md`（逐字原文） |
| evidence.json 失实（自称"纯文档、无脚本、未验证"） | 已改写真值：CLI 入口、verified=true、三轮独立实跑证据链引用 |
| llms.txt 输出字段缺 rules_verified_on | 已补（含版本 1.0.1、核验日期、rc 语义一行） |
| overview.svg 孤儿资产且信息量低（未升级、无人引用） | 已重绘（三市场卡片 + EU 硬日期 + rc 图例 + 版本/核验日期），README 顶部挂引用，XML 有效性验证通过 |
| v1.0.2 修复只停留在"建议" | 已写成可直接落地的补丁提案：`evidence/v102_enum_strictness_proposal.md`（含改法、红队用例对照表、4 步落地清单），批准后约 5 分钟完成 |
| GitHub 侧外人实测 | **NOT VERIFIED（边界如实声明）**：push 前仓库远端仍是旧版，外人角度的 GitHub 侧实测（clone→冷启动→跑通）必须在 push 后重做一轮，已列为发布后门禁动作 |

补强后回归（R9 整轮重跑）：demo=0 / cn=0 / us=1 / jp=2 / EU 硬日期与 rules_verified_on 全对；manifest 7/7 指纹 + 包指纹复验全匹配。

## 9. v1.0.2 回执（2026-10-29，Steven 批准「全部按照你的建议 做到最好」后实施）

- **枚举从严化已落地**：未识别枚举值 → 归一为缺失 + 显式警告（rc=1）；unknown reusable/implant 追加「PI 高风险缺口确认」警告（回归中发现提案承诺与实现的偏差并补强——R9 收敛实例）。
- **回归 PROOF**：rc 三档（0/1/2）+ demo=0；红队复测 caseA（--has_di 1 → rc=1 双警告）/ caseB（--reusable abc → rc=1 枚举+PI 警告）/ caseC（大小写合法枚举 → rc=0 零行为变化）/ caseD（合法 PI 缺失路径不受影响）；EU 硬日期 + obligations 4 条 + rules_verified_on=2026-10-29；CN-4A 与 SKILL.md 样例一致；manifest 7/7 + 包指纹复验；全包无 1.0.0/1.0.1 残留（CHANGELOG 历史条目除外）。
- 红队清单收敛状态：#1 已修 ｜ #2 指纹已修 ｜ #3 错误码表已修 ｜ #4 --market ""（低，接受）｜ #5/#6 提示项知悉。**清单归零。**
