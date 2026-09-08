import argparse, json, os, sys

def plan_renames(files, a):
    plan = []
    for i, f in enumerate(files):
        name = os.path.basename(f)
        if a.start is not None:
            # 序号模式：prefix 或原stem + 补零序号 + suffix + 扩展名（保证不丢原名）
            stem = os.path.splitext(name)[0]
            base = a.prefix if a.prefix else stem
            ext = os.path.splitext(name)[1]
            new = "%s%0*d%s%s" % (base, max(2, len(str(a.start + len(files) - 1))), a.start + i, a.suffix or "", ext)
        else:
            new = name
            if a.replace:
                old, new_s = a.replace.split("|", 1) if "|" in a.replace else (a.replace, "")
                new = new.replace(old, new_s)
            if a.prefix:
                new = a.prefix + new
            if a.suffix:
                r, e = os.path.splitext(new)
                new = r + a.suffix + e
        if new != name:
            plan.append((f, os.path.join(os.path.dirname(f), new)))
    return plan

def main():
    ap = argparse.ArgumentParser(description="batch-renamer · 规则式批量重命名（默认预览，--apply 才执行）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix"), ap.add_argument("--suffix")
    ap.add_argument("--replace", help="查找替换，格式 旧|新")
    ap.add_argument("--start", type=int, help="按序号重命名（起始编号）")
    ap.add_argument("--ext", help="只处理该扩展名，如 .jpg")
    ap.add_argument("--apply", action="store_true", help="执行（缺省只预览）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    files = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir)
                   if os.path.isfile(os.path.join(a.dir, f))
                   and (not a.ext or f.lower().endswith(a.ext.lower())))
    plan = plan_renames(files, a)
    if a.json:
        print(json.dumps({"mode": "apply" if a.apply else "dry-run", "count": len(plan),
                          "plan": [{"from": os.path.basename(x), "to": os.path.basename(y)} for x, y in plan]},
                         ensure_ascii=False, indent=2))
    else:
        print("模式: %s ｜ 计划重命名 %d 个" % ("APPLY" if a.apply else "DRY-RUN 预览", len(plan)))
        for x, y in plan:
            print("  %s -> %s" % (os.path.basename(x), os.path.basename(y)))
    if a.apply and plan:
        for x, y in plan:
            os.rename(x, y)
        print("已执行 %d 项" % len(plan))
    elif not a.apply:
        print("预览完成，加 --apply 执行")
    sys.exit(0)

if __name__ == "__main__":
    main()
