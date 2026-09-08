# 权限有门禁生成器 · Gate Policy Generator

![LGD-Powered](./lgd-powered.png)

> **LGD-III 有门禁（GATED）** 的执行器 ——「凡自治之物：有籍 · 有证 · 有门禁」

把一份 agent 能力清单，落成可挂载的**权限门禁策略（policy-as-code）**，划清它能 / 需评审 / 不能做的事，并内置四道门禁防越权、误删误发、失控循环。

## 痛点 → 三律映射
| 行业痛点 | LGD 三律 | 本技能做法 |
|---|---|---|
| agent 越权 | LGD-III 有门禁 | tool_allow / tool_review / tool_deny 三档边界 |
| 误删误发 | LGD-III 有门禁 | 放行门禁（release）二次确认 |
| 失控循环 | LGD-III 有门禁 | budget 上限（max_loop / max_tokens） |
| 无统一权限词汇 | LGD 标准定义权 | 四道门禁术语即行业评判尺 |

## 快速开始
```bash
# 示例策略（无需 manifest）
python scripts/gate_policy.py --preset default --json

# 从清单生成
python scripts/gate_policy.py --manifest agent_manifest.json --out policy.json

# 校验是否满足 LGD-III 四道门禁
python scripts/gate_policy.py --check policy.json
```

## 三档预设
- `default`（平衡）：高危/敏感 → deny，中危 → review，低危 → allow
- `paranoid`（严苛）：中危也 deny，循环上限 5、token 上限 5 万
- `open`（宽松）：仅敏感 deny，其余 allow，循环上限 50

## 输出结构
```json
{
  "law": "LGD-III 有门禁 (GATED)",
  "tool_allow": [...], "tool_review": [...], "tool_deny": [...],
  "gates": {"trigger":..., "review":..., "release":..., "retro":...},
  "budget": {"max_loop_iterations": 20, "max_tokens": 200000}
}
```

## 与兄弟技能
- `tool-call-guard`（第三批）= 运行时单次调用闸门
- 本技能 = 策略生成层（治理配置）

## 红线
只生成策略配置，不替代持证申报 / 合同 / 人工放行；不含密钥与内部代号。

---
© MedXpert × SynomosAI · LGD-Powered · 凡自治之物：有籍 · 有证 · 有门禁
