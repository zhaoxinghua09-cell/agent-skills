# -*- coding: utf-8 -*-
"""法规动态雷达：扫目录(.md)抽取监管关键词，按主题归类并留痕。零依赖。"""
import argparse, pathlib, re, sys

THEMES = {
    "风险分级": re.compile(r"high-?risk|高风险|风险分级|风险分类", re.I),
    "透明度": re.compile(r"透明|披露|标识|transparen|disclos", re.I),
    "数据": re.compile(r"训练数据|数据(集|保护)|隐私|GDPR|personal data", re.I),
    "准入": re.compile(r"上市|备案|登记|准入|market access|conformity|ce 标志", re.I),
}
REG = re.compile(r"EU AI Act|NMPA|FDA|GDPR|人工智能法|AI Act|脆监会|网信办", re.I)

def run_selftest():
    """自检：临时目录写法规/无关两类 .md，跑真实 main() 并断言雷达判定——
    含监管关键词的条目被抽取并归类（须过）；无关条目与 --since 过滤后零命中（须拦）。"""
    import contextlib, io, tempfile
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
        sys.argv = ["policy_radar.py"] + argv
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                main()
        finally:
            sys.argv = old
        return buf.getvalue()

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "reg.md").write_text(
            "# 法规月报\nEU AI Act 对高风险系统要求披露训练数据来源（2026-09 更新）。\n",
            encoding="utf-8")
        (td / "plain.md").write_text("# 团建通知\n周五下午茶，地点三楼。\n",
                                     encoding="utf-8")
        out = run(["--dir", str(td)])
        check("法规条目被抽取且归类风险分级",
              "法规动态（1 条）" in out and "风险分级" in out and "reg.md" in out)
        out = run(["--dir", str(td), "--since", "2027-01"])
        check("--since 过滤后零命中", "本月无新增法规相关条目" in out)
        empty = td / "empty"
        empty.mkdir()
        out = run(["--dir", str(empty)])
        check("空目录零命中", "本月无新增法规相关条目" in out)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--since", default="")
    a = ap.parse_args()
    d = pathlib.Path(a.dir)
    hits = []
    for p in sorted(d.glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        if a.since and a.since not in txt:
            # 简单按 since 过滤（如 2026-09）
            if not re.search(a.since, txt):
                continue
        for line in txt.splitlines():
            if REG.search(line):
                themes = [name for name, pat in THEMES.items() if pat.search(line)]
                if themes:
                    hits.append((p.name, line.strip()[:60], themes))
    if not hits:
        print("本月无新增法规相关条目")
        return
    print(f"法规动态（{len(hits)} 条）：\n" + "=" * 40)
    for f, line, themes in hits:
        print(f"  [{','.join(themes)}] {f}: {line}")

if __name__ == "__main__":
    main()
