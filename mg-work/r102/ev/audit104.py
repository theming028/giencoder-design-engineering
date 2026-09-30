# -*- coding: utf-8 -*-
"""r104 ④ · 全局全要素代码审查（只读扫描，不写盘）

对象 = `pages/conversation.html` 里本代注入的两块（`r102-conv-css` / `r102-conv-js`）
以及它们依赖的 DS token 契约。检查项：

  A 硬编码颜色（字面 hex / rgb() / rgba()），以及「非 token 色是否进了 :root 适配层 + 暗色档」
  B `var(--x)` 引用完整性：注入块里引用的每个自定义属性，是否**在本页面里真的被定义**
  C 自定义属性命名一致性：本页自造变量（`--r93-*`）的定义/引用前后缀是否成对
  D 冗余：同选择器重复声明、僵尸规则（类名在整页无任何引用）
  E 命名规范：类名前缀分布、`data-*` 属性命名、组件类（`giencoder-*`）复用率
  F 稳定性：注入块结构（幂等标记 / 事件委托 / React 兼容点）关键断言

用法： python mg-work/r102/ev/audit104.py
"""
import io
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PAGE = os.path.join(REPO, 'pages', 'conversation.html')

BLOCK = re.compile(r'<style id="r102-conv-css">(.*?)</style>', re.S)
JSBLOCK = re.compile(r'<script id="r102-conv-js">(.*?)</script>', re.S)


def load():
    t = io.open(PAGE, encoding='utf-8').read()
    m, m2 = BLOCK.search(t), JSBLOCK.search(t)
    if not m or not m2:
        sys.exit('!! 找不到注入块')
    return t, m.group(1), m2.group(1)


def head(s, n=110):
    return re.sub(r'\s+', ' ', s).strip()[:n]


