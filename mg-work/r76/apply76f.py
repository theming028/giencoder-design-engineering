#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76f 补丁 —— 修掉 r76 需求 3 引入的唯一一条门禁新增项。

verify-design.py 的 CRAFT-ANIM 用正则 (?:animation|transition)[^;}`]*?(\\d+)ms
抓所有 >300ms 的时长 —— 连 animation-delay 一起抓。
r76 的亮相错峰最后一段是 animation-delay: 325ms ⇒ 触发 🟡（实测唯一一条新增）。

修法：把错峰由 40/80/115/150/185/220/255/290/325 改成统一 32ms 步进
      32/64/96/128/160/192/224/256/288（末段 288 ≤ 300）。
      总跨度 325→288（-11%），观感差异可忽略；动画时长 260ms 不变。
同时更新那段注释里的「递进 35~40ms」——注释与代码不一致是负资产。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'avatar.html')

MAP = [
    ('animation-delay: 40ms;', 'animation-delay: 32ms;'),
    ('animation-delay: 80ms;', 'animation-delay: 64ms;'),
    ('animation-delay: 115ms;', 'animation-delay: 96ms;'),
    ('animation-delay: 150ms;', 'animation-delay: 128ms;'),
    ('animation-delay: 185ms;', 'animation-delay: 160ms;'),
    ('animation-delay: 220ms;', 'animation-delay: 192ms;'),
    ('animation-delay: 255ms;', 'animation-delay: 224ms;'),
    ('animation-delay: 290ms;', 'animation-delay: 256ms;'),
    ('animation-delay: 325ms;', 'animation-delay: 288ms;'),
]
OLD_NOTE = '错峰按「头部 → 分隔线 → 4 张卡 → 3 行 → 页脚」递进 35~40ms，'
NEW_NOTE = '错峰按「头部 → 分隔线 → 4 张卡 → 3 行 → 页脚」递进 32ms，'


def main():
    s = io.open(PAGE, encoding='utf-8').read()

    done = all(new in s for _, new in MAP)
    if done:
        print('  skip  avatar.html 错峰重排 已应用')
        return

    for old, new in MAP:
        n = s.count(old)
        if n != 1:
            sys.exit('!! 锚点 %r 出现 %d 次（期望 1）' % (old, n))
    for old, new in MAP:
        s = s.replace(old, new)
    if s.count(OLD_NOTE) != 1:
        sys.exit('!! 注释锚点出现 %d 次（期望 1）' % s.count(OLD_NOTE))
    s = s.replace(OLD_NOTE, NEW_NOTE)

    # 自检：新值齐、旧值尽、标签计数不变
    for _, new in MAP:
        if s.count(new) != 1:
            sys.exit('!! 自检失败：%r 计 %d' % (new, s.count(new)))
    for old, _ in MAP:
        if s.count(old) != 0:
            sys.exit('!! 自检失败：旧值残留 %r' % old)
    if '325ms' in s:
        sys.exit('!! 自检失败：文件内仍有 325ms')
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('  ok    avatar.html 错峰重排 9 处 + 注释 1 处')


if __name__ == '__main__':
    main()
