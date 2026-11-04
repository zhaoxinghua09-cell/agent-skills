# -*- coding: utf-8 -*-
"""评测基准生成器：读 spec(能力+边界用例)，产出 JSONL 评测集。零依赖。"""
import argparse, json, pathlib, re, sys

def parse_spec(txt):
    cases = []
    # 支持 Markdown 列表： - [能力] 输入 => 期望 (judge)
    for m in re.finditer(r"-\s*\[([^\]]+)\]\s*(.+?)\s*=>\s*(.+?)(?:\(([^)]*)\))?$", txt, re.M):
        cap, inp, exp, judge = m.group(1), m.group(2), m.group(3), m.group(4) or "包含"
        cases.append({"capability": cap.strip(), "input": inp.strip(),
                      "expect": exp.strip(), "judge": judge.strip()})
    return cases


def run_selftest():
    """自检：临时目录内跑真实 parse_spec()/main()——合法 spec 行须解析并生成
    JSONL（须过）；无用例 spec 须不产文件并提示、缺失 spec 须 rc=2（须拦）。
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
        sys.argv = ["bench_build.py"] + argv
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

    spec = ("- [摘要] 把长文压缩 => 三句话摘要 (包含)\n"
            "- [问答] 什么是LGD => 三律框架\n"
            "这行不是用例\n")
    cases = parse_spec(spec)
    check("parse_spec 解析 2 条且默认 judge=包含",
          len(cases) == 2 and cases[0]["capability"] == "摘要"
          and cases[0]["judge"] == "包含" and cases[1]["expect"] == "三律框架")
    with tempfile.TemporaryDirectory() as td:
        sp = pathlib.Path(td) / "spec.md"
        op = pathlib.Path(td) / "out.jsonl"
        sp.write_text(spec, encoding="utf-8")
        code, out = call_main(["--spec", str(sp), "--out", str(op)])
        lines = op.read_text(encoding="utf-8").splitlines() if op.exists() else []
        check("main 生成 2 条 JSONL",
              code == 0 and len(lines) == 2
              and json.loads(lines[0])["input"] == "把长文压缩"
              and "已生成 2 条" in out)
        sp2 = pathlib.Path(td) / "bad.md"
        op2 = pathlib.Path(td) / "out2.jsonl"
        sp2.write_text("没有任何用例行", encoding="utf-8")
        code, out = call_main(["--spec", str(sp2), "--out", str(op2)])
        check("无用例 spec 不产文件且提示",
              code == 0 and not op2.exists() and "未解析出用例" in out)
    code, _ = call_main(["--spec", "/nonexistent-spec-xyz.md", "--out", "/tmp/x.jsonl"])
    check("spec 不存在→rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec_p = pathlib.Path(a.spec)
    if not spec_p.exists():
        ap.error(f"spec 文件不存在: {a.spec}")
    txt = spec_p.read_text(encoding="utf-8")
    cases = parse_spec(txt)
    if not cases:
        print("spec 未解析出用例（格式：- [能力] 输入 => 期望 (judge)）")
        return
    out_p = pathlib.Path(a.out)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in cases), encoding="utf-8")
    print(f"已生成 {len(cases)} 条评测样本 → {a.out}")

if __name__ == "__main__":
    main()
