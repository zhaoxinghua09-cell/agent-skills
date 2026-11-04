import argparse, json, sys

ITEMS = ["已阅读合约源码或第三方审计报告", "确认目标地址与审计报告一致（防假合约）",
         "明确approve授权额度（拒绝无限授权）", "知悉授权可随时撤销及撤销Gas成本",
         "私钥/助记词离线保管，绝不输入任何网页", "大额操作先小额试交互"]


def run_selftest():
    """自检：跑真实 main() 清单判定——六项全完成+限额授权须 PASS rc=0（须过）；
    缺项与无限授权须 FAIL rc=1（须拦）。只用内置夹具。"""
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
        sys.argv = ["contract_interact_checklist.py"] + argv
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

    code, out = run(["--have", "1,2,3,4,5,6", "--approve", "limited", "--json"])
    d = json.loads(out)
    check("六项全完成+限额授权→PASS rc=0",
          code == 0 and d["pass"] is True and d["missing_no"] == [])
    code, out = run(["--have", "1,2", "--json"])
    d = json.loads(out)
    check("仅完成两项→FAIL rc=1 且缺项为 3,4,5,6",
          code == 1 and d["missing_no"] == [3, 4, 5, 6])
    code, out = run(["--have", "1,2,3,4,5,6", "--approve", "unlimited", "--json"])
    d = json.loads(out)
    check("无限授权→FAIL rc=1",
          code == 1 and any("无限授权" in p for p in d["problems"]))
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="contract-interact-checklist · 智能合约交互前风险清单（零依赖）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--have", help="已完成项编号，逗号分隔，如 1,2,3")
    ap.add_argument("--approve", choices=["limited", "unlimited"], default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    have = set()
    if a.have:
        for tok in a.have.split(","):
            tok = tok.strip()
            if tok.isdigit() and 1 <= int(tok) <= len(ITEMS):
                have.add(int(tok))
    missing = [i for i in range(1, len(ITEMS) + 1) if i not in have]
    problems = []
    if missing:
        problems.append("未完成项：" + "、".join(str(i) + ". " + ITEMS[i-1] for i in missing))
    if a.approve == "unlimited":
        problems.append("无限授权(unlimited approve)高危——建议改为按次限额授权")
    if a.json:
        print(json.dumps({"pass": not problems, "items": ITEMS, "missing_no": missing,
                          "problems": problems}, ensure_ascii=False, indent=2))
    else:
        for i, it in enumerate(ITEMS, 1):
            print(("  [x] " if i in have else "  [ ] ") + str(i) + ". " + it)
        print("  判定：" + ("PASS 可交互" if not problems else "FAIL 交互前需补齐"))
        for p in problems:
            print("    - " + p)
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
