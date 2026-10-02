# -*- coding: utf-8 -*-
u"""r109 第四拍（裁决④ 同族就近全收敛）· **映射规划器**

输入：
  A. §30.6 的 5 类 hex 残余（从 PAGES/acceptance 里量出来的现值）
  B. 页面自带的非 var `rgb()/rgba()` 字面（含**属性上下文**，用来判「整条阴影/遮罩 ⇒ 保留」）
输出：每个值 → DS 同族最近档 + Δ + 建议目标串；并给出按属性分类的分布。

只读，不落盘。
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


def nearest(rgb, fam=None, exclude=None):
    best = None
    for f, steps in RAMP.items():
        if fam and f != fam:
            continue
        for lv, c in steps.items():
            d = max(abs(c[0] - rgb[0]), abs(c[1] - rgb[1]), abs(c[2] - rgb[2]))
            if best is None or d < best[2]:
                best = (f, lv, d)
    return best


def parse_func(raw):
    m = re.match(r'^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*'
                 r'(?:,\s*([\d.]+)\s*)?\)$', raw.strip(), re.I)
    if not m:
        return None
    r, g, b = (int(float(m.group(i))) for i in (1, 2, 3))
    a = m.group(4)
    return (r, g, b), (1.0 if a is None else float(a))


# ---------- A. 5 类 hex 残余 ----------
HEX_TARGETS = collections.OrderedDict([
    # ① 类型 / 状态标签前景（同族深档）
    ('#7766fd', u'① 类型标签·紫'),
    ('#f3881e', u'① 状态标签·橙'),
    ('#0fa79a', u'① 状态标签·青'),
    ('#5592eb', u'① 状态标签·蓝'),
    ('#009e61', u'① 状态标签·绿'),
    # ② 代码语法高亮
    ('#0451a5', u'② 语法·关键字蓝'),
    ('#a31515', u'② 语法·字符串红'),
    ('#098658', u'② 语法·数字绿'),
    # ③ 头像身份色板
    ('#e57470', u'③ 头像色板 1'),
    ('#e88b4d', u'③ 头像色板 2'),
    ('#dcab35', u'③ 头像色板 3'),
    ('#a2c143', u'③ 头像色板 4'),
    ('#67b85d', u'③ 头像色板 5'),
    ('#47c2c4', u'③ 头像色板 6'),
    ('#4c93d4', u'③ 头像色板 7'),
])

print(u'======== A. 5 类 hex 残余 → 同族最近档 ========')
print(u'%-10s %-22s %-16s %-6s %s' % (u'现值', u'角色', u'建议目标', u'Δ', u'现值×'))
FUNC = re.compile(r'\b(rgba?|hsla?)\s*\(([^()]*)\)')


def load_pages():
    out = {}
    for pg in at.ALL:
        p = os.path.join(at.PAGES, pg + '.html')
        raw = io.open(p, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n')
        # 剥掉我们自己注入的暗色块
        raw = re.sub(r'<style id="r109-dark-css">.*?</style>', u'', raw, flags=re.S)
        out[pg] = raw
    return out


PG = load_pages()

for v, role in HEX_TARGETS.items():
    rgb = tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    n = sum(t.lower().count(v) for t in PG.values())
    fam_hint = None
    # 同族：先找「最近的非灰族」，避免被灰阶吃掉
    best_col = None
    for f, steps in RAMP.items():
        if f == 'gray':
            continue
        b = nearest(rgb, fam=f)
        if b and (best_col is None or b[2] < best_col[2]):
            best_col = b
    b = best_col
    tgt = u'rgb(var(--%s-%d))' % (b[0], b[1]) if b else u'—'
    print(u'%-10s %-22s %-16s %-6s %d' % (v, role, tgt, b[2] if b else '-', n))

print()
print(u'======== B. 页面自带非 var rgb()/rgba() 字面（按属性归类） ========')
FUNCS = collections.Counter()
CTX = collections.defaultdict(collections.Counter)     # 值 -> 属性 Counter
DECL = re.compile(r'([-a-zA-Z][-a-zA-Z0-9]*)\s*:\s*([^;{}]*)')
for pg, t in PG.items():
    for m in FUNC.finditer(t):
        raw = m.group(0).replace(u' ', u'')
        if u'var(' in m.group(2):
            continue
        p = parse_func(raw)
        if not p:
            continue
        key = u'rgb(%d,%d,%d%s)' % (p[0][0], p[0][1], p[0][2],
                                    u'' if p[1] == 1.0 else u',%g' % p[1])
        FUNCS[key] += 1

# 属性上下文（只在能被 RE_DECL 归到声明时）
for pg, t in PG.items():
    for m in DECL.finditer(t):
        prop, val = m.group(1), m.group(2)
        for fm in FUNC.finditer(val):
            if u'var(' in fm.group(2):
                continue
            p = parse_func(fm.group(0))
            if not p:
                continue
            key = u'rgb(%d,%d,%d%s)' % (p[0][0], p[0][1], p[0][2],
                                        u'' if p[1] == 1.0 else u',%g' % p[1])
            CTX[key][prop.strip().lower()] += 1

for key, n in FUNCS.most_common():
    p = parse_func(key)
    rgb = p[0]
    b = nearest(rgb)
    bc = nearest(rgb, fam=b[0]) if b else None
    props = CTX.get(key, collections.Counter())
    skippable = all(any(s in pr for s in at.SKIP_PROP_SUB) or pr in at.SKIP_PROP_EXACT
                    for pr in props) if props else False
    print(u'%-30s ×%-4d 最近 %-16s Δ%-3s %s'
          % (key, n, u'%s-%d' % (b[0], b[1]) if b else u'—', b[2] if b else '-',
             u'[整条阴影/遮罩 ⇒ 保留]' if skippable else u''))
    for pr, c in props.most_common(6):
        print(u'        %-22s ×%d' % (pr, c))
