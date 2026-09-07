# -*- coding: utf-8 -*-
"""红队扫描器：中英双库扫描越狱/危险能力请求，输出风险分级+命中模式。零依赖。"""
import argparse, pathlib, re, sys

PATTERNS = [
    ("指令覆盖", re.compile(r"忽略(之前|以上|前面)的?(指令|规定|设定)|ignore (the )?(previous|above|prior) (instructions|rules)", re.I)),
    ("角色扮演越狱", re.compile(r"\bDAN\b|无限制模式|扮演(一个)?(邪恶|evil)|developer mode|无限制", re.I)),
    ("提权", re.compile(r"以(管理员|admin|root)身份|关闭安全(限制|措施)|disable (the )?safe(guard|ty)|escalate", re.I)),
    ("数据外泄", re.compile(r"打印(出)?(system prompt|系统提示)|泄露(记忆|密钥|密码|api)|print (the )?(system prompt|memory)|exfiltrat", re.I)),
    ("自修改", re.compile(r"修改(你|自己)的?(代码|规则|指令)|modify (your|its) (own )?(code|rules|instructions)|self-?improv", re.I)),
    ("去约束", re.compile(r"不要(再)?(遵守|受限)|不用(遵守|管)规则|ignore (all )?constraints|without (any )?restriction", re.I)),
]

TIER = {"指令覆盖": "🔴高危", "数据外泄": "🔴高危", "自修改": "🔴高危",
        "提权": "🔴高危", "角色扮演越狱": "🟡中危", "去约束": "🟡中危"}

def scan(text):
    hits = []
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            hits.append((name, m.group(0)))
    return hits

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    a = ap.parse_args()
    text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8")
    hits = scan(text)
    if not hits:
        print("✅ 未发现已知红队模式")
        return
    tiers = {}
    for name, frag in hits:
        tiers.setdefault(TIER.get(name, "🟡中危"), []).append((name, frag))
    print(f"⚠️ 命中 {len(hits)} 处：")
    for tier in ("🔴高危", "🟡中危"):
        if tier in tiers:
            print(f"  {tier}")
            for name, frag in tiers[tier]:
                print(f"    - [{name}] …{frag}…")
    if "🔴高危" in tiers:
        print("\n🔒 处置：高危请求直接拦截，不执行、不解释攻击细节。")

if __name__ == "__main__":
    main()
