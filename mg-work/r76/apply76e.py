#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r76e 补丁 —— 把列表底部渐隐由 30px 加长到 52px。

实测 1440×720：渐隐 30px 时，被切断那半行的文字仍保留约 66% 不透明度，
依旧看得出来"串"，只是浅了些。加长到 52px 后同一位置降到约 35%，
末行完整技能（create-ex 行，位于列表 168~200px 处）的文字区仍保 0.94 以上 ⇒ 不受影响。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, 'pages', 'base.html')

OLD = 'linear-gradient(to bottom, #000 calc(100% - 30px), transparent 100%)'
NEW = 'linear-gradient(to bottom, #000 calc(100% - 52px), transparent 100%)'


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    n = s.count(NEW)
    if n == 2:
        print('  skip  base.html 渐隐长度 已应用')
        return
    n = s.count(OLD)
    if n != 2:
        sys.exit('!! 锚点 OLD 出现 %d 次（期望 2：webkit + 标准各一）' % n)
    s = s.replace(OLD, NEW)
    if s.count(NEW) != 2 or s.count(OLD) != 0:
        sys.exit('!! 自检失败')
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('  ok    base.html 渐隐长度 2 处 → 52px')


if __name__ == '__main__':
    main()
