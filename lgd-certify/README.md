# LGD 三律闭环认证（有籍→有证→有门禁）· lgd-certify

> LGD 旗舰执行器。市场**唯一**把「有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章」做成闭环的 CLI。

## 三命令闭环

```bash
python scripts/lgd_certify.py init --dir ./my-ai                 # 建 evidence/ 六类骨架
python scripts/lgd_certify.py register --dir ./my-ai --name "客服助手" --id "did:web:medxpert/ka" --issuer MedXpert
python scripts/lgd_certify.py evidence --dir ./my-ai             # 放六类工件后重跑→链式哈希
python scripts/lgd_certify.py gate --dir ./my-ai                # 三律评审 PASS→certification.json + BADGES.md
```

- `register` 有籍：算法护照（三锚一票同源）+ SHA-256 指纹
- `evidence` 有证：六类证据工件（身份/数据/验证/行为边界/变更/签发）链式哈希
- `gate` 有门禁：评审 PASS/FAIL，签发认证 + medxpert.cn 三律徽章嵌入码

## 护城河

唯一闭环 + 可挂载视觉徽章（medxpert.cn/badge 已上线）。"凡用 LGD 工具即有徽章"。

© MedXpert × SynomosAI · CC BY 4.0 · LGD-Powered
