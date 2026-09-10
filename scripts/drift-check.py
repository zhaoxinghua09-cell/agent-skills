#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drift-check.py — 本地 ↔ GitHub 远端一致性体检（只读，不改任何东西）

为什么存在：此前"本地目录"和"GitHub 远端"是两套互不知情的账本，
靠人工比对，反复出问题。本脚本把"是否一致"变成一条命令。

用法：
    python scripts/drift-check.py            # 体检当前仓库
    python scripts/drift-check.py --fix-hint # 附修复建议

输出分四段：
  [1] git 血缘    —— 是否有 remote、能否解析 origin/main
  [2] 工作区状态  —— 未提交 / 未跟踪文件
  [3] 内容差异    —— 本地 vs origin/main 的文件差异
  [4] 结论        —— 一致 / 不一致（附下一步）

退出码：0 = 完全一致；1 = 有漂移；2 = 环境不可用（如无 remote）
"""
import subprocess
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(args, check=False):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       encoding='utf-8', errors='ignore')
    if check and r.returncode != 0:
        return None
    return r


def main():
    fix_hint = '--fix-hint' in sys.argv
    print('=' * 64)
    print('  本地 ↔ GitHub 远端一致性体检')
    print(f'  仓库: {REPO}')
    print('=' * 64)

    drift = False

    # ---- [1] git 血缘 ----
    print('\n[1] git 血缘')
    remotes = run(['git', 'remote', '-v']).stdout.strip()
    if not remotes:
        print('  ❌ 未配置任何 remote —— 本地成为孤立仓库，无法与远端对账')
        print('     修复: git remote add origin https://github.com/<OWNER>/<REPO>.git')
        return 2
    origin = [l for l in remotes.split('\n') if l.startswith('origin')]
    print(f'  ✅ origin 已配置: {origin[0].split()[1] if origin else "(无)"}')

    # origin/main 是否可解析
    rb = run(['git', 'rev-parse', '--verify', 'origin/main'])
    if rb.returncode != 0:
        print('  ⚠️  origin/main 未建立（从未成功 fetch）')
        print('     修复: git fetch origin "+refs/heads/main:refs/remotes/origin/main"')
        return 2
    remote_sha = rb.stdout.strip()
    local_sha = run(['git', 'rev-parse', 'HEAD']).stdout.strip()
    print(f'  本地 HEAD   : {local_sha[:12]}')
    print(f'  origin/main : {remote_sha[:12]}')

    # 共同祖先
    mb = run(['git', 'merge-base', 'HEAD', 'origin/main'])
    if mb.returncode != 0:
        print('  ❌ 本地与远端无共同祖先（unrelated histories）—— 两套账本的根源')
        print('     修复: git merge origin/main --allow-unrelated-histories')
        drift = True
    else:
        print(f'  共同祖先    : {mb.stdout.strip()[:12]} ✅')

    # ---- [2] 工作区状态 ----
    print('\n[2] 工作区状态')
    tracked_dirty = run(['git', 'status', '--porcelain', '--untracked-files=no']).stdout.strip()
    untracked = run(['git', 'status', '--porcelain', '--untracked-files=all']).stdout
    untracked = [l for l in untracked.split('\n') if l.startswith('??')]
    if tracked_dirty:
        lines = tracked_dirty.split('\n')
        print(f'  ⚠️  已跟踪文件有 {len(lines)} 处未提交改动')
        for l in lines[:5]:
            print(f'      {l}')
        if len(lines) > 5:
            print(f'      ... 另有 {len(lines)-5} 处')
        drift = True
    else:
        print('  ✅ 已跟踪文件无未提交改动')

    if untracked:
        print(f'  ⚠️  有 {len(untracked)} 个未跟踪条目（不会随 push 上远端）')
        for l in untracked[:8]:
            print(f'      {l[3:]}')
        if len(untracked) > 8:
            print(f'      ... 另有 {len(untracked)-8} 个')
        print('     修复: git add -A && git commit -m "chore: track previously untracked"')
        drift = True
    else:
        print('  ✅ 无未跟踪条目')

    # ---- [3] 内容差异 ----
    print('\n[3] 本地 vs origin/main 内容差异')
    # 先 fetch 静默（失败不致命）
    run(['git', 'fetch', 'origin', '+refs/heads/main:refs/remotes/origin/main'])
    diff = run(['git', 'diff', '--stat', 'HEAD', 'origin/main'])
    if diff.stdout.strip():
        print('  ⚠️  两侧内容不一致：')
        for l in diff.stdout.strip().split('\n')[:12]:
            print(f'      {l}')
        drift = True
    else:
        print('  ✅ 内容完全一致')

    # ahead / behind
    counts = run(['git', 'rev-list', '--left-right', '--count', 'HEAD...origin/main']).stdout.strip()
    if counts:
        ahead, behind = counts.split()
        print(f'  提交差: 本地领先 {ahead} / 落后 {behind}')
        if ahead != '0' or behind != '0':
            drift = True

    # ---- [4] 结论 ----
    print('\n' + '=' * 64)
    if drift:
        print('  结论: ❌ 存在漂移，本地与远端不是同一状态')
        if fix_hint:
            print('\n  下一步（按顺序）:')
            print('    1. git add -A && git commit -m "chore: 纳入全部本地变更"')
            print('    2. git fetch origin && git merge origin/main   # 或 git pull --rebase')
            print('    3. 解决冲突（如有），git push origin main')
            print('    4. 重跑本脚本，直到输出全 ✅')
        return 1
    print('  结论: ✅ 完全一致 —— 本地与远端同步，无漂移')
    print('=' * 64)
    return 0


if __name__ == '__main__':
    sys.exit(main())
