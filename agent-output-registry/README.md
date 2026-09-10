# AI 产出有籍登记器（LGD-I 有籍）· agent-output-registry

> LGD-I 有籍 · 凡造必登。给每条 AI 产出发一张「籍」（户口），可溯源、可证完整性、可查归属。

## 用法

```bash
# 登记（--out 传文件路径或文本）
python scripts/output_registry.py add --out 报告.txt --model qwen3.5 --version 9b \
  --prompt "写合规总结" --issuer MedXpert --license MIT
# → 返回籍号 LGD-REG-xxxxxxxx

python scripts/output_registry.py verify --id LGD-REG-xxxxxxxx --out 报告.txt   # 证完整性
python scripts/output_registry.py lookup --id LGD-REG-xxxxxxxx                  # 查归属
python scripts/output_registry.py report                                        # 列全部
```

台账落 `registry/`（md + csv + jsonl），纯离线零依赖。

## 解决痛点

AI 产出说不清来源、被改了认不出、权属扯不清 → 指纹 + 模型/版本/提示哈希 + 权属人 = 可举证户口。

© MedXpert × SynomosAI · MIT · LGD-Powered
