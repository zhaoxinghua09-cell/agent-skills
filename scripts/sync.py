#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync.py — 本地 → GitHub 单向同步（唯一推送入口）

设计原则：
  1. 本地目录是唯一真源（single source of truth），远端是它的镜像。
  2. 所有推送都必须走本脚本，不许再手工 git push、更不许用 GitHub API 单文件写。
  3. 推送前强制检查"远端有没有我不知道的提交"，有则先合并，绝不强推覆盖。

用法：
    python scripts/sync.py                 # 全自动：add -> commit -> 合并远端 -> push
    python scripts/sync.py --dry-run       # 只看会做什么，不实际提交/推送
    python scripts/sync.py -m "提交说明"    # 自定义提交说明

退出码：0 = 成功；1 = 失败（含冲突需人工处理）
"""
import subprocess
import sys
import os
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(args, check=True, capture=True):
    r = subprocess.run(args, cwd=REPO, capture_output=capture, text=True,
                       encoding='utf-8', errors='ignore')
    if check and r.returncode != 0:
        print(f'  ❌ 命令失败: {" ".join(args)}')
        if r.stderr:
            print(f'     {r.stderr.strip()[:300]}')
    return r


def main():
    dry = '--dry-run' in sys.argv
    msg = None
    if '-m' in sys.argv:
        i = sys.argv.index('-m')
        if i + 1 < len(sys.argv):
            msg = sys.argv[i + 1]
    if not msg:
        msg = f'sync: {datetime.now().strftime("%Y-%m-%d %H:%M")}'

    print('=' * 64)
    print('  本地 → GitHub 单向同步' + ('（演练模式）' if dry else ''))
    print('=' * 64)

    # ---- 0. 前置：remote 是否存在 ----
    if not run(['git', 'remote', 'get-url', 'origin'], check=False).stdout.strip():
        print('\n❌ 未配置 remote origin。先执行：')
        print('   git remote add origin https://github.com/<OWNER>/<REPO>.git')
        return 1

    # ---- 1. 纳入所有变更（含 untracked） ----
    print('\n[1] 纳入本地变更')
    run(['git', 'add', '-A'])
    staged = run(['git', 'diff', '--cached', '--name-only']).stdout.strip()
    if staged:
        n = len(staged.split('\n'))
        print(f'  待提交 {n} 个文件')
        for l in staged.split('\n')[:8]:
            print(f'    + {l}')
        if n > 8:
            print(f'    ... 另有 {n-8} 个')
        if dry:
            print(f'  （演练）将提交: {msg}')
        else:
            r = run(['git', 'commit', '-m', msg])
            if r.returncode == 0:
                print(f'  ✅ 已提交: {msg}')
            else:
                print('  ❌ 提交失败')
                return 1
    else:
        print('  ✅ 无待提交变更')

    # ---- 2. 检查远端是否有新提交（防漂移的关键） ----
    print('\n[2] 检查远端状态')
    run(['git', 'fetch', 'origin', '+refs/heads/main:refs/remotes/origin/main'], check=False)
    behind = run(['git', 'rev-list', '--count', 'HEAD..origin/main']).stdout.strip()
    if behind and behind != '0':
        print(f'  ⚠️  远端有 {behind} 个本地没有的提交（可能来自 GitHub 网页编辑或 API 写入）')
        if dry:
            print('  （演练）将执行: git merge origin/main')
        else:
            r = run(['git', 'merge', 'origin/main', '--no-rebase', '-m', 'merge: 合并远端提交'])
            if r.returncode != 0:
                print('  ❌ 合并冲突，需人工处理。冲突文件：')
                cf = run(['git', 'diff', '--name-only', '--diff-filter=U']).stdout.strip()
                for l in cf.split('\n'):
                    if l:
                        print(f'     ! {l}')
                print('  处理完成后执行: git add <file> && git commit && python scripts/sync.py')
                return 1
            print('  ✅ 已合并远端提交')
    else:
        print('  ✅ 远端无新提交')

    # ---- 3. 推送 ----
    print('\n[3] 推送')
    if dry:
        print('  （演练）将执行: git push origin main')
        print('\n' + '=' * 64)
        print('  演练结束，未做任何实际改动')
        return 0

    r = run(['git', 'push', 'origin', 'main'])
    if r.returncode != 0:
        print('  ❌ 推送失败。若是认证问题，检查：')
        print('     git config --global --get-all credential.helper')
        print('     （应答内容应为指向 git-credential-ucvault.py 的唯一一项）')
        return 1
    print('  ✅ 推送成功')

    # ---- 4. 收尾校验 ----
    print('\n[4] 收尾校验')
    run(['git', 'fetch', 'origin', '+refs/heads/main:refs/remotes/origin/main'], check=False)
    diff = run(['git', 'diff', '--stat', 'HEAD', 'origin/main']).stdout.strip()
    if diff:
        print('  ⚠️  推送后仍有差异，请重跑 scripts/drift-check.py')
        return 1
    print('  ✅ 本地与远端已完全一致')

    print('\n' + '=' * 64)
    print('  同步完成')
    print('=' * 64)
    return 0


if __name__ == '__main__':
    sys.exit(main())
