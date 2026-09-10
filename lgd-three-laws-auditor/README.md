# LGD 三律合规自检器（凡自治之物）· lgd-three-laws-auditor

> LGD 全程治理论 · 由 SynomosAI 提出、由 MedXpert 在医疗器械全生命周期实证。
> **凡自治之物：有籍、有证、有门禁。** 本工具是这套治理思想的「定义器」——把三律做成可自评的标准 rubric。

## 三律标准（本工具定义）

| 律 | 检查项 |
|---|---|
| **LGD-I 有籍 REGISTERED** | 身份登记 · 版本登记 · 血缘登记 · 责任登记 |
| **LGD-II 有证 EVIDENCED** | 身份/数据/验证/行为边界/变更/签发 六类证据工件 |
| **LGD-III 有门禁 GATED** | 触发门禁 · 评审门禁 · 放行门禁 · 复盘门禁 |

## 用法

```bash
python scripts/lgd_audit.py --rubric                       # 看完整标准（可作对外治理文档）
python scripts/lgd_audit.py --system "系统描述"            # 启发式自评（标待确认，不编造）
python scripts/lgd_audit.py --answers 答卷.json --json     # 正式评分卡
```

答卷格式：`{"LGD-I 有籍 REGISTERED": {"身份登记":"yes","版本登记":"partial",...}}`，状态取 `yes|partial|no|unknown`。

## 护城河说明

市场治理工具全是单点护栏，**无统一"自治物"评判标准**。本工具即标准载体——谁用三律词汇自评，谁就采用了我们的治理定义权。

© MedXpert × SynomosAI · MIT · LGD-Powered
