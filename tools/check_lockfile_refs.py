"""actions.lock 与工作流 uses: 的一致性校验器（v2）。

为什么需要它：GitHub 要求 actions.lock 里登记工作流实际引用的每一个 action ref。
只要工作流写浮动 major（如 actions/checkout@v7）而 lockfile 里是
actions/checkout@v7.0.1，整仓**所有**工作流都会 startup_failure，而且 git push
不报错 —— 静默瘫痪，只能靠 workflow_dispatch 才能逼出报错。

v2 修正两处平台侧归一化规则（否则会误报）：
1. 子路径 action 归一化到仓库级：github/codeql-action/init@v4.39.4 -> github/codeql-action@v4.39.4
2. 复用的 reusable workflow（uses 指向 .github/workflows/*.yml）不计入 actions.lock

用法：python check_lockfile_refs.py <repo_dir>
退出码：0 一致 / 1 有不一致 / 2 无 lockfile
"""
import re
import sys
import glob
from pathlib import Path


def load_lock(p: Path):
    """极简 YAML 子集解析：只取 workflows / dependencies 两块。"""
    data = {"workflows": {}, "dependencies": set()}
    cur = None
    last_wf = None
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0 and s.endswith(":"):
            cur = s[:-1]
            continue
        if indent == 4 and s.startswith("'"):
            key = s.split(":", 1)[0].strip().strip("'")
            rest = s.split(":", 1)[1].strip()
            if cur == "workflows":
                data["workflows"][key] = [] if rest == "[]" else None
                last_wf = key
            elif cur == "dependencies":
                data["dependencies"].add(key)
            continue
        if indent == 8 and cur == "workflows" and s.startswith("- ") and last_wf:
            data["workflows"][last_wf] = (data["workflows"][last_wf] or []) + [
                s[2:].strip().strip("'")
            ]
    return data


def refs_of(path: Path):
    out = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.search(r"uses:\s*['\"]?([^#\s'\"]+)", line)
        if m:
            out.append(m.group(1))
    return out


def normalize(ref: str):
    """返回归一化后的 ref；None 表示不计入 actions.lock。"""
    if ref.startswith("./"):
        return None
    if "/.github/workflows/" in ref:
        return None
    if "@" not in ref:
        return None
    left, right = ref.split("@", 1)
    parts = left.split("/")
    if len(parts) > 2:
        left = "/".join(parts[:2])
    return f"{left}@{right}"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    lock_path = root / ".github" / "workflows" / "actions.lock"
    if not lock_path.exists():
        print("NO_LOCK: 该仓没有 actions.lock，不需要一致性校验")
        return 2

    lock = load_lock(lock_path)
    deps = lock["dependencies"]
    wf_map = {k.replace("\\", "/"): v for k, v in lock["workflows"].items()}
    bad = 0

    for f in sorted(glob.glob(str(root / ".github/workflows/*.y*ml"))):
        p = Path(f)
        rel = str(p.relative_to(root)).replace("\\", "/")
        raw_refs = refs_of(p)
        if not raw_refs:
            continue  # 零 action 工作流只需登记 []
        refs = [r for r in (normalize(x) for x in raw_refs) if r]
        listed = wf_map.get(rel)
        if listed is None:
            bad += 1
            print(f"WARN {rel}: lockfile 无此 workflow 条目（应登记 [] 或列引用）")
            continue
        listed_norm = {normalize(x) or x for x in listed}
        missing_dep = sorted({r for r in refs if r not in deps})
        not_listed = sorted({r for r in refs if r not in listed_norm})
        if missing_dep or not_listed:
            bad += 1
            print(f"BAD  {rel}")
            if missing_dep:
                print("     依赖表缺:", ", ".join(missing_dep))
            if not_listed:
                print("     工作流清单缺:", ", ".join(not_listed))

    print("RESULT:", "OK 一致" if bad == 0 else f"{bad} 个 workflow 不一致（会导致 startup_failure）")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
