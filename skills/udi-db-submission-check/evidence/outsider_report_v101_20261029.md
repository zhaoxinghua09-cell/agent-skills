# 第三方发布前评测报告 · udi-db-submission-check v1.0.1（原文存档）

> 独立席：outsider-checker（零上下文冷启动，未参与开发）｜评测日期：2026-10-29｜存档说明：会话原文逐字存档

【udi-db-submission-check 第三方发布前评测报告】（评测人：outsider-checker，未参与开发，仅凭包内文档冷启动 + 全量实测 + 独立网络核验）

① 总评：PASS（有保留——核心功能与全部事实性声称均验证通过；存在 2 处文档自相矛盾，属应修但不阻断发布）

② 各节结论与证据：

1. 冷启动可用性 — PASS
只读 README.md / SKILL.md，5 分钟内即可明确：零依赖 Python CLI、UDI 数据库提交合规判定、--demo 先行。
实际第一条命令：`python udi-db-submission-check.py --demo` → 一次成功，EXIT=0。

2. 全量实跑 — PASS（全部声称逐条复现）
- --demo：EXIT=0，内置 3 案例（cn rc=1 PI 缺失 / us rc=0 / eu rc=1 DI 缺失）。
- `--market cn --is_registered yes --has_di yes --has_pi yes --sterile no --implant no` → rc=0 ✓（README 声称吻合）
- `--market us --has_di yes --reusable yes` → rc=1，warning「可重复使用或植入类器械须具备 PI…属高风险缺口」✓
- `--market jp` → rc=2，error_code=E_ENUM_INVALID「--market 必填，且必须为 cn / us / eu 之一」✓
- 四A 复现 `--json --market cn --has_di yes --sterile yes`（Python 3.13.14）→ 与 SKILL.md 样例逐字一致：warnings 的 is_registered 从严提示、rules_verified_on="2026-10-29"、version="1.0.1"、aigc_mark(GB 45438-2025) 全部吻合 ✓
- --sterile yes → core_fields 末尾新增「无菌指示项（须与标签申报一致）」；sterile no 时无此项 ✓
- 进程退出码镜像 rc（1/2 均实测）✓
- 确定性：同输入两次运行 md5 完全相同 ✓
- 零依赖：仅 import argparse/json/sys，无 urllib/requests/socket ✓
- rules_verified_on 与脚本常量 RULES_VERIFIED_ON（脚本第 11 行，单一来源）同源 ✓
- version 1.0.1：输出 / SKILL.md frontmatter / manifest.json / CHANGELOG v1.0.1 四处一致 ✓；文本核验日期 2026-10-29 ✓

3. EU 事实抽查 — PASS（与欧盟委员会官方口径一致）
- 2026-05-28 四模块强制：EC 官网（health.ec.europa.eu 新闻稿）+ 奥地利 BASG + 爱尔兰 HPRA 均确认。
- 2026-11-28 存量/法规器械 UDI/Dev 登记截止：EC 官方过渡期 PDF 原文「28 November 2026 Deadline to register the device in the UDI/Dev module」+ HPRA 表格「Deadline: 28 November 2026」确认。包内写的是 11-28，未写成 11-27 ✓；OJEU 2025-11-27 是决策发布日，包内表述准确。

4. 链接直达性 — PASS（14/14 可达）
200：shields.io 徽章、medxpert.cn 首页//knowledge//skills/ 及 5 个徽章 svg、lgd-skills-index.github.io、udi.nmpa.gov.cn、ec.europa.eu/tools/eudamed；202：accessgudid.nlm.nih.gov；github.com/zhaoxinghua09-cell/lgd-theory 经 WebFetch 确认 200 且仓库存在（curl 000 为本地网络抖动）。
备注：SKILL.md verified_links 写「11/11 可达（2026-09-12 快照）」，现外链共 14 条，数字已过时（非错误）。

5. 陌生人视角风险审查 — PASS（有 1 处内部矛盾）
- 免责声明清楚：SKILL.md 开头加粗「决策支持，不构成注册/合规/法律意见，须人工复核，以官方为准」；aigc_mark.disclaimer 同口径；「能力边界」一节明确不覆盖特殊情形。误当成法律意见的风险低。
- 分层许可（代码 MIT / 文档理论保留所有权利）表述自洽；「AI 辅助生成、署名机构承担出品责任」清楚；SynomosAI 未注册实体/无商标如实披露；无夸大声明（甚至主动写「无 DOI」「未做独立安全扫描（TBD）」）。
- 发现矛盾：README 的 LGD 统一块写「生产参考部署：无（未声明）」，SKILL.md 同一块写「生产参考部署：MedXpert」——两处口径不一致。

6. 可视化与人读体验 — PASS
assets/overview.svg 存在、1146 字节、有效 SVG（xmlns 正确、800×240 viewBox），标题「UDI 数据库提交合规判定器」+ 副标「零依赖 · 确定性 JSON IR · 离线可用 · 决策支持」，与本技能直接相关。文档表格结构对人类评审者清晰。

③ 问题清单（按严重度）
【阻断发布】无。
【建议改进】
1.（中高）demo/README.md 与事实相反：声称「本技能为文档型…本包无可执行代码；不提供 python 入口（红线）」，但包内实际有可执行 .py 且 SKILL/README 提供运行命令——明显是文档型技能模板未适配，会误导冷启动读者。
2.（中）--demo 与 --json 输出 schema 不一致：--demo 输出缺 `version` 与 `aigc_mark` 字段，而 SKILL.md「判定核心」声称输出含 aigc_mark。建议 --demo 也带全字段或文档注明差异。
3.（中低）README 与 SKILL.md 的 LGD 统一块「生产参考部署」字段互相矛盾（无 vs MedXpert）。
4.（低）verified_links「11/11 可达」为 9 月快照，现外链 14 条，建议随版本更新。

④ 评分：4 / 5 星
理由：核心功能、三档 rc、sterile 行为、EU 硬日期、外链、版本与核验日期全部实测吻合且事实准确，诚实披露充分；扣一星在于 demo/README 模板矛盾与 --demo 输出缺 aigc_mark 两处发布前应修的文档卫生问题。
