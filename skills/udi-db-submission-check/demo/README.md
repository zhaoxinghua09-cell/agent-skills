# demo · udi-db-submission-check（UDI 数据库提交合规判定器）

> 本目录为 LGD「有证 3/3」工件位。本技能为**零依赖单文件 CLI 判定器**，入口脚本位于包根：`udi-db-submission-check.py`（Python 3.8+，仅标准库）。

## 何时用
见 `SKILL.md`「何时用」段：需要判定 UDI 数据库提交义务（哪个库、何时传、必填哪些字段）时使用。

## 手工走查步骤
1. 在包根目录运行冒烟案例：`python udi-db-submission-check.py --demo`（含 cn/us/eu 三案例，rc=0/1/2 各一）。
2. 正式判定：`python udi-db-submission-check.py --json --market cn --has_di yes --sterile yes`（参数见 SKILL.md「四、用法」）。
3. 核对输出：JSON IR 含 `result` + `rc` + `error_code` + `rules_verified_on` + `aigc_mark`；退出码与 `rc` 一致。

## 不做什么（红线）
- 判定结论须对照规范原文人工复核，本技能不作技术背书。
- 输出为决策支持，不构成法律/注册意见。
