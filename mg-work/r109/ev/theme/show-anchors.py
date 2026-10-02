# -*- coding: utf-8 -*-
u"""打印 doc109l3.py 要用的锚点（Python repr，便于逐字粘贴）。"""
import io
import os

M = 'E:/GienCoder/giencoder-design-engineering/.workbuddy/memory'


def show(path, keys, ctx=0):
    t = io.open(os.path.join(M, path), encoding='utf-8').read()
    lines = t.split('\n')
    print('=============== %s' % path)
    for i, l in enumerate(lines):
        for k in keys:
            if k in l:
                print('L%04d %r' % (i + 1, l))
                for j in range(1, ctx + 1):
                    if i + j < len(lines):
                        print('      +%d %r' % (j, lines[i + j]))
                break


show('HANDOFF.md', [u'最新一拍 = r109 第二拍', u'第一 / 二拍 —— 🚫 未提交',
                    u'r109 新增（5 条', u'最后更新：2026-10-02'])
show('HANDOFF.md', [u'还原 part 侧：git checkout -- mg-work/r109/part109/'], ctx=3)
show('PAGES.md', [u'### P3.11i'])
show('PAGES.md', [u'**⚠ 改这一块之前必看**'], ctx=0)
show('PLAYBOOK.md', [u'## 附：工作区速览 106 条'])
