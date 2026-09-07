# -*- coding: utf-8 -*-
"""grounding 校验器：逐声明在来源里查支撑词覆盖，输出覆盖率与未覆盖清单。零依赖。"""
import argparse, pathlib, re

def entities(s):
    # 抽取 数字/专名(连续非标点)/关键短语 作为可核验实体
    toks = re.findall(r"\d+(?:\.\d+)?%|[A-Za-z][A-Za-z0-9/+.-]{2,}|[\u4e00-\u9fff]{2,8}", s)
    return set(t.lower() for t in toks if len(t) >= 2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--sources", required=True)
    a = ap.parse_args()
    claims = [l.strip() for l in pathlib.Path(a.claims).read_text(encoding="utf-8").splitlines() if l.strip()]
    src_text = pathlib.Path(a.sources).read_text(encoding="utf-8").lower()
    covered, uncovered = [], []
    for c in claims:
        es = entities(c)
        if not es:
            covered.append((c, 0))
            continue
        hit = sum(1 for e in es if e in src_text)
        cov = hit / len(es)
        if cov >= 0.5:
            covered.append((c, cov))
        else:
            uncovered.append((c, cov))
    total = len(claims)
    rate = (len(covered) / total * 100) if total else 0
    print(f"Grounding 覆盖率：{rate:.0f}%  ({len(covered)}/{total})")
    if uncovered:
        print("\n⚠️ 无来源支撑（幻觉风险）：")
        for c, cov in uncovered:
            print(f"  [{cov*100:.0f}%] {c}")
    if covered:
        print("\n✅ 有支撑：")
        for c, cov in covered:
            print(f"  [{cov*100:.0f}%] {c}")

if __name__ == "__main__":
    main()
