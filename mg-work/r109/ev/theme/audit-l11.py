# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 偏差审计：逐页比对「当前 vs git HEAD」，只关注第 11 拍可能碰过的串。

目的：在不确定快照是否干净时，**用 git 作为唯一真值源**核对我改了什么。
注意：git HEAD 是 r108 定稿态，工作区含整个 r109 ⇒ 差异必然巨大，
      本脚本只统计**第 11 拍特征串**的计数，判断是否回到「第十拍定稿」基线。
"""
import io
import os
import re
import subprocess
import sys

ROOT = u'E:/GienCoder/giencoder-design-engineering'
PAGES = os.path.join(ROOT, 'pages')
ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

# 第 11 拍特征串（改成什么样 vs 应该是什么样）
MARKS = {
    u'var(--color-bg-1)': None,               # 总量（含既有）
    u'rgba(var(--gray-1),0.88)': None,
    u'rgba(var(--gray-1), 0.88)': None,
    u'rgba(var(--gray-1), 0.9)': None,
    u'r109-menuwhite-css': None,
    u'.giencoder-select-popup{z-index:1000;background:': None,
    u'.skills-popup-bg{width:760px;height:320px;border-radius:8px;background:': None,
}


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def main():
    print(u'=== 第 11 拍特征串 · 当前工作区计数 ===')
    print()
    hdr = u'%-14s' % u'page'
    for m in MARKS:
        hdr += u'%-16s' % m[-14:]
    print(hdr)
    tot = {m: 0 for m in MARKS}
    for pg in ALL:
        t = rd(os.path.join(PAGES, pg + u'.html'))
        row = u'%-14s' % pg
        for m in MARKS:
            n = t.count(m)
            tot[m] += n
            row += u'%-16d' % n
        print(row)
    print(u'%-14s' % u'合计' + u''.join(u'%-16d' % tot[m] for m in MARKS))
    print()
    # 关键判定
    print(u'=== 判定 ===')
    print(u'  r109-menuwhite-css 残留 = %d（应为 0）' % tot[u'r109-menuwhite-css'])
    tail = u'.giencoder-select-popup{z-index:1000;background:'
    for pg in ALL:
        t = rd(os.path.join(PAGES, pg + u'.html'))
        k = t.find(tail)
        if k >= 0:
            val = t[k + len(tail):t.find(u';', k + len(tail))]
            print(u'  %-14s select-popup 底 = %s' % (pg, val))
    for pg in ALL:
        t = rd(os.path.join(PAGES, pg + u'.html'))
        tail2 = u'.skills-popup-bg{width:760px;height:320px;border-radius:8px;background:'
        k = t.find(tail2)
        if k >= 0:
            val = t[k + len(tail2):t.find(u';', k + len(tail2))]
            print(u'  %-14s skills-popup 底 = %s' % (pg, val))
    return 0


if __name__ == '__main__':
    sys.exit(main())
