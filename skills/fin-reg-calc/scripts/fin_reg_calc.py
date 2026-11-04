#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fin-reg-calc — 金融AI合规计算纵深工具（零依赖）。
把 LGD 三律"有证/有门禁"落地为可执行的合规计算：投资者适当性 + 大额上报阈值。
理论真源：LGD 凡自治之物三律（MedXpert × SynomosAI）。"""
import argparse, json, sys
NAME = "fin-reg-calc"
# 大额上报阈值(量级参考, 以监管最新为准)
LARGE_TX_THRESHOLD = 50000
def suitability(client_risk, product_risk):
    diff = product_risk - client_risk
    if diff <= 0:
        return "允许", True
    if diff == 1:
        return "限制(加签/告知)", True
    return "禁止(适当性不匹配)", False
def threshold(amount):
    over = amount > LARGE_TX_THRESHOLD
    return ("超大额须报备" if over else "未超阈"), (not over)
def run_selftest():
    """自检:跑真实 suitability()/threshold()/main()——同级适当性与阈值内金额须合规(须过);
    适当性高两级与超大额须判违规且 main rc=1(须拦);无参数须 rc=2。只用内置夹具。"""
    import contextlib, io
    passed = failed = 0
    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)
    def call_main(argv):
        old = sys.argv
        sys.argv = ["fin_reg_calc.py"] + argv
        buf = io.StringIO()
        code = 0
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                main()
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        finally:
            sys.argv = old
        return code, buf.getvalue()
    check("适当性同级→允许", suitability(3, 3) == ("允许", True))
    check("适当性高一级→限制但合规", suitability(3, 4) == ("限制(加签/告知)", True))
    check("适当性高两级→禁止", suitability(2, 5) == ("禁止(适当性不匹配)", False))
    check("阈值恰 50000 未超", threshold(50000) == ("未超阈", True))
    check("阈值 50001 超大额", threshold(50001) == ("超大额须报备", False))
    code, out = call_main(["--suitability", "2", "5", "--json"])
    d = json.loads(out)
    check("main 不匹配 rc=1 且 compliant=false", code == 1 and d["compliant"] is False)
    code, out = call_main(["--threshold", "100", "--json"])
    check("main 小额 rc=0", code == 0 and json.loads(out)["compliant"] is True)
    code, _ = call_main([])
    check("main 无参数 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1
def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description=NAME + " · 金融AI合规计算")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--suitability", nargs=2, type=int, metavar=("CLIENT_RISK", "PRODUCT_RISK"), help="适当性: 客户风险等级 产品风险等级(1-5)")
    ap.add_argument("--threshold", type=float, help="大额上报阈值校验: 交易金额(元)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.suitability and a.threshold is None:
        print("用法: --suitability 客户风险 产品风险 | --threshold 金额", file=sys.stderr); sys.exit(2)
    out = {}
    ok = True
    if a.suitability:
        r, c = suitability(a.suitability[0], a.suitability[1])
        out["suitability"] = {"client": a.suitability[0], "product": a.suitability[1], "result": r, "compliant": c}
        ok = ok and c
    if a.threshold is not None:
        r, c = threshold(a.threshold)
        out["threshold"] = {"amount": a.threshold, "result": r, "compliant": c}
        ok = ok and c
    out["compliant"] = ok
    if a.json: print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 金融AI合规计算 ===")
        for k, v in out.items():
            if k != "compliant": print("  " + k + ": " + json.dumps(v, ensure_ascii=False))
        print("  结论: " + ("合规 ✅" if ok else "存在违规项 ⛔"))
    sys.exit(0 if ok else 1)
if __name__ == "__main__":
    main()