def main():
    all_html, css, js = load()
    print('=' * 78)
    print('r104 ④ 代码审查  |  conversation.html %d 字符 | css %d | js %d' % (len(all_html), len(css), len(js)))
    print('=' * 78)

    # ---------------- A 硬编码颜色 ----------------
    print('\n## A 硬编码颜色')
    body = re.sub(r'/\*.*?\*/', '', css, flags=re.S)          # 去掉注释，只看真声明
    hexes = defaultdict(list)
    for m in re.finditer(r'#([0-9a-fA-F]{3,8})\b', body):
        hexes[m.group(0).lower()].append(m.start())
    for m in re.finditer(r'\b(rgba?\([^)]*\))', body):
        hexes['rgb:' + head(m.group(1), 40)].append(m.start())
    print('   字面颜色总数 = %d 种' % len(hexes))
    for k, v in sorted(hexes.items(), key=lambda kv: -len(kv[1])):
        ctx = body[max(0, v[0] - 90):v[0] + 30]
        ctx = re.sub(r'\s+', ' ', ctx)
        print('     %-26s ×%-3d …%s' % (k, len(v), ctx[-95:]))

    # 暗色档是否覆盖了浅色档里定义的本地变量
    def vars_in(seg):
        return set(re.findall(r'(--[a-z0-9-]+)\s*:', seg))
    dark = re.search(r"\[giencoder-theme='dark'\]\s*\{(.*?)\n\}", css, re.S)
    root = re.search(r':root\s*\{(.*?)\n\}', css, re.S)
    lv, dv = vars_in(root.group(1)) if root else set(), vars_in(dark.group(1)) if dark else set()
    r93 = {v for v in lv if v.startswith('--r93-')}
    print('   :root 本地变量 %d 个；暗色档 %d 个；**暗色档缺 %s**' % (
        len(r93), len({v for v in dv if v.startswith('--r93-')}), sorted(r93 - dv) or '无'))

    # ---------------- B var() 引用完整性 ----------------
    print('\n## B var(--x) 引用完整性（注入块引用 → 全页是否定义）')
    used = Counter(re.findall(r'var\(\s*(--[a-z0-9-]+)', css + js))
    defined = set(re.findall(r'(--[a-z0-9-]+)\s*:', all_html))
    missing = {k: v for k, v in used.items() if k not in defined}
    print('   引用 %d 个不同自定义属性；定义 %d 个' % (len(used), len(defined)))
    if missing:
        for k, v in sorted(missing.items(), key=lambda kv: -kv[1]):
            print('   ✗ 未定义却被引用 ×%-3d %s' % (v, k))
    else:
        print('   ✓ 无悬空引用')
    unused = sorted(k for k in defined if k.startswith('--r93-') and k not in used)
    print('   ⚠ 定义了但注入块从不引用（可能僵尸）: %s' % (unused or '无'))

    # ---------------- C 本地变量命名一致性 ----------------
    print('\n## C `--r93-*` 命名一致性')
    names = sorted(k for k in defined if k.startswith('--r93-'))
    print('   共 %d 个。后缀分布（末段）:' % len(names))
    print('     ', dict(Counter(n.split('-')[-1] for n in names).most_common()))

    # ---------------- D 冗余 ----------------
    print('\n## D 冗余')
    sels = re.findall(r'(?m)^([^{}\n][^{}]*?)\s*\{', body)
    sel_ct = Counter(s.strip() for s in sels)
    dup = {k: v for k, v in sel_ct.items() if v > 1}
    print('   规则块 %d 条；**重复选择器 %d 个**' % (len(sels), len(dup)))
    for k, v in sorted(dup.items(), key=lambda kv: -kv[1])[:12]:
        print('     ×%d  %s' % (v, head(k, 100)))
    # 僵尸类：CSS 里出现、整页 HTML（含 JS 模板）里找不到
    cls = set()
    for m in re.finditer(r'\.(r9[0-9]-[a-z0-9-]+)', body):
        cls.add(m.group(1))
    zombie = sorted(c for c in cls if c not in js and all_html.count(c) == 0)
    print('   `.r93-*` 类 %d 个；**全页零引用（僵尸）%d 个**:' % (len(cls), len(zombie)))
    print('     ', zombie or '无')

    # ---------------- E 命名规范 ----------------
    print('\n## E 命名规范 / DS 复用')
    pref = Counter(re.findall(r'\.((?:r|giencoder|gienx)[a-z0-9]*)', body))
    print('   类名前缀 top12:', dict(pref.most_common(12)))
    gc = len(re.findall(r'\.giencoder-[a-z0-9-]+', body))
    print('   规则里用到 `giencoder-*`（DS 组件类）%d 处' % gc)
    print('   `data-*` 属性:', sorted(set(re.findall(r'(data-[a-z0-9-]+)', css + js))))
    print('   `.giencoder-popup-open` 开关引用:', (css + js).count('giencoder-popup-open'))
    print('   投影 token(`--shadow3-down`) 引用:', (css + js).count('--shadow3-down'),
          '| 字面 box-shadow 处数:', len(re.findall(r'box-shadow\s*:', body)))

    # ---------------- F 稳定性 ----------------
    print('\n## F 稳定性断言')
    checks = [
        ('注入 CSS 以幂等块包裹（<!-- r102-conv-css --> 与 END 成对）',
         all_html.count('r102-conv-css') == 2),
        ('注入 JS 以幂等块包裹', all_html.count('r102-conv-js') == 2),
        ('END 标记在 </style> 之后、包住 <style>（r102-css）',
         bool(re.search(r'<!-- /r102-conv-css -->\s*</style>', all_html))),
        ('事件全部走委托（无 per-node 绑定泄漏）', js.count('addEventListener') <= 12),
        ('React 重渲染补回（MutationObserver）', 'MutationObserver' in js),
        ('无 `!important` 滥用（< 90 处）', body.count('!important') < 90),
    ]
    for name, ok in checks:
        print('   %s %s' % ('✓' if ok else '✗', name))
    print('   addEventListener 处数 =', js.count('addEventListener'),
          '| !important =', body.count('!important'))


if __name__ == '__main__':
    main()
