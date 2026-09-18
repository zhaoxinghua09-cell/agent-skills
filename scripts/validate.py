#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate.py — 仓库结构校验（提交前跑，防"半成品"进仓）

规则：
  R1  每个 skills/<name>/ 目录必须含 SKILL.md
  R2  SKILL.md 必须有 YAML frontmatter（--- 包裹）
  R3  frontmatter 必须含 name 与 description
  R4  frontmatter 的 name 必须与目录名一致
  R5  仓库根目录必须含 LICENSE
  R6  仓库根目录必须含 README.md
  R7  不得出现明文密钥（ghp_ / sk- / AKID 等模式）进入仓库

用法：
    python scripts/validate.py           # 全量校验
    python scripts/validate.py --quick   # 只查 R1/R5/R6

退出码：0 = 全过；1 = 有违规
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(REPO, 'skills')

SECRET_PATTERNS = [
    (r'ghp_[A-Za-z0-9]{30,}', 'GitHub PAT'),
    (r'github_pat_[A-Za-z0-9_]{30,}', 'GitHub fine-grained PAT'),
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI-style key'),
    (r'AKID[A-Za-z0-9]{10,}', 'Tencent SecretId'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'private key'),
]

# 占位符豁免：形如 AKIDxxxx / AKID**** / sk-xxxx 的掩码串不是真密钥
PLACEHOLDER_RE = [
    r'^AKID[xX*]+$',
    r'^AKIDx{6,}$',
    r'^sk-[xX*]+$',
    r'^ghp_[xX*]+$',
]


def is_placeholder(token):
    for p in PLACEHOLDER_RE:
        if re.match(p, token):
            return True
    return False

violations = []


def add(rule, msg):
    violations.append((rule, msg))


def check_frontmatter(p):
    txt = open(p, encoding='utf-8', errors='ignore').read()
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line and not line.strip().startswith('#'):
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def main():
    quick = '--quick' in sys.argv

    # R5 / R6 根文件
    if not os.path.isfile(os.path.join(REPO, 'LICENSE')):
        add('R5', '根目录缺 LICENSE')
    if not os.path.isfile(os.path.join(REPO, 'README.md')):
        add('R6', '根目录缺 README.md')

    if not os.path.isdir(SKILLS):
        add('R1', 'skills/ 目录不存在')
    else:
        dirs = sorted(d for d in os.listdir(SKILLS)
                      if os.path.isdir(os.path.join(SKILLS, d)))
        print(f'校验 {len(dirs)} 个技能目录...')
        for d in dirs:
            sp = os.path.join(SKILLS, d, 'SKILL.md')
            if not os.path.isfile(sp):
                add('R1', f'{d}: 缺 SKILL.md')
                continue
            if quick:
                continue
            fm = check_frontmatter(sp)
            if fm is None:
                add('R2', f'{d}: SKILL.md 无 YAML frontmatter')
                continue
            if not fm.get('name'):
                add('R3', f'{d}: frontmatter 缺 name')
            elif fm['name'] != d:
                add('R4', f'{d}: frontmatter name="{fm["name"]}" 与目录名不符')
            if not fm.get('description'):
                add('R3', f'{d}: frontmatter 缺 description')

    # R7 明文密钥扫描（仅扫代码/文本）
    if not quick:
        exts = {'.py', '.md', '.sh', '.yml', '.yaml', '.json', '.txt', '.cmd', '.ini'}
        for root, dirs, files in os.walk(REPO):
            dirs[:] = [x for x in dirs if x not in ('.git', 'node_modules', '__pycache__', '_backup')]
            for f in files:
                if os.path.splitext(f)[1].lower() not in exts:
                    continue
                fp = os.path.join(root, f)
                try:
                    txt = open(fp, encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue
                for pat, label in SECRET_PATTERNS:
                    hits = [m.group(0) for m in re.finditer(pat, txt)]
                    real = [h for h in hits if not is_placeholder(h)]
                    if real:
                        rel = os.path.relpath(fp, REPO)
                        add('R7', f'{rel}: 疑似明文 {label}')

    print()
    if violations:
        print(f'❌ 发现 {len(violations)} 项违规：')
        for rule, msg in violations:
            print(f'   [{rule}] {msg}')
        print('\n修复后重跑本脚本。')
        return 1
    print('✅ 全部校验通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
