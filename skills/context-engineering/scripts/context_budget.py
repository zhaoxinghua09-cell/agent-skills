# -*- coding: utf-8 -*-
"""上下文预算计算器 + 审计清单生成器（零依赖，stdlib only）。

用法：
  python context_budget.py --window 128000 --system sys.txt --memory mem.txt \
      --retrieval retr.txt --tool tool.txt --history hist.txt
  # 或从 stdin 直接贴文本，按 --block 指定归属
  echo "..." | python context_budget.py --window 128000 --block system

输出：各块 token 估算、窗口占比、冗余检测、审计清单（pass/warn/fail）。
token 估算：中文≈字符数/1.6，英文≈词数×1.3（粗略，够做预算决策）。
"""
import argparse
import hashlib
import sys
from pathlib import Path


def est_tokens(text: str) -> int:
    cn = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    en = len(text) - cn
    en_words = max(1, len(text.split()))
    return int(cn / 1.6 + en_words * 1.3)


def read_block(p):
    if p == "-":
        return sys.stdin.read()
    fp = Path(p)
    return fp.read_text(encoding="utf-8") if fp.exists() else ""


def redundancy_blocks(blocks: dict) -> list:
    """跨块重复检测：把每块按行做 hash 集合，找交集行。"""
    flagged = []
    names = list(blocks)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = {ln.strip() for ln in blocks[names[i]].splitlines() if len(ln.strip()) > 20}
            b = {ln.strip() for ln in blocks[names[j]].splitlines() if len(ln.strip()) > 20}
            dup = a & b
            if dup:
                flagged.append((names[i], names[j], len(dup)))
    return flagged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=128000, help="上下文窗口 token 上限")
    for b in ("system", "memory", "retrieval", "tool", "history"):
        ap.add_argument(f"--{b}", default="", help=f"{b} 块文本文件；- 表示 stdin")
    ap.add_argument("--block", help="配合 stdin 指定归属块名")
    args = ap.parse_args()

    blocks = {}
    if args.block and not args.system:
        blocks[args.block] = read_block("-")
    else:
        for b in ("system", "memory", "retrieval", "tool", "history"):
            v = getattr(args, b)
            if v != "":
                blocks[b] = read_block(v)

    if not blocks:
        print("未提供任何上下文块。用法见文件头注释。")
        return

    total = 0
    print(f"{'块':<12}{'字符':>10}{'token估算':>12}{'窗口占比':>10}   建议上限")
    print("-" * 60)
    caps = {"system": 0.15, "memory": 0.10, "retrieval": 0.40, "tool": 0.20, "history": 0.15}
    for name, txt in blocks.items():
        tk = est_tokens(txt)
        total += tk
        pct = tk / args.window
        cap = caps.get(name, 0.5)
        flag = "OK" if pct <= cap else "超预算"
        print(f"{name:<12}{len(txt):>10}{tk:>12}{pct*100:>9.1f}%   ≤{int(cap*100)}%  [{flag}]")

    print("-" * 60)
    print(f"{'合计':<12}{'':>10}{total:>12}{total/args.window*100:>9.1f}%")
    print()

    print("== 审计清单 ==")
    print(f"[相关性] 各块是否都对当前任务有用？人工复核非文本块。")
    print(f"[预算]   总占比 {total/args.window*100:.1f}%（窗口 {args.window}）" +
          (" -> 超 60% 警告" if total/args.window > 0.6 else " -> OK"))
    red = redundancy_blocks(blocks)
    if red:
        print("[冗余]   发现跨块重复，建议收敛为单一真源：")
        for a, b, n in red:
            print(f"        {a} × {b}: {n} 行重复")
    else:
        print("[冗余]   未检出明显跨块重复 -> OK")

    # 衰减提示：system 占比应最高且置顶
    if "system" in blocks and est_tokens(blocks["system"]) / args.window < 0.05:
        print("[衰减]   关键约束建议置于 system 顶部（当前占比偏低，确认已置顶）")


if __name__ == "__main__":
    main()
