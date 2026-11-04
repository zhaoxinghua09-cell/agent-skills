import argparse, json, os, sys

def dir_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def run_selftest():
    """自检：临时目录树上跑真实 dir_size()/main()——递归求和与 Top 文件/目录
    须与夹具字节数一致（须过）；目录不存在须 rc=2（须拦）。只用临时目录。"""
    import contextlib, io, tempfile
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
        sys.argv = ["disk_scan.py"] + argv
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
        sub = os.path.join(td, "sub")
        os.makedirs(sub)
        with open(os.path.join(td, "f1.bin"), "wb") as f:
            f.write(b"x" * 1000)
        with open(os.path.join(sub, "f2.bin"), "wb") as f:
            f.write(b"y" * 2000)
        check("dir_size 递归求和=3000", dir_size(td) == 3000)
        code, out = call_main(["--dir", td, "--json"])
        d = json.loads(out)
        check("main total_bytes=3000 且最大文件为 sub/f2.bin",
              code == 0 and d["total_bytes"] == 3000
              and d["top_files"][0]["bytes"] == 2000
              and d["top_files"][0]["path"].endswith("f2.bin"))
        check("top_dirs 含 sub=2000",
              any(x["path"] == "sub" and x["bytes"] == 2000 for x in d["top_dirs"]))
    code, _ = call_main(["--dir", "/nonexistent-dir-xyz-123"])
    check("目录不存在 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="disk-scan · 目录占用扫描（只读不删）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    files = []
    subdirs = {}
    for root, dirs, fs in os.walk(a.dir):
        rel = os.path.relpath(root, a.dir)
        if rel != ".":
            subdirs[rel] = dir_size(root)
        for f in fs:
            p = os.path.join(root, f)
            try:
                files.append((os.path.getsize(p), p))
            except OSError:
                pass
    files.sort(reverse=True)
    subs = sorted(subdirs.items(), key=lambda kv: -kv[1])[:a.top]
    total = dir_size(a.dir)
    if a.json:
        print(json.dumps({"total_bytes": total,
                          "top_files": [{"path": os.path.relpath(p, a.dir), "bytes": s} for s, p in files[:a.top]],
                          "top_dirs": [{"path": k, "bytes": v} for k, v in subs]},
                         ensure_ascii=False, indent=2))
    else:
        print("总占用: %.2f MB ｜ Top %d 大文件:" % (total / 1048576, min(a.top, len(files))))
        for s, p in files[:a.top]:
            print("  %8.2f MB  %s" % (s / 1048576, os.path.relpath(p, a.dir)))
        print("Top %d 子目录:" % len(subs))
        for k, v in subs:
            print("  %8.2f MB  %s" % (v / 1048576, k))
        print("（只读扫描，删除请自行判断或配合 dup-finder）")
    sys.exit(0)

if __name__ == "__main__":
    main()
