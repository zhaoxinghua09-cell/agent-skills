---
name: dir-organizer
description: 文件夹整理器 — 按扩展名把杂乱目录归类到 图片/文档/表格/音视频/压缩包/代码/其他 子目录，默认预览 --apply 才移动（零依赖）
slug: dir-organizer
version: 1.0.0
display_name: 文件夹整理器
display_name_en: Directory Organizer
agent_created: true
author: zhaoxinghua09-cell
license: MIT
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
---

# 文件夹整理器 / Directory Organizer

**dir-organizer** v1.0.0 · LGD-Powered 效率工具家族 · 零依赖

## 痛点
下载夹几百个文件混在一起，找东西全靠搜，归类又懒得手动拖

## 用法
```bash
python scripts/dir_organizer.py --help
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
