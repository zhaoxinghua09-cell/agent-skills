# -*- coding: utf-8 -*-
"""提示压缩器：按 关键词密度+位置 给句子打分，按目标比例删低分句。零依赖。"""
import argparse, pathlib, re, sys

KEYWORDS = ["必须", "禁止", "默认", "重要", "关键", "不能", "务必", "require", "must", "never",
            "always", "default", "important", "key", "约束", "规则", "步骤", "注意"]
CONSTRAINT = re.compile(r"(必须|禁止|不能|务必|require|must|never|always|约束|规则)", re.I)

def split_sentences(txt):
    # 中英文句子切分（保留句号/问号/叹号/换行）
    parts = re.split(r"(?<=[。！？!?\n])", txt)
    return [p.strip() for p in parts if p.strip()]

def score(sent, idx, total):
    kw = sum(1 for k in KEYWORDS if k.lower() in sent.lower())
    length = len(sent)
    # 适中长度得分（<=120字最佳）
    length_ok = 1.0 if length <= 120 else max(0.2, 120 / length)
    # 位置权重：首尾更高
    pos = 1.0
    if idx == 0 or idx == total - 1:
        pos = 1.4
    elif idx < total * 0.2 or idx > total * 0.8:
        pos = 1.15
    return kw * 2.0 + length_ok + pos

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--ratio", type=float, default=0.5, help="保留比例 0-1")
    a = ap.parse_args()

    txt = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8")
    sents = split_sentences(txt)
    if not sents:
        print(txt)
        return
    total = len(sents)
    scored = [(i, s, score(s, i, total)) for i, s in enumerate(sents)]
    # 约束句永远保留
    keep = [i for i, s, _ in scored if CONSTRAINT.search(s)]
    # 其余按分排序删低分
    rest = sorted([x for x in scored if x[0] not in keep], key=lambda x: x[2])
    target_keep = max(len(keep), int(total * a.ratio))
    need = target_keep - len(keep)
    for i, s, sc in rest:
        if need <= 0:
            break
        keep.append(i)
        need -= 1
    keep = sorted(keep)
    out = "\n".join(sents[i] for i in keep)
    print(f"# 压缩 {total}→{len(keep)} 句 (ratio={a.ratio})\n")
    print(out)

if __name__ == "__main__":
    main()
