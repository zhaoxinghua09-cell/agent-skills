import argparse, json, sys

ITEMS = [
    "数据分类分级完成（识别是否含个人信息/重要数据）",
    "取得个人单独同意（如涉个人信息）",
    "完成个人信息保护影响评估（PIA）并留存3年",
    "与境外接收方签订标准合同/通过安全评估（视门槛）",
    "留存出境记录与接收方合规承诺",
]


def run_selftest():
    """自检：跑真实 main() 出境义务判定——五项全完成须 PASS rc=0（须过）；
    部分缺项与全缺须 FAIL rc=1 且缺项编号准确（须拦）。只用内置夹具。"""
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
        sys.argv = ["data_export_check.py"] + argv
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

    code, out = run(["--have", "1,2,3,4,5", "--json"])
    d = json.loads(out)
    check("五项全完成→PASS rc=0",
          code == 0 and d["pass"] is True and d["missing_no"] == [])
    code, out = run(["--have", "1,3", "--json"])
    d = json.loads(out)
    check("缺 2,4,5→FAIL rc=1", code == 1 and d["missing_no"] == [2, 4, 5])
    code, out = run(["--json"])
    d = json.loads(out)
    check("未完成任何项→FAIL rc=1 且全缺",
          code == 1 and d["missing_no"] == [1, 2, 3, 4, 5])
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="data-export-check · 数据出境合规自检（零依赖）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--have", help="已完成项编号，逗号分隔，如 1,2,3")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    have = set()
    if a.have:
        for tok in a.have.split(","):
            tok = tok.strip()
            if tok.isdigit() and 1 <= int(tok) <= len(ITEMS):
                have.add(int(tok))
    missing = [i for i in range(1, len(ITEMS) + 1) if i not in have]
    if a.json:
        print(json.dumps({"pass": not missing, "items": ITEMS, "missing_no": missing,
                          "missing": [ITEMS[i-1] for i in missing]}, ensure_ascii=False, indent=2))
    else:
        for i, it in enumerate(ITEMS, 1):
            print(("  [x] " if i in have else "  [ ] ") + str(i) + ". " + it)
        print("  判定：" + ("PASS 可进入出境流程" if not missing else "FAIL 未满足全部前置义务"))
        print("  依据：个人信息保护法第38-39条、数据出境安全评估办法、标准合同办法。")
    sys.exit(0 if not missing else 1)

if __name__ == "__main__":
    main()
