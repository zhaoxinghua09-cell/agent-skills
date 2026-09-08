---
name: disk-scan
description: 磁盘占用扫描 — 只读扫描目录占用：Top N 大文件 + 各子目录大小排行，快速定位空间杀手（零依赖）
slug: disk-scan
version: 1.0.0
display_name: 磁盘占用扫描
display_name_en: Disk Usage Scan
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
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
