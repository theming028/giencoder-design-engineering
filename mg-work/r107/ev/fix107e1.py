# -*- coding: utf-8 -*-
"""r107 第五拍 · _mods.html 组件族迁移（menu → dropdown）

把四枚下拉 + 右键菜单容器从「giencoder-select-popup + giencoder-menu（导航菜单族）」
迁到 DS 的 Dropdown 组件族（giencoder-dropdown-popup / -item / -item-selected? /
-divider），并给两枚 radio 项补 DS 契约认可的「勾选图标」选中态。
"""
import io, sys

P = 'mg-work/r107/part107/_mods.html'
s = io.open(P, 'rb').read().decode('utf-8')
raw = s
s = s.replace('\r\n', '\n')
crlf = raw.count('\r\n')

log = []


def rep(old, new, expect):
    global s
    n = s.count(old)
    assert n == expect, 'FAIL count %d != %d  for %r' % (n, expect, old[:70])
    s = s.replace(old, new)
    log.append('%2d  %s' % (n, old[:72]))


# ① 三枚下拉容器：去掉 select-popup + menu，换 dropdown-popup
for slug in ['td-rv-scope-menu', 'td-commit-menu', 'td-rv-opts']:
    rep('class="td-rv-menu giencoder-select-popup giencoder-menu %s"' % slug,
        'class="td-rv-menu giencoder-dropdown-popup %s"' % slug, 1)

# ② 右键菜单容器
rep('class="td-ctxmenu giencoder-select-popup giencoder-menu"',
    'class="td-ctxmenu giencoder-dropdown-popup"', 1)

# ③ 选中项：先去 menu 族的 -selected（4 处）
rep('td-mm-item giencoder-menu-item giencoder-menu-item-selected is-checked',
    'td-mm-item giencoder-dropdown-item is-checked', 4)

# ④ 其余条目
rep('class="td-mm-item giencoder-menu-item"',
    'class="td-mm-item giencoder-dropdown-item"', 11)

# ⑤ 图标位：DS Dropdown 无 icon 子部件 ⇒ 收回自绘
rep('<span class="td-mm-ico giencoder-menu-icon">', '<span class="td-mm-ico">', 15)

# ⑥ 分隔线 → DS Dropdown 的 divider 子部件
rep('<span class="td-mm-line"></span>',
    '<span class="td-mm-line giencoder-dropdown-divider"></span>', 3)

# ⑦ 两枚 radio 项补「勾选图标」（DS dropdown 契约：selected = 文字 primary-6 或勾选图标）
for view in ['unified', 'split']:
    old = '<span class="td-mm-key">%s</span></button>' % ('⌘1' if view == 'unified' else '⌘2')
    new = '<span class="td-mm-key">%s</span><span class="td-mm-mark">✓</span></button>' % (
        '⌘1' if view == 'unified' else '⌘2')
    n = s.count(old)
    assert n == 1, 'FAIL radio mark %s count=%d' % (view, n)
    s = s.replace(old, new)
    log.append(' 1  radio mark += %s' % view)

# ⑧ 残留断言：menu 族类必须清零
for bad in ['giencoder-select-popup', 'giencoder-menu-item', 'giencoder-menu-icon', 'giencoder-menu"']:
    n = s.count(bad)
    assert n == 0, 'RESIDUE %s => %d' % (bad, n)

# ⑨ 新类计数
for good in ['giencoder-dropdown-popup', 'giencoder-dropdown-item', 'giencoder-dropdown-divider']:
    log.append('NEW %s => %d' % (good, s.count(good)))

out = s.replace('\n', '\r\n') if crlf else s
io.open(P, 'wb').write(out.encode('utf-8'))
print('\n'.join(log))
print('chars %d -> %d (LF-normalized)' % (len(raw.replace('\r\n', '\n')), len(s)))
