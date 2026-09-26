# -*- coding: utf-8 -*-
"""kanban.html select 错位修复（幂等，直接对转义后的 JS 字符串文本做替换）"""
import io, os, re, sys

P = os.path.join(os.path.dirname(__file__), '..', '..', 'pages', 'kanban.html')
P = os.path.abspath(P)
s = io.open(P, encoding='utf-8').read()
orig = s


def rep(old, new, name, expect=True):
    global s
    n = s.count(old)
    if n:
        s = s.replace(old, new)
    print(('OK  ' if n else 'SKIP') + ' %-22s x%d' % (name, n), file=sys.stderr)
    return n


# 1. select 根：去掉写死的 width:101px，让 inline-flex 按内容自适应
rep('data-size=\\"small\\" style=\\"position:absolute; left:120px; top:0; width:101px;\\"',
    'data-size=\\"small\\" style=\\"position:absolute; left:120px; top:0;\\"',
    'select-root width')

# 2. select-view：清掉行内尺寸，交由 data-size="small" 契约 + 适配层 CSS
rep('role=\\"combobox\\" aria-expanded=\\"false\\" aria-haspopup=\\"listbox\\" style=\\"min-height:28px; height:28px; padding:0 8px 0 12px; border-radius:6px; font-size:13px;\\"',
    'role=\\"combobox\\" aria-expanded=\\"false\\" aria-haspopup=\\"listbox\\"',
    'view inline style')

# 3. 标签：kb-lbl + 行内样式 -> rq-sel-lbl（放进触发框内的独立 flex 项）
rep('<span class=\\"kb-lbl\\" style=\\"color:var(--color-neutral-7); font-size:13px; line-height:20px; white-space:nowrap; flex:none;\\">类型：</span>',
    '<span class=\\"rq-sel-lbl\\">类型：</span>',
    'lbl -> rq-sel-lbl')

# 4. view-text：清行内样式，由 flex:1 撑开
rep('data-placeholder=\\"全部\\" style=\\"font-size:13px; flex:none; padding-right:4px;\\"',
    'data-placeholder=\\"全部\\"',
    'view-text inline style')

# 5. 去重：注入的 select 适配 CSS 若重复只保留一份
CSS_ONE = (
    '      .kb-boardhead .giencoder-select[data-size="small"] .giencoder-select-view { min-height: 28px; height: 28px; padding: 0 8px 0 12px; border-radius: 6px; }\n'
    '      /* popup 宽度跟随触发框（覆盖组件默认 min-width:200px，避免 101px 触发框被撑开错位） */\n'
    '      .kb-boardhead .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }\n'
    '      .kb-boardhead .giencoder-select-view { gap: 4px; justify-content: flex-start; }\n'
    '      .kb-boardhead .giencoder-select-view .rq-sel-lbl { flex: none; color: var(--color-neutral-7); }\n'
    '      .kb-boardhead .giencoder-select-view-text { flex: 1; min-width: 0; }\n'
)
c = s.count(CSS_ONE)
if c > 1:
    s = s.replace(CSS_ONE, '', c - 1)
print(('OK  ' if c > 1 else 'SKIP') + ' %-22s x%d' % ('dedup select css', c), file=sys.stderr)

if s != orig:
    io.open(P, 'w', encoding='utf-8', newline='').write(s)

# 诊断
print('lbl-span=%d  fixed-width=%d  view-inline=%d  rq-sel-lbl=%d  popup-fit=%d' % (
    s.count('class=\\"kb-lbl\\" style=\\"color:var(--color-neutral-7); font-size:13px'),
    s.count('width:101px'),
    s.count('border-radius:6px; font-size:13px;\\"'),
    s.count('rq-sel-lbl'),
    s.count('.kb-boardhead .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }'),
), file=sys.stderr)
print('DONE')
