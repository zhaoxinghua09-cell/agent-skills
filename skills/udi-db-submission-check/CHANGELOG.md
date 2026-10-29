# Changelog

## v1.0.2 (2026-10-29)
- 枚举从严化：未识别的枚举值（如 `--has_di 1`/`on`）一律按缺失处理并在 `warnings` 显式警告（rc=1），不再静默放行；合法枚举（yes/no/true/false，含大小写）行为零变化，rc 语义框架不变。（依据：发布前红队高危 #1，提案 evidence/v102_enum_strictness_proposal.md，Steven 2026-10-29 批准）

## v1.0.1 (2026-10-29)
- EU 时点补硬日期：`submit_timing` 明示 EUDAMED 首批四模块 2026-05-28 起强制使用、存量/法规器械 2026-11-28 前 UDI/Dev 登记截止；`obligations` 增补对应条目（依据：欧盟委员会决定 (EU) 2025/2371 + 欧委会 EUDAMED 过渡期时间表，2026-10-29 复核）。
- 输出自带核验日期：新增 `rules_verified_on` 字段（与 `rc` 同级，全案例一致），值取脚本单一常量 `RULES_VERIFIED_ON`，与 SKILL.md「文本核验日期」同源同值（2026-10-29）。
- 发布前审查修正（红队+外人双席实测）：`--demo` 输出补齐 `version`/`aigc_mark`；SKILL.md 错误码表对齐实际实现（移除未使用的 E_INPUT_MISSING）；demo/README 纠偏（实为 CLI 包，非文档型）；README LGD 统一块「生产参考部署」与 SKILL.md 对齐；manifest.json 全量指纹重算；外链快照更新至 2026-10-29（13/13 可达）。
- 判定逻辑与 rc 语义未动。
