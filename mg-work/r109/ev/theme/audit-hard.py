# -*- coding: utf-8 -*-
u"""
r109 第六拍 · 全形态硬编码色值清点器（只读）

与 hard-colors.py 的差别：
  * 同时覆盖 #hex / rgb() / rgba() / hsl() / hsla() 五种字面形态
  * **剥离** CSS 与 JS 注释（注释里的色值只是说明文字，不是渲染值）
  * **剥离** 补丁自注入的 <style id="r109-dark-css"> 块（那是产物、不是页面源码）
  * 记录每个字面的**所属属性名**（background / color / box-shadow / fill / 其它）

输出：按「属性族 × 字面值」汇总，供裁决与收敛。
"""
import io, os, re, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    u'..', u'..', u'..', u'..'))
PAGES = os.path.join(ROOT, u'pages')
ALL = [u'base', u'dev', u'kanban', u'req-kanban', u'task-detail',
       u'automation', u'avatar', u'skills', u'conversation', u'settings']

# ---------- 字面匹配 ----------
RE_HEX = re.compile(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{4}\b|#[0-9a-fA-F]{3}\b')
RE_FUNC = re.compile(r'\b(rgba?|hsla?)\s*\(([^()]*)\)')
RE_ANY = re.compile(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\s*\([^()]*\)')

# 属性名（CSS 声明 / JS 规格键 / SVG 属性）→ 归族
def fam_of(prop):
    p = (prop or u'').lower()
    if not p:
        return u'(未知)'
    if 'shadow' in p:
        return u'阴影'
    if p in (u'background', u'background-color', u'bg', u'backgroundColor', u'fill') or p.endswith('bg'):
        return u'面'
    if p in (u'color', u'textColor'):
        return u'字'
    if 'border' in p:
        return u'线'
    if p in (u'stroke', u'outline', u'caret-color', u'accent-color'):
        return u'线'
    if 'filter' in p or 'backdrop' in p:
        return u'滤镜'
    if p in (u'scrollbar-color',) or 'scrollbar' in p:
        return u'滚动条'
    return u'其它(%s)' % p


def prop_before(text, i):
    u"""取 i 位置之前最近的属性名：兼容 CSS `prop: value;` 与 JS `prop:` / `prop="`。"""
    seg = text[max(0, i - 120):i]
    m = None
    for m2 in re.finditer(r'([a-zA-Z-]{2,32})\s*[:=]\s*$', seg):
        m = m2
    if m:
        return m.group(1)
    # SVG: fill="#xxx"
    for m2 in re.finditer(r'([a-zA-Z-]{2,32})\s*[:=]\s*["`\']?$', seg):
        m = m2
    return m.group(1) if m else u''


def norm_lit(raw):
    u"""规范化：rgb/rgba 统一为 rgb(r,g,b[,a])；hex 小写。"""
    s = raw.strip()
    m = re.match(r'^(rgba?|hsla?)\(([^()]*)\)$', s, re.I)
    if not m:
        return s.lower()
    fn, inner = m.group(1).lower(), m.group(2)
    parts = [p.strip() for p in inner.split(',')]
    if fn.startswith('rgb') and len(parts) in (3, 4):
        try:
            rgb = [int(round(float(p))) for p in parts[:3]]
        except ValueError:
            return s
        if len(parts) == 3:
            return u'rgb(%d,%d,%d)' % tuple(rgb)
        try:
            a = float(parts[3])
        except ValueError:
            return s
        return u'rgb(%d,%d,%d,%s)' % (rgb[0], rgb[1], rgb[2], u'%g' % a)
    return s


def strip_noise(t):
    u"""剥离注释与补丁块。"""
    t = re.sub(r'<style id="r109-dark-css">.*?</style>', u'', t, flags=re.S)
    t = re.sub(r'<!--.*?-->', u'', t, flags=re.S)
    t = re.sub(r'/\*.*?\*/', u'', t, flags=re.S)
    # JS 行注释（保守：只在行首或 ; 或 { 后）
    t = re.sub(r'(?m)^\s*//[^\n]*$', u'', t)
    return t


def rd(p):
    b = io.open(p, 'rb').read()
    return b.decode('utf-8').replace(u'\r\n', u'\n')


def main():
    byfam = collections.defaultdict(collections.Counter)
    byval = collections.Counter()
    val_fam = collections.defaultdict(set)
    per_page = collections.Counter()
    detail = collections.defaultdict(list)

    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = strip_noise(rd(p))
        for m in RE_ANY.finditer(t):
            raw = m.group(0)
            inner = raw[raw.find(u'(') + 1:raw.rfind(u')')] if u'(' in raw else u''
            if u'var(' in inner:
                continue                       # DS 消费形态
            key = norm_lit(raw)
            prop = prop_before(t, m.start())
            fam = fam_of(prop)
            byfam[fam][key] += 1
            byval[key] += 1
            val_fam[key].add(fam)
            per_page[pg] += 1
            if len(detail[key]) < 4:
                ctx = t[max(0, m.start() - 70):m.start() + 30].replace(u'\n', u'\\n')
                detail[key].append(u'%s:%s | %s' % (pg, prop, ctx))

    tot = sum(byval.values())
    print(u'=== 全形态非 var 色值字面：%d 处 / %d 值 ===' % (tot, len(byval)))
    print(u'按页：' + u'  '.join(u'%s=%d' % (k, v) for k, v in sorted(per_page.items(), key=lambda kv: -kv[1])))
    print()
    for fam in sorted(byfam, key=lambda f: -sum(byfam[f].values())):
        sub = byfam[fam]
        print(u'── %s：%d 处 / %d 值 ──' % (fam, sum(sub.values()), len(sub)))
        for v, n in sub.most_common(40):
            print(u'   %-30s ×%-4d' % (v, n))
        print()


if __name__ == '__main__':
    main()
