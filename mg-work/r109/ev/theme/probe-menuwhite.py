# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 侦察 B：全站「下拉菜单容器」的**浅色档**背景现状。

要枚举的家族（凡是有 popup / dropdown / menu / select / date-picker 且带 background 的规则）：
  .giencoder-select-popup / .giencoder-dropdown-popup / .giencoder-popup
  .zd-menu / .giencoder-date-picker-popup / 内联 style 里的菜单面板
并判定：该规则是「浅色档通用」还是「暗色档专用」，浅色档实际解析出来是不是纯白。
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

# 菜单容器选择器族
RE_SEL = re.compile(
    u'(?:\\.giencoder-[a-z-]*(?:popup|dropdown|menu|select)[a-z-]*'
    u'|\\.zd-menu[a-z-]*|\\.giencoder-date-picker-popup)')

RE_BG = re.compile(u'background\\s*:\\s*([^;`\'}]+)')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def norm(t):
    return t.replace(u'\r\n', u'\n')


def main():
    agg = collections.OrderedDict()
    for pg in ALL:
        t = norm(rd(os.path.join(PAGES, pg + u'.html')))
        # 遍历所有含菜单选择器的规则块
        for m in RE_SEL.finditer(t):
            sel_start = m.start()
            # 往后找最近的 '{'
            b = t.find(u'{', sel_start)
            if b < 0 or b - sel_start > 160:
                continue
            sel = t[sel_start:b].strip()
            e = t.find(u'}', b)
            if e < 0 or e - b > 700:
                continue
            body = t[b + 1:e]
            bm = RE_BG.search(body)
            if not bm:
                continue
            val = bm.group(1).strip()
            # 判定块归属：往前找最近的顶层选择器（含 dark 关键字即暗块）
            head = t[max(0, sel_start - 260):sel_start]
            is_dark = u'[giencoder-theme=dark]' in head or u'theme=dark' in head
            key = (sel[:78], val[:52], u'暗' if is_dark else u'浅')
            agg.setdefault(key, []).append(pg)

    print(u'=== 全站下拉菜单容器 background 声明（选择器 × 值 × 档）===')
    print()
    for (sel, val, tag), pgs in sorted(agg.items(), key=lambda x: (x[0][2], x[0][0])):
        print(u'  [%s] %-12s' % (tag, u','.join(sorted(set(pgs)))))
        print(u'        sel: %s' % sel)
        print(u'        bg : %s' % val)
    print()
    print(u'  合计不同组合：%d' % len(agg))
    return 0


if __name__ == '__main__':
    sys.exit(main())
