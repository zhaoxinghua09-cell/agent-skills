#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aml-sentinel — 反洗钱(AML)哨兵纵深工具（零依赖）。
对交易做可疑模式检测(拆分/快进快出/跨境无KYC/大额未报备)，输出风险等级。
理论真源：LGD 凡自治之物三律（MedXpert × SynomosAI）。"""
import argparse, json, sys
NAME = "aml-sentinel"
def scan(tx):
    hits = []
    amt = float(tx.get("amount", 0) or 0)
    kyc = bool(tx.get("counterparty_kyc"))
    cross = bool(tx.get("cross_border"))
    structured = bool(tx.get("structured"))
    freq = int(tx.get("freq", 0) or 0)
    fast = bool(tx.get("fast_in_out"))
    if amt >= 50000 and not tx.get("reported"): hits.append("大额未报备")
    if (amt >= 50000 or cross) and not kyc: hits.append("无对手KYC")
    if cross and not kyc: hits.append("跨境无KYC")
    if structured: hits.append("拆分/结构化交易")
    if fast and freq >= 3: hits.append("快进快出+高频")
    score = min(100, len(hits) * 25 + (30 if cross else 0))
    level = "高" if score >= 70 else ("中" if score >= 40 else "低")
    return {"hits": hits, "score": score, "level": level, "risk": score >= 70}
def run_selftest():
    """自检：跑真实 scan()/main() 并断言 AML 判定——
    普通小额已 KYC 交易零命中低风险（须过）；大额+跨境+拆分+快进快出五项全中高风险（须拦）。"""
    import contextlib, io
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(argv):
        old = sys.argv
        sys.argv = ["aml_sentinel.py"] + argv
        buf = io.StringIO()
        code = 0
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                main()
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        finally:
            sys.argv = old
        return code

    clean = {"amount": 100, "counterparty_kyc": True}
    r = scan(clean)
    check("干净交易零命中低风险",
          r["hits"] == [] and r["score"] == 0 and r["level"] == "低" and r["risk"] is False)
    dirty = {"amount": 80000, "cross_border": True, "structured": True,
             "fast_in_out": True, "freq": 5}
    r = scan(dirty)
    check("可疑交易五项全中且高风险",
          len(r["hits"]) == 5 and "跨境无KYC" in r["hits"]
          and r["score"] == 100 and r["level"] == "高" and r["risk"] is True)
    check("main 干净交易 rc=0", run(["--tx", json.dumps(clean), "--json"]) == 0)
    check("main 高风险交易 rc=1", run(["--tx", json.dumps(dirty), "--json"]) == 1)
    check("main 无输入 rc=2", run([]) == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description=NAME + " · AML哨兵")
    ap.add_argument("--selftest", action="store_true", help="自检（内置交易夹具，不读外部文件）")
    ap.add_argument("--tx", help="单笔交易 JSON")
    ap.add_argument("--file", help="交易JSONL文件(逐行)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.tx and not a.file:
        print("用法: --tx <JSON> | --file <path>", file=sys.stderr); sys.exit(2)
    results = []
    if a.tx:
        try: results.append(scan(json.loads(a.tx)))
        except Exception as e: print("tx JSON 解析失败: " + str(e), file=sys.stderr); sys.exit(2)
    if a.file:
        for line in open(a.file, encoding="utf-8"):
            line = line.strip()
            if line: results.append(scan(json.loads(line)))
    any_high = any(r["risk"] for r in results)
    if a.json: print(json.dumps({"results": results, "any_high_risk": any_high}, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · AML 检测 ===")
        for r in results:
            print("  风险" + str(r["score"]) + " " + r["level"] + " 命中:" + (",".join(r["hits"]) or "无"))
        print("  结论: " + ("存在高风险 ⛔" if any_high else "未发现高风险 ✅"))
    sys.exit(1 if any_high else 0)
if __name__ == "__main__":
    main()
