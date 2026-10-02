# -*- coding: utf-8 -*-
u"""r109 第四拍 · 侦察：把「我们自己的补丁块」里的**硬编码绝对色值**列出来，
   并逐个问一句：**DS 里有没有一个 token 的浅色值正好等于它？**

判据（邵先生 2026-10-02 铁律）：
  · 「全局所有界面色值一律用 giencoder 设计系统变量，不得写死绝对色值」；
  · 「前提是**绝对不得影响目前已经正确的浅色模式**」
  ⇒ **替换的必要条件 = DS token 的浅色值与该字面值逐位相等**（浅色零变化，暗色自动跟随）。
     不等 ⇒ 不许动（要动必须邵先生点头）。

用法：
  python mg-work/r109/ev/theme/scan-hardcolors.py            # 全 10 页概览 + 未匹配汇总
  python mg-work/r109/ev/theme/scan-hardcolors.py base       # 单页明细
"""
import io
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
DS = os.path.join(REPO, 'giencoder-design-system', 'colors_and_type.css')

ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']
BASE5 = ['base', 'avatar', 'automation', 'skills', 'settings']

HEX = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b')
FUN = re.compile(r'\b(rgba?|hsla?)\(([^)]*)\)')
NAMED = re.compile(r'(?<![\w-])(white|black|silver|gray|grey|red|maroon|yellow|olive|'
                   r'lime|green|aqua|teal|blue|navy|fuchsia|purple|orange)(?![\w-])')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read().replace(u'\r\n', u'\n')


def hx(s):
    if len(s) in (3, 4):
        s = u''.join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def norm(kind, args):
    u"""把字面值规范成 (r,g,b,a) 或 None。"""
    a = [x.strip() for x in args.split(',')]
    if kind in ('rgb', 'rgba'):
        if any(x.startswith('var(') for x in a):
            return None
        try:
            rgb = [int(float(x)) for x in a[:3]]
        except ValueError:
            return None
        al = 255
        if len(a) > 3:
            try:
                al = round(float(a[3]) * 255)
            except ValueError:
                al = 255
        return tuple(rgb) + (al,)
    return None


def token_table():
    u"""→ (name, (r,g,b,a)) 列表（浅色档）。"""
    t = rd(DS)
    i = t.find(u"giencoder-theme='dark'")
    light = t[:i]
    raw = {k: v for k, v in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', light)}
    out = []
    for k, v in raw.items():
        v = v.strip()
        if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', v):
            out.append((k, tuple(int(x) for x in v.split(',')) + (255,)))
    # 语义 token：rgb(var(--x)) / #hex / rgba(...)
    for k, v in raw.items():
        v = v.strip()
        m = re.match(r'^rgb\(\s*var\((--[a-z0-9-]+)\)\s*\)$', v)
        if m and m.group(1) in raw:
            base = raw[m.group(1)].strip()
            if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', base):
                out.append((k, tuple(int(x) for x in base.split(',')) + (255,)))
        elif re.match(r'^#[0-9a-fA-F]{6}$', v):
            out.append((k, hx(v[1:])))
        elif v.startswith(u'rgba('):
            n = norm('rgba', v[v.find(u'(') + 1:v.rfind(u')')])
            if n:
                out.append((k, n))
    return out


def blocks(t):
    for m in re.finditer(r'<(style|script)([^>]*)>', t):
        tag = m.group(1)
        end = t.find(u'</' + tag + u'>', m.end())
        if end < 0:
            continue
        idm = re.search(r'id="([^"]+)"', m.group(2))
        yield (idm.group(1) if idm else u'(anon)'), tag, t[m.end():end]


def decls(tag, body):
    u"""只取**声明块**（`{...}` 之内）；CSS 里选择器中的 `[style*="…"]` 是**匹配用字面**、
      不是色值 ⇒ 必须排除（否则「未匹配」会被自己的属性选择器灌爆）。"""
    if tag == 'style':
        out = []
        for m in re.finditer(r'\{([^{}]*)\}', body):
            out.append(m.group(1))
        return u'\n'.join(out)
    return body


def scan(pg):
    """→ (命中表, 未匹配表, 逐块明细)。键 = (r,g,b,a)。"""
    toks = token_table()
    by = collections.defaultdict(list)
    for k, v in toks:
        by[v].append(k)
    hit = collections.Counter()
    miss = collections.Counter()
    where = collections.defaultdict(set)
    detail = []
    for bid, tag, body in blocks(rd(os.path.join(PAGES, pg + '.html'))):
        if bid == u'(anon)':
            continue
        body = decls(tag, body)
        local = collections.Counter()
        for m in HEX.finditer(body):
            v = hx(m.group(1))
            local[v] += 1
        for m in FUN.finditer(body):
            v = norm(m.group(1), m.group(2))
            if v:
                local[v] += 1
        if not local:
            continue
        detail.append((bid, local))
        for v, n in local.items():
            (hit if v in by else miss)[v] += n
            where[v].add(bid)
    return by, hit, miss, where, detail


def fmt(v):
    r, g, b, a = v
    s = u'#%02x%02x%02x' % (r, g, b)
    return s if a == 255 else s + u' α%.2f' % (a / 255.0)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    pages = [only] if only else ALL
    gmsg = collections.Counter()
    for pg in pages:
        by, hit, miss, where, detail = scan(pg)
        print(u'== %-12s 可换 token %4d 处 / 未匹配 %4d 处 =='
              % (pg, sum(hit.values()), sum(miss.values())))
        if only:
            for bid, local in detail:
                print(u'   -- %s --' % bid)
                for v, n in sorted(local.items(), key=lambda x: -x[1]):
                    tagv = u'✓ ' + u'/'.join(by[v][:2]) if v in by else u'✗ 无对应'
                    print(u'      %-18s ×%-3d %s' % (fmt(v), n, tagv))
        else:
            for v, n in sorted(miss.items(), key=lambda x: -x[1])[:6]:
                print(u'      ✗ %-18s ×%-3d  %s' % (fmt(v), n, u','.join(sorted(where[v]))[:70]))
                gmsg[fmt(v)] += n
    if not only:
        print()
        print(u'== 未匹配（DS 里没有等值 token）汇总 ==')
        for v, n in gmsg.most_common(40):
            print(u'   %-18s ×%d' % (v, n))


if __name__ == '__main__':
    main()
