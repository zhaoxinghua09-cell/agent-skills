# v1.0.2 提案 · 枚举未识别值从严化

> **状态：已实施（2026-10-29，Steven 批准「全部按照你的建议 做到最好」）→ 已随 v1.0.2 发布，本文件留作提案存档；回执见 PRE_RELEASE_REVIEW_v1.0.1.md §9。**

> 背景：红队高危 #1（evidence/redteam_report_v101_20261029.md 第 2 项）——`--has_di 1` / `on` 等未识别值被静默放行（rc=0、无警告），违反 SKILL.md「从严推定、不静默按可提交输出」与 README「never silently treated as submittable」。
> v1.0.1 规格明令「判定逻辑、rc 语义一概不动」，故未实施；本提案批准后约 5 分钟落地并重跑全量回归。

## 改法（最小改动，不动 rc 框架）

位置：`udi-db-submission-check.py` 的 `check_udi_submission()`，在 6 个枚举参数读取之后、`db/timing/issuer` 分派之前，插入统一归一化：

```python
    # v1.0.2 从严化：未识别枚举值一律按缺失处理并显式警告（不静默、不臆测）
    _ENUM_OK = ("yes", "true", "no", "false")
    unknown = []
    for k in ("is_registered", "has_di", "has_pi", "reusable", "implant", "sterile"):
        v = (args.get(k) or "").strip().lower()
        if v and v not in _ENUM_OK:
            unknown.append(k)
            args[k] = None  # 强制走既有「缺失」分支
    if unknown:
        extra_warn = ("枚举值无法识别，按缺失从严处理，请使用 yes/no："
                      + "、".join("--" + k for k in unknown))
```

随后 `warns = []` 改为 `warns = [extra_warn] if unknown else []`（其余逻辑零改动）。

## 生效行为（对照红队用例）

| 红队用例 | v1.0.1 现状 | v1.0.2 生效后 |
|---|---|---|
| `cn --is_registered yes --has_di 1` | rc=0 无警告（静默放行） | rc=1 + 「--has_di 无法识别，按缺失从严」+ DI 缺失警告 |
| `us --has_di yes --reusable abc` | rc=0 漏报 PI 缺口 | rc=1 + 枚举警告 + PI 高风险缺口警告 |
| 全部合法枚举（yes/no/true/false，含大小写） | 不变 | 不变（零行为差异） |
| rc 语义（0/1/2 映射） | 不变 | 不变（仍是 warnings 非空⇔1） |

## 落地清单（批准后执行）

1. 打上补丁，META version → 1.0.2；SKILL.md frontmatter / manifest.json 同步；CHANGELOG 增行。
2. 重跑全量回归：--demo、三档 rc、红队 8 项（重点第 2 项）、EU 硬日期、文档-实跑逐字比对。
3. manifest 指纹重算；PRE_RELEASE_REVIEW 增补 v1.0.2 回执；外人角度抽测一轮。
4. 与 v1.0.1 一并 push（或 v1.0.1 先行、v1.0.2 随后，按 Steven 指令）。
