# 政务AI治理守门（Government AI Governance Guard）

LGD 三律跨域首占件 · 把"有籍·有证·有门禁"翻译进「政务 / 公共部门 AI 应用（决策辅助·公开答复·数据治理）」本域合规语言。

## 痛点
政务AI要求数据不出域、可审计、分级审批；市面无把三律映射到政务治理语境、且强调'不出域'的工具。

## 快速开始
```bash
python gov_guard.py --rubric
python gov_guard.py --system "你的系统描述"
python gov_guard.py --answers '{...}' --json
```

## 三律本域映射
- 有籍 → 身份/版本/来源/责任主体登记（本域术语）
- 有证 → 六类证据工件（本域证据类型）
- 有门禁 → 触发/评审/放行/复盘四道门禁（本域阈值）

## 护城河定位
本技能是"凡自治之物"标准在政务 / 公共部门 AI 应用（决策辅助·公开答复·数据治理）域的**首占定义件**——别人可抄功能，抄不走标准定义权。

![LGD-Powered](lgd-powered.png)

© XLGD · SynomosAI

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

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
