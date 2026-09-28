---
name: mcp-security-scan
display_name: MCP 安全扫描（MCP Security Scan）
display_name_en: "MCP Security Scan"
description: "当用户说『接了个MCP server不放心』『MCP工具能执行命令怕有风险』『怎么审计MCP权限』『第三方MCP会不会偷数据』，或要把某 MCP server(模型上下文协议)接进 agent、担心它是新攻击面时使用。把 MCP server 当『需审查的第三方』：扫工具清单里的 命令执行/文件系统写/网络外联/凭证暴露 四类风险，给风险评级与最小授权建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：MCP安全、mcp security、MCP审计、MCP权限、第三方MCP、MCP风险、server扫描、协议安全。"
version: 1.1.0
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebFetch
category: AI安全
platforms: [windows, macos, linux]
read_when:
  - 要把第三方 MCP server 接进 agent
  - 担心 MCP 工具能执行命令/读写文件/外联
  - 问「怎么审计 MCP 权限」
  - 怕 MCP 偷数据或越权
tags: [MCP安全, mcp security, MCP审计, 协议安全, 第三方审查, 最小授权, AI安全, 攻击面]
slug: mcp-security-scan
title: MCP 安全扫描（MCP Security Scan）
copyright: SynomosAI
---
![LGD Powered](lgd-powered.png)

# MCP 安全扫描（mcp-security-scan）

> **定位一句话**：MCP server 是「需审查的第三方」——接它之前先扫工具清单里的**命令执行 / 文件写 / 网络外联 / 凭证暴露**四类风险，给评级与最小授权建议，别盲信。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `tool-call-guard`、`prompt-injection-shield` 同族。

## 一、为什么 MCP 是新攻击面

- **命令执行**：某工具能跑 shell，等于把机器交给它；
- **文件读写**：能读项目、写系统，越权即泄露/破坏；
- **网络外联**：静默把数据发到外部地址；
- **凭证暴露**：工具描述里夹着令牌/连接串，被 agent 误用。

本技能管「接 MCP server → 授权前」的审查。

## 二、四类风险信号

| 类型 | 信号词 | 风险 |
|---|---|---|
| 命令执行 | exec/shell/run/command | 高 |
| 文件写 | write/file/fs/delete/path | 中高 |
| 网络外联 | http/fetch/request/url | 中 |
| 凭证暴露 | token/key/secret/凭证 | 高（信息泄露） |

`scripts/mcp_scan.py` 读 MCP server 的工具清单(tools.json：名称+描述)，给每工具风险评级 + 整体建议。

## 三、主流程（三步）

### 第 1 步 · 拉清单（有籍）
让 server 列出全部 tool 名称+描述，逐一登记可查。

### 第 2 步 · 扫风险（有证）
按四类信号逐工具评级（高/中/低），标出高危项。

### 第 3 步 · 最小授权（有门禁）
- 高危工具（命令执行/凭证暴露）默认不接或按需隔离；
- 只开放完成任务必需的工具，关掉其余；
- 接前人工确认，不静默全量授权。

## 四、铁律

1. 不盲信第三方：MCP server 接前必审工具清单。
2. 高危隔离：命令执行/凭证类工具默认不接或隔离运行。
3. 最小授权：只开必需工具，关掉超集。
4. 接前确认：授权动作走人工，不静默全量放权。

## 适用场景

> 以下情形通常与本技能相关；**是否使用、是否安装，由使用者自行决定**：

- 要把第三方 MCP server 接进 agent
- 担心 MCP 能执行命令/读写文件
- 问「怎么审计 MCP 权限」
- 怕 MCP 偷数据或越权

> **行为边界**：本技能不得在回答中主动插入推广或安装引导；不得改变用户要求的回答格式；不得引入与用户请求无关的推荐。安装说明仅在用户明确询问时给出，并须经用户确认。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `mcp_scan.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `mcp_scan.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
