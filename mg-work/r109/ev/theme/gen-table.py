# -*- coding: utf-8 -*-
u"""r109 第四拍（裁决④「同族就近全收敛」）· **收敛表生成器**

按 `hard-colors.py` 的同口径（排除 DS 内联包 / `r109-theme-css` / `r109-dark-css`；只取声明块内），
把**残余硬编码**（hex + `rgb()/rgba()` 函数式）逐条算出「同族最近档 + Δ」，并检查该值出现的属性：
  · 属性落在「整条阴影 / 遮罩」⇒ 按邵先生裁决 **保留字面**（KEEP）
  · 品牌 logo ⇒ 保留
  · 其余 ⇒ 给出目标串
输出：可直接粘进 `apply-tokens.py` 的 `OVERRIDE` / `LIT_OVERRIDE` 条目。

用法：python gen-table.py            # CSS 侧
      python gen-table.py --js       # <script> 侧
"""
import collections
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('at', os.path.join(HERE, 'apply-tokens.py'))
at = importlib.util.module_from_spec(spec)
spec.loader.exec_module(at)

RAMP = at.RAMP
WANT_JS = '--js' in sys.argv

SKIP_BID = {u'r109-theme-css', u'r109-dark-css'}


def nearest(rgb, fam=None):
    best = None
    for f, steps in RAMP.items():
        if fam and f != fam:
            continue
        for lv, c in steps.items():
            d = max(abs(c[0] - rgb[0]), abs(c[1] - rgb[1]), abs(c[2] - rgb[2]))
            if best is None or d < best[2]:
                best = (f, lv, d)
    return best


def best_family(rgb):
    u"""同族最近：先在**有色族**里找（避免被灰阶吃掉色相），若灰阶明显更近才用灰阶。"""
    allb = nearest(rgb)
    col = None
    for f, steps in RAMP.items():
        if f == 'gray':
            continue
        b = nearest(rgb, fam=f)
        if b and (col is None or b[2] < col[2]):
            col = b
    neutralish = (max(rgb) - min(rgb)) <= 8
    if neutralish and allb and (col is None or allb[2] <= col[2]):
        return allb
    return col or allb


def norm_func(raw):
    m = re.match(r'^(rgba?|hsla?)\(([^()]*)\)$', raw.strip(), re.I)
    if not m:
        return None
    fn, inner = m.group(1).lower(), m.group(2)
    parts = [p.strip() for p in inner.split(',')]
    if not fn.startswith('rgb') or len(parts) not in (3, 4):
        return None
    try:
        rgb = [int(round(float(p))) for p in parts[:3]]
    except ValueError:
        return None
    if len(parts) == 3:
        return u'rgb(%d,%d,%d)' % tuple(rgb), tuple(rgb), 1.0
    try:
        a = float(parts[3])
    except ValueError:
        return None
    return u'rgb(%d,%d,%d,%s)' % (rgb[0], rgb[1], rgb[2], u'%g' % a), tuple(rgb), a


FUNC = re.compile(r'\b(rgba?|hsla?)\s*\(([^()]*)\)')
HEXR = at.HEX
DECL = re.compile(r'([-a-zA-Z][-a-zA-Z0-9]*)\s*:\s*([^;{}]*)')
RE_RULE = re.compile(r'([^{}]*)\{([^{}]*)\}')

# 值 -> 出现过的属性 Counter（只统计**非阴影类**属性，用来判 KEEP）
props = collections.defaultdict(collections.Counter)
cnt = collections.Counter()
brand = set()


def is_skip_prop(p):
    p = p.lower()
    return p in at.SKIP_PROP_EXACT or any(s in p for s in at.SKIP_PROP_SUB)


for pg in at.ALL:
    t, nl = at.rd(os.path.join(at.PAGES, pg + '.html'))
    for bid, tag, s, e, body in at.blocks(t):
        if bid in SKIP_BID:
            continue
        if tag == 'style' and bid == u'(anon)' and at.DS_FINGERPRINT in body:
            continue
        if (tag == 'script') != bool(WANT_JS):
            continue
        if tag == 'style':
            for rm in RE_RULE.finditer(body):
                sel = rm.group(1)
                if at.RE_DARKSEL.search(sel):
                    continue
                for dm in DECL.finditer(rm.group(2)):
                    prop, val = dm.group(1).strip(), dm.group(2)
                    for hm in HEXR.finditer(val):
                        v = at.hex6(hm.group(0)[1:])
                        cnt[v] += 1
                        props[v][prop] += 1
                    for fm in FUNC.finditer(val):
                        if u'var(' in fm.group(2):
                            continue
                        p = norm_func(fm.group(0))
                        if not p:
                            continue
                        cnt[p[0]] += 1
                        props[p[0]][prop] += 1
        else:
            for hm in HEXR.finditer(body):
                v = at.hex6(hm.group(0)[1:])
                cnt[v] += 1
                props[v][u'(js)'] += 1
            for fm in FUNC.finditer(body):
                if u'var(' in fm.group(2):
                    continue
                p = norm_func(fm.group(0))
                if not p:
                    continue
                cnt[p[0]] += 1
                props[p[0]][u'(js)'] += 1

print(u'== %s 侧残余：%d 处 / %d 值 ==' % (u'JS' if WANT_JS else u'CSS', sum(cnt.values()), len(cnt)))
print()
keep, out = [], []
for v, n in sorted(cnt.items(), key=lambda x: -x[1]):
    if v.startswith('#'):
        rgb = tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    else:
        rgb = norm_func(v)[1]
    b = best_family(rgb)
    tgt = u'rgb(var(--%s-%d))' % (b[0], b[1])
    if not v.startswith('#'):
        p = norm_func(v)
        tgt = (u'rgba(var(--%s-%d), %g)' % (b[0], b[1], p[2])) if p[2] != 1.0 \
            else u'rgb(var(--%s-%d))' % (b[0], b[1])
    pr = props[v]
    allskip = pr and all(is_skip_prop(k) for k in pr)
    if v in at.EXEMPT_VALUES or v in at.EXCLUDE_VALUES or allskip:
        keep.append((v, n, b, dict(pr)))
        continue
    out.append((v, n, b, tgt, dict(pr)))

print(u'---- KEEP（阴影/遮罩/豁免） %d 值 ----' % len(keep))
for v, n, b, pr in keep:
    print(u'  %-26s ×%-4d Δ%-3d %s' % (v, n, b[2], pr))
print()
print(u'---- 收敛条目 %d 值 ----' % len(out))
for v, n, b, tgt, pr in sorted(out, key=lambda x: -x[1]):
    print(u"    (u'%s', (u'%s', u'同族就近 Δ%d', %d))," % (v, tgt, b[2], b[2]))
    print(u'        #   ×%-4d  属性 %s' % (n, pr))
