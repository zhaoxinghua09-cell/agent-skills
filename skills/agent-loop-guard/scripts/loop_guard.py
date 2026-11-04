# -*- coding: utf-8 -*-
"""失控循环护栏：读动作轨迹，监测 步数超限/重复动作/无进展，给熔断建议+诊断。零依赖。"""
import argparse, json, pathlib, re, sys

def parse_trace(p):
    rows = []
    for line in pathlib.Path(p).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"(\d+)\s+(\S+)\s*(.*)", line)
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    return rows

def run_selftest():
    """自检：临时目录写四种轨迹，跑真实 main() 并断言风险判定——
    健康轨迹=低、步数超限=高、连续重复=高、同工具无进展=中。"""
    import contextlib, io, tempfile
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(trace_path):
        old = sys.argv
        sys.argv = ["loop_guard.py", "--trace", str(trace_path), "--json"]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                main()
        finally:
            sys.argv = old
        return json.loads(buf.getvalue())

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)

        def trace(name, lines):
            p = td / name
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return p

        r = run(trace("ok.txt", ["1 search a", "2 read b", "3 write c"]))
        check("健康轨迹→低风险", r["steps"] == 3 and r["risk"] == "低")
        r = run(trace("long.txt", [f"{i} tool{i} arg{i}" for i in range(1, 36)]))
        check("35 步超上限→高风险", r["steps"] == 35 and r["risk"] == "高")
        r = run(trace("repeat.txt", ["1 search a", "2 read b", "3 click same",
                                     "4 click same", "5 click same"]))
        check("尾部连续重复同动作→高风险", r["risk"] == "高" and "重复" in r["diagnosis"])
        r = run(trace("spin.txt", [f"{i} poll status-{i}" for i in range(1, 7)]))
        check("近 6 步同工具无进展→中风险", r["risk"] == "中")
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--trace", required=True)
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows = parse_trace(a.trace)
    n = len(rows)
    risk = "低"
    advice = "继续运行"
    diag = ""
    if n > a.max_steps:
        risk = "高"; advice = "熔断：超过最大步数"; diag = f"已执行 {n} 步 > 上限 {a.max_steps}"
    # 重复动作检测
    last = rows[-a.repeat:] if len(rows) >= a.repeat else rows
    if len(last) == a.repeat and len(set((t[1], t[2]) for t in last)) == 1:
        risk = "高"; advice = "熔断：连续重复相同动作"; diag = f"第 {last[0][0]} 步起重复 {last[0][1]}({last[0][2]})"
    # 无进展（状态hash 相似，简化为 step 差值无新 tool）
    if n >= 6 and len(set(t[1] for t in rows[-6:])) == 1:
        if risk != "高":
            risk = "中"
        advice = "建议熔断：近 6 步无新动作，疑似原地打转"
        diag = diag or f"近 6 步均为 {rows[-1][1]}"
    if a.json:
        print(json.dumps({"steps": n, "risk": risk, "advice": advice, "diagnosis": diag}, ensure_ascii=False, indent=2))
    else:
        print(f"轨迹步数：{n}  风险：{risk}  建议：{advice}")
        if diag:
            print(f"  诊断：{diag}")

if __name__ == "__main__":
    main()
