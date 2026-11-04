# -*- coding: utf-8 -*-
"""AI供应商尽调清单：10 项 AI 采购尽调清单。零依赖。

--template 输出清单（供发供应商填）；--score 1,1,0,... 按序打分，
得分低于 --threshold(默认 0.8) rc=1 拦下签约。
三律映射：LGD-I 有籍 —— 供应商资质与承诺有据。

用法：
  python ai_vendor_checklist.py --template --vendor "XX智能" --out dd.md
  python ai_vendor_checklist.py --score 1,1,1,0,1,1,0,1,0,1 --json
"""
import argparse, json, pathlib, sys

ITEMS = [
    "1 数据权属：我方数据归我方所有，vendor 不得用于改进其模型（除非书面同意）",
    "2 训练退出：可一键/书面退出训练用途，且有生效证明",
    "3 留存期限：输入/输出留存期明确（默认应 ≤30 天或零留存）",
    "4 合规资质：具备适用法域要求的备案/认证（口径以官方最新为准）",
    "5 事故通报：安全事件 SLA（如 72h 内书面通报）写入合同",
    "6 子处理者：分包/子处理者清单披露并经我方同意",
    "7 数据出境：涉及跨境传输的，明确机制与合规路径",
    "8 模型卡：提供模型卡/系统卡（用途、限制、评测）",
    "9 审计权：我方或第三方可审计安全与数据使用",
    "10 退出迁移：终止时数据导出格式与删除证明",
]


def run_selftest():
    """自检：跑真实 main() 并断言尽调门——满分达标 rc=0（须过）、
    0.7 分低于阈值 rc=1 且缺项编号正确（须拦）、项数不对 rc=2（须拦）、模板含全 10 项（须过）。"""
    import contextlib, io
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
        sys.argv = ["ai_vendor_checklist.py"] + argv
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

    code, out = run(["--score", ",".join(["1"] * 10), "--json"])
    r = json.loads(out) if code == 0 else {}
    check("满分达标 rc=0", code == 0 and r.get("pass") is True and r.get("score") == 1.0)
    code, out = run(["--score", "1,1,0,1,1,0,1,1,0,1", "--json"])
    r = json.loads(out)
    check("0.7 分被拦 rc=1 且缺项=3/6/9",
          code == 1 and r.get("pass") is False and r.get("missed_items") == ["3", "6", "9"])
    code, _ = run(["--score", "1,1,1"])
    check("项数不对 rc=2", code == 2)
    code, out = run(["--template", "--vendor", "XX智能"])
    check("模板含供应商名与全 10 项",
          code == 0 and "XX智能" in out and ITEMS[0][:12] in out and ITEMS[9][:12] in out)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="AI供应商尽调清单 · 签约前 10 问")
    ap.add_argument("--selftest", action="store_true", help="自检（内置打分夹具，不写文件）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--template", action="store_true", help="输出清单模板")
    g.add_argument("--score", help="按 10 项顺序打分，如 1,1,0,...（0/1）")
    ap.add_argument("--vendor", default="", help="供应商名（模板用）")
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--out", help="模板输出路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.template:
        md = [f"# AI 供应商尽调清单 · {a.vendor or '（供应商）'}", "",
              "> 请供应商逐项书面回答并附证明；任一项答『否』需说明理由与替代控制。", ""] + \
             [x for x in ITEMS] + ["", "> 依据 LGD『有籍』：供应商资质与承诺留档可查。口径以官方最新为准。"]
        text = "\n".join(md)
        if a.out:
            outp = pathlib.Path(a.out)
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(text, encoding="utf-8")
        print(text if not a.json else json.dumps({"template": text, "out": a.out},
                                                 ensure_ascii=False, indent=2))
        sys.exit(0)

    try:
        vals = [int(x) for x in a.score.split(",")]
    except ValueError:
        print("score 格式应为逗号分隔的 0/1", file=sys.stderr)
        sys.exit(2)
    if len(vals) != len(ITEMS) or any(v not in (0, 1) for v in vals):
        print(f"score 须为 {len(ITEMS)} 个 0/1", file=sys.stderr)
        sys.exit(2)
    ratio = sum(vals) / len(ITEMS)
    ok = ratio >= a.threshold
    misses = [ITEMS[i].split(" ")[0] for i, v in enumerate(vals) if v == 0]
    if a.json:
        print(json.dumps({"score": ratio, "pass": ok, "missed_items": misses},
                         ensure_ascii=False, indent=2))
    else:
        print(f"尽调得分：{ratio:.0%}（阈值 {a.threshold:.0%}）")
        if misses:
            print("未达标项：" + "、".join(misses))
        print(("⛔ 得分不足，暂缓签约" if not ok else "✅ 达标（仍建议法务复核合同条款）"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
