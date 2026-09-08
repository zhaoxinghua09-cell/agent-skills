---
name: hash-check
description: 文件哈希校验 — 生成/校验目录 SHA-256 清单：下载验 integrity、传输前后比对、防篡改留证（零依赖）
slug: hash-check
version: 1.0.0
display_name: 文件哈希校验
display_name_en: File Hash Check
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 文件哈希校验 / File Hash Check

**hash-check** v1.0.0 · LGD-Powered 效率工具家族 · 零依赖

## 痛点
下载的文件不知道完不完整，传给同事再传回来不确定有没有被改

## 用法
```bash
python scripts/hash_check.py --help
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
