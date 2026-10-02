# -*- coding: utf-8 -*-
u"""汇总 `scan-mix.sh` 产出的 10 页暗色探针 JSON。

输出：
  · 每页 `total`（暗色档下仍「发亮」的元素数）+ sanity 自证
  · 按「颜色值」聚合，列出该值对应的选择器样本
  · 与上一轮基线目录对比（可选，第二个参数）
"""
import collections
import io
import json
import os
import sys

ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']


def load(d, pg):
    p = os.path.join(d, pg + '.json')
    if not os.path.exists(p):
        return None
    o = json.loads(io.open(p, encoding='utf-8').read())
    while isinstance(o, str):
        o = json.loads(o)
    return o


def short(sel):
    parts = sel.split('>')
    return '>'.join(parts[-2:])[:110]


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else 'mg-work/r109/raw/mix4'
    base = sys.argv[2] if len(sys.argv) > 2 else None
    print(u'=== 暗色档「亮残」汇总：%s ===' % d)
    tot = 0
    grand = collections.Counter()
    for pg in ALL:
        o = load(d, pg)
        if o is None:
            print(u'  %-14s (缺)' % pg)
            continue
        n = o.get('total', 0)
        tot += n
        s = o.get('sanity', {})
        old = ''
        if base:
            b = load(base, pg)
            if b:
                old = u'  [上轮 %d]' % b.get('total', 0)
        print(u'  %-14s 亮残 %-4d%s   sanity: attr=%s gi=%s bg1=%s'
              % (pg, n, old, s.get('attr'), s.get('dataGiDark'), s.get('bg1')))
        per = collections.Counter()
        for it in o.get('items', []):
            per[(it['k'], it['v'])] += 1
        for (k, v), c in per.most_common():
            grand[v] += c
            sels = [short(i['sel']) for i in o.get('items', [])
                    if i['v'] == v][:2]
            print(u'       %-5s %-24s ×%-3d  %s' % (k, v, c, ' | '.join(sels)))
    print()
    print(u'   合计亮残 %d' % tot)
    if base:
        btot = 0
        for pg in ALL:
            b = load(base, pg)
            if b:
                btot += b.get('total', 0)
        print(u'   上轮合计 %d  ⇒  变化 %+d' % (btot, tot - btot))
    print()
    print(u'   按颜色值聚合（全站）：')
    for v, c in grand.most_common():
        print(u'       %-26s ×%d' % (v, c))


if __name__ == '__main__':
    main()
