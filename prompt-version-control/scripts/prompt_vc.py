# -*- coding: utf-8 -*-
"""提示版本管理：diff 两版提示，写入版本记录(JSON)。零依赖。"""
import argparse, json, pathlib, difflib, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--score", type=float, default=0.0)
    ap.add_argument("--registry", default="prompt_registry.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    old = pathlib.Path(a.old).read_text(encoding="utf-8").splitlines()
    new = pathlib.Path(a.new).read_text(encoding="utf-8").splitlines()
    diff = list(difflib.unified_diff(old, new, lineterm="", n=1))
    reg_path = pathlib.Path(a.registry)
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {"versions": []}
    ver = f"v{len(reg['versions']) + 1}"
    reg["versions"].append({
        "version": ver, "score": a.score,
        "time": datetime.datetime.now().isoformat(timespec="seconds"),
        "added": [l for l in diff if l.startswith("+") and not l.startswith("+++")],
        "removed": [l for l in diff if l.startswith("-") and not l.startswith("---")],
    })
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.json:
        print(json.dumps({"version": ver, "score": a.score, "diff_lines": len(diff)}, ensure_ascii=False, indent=2))
    else:
        print(f"登记版本：{ver}  效果分：{a.score}  变更行：{len(diff)}")
        print("已写入", a.registry)

if __name__ == "__main__":
    main()
