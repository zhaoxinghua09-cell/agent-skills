# -*- coding: utf-8 -*-
"""智能体紧急制动卡：部署智能体前生成『紧急制动卡』。零依赖。

先想好怎么停，再放它跑。--check 校验制动卡完整性，缺项 rc=1 拦下上线。
三律映射：LGD-III 有门禁 —— 制动是门禁的最后一档。

用法：
  生成：python agent_kill_switch.py --agent crawler-bot \
      --conditions "连续5次报错" "输出含客户PII" "单日费用超¥200" \
      --revoke "撤 API key" --owner 运维-王五 --out cards/crawler.json
  校验：python agent_kill_switch.py --check cards/crawler.json
"""
import argparse, json, pathlib, sys

REQUIRED = ["agent", "conditions", "revoke", "owner", "recovery", "generated_at"]


def cmd_issue(a):
    card = {"card_type": "lgd-agent-kill-switch", "agent": a.agent,
            "conditions": a.conditions or [], "revoke": a.revoke,
            "owner": a.owner, "recovery": a.recovery,
# skillgate: ignore
            "generated_at": __import__("datetime").date.today().isoformat()}
    miss = []
    if not card["conditions"]:
        miss.append("conditions(停止条件)")
    for k in ("revoke", "owner", "recovery"):
        if not card[k]:
            miss.append(k)
    if miss:
        print("⛔ 制动卡不完整，禁止上线，缺：" + "、".join(miss))
        sys.exit(1)
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.json:
        print(json.dumps({"issued": True, "card": card}, ensure_ascii=False, indent=2))
    else:
        print("✅ 制动卡已生成：" + card["agent"])
        print("  停止条件：")
        for c in card["conditions"]:
            print("   - " + c)
        print(f"  断权动作：{card['revoke']}   责任人：{card['owner']}   恢复条件：{card['recovery']}")
    sys.exit(0)


def cmd_check(a):
    q = a.check[1:] if a.check.startswith("@") else a.check
    try:
        raw = pathlib.Path(q).read_text(encoding="utf-8") if pathlib.Path(q).is_file() else a.check
        card = json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        print(f"制动卡不可读/非 JSON：{e}", file=sys.stderr)
        sys.exit(2)
    miss = [k for k in REQUIRED if not card.get(k)]
    empty = ("conditions" not in miss) and not card.get("conditions")
    if empty:
        miss.append("conditions(停止条件为空)")
    ok = not miss
    if a.json:
        print(json.dumps({"check_ok": ok, "missing": miss}, ensure_ascii=False, indent=2))
    else:
        print(("✅ 制动卡完整，可上线" if ok else "⛔ 缺项：" + "、".join(miss)))
    sys.exit(0 if ok else 1)


def run_selftest():
    """自检：临时目录内跑真实 cmd_issue()/cmd_check()——完整卡生成+校验（须过）、
    缺项生成被拦（须拦）、缺项卡校验不过（须拦）。不触碰真实文件。"""
    import contextlib, io, tempfile
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def call(fn, **kw):
        buf = io.StringIO()
        code = 0
        try:
            with contextlib.redirect_stdout(buf):
                fn(argparse.Namespace(**kw))
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        return code, buf.getvalue()

    with tempfile.TemporaryDirectory() as td:
        outp = str(pathlib.Path(td) / "card.json")
        code, _ = call(cmd_issue, agent="selftest-bot", conditions=["连续5次报错"],
                       revoke="撤 API key", owner="运维-测试", recovery="人工确认后重启",
                       out=outp, json=False)
        check("完整制动卡生成 rc=0 且落盘", code == 0 and pathlib.Path(outp).is_file())
        code, out = call(cmd_check, check=outp, json=True)
        check("完整卡校验通过 rc=0", code == 0 and json.loads(out).get("check_ok") is True)
        code, _ = call(cmd_issue, agent="selftest-bot", conditions=[], revoke="",
                       owner="", recovery="人工确认后重启",
                       out=str(pathlib.Path(td) / "bad.json"), json=False)
        check("缺条件/断权/责任人→生成被拦 rc=1", code == 1)
        badp = pathlib.Path(td) / "incomplete.json"
        badp.write_text(json.dumps({"card_type": "lgd-agent-kill-switch",
                                    "agent": "x", "conditions": ["c"]}),
                        encoding="utf-8")
        code, out = call(cmd_check, check=str(badp), json=True)
        check("缺项卡校验不过 rc=1", code == 1 and json.loads(out).get("check_ok") is False)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="智能体紧急制动卡 · 先想好怎么停")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--agent", help="生成：智能体名")
    g.add_argument("--check", help="校验：制动卡 JSON（内联/@文件/纯路径）")
    ap.add_argument("--conditions", nargs="*", default=[], help="停止条件（多条）")
    ap.add_argument("--revoke", default="", help="断权动作（如撤 key/断网/停容器）")
    ap.add_argument("--owner", default="", help="责任人")
    ap.add_argument("--recovery", default="人工确认后重启", help="恢复条件")
    ap.add_argument("--out", help="制动卡输出路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.agent:
        cmd_issue(a)
    else:
        cmd_check(a)


if __name__ == "__main__":
    main()
