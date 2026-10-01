# -*- coding: utf-8 -*-
u"""补齐：仓库 MEMORY.md 的 r107 段应只保留**一份**产物/门禁块（最新的第十拍）。
把第九拍那份（= doc107k.MEM_TAIL_OLD，现仍在文件里）换成一行并入提示。
幂等：mark = '第九拍产物段已并入下方'。
"""
import importlib.util, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('d', os.path.join(HERE, 'doc107k.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

MARK = u'第九拍产物段已并入下方'
NEW = u'> （第九拍产物段已并入下方「第十拍」段 —— 见 PLAYBOOK P3.39 ~ P3.46。）\n'

t, nl = m.rd(m.MEM)
if MARK in t:
    print(u'已应用（跳过）')
    sys.exit(0)
c = t.count(m.MEM_TAIL_OLD)
if c != 1:
    sys.exit(u'!! MEM_TAIL_OLD 命中 %d 次（应 1）' % c)
t2 = t.replace(m.MEM_TAIL_OLD, NEW, 1)
m.wr(m.MEM, t2, nl)
print(u'%s %d -> %d' % (os.path.relpath(m.MEM, m.WS), len(t), len(t2)))
