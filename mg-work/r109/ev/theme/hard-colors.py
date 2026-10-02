# -*- coding: utf-8 -*-
u"""r109 第四拍 · 侦察②：把「**我们自己的页面 CSS**」里的硬编码绝对色值全量列出来。

与 `scan-hardcolors.py` 的分工：
  · 旧工具只看**具名**块（跳过匿名块）⇒ 漏掉了 kanban / req-kanban / task-detail / dev
    那几大块**匿名的页面级 `<style>`**（`--kb-*` 等就住在那里）；
  · 本工具把**匿名 `<style>` 块也一并纳入**，但**排除 DS 内联包**与**本拍自己写的两个适配块**。

排除清单（各自有硬理由）：
  · **DS 内联包**（每页 1 块、~93.7KB，指纹 `:root{--giencoderblue-1:245, 248, 255;`）
    —— 那是**设计系统本体**的构建产物（`--color-*` / `--gray-N` 的**定义处**），
    改它 = 改设计系统，不属于「页面用色」范畴；
  · `r109-theme-css` —— 只有 `color-scheme`，无色值；
  · `r109-dark-css` —— 本拍的**暗色适配层**，里面本来就该出现暗色值
    （含 `rgba(0,0,0,0)` 渐变端与阴影），计入会污染统计。

只取**声明块** `{...}` 之内（选择器里的 `[style*="…"]` 是匹配用字面、不是色值）。

用法：
  python mg-work/r109/ev/theme/hard-colors.py                 # 全站汇总（按值）
  python mg-work/r109/ev/theme/hard-colors.py --by-block      # 按「值 × 块」逐条
  python mg-work/r109/ev/theme/hard-colors.py --map           # 附 DS 映射建议
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
DS = os.path.join(REPO, 'giencoder-design-system', 'colors_and_type.css')

ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']

DS_FINGERPRINT = u':root{--giencoderblue-1:245, 248, 255;'
SKIP_BID = {u'r109-theme-css', u'r109-dark-css'}

HEX = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b')
FUN = re.compile(r'\b(rgba?|hsla?)\(([^)]*)\)')

# ★★ 必须与 apply-tokens.py 的豁免**逐条对齐**，否则统计虚高：
#   · `mask*` 属性里的 `#000` 是**遮罩 alpha 通道，根本不是颜色**（实测 41 处全是这个）；
#   · 阴影是主题中性的黑/白 scrim，DS 用 `--shadow*` 整条表达，不拆色值；
#   · `logo` 属性 = 品牌豁免（邵先生：「只豁免品牌 logo」）。
SKIP_PROP_EXACT = {'box-shadow', 'text-shadow', 'filter', 'backdrop-filter',
                   '-webkit-filter', '-webkit-backdrop-filter', 'mask', 'mask-image'}
SKIP_PROP_SUB = ('mask', 'logo', 'shadow')
EXEMPT_VALUES = {'#000000', '#000',
                 '#4285f4', '#ea4335', '#fbbc05', '#34a853',
                 '#0f5197', '#0c88da', '#2cc3d5', '#49d66a',
                 '#f9a01e', '#f7c015', '#2196f3', '#00cb60'}
RE_DARKSEL = re.compile(r"giencoder-theme|\.dark\b|\[data-theme|prefers-color-scheme")
RE_DECL = re.compile(r'([-a-zA-Z][-a-zA-Z0-9]*)\s*:\s*([^;{}]*)')


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read().replace(u'\r\n', u'\n')


def hx(s):
    if len(s) in (3, 4):
        s = u''.join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def norm(kind, args):
    u"""→ (r,g,b,a) 或 None（带 var() / calc() 的一律不认，交给浏览器）。"""
    a = [x.strip() for x in args.split(',')]
    if kind in ('rgb', 'rgba'):
        if any(x.startswith('var(') or x.startswith('calc(') for x in a):
            return None
        try:
            rgb = [int(round(float(x))) for x in a[:3]]
        except ValueError:
            return None
        al = 255
        if len(a) > 3:
            try:
                al = round(float(a[3]) * 255)
            except ValueError:
                return None
        return tuple(rgb) + (al,)
    if kind in ('hsl', 'hsla'):
        return None
    return None


def decls(tag, body):
    u"""→ 逐条 `(属性, 值)`，**已对齐 apply-tokens.py 的豁免**：
       剔掉 `{...}` 之外的一切（选择器里的匹配用字面 / `@media` 前导）、
       剔掉**暗色选择器整条规则**、剔掉 `mask*` / 阴影 / `logo` 属性。"""
    if tag != 'style':
        return
    for m in re.finditer(r'([^{}]*)\{([^{}]*)\}', body):
        if RE_DARKSEL.search(m.group(1)):
            continue
        for d in RE_DECL.finditer(m.group(2)):
            prop = d.group(1).strip()
            p = prop.lower()
            if p in SKIP_PROP_EXACT or any(s in p for s in SKIP_PROP_SUB):
                continue
            yield prop, d.group(2)


def blocks(t):
    for m in re.finditer(r'<(style|script)([^>]*)>', t):
        tag = m.group(1)
        end = t.find(u'</' + tag + u'>', m.end())
        if end < 0:
            continue
        idm = re.search(r'id="([^"]+)"', m.group(2))
        bid = idm.group(1) if idm else u'(anon)'
        yield bid, tag, m.end(), t[m.end():end]


def scan(pg):
    u"""→ (按值计数, 值→块集合, 按块计数, 块→值集合)"""
    t = rd(os.path.join(PAGES, pg + '.html'))
    by_val = collections.Counter()
    val_blk = collections.defaultdict(set)
    by_blk = collections.Counter()
    blk_val = collections.defaultdict(collections.Counter)
    for bid, tag, _s, body in blocks(t):
        if bid in SKIP_BID:
            continue
        if bid == u'(anon)' and DS_FINGERPRINT in body:
            continue
        if bid == u'(anon)' and tag != 'style':
            continue
        local = collections.Counter()
        for prop, val in decls(tag, body):
            for m in HEX.finditer(val):
                v = hx(m.group(1))
                if u'#%02x%02x%02x' % v[:3] in EXEMPT_VALUES:
                    continue
                local[v] += 1
            for m in FUN.finditer(val):
                v = norm(m.group(1), m.group(2))
                if v:
                    local[v] += 1
        if not local:
            continue
        for v, n in local.items():
            by_val[v] += n
            val_blk[v].add(bid)
            blk_val[bid][v] += n
        by_blk[bid] += sum(local.values())
    return by_val, val_blk, by_blk, blk_val


def fmt(v):
    r, g, b, a = v
    s = u'#%02x%02x%02x' % (r, g, b)
    return s if a == 255 else s + u' α%.2f' % (a / 255.0)


# ------------------------------------------------------------------ DS 参考表
def ds_tables():
    t = rd(DS)
    i = t.find(u"giencoder-theme='dark'")
    light = t[:i]
    raw = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', light))
    prim = {}
    sem = {}
    for k, v in raw.items():
        v = v.strip()
        if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', v):
            prim[k] = tuple(int(x) for x in v.split(',')) + (255,)
    for k, v in raw.items():
        v = v.strip()
        m = re.match(r'^rgb\(\s*var\((--[a-z0-9-]+)\)\s*\)$', v)
        if m and m.group(1) in prim:
            sem[k] = prim[m.group(1)]
            continue
        # ⚠ 语义 token 里还有**直接写字面**的一批（`--color-bg-1: #ffffff`、
        #   `--color-mask-bg: rgba(0,0,0,.4)`、`--color-menu-dark-bg: #232324`…）
        #   不补进来的话 `#ffffff` 会被「就近」错配到某个有色阶梯上（真踩过）。
        if re.match(r'^#[0-9a-fA-F]{6}$', v):
            sem[k] = hx(v[1:])
        elif re.match(r'^rgba?\(', v):
            n = norm('rgba' if v.startswith('rgba') else 'rgb',
                     v[v.find('(') + 1:v.rfind(')')])
            if n:
                sem[k] = n
    return prim, sem


def main():
    flags = set(a for a in sys.argv[1:] if a.startswith('--'))
    prim, sem = ds_tables()
    exact_prime = collections.defaultdict(list)
    for k, v in prim.items():
        exact_prime[v].append(k)
    exact_sem = collections.defaultdict(list)
    for k, v in sem.items():
        exact_sem[v].append(k)

    gv = collections.Counter()
    gblk = collections.defaultdict(set)
    per_page = {}
    for pg in ALL:
        by_val, val_blk, by_blk, blk_val = scan(pg)
        per_page[pg] = (by_val, val_blk, by_blk, blk_val)
        for v, n in by_val.items():
            gv[v] += n
            gblk[v] |= val_blk[v]

    if '--by-block' in flags:
        for pg in ALL:
            by_val, val_blk, by_blk, blk_val = per_page[pg]
            print(u'== %s（%d 处）' % (pg, sum(by_val.values())))
            for bid, cnt in blk_val.items():
                print(u'   -- %-16s %4d 处 / %2d 个值' % (bid, sum(cnt.values()), len(cnt)))
                for v, n in sorted(cnt.items(), key=lambda x: -x[1]):
                    print(u'        %-18s ×%-3d' % (fmt(v), n))
        return

    print(u'== 全站硬编码色值（我们的页面 CSS）汇 ==')
    print(u'   合计 %d 处 / %d 个不同值' % (sum(gv.values()), len(gv)))
    exact_all = 0
    near_all = 0
    scrim_all = 0
    for v, n in gv.most_common():
        r, g, b, a = v
        rgb3 = (r, g, b)
        if a < 255:
            tagv = u'半透明（α=%.2f）' % (a / 255.0)
            scrim_all += n
        elif v in exact_prime or v in exact_sem:
            names = exact_prime.get(v, []) + exact_sem.get(v, [])
            tagv = u'EXACT → ' + u'/'.join(names[:3])
            exact_all += n
        else:
            # 就近（同族优先）
            def d(p):
                return (p[0] - r) ** 2 + (p[1] - g) ** 2 + (p[2] - b) ** 2
            best = min(list(prim.items()) + list(sem.items()), key=lambda kv: d(kv[1]))
            dd = max(abs(best[1][i] - rgb3[i]) for i in range(3))
            tagv = u'NEAR → %-24s Δ%d' % (best[0], dd)
            near_all += n
        print(u'   %-18s ×%-4d %s   [%s]'
              % (fmt(v), n, tagv, u','.join(sorted(gblk[v]))[:64]))
    print()
    print(u'   桶：EXACT %d 处 / NEAR %d 处 / 半透明 %d 处' % (exact_all, near_all, scrim_all))


if __name__ == '__main__':
    main()
