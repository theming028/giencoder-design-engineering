# -*- coding: utf-8 -*-
"""r109 · 定位每页「暗色档变量块」的精确起止，并列出块内 border 令牌的原文。
浅色块与暗色块里 `--color-border-N: rgb(var(--gray-M))` **逐字相同** ⇒ 只能靠块范围区分。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = ['base', 'conversation', 'avatar', 'automation', 'skills',
         'dev', 'kanban', 'req-kanban', 'settings', 'task-detail']


def brace_end(t, i):
    """从 t[i] == '{' 开始，返回配对 '}' 的下标"""
    d = 0
    k = i
    while k < len(t):
        if t[k] == '{':
            d += 1
        elif t[k] == '}':
            d -= 1
            if d == 0:
                return k
        k += 1
    return -1


for pg in PAGES[:3]:
    t = io.open(os.path.join(ROOT, 'pages', pg + '.html'), encoding='utf-8', newline='').read()
    print('=' * 90)
    print(pg)
    # 找暗色块选择器
    hits = [m for m in re.finditer(r"giencoder-theme='dark'\]", t)]
    print('  dark 选择器出现次数 =', len(hits))
    for m in hits[:6]:
        # 往前找选择器起点
        s = t.rfind('}', 0, m.start()) + 1
        sel = t[s:m.end() + 1]
        # 找该选择器后的 '{'
        b = t.find('{', m.end())
        if b < 0:
            continue
        e = brace_end(t, b)
        if e < 0:
            continue
        body = t[b + 1:e]
        if '--color-border-2' not in body and '--gray-3' not in body:
            continue
        print()
        print('  块 @%d..%d  (LEN=%d)' % (b, e, e - b))
        print('  选择器尾部: ...%s' % ' '.join(sel.split())[-70:])
        for nm in ['--color-border-1', '--color-border-2', '--color-border-3']:
            mm = re.search(re.escape(nm) + r'\s*:\s*([^;}]+)', body)
            print('    %-20s %s' % (nm, mm.group(1).strip() if mm else '-'))
