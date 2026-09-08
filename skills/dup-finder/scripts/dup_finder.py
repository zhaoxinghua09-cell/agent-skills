import argparse, hashlib, json, os, sys

def sha_of(path, full):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read(65536) if not full else f.read())
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description="dup-finder · 重复文件查找（默认只报告，--apply 删多余）")
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
