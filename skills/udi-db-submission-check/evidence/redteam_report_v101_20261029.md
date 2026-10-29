# 红队测试报告 · udi-db-submission-check v1.0.1（原文存档）

> 独立席：redteam-checker（worker≠checker）｜测试日期：2026-10-29｜全部实跑，Python 3.13.14，Windows/Git Bash｜存档说明：会话原文逐字存档，处置结论见 PRE_RELEASE_REVIEW_v1.0.1.md

═══ 总体结论：FAIL ═══（8 项中 1 项 FAIL，另附加发现 1 项高危）

【逐项结果】

1. 参数边界 — PASS
   - --market EU / Cn → 正确 lower 化，EU 输出 eu 分支、Cn 输出 cn 分支，rc 语义正常。
   - --market xx --has_di yes → rc=2，error_code="E_ENUM_INVALID"，errors=["--market 必填，且必须为 cn / us / eu 之一"]，JSON 含 rules_verified_on="2026-10-29" ✓
   - --market 缺失但有其他参数 → rc=2 / E_ENUM_INVALID ✓
   - 注意点：--market ""（空字符串）不报错，走"全参数为空→打印帮助 exit 0"分支，rc=0 而非 rc=2。

2. 枚举注入 — FAIL
   - 不崩溃 ✓；"YES" 被认可为 yes、未误判 ✓；is_registered 怪值（"1"/"on"/"abc"）从严触发"输入不完整"警告 ✓。
   - 但 has_di / reusable / implant / sterile 的未识别值被【静默放行】：
     * 隔离测试（cn + --is_registered yes）：has_di ∈ {"True","1","on","abc"} 全部 → rc=0、warnings=0，formatters_present 直接回显 "1"/"on"/"abc"。
     * 更严重：--market us --has_di abc --reusable no --implant no → rc=0；--market us --has_di yes --reusable abc（has_pi 缺失）→ rc=0、无 PI 高风险警告——怪值 reusable 被当作"非可重复使用"，漏报 PI 缺口。
   - 对照声称：SKILL.md 五节「输入不足时从严提示…不静默按可提交输出」、README「never silently treated as submittable」——实测违反。未识别值效果等同 yes，不是"视为缺失/触发警告"。
   - 另：rc=2 仅对 market 非法成立，其余枚举无校验（"枚举非法⇔rc=2"仅部分成立）。

3. rc 语义一致性 — PASS（8/8）
   - 批量验证：warnings 非空⇔exit=1⇔json_rc=1；无警告⇔0；market 非法⇔2。全部 match=True。
   - 证据：full CN args → exit=0/rc=0/w=0；us+reusable yes → 1/1/1；cn is_registered no → 1/1/1；jp → 2/2；XX → 2/2。

4. EU 分支正确性 — PASS
   - submit_timing 同时含 2026-05-28 与 2026-11-28，措辞「在强制使用日前已投放市场的存量/法规器械，须在 2026-11-28 前完成 UDI/Dev 模块登记」与规格一致。
   - obligations 第 4 条「存量/法规器械的 UDI/Dev 登记截止为 2026-11-28…」仅 EU 出现；cn/us 均 3 条。
   - rules_verified_on 在 demo 三案例、--json 成功路径、--json 错误路径（--market jp）全部存在且同为 "2026-10-29"。

5. 文档-实跑一致性 — PASS
   - SKILL.md 四A 样例与实跑 `--json --market cn --has_di yes --sterile yes` 逐字段一致（input/tool/version/core_fields 10 项含无菌指示项/formatters_present/warnings 逐字/rc=1/error_code=null/rules_verified_on/aigc_mark 全对；obligations/notes 折叠处条数一致）。
   - 三档 rc 复现：SKILL.md L141 三条命令实测 0 / 1 / 2，与声称一致。
   - --sterile yes 加字段 / --sterile no 不加（计数 0）✓。README「Text verified: 2026-10-29」与输出同值 ✓。
   - 小差异：SKILL.md 三节错误码表列有 E_INPUT_MISSING（参数不足），代码中不存在该码（仅 E_ENUM_INVALID/E_RUNTIME），market 缺失实际报 E_ENUM_INVALID。

6. 措辞红线 — PASS（附提示）
   - 三市场 + --demo 全部输出 grep "11-27" = 0 命中；全包无「罚款/罚则/处罚/吊销」。
   - 截止范围表述限定正确（「强制使用日前已投放市场的存量/法规器械」）。
   - 提示：README.md:20 含 "OJEU 2025-11-27"——是欧盟公报刊发决定的日期，语义正确、非截止日，但字符串可被机械扫描误命中，建议发布方知悉。

7. 版本一致性 — PASS
   - SKILL.md frontmatter(L8)、SKILL.md 证据声明(L73)、脚本 META(L7)、manifest.json(L4)、CHANGELOG.md(L3) 五处均 1.0.1；全包 grep "1.0.0" = 0 残留。

8. 健壮性 — PASS
   - 10KB 超长参数：不崩溃，JSON 合法（但印证第 2 项问题：垃圾值 rc=0 静默通过）。
   - 引号/unicode/控制字符参数（'he said "yes"'、'日本語✓<>&'）：JSON 合法、原值回显。
   - --demo --json 同给：demo 优先、--json 被忽略，exit 0，无冲突。
   - 只给 --json：打印 argparse 帮助，exit 0（符合预期）。

【附加发现（清单外，发布前须处理）】
- 【高】manifest.json 的 sha256 指纹与实际文件全部不匹配：实测 README=46d0818f…、SKILL.md=9ea0ee61…、py=c357cf20…，manifest 声称 77b040d5…/158a71ff…/5cc4efee…。v1.0.1 改动文件后指纹未重算，包内完整性证明已失效。
- 【低】--market "" 与全空参数共用 help+exit 0 分支，未按"参数缺失"从严报 E_ENUM_INVALID/rc=2（语义上 market 空字符串≠未调用）。

【问题清单（按严重度）】
1. [高·功能性+合规声称不符] 枚举未识别值静默放行（has_di/reusable/implant/sterile），可致 rc=0 误判"可提交"、漏报 PI 高风险缺口，直接违反 SKILL.md/README 的从严/不静默声称。
2. [高·完整性] manifest.json 三文件指纹过期，与实际文件不符。
3. [低] SKILL.md 错误码表 E_INPUT_MISSING 与实现不符（代码无此码）。
4. [低] --market "" 未按缺失处理，走 help/rc=0。
5. [提示] README "OJEU 2025-11-27" 字符串易被机械扫描误判（语义正确）。
6. [提示] --demo 输出 JSON 无 version 字段（非 demo 成功路径有），不影响 rules_verified_on 一致性。

测试方式说明：全部为 python 直跑实机输出，未静态推断；退出码经 bash echo $? 逐条抓取；未修改任何被测文件（临时文件已清理）。
