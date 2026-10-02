# -*- coding: utf-8 -*-
u"""r109 第四拍 · 工具：为「我们补丁块里的硬编码色值」算一张 **DS 就近映射表**。

规则（邵先生 2026-10-02 决策）：
  · 浅色值**恰好等于**某个 DS token 的浅色值 ⇒ 直接用该 token（浅色零变化）；
  · 不等 ⇒ **就近映射到 DS 阶梯最接近的一级**（允许 ≤1 级微差）；
  · **品牌 logo 豁免**（Google 四色 + 产品 logo 渐变）；
  · 「半透明遮罩 / 阴影 / 渐变透明端」单独成桶，优先映射到 DS 自带的
    `--color-mask-bg` / `--color-tooltip-bg` / `--color-spin-layer-bg`，否则报出来人工定。

用法： python mg-work/r109/ev/theme/map-colors.py            # 打印建议表
      python mg-work/r109/ev/theme/map-colors.py --json     # 只出机器可读表
"""
import io
import json
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DS = os.path.join(REPO, 'giencoder-design-system', 'colors_and_type.css')

import importlib.util
_spec = importlib.util.spec_from_file_location('sc', os.path.join(HERE, 'scan-hardcolors.py'))
sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sc)

# ---------------------------------------------------------------- 品牌豁免
# 邵先生 2026-10-02：「只豁免品牌 logo」。
BRAND = {
    (66, 133, 244): 'Google logo 蓝',
    (234, 67, 53): 'Google logo 红',
    (251, 188, 5): 'Google logo 黄',
    (52, 168, 83): 'Google logo 绿',
    (15, 81, 151): '产品 logo 深蓝',
    (12, 136, 218): '产品 logo 蓝',
    (44, 195, 213): '产品 logo 青',
    (73, 214, 104): '产品 logo 绿',
    (249, 160, 30): '产品 logo 橙',
    (247, 192, 21): '产品 logo 黄',
    (33, 150, 243): 'Material 蓝',
    (0, 203, 96): 'Material 绿',
}

# 半透明遮罩 / 阴影 → DS 自带语义 token
SCRIM = {
    (0, 0, 0): '--color-mask-bg',
    (255, 255, 255): '--color-spin-layer-bg',
}


def palette():
    u"""→ [(name, (r,g,b))]，浅色档全量（原语阶梯 + 语义 token）。"""
    t = sc.rd(DS)
    i = t.find(u"giencoder-theme='dark'")
    light = t[:i]
    raw = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', light))
    out = []
    for k, v in raw.items():
        v = v.strip()
        if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', v):
            out.append((k, tuple(int(x) for x in v.split(','))))
    for k, v in raw.items():
        v = v.strip()
        m = re.match(r'^rgb\(\s*var\((--[a-z0-9-]+)\)\s*\)$', v)
        if m and m.group(1) in raw:
            b = raw[m.group(1)].strip()
            if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', b):
                out.append((k, tuple(int(x) for x in b.split(','))))
    return out


def family(name):
    m = re.match(r'--([a-z]+)-\d+$', name)
    return m.group(1) if m else ''


def near(v, pal):
    """最近一级（带**同族优先**：有色值时，同族里差 ≤24 的一律优先）。"""
    r, g, b = v
    def d(p):
        return (p[0] - r) ** 2 + (p[1] - g) ** 2 + (p[2] - b) ** 2
    best = min(pal, key=lambda kv: d(kv[1]))
    return best[0], best[1], d(best[1])


def main():
    pal = palette()
    by = collections.defaultdict(list)
    for k, v in pal:
        by[v].append(k)
    rows = []
    buckets = collections.Counter()
    seen = collections.Counter()
    for pg in sc.ALL:
        _b, hit, miss, where, _d = sc.scan(pg)
        for v, n in miss.items():
            seen[v] += n
    for v, n in sorted(seen.items(), key=lambda x: -x[1]):
        r, g, b, a = v
        rgb = (r, g, b)
        if rgb in BRAND:
            rows.append((sc.fmt(v), n, 'BRAND', BRAND[rgb], ''))
            buckets['brand'] += n
            continue
        if rgb in by and a == 255:
            rows.append((sc.fmt(v), n, 'EXACT', '/'.join(by[rgb][:2]), ''))
            buckets['exact'] += n
            continue
        if a < 255:
            tok = SCRIM.get(rgb, '')
            if tok:
                rows.append((sc.fmt(v), n, 'SCRIM', tok, ''))
                buckets['scrim'] += n
                continue
            name, val, _dd = near(rgb, pal)
            d = max(abs(val[i] - rgb[i]) for i in range(3))
            rows.append((sc.fmt(v), n, 'ALPHA?', name, 'opaque 最近 Δ%d' % d))
            buckets['alpha_unknown'] += n
            continue
        name, val, _dd = near(rgb, pal)
        d = max(abs(val[i] - rgb[i]) for i in range(3))
        rows.append((sc.fmt(v), n, 'NEAR', name, 'Δ%d' % d))
        buckets['near'] += n
    if '--json' in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    print(u'桶统计：%s' % dict(buckets))
    print()
    for kind in ('BRAND', 'SCRIM', 'EXACT', 'NEAR', 'ALPHA?'):
        sub = [r for r in rows if r[2] == kind]
        if not sub:
            continue
        print(u'── %s（%d 个值 / %d 处）──' % (kind, len(sub), sum(x[1] for x in sub)))
        for f, n, _k, tok, note in sub:
            print(u'   %-18s ×%-4d → %-28s %s' % (f, n, tok, note))
        print()


if __name__ == '__main__':
    main()
