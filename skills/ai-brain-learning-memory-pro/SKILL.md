---
name: ai-brain-learning-memory-pro
title: AI记忆工程实战版
display_name: AI记忆工程实战版
display_name_en: AI Memory Engineering Pro
description: "ai-brain-learning-memory 的进阶工程版，面向 AI 开发者 / 认知科学爱好者 / agent 架构师。在基础版（概念+例子+速查）之上往工程化推一步：三层记忆的参考实现（Python）、与 agent-memory 工具集成、评测电池 memory_eval_battery.py 的跑法与 6 维解读、OWASP ASI06 记忆投毒防御的代码落地、复习四节点的自动化 rrule 配置、认知科学证据→工程决策映射。建议先读基础版再读本版。触发词：大脑学习记忆进阶、记忆系统实现、memory system design、记忆架构代码、agent-memory 集成、记忆评测电池、记忆投毒防御、ASI06、间隔重复实现、遗忘曲线代码、记忆溯源、reference implementation、学习记忆工程版、brain memory pro。"
description_zh: "ai-brain-learning-memory 的进阶工程版，面向 AI 开发者 / 认知科学爱好者 / agent 架构师。在基础版（概念+例子+速查）之上往工程化推一步：三层记忆的参考实现（Python）、与 agent-memory 工具集成、评测电池 memory_eval_battery.py 的跑法与 6 维解读、OWASP ASI06 记忆投毒防御的代码落地、复习四节点的自动化 rrule 配置、认知科学证据→工程决策映射。建议先读基础版再读本版。触发词：大脑学习记忆进阶、记忆系统实现、memory system design、记忆架构代码、agent-memory 集成、记忆评测电池、记忆投毒防御、ASI06、间隔重复实现、遗忘曲线代码、记忆溯源、reference implementation、学习记忆工程版、brain memory pro。"
description_en: "Advanced engineering version of ai-brain-learning-memory. Aimed at AI developers, cognitive-science enthusiasts, and agent architects. Pushes beyond the basic version (concepts + examples + cheatsheet) into engineering-grade depth: three-tier memory reference implementation (Python), integration with the agent-memory tool, how to run memory_eval_battery.py and interpret its 6 dimensions, code-level defense against OWASP ASI06 memory poisoning, automated rrule config for the four review nodes, and cognitive-science evidence → engineering decision mapping. Recommend reading the basic version first."
version: 1.0.0
agent_created: true
author: 潘布达 (Buda Pan) @SynomosAI
license: MIT
category: AI学习方法论
platforms: [windows, macos, linux]
read_when:
  - 要把「学习记忆方法论」落地成可运行的 agent 记忆系统（写代码）时
  - 需要参考实现 / 集成 agent-memory 工具时
  - 要跑记忆评测电池、出量化结果时
  - 要在代码层防御记忆投毒（OWASP ASI06）时
  - 要配置复习四节点的自动化（rrule）时
  - 已读过基础版 ai-brain-learning-memory，想深入工程细节时
tags:
  - 学习记忆
  - 记忆架构
  - 参考实现
  - 记忆安全
  - 评测电池
  - 自动化
  - AI工程
  - 认知科学
---

<div align="center">

![LGD 头像 · 终版](lgd-avatar.png)

</div>

