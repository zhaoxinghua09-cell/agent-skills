import argparse, hashlib, json, os, sys

def sha_of(path, full):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read(65536) if not full else f.read())
    return h.hexdigest()


def run_selftest():
    """自检：临时目录内跑真实 sha_of()/main()——同内容文件须成一组重复且未删时
    rc=1（须拦）；--apply 须删多余保留首个 rc=0、无重复目录须 rc=0（须过）。
    只用临时目录。"""
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
        sys.argv = ["dup_finder.py"] + argv
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

    def fixture(td):
        data = b"hello-lgd" * 100
        sub = os.path.join(td, "sub")
        os.makedirs(sub)
        for p in (os.path.join(td, "a.txt"), os.path.join(td, "b.txt"),
                  os.path.join(sub, "d.txt")):
            with open(p, "wb") as f:
                f.write(data)
        with open(os.path.join(td, "c.txt"), "wb") as f:
            f.write(b"unique-content")
        return data

    with tempfile.TemporaryDirectory() as td:
        data = fixture(td)
        check("sha_of 同内容同哈希、异内容异哈希",
              sha_of(os.path.join(td, "a.txt"), True)
              == sha_of(os.path.join(td, "b.txt"), True)
              != sha_of(os.path.join(td, "c.txt"), True))
        code, out = call_main(["--dir", td, "--json"])
        d = json.loads(out)
        check("报告模式：一组 3 份重复、waste=2 份、rc=1",
              code == 1 and d["groups"] == 1 and len(d["detail"][0]) == 3
              and d["waste_bytes"] == 2 * len(data) and d["removed"] == 0)
    with tempfile.TemporaryDirectory() as td:
        fixture(td)
        code, out = call_main(["--dir", td, "--apply", "--json"])
        d = json.loads(out)
        left = [p for p in (os.path.join(td, "a.txt"), os.path.join(td, "b.txt"),
                            os.path.join(td, "sub", "d.txt")) if os.path.isfile(p)]
        check("--apply 删 2 留 1 且 rc=0",
              code == 0 and d["removed"] == 2 and len(left) == 1)
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "only.txt"), "wb") as f:
            f.write(b"single")
        code, out = call_main(["--dir", td, "--json"])
        d = json.loads(out)
        check("无重复目录 rc=0 且 groups=0", code == 0 and d["groups"] == 0)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="dup-finder · 重复文件查找（默认只报告，--apply 删多余）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--min-size", type=int, default=0, help="忽略小于该KB的文件")
    ap.add_argument("--apply", action="store_true", help="删除每组重复（保留首个）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    by_size = {}
    for root, _, files in os.walk(a.dir):
        for f in files:
            p = os.path.join(root, f)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            if sz >= a.min_size * 1024:
                by_size.setdefault(sz, []).append(p)
    cand = [ps for ps in by_size.values() if len(ps) > 1]
    groups = []
    for ps in cand:
        by_head = {}
        for p in ps:
            by_head.setdefault(sha_of(p, False), []).append(p)
        for ps2 in by_head.values():
            if len(ps2) > 1:
                by_full = {}
                for p in ps2:
                    by_full.setdefault(sha_of(p, True), []).append(p)
                for ps3 in by_full.values():
                    if len(ps3) > 1:
                        groups.append(sorted(ps3))
    waste = sum(os.path.getsize(g[i]) for g in groups for i in range(1, len(g)))
    removed = 0
    if a.apply:
        for g in groups:
            for p in g[1:]:
                try:
                    os.remove(p); removed += 1
                except OSError:
                    pass
    if a.json:
        print(json.dumps({"groups": len(groups), "waste_bytes": waste,
                          "removed": removed,
                          "detail": [[os.path.relpath(p, a.dir) for p in g] for g in groups]},
                         ensure_ascii=False, indent=2))
    else:
        print("重复组: %d ｜ 可释放: %.1f MB%s" % (len(groups), waste / 1048576,
              " ｜ 已删 %d 个" % removed if a.apply else "（默认只报告，--apply 删多余保留首个）"))
        for g in groups:
            print("  [组] " + g[0])
            for p in g[1:]:
                print("        dup " + p)
    sys.exit(1 if groups and not a.apply else 0)

if __name__ == "__main__":
    main()
