"""capability_scan.py — 技能"能力声明 vs 实际用法"越界扫描（启发式、非阻塞）。

为什么需要：完整性锁能证明"字节没被改"，但证明不了"这个技能没有超出它声明的能力"。
SkillFortify（arXiv 2603.00195）用抽象解释 + 能力格 (NONE/READ/WRITE/ADMIN) 给出
soundness 证明；我们这里做的是**便宜的启发式近似**：读 SKILL.md front matter 里
声明的 capabilities，再按代码模式推断实际用到哪几类，把"用了没声明"的地方点名。

诚实边界：这是模式匹配，不是抽象解释，必然有漏报与误报。因此默认只输出
`::warning::`（不判红），加 `--strict` 才以退出码 1 结束。不要把它当成安全证明。

用法：
    python tools/capability_scan.py --root .            # 告警模式
    python tools/capability_scan.py --root . --strict    # 有越界即失败
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "tests", "fixtures", "testdata"}
CAPS = ("read", "write", "exec", "network")

# 模式 -> 能力。只用高置信度的写法，宁可漏报也不制造噪音。
PATTERNS = {
    "write": [
        r"open\([^)]*,\s*['\"](?:w|a|w\+|a\+|x)['\"]",
        r"\bos\.remove\b", r"\bos\.unlink\b", r"\bshutil\.rmtree\b",
        r"\bos\.rename\b", r"\bos\.mkdir\b", r"\bpathlib[^\n]*\.write_text\b",
        r"\.write_bytes\b", r"Path\([^)]*\)\.unlink\b",
    ],
    "exec": [
        r"\bsubprocess\.(?:run|call|check_output|Popen)\b", r"\bos\.system\b",
        r"\bos\.popen\b", r"\beval\((?![^)]*['\"]\d)", r"\bexec\(",
    ],
    "network": [
        r"\brequests\.(?:get|post|put|delete|Session)\b", r"\burllib\.request\b",
        r"\bhttpx\.", r"\bsocket\.socket\b", r"\baiohttp\b", r"\bcurl\s+-",
    ],
    "read": [],  # read 几乎是默认能力，不做推断，只用来接收声明
}

FRONT_MATTER_DECL = re.compile(r"^\s*capabilities\s*:\s*(.*)$", re.MULTILINE)


def parse_declared(text: str) -> set[str]:
    """从 SKILL.md 的 YAML front matter 里取 capabilities 列表。

    支持两种写法：
      capabilities: [read, write]
      capabilities:
        - read
        - exec
    """
    if not text.startswith("---"):
        return set()
    end = text.find("\n---", 3)
    head = text[: end if end != -1 else 400]
    declared: set[str] = set()
    m = FRONT_MATTER_DECL.search(head)
    if not m:
        return declared
    inline = m.group(1).strip()
    if inline.startswith("["):
        items = inline.strip("[]").split(",")
        declared |= {i.strip().strip("'\"").lower() for i in items if i.strip()}
    else:
        tail = head[m.end():]
        for line in tail.splitlines():
            s = line.strip()
            if s.startswith("- "):
                declared.add(s[2:].strip().strip("'\"").lower())
            elif s and not s.startswith("-"):
                break
    return {c for c in declared if c in CAPS}


def infer_used(skill_dir: Path) -> dict[str, set[str]]:
    used: dict[str, set[str]] = {c: set() for c in CAPS if c != "read"}
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            if not fn.endswith((".py", ".sh", ".ps1", ".js", ".ts")):
                continue
            p = Path(root) / fn
            try:
                if p.stat().st_size > 1_000_000:
                    continue
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:  # noqa: BLE001
                continue
            for cap, pats in PATTERNS.items():
                for pat in pats:
                    if re.search(pat, txt):
                        used[cap].add(str(p.relative_to(skill_dir)))
                        break
    return used


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve()

    skills = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        if "SKILL.md" in filenames and Path(dirpath) != root:
            skills.append(Path(dirpath))
    if not skills:
        print("capability scan: no skills found")
        return 0

    out_of_scope = 0
    undeclared_any = 0
    no_decl = 0
    for d in sorted(skills):
        text = (d / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
        declared = parse_declared(text)
        used = infer_used(d)
        if not declared:
            no_decl += 1
        extra = {c: sorted(fs) for c, fs in used.items() if fs and c not in declared}
        if not extra:
            continue
        undeclared_any += 1
        rel = d.relative_to(root).as_posix()
        detail = "; ".join(f"{c}: {', '.join(fs[:3])}" for c, fs in extra.items())
        print(f"::warning file={rel}/SKILL.md::capability not declared [{detail}]")
        if "none" in declared:
            out_of_scope += 1

    total = len(skills)
    print(
        f"capability scan: {total} skill(s), {no_decl} without a capabilities declaration, "
        f"{undeclared_any} using capabilities they did not declare, "
        f"{out_of_scope} declared 'none' but use capabilities"
    )
    if a.strict and undeclared_any:
        print("::error::strict mode: undeclared capability use is treated as failure")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
