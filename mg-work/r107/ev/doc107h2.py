# -*- coding: utf-8 -*-
"""r107 第七拍 · HANDOFF.md 第二批（EDITS 处数 / 索举行 / 资产行 / 探针与裁片清单）。
用法： python mg-work/r107/ev/doc107h2.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')

TABLE = [
    (u'（由 `ev/make107.py` 从 apply106 做 **11 处精确替换**生成），',
     u'（由 `ev/make107.py` 从 apply106 做 **13 处精确替换**生成），', 1),

    (u'⇒ `apply107.py` 仍是「apply106 + **11 处替换**」的干净产物。',
     u'⇒ `apply107.py` 是「apply106 + **13 处替换**」（第七拍新增 `2d)` 正 + 逆）的干净产物。', 1),

    (u'`mg-work/r107/ev/make107.py`（从 `apply106.py` **11 处精确替换**）；',
     u'`mg-work/r107/ev/make107.py`（从 `apply106.py` **13 处精确替换**）；', 1),

    (u'从 `apply106.py` 做 **11 处精确替换**生成（每处命中数断言',
     u'从 `apply106.py` 做 **13 处精确替换**生成（每处命中数断言', 1),

    (u'从 apply106 做 11 处精确替换生成**；GENS 五代',
     u'从 apply106 做 13 处精确替换生成**；GENS 五代', 1),

    (u'/ `acceptance.md`（**十一节**：口径', u'/ `acceptance.md`（**十二节**：口径', 1),

    (u'/ **第六拍三条**）/ **`part107/`**（第六拍后：`_head.html` 5270 · `_mods.html` 35876 · **`browse.html` 71538 = 组装件** · `panel.css` 38038 · `panel.js` 48583）',
     u'/ **第六拍三条** / **第七拍七条**）/ **`part107/`**（第七拍后：`_head.html` 5270 · `_mods.html` 35916 · **`browse.html` 71578 = 组装件** · `panel.css` 39686 · `panel.js` 48583）', 1),

    (u'· **`p107f1~p107f7.js` + `p107g1.js`（第六拍探针）** · `scan-flatten.py`',
     u'· **`p107f1~p107f7.js` + `p107g1.js`（第六拍探针）** · **`p107h1~h3.js` + `probe107h{,2,3}.sh` + `patch107h{,2}.py` + `doc107h{,2}.py`（第七拍）** · `scan-flatten.py`', 1),

    (u'· **`f1-composer` / `f3-alert1100` / `f4-skill1280`（第六拍改前）· `g1-stats` / `g2-skill1440` / `g3-skill1280` / `g4-alert1100` / `g5-alert1100`（第六拍改后）**）。',
     u'· **`f1-composer` / `f3-alert1100` / `f4-skill1280`（第六拍改前）· `g1-stats` / `g2-skill1440` / `g3-skill1280` / `g4-alert1100` / `g5-alert1100`（第六拍改后）** · **`h2-{add-menu,opts-menu,commit}`（第七拍改前）· `h3-{add-menu,opts-menu,commit,ctxmenu}`（第七拍改后）**）。', 1),
]


def main():
    b = io.open(P, 'rb').read()
    t = b.decode('utf-8')
    for old, new, want in TABLE:
        n = t.count(old)
        if n != want:
            sys.exit(u'!! 锚点命中 %d 次（应 %d 次）：%r' % (n, want, old[:80]))
        t = t.replace(old, new)
    io.open(P, 'wb').write(t.encode('utf-8'))
    t2 = t.replace('\r\n', '\n')
    print(u'   HANDOFF.md → %d 字符' % len(t2))
    for k in [u'13 处', u'十二节', u'39686', u'71578', u'35916', u'p107h1']:
        print(u'   %s x %d' % (k, t2.count(k)))
    for k in [u'11 处精确替换', u'做 11 处精确替换']:
        print(u'   残留 %r x %d' % (k, t2.count(k)))


if __name__ == '__main__':
    main()
