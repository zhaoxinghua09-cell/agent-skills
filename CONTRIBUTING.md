# 贡献指南（Contributing Guide）

感谢你想为 **agent-skills** 做贡献。

本项目是 **LGD 三律（有籍 · 有证 · 有门禁）** 指导下的 AI Agent 治理技能标准库。
我们欢迎任何形式的贡献：新增技能、改进现有技能、修 bug、写文档、翻译、报问题。

> **一句原则**：**方法与工具全开源，权威与裁决权保留。** 你贡献的是"怎么做"，我们共同维护的是"标准是什么"。

---

## 一、先看这里（30 秒）

| 你想做什么 | 去哪里 |
|---|---|
| 报告一个问题 | [开 Issue](https://github.com/zhaoxinghua09-cell/agent-skills/issues/new/choose) |
| 提一个新技能 | 先开 Issue 讨论，再提 PR |
| 修 bug / 改文档 | 直接提 PR |
| 讨论规范本身 | 开 Issue，打 `discussion` 标签 |
| 安全问题 | **不要开公开 Issue**，见 [SECURITY.md](SECURITY.md) |

---

## 二、开发环境

```bash
# 1. 克隆
git clone https://github.com/zhaoxinghua09-cell/agent-skills.git
cd agent-skills

# 2. 无需安装依赖 —— 本项目所有技能零依赖（仅 Python 标准库）
python --version   # 建议 3.10+

# 3. 跑一个技能试试
python skills/token-disclosure-check/scripts/check.py --help
```

**技术约束（重要）**：
- ✅ **仅用 Python 标准库**，不引入第三方依赖
- ✅ 每个技能必须**独立可运行**（不依赖其他技能）
- ✅ 必须提供**可运行脚本**（不是只有文档）
- ✅ SKILL.md 须含 **frontmatter 八字段**（见下）
- ❌ 不提交密钥、凭据、个人路径、内部代号

---

## 三、新增一个技能

### 3.1 目录结构（标准）

```
skills/<skill-name>/
├── SKILL.md              # 必需：技能说明（含 frontmatter）
├── scripts/
│   └── <main>.py         # 必需：可运行脚本
├── references/           # 可选：参考文档
└── assets/               # 可选：模板、数据
```

### 3.2 SKILL.md frontmatter（八字段，以质量门禁判据为准）

```yaml
---
name: skill-name                  # 与目录名一致，kebab-case
slug: skill-name
version: 1.0.0                    # 语义化版本
author: 你的笔名@SynomosAI         # 署名
license: MIT
category: AI 治理                  # 分类
description: >                    # 双语（EN + 中文），含触发词/场景
  What it does and when to use it. 中文：做什么、什么时候用。
display_name: 显示名               # 或 displayName
---
```

### 3.3 命名规范

| 类型 | 前缀 | 示例 |
|---|---|---|
| LGD 护城河系列 | `lgd-` | `lgd-badge-issuer` |
| 通用治理技能 | 无前缀 | `agent-trace-audit` |
| 领域合规技能 | 领域缩写 | `fin-reg-calc`、`gov-disclosure-check` |

> ⚠️ 不要用 `medxpert-` 前缀 —— 该前缀属医疗器械合规品牌线，与本项目（SynomosAI 治理线）严格隔离。

---

## 四、提 PR 前必须自检

**运行质量门禁**：

```bash
python skills/skill-quality-gate/scripts/quality_gate.py --dir skills/<your-skill>
```

输出示例：

```
质量门禁：skills/token-disclosure-check
========================================
  [PASS] frontmatter八字段
  [PASS] 脚本可编译
  [PASS] 图标icon.png
  [PASS] README双语
  [PASS] 无密钥明文
  [FAIL] description双语
  [FAIL] 触发词/场景
  [PASS] 门禁/铁律节
  [PASS] 去敏无泄漏
========================================
结果：7/9  → 🔒 拦截发布
```

**九维检查清单**（与门禁脚本对应的判据）：

- [ ] frontmatter 八字段齐备（`name` / `slug` / `version` / `author` / `license` / `category` / `description` / `display_name`）
- [ ] 脚本可编译（`python -m py_compile`）
- [ ] 有图标 `icon.png`
- [ ] README 双语（EN + 中文）
- [ ] `description` 双语
- [ ] 含触发词 / 使用场景
- [ ] 含门禁 / 铁律节
- [ ] 无密钥明文
- [ ] 去敏无泄漏

---

## 五、提交规范

### 5.1 Commit message

```
<type>(<scope>): <subject>

<body>

Signed-off-by: Your Name <your@email>
```

**type**：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

示例：
```
feat(skills): add agent-cost-guard for LLM budget gating

Closes #42

Signed-off-by: Zhao Xinghua <steven@example.com>
```

### 5.2 DCO（开发者原创声明）

本项目采用 **DCO**（而非 CLA）。**在 commit 中加 `Signed-off-by` 即表示你声明**：

> 该贡献由我原创，或我有权按本项目的开源许可提交，且我同意按本项目许可分发。

```bash
# 自动加签名
git commit -s -m "feat: add xxx"
```

> 用 CLA 的项目门槛高，用 DCO 的项目更开放 —— 我们选后者。

---

## 六、评审流程

```
提 Issue / PR
   ↓
自动检查（如有配置）
   ↓
维护者评审（通常 7 天内给回复）
   ↓
可能需要修改 → 你更新 PR
   ↓
合并 → 进入 CHANGELOG
```

**评审关注点**：
1. 是否符合三律精神（有籍 / 有证 / 有门禁）
2. 是否零依赖、可独立运行
3. 是否有可验证的输出
4. 是否有清晰边界声明

---

## 七、红线（会被直接关闭的 PR）

| 情形 | 说明 |
|---|---|
| ❌ 引入第三方依赖 | 本项目坚持零依赖 |
| ❌ 提交密钥 / 凭据 | 严重安全问题 |
| ❌ 包含个人隐私数据 | 包括测试数据 |
| ❌ 冒充官方 / 误导性宣传 | 不得声称"官方认证" |
| ❌ 用于欺骗、绕过监管的用途 | 与项目理念相悖 |
| ❌ 改动 LICENSE / 版权署名 | 需维护者单独讨论 |
| ❌ 把 `medxpert-` 医疗品牌线内容混入 | 品牌隔离铁律 |

---

## 八、署名与版权

- **版权**：`© SynomosAI`（见 [LICENSE](LICENSE)）
- **学术引用**：理论主张署名 `Zhao, X.` + ORCID `0009-0001-0512-1237`
- **贡献者**：你的贡献会记录在 CHANGELOG 与 git history 中
- **品牌**：项目名称与徽章使用权归 SynomosAI，不得用于误导性宣传

---

## 九、有问题？

- 开 Issue 打 `question` 标签
- 或先看 [README](README.md) 与 [规范总页](https://medxpert.cn/uibc/standards/)

**再次感谢 —— 标准要成立，必须先能被自由获得。你正在帮它成立。**
