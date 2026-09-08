---
name: batch-renamer
description: 批量重命名器 — 规则式批量重命名：前缀/后缀/序号/查找替换/扩展名过滤，默认预览 --apply 才执行（零依赖）
slug: batch-renamer
version: 1.0.0
display_name: 批量重命名器
display_name_en: Batch File Renamer
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 批量重命名器 / Batch File Renamer

**batch-renamer** v1.0.0 · LGD-Powered 效率工具家族 · 零依赖

## 痛点
几十个文件要加前缀改序号，手动改到怀疑人生，还怕改错

## 用法
```bash
python scripts/batch_renamer.py --help
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
