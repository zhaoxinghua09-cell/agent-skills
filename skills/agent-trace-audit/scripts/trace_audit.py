# -*- coding: utf-8 -*-
"""行为留痕审计：读 JSONL 动作日志，建账本，标出未过闸越界项。零依赖。"""
import argparse, json, pathlib, sys

def run_selftest():
    """自检：临时目录写 JSONL 动作日志，跑真实 main() 并断言审计判定——
    过闸写+未过闸读=无越界（须过）；未过闸写操作被标违规（须拦）。"""
    import contextlib, io, tempfile
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(log_path):
        old = sys.argv
        sys.argv = ["trace_audit.py", "--log", str(log_path)]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                main()
        finally:
            sys.argv = old
        return buf.getvalue()

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        clean = td / "clean.jsonl"
        clean.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in [
            {"ts": "2026-11-04T09:00:00", "actor": "bot", "action": "写入报告",
             "target": "r.md", "gate": "l3-gate"},
            {"ts": "2026-11-04T09:01:00", "actor": "bot", "action": "读取数据",
             "target": "d.csv"},
        ]) + "\n", encoding="utf-8")
        out = run(clean)
        check("过闸写+只读→无越界", "行为账本（2 条）" in out and "✅ 无越界写操作" in out)
        bad = td / "bad.jsonl"
        bad.write_text(json.dumps(
            {"ts": "2026-11-04T10:00:00", "actor": "bot", "action": "写入数据库",
             "target": "db"}, ensure_ascii=False) + "\n", encoding="utf-8")
        out = run(bad)
        check("未过闸写操作→违规 1 条", "违规（未过闸写操作）：1 条" in out and "🔒越界" in out)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--log", required=True)
    a = ap.parse_args()
    rows = []
    for line in pathlib.Path(a.log).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    if not rows:
        print("无动作记录")
        return
    rows.sort(key=lambda r: r.get("ts", ""))
    violations = []
    print(f"行为账本（{len(rows)} 条）：\n" + "=" * 50)
    for r in rows:
        gate = r.get("gate", "无闸")
        flag = "🔒越界" if gate in ("无闸", "ungated", None) and r.get("action", "").find("写") >= 0 else ""
        if flag:
            violations.append(r)
        print(f"  {r.get('ts','?')} | {r.get('actor','?')} | {r.get('action','?')} → {r.get('target','?')} | gate={gate} {flag}")
    print("=" * 50)
    print(f"违规（未过闸写操作）：{len(violations)} 条" if violations else "✅ 无越界写操作")

if __name__ == "__main__":
    main()
