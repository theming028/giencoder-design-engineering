# -*- coding: utf-8 -*-
"""定位每页 --color-border-1/2/3 的「定义处」，并回溯所属选择器，判定浅/暗档。

背景：浅块与暗块的 border 声明逐字相同（都是 rgb(var(--gray-3))），
      只能靠「所在块的 selector 是否含 dark」来区分。
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = ['base', 'conversation', 'avatar', 'kanban', 'req-kanban',
         'dev', 'settings', 'automation', 'skills', 'task-detail']

NAMES = ['--color-border-1', '--color-border-2', '--color-border-3']


def enclosing(t, pos):
    """给定位置 pos，回溯找最内层包含它的 {...} 块，返回 (sel_text, b, e)。
    做法：从 pos 往左扫，维护深度；遇到 '}' 深度+1，遇到 '{' 深度-1；
    深度归零时的那个 '{' 就是块的开口。"""
    d = 0
    k = pos
    while k >= 0:
        c = t[k]
        if c == '}':
            d += 1
        elif c == '{':
            if d == 0:
                # 选择器 = 上一个 '}' 或 ';' 或块边界之后
                s = max(t.rfind('}', 0, k), t.rfind(';', 0, k), t.rfind('{', 0, k))
                return t[s + 1:k].strip(), k, -1
            d -= 1
        k -= 1
    return None, -1, -1


def decl_value(t, pos):
    """从 --color-border-N 的起始位置取到分号或右花括号。"""
    e = pos
    while e < len(t) and t[e] not in ';}':
        e += 1
    return t[pos:e].strip()


for pg in PAGES:
    p = os.path.join(ROOT, 'pages', pg + '.html')
    if not os.path.exists(p):
        print(pg, 'MISSING'); continue
    t = io.open(p, encoding='utf-8').read()
    print('=' * 78)
    print(pg)
    for nm in NAMES:
        pat = re.escape(nm) + r'\s*:'
        for m in re.finditer(pat, t):
            # 必须是「定义」而不是「引用」：引用写作 var(--color-border-2)
            # 排除 var( 前缀
            pre = t[max(0, m.start() - 6):m.start()]
            if 'var(' in pre:
                continue
            sel, b, _ = enclosing(t, m.start())
            if sel is None:
                continue
            dark = 1 if ("giencoder-theme='dark'" in sel or
                         'giencoder-theme="dark"' in sel or
                         'theme=dark' in sel or
                         '.dark' in sel.lower()) else 0
            val = decl_value(t, m.start())
            print('  %-18s @%-8d %s  %s' % (nm, m.start(),
                                            'DARK ' if dark else 'LIGHT', val))
            print('        sel: %s' % (sel[:150].replace('\n', ' ')))
