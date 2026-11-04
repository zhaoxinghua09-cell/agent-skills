import argparse, csv, json, sys


def run_selftest():
    """自检：临时 CSV 上跑真实 main()——计数/条件筛选/去重/取列四种切片须正确（须过）；
    空文件与缺失文件须分别以 rc=1/rc=2 拦下（须拦）。只用临时目录。"""
    import contextlib, io, os, tempfile
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
        sys.argv = ["csv_slice.py"] + argv
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

    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "t.csv")
        with open(fp, "w", encoding="utf-8", newline="") as f:
            f.write("姓名,城市,分数\n张三,北京,90\n李四,上海,80\n张三,北京,90\n王五,北京,70\n")
        code, out = run(["--file", fp, "--json"])
        d = json.loads(out)
        check("全量读取 total=4", code == 0 and d["total"] == 4)
        code, out = run(["--file", fp, "--where", "2=北京", "--json"])
        d = json.loads(out)
        check("条件筛选 城市=北京 → 3 行", code == 0 and d["total"] == 3)
        code, out = run(["--file", fp, "--where", "2=北京", "--dedup", "--json"])
        d = json.loads(out)
        check("筛选+去重 → 2 行且 removed=1",
              code == 0 and d["total"] == 2 and d["dedup_removed"] == 1)
        code, out = run(["--file", fp, "--cols", "1,3", "--head", "1", "--json"])
        d = json.loads(out)
        check("取列 1,3 + head 1 → 表头与首行正确",
              code == 0 and d["header"] == ["姓名", "分数"] and d["rows"] == [["张三", "90"]])
        ep = os.path.join(td, "empty.csv")
        open(ep, "w").close()
        code, _ = run(["--file", ep])
        check("空文件 rc=1", code == 1)
        code, _ = run(["--file", os.path.join(td, "nope.csv")])
        check("文件不存在 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="csv-slice · CSV 快速查看/筛选/去重（零依赖）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--file", required=True)
    ap.add_argument("--head", type=int, help="只看前N行")
    ap.add_argument("--cols", help="只取这些列（序号从1起，逗号分隔，如 1,3）")
    ap.add_argument("--where", help="条件筛选，格式 列号=值，如 2=北京")
    ap.add_argument("--dedup", action="store_true", help="整行去重")
    ap.add_argument("--count", action="store_true", help="只统计行数")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        rows = list(csv.reader(open(a.file, encoding="utf-8-sig", newline="")))
    except Exception as e:
        print("读取失败: %s" % e); sys.exit(2)
    if not rows:
        print("空文件"); sys.exit(1)
    hdr, body = rows[0], rows[1:]
    if a.where and "=" in a.where:
        ci, val = a.where.split("=", 1)
        ci = int(ci) - 1
        body = [r for r in body if ci < len(r) and r[ci] == val]
    if a.dedup:
        seen, out = set(), []
        for r in body:
            k = tuple(r)
            if k not in seen:
                seen.add(k); out.append(r)
        removed = len(body) - len(out)
        body = out
    else:
        removed = 0
    cols = None
    if a.cols:
        cols = [int(c) - 1 for c in a.cols.split(",")]
        hdr = [hdr[i] for i in cols if i < len(hdr)]
        body = [[r[i] for i in cols if i < len(r)] for r in body]
    if a.json:
        print(json.dumps({"header": hdr, "rows": body[:a.head] if a.head else body,
                          "total": len(body), "dedup_removed": removed},
                         ensure_ascii=False, indent=2))
        sys.exit(0)
    if a.count:
        print("数据行: %d（不含表头）%s" % (len(body), "｜去重删除 %d 行" % removed if removed else ""))
        sys.exit(0)
    print(" | ".join(hdr))
    for r in (body[:a.head] if a.head else body):
        print(" | ".join(r))
    tail = "（前%d行/共%d行）" % (a.head, len(body)) if a.head and len(body) > a.head else "（共%d行）" % len(body)
    print(tail + ("｜去重删除 %d 行" % removed if removed else ""))
    sys.exit(0)

if __name__ == "__main__":
    main()
