# -*- coding: utf-8 -*-
u"""补齐：仓库 MEMORY.md 头部索引行（L5）的 P3.11i「共九拍」→「共十拍」+ 追加第十拍要点。"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    return raw.replace(u'\r\n', u'\n'), (u'\r\n' if u'\r\n' in raw else u'\n')


STEPS = [
    (u'共十拍：三段式', u'共九拍：三段式', u'共十拍：三段式', u'索引行 九拍→十拍'),
    (u'改为按触发器现场摆位（原跑到按钮上方', u'+ 拖拽与收起联动退全屏**）**）',
     u'+ 拖拽与收起联动退全屏 / **三枚 `.td-rv-menu` 改为按触发器现场摆位（原跑到按钮上方 34~36px）**）**）',
     u'索引行 +第十拍'),
]

t, nl = rd(MEM)
n0 = len(t)
done, skip = [], []
for mark, old, new, sub in STEPS:
    if mark in t:
        skip.append(sub)
        continue
    c = t.count(old)
    if c != 1:
        sys.exit(u'!! %s：锚点命中 %d 次（应 1）' % (sub, c))
    t = t.replace(old, new, 1)
    done.append(sub)
if len(t) != n0:
    io.open(MEM, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))
print(u'%s %d -> %d' % (os.path.relpath(MEM, REPO), n0, len(t)))
print(u'应用 %d / 跳过 %d' % (len(done), len(skip)))
for x in done:
    print(u'  + ' + x)
for x in skip:
    print(u'  = ' + x)
