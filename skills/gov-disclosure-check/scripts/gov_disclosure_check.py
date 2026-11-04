#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gov-disclosure-check — 政务公开披露校验纵深工具（零依赖）。
校验公开信息是否含强制披露字段(决策依据/责任部门/时限/救济渠道/数据来源)。
理论真源：LGD 凡自治之物三律（MedXpert × SynomosAI）。"""
import argparse, json, sys
NAME = "gov-disclosure-check"
REQUIRED = [
    ("决策依据", ["依据", "法", "条例", "规定", "policy"]),
    ("责任部门", ["责任部门", "主办", "牵头", "负责单位"]),
    ("时限", ["时限", "期限", "截止", "ddl", "deadline"]),
    ("救济渠道", ["复议", "诉讼", "救济", "申诉", "投诉"]),
    ("数据来源", ["来源", "数据", "统计", "口径"]),
]
def check(text):
    t = (text or "").lower()
    missing = [name for name, hints in REQUIRED if not any(h.lower() in t for h in hints)]
    return {"missing": missing, "complete": len(missing) == 0}
def run_selftest():
    """自检:跑真实 check()/main()——五字段齐全文本须判 complete 且 main rc=0(须过);
    空泛通知须五字段全缺且 main rc=1(须拦);无输入须 rc=2。
    注:断言助手命名 expect,避免遮蔽本模块 check()。只用内置夹具文本。"""
    import contextlib, io
    passed = failed = 0
    def expect(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)
    def call_main(argv):
        old = sys.argv
        sys.argv = ["gov_disclosure_check.py"] + argv
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
    full = "依据《政府信息公开条例》规定，责任部门为市监局，应在15日期限内办结；不服可申请行政复议或提起诉讼。数据来源：本局统计口径说明。"
    r = check(full)
    expect("五字段齐全→complete", r["complete"] is True and r["missing"] == [])
    r = check("通知：明天开会。")
    expect("空泛通知→五字段全缺", r["complete"] is False and len(r["missing"]) == 5)
    code, _ = call_main(["--text", full])
    expect("main 完整文本 rc=0", code == 0)
    code, _ = call_main(["--text", "通知：明天开会。"])
    expect("main 缺字段 rc=1", code == 1)
    code, _ = call_main([])
    expect("main 无输入 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1
def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description=NAME + " · 公开披露校验")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--text", help="公开信息文本")
    ap.add_argument("--file", help="文本文件")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.text and not a.file: print("用法: --text <str> | --file <path>", file=sys.stderr); sys.exit(2)
    text = a.text or open(a.file, encoding="utf-8").read()
    r = check(text)
    if a.json: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 公开披露校验 ===")
        print("  缺失字段: " + (",".join(r["missing"]) or "无"))
        print("  结论: " + ("披露完整 ✅" if r["complete"] else "缺强制披露 ⛔"))
    sys.exit(0 if r["complete"] else 1)
if __name__ == "__main__":
    main()
