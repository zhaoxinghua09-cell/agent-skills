# AI 论断有证证据链（LGD-II 有证）· evidence-chain-builder

> LGD-II 有证 · 凡所行必有证据。把论断拆成可验证证据链，治幻觉、强举证。

## 用法

```bash
python scripts/evidence_chain.py --claim "本产品不良率低于 0.5%" \
  --evidences "2025 质检报告@official:公司QA" "客户无相关投诉@internal:客服"

python scripts/evidence_chain.py --from claim.json --json
```

证据格式：`文本@类型:来源`，类型取 `official|paper|data|internal|assertion`。可验证类型（official/paper/data）计权，其余降权。

## 边界（不编造）

本工具**不判论断真假**，只评证据质量；缺可验证证据即标「勿作结论」。

© MedXpert × SynomosAI · MIT · LGD-Powered
