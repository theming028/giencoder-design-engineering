# -*- coding: utf-8 -*-
u"""解析 base-brand2.json（可能是 JSON 套 JSON），打印品牌 LOGO 详情。"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, os.pardir, os.pardir, u'raw', u'find11',
                   u'base-brand2.json')


def load(path):
    raw = io.open(path, encoding='utf-8').read().strip()
    d = raw
    for _ in range(4):
        if isinstance(d, (list, dict)):
            break
        d = json.loads(d)
    return d


def main():
    d = load(RAW)
    if isinstance(d, dict):
        d = [d]
    for it in d:
        print(u'--- x=%s y=%s w=%s h=%s  cls=%s' % (
            it.get('x'), it.get('y'), it.get('w'), it.get('h'), it.get('cls')))
        print(u'    filter=%s opacity=%s srcLen=%s' % (
            it.get('filter'), it.get('opacity'), it.get('srcLen')))
        print(u'    head : %s' % it.get('srcHead', u'')[:250])
        print(u'    tail : %s' % it.get('srcTail', u'')[-300:])
        print(u'    chain:')
        for c in it.get('chain', []):
            print(u'       %-8s %-44s bg=%-24s filter=%s' % (
                c.get('tag'), c.get('cls'), c.get('bg'), c.get('filter')))
        full = it.get('srcFull') or u''
        if full:
            out = os.path.join(os.path.dirname(RAW), u'brand-full.txt')
            io.open(out, 'w', encoding='utf-8', newline='').write(full)
            print(u'    完整 src → %s（%d 字符）' % (out, len(full)))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
