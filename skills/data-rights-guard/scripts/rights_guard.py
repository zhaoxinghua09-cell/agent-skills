# -*- coding: utf-8 -*-
"""数据版权护栏：读数据集清单(manifest.json)，按许可证/商用/署名/来源给可训练评级。零依赖。"""
import argparse, json, pathlib, sys

def rate(entry):
    lic = (entry.get("license") or "").strip().lower()
    commercial = entry.get("commercial", True)
    attr = entry.get("attribution", False)
    source = (entry.get("source") or "").strip()
    problems = []
    if not lic:
        problems.append("无许可证(高危)")
    if commercial is False or "non-commercial" in lic or "nc" == lic:
        problems.append("非商用锁(不可商用)")
    if attr is True and not entry.get("attributed", False):
        problems.append("需署名但未标")
    if not source:
        problems.append("来源不可溯(隔离待核)")
    if any("高危" in p or "非商用" in p for p in problems):
        return "排除", problems
    if problems:
        return "需处理", problems
    return "可训练", problems


def run_selftest():
    """自检：跑真实 rate()/main() 评级——合规条目须评「可训练」（须过）；
    无许可证/非商用须评「排除」、缺署名/缺来源须评「需处理」（须拦）。
    清单只写临时目录。"""
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
        sys.argv = ["rights_guard.py"] + argv
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

    st, probs = rate({"license": "MIT", "commercial": True, "source": "kaggle"})
    check("许可齐全条目→可训练", st == "可训练" and probs == [])
    st, probs = rate({"license": "", "source": "内部网盘"})
    check("无许可证→排除", st == "排除" and any("无许可证" in p for p in probs))
    st, probs = rate({"license": "MIT", "commercial": False, "source": "官网"})
    check("非商用锁→排除", st == "排除" and any("非商用" in p for p in probs))
    st, probs = rate({"license": "CC-BY", "attribution": True, "attributed": False,
                      "source": "官网"})
    check("需署名未标→需处理", st == "需处理" and any("需署名" in p for p in probs))
    st, probs = rate({"license": "MIT"})
    check("来源不可溯→需处理", st == "需处理" and any("来源不可溯" in p for p in probs))
    with tempfile.TemporaryDirectory() as td:
        mp = pathlib.Path(td) / "manifest.json"
        mp.write_text(json.dumps([
            {"id": "ok", "license": "MIT", "source": "kaggle"},
            {"id": "bad", "license": "", "source": "x"},
            {"id": "todo", "license": "CC-BY", "attribution": True, "source": "y"},
        ]), encoding="utf-8")
        code, out = call_main(["--manifest", str(mp), "--json"])
        d = json.loads(out)
        sts = {i["id"]: i["status"] for i in d["items"]}
        check("main 三类条目评级与 excluded=1 正确",
              code == 0 and sts == {"ok": "可训练", "bad": "排除", "todo": "需处理"}
              and d["excluded"] == 1)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.manifest).read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = items.get("items", [])
    out = []
    excl = 0
    for e in items:
        st, probs = rate(e)
        if st == "排除":
            excl += 1
        out.append({"id": e.get("id", "?"), "status": st, "problems": probs})
    if a.json:
        print(json.dumps({"items": out, "excluded": excl, "advice": "排除项不出训练集；需处理项补全后再进"}, ensure_ascii=False, indent=2))
    else:
        for o in out:
            icon = "✅" if o["status"] == "可训练" else "⚠️" if o["status"] == "需处理" else "🔒"
            print(f"  {icon} [{o['status']}] {o['id']}  {o['problems'] or ''}")
        print(f"\n排除出训练集：{excl}  建议：排除项不出集，需处理项补全后再进")

if __name__ == "__main__":
    main()
