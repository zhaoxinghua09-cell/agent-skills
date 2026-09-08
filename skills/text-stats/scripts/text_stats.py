import argparse, glob, json, os, re, sys
from collections import Counter

def main():
    ap = argparse.ArgumentParser(description="text-stats · 文本统计（字数/行数/词频/阅读时长）")
    ap.add_argument("--file"), ap.add_argument("--dir")
    ap.add_argument("--ext", default=".txt,.md", help="目录模式下的扩展名（逗号分隔）")
    ap.add_argument("--top", type=int, default=10, help="词频TopN")
    ap.add_argument("--cjk-chars", type=int, default=400, help="每分钟阅读字数")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.file and not a.dir:
        ap.error("需要 --file 或 --dir")
    files = ([a.file] if a.file else
             [f for e in a.ext.split(",") for f in glob.glob(os.path.join(a.dir, "**", "*" + e), recursive=True)])
    chars = words = lines = 0
    freq = Counter()
    for f in files:
        try:
            txt = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        chars += len(txt.replace(" ", "").replace("\n", ""))
        lines += txt.count("\n") + (0 if txt.endswith("\n") or not txt else 1)
        words += len(re.findall(r"[A-Za-z0-9_]+", txt))
        freq.update(w for w in re.findall(r"[\u4e00-\u9fff]{2,6}|[A-Za-z][A-Za-z0-9_]+", txt) if len(w) > 1)
    minutes = max(1, round(chars / a.cjk_chars))
    if a.json:
        print(json.dumps({"files": len(files), "chars": chars, "words": words, "lines": lines,
                          "read_minutes": minutes,
                          "top": freq.most_common(a.top)}, ensure_ascii=False, indent=2))
    else:
        print("文件: %d ｜ 字符: %d ｜ 英文词: %d ｜ 行: %d ｜ 预计阅读: %d 分钟" % (len(files), chars, words, lines, minutes))
        print("词频 Top %d: %s" % (a.top, ", ".join("%s(%d)" % kv for kv in freq.most_common(a.top))))
    sys.exit(0)

if __name__ == "__main__":
    main()
