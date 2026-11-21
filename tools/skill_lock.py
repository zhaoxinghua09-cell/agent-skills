#!/usr/bin/env python3
"""skill_lock.py — 技能树的完整性锁（对标策展注册表的 checksum + lockfile 模型）。

为什么需要：任何"技能目录 + 提示词"被加载进智能体，就等于把一段可执行意图
送进上下文。没有完整性锁时，上游改一个字节、加一个文件、删一个文件，下游
完全无感。策展注册表（Skills.sh 一类）用"静态分析 + 校验和 + 版本锁定"解决这个，
本工具把同一层能力落到仓库内、不依赖任何外部服务。

设计要点：
  1. 只读、可复算：锁文件是纯文本 JSON，任何人在任何机器上重算应当一致。
  2. 双向可证伪：`--selftest` 会自己改坏一个字节，verify 必须失败；
     只做"必须通过"的锁等于没有锁。
  3. 拒绝静默漂移：多出的技能、消失的技能、改动的字节，三种都报。

用法：
    python tools/skill_lock.py generate --root .
    python tools/skill_lock.py verify   --root .
    python tools/skill_lock.py selftest --root .
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

LOCK_NAME = "skills.lock.json"
ANCHOR_NAME = "skills.lock.anchor.json"
LEDGER_NAME = "skills.lock.log.jsonl"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "tests", "fixtures", "testdata"}
# 锁自身的产物必须排除，否则"仓库根目录本身就是一个技能"的仓会自我递归漂移
SKIP_FILES = {"skills.lock.json", "skills.lock.sig", "skills.lock.pub", "skills.lock.policy.json", "skills.lock.anchor.json", "skills.lock.log.jsonl"}
TEXT_LIMIT = 1_000_000  # 单文件 >1MB 按二进制处理，避免读爆内存


def _write_lf(p: Path, text: str) -> None:
    """一律写 LF 字节。

    坑（2026-11-22 真踩）：Windows 上 Path.write_text 会把 \\n 转成 \\r\\n，
    而 git blob 在 CI/Linux 侧是 LF，于是签名（对锁文件字节签名）在本地有效、
    在 CI 里永远 ``signature invalid``。锁产物必须字节稳定，不能依赖平台换行。
    """
    p.write_bytes(text.encode("utf-8"))


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _skill_dirs(root: Path) -> list[Path]:
    """任何含 SKILL.md 的目录都算一个技能，跳过明显的非技能目录。"""
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        # 仓库根目录本身不算技能：否则 CI/基建文件会被算进摘要，造成跨环境假红
        if "SKILL.md" in filenames and Path(dirpath) != root:
            found.append(Path(dirpath))
    # 只按 POSIX 相对路径字符串排序，避免 Windows 的大小写不敏感排序造成跨平台摘要不一致
    return sorted(found, key=lambda d: (d.relative_to(root).as_posix() or "."))


def _tree_digest(skill_dir: Path) -> tuple[str, int]:
    """目录摘要 = sha256( 排序后的 "相对路径\\0文件sha256" 逐行拼接 )。"""
    files: list[tuple[str, str]] = []
    for p in skill_dir.rglob("*"):
        if not p.is_file():
            continue
        parts = set(p.relative_to(skill_dir).parts)
        if parts & SKIP_DIRS or p.name in SKIP_FILES:
            continue
        rel = p.relative_to(skill_dir).as_posix()
        files.append((rel, _sha256_file(p)))
    # 关键：按 POSIX 字符串排序（字节序），Windows 的 case-insensitive 排序会让摘要跨平台不一致
    files.sort(key=lambda item: item[0])
    h = hashlib.sha256()
    for rel, digest in files:
        h.update(f"{rel}\0{digest}\n".encode())
    return h.hexdigest(), len(files)


def _front_matter(skill_md: Path) -> tuple[str, str]:
    name, desc = "", ""
    try:
        lines = skill_md.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except Exception:
        return name, desc
    if not lines or lines[0].strip() != "---":
        return name, desc
    for line in lines[1:]:
        if line.strip() == "---":
            break
        low = line.strip()
        if low.lower().startswith("name:"):
            name = low.split(":", 1)[1].strip().strip('"\'')
        elif low.lower().startswith("description:"):
            desc = low.split(":", 1)[1].strip().strip('"\'')
    return name, desc


def build_lock(root: Path, previous: dict | None = None) -> dict:
    entries = []
    for d in _skill_dirs(root):
        rel = d.relative_to(root).as_posix() or "."
        digest, count = _tree_digest(d)
        fm_name, fm_desc = _front_matter(d / "SKILL.md")
        entries.append(
            {
                "path": rel,
                "declared_name": fm_name,
                "has_description": bool(fm_desc),
                "file_count": count,
                "digest": digest,
            }
        )
    h = hashlib.sha256()
    for e in entries:
        h.update(f"{e['path']}\0{e['digest']}\n".encode())
    root_digest = h.hexdigest()

    # 回滚保护：sequence 单调递增，history 只能追加，等于一本防篡改的账本
    prev_seq = 0
    prev_history: list = []
    attest: list = []
    if isinstance(previous, dict):
        prev_seq = int(previous.get("sequence") or 0)
        prev_history = list(previous.get("history") or [])
        attest = list(previous.get("validated_against") or [])
    seq = prev_seq + 1
    history = prev_history + [{"sequence": seq, "root_digest": root_digest}]

    return {
        "schema_version": 2,
        "algorithm": "sha256(sorted relpath + NUL + file sha256, per line)",
        "root_digest": root_digest,
        "skill_count": len(entries),
        "sequence": seq,
        "history": history,
        "validated_against": attest,
        "skills": entries,
    }


def diff_lock(root: Path, lock: dict) -> list[str]:
    problems: list[str] = []
    recorded = {e["path"]: e for e in lock.get("skills", [])}
    actual = {d.relative_to(root).as_posix() or ".": d for d in _skill_dirs(root)}

    for path, entry in sorted(recorded.items()):
        d = actual.get(path)
        if d is None:
            problems.append(f"{path}: recorded in {LOCK_NAME} but missing on disk (skill removed)")
            continue
        digest, count = _tree_digest(d)
        if digest != entry["digest"]:
            problems.append(
                f"{path}: digest drift (locked {entry['digest'][:12]}, actual {digest[:12]}); "
                f"files {entry['file_count']} -> {count}"
            )
        if entry["declared_name"] and entry["declared_name"] != path.split("/")[-1] and path != ".":
            print(
                f"::warning::{path}: SKILL.md name '{entry['declared_name']}' "
                f"does not match directory name (lint only, not an integrity failure)"
            )
    for path in sorted(actual):
        if path not in recorded:
            problems.append(f"{path}: skill present on disk but absent from {LOCK_NAME}")

    # 根摘要：把"整体一致"也做成一个可比较的量
    if not problems:
        rebuilt = build_lock(root)
        if rebuilt["root_digest"] != lock.get("root_digest"):
            problems.append(
                f"root_digest mismatch (locked {str(lock.get('root_digest'))[:12]}, "
                f"rebuilt {rebuilt['root_digest'][:12]})"
            )

    problems.extend(_chain_problems(root, lock))
    problems.extend(_attestation_problems(lock))
    return problems


def _chain_problems(root: Path, lock: dict) -> list[str]:
    """回滚保护：sequence/history 必须自洽，且不得落后于锚点。

    行业前沿（ContextLock 的 rollback v7 >= v7）要防的是"把锁换回旧版本"这种攻击：
    旧锁本身完全自洽，校验和也对，只是它描述的是过去的状态。
    """
    problems: list[str] = []
    seq = lock.get("sequence")
    history = lock.get("history")
    if not isinstance(seq, int) or seq < 1:
        problems.append("sequence missing or invalid: rollback protection cannot be evaluated")
        return problems
    if not isinstance(history, list) or len(history) != seq:
        problems.append(
            f"history incomplete: sequence={seq} but history has "
            f"{len(history) if isinstance(history, list) else 'no'} entry(ies)"
        )
        return problems
    for i, item in enumerate(history, start=1):
        if not isinstance(item, dict) or item.get("sequence") != i or not item.get("root_digest"):
            problems.append(f"history[{i}]: malformed entry (expected sequence={i} with root_digest)")
            break
    if history[-1].get("root_digest") != lock.get("root_digest"):
        problems.append("history tail does not match root_digest (history was edited by hand)")

    anchor_path = root / ANCHOR_NAME
    if anchor_path.exists():
        try:
            anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{ANCHOR_NAME}: unreadable ({exc})")
            return problems
        a_seq = int(anchor.get("sequence") or 0)
        a_digest = anchor.get("root_digest")
        if a_seq < 1 or not a_digest:
            problems.append(f"{ANCHOR_NAME}: missing sequence/root_digest")
        elif seq < a_seq:
            problems.append(
                f"lock rolled back: anchor sequence {a_seq} > lock sequence {seq} "
                f"(an older lock was restored)"
            )
        elif history[a_seq - 1].get("root_digest") != a_digest:
            problems.append(
                f"anchor mismatch at sequence {a_seq}: anchor {str(a_digest)[:12]} != "
                f"history {str(history[a_seq - 1].get('root_digest'))[:12]}"
            )
    return problems


def _attestation_problems(lock: dict) -> list[str]:
    """行为证明：字节没变不等于行为没变，必须显式声明"在什么 harness/model 上验过"。

    取自 skill-provenance 的 validated_against：与 integrity pin 分开记，
    只有 result=pass 才允许放行，partial/fail 一律视为未验证。
    """
    problems: list[str] = []
    entries = lock.get("validated_against") or []
    if not isinstance(entries, list):
        problems.append("validated_against must be a list")
        return problems
    required = ("bundle_version", "harness", "model", "date", "result")
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            problems.append(f"validated_against[{i}]: not an object")
            continue
        missing = [k for k in required if not e.get(k)]
        if missing:
            problems.append(f"validated_against[{i}]: missing {', '.join(missing)}")
            continue
        if str(e["result"]).lower() != "pass":
            problems.append(
                f"validated_against[{i}]: result={e['result']} means this bundle is not validated "
                f"(only 'pass' is accepted)"
            )
    return problems


def cmd_generate(root: Path, out: Path) -> int:
    previous = None
    if out.exists():
        try:
            previous = json.loads(out.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            previous = None
    lock = build_lock(root, previous)
    # 内容没变就不推进 sequence：账本只记录真实的变更点
    if isinstance(previous, dict) and previous.get("root_digest") == lock["root_digest"]:
        lock["sequence"] = previous.get("sequence", lock["sequence"])
        lock["history"] = previous.get("history", lock["history"])
    _write_lf(out, json.dumps(lock, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        f"wrote {out} : {lock['skill_count']} skills, root_digest={lock['root_digest'][:16]}, "
        f"sequence={lock['sequence']}"
    )
    return 0


def cmd_anchor(root: Path, lock_path: Path) -> int:
    """把当前锁的 (sequence, root_digest) 钉进锚点；之后回滚到旧锁会被 verify 拒绝。"""
    if not lock_path.exists():
        print(f"::error::missing {LOCK_NAME}; run generate first")
        return 1
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    anchor = {
        "schema_version": 1,
        "sequence": lock.get("sequence"),
        "root_digest": lock.get("root_digest"),
        "skill_count": lock.get("skill_count"),
    }
    path = root / ANCHOR_NAME
    _write_lf(path, json.dumps(anchor, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"wrote {path} : sequence={anchor['sequence']}, root_digest={str(anchor['root_digest'])[:16]}")
    return 0


def _git_meta(root: Path) -> dict:
    """取 HEAD 与 repo 名，用于把日志条目钉到具体提交上（取不到就留空，不阻塞）。"""
    meta = {"repo": "", "commit": ""}
    try:
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True
        ).stdout.strip()
        url = subprocess.run(
            ["git", "-C", str(root), "config", "--get", "remote.origin.url"],
            capture_output=True, text=True,
        ).stdout.strip()
        meta["commit"] = commit
        if url:
            meta["repo"] = url.rstrip("/").split("/")[-1].replace(".git", "")
            if ":" in url.split("/")[0] and not url.startswith("http"):
                owner = url.split(":")[-1].split("/")[0]
                meta["repo"] = f"{owner}/{meta['repo']}"
    except Exception:  # noqa: BLE001
        pass
    return meta


def _content_hash(lock: dict) -> str:
    payload = json.dumps(
        {"root_digest": lock.get("root_digest"), "skill_count": lock.get("skill_count")},
        sort_keys=True, ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _entry_chain(entry: dict) -> str:
    """对**整条条目**（除 chain 自身）做承诺。

    坑（2026-11-22 真踩）：第一版只承诺 content_hash|prev_chain|ts|repo，
    于是往条目里加一个字段（`"note":"x"`）仍能验过 —— 等于日志可被悄悄篡改。
    SCITT 的做法是对整条受保护字段做承诺，这里照做。
    """
    payload = {k: v for k, v in entry.items() if k != "chain"}
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _read_ledger(path: Path) -> list[dict]:
    out: list[dict] = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


def cmd_ledger(root: Path, lock_path: Path) -> int:
    """把当前锁追加进哈希链日志（skills.lock.log.jsonl）。幂等：内容没变就不追加。"""
    if not lock_path.exists():
        print(f"::error::missing {LOCK_NAME}; run generate first")
        return 1
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    path = root / LEDGER_NAME
    entries = _read_ledger(path)
    last = entries[-1] if entries else None
    if last and last.get("root_digest") == lock.get("root_digest") and last.get(
        "skill_count"
    ) == lock.get("skill_count"):
        print(f"ledger unchanged: seq={last.get('seq')} root_digest={str(lock.get('root_digest'))[:16]}")
        return 0
    meta = _git_meta(root)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = _content_hash(lock)
    prev_chain = str(last.get("chain")) if last else "0" * 64
    entry = {
        "seq": (int(last.get("seq", 0)) + 1) if last else 1,
        "ts": ts,
        "repo": meta["repo"],
        "commit": meta["commit"],
        "root_digest": lock.get("root_digest"),
        "skill_count": lock.get("skill_count"),
        "content_hash": content,
        "prev_chain": prev_chain,
    }
    entry["chain"] = _entry_chain(entry)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"ledger appended: seq={entry['seq']} chain={entry['chain'][:16]}")
    return 0


def _ledger_problems(root: Path, lock: dict) -> list[str]:
    """校验哈希链：链接连续性、逐条 chain 重算、序号连续性、是否覆盖当前锁、是否被截断。"""
    path = root / LEDGER_NAME
    if not path.exists():
        return []  # 未启用日志不阻塞，属于可选加固
    problems: list[str] = []
    try:
        entries = _read_ledger(path)
    except Exception as exc:  # noqa: BLE001
        return [f"{LEDGER_NAME}: unreadable ({exc})"]
    if not entries:
        return [f"{LEDGER_NAME}: empty"]
    prev_chain = "0" * 64
    for i, e in enumerate(entries):
        if e.get("seq") != i + 1:
            problems.append(f"ledger[{i}]: seq={e.get('seq')} breaks 1-based continuity")
        if str(e.get("prev_chain")) != prev_chain:
            problems.append(f"ledger[{i}]: prev_chain does not link to previous entry (truncated or rewritten)")
        recomputed = _entry_chain(e)
        if recomputed != str(e.get("chain")):
            problems.append(f"ledger[{i}]: chain hash mismatch (entry edited after being written)")
        prev_chain = str(e.get("chain"))
    last = entries[-1]
    if last.get("root_digest") != lock.get("root_digest") or last.get("skill_count") != lock.get(
        "skill_count"
    ):
        problems.append(
            "ledger does not cover the current lockfile (lock changed without appending a ledger entry)"
        )
    if int(last.get("seq", 0)) < int(lock.get("sequence", 1)):
        problems.append(
            f"ledger behind lockfile: ledger seq={last.get('seq')} but lock sequence={lock.get('sequence')} "
            f"(entries were truncated)"
        )
    anchor = root / ANCHOR_NAME
    if anchor.exists():
        try:
            seq = int(json.loads(anchor.read_text(encoding="utf-8")).get("sequence", 1))
            if int(last.get("seq", 0)) < seq:
                problems.append(f"ledger truncated relative to anchor: ledger seq={last.get('seq')} < anchor seq={seq}")
        except Exception:  # noqa: BLE001
            pass
    return problems


def cmd_verify(root: Path, lock_path: Path) -> int:
    if not lock_path.exists():
        print(f"::error file={lock_path}::missing {LOCK_NAME}; run `python tools/skill_lock.py generate`")
        return 1
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    problems = diff_lock(root, lock)
    problems.extend(_signature_problems(root, lock_path))
    problems.extend(_ledger_problems(root, lock))
    for p in problems:
        print(f"::error::{p}")
    if problems:
        print(f"SKILL LOCK FAIL: {len(problems)} problem(s)")
        return 1
    print(f"SKILL LOCK OK: {lock['skill_count']} skills match {lock_path.name}")
    return 0


def cmd_selftest(root: Path) -> int:
    """负控：改坏一个字节必须红，恢复后必须绿。"""
    if not (root / LOCK_NAME).exists():
        print("selftest skipped: no lockfile")
        return 0
    tmp = Path(tempfile.mkdtemp())
    failures = 0
    try:
        work = tmp / "tree"
        shutil.copytree(root, work, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
        lock = json.loads((work / LOCK_NAME).read_text(encoding="utf-8"))
        target = None
        for e in lock["skills"]:
            d = work / e["path"]
            for p in sorted(d.rglob("*")):
                if p.is_file():
                    target = p
                    break
            if target:
                break
        if target is None:
            print("selftest skipped: no files inside any skill")
            return 0

        orig = target.read_bytes()
        target.write_bytes(orig[:-1] + bytes([orig[-1] ^ 0x01]))
        rc1 = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
            capture_output=True, text=True
        ).returncode
        if rc1 == 0:
            print("::error::negative control failed: a mutated byte still verified clean")
            failures += 1
        else:
            print(f"negative control OK: mutated byte rejected (exit {rc1})")

        target.write_bytes(orig)
        rc2 = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
            capture_output=True, text=True
        ).returncode
        if rc2 != 0:
            print("::error::positive control failed: restored tree does not verify")
            failures += 1
        else:
            print("positive control OK: restored tree verifies")

        # 第三个负控：回滚保护。把锁换回旧版本（内容自洽、校验和也对），必须被拒。
        lock_path = work / LOCK_NAME
        cur_bytes = lock_path.read_bytes()
        cur = json.loads(cur_bytes.decode("utf-8"))
        _write_lf(
            work / ANCHOR_NAME,
            json.dumps(
                {
                    "schema_version": 1,
                    "sequence": cur["sequence"],
                    "root_digest": cur["root_digest"],
                    "skill_count": cur["skill_count"],
                },
                indent=2,
            ),
        )
        rolled = dict(cur)
        if cur["sequence"] > 1:
            rolled["sequence"] = cur["sequence"] - 1
            rolled["history"] = cur["history"][: cur["sequence"] - 1]
        else:
            rolled["sequence"] = 1
            rolled["history"] = [{"sequence": 1, "root_digest": "0" * 64}]
            rolled["root_digest"] = "0" * 64
        _write_lf(lock_path, json.dumps(rolled, indent=2, sort_keys=True))
        rc3 = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
            capture_output=True, text=True
        ).returncode
        if rc3 == 0:
            print("::error::rollback control failed: a rolled-back lockfile still verified clean")
            failures += 1
        else:
            print(f"rollback control OK: restored old lockfile rejected (exit {rc3})")

        # 第四个负控：签名。锁被改一个字节（即使内容仍自洽）必须被签名校验拒绝。
        if (work / PUB_FILE).exists() and _crypto():
            lock_path.write_bytes(cur_bytes + b"\n")
            rc4 = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
                capture_output=True, text=True
            )
            if rc4.returncode == 0:
                print("::error::signature control failed: an unsigned edit still verified clean")
                failures += 1
            else:
                print(f"signature control OK: post-signing edit rejected (exit {rc4.returncode})")
            lock_path.write_bytes(cur_bytes)

        # 第五个负控：哈希链日志被截断。前面的环仍然自洽，只删最后一环——必须被拒。
        ledger_path = work / LEDGER_NAME
        if ledger_path.exists():
            lines = ledger_path.read_text(encoding="utf-8").splitlines()
            if len(lines) > 1:
                _write_lf(ledger_path, "\n".join(lines[:-1]) + "\n")
                rc5 = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
                    capture_output=True, text=True
                ).returncode
                if rc5 == 0:
                    print("::error::ledger control failed: a truncated transparency log still verified clean")
                    failures += 1
                else:
                    print(f"ledger control OK: truncated log rejected (exit {rc5})")
                _write_lf(ledger_path, "\n".join(lines) + "\n")
            else:
                # 只有一环时，把整条日志清空：链必须因此判红（不能出现"空日志也算通过"）
                ledger_path.write_bytes(b"")
                rc5 = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()), "verify", "--root", str(work)],
                    capture_output=True, text=True
                ).returncode
                if rc5 == 0:
                    print("::error::ledger control failed: an emptied transparency log still verified clean")
                    failures += 1
                else:
                    print(f"ledger control OK: emptied log rejected (exit {rc5})")
                _write_lf(ledger_path, "\n".join(lines) + "\n")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["generate", "verify", "selftest", "anchor", "keygen", "sign", "ledger"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--key", default=None)
    a = ap.parse_args()
    root = Path(a.root).resolve()
    lock_path = Path(a.out).resolve() if a.out else root / LOCK_NAME
    key_path = Path(a.key).resolve() if a.key else Path(
        os.environ.get("SKILLLOCK_KEY") or (Path.home() / ".lgd" / "skilllock_key.json")
    ).resolve()
    if a.command == "generate":
        return cmd_generate(root, lock_path)
    if a.command == "verify":
        return cmd_verify(root, lock_path)
    if a.command == "anchor":
        return cmd_anchor(root, lock_path)
    if a.command == "keygen":
        return cmd_keygen(key_path)
    if a.command == "sign":
        return cmd_sign(root, lock_path, key_path)
    if a.command == "ledger":
        return cmd_ledger(root, lock_path)
    return cmd_selftest(root)




# ---------- 签名与身份策略（Ed25519）----------
PUB_FILE = "skills.lock.pub"
SIG_FILE = "skills.lock.sig"
POLICY_NAME = "skills.lock.policy.json"


def _crypto():
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey, Ed25519PublicKey,
        )
        from cryptography.hazmat.primitives import serialization
        return Ed25519PrivateKey, Ed25519PublicKey, serialization
    except Exception as exc:  # noqa: BLE001
        print(f"::error::signature support unavailable ({exc}); pip install cryptography")
        return None


def cmd_keygen(key_path: Path) -> int:
    c = _crypto()
    if not c:
        return 1
    Ed25519PrivateKey, _, serialization = c
    key = Ed25519PrivateKey.generate()
    priv = key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()
    pub = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    ).hex()
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps({"algorithm": "ed25519", "private_hex": priv, "public_hex": pub}, indent=2), encoding="utf-8")
    print(f"private key written to {key_path} (NEVER commit this file)")
    print(f"public key (commit as {PUB_FILE}): {pub}")
    return 0


def _sign_bytes(payload: bytes, key_path: Path) -> str:
    c = _crypto()
    if not c:
        return ""
    Ed25519PrivateKey, _, _ = c
    data = json.loads(key_path.read_text(encoding="utf-8"))
    key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(data["private_hex"]))
    return key.sign(payload).hex()


def _verify_bytes(payload: bytes, sig_hex: str, pub_hex: str) -> bool:
    c = _crypto()
    if not c:
        return False
    _, Ed25519PublicKey, _ = c
    from cryptography.exceptions import InvalidSignature
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(
            bytes.fromhex(sig_hex), payload
        )
        return True
    except (InvalidSignature, ValueError):
        return False


def cmd_sign(root: Path, lock_path: Path, key_path: Path) -> int:
    if not lock_path.exists():
        print(f"::error::missing {LOCK_NAME}")
        return 1
    if not key_path.exists():
        print(f"::error::signing key not found at {key_path} (run keygen and keep it outside the repo)")
        return 1
    pub_hex = json.loads(key_path.read_text(encoding="utf-8"))["public_hex"]
    sig = _sign_bytes(lock_path.read_bytes(), key_path)
    if not sig:
        return 1
    _write_lf(root / SIG_FILE, sig + "\n")
    _write_lf(root / PUB_FILE, pub_hex + "\n")
    print(f"signed {lock_path.name} -> {SIG_FILE} (pub {pub_hex[:16]}…)")
    return 0


def _signature_problems(root: Path, lock_path: Path) -> list[str]:
    problems: list[str] = []
    pub_path = root / PUB_FILE
    sig_path = root / SIG_FILE
    if not pub_path.exists() and not sig_path.exists():
        return problems  # 未启用签名不阻塞（政策在 policy 文件里显式声明）
    if not pub_path.exists():
        problems.append(f"{SIG_FILE} present but {PUB_FILE} missing")
        return problems
    if not sig_path.exists():
        problems.append(f"{PUB_FILE} present but {SIG_FILE} missing (lock is unsigned)")
        return problems
    pub_hex = pub_path.read_text(encoding="utf-8").strip()
    sig_hex = sig_path.read_text(encoding="utf-8").strip()
    policy_path = root / POLICY_NAME
    if policy_path.exists():
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{POLICY_NAME}: unreadable ({exc})")
            policy = {}
        allowed = [str(x).strip() for x in (policy.get("allowed_signers") or [])]
        if allowed and pub_hex not in allowed:
            problems.append("signer not authorized by policy (public key is not an allowed signer)")
        prefixes = [str(x) for x in (policy.get("path_prefixes") or [])]
        if prefixes:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            for e in lock.get("skills", []):
                if not any(e["path"].startswith(p) for p in prefixes):
                    problems.append(f"{e['path']}: outside the signer's authorized path_prefixes")
    if not _verify_bytes(lock_path.read_bytes(), sig_hex, pub_hex):
        problems.append(f"signature invalid: {SIG_FILE} does not match {lock_path.name} (lock edited after signing)")
    return problems


if __name__ == "__main__":
    sys.exit(main())
