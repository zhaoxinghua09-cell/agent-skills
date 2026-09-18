---
title: "skill-admission-gate"
slug: skill-admission-gate
displayName: "skill-admission-gate"
category: "lgd-theory"
compliance_review: "待核验：上架三铁律 ①国家/国际合规 ②AI特别友好 ③理念文化传播+强IP；发布前由 skill-release-gate 审查"
name: skill-admission-gate
description: 技能上架安全闸门——一个技能/插件在安装或上架前，先跑确定性安全审查：查破坏性命令、远程执行、数据外泄、提示注入、隐蔽行为、混淆载荷与作用域越界，产出「分级发现 + 闸门判定 + 包指纹证据」。当需要审查第三方 skill、安装来源不明的技能、给自研技能做发布前安检、做供应链安全评估、或需要出具"该包未被篡改且已评估风险"的证据时调用。核心三件事：①按规则集扫全部文件并分级（BLOCK/WARN）②支持"已接受风险"声明（.admission-allow.json，须署名留痕）③输出包指纹与文件哈希作为"有证"产物。触发词：技能安全、审查 skill、安装前检查、恶意技能、skill 安全扫描、上架闸门、供应链安全、这个技能安全吗、第三方技能、能不能装、木马、后门、提示注入。
version: 1.0.0
license: MIT
agent_created: true
author: XLGD · SynomosAI
---

# skill-admission-gate · 技能上架安全闸门

> **LGD 三律的可执行实现**：有籍（包指纹）· 有证（扫描证据留痕）· 有门禁（判定与已接受风险须署名）。
> 规则版本 `1.0.0` ｜ 纯标准库 ｜ 离线可跑 ｜ 无需 API key

---

## 一、为什么需要它

技能生态的安全问题**不是"有没有恶意包"，而是"没有上架闸门"**：

- 技能可以执行任意代码、访问文件系统、发起网络请求——权限面等同于一个本地程序；
- 但其分发形式常看起来像"一段说明文档"，**审查直觉失效**；
- 一旦装上，它就在你的机器上以你的身份运行。

**结论**：技能需要一个**确定性、可留痕、可复核**的安检环节，而不是靠"看起来没问题"。

---

## 二、什么时候用

| 场景 | 说明 |
|---|---|
| 安装第三方技能前 | 尤其是来源不明、无仓库背书、无 license 的包 |
| 自研技能发布前 | 与 skill-release-gate 配套，作为安全前置 |
| 供应链安全评估 | 批量扫描技能根目录，出一张风险清单 |
| 需要出具证据 | 包指纹 + 文件哈希 + 时间戳，证明"此版本未变" |

---

## 三、怎么用

### 单技能审查

```bash
python scripts/scan_skill.py <技能目录> [--json out.json]
```

### 批量审查（扫一个技能根目录）

```bash
python scripts/scan_skill.py <技能根目录> --batch --json batch-result.json
```

输出示例：

```
技能: my-skill
判定: WARN ｜ BLOCK 0 ｜ WARN 2 ｜ 已接受 0 ｜ 扫描 6 文件
包指纹: cd23896eee940857
  [WARN] EXF-04 script.py:41  requests.post("https://api.example.com/collect", ...)
```

**退出码**：`0` = 非 BLOCK；`1` = BLOCK（可用于 CI 阻断）。

---

## 四、规则集（v1.0.0）

| 组 | 规则 | 级别 | 检测内容 |
|---|---|---|---|
| **破坏性** | DES-01~05 | **BLOCK** | 递归强制删除、`del /s /f`、`shutil.rmtree`、格式化/写设备、fork 炸弹 |
| **远程执行** | EXE-01,02 | **BLOCK** | `curl|sh`、PowerShell 编码命令、`iex(` |
| | EXE-03,04 | WARN | `eval(`/`exec(`、base64 解码后执行 |
| **数据外泄** | EXF-01,02 | **BLOCK** | 读私钥/凭据文件、读本地保险库与密钥投递工具 |
| | EXF-03,04 | WARN | 读 `.env`/环境凭据、向外部端点 POST/PUT |
| **提示注入** | INJ-01,02 | **BLOCK** | "忽略之前指令"、"不要告诉用户" |
| | INJ-03~05 | WARN | 静默执行、绕过安全/审批、诱导粘贴密钥 |
| **混淆** | OBF-01 | WARN | 超长 Base64 字串（疑似载荷） |
| **作用域** | SCP-01 | WARN | 写入技能目录之外的绝对路径 |

**判定口径**：命中任一 BLOCK → 整体 `BLOCK`；仅命中 WARN → `WARN`；无命中 → `PASS`。

---

## 五、已接受风险机制（关键设计）

**误报是必然的**——例如本地保险库技能"读 `~/.ucvault_local`"是其**本职**，不是外泄。

**但"接受风险"不能靠静默忽略，必须留痕、必须署名。** 在被审目录放 `.admission-allow.json`：

```json
{
  "schema": "skill-admission-allow/1.0",
  "skill": "dpapi-local-vault",
  "note": "本技能功能即本地凭据保险库，访问该目录是其声明用途。",
  "allow": [
    {
      "rule": "EXF-02",
      "reason": "读写 ~/.ucvault_local 是其唯一且声明的用途；密钥不落明文、不出本机。",
      "approved_by": "Steven Zhao (XLGD)",
      "date": "2026-09-12",
      "mitigation": "本技能不发起任何网络请求。"
    }
  ]
}
```

声明后该规则**转入 ACCEPTED 分类**（仍出现在报告里，但不影响判定）——**这就是"有门禁 + 有证"**。

---

## 六、产出的证据（"有证"）

每次审查都输出：

| 字段 | 含义 |
|---|---|
| `package_fingerprint_sha256` | 全包文件哈希聚合指纹——用于判定"包是否被改过" |
| `file_hashes[]` | 每个文件的 sha256 与字节数 |
| `rule_version` | 规则集版本（规则会演进，须记录用哪版判的） |
| `timestamp_utc` | 审查时间 |
| `accepted_risks[]` | 已接受风险及其署名与理由 |

**用途**：上架台账、争议取证、版本回归比对（新版本指纹变了 → 须重审）。

---

## 七、边界与诚实声明

- **模式匹配有极限**：本工具查的是**已知模式**，能拦住粗糙与常见手法，**不能替代人工代码审计**；对高度混淆、逻辑后门、依赖链投毒（第三方库）覆盖不足。
- **不做沙箱执行**：只做**静态审查**，不运行动态行为分析。
- **规则会演进**：判定依赖 `rule_version`；跨版本比较结论时须对齐规则版本。
- **不构成安全保证**：`PASS` 表示"未命中本规则集"，**不等于"安全"**。

---

## 八、与 LGD 的对应

| LGD 法则 | 本技能的实现 |
|---|---|
| **有籍（Registry）** | 包指纹 + 文件哈希：这个包"是谁、是什么版本"可唯一标识 |
| **有证（Evidence）** | 扫描发现 + 规则版本 + 时间戳，全部落盘 JSON |
| **有门禁（Gates）** | BLOCK 则阻断（退出码 1）；接受风险须署名 + 给理由 + 给缓解措施 |

---

*skill-admission-gate v1.0.0 · © XLGD · SynomosAI · 2026-09-12*
