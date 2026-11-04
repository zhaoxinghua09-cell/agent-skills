# -*- coding: utf-8 -*-
"""记忆审计器：扫目录(.md/.jsonl)或 JSONL，标记 重复·孤儿·陈旧·无籍 四类问题。零依赖。"""
import argparse, json, pathlib, re, sys
from datetime import datetime, timezone

def norm(s):
    return re.sub(r"\s+", "", (s or "").lower())

def parse_jsonl(p):
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        out.append({
            "title": d.get("title", ""),
            "source": d.get("source", ""),
            "updated": d.get("updated", ""),
            "category": d.get("category", ""),
            "file": p.name,
        })
    return out

def parse_md(p):
    txt = p.read_text(encoding="utf-8")
    title = ""
    m = re.search(r"^#\s+(.+)$", txt, re.M)
    if m:
        title = m.group(1).strip()
    source = "source:" in txt.lower() and re.search(r"source:\s*(.+)", txt, re.I)
    updated = re.search(r"updated:\s*(\S+)", txt, re.I)
    category = re.search(r"category:\s*(\S+)", txt, re.I)
    return [{
        "title": title,
        "source": source.group(1).strip() if source else "",
        "updated": updated.group(1).strip() if updated else "",
        "category": category.group(1).strip() if category else "",
        "file": p.name,
    }]

def run_selftest():
    """自检：临时目录写 JSONL 夹具，跑真实 main() 并断言审计判定——
    干净条目零问题（须过）；重复/陈旧/无来源/无归属条目被逐类标出（须拦）。"""
    import contextlib, io, tempfile
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(path):
        old = sys.argv
        sys.argv = ["memory_audit.py", "--file", str(path), "--json"]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                main()
        finally:
            sys.argv = old
        return json.loads(buf.getvalue())

    today = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        clean = td / "clean.jsonl"
        clean.write_text(json.dumps(
            {"title": "Alpha", "source": "doc", "updated": today, "category": "ops"},
            ensure_ascii=False) + "\n", encoding="utf-8")
        r = run(clean)
        check("干净条目→零问题", r["entries"] == 1 and r["issues"] == [])
        dirty = td / "dirty.jsonl"
        rows = [
            {"title": "Alpha", "source": "doc", "updated": today, "category": "ops"},
            {"title": "Alpha", "source": "doc", "updated": today, "category": "ops"},
            {"title": "Old", "source": "doc", "updated": "2020-01-01T00:00:00+00:00",
             "category": "ops"},
            {"title": "NoSrc", "updated": today, "category": ""},
        ]
        dirty.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n",
                         encoding="utf-8")
        r = run(dirty)
        kinds = [i[0] for i in r["issues"]]
        check("条目计数=4", r["entries"] == 4)
        check("重复被标出", any(k == "重复" for k in kinds))
        check("陈旧被标出", any(k.startswith("陈旧") for k in kinds))
        check("无籍(无来源)被标出", "无籍(无来源)" in kinds)
        check("孤儿(无归属)被标出", "孤儿(无归属)" in kinds)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir")
    g.add_argument("--file")
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    entries = []
    if a.dir:
        d = pathlib.Path(a.dir)
        if not d.exists():
            ap.error(f"目录不存在: {a.dir}")
        if not d.is_dir():
            ap.error(f"不是目录: {a.dir}")
        for p in sorted(d.iterdir()):
            if p.suffix == ".jsonl":
                entries += parse_jsonl(p)
            elif p.suffix == ".md":
                entries += parse_md(p)
    else:
        f = pathlib.Path(a.file)
        if not f.exists():
            ap.error(f"文件不存在: {a.file}")
        entries = parse_jsonl(f)

    if not entries:
        print("无记忆条目可审计")
        return

    by_title = {}
    for e in entries:
        by_title.setdefault(norm(e["title"]), []).append(e)

    now = datetime.now(timezone.utc)
    issues = []
    for e in entries:
        if not e["title"]:
            issues.append(("孤儿(无标题)", e["file"], "条目缺 title"))
        if not e["category"]:
            issues.append(("孤儿(无归属)", e["file"], e["title"]))
        if not e["source"]:
            issues.append(("无籍(无来源)", e["file"], e["title"]))
        if not e["updated"]:
            issues.append(("无籍(无时间)", e["file"], e["title"]))
        else:
            try:
                dt = datetime.fromisoformat(e["updated"].replace("Z", "+00:00"))
                age = (now - dt).days
                if age > a.stale_days:
                    issues.append((f"陈旧(>{a.stale_days}天)", e["file"], f"{e['title']} ({age}天)"))
            except Exception:
                pass
        if len(by_title.get(norm(e["title"]), [])) > 1:
            issues.append(("重复", e["file"], e["title"]))

    if a.json:
        print(json.dumps({"entries": len(entries), "issues": issues}, ensure_ascii=False, indent=2))
    else:
        print(f"审计条目：{len(entries)}  问题：{len(issues)}")
        print("-" * 50)
        for kind, f, info in issues:
            print(f"[{kind}] {f}  {info}")

if __name__ == "__main__":
    main()
