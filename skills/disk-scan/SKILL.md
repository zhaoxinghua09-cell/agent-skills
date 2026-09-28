---
name: disk-scan
description: 磁盘占用扫描 — 只读扫描目录占用：Top N 大文件 + 各子目录大小排行，快速定位空间杀手（零依赖）
slug: disk-scan
version: 1.0.0
display_name: 磁盘占用扫描
display_name_en: Disk Usage Scan
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "磁盘占用扫描 — 只读扫描目录占用：Top N 大文件 + 各子目录大小排行，快速定位空间杀手（零依赖）"
description_en: "Read-only disk usage scan: Top-N largest files plus per-subdirectory size ranking to locate space hogs quickly (zero-dependency)."
classification:
  internal: ["通用工具(跨主轴·待归类)"]
  skillhub: ["productivity"]
  clawhub: ["productivity", "data-analytics", "development"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（Steven 2026-09-28 令：我们的 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走 Steven 批准。"
---
# 磁盘占用扫描 / Disk Usage Scan

**disk-scan** v1.0.0 · LGD-Powered 效率工具家族 · 零依赖

## 痛点
盘满了不知道谁吃的空间，资源管理器算半天还看不清

## 用法
```bash
python scripts/disk_scan.py --help
```
- 成功 → rc=0；发现问题 → rc=1；用法错误 → rc=2
- 支持 `--json` 机器可读输出
- 涉及写盘的操作默认 **dry-run 预览**，加 `--apply` 才执行（text-replace/dup-finder 还会先备份）

## 安全设计
- 只移动/重命名，不删除内容文件（dup-finder 的 --apply 仅删除与首个完全同哈希的副本）
- 写盘前自动备份（text-replace 生成 .bak；batch-renamer/organizer 可用 --json 记录计划回滚）

## LGD-Powered
本技能是「LGD 三律」效率家族件：把高频文件操作做成**可预览、可回滚、有留痕**的确定性工具。

## 免责
本工具为效率辅助；对重要数据请先备份并在预览确认后再 --apply。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `disk_scan.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `disk_scan.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
