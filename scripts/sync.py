#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync.py — 本地 → 远端单向同步（唯一推送入口）

设计原则：
  1. 本地目录是唯一真源（single source of truth），远端是它的镜像。
  2. 所有推送都必须走本脚本，不许再手工 git push、更不许用 GitHub API 单文件写。
  3. 推送前强制检查"远端有没有我不知道的提交"，有则先合并，绝不强推覆盖。

用法：
    python scripts/sync.py                          # 默认 origin（与历史行为一致）
    python scripts/sync.py --remote gitee           # 只推 gitee
    python scripts/sync.py --remote gitee,atomgit   # 推多个远端
    python scripts/sync.py --remote all             # 所有已配置远端（origin 优先）
    python scripts/sync.py --dry-run                # 只看会做什么，不实际提交/推送
    python scripts/sync.py -m "提交说明"             # 自定义提交说明

  --remote 省略时 = origin（向后兼容）。提交（第 1 步）只做一次，推送按远端逐个执行。

退出码：0 = 成功；1 = 任一远端失败（含冲突需人工处理）
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


def parse_remotes(argv):
    """解析 --remote a,b 或 --remote=a,b（可多次）；缺省 = ['origin']。"""
    out = []
    for i, a in enumerate(argv):
        if a == '--remote' and i + 1 < len(argv):
            out += [x.strip() for x in argv[i + 1].split(',') if x.strip()]
        elif a.startswith('--remote='):
            out += [x.strip() for x in a.split('=', 1)[1].split(',') if x.strip()]
    if not out:
        return ['origin']
    if out == ['all']:
        names = run(['git', 'remote']).stdout.split()
        if not names:
            return []
        return ['origin'] + [n for n in names if n != 'origin'] if 'origin' in names else names
    return out


def main():
    dry = '--dry-run' in sys.argv
    msg = None
    if '-m' in sys.argv:
        i = sys.argv.index('-m')
        if i + 1 < len(sys.argv):
            msg = sys.argv[i + 1]
    if not msg:
        msg = f'sync: {datetime.now().strftime("%Y-%m-%d %H:%M")}'

    remotes = parse_remotes(sys.argv[:])

    print('=' * 64)
    print('  本地 → 远端单向同步' + ('（演练模式）' if dry else ''))
    print(f'  目标远端: {", ".join(remotes) if remotes else "(无)"}')
    print('=' * 64)

    if not remotes:
        print('\n❌ 未解析到任何远端。用 --remote <name> 指定。')
        return 1

    # ---- 0. 前置：所有目标 remote 必须已配置 ----
    for rm in remotes:
        if not run(['git', 'remote', 'get-url', rm], check=False).stdout.strip():
            print(f'\n❌ 未配置 remote {rm}。先执行：')
            print(f'   git remote add {rm} <url>')
            return 1

    # ---- 1. 纳入所有变更（含 untracked）—— 只做一次，多远端共享同一 commit ----
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

    rc = 0
    for rm in remotes:
        print(f'\n{"-"*64}\n  ▶ 远端: {rm}\n{"-"*64}')

        # ---- 2. 检查远端是否有新提交（防漂移的关键） ----
        print(f'[2] 检查远端状态（{rm}）')
        run(['git', 'fetch', rm, f'+refs/heads/main:refs/remotes/{rm}/main'], check=False)
        behind = run(['git', 'rev-list', '--count', f'HEAD..{rm}/main'], check=False).stdout.strip()
        if behind and behind != '0':
            print(f'  ⚠️  远端有 {behind} 个本地没有的提交（可能来自网页编辑或 API 写入）')
            if dry:
                print(f'  （演练）将执行: git merge {rm}/main')
            else:
                r = run(['git', 'merge', f'{rm}/main', '--no-rebase',
                         '-m', f'merge: 合并 {rm} 远端提交'])
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
        print(f'[3] 推送（{rm}）')
        if dry:
            print(f'  （演练）将执行: git push {rm} main')
            continue

        r = run(['git', 'push', rm, 'main'])
        if r.returncode != 0:
            print('  ❌ 推送失败。若是认证问题，检查：')
            print('     git config --global --get-all credential.helper')
            print('     （应答内容应为指向 git-credential-ucvault.py 的唯一一项）')
            rc = 1
            continue
        print('  ✅ 推送成功')

        # ---- 4. 收尾校验 ----
        print(f'[4] 收尾校验（{rm}）')
        run(['git', 'fetch', rm, f'+refs/heads/main:refs/remotes/{rm}/main'], check=False)
        diff = run(['git', 'diff', '--stat', 'HEAD', f'{rm}/main'], check=False).stdout.strip()
        if diff:
            print('  ⚠️  推送后仍有差异，请重跑 scripts/drift-check.py')
            rc = 1
            continue
        print(f'  ✅ 本地与 {rm} 已完全一致')

    print('\n' + '=' * 64)
    print('  同步完成' if rc == 0 else '  同步存在失败项，见上')
    print('=' * 64)
    return rc


if __name__ == '__main__':
    sys.exit(main())
