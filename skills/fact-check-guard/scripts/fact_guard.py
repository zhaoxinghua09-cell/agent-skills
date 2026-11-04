# -*- coding: utf-8 -*-
"""事实核查：声明列表对照来源文本，逐条标 已支撑/存疑/无来源。零依赖。"""
import argparse, json, pathlib, re, sys

def load_lines(p):
    """支持三种输入：@文件路径 / 已存在的纯文件路径 / 内联文本(按行拆分)。"""
    if p.startswith("@"):
        p = p[1:]
    if pathlib.Path(p).is_file():
        raw = pathlib.Path(p).read_text(encoding="utf-8")
    else:
        raw = p
    return [l.strip() for l in raw.splitlines() if l.strip()]

def support(claim, sources):
    c = claim.lower()
    # 抽取声明里的实体词（>=2字中文 或 >=4英文字母）
    ents = set(re.findall(r"[一-鿿]{2,}|[a-z]{4,}", c))
    if not ents:
        return "存疑", "无可比对实体"
    hits = 0
    for s in sources:
        sl = s.lower()
        if sum(1 for e in ents if e in sl) >= max(1, len(ents) // 2):
            hits += 1
    if hits >= 1:
        return "已支撑", f"来源命中 {hits} 处"
    return "无来源", "检索无实质支撑"


def run_selftest():
    """自检：跑真实 support()/load_lines()/main()——实体命中来源的声明须标
    「已支撑」（须过）；无命中须标「无来源」、无实体须标「存疑」（须拦）。
    来源与声明只写临时目录/内置文本。"""
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
        sys.argv = ["fact_guard.py"] + argv
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

    src = ["根据国家统计局数据，中国的首都 是北京，人口众多"]
    st, _ = support("中国的首都", src)
    check("实体命中来源→已支撑", st == "已支撑")
    st, _ = support("火星的天气", src)
    check("实体无命中→无来源", st == "无来源")
    st, _ = support("42", src)
    check("无可比对实体→存疑", st == "存疑")
    check("load_lines 内联拆行去空", load_lines(" 甲 \n\n 乙 ") == ["甲", "乙"])
    with tempfile.TemporaryDirectory() as td:
        cf = pathlib.Path(td) / "claims.txt"
        sf = pathlib.Path(td) / "sources.txt"
        cf.write_text("中国的首都\n火星的天气\n", encoding="utf-8")
        sf.write_text("根据国家统计局数据，中国的首都 是北京，人口众多\n", encoding="utf-8")
        code, out = call_main(["--claims", str(cf), "--sources", str(sf), "--json"])
        d = json.loads(out)
        sts = [r["status"] for r in d["results"]]
        check("main 文件输入两条判定正确", code == 0 and sts == ["已支撑", "无来源"])
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--claims", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    claims = load_lines(a.claims)
    sources = load_lines(a.sources)
    out = []
    for c in claims:
        st, why = support(c, sources)
        out.append({"claim": c, "status": st, "why": why})
    if a.json:
        print(json.dumps({"results": out}, ensure_ascii=False, indent=2))
    else:
        for o in out:
            icon = "✅" if o["status"] == "已支撑" else "⚠️" if o["status"] == "存疑" else "🔒"
            print(f"  {icon} [{o['status']}] {o['claim']}  ({o['why']})")

if __name__ == "__main__":
    main()
