import argparse, json, os, shutil, sys

MAP = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".heic"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".epub"],
    "表格": [".xls", ".xlsx", ".csv", ".ods"],
    "演示": [".ppt", ".pptx", ".key"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "视频": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "代码": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".sh", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sql"],
}

def cat_of(ext):
    for cat, exts in MAP.items():
        if ext in exts:
            return cat
    return "其他"


def run_selftest():
    """自检：临时目录内跑真实 cat_of()/main()——后缀分类须正确、预览模式只计划
    不动盘（须过）；--apply 须真移动到分类目录，目录不存在须 rc=2（须拦）。
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
        sys.argv = ["dir_organizer.py"] + argv
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

    check("cat_of 后缀分类",
          cat_of(".jpg") == "图片" and cat_of(".py") == "代码" and cat_of(".xyz") == "其他")
    with tempfile.TemporaryDirectory() as td:
        for fn in ("a.jpg", "b.pdf", "c.zzz"):
            with open(os.path.join(td, fn), "wb") as f:
                f.write(b"x")
        code, out = call_main(["--dir", td, "--json"])
        d = json.loads(out)
        plan = {p["file"]: p["to"] for p in d["plan"]}
        check("预览模式计划正确且不动盘",
              code == 0 and d["mode"] == "dry-run" and d["moved"] == 0
              and plan == {"a.jpg": "图片", "b.pdf": "文档", "c.zzz": "其他"}
              and os.path.isfile(os.path.join(td, "a.jpg")))
        code, out = call_main(["--dir", td, "--apply", "--json"])
        d = json.loads(out)
        check("--apply 真移动到分类目录",
              code == 0 and d["moved"] == 3
              and os.path.isfile(os.path.join(td, "图片", "a.jpg"))
              and os.path.isfile(os.path.join(td, "文档", "b.pdf"))
              and os.path.isfile(os.path.join(td, "其他", "c.zzz")))
    code, _ = call_main(["--dir", "/nonexistent-dir-xyz-123"])
    check("目录不存在 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="dir-organizer · 按类型整理目录（默认预览，--apply 才移动）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--apply", action="store_true", help="执行移动（缺省只预览）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    plan = []
    for f in sorted(os.listdir(a.dir)):
        p = os.path.join(a.dir, f)
        if not os.path.isfile(p):
            continue
        cat = cat_of(os.path.splitext(f)[1].lower())
        plan.append((p, os.path.join(a.dir, cat, f)))
    moved = 0
    if a.apply:
        for src, dst in plan:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst); moved += 1
    if a.json:
        print(json.dumps({"mode": "apply" if a.apply else "dry-run", "moved": moved,
                          "plan": [{"file": os.path.basename(s), "to": os.path.basename(os.path.dirname(d))} for s, d in plan]},
                         ensure_ascii=False, indent=2))
    else:
        print("模式: %s ｜ 计划归类 %d 个文件" % ("APPLY" if a.apply else "DRY-RUN 预览", len(plan)))
        for s, d in plan:
            print("  %s -> %s/" % (os.path.basename(s), os.path.basename(os.path.dirname(d))))
        if not a.apply:
            print("预览完成，加 --apply 执行（文件只移动不删除）")
    sys.exit(0)

if __name__ == "__main__":
    main()