> **品牌归属**：本技能隶属 **LGD「凡自治之物」** 治理理论线，采用**终版头像**（3D 金属红环 + 藏青盾 + LGD 字标 + 三律横杠 + 下弧铭文"有籍·有证·有门禁"，新魏体，1536×1536，永久定版）。
> 同步挂载官方徽记「三律之盾」[lgd-shield-color.svg](lgd-shield-color.svg)（徽章程序 v1.0 · 母本 = LGD 项目号头像 B 系统化）。
> 头像与徽记 © SynomosAI 2026；理论 CC BY 4.0（DOI 10.5281/zenodo.22456647）。参照声明须回链：[LGD-theory](https://github.com/zhaoxinghua09-cell/lgd-theory）。

# AI 大脑学习记忆方法论 · 进阶工程版

> **给谁看**：AI 开发者、认知科学爱好者、agent 架构师。如果你想要"概念 + 例子 + 速查"，先读基础版 `ai-brain-learning-memory`（已改到 v2.4.0，通俗友好）。本版专讲**怎么把方法论写成能跑的代码和系统**。
> **与基础版的关系**：基础版 = 为什么 + 是什么；本版 = 怎么做（代码 / 配置 / 评测 / 防御）。两者配套，不重复概念，只补工程。

---

## 0. 工程总览（一张图看懂系统）

```
┌─────────────┐   编码(价值判断)   ┌──────────────────────┐
│  当前会话    │ ───────────────▶ │  三层记忆存储          │
│ (工作记忆)   │                   │  · 当日日志 → 情节      │
└─────────────┘   提取(先读后做)   │  · MEMORY.md → 语义    │
       ▲                          │  · skills/ → 程序性    │
       │                          └──────────┬───────────┘
       │           复习(五节点自动化)          │ 写入带溯源 + 不可信输入门
       └─────────────────────────────────────┘
                   遗忘曲线 / 间隔重复 / 记忆投毒防御
```

关键工程决策（本节结论，后面逐条展开）：
1. 记忆不是「一个向量库」，而是**三类存储 + 各自生命周期**。
2. 写入即带**溯源元数据**（来源 / 信任级），这是抗投毒的命门。
3. 提取时把所有记忆当**不可信输入**，关键动作先核实。
4. 复习靠**制度（自动化）**而非自觉。
5. 用 `memory_eval_battery.py` **量化**记忆系统质量，而不是凭感觉。

---

## 1. 参考实现：三层记忆（Python 伪代码）

下面是一套最小可运行骨架，把基础版的三层映射到代码。生产环境请替换为 agent-memory / Mem0 / Zep 等成熟库，但**分层思想不变**。

```python
import json, os, datetime
from pathlib import Path

MEM_ROOT = Path(os.environ.get("MEM_ROOT", "~/agent_memory"))  # 你的记忆根目录

class MemoryStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    # ---- 语义记忆：MEMORY.md（用户级/项目级）----
    def write_semantic(self, text: str, scope="user", source="chat", trust="medium"):
        path = self.root / ("MEMORY.md" if scope == "user" else "project_MEMORY.md")
        entry = f"\n- {text}  <!-- src={source} trust={trust} ts={datetime.date.today()} -->"
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)

    # ---- 情节记忆：当日日志（append-only）----
    def write_episodic(self, event: str, source="chat"):
        today = datetime.date.today().isoformat()
        path = self.root / f"{today}.md"
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n- [{datetime.datetime.now():%H:%M}] {event}  <!-- src={source} -->")

    # ---- 程序性记忆：技能（动作型，落 skills/）----
    def skill_exists(self, name: str) -> bool:
        return (self.root.parent / "skills" / name / "SKILL.md").exists()

    # ---- 提取：先读语义+最近情节，再行动 ----
    def retrieve(self, scope="user", days=7):
        out = []
        sem = self.root / ("MEMORY.md" if scope == "user" else "project_MEMORY.md")
        if sem.exists():
            out.append(sem.read_text(encoding="utf-8"))
        for d in range(days):
            day = (datetime.date.today() - datetime.timedelta(days=d)).isoformat()
            log = self.root / f"{day}.md"
            if log.exists():
                out.append(log.read_text(encoding="utf-8"))
        return "\n".join(out)
```

> **工程要点**：
> - 每条写入都带 `src` / `trust` / `ts` 注释——这就是「溯源元数据」，第 4 节的防御靠它。
> - `retrieve` 永远先读记忆再行动，对应基础版「阶段3·提取」。
> - 程序性记忆（技能）不走这个 store，而是独立 `skills/<name>/SKILL.md`——代码即记忆（CoALA）。

---

## 2. 与 agent-memory 工具集成

基础版提到 `agent-memory`（底层记忆存取 Python 库）。工程上推荐**直接用成熟库**，而不是自己造轮子：

| 你的需求 | 推荐 |
|---------|------|
| 轻量、本地、零依赖 | 上面 §1 的 `MemoryStore` 骨架 |
| 带向量检索 / 语义去重 | `agent-memory`（本仓库配套工具） |
| 多 agent 共享、图记忆、有效性区间 | Zep / Mem0 |
| 需要「对话压缩 + 笔记 + 子代理」长任务心法 | 直接套用 Anthropic 2025 memory tool 模式（基础版 §2 末） |

**集成检查清单**：
- [ ] 写入接口统一带溯源参数（source / trust / timestamp）
- [ ] 读取接口默认「会话开始先读语义+最近情节」
- [ ] 冲突解决：以「最新 + 带时间戳」为准
- [ ] 敏感明文（密码 / 令牌 / 密钥）在写入层**硬性拦截**，绝不落盘

---

## 3. 评测电池：memory_eval_battery.py

本技能自带 `scripts/memory_eval_battery.py`——一个**配置层自评**工具，按 6 个维度（0–5 分）量化记忆系统设计是否达标。它不依赖真实凭据、纯本地跑。

**怎么跑**：

```bash
python scripts/memory_eval_battery.py --root <你的记忆根目录> --out security_results.json
```

**6 维含义与达标线**：

| 维度 | 测什么 | 达标信号 |
|------|--------|---------|
| T 可信任 | 有无溯源 / 是否本地 / 有无 P0 风险 | 每条记忆可溯源、零联网依赖 |
| R 可靠性 | 写入是否幂等、读取是否稳定 | 重复写入不脏数据、读取不丢 |
| A 适用性 | 边界是否清楚（该记/不记） | 有明确编码判断标准 |
| C 规范性 | 文件结构 / 容量上限是否守约 | MEMORY.md ≤ 4000 字符等 |
| E 有效性 | 是否真能「学的进·记得住·用得上」 | 新会话能正确提取旧记忆 |
| S 安全性 | 投毒防御是否落地 | 不可信输入门 + 溯源 + 审计 |

**解读**：综合 ≥ 4.5 为优秀；任一维 < 3 必须修。脚本输出 JSON，可进 CI、可重跑、可附发布说明（对应发布规矩的「安全稳定性验证门」）。

> 注：基础版声称「实测全 5.0」，那是配置层自评口径（系统在本地闭环、零真实凭据下的设计合规度），不代表真实对抗强度——真实红队另算。

---

## 4. 记忆投毒防御：OWASP ASI06 的代码落地

基础版讲了投毒的原理（MINJA / MemoryGraft / AgentPoison）。工程上怎么挡？三道闸：

### 闸一：写入带溯源（每条记忆可追踪）
```python
def safe_write(self, text, source, trust):
    # 强制三件套，缺一不让写
    assert source and trust and datetime.date.today()
    self.write_semantic(f"{text}  <!-- src={source} trust={trust} ts={datetime.date.today()} -->")
```

### 闸二：提取即「不可信输入」门
```python
def act_on_memory(self, action, memory_text):
    CRITICAL = {"转账", "改价", "发消息", "删文件", "外发"}
    if any(k in action for k in CRITICAL):
        # 关键动作：记忆只是参考，必须先核实来源 + 问人确认
        if not self.verify_source(memory_text) or not self.ask_human(action):
            return "BLOCKED: 需人工确认"
    return do(action)
```

### 闸三：定期审计（异常即隔离）
```python
def audit(self):
    for entry in self.scan_all():
        if entry.trust == "unverified" and entry.age > 30:
            self.quarantine(entry)   # 隔离，不删除，留痕复核
```

**四条本质差异（写进防御逻辑）**：时间解耦（单点看正常≠安全）、隐式信任（记忆无质疑）、复合效应（一条毒污染全部未来）、检测困难（LLM 检测器漏 66%）。所以**默认不信任记忆**，关键动作必核实。

---

## 5. 复习四节点的自动化配置（rrule）

基础版「第四节」列了当日/每周/30天/季度五节点。工程上用调度器的 rrule 落地（以 WorkBuddy automation 为例）：

| 节点 | rrule | 动作 |
|------|-------|------|
| 当日复盘 | `FREQ=DAILY;BYHOUR=23;BYMINUTE=30` | 写当日日志（情节编码） |
| 每周归拢 | `FREQ=WEEKLY;BYDAY=SU;BYHOUR=22` | 蒸馏进 MEMORY.md（语义巩固） |
| 月度蒸馏 | `FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=2` | 旧日志归档（修剪） |
| 季度审查 | `FREQ=MONTHLY;INTERVAL=3;BYMONTHDAY=1` | 技能库重访（程序性重激活） |

> 路径用环境变量 `MEM_ROOT` 注入，不在技能里硬编码绝对路径（避免泄露本地布局，也便于多环境）。

---

## 6. 认知科学证据 → 工程决策映射

基础版有 9 条人脑学习法。这里给「研究 → 我必须在系统里做什么」的硬映射：

| 研究（出处） | 工程必须做的 |
|------------|------------|
| 艾宾浩斯遗忘曲线（1885，2015 复现） | 写入后必须有「复习节点」调度，否则默认遗忘 |
| 间隔重复（Cepeda 2006, 317 实验/14000人） | 重访间隔随熟悉度递增，越熟查得越稀 |
| 主动回忆 > 重读（Karpicke-Blunt 2011, Science） | 日志撰写前先「合上回想」再补证，不抄对话 |
| 检索练习效应 / 合意困难（Bjork） | 提取留一点「吃力」，别全量无脑预读 |
| 情节→语义必要性（Tulving / CoALA 2024） | 必须有当日日志（情节）作为语义蒸馏的原料 |
| 程序性记忆=代码（CoALA） | 可复用流程沉淀为技能文件，不是文字 |
| 记忆投毒（OWASP ASI06 / MINJA 2025） | 写入溯源 + 提取不可信门 + 定期审计 |

> 设计记忆系统时，逐条对照此表打勾。缺一条，对应的人脑能力就「工程上没实现」。

---

## 7. 工程版自检清单

```
□ 存储分层：情节/语义/程序性三类是否各自独立存储+独立生命周期？
□ 溯源：每条写入是否带 source/trust/timestamp？
□ 提取门：关键动作（转账/改价/发消息/删/外发）是否先核实+问人？
□ 敏感拦截：密码/令牌/密钥写入层是否硬拒？
□ 复习调度：当日/周/月/季四节点是否真有自动化在跑？
□ 评测：memory_eval_battery.py 是否跑过、综合≥4.5、无维<3？
□ 容量：MEMORY.md 是否守 ≤4000(用户)/≤3000(项目) 字符？
□ 审计：能否隔离异常记忆而不破坏整体？
```

---

## 8. 参考文献与出处

工程设计与证据依据，见 `references/调研出处与证据.md`（pro 版，含工程启示列）。模块对照：

| 模块 | 出处 |
|------|------|
| 记忆架构 | CoALA（TMLR 2024）/ MemGPT / Mem0 / Zep / Anthropic memory tool (2025) |
| 记忆安全 | OWASP ASI06 / MINJA (NeurIPS 2025) / MemoryGraft / AgentPoison (NeurIPS 2024) / A-MemGuard (2025) |
| 认知科学 | Ebbinghaus / Cepeda 2006 / Karpicke-Blunt 2011 / Dunlosky 2013 / Bjork / Tulving |
| 评测电池 | `scripts/memory_eval_battery.py`（配置层 6 维自评，0–5，纯本地） |
| 配套基础版 | `ai-brain-learning-memory` v2.4.0（概念/例子/速查） |

---

## 版权与许可

© 2026 SynomosAI。本技能按 MIT 许可证开源（见 LICENSE.md）。

**知识版权声明**：本技能中的合成知识、方法论、参考实现与编排体系归「注册老炮」所有。未经授权，禁止复制、转售、二次分发，或用于训练任何机器学习/人工智能模型（含微调、蒸馏、检索增强等）。引用请注明出处。

**免责声明**：本作品按「现状」（AS IS）提供，作者不作任何明示或默示担保；因使用本作品产生的任何后果由使用者自行承担。本技能为 AI 学习方法论与工程参考，不构成专业建议。
